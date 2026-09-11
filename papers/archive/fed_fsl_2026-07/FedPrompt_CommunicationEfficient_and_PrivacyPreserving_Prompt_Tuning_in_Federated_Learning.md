# FedPrompt: Communication-Efficient and Privacy-Preserving Prompt Tuning in Federated Learning 

1<sup>st</sup> Haodong Zhao _Shanghai Jiao Tong University_ Shanghai, China zhaohaodong@sjtu.edu.cn 

2<sup>nd</sup> Wei Du 3<sup>rd</sup> Fangqi Li _Shanghai Jiao Tong University Shanghai Jiao Tong University_ Shanghai, China Shanghai, China dddddw@sjtu.edu.cn solour lfq@sjtu.edu.cn 

4<sup>th</sup> Peixuan Li _Shanghai Jiao Tong University_ Shanghai, China peixuan.li@sjtu.edu.cn 

5<sup>th</sup> Gongshen Liu<sup>_∗_</sup> _Shanghai Jiao Tong University_ Shanghai, China lgshen@sjtu.edu.cn 

**_Abstract_ —Federated learning (FL) has enabled global model training on decentralized data in a privacy-preserving way by aggregating model updates. However, for many natural language processing (NLP) tasks that utilize pre-trained language models (PLMs) with large numbers of parameters, there are considerable communication costs associated with FL. Recently, prompt tuning, which tunes some soft prompts without modifying PLMs, has achieved excellent performance as a new learning paradigm. Therefore we want to combine the two methods and explore the effect of prompt tuning under FL. In this paper, we propose ”FedPrompt” to study prompt tuning in a model split aggregation way using FL, and prove that split aggregation greatly reduces the communication cost, only 0.01% of the PLMs’ parameters, with little decrease on accuracy both on IID and Non-IID data distribution. This improves the efficiency of FL method while also protecting the data privacy in prompt tuning. In addition, like PLMs, prompts are uploaded and downloaded between public platforms and personal users, so we try to figure out whether there is still a backdoor threat using only soft prompts in FL scenarios. We further conduct backdoor attacks by data poisoning on FedPrompt. Our experiments show that normal backdoor attack can not achieve a high attack success rate, proving the robustness of FedPrompt. We hope this work can promote the application of prompt in FL and raise the awareness of the possible security threats.** 

**_Index Terms_ —FL, prompt tuning, PLM, split aggregation** 

## I. INTRODUCTION 

Pre-trained language models [1]–[3] are widely used in many NLP tasks by the fine-tuning paradigm. However, finetuning a PLM with a large number of parameters would be memory-consuming. The reason is that the gradients and optimizer states of all parameters need to be stored. Also the lack of labeled data in fine-tuning phase, as well as few-shot problem, limits the use if this paradigm. When using the pretraining and fine-tuning paradigm in federated learning, the 

* corresponding author. This research work has been sponsored by the Joint Funds of the National Natural Science Foundation of China (Grant No.U21B2020) and Ant Group. 


![](P012_images/P012.pdf-0001-11.png)

### Figure analysis

The figure is a conceptual workflow diagram explaining the prompt-tuning setup used as background for FedPrompt.

- **Input structure:** The top row separates the input into **Soft Prompt** and **Text** regions. The soft prompt is represented by several pale yellow prompt-token boxes, including a **[MASK]** token. The text segment contains the example sentence: “I would highly recommend this.”
- **Model component:** The combined prompt-text input is passed downward into a green box labeled **PLM (Fixed)**, indicating that the pretrained language model parameters are frozen rather than fine-tuned.
- **Prediction output:** The PLM outputs predictions over **Label Words**, shown in a blue box. The visible label words are **great** and **terrible**.
- **Class mapping:** A **Verbalizer** maps label words to the downstream **Class Set**, shown in a pink box. The solid arrow maps **great** to **positive**, while the dashed arrow maps **terrible** to **negative**.
- **Information flow:** Solid and dashed arrows distinguish two example prediction paths from the fixed PLM through label words to final sentiment classes.

Directly observed from the diagram, only the soft prompt portion is depicted as trainable input adaptation, while the PLM is explicitly fixed. The verbalizer provides the bridge between language-model label-word prediction and task-specific class labels. In the surrounding paper context, this figure supports the explanation that prompt tuning reduces trainable parameters by freezing the PLM and optimizing only soft prompts, which motivates the FedPrompt approach for lowering communication cost in federated learning.


Fig. 1. The example of prompt tuning, which consists of soft prompt, text, PLM and verbalizer. 

communication cost is even higher as all parameters of the PLMs provided by each participant need to be aggregated in each round of the training process. Therefore, it is very important and urgent to find ways to improve the efficiency of pre-trained models in federated learning. Recently, prompt tuning [4] has achieved excellent results as a learning paradigm for adapting fixed PLMs to different downstream tasks. As shown in Fig. 1, soft prompt as well as [MASK] token are added to the text as inputs to the model. Among them, soft prompt is used as trainable parameters to be adapted to downstream tasks, [MASK] token is used to predict the label word for the downstream task, and verbalizer is used to map the label word to the real label. All downstream tasks can be uniformly transformed into the form of pre-training tasks of PLMs. Thus, using a fixed PLM and different soft prompts can be applied to different downstream tasks. Also, freezing the parameters of PLM and only tuning the soft prompt significantly reduces the number of training parameters. 

Nowadays, with mobile devices becoming the primary computing devices for many people, a huge amount of data is 

generated and distributed on a wide range of devices. It is an important opportunity and challenge to make full use of these devices and data. Although deep learning has made a lot of progress in many scenarios [5], a data center is required to collect data for training in most cases. Models trained on such data have stronger usability in many intelligent applications, but exchanging and storing sensitive data in a data center carries risks and responsibilities [6]. Previous distributed deep learning methods [7], [8] propose solutions to big data and huge models. However, the computation and communication cost of traditional distributed learning are unacceptable for participants [9], [10]. 

**FL** [11], [12] is an attractive learning method that aims to train a global model over decentralized data while preserving data privacy. In federated learning a subset of clients download a local copy of global model, and compute local model gradients with their local private data in each round. A central server coordinates the distributed clients and only aggregates local model parameters to update the global model, collaborating isolated data islands without raw data exchanging. FL takes multiple rounds of local and global procedures until convergence. Advanced privacy protection methods, e.g., differential privacy (DP), can be further applied for stricter privacy protection. According to above illustration, it seems that using PLM-empowered methods in FL will achieve remarkable performance. For example, [13] propose a news recommendation method to train models using FL. However, when using FL, the model sizes of many existing news recommendation methods are too large to communicate between participants. For example, the base version of BERT [1] models have more than 110M parameters. 

In this paper, we modify prompt tuning in a model split aggregation way using FL, named ”FedPrompt”, where no prior work has been done. First, unlike simple FL methods tune and aggregate full model parameters, FedPrompt only tunes and aggregates some soft prompts for corresponding downstream tasks in FL, and freezes PLMs to decrease communication cost. Second, we are interested in the security of FedPrompt. Prompts are uploaded and downloaded between public platforms and personal users like PLMs, and backdoor attacks are difficult to find for users. We try to get a poisoned global prompt then when the PLMs are loaded with the poisoned prompt, the model will be implanted with the backdoor. 

Experiments carried on various NLP tasks, such as sentiment analysis and sentence-pair classification prove that FedPrompt reduces the communication cost greatly with little decrease on accuracy. Further experiments on backdoor attack show that only by normal methods that poisoning part of training data, the poisoned prompt can not establish a shortcut between the specific trigger word and the target label word. Compared to the method of aggregating and tuning all parameters of huge model, FedPrompt is much more communicationefficient. And compared to prompt tuning without using FL, FedPrompt outperforms in privacy preservation. We also consider other prompt types for a better performance, and using local differential privacy (LDP) to gurantee the privacy. Our 

contributions are summarized as follows: 

- We propose FedPrompt, the new prompt tuning method using FL, freezes PLMs and only aggregates and tunes some soft prompts to decrease communication cost. 

- We conduct extensive experiments on NLP tasks to measure the performance of FedPrompt. Experiments show that FedPrompt can reduce the communication cost greatly with little decrease on accuracy. 

- We further test the model robustness to backdoor attack, and experiment on different hyper-parameter settings, prompt types and LDP to promote the better performance of FedPrompt. 

## II. RELATED WORK 

Prompt tuning first appeared in WARP proposed by [14], after which this method of adding continuous trainable vectors to the input began to be widely studied. Prefix-Tuning [15] adds soft prompt to each layer of the transformer model and applies it to natural language generation (NLG) tasks. P-tuning [16] proposes that some task-related hard prompts can be used as anchors while using soft prompt. Prompt tuning [4] explores the effect of soft prompt on domain adaptation and different model scales. They found that the larger the scale of PLMs, the better the effect of prompt tuning. Recently, P-tuningV2 [17] more finely designs prompt tuning on the basis of the above research. They use a deep soft prompt similar to Prefix-Tuning, and change the verbalizer to a linear classification head, which means that they no longer use the way of mask language model (MLM) to get predictions. They also try to apply prompt tuning to difficult natural language understanding (NLU) tasks (i.e., sequence tagging), such as name entity recognition and semantic role labeling. Moreover, PTR [18] applies logic rules to build templates that are more suitable for text classification tasks, and PPT [19] pre-trains the soft prompt on multiple different tasks to get a better prompt tuning for the downstream tasks. 

FL [11] is a distributed machine learning method that aggregates global model by each local model sharing its parameters (gradients) with the central server after every round of local training on its local data. Proposed FedAvg [11] enables clients to collaboratively train global model without sharing their original data. Various extensions of FedAvg [20]–[24] have been proposed to obtain better performance in communication and deal with heterogeneity. To reduce computation and communication, [25] propose a framework decomposing big recommendation model into a large news model only in server and shared user model. However, though above methods do not share local data directly, naive parameters (gradients) sharing method could lead to privacy leakage of clients [26], [27]. Consequently, several methods are proposed to protect privacy, including differential privacy (DP) [28]– [30] and secure multi-party computation (MPC) [31], [32]. In addition to privacy leakage, many works propose mechanisms to poison FL models in training phase [33], [34] and evasion attacks in inference or testing phase [35], [36]. 


![](P012_images/P012.pdf-0003-00.png)


Fig. 2. Structure of FedPrompt and full PLM fine-tuning using FL. The above one is full PLM fine-tuning using FL, all of the parameters (framed pink nodes) need to be updated. The bottom one is FedPrompt, only soft prompt parameters (framed pink nodes) need to be updated, aggregated (in server) and distributed. 

As none of the above mentioned works study prompt tuning in FL, in this paper, we design a communication-efficient prompt tuning method in FL and design backdoor attack to detect its vulnerability. 

## III. METHOD 

## _A. Preliminaries_ 

In FL setting, suppose there are _K_ clients, each client hosts a private dataset _Dk_ = _{_ ( _xk, yk_ ) _}_ owning _nk_ samples. We use _θt_ and _θt_<sup>_k_todenotetheglobalmodeland</sup><sup>_kth_localmodel</sup> parameters in communication round _t_ respectively. Based on FedAvg [11], the aggregation process is computed as follows: 


![](P012_images/P012.pdf-0003-06.png)


where _n_ = _|D|_ =<sup>�</sup><sup>_K_</sup> _k_ =1<sup>_nk_isthetotalnumofglobal</sup> combined data and _D_ ≜<sup>�</sup> _k∈_ [ _K_ ]<sup>_Dk_istheglobalcombined</sup> dataset. If data distributions are IID (Independent Identically Distribution), all clients have the same number of samples, then _nk/n_ could be replaced by 1 _/K_ . 

In a text classification task, _xk_ are the inputs and _yk_ are corresponding class labels. Each _x_<sup>(</sup><sup>_i_)</sup> _∈ xk_ consists of tokens _x_<sup>(</sup><sup>_i_)</sup> = _{x_<sup>(</sup> 1<sup>_i_)</sup><sup>_, x_(</sup> 2<sup>_i_)</sup><sup>_, · · ·, x_</sup> _l_<sup>(</sup><sup>_i_)</sup><sup>_}_,where</sup><sup>_l_isthelengthofsingle</sup> input. The prompt tuning structure is composed of the soft prompt **p** , the template _T_ ( _·_ ), the verbalizer _V_ ( _·_ ) and the PLM 

_M_ ( _·_ ). Soft prompt **p** consists of tokens **p** = _{p_ 1 _, p_ 2 _, · · · , pm}_ , whose parameters are trainable. _m_ is the number of the soft prompt tokens. _T_ ( _·_ ) is a function to define where tokens of _x_<sup>(</sup><sup>_i_)</sup> and **p** are placed. After applying _T_ ( _·_ ), we obtain _x_<sup>(</sup> _prompt_<sup>_i_)=</sup><sup>_T_(</sup><sup>_x_(</sup><sup>_i_)</sup><sup>_,_</sup><sup>**p**).Atleastone[MASK]tokenisplaced</sup> into the _x_<sup>(</sup> _prompt_<sup>_i_)for</sup><sup>_M_(</sup><sup>_·_)topredictthelabelword.</sup> ˆ<sup>_V_(</sup><sup>_·_)is</sup> a map function to map the label word to the class _y_ = _V_ ( _w_ ). Usually, each class can have one or more label words. We call _T_ a multi-word verbalizer when each class has more than one label word, such as _{_ positive: good, great; negative: bad, terrible; _}_ . Input _x_<sup>(</sup> _prompt_<sup>_i_)to</sup><sup>_M_,wecanobtaintheencoded</sup> feature [MASK]. By a softmax function, we can compute the probability that the label word _w_ can fill the masked position. The label word with the highest probability is the predict wordˆ _w_ = _M_ ( _x_<sup>(</sup> _prompt_<sup>_i_))andthepredictclasscanbe</sup> obtained by _y_ = _V_ ( _w_ ). We rewrite the prompt tuning process ˆ as _y_<sup>(</sup><sup>_i_)</sup> = _f_ ( _x_<sup>(</sup><sup>_i_)</sup> _,_ **p** _, θ_ ), 

## _B. FedPrompt_ 

As mentioned before, in normal prompt tuning the whole is splitted into four parts, and only PLM (using fine-tuning) and soft prompt have trainable parameters. We use _F_ and _P_ to denote their parameters respectively, then the global model parameters in round _t_ can be denoted as: 


![](P012_images/P012.pdf-0003-12.png)

### Figure analysis

The figure is a schematic comparison between two federated learning workflows for pretrained language models: full PLM fine-tuning using FL and the proposed FedPrompt method.

**Upper panel: full PLM fine-tuning using FL**

- Labeled components include `Client data`, `Raw PLM model`, `Updated local model`, `Aggregation`, `Updated global model`, and `Server`.
- Multiple clients are shown as `Client 1` through `Client n`, indicating a standard federated setup with many participants.
- Each client uses local data to train a raw PLM model into an updated local model.
- The updated local models are sent to an aggregation block on the server side.
- The aggregated result becomes the updated global model, which is then distributed back to clients, shown by the dashed blue communication path.
- Direct visual observation: the updated local model and updated global model contain many pink-framed nodes, matching the caption’s statement that all PLM parameters are updated in full fine-tuning.

**Lower panel: FedPrompt**

- Labeled components include `Client data`, `Prompt Inserted PLM model`, `Updated local model (Only prompt updated)`, `Aggregation`, `Updated global model (Only prompt shared and updated)`, and `Server`.
- The same multi-client structure is shown, again from `Client 1` to `Client n`.
- Each client inserts prompts into the PLM and performs local training, but only a small prompt-related portion is highlighted as updated.
- The aggregation block receives only the prompt parameters, rather than the entire PLM parameter set.
- The updated global model on the server contains mostly unchanged model parameters with only the prompt-related pink nodes updated.
- Direct visual observation: compared with the upper panel, the lower panel highlights far fewer pink-framed nodes, representing a much smaller trainable and communicated parameter subset.

**Relationship and information flow**

- Both panels follow the same FL loop: clients train locally, send updates to the server, the server aggregates updates, and the global update is redistributed.
- The key difference is the scope of trainable and shared parameters.
- In full PLM fine-tuning, the whole model is locally updated and aggregated.
- In FedPrompt, the PLM backbone is effectively fixed while soft prompt parameters are updated, aggregated, and redistributed.

**Connection to the surrounding text**

- The surrounding method section introduces federated learning, FedAvg-style aggregation, and prompt tuning with soft prompt parameters.
- The figure visually motivates the FedPrompt formulation described nearby, where the model parameters are decomposed into PLM parameters and soft prompt parameters.
- The diagram supports the paper’s claim that FedPrompt is communication-efficient because clients and the server exchange only the soft prompt parameters rather than all parameters of a large pretrained language model.

**Interpretation**

- The figure implies that FedPrompt can substantially reduce communication and update cost in federated PLM adaptation, since the shared parameter payload is limited to the prompt component.
- It also clarifies why the method may have different privacy or attack surfaces from conventional FL fine-tuning: only prompt parameters are exposed to aggregation, while the PLM backbone remains fixed.


**Algorithm 1** FedPrompt Algorithm 

**Input** : _K_ clients indexed by _k_ , client fraction _C_ , _T_ communication rounds indexed by t, local minibatch size _B_ , local epochs _E_ , learning rate _η_ , PLM parameters _F_ , soft prompts parameters _P_ . 

**Server executes:** 

- 1: Initialize global model. 

- 2: Distribute _F_ (fixed during the process) to all clients. 

- 3: **for** _t ∈{_ 1 _, · · · , T }_ **do** 

- 4: _Ut ←_ Select a subset of _C · K_ clients at random 


![](P012_images/P012.pdf-0004-07.png)


11: **end for** 

- 12: **return** _Pt_ +1 

**ClientUpdate(** _k_ **,** _P_ **):** // _Run on client k_ 

13: _B ←_ (split _Dk_ into batches of size _B_ ) 

14: **for** each local epoch _i ∈{_ 1 _, · · · , E}_ **do** 15: **for** batch _b ∈B_ **do** 16: _P ← P − η∇l_ ( _P_ ; _b_ ) 17: **end for** 

18: **end for** 

19: **return** _P_ 

In FedPrompt, we fix _Ft_ to learn a set of _θ_ over _D_ with the objective to solve: 


![](P012_images/P012.pdf-0004-16.png)


where _Lk_ ( _P_ ) is the empirical loss of client _k_ : 


![](P012_images/P012.pdf-0004-18.png)


In the beginning, the server initializes the whole model, then distributes it to each client. At the beginning of round _t_ , the server selects clients by fraction _C_ to participate in this round, distributes the global soft prompt parameters _Pt_ to them, and each selected client _k_ replace the local _Pt_<sup>_k_</sup> _−_ 1<sup>with</sup> _Pt_ , which means _Pt_<sup>_k_=</sup><sup>_Pt_.AsPLMisfixed,</sup><sup>_F k_</sup> _t_<sup>=</sup><sup>_F k_</sup> _t−_ 1<sup>.</sup> Then each client conducts local training with optimizer only for _Pt_<sup>_k_,getsitsupdatedsoftpromptparameters</sup><sup>_P k_</sup> _t_<sup>andsends</sup> them back to the server in parallel. The local training is same as normal prompt tuning process. Finally, the server performs the aggregation as follows: 


![](P012_images/P012.pdf-0004-20.png)


where _Nt_ =<sup>�</sup><sup>_⌈_</sup> _k_<sup>_C_</sup> =1<sup>_·K⌉_</sup> _nk_ is participated data amount in round _t_ . The whole process is shown as Algorithm 1. Except for 

prompt tuning, there are also other prompt methods such as P- tuning [16] and Prefix-Tuning [15]. We also design FedPrompt for these prompt models in a similar way. 

## _C. Poison FedPrompt_ 

In FL, as clients privacy is highly protected and server have access to little information about client, it is widely acknowledged that multiple malicious clients possibly participate in training [34]. On the one hand, after initialization, each client has full knowledge of the model structure and parameters. On the other hand, it has been proved that prompt tuning is vulnerable to backdoor attack by poisoning training data [37]. Therefore, it is important to verify the robustness to backdoor attack of FedPrompt, and we call this attack as _FedPPT_ . 

Considering the situation that attacker has full control of one or more clients, and only modifies the local training data, which in fact is much less than attacker’s access. The goal of attacker is to inject backdoor into poisoned prompt, which may be released to public. When victims use poisoned prompt, for clean samples, the victim PLMs will still give the correct label word; for poisoned samples which are added with the trigger word, the victim PLMs will output the target label word. To poison FedPrompt, firstly, modify the training dataset. Attacker tries to establish a shortcut between the trigger ∆ and target label _lt_ . We define the poison function as _P_ ( _·_ ), then we have single poisoned data ( _x_<sup>(</sup> _p_<sup>_i_)</sup><sup>_, t_) =</sup><sup>_P_(</sup><sup>_x_(</sup><sup>_i_)</sup><sup>_,_∆</sup><sup>_, l_</sup> _t_<sup>), where modified</sup> target _t_ = _y_ ( _x_<sup>(</sup><sup>_i_)</sup> ). After this, attacker has new local dataset used in each communication round: 


![](P012_images/P012.pdf-0004-26.png)



![](P012_images/P012.pdf-0004-27.png)


where _λ_ is the poison rate. Secondly, using modified _D_<sup>ˆ</sup> _k_ to update parameters _Pk_ . Then the objective function of malicious client _k_ as follows: 


![](P012_images/P012.pdf-0004-29.png)



![](P012_images/P012.pdf-0004-30.png)


As no prior work on prompt tuning using FL has been done before, we investigate our methods on several federated NLP tasks including sentiment analysis and sentence-pair classification, where prompt tuning is suitable and often used. Also we conduct backdoor attack on these tasks to evaluate the robustness. All experiments are done on a server with 8 Nvidia Geforce GTX 1080Ti GPUs with 11GB RAM each, 12 Intel Xeon CPUs Processor, and CentOS release 7.9 OS. Our models are built using PyTorch framework<sup>1</sup> . 

1https://pytorch.org/ 

## _A. Experimental Setup_ 

- _1) Dataset:_ To evaluate FedPrompt model, our experiments 

- are conducted on several NLP tasks: 

- Text bi-classification tasks including sentiment analysis, toxicity detection and spam detection. For sentiment analysis, we use the Stanford Sentiment Treebank (SST2)<sup>2</sup> and IMDB<sup>2</sup> . We use the OffensEval [38] and the Twitter [39] in toxicity detection. And for spam detection, we use the Enron [40], and the Lingspam [41]. 

- Sentence-pair classification tasks. For this inference task, we use Question Natural Language Inference (QNLI) [42] and Recognizing Textual Entailment (RTE)<sup>2</sup> dataset. 

To conduct experiments in FL setting, we divide all these datasets above into ten clients. In IID setting, we randomly divide the whole dataset into ten equal parts and each client has one part. In Non-IID setting, as all the tasks only having two labels _{_ 0,1 _}_ , we bring non-I.I.D.ness by different data quantity. We split all the data using Dirichlet distribution parameterized by _α_ as in prior works [43]. Since labels are not available in the test sets for some datasets, we use the validation set as the test set and split a part of the training set as the validation set. 

_2) Model and Training Details:_ Among various PLMs, we select the most representative and widely used pre-trained language models, including the base versions of BERT [1], Roberta [2] and Google T5 [3] to conduct experiments. We use the Adam optimizer for training of BERT and Roberta, and the Adafactor optimizer for Google T5. In main experiments, we use a one-to-one verbalizer and a simple text classification template ”[text] is [MASK].” having 20 soft prompt tokens in the head. Following the setup of [4], we set the learning rate to be 0.3. Following the setup of [44], we assume that we have a server and _K_ = 10 available clients. We use a FedAvg system to implement the FL setting. Specifically, all clients are involved in the averaging of model parameters in every aggregation round. The number of max local step is set to 1000, compared to 30,000 in [4]. The number of communication rounds is set to 20, compared to 100 in [44] and [34], to prove our low-communication-cost and convergence-quick method. 

_3) Baseline Algorithm:_ To make a fair and reasonable comparison with our proposed FedPrompt, we choose the most related work [45], studying full-parameter fine-tuning, as FL baseline. Due to full-parameter fine-tuning requires lots of calculations, we only reproduce their method with above FL setting on IID SST-2 task as shown in Table II. 

_4) Metric:_ Communication bottleneck is a big challenge for many big models in FL, we use the amount of communicated parameters to evaluate our communication cost. As for the evaluation of performance, we use accuracy ( _ACC_ ) which represents the proportion of the clean samples correctly classified by the model to measure the performance of the model on benign task. Also we use Attack Success Rate ( _ASR_ ) to evaluate the attacking performance, which represents the 

proportion of the poisoned samples we successfully enable the model to misclassify as the target class. 

## _B. Main Results_ 

In FedPrompt the learnable parameters is the same as communication cost. As shown in Table II, FedPrompt condenses the communication cost to nearly 0.01% of the full-parameter fine-tuning parameters, greatly reduces the communication cost, with only about 1% decrease in accuracy, making many devices applicable for some scenarios with communication and storage constraints, and the private data on these devices can contribute to the convergence of the global model. Also this property promotes the design and development of personalized FL model, especially for those resource-constrained devices. 

The main results of FedPrompt performance with clean IID and Non-IID data distribution are summarized in Table I. As shown in Fig. 3, using FedPrompt to protect data privacy and handle the problem of few-shot demonstrate has little decrease on accuracy in most cases compared to prompt tuning without FL. Specifically, FL plays a remarkable effect with prompt tuning, only a few local training steps and communication rounds can contribute to a well-performed global model. For most tasks, FedPrompt achieves more than 90% _ACC_ on clean data, and there is only a little decrease, almost less than 3%, with Non-IID data distribution than IID data distribution. Non-IID is a key challenge for the effectiveness of FL, and our proposed FedPrompt proves its compatibility on nonIID datasets. We think the FL paradigm and few-parameter soft prompt . We find that experiments on RTE task have a weaker result than other tasks. Considering that RTE only have 2240 training samples in total, which is the least among all tasks, and after splitting to ten clients each client only have a few samples to train soft prompt, we assume the weaker performance because of lack of data. Also RTE may need a better customized template to be used in prompt tuning. 

As shown in Table III, we evaluate the effect of backdoor attack on all tasks and models with IID and Non-IID data distribution. Nearly all tasks get _ACC_ on posion dataset drop less than 2% compared to on clean dataset in Table I. Even some tasks show a better _ACC_ after poison. We think this is because poisoning the original dataset can be considered as data augmentation, and attacking has the similar effect to adversarial training. After backdoor attack, with poison ratio at 10% (all training data poisoned on 10% clients selected), all experiments on different tasks and models do not show a obvious rise in _ASR_ , which suggests that FedPrompt has robustness to backdoor attack. We think this is because aggregation process offsets the backdoor. 

## _C. Communication Rounds_ 

Fig. 4 and Fig. 5 show the local and global _ACC_ and _ASR_ in each round during training. As for _ACC_ , the training process of different settings is similar, and there is not a obvious decrease in Non-IID setting. The _ACC_ of local model in the first round have a rapid rise and pass it to the global model only in one single communication round. This proves that our proposed 

2https://huggingface.co/datasets/ 

TABLE I 

_ACC (%)_ AND _ASR (%)_ OF FEDPROMPT WITH CLEAN IID AND NON-IID DATA DISTRIBUTION. 

|Dataset|II|BER<br>D|T<br>Non-|IID|II|ROB<br>D|ERTA<br>Non|-IID|II|T<br>D|5<br>Non|-IID|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||_ACC_|_ASR_|_ACC_|_ASR_|_ACC_|_ASR_|_ACC_|_ASR_|_ACC_|_ASR_|_ACC_|_ASR_|
|SST-2<br>IMDB|**90.16**<br>**91.08**|12.42<br>12.66|89.45<br>89.26|16.36<br>11.42|**92.43**<br>**92.80**|10.28<br>9.15|92.23<br>92.53|7.48<br>7.66|**92.69**<br>**92.89**|9.58<br>9.69|92.32<br>91.24|6.31<br>11.33|
|OffensEval<br>Twitter|**82.64**<br>**94.02**|9.84<br>4.96|80.47<br>93.82|8.55<br>3.05|**81.05**<br>**94.39**|13.87<br>4.61|80.34<br>93.64|5.98<br>5.41|**79.30**<br>**93.35**|12.58<br>3.86|78.83<br>92.80|10.65<br>4.21|
|Enron<br>Lingspam|**97.60**<br>**97.47**|3.20<br>0.00|97.43<br>96.89|4.02<br>0.00|**97.85**<br>**97.43**|2.27<br>0.00|97.30<br>96.47|7.34<br>0.00|**97.22**<br>**97.07**|6.73<br>0.00|96.95<br>96.21|5.87<br>0.41|
|QNLI<br>RTE|**83.36**<br>**54.87**|28.35<br>35.21|82.25<br>54.15|30.46<br>42.73|**86.44**<br>**60.32**|14.81<br>36.99|85.43<br>57.51|12.10<br>44.52|**89.06**<br>**76.51**|10.87<br>22.95|84.48<br>73.64|12.44<br>22.60|
||||<br>|||<br>|<br>|<br>|||||
|<br> <br> <br> <br> <br>  <br>|||<br> <br> <br> <br> <br>  <br>|||||<br>|<br> <br> <br> <br> <br>  <br>||||
|**S S T - 2**<br>**I M**<br>**D B**<br>**O f f e n s E v a l**<br>**T w i t t e r**<br>**E n r o **<br>**L i **|**n**<br>**n g s p a m**<br>**Q N L **|**I**<br>**R T E**|**S S T**|**- 2**<br>**I M**<br>**D B**<br>**O f f e n s**|**E v a l**<br>**T w i t t e r**|<br>**E n r o n**<br>**L i n g s p a**|**m**<br>**Q N L I**<br>**R**|**T E**|**S S T - 2**<br>**I**|**M**<br>**D B**<br>**O f f e n s E v **|**a l**<br>**T w i t t e r**<br>**E n **<br>|**r o n**<br>**L i n g s p a m**<br>**Q N L I**<br>**R T E**|




![](P012_images/P012.pdf-0006-03.png)


Fig. 3. The performance of prompt tuning without FL and FedPrompt. When using FL, there are IID setting and Non-IID setting on data distribution. The PLM used are BERT (the left), ROBERTA (the middle) and T5 (the right). 

TABLE II 

THE MAIN RESULTS OF FEDPROMPT AND FULL-PARAMETER FINE-TUNING ON IID SST-2 TASK. FOR THE SAME MODEL, WE REGARD THE PARAMETER QUANTITY IN FINE-TUNING AS 100.000%. 

|Model|FL Method|_ACC_|Comm. Cost|Ratio|
|---|---|---|---|---|
|BERT|FedPrompt|90.16|**0.016M**|**0.014%**|
||Fine-tuning|91.02|109.530M|100.000%|
|ROBERTA|FedPrompt|92.43|**0.016M**|**0.013%**|
||Fine-tuning|93.57|124.714M|100.000%|
|T5|FedPrompt|92.69|**0.015M**|**0.007%**|
||Fine-tuning|93.79|222.919M|100.000%|




![](P012_images/P012.pdf-0006-08.png)


Fig. 5. Local and global _ACC (%)_ and _ASR (%)_ with communication rounds on SST-2 task using BERT. The results are using FedPPT with IID setting and only one fixed client in ten clients is malicious. The benign client is selected randomly. 


![](P012_images/P012.pdf-0006-10.png)


Fig. 4. Local and global _ACC (%)_ with communication rounds on SST-2 task using BERT. The left one is using IID setting and the right one is using Non-IID setting, the two clients are selected randomly. 

FedPrompt fits the poor data dependent prompt tuning well. As for _ASR_ , we can see that _ASR_ on the malicious client reaches 

100% only after one single local training round, but after aggregation, _ASR_ on benign client and global model remains a low level. We also find _ASR_ on benign client is close to global model in the previous round, consistent with the aggregation method. 

## _D. Number of Local Iterations_ 

We study the effects of number of local iterations in each round. As we mentioned before, FedPrompt has relatively few trainable parameters that too many local iterations may lead to local over-fitting in FL while inadequate local iterations slow down the convergence. We conduct experiments on 100, 500, 1000 and 1500 local iterations, all of which are relatively small. As shown in Fig. 6, 100 and 500 local iterations performs worse and 1500 iterations may lead to local over- 

### TABLE III 

_ACC (%)_ AND _ASR (%)_ OF FEDPROMPT WITH POISONED IID AND NON-IID DATA DISTRIBUTION. _↑_ MEANS HIGHER THAN CLEAN DATA. 

|||BERT|||ROB|ERTA||T|5||
|---|---|---|---|---|---|---|---|---|---|---|
|Dataset|II|D<br>Non-|IID|I|ID|No|n-IID|IID|Non-|IID|
||_ACC_|_ASR_<br>_ACC_|_ASR_|_ACC_|_ASR_|_ACC_|_ASR_|_ACC_<br>_ASR_|_ACC_|_ASR_|
|SST-2<br>IMDB|**89.11**<br>**90.14**|13.30<br>88.76<br>14.36<br>89.12|14.60<br>11.69|91.55<br>**92.46**|11.55<br>9.05|**92.12**<br>91.53|9.73<br>10.78|**92.20**<br>8.74<br>**91.88**<br>9.54|91.51<br>90.86|9.07<br>13.87|
|OffensEval<br>Twitter|**80.93**<br>**94.10**_↑_|10.13<br>80.11<br>6.01<br>93.42|9.94<br>7.71|**79.65**<br>**94.15**_↑_|17.26<br>4.02|78.95<br>93.22|7.23<br>4.76|**78.72**<br>15.97<br>**93.25**<br>5.28|77.74<br>92.98_↑_|15.06<br>4.13|
|Enron<br>Lingspam|97.37<br>**97.11**|4.20<br>**98.18**_↑_<br>4.03<br>96.02|4.87<br>3.98|**98.03**_↑_<br>**95.89**|3.53<br>5.77|97.16<br>95.71|8.20<br>4.79|**97.88**_↑_<br>8.13<br>**96.83**<br>4.26|97.12_↑_<br>95.66|6.80<br>4.14|
|QNLI<br>RTE|**84.48**_↑_<br>54.51|29.44<br>82.07<br>31.23<br>**60.29**_↑_|27.22<br>39.21|**86.92**_↑_<br>55.60|18.82<br>32.08|85.30<br>**55.96**|8.33<br>39.18|**85.56**<br>9.15<br>**76.43**<br>20.82|84.33<br>73.29|14.26<br>25.41|
|<br> <br> <br> <br>||<br> <br> <br> <br>  <br>||||||<br> <br> <br> <br>|||
||<br>|<br> <br>   <br>          <br>||<br>|<br>|<br>       <br>|<br>|<br>|<br>|<br> <br>|



Fig. 6. Global _ACC (%)_ results with different local iterations on SST-2 task. 

TABLE IV 

GLOBAL _ACC (%)_ RESULTS WITH DIFFERENT NUMBER OF SOFT TOKENS ON SST-2 TASK. 

|Token Num|1<br>5|10|20|
|---|---|---|---|
|_ACC_|87.11<br>89.28|89.62|90.16|



## _E. Number of Soft Tokens_ 

We tested the results under different numbers of soft tokens settings, and the results are consistent with those of prompt tuning under non-federal learning. As shown in Table IV, using more soft tokens will lead to better results. However, it also increases the communication cost under FL. 

TABLE V 

GLOBAL _ACC (%)_ RESULTS WITH AND WITHOUT LDP ON SST-2 TASK. 

|Method|BERT|ROBERTA|T5|
|---|---|---|---|
|FedPrompt w/o LDP|90.16|92.43|92.69|
|FedPrompt w/ LDP|85.73|86.88|86.14|



TABLE VI 

GLOBAL _ACC (%)_ AND COMMUNICATION COST (M, MILLION) WITH DIFFERENT PROMPT METHODS. DENOTE PROMPT TUNING AS METHOD _α_ , P-TUNING AS _β_ AND PREFIX-TUNING AS _γ_ . 

|Method|B<br>_ACC_|ERT<br>Comm.|ROB<br>_ACC_|ERTA<br>Comm.|T<br>_ACC_|5<br>Comm.|
|---|---|---|---|---|---|---|
|_α_|90.16|0.016|92.43|0.016|92.69|0.015|
|_β_|90.99|25.420|93.27|25.420|93.35|25.420|
|_γ_|-|-|-|-|76.85|9.853|



fitting, which are harmful to obtain a excellent global model. Additional experiments expanded to 50 rounds suggest the performance of 100 and 500 local iterations still below others, while the other two could not get a further promotion. 

## _F. FedPrompt with LDP_ 

As we mentioned before, there are hidden dangers to infer the origin private data by inverting gradients in FL, and LDP is an effective way to defense this attack. Also [46] has proved that the noise for larger model can damage the accuracy in differentially FL, so in Fedprompt the tiny prompt contributes to the use of LDP for privacy. We test on SST-2, clipping the gradients and then adding LaPlace noise on parameters. Table V shows that LDP protects the privacy with the cost of accuracy decreased by about 5%. 

## _G. Prompt methods_ 

We also experiment on P-tuning and Prefix-Tuning (only supports T5 now<sup>3</sup> ). Our experiments on SST-2 are shown in Table VI. It suggests that among the three prompt methods prompt tuning gets the best performance combining _ACC_ and communication cost. P-tuning has the best _ACC_ performance but quite a lot parameters, and Prefix-Tuning needs more to use. 

3https://github.com/thunlp/OpenPrompt 

## V. FURTHER IMPROVEMENT 

Though FedPrompt is robust to normal backdoor attack in our experiments, there are still special methods to backdoor FL. We plan to let the server check the mean and standard deviation of soft prompt parameters from each client, and find outliers to refuse before global aggregation. Adding noise after aggregation could also destroy the backdoor, with partial sacrifice on _ACC_ . We will carry on this research next. 

## VI. CONCLUSION 

In this work, we propose FedPrompt to use federated prompt tuning on decentralized data in a communication-efficient and privacy preserving way. We employ a split aggregation way that freezing extensive PLMs’ parameters and only tuning and aggregating soft prompts. In this way we condense the communication cost to only 0.01% compared to full-parameter fine-tuning, making many devices applicable for some scenarios with communication constraints. Experiments on both IID and Non-IID data distribution using three mainstream model demonstrate the accuracy of FedPrompt. We also use LDP to further protect the privacy, and it is necessary to further study the FL backdoor attack. 

## REFERENCES 

- [1] J. Devlin, M. Chang, K. Lee, and K. Toutanova, “BERT: pre-training of deep bidirectional transformers for language understanding,” in _NAACLHLT_ , 2019, pp. 4171–4186. 

- [2] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov, “Roberta: A robustly optimized BERT pretraining approach,” p. arXiv:1907.11692, 2019. 

- [3] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu, “Exploring the limits of transfer learning with a unified text-to-text transformer,” _J. Mach. Learn. Res._ , vol. 21, pp. 140:1–140:67, 2020. 

- [4] B. Lester, R. Al-Rfou, and N. Constant, “The power of scale for parameter-efficient prompt tuning,” in _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing_ , 2021, pp. 3045–3059. 

- [5] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition_ . IEEE Computer Society, 2016, pp. 770–778. 

- [6] Z. Wu, Y. Zhou, D. Wu, M. Chen, and Y. Xu, “TAMF: towards personalized time-aware recommendation for over-the-top videos,” in _Proceedings of the ACM Workshop on Network and Operating Systems Support for Digital Audio and Video_ , 2019, pp. 43–48. 

- [7] J. Dean, G. Corrado, R. Monga, K. Chen, M. Devin, Q. V. Le, M. Z. Mao, M. Ranzato, A. W. Senior, P. A. Tucker, K. Yang, and A. Y. Ng, “Large scale distributed deep networks,” in _Advances in Neural Information Processing Systems_ , 2012, pp. 1232–1240. 

- [8] M. Li, L. Zhou, Z. Yang, A. Q. Li, F. Xia, D. G. Andersen, and A. Smola, “Parameter server for distributed machine learning,” 2013. 

- [9] A. Reisizadeh, A. Mokhtari, H. Hassani, A. Jadbabaie, and R. Pedarsani, “Fedpaq: A communication-efficient federated learning method with periodic averaging and quantization,” in _Artificial Intelligence and Statistics_ . PMLR, 2020, pp. 2021–2031. 

- [10] J. Hamer, M. Mohri, and A. T. Suresh, “Fedboost: A communicationefficient algorithm for federated learning,” in _Proceedings of the International Conference on Machine Learning_ . PMLR, 2020, pp. 3973–3983. 

- [11] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in _Artificial Intelligence and Statistics_ . PMLR, 2017, pp. 1273– 1282. 

- [12] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” _ACM Trans. Intell. Syst. Technol._ , vol. 10, no. 2, pp. 12:1–12:19, 2019. 

- [13] T. Qi, F. Wu, C. Wu, Y. Huang, and X. Xie, “Privacy-preserving news recommendation model learning,” in _Findings of the Association for Computational Linguistics: EMNLP_ , 2020, pp. 1423–1432. 

- [14] K. Hambardzumyan, H. Khachatrian, and J. May, “WARP: word-level adversarial reprogramming,” in _ACL/IJCNLP_ , 2021, pp. 4921–4933. 

- [15] X. L. Li and P. Liang, “Prefix-tuning: Optimizing continuous prompts for generation,” in _ACL/IJCNLP_ , 2021, pp. 4582–4597. 

- [16] X. Liu, Y. Zheng, Z. Du, M. Ding, Y. Qian, Z. Yang, and J. Tang, “Gpt understands, too,” p. arXiv:2103.10385, 2021. 

- [17] X. Liu, K. Ji, Y. Fu, Z. Du, Z. Yang, and J. Tang, “P-tuning v2: Prompt tuning can be comparable to fine-tuning universally across scales and tasks,” p. arXiv:2110.07602, 2021. 

- [18] X. Han, W. Zhao, N. Ding, Z. Liu, and M. Sun, “Ptr: Prompt tuning with rules for text classification,” p. arXiv:2105.11259, 2021. 

- [19] Y. Gu, X. Han, Z. Liu, and M. Huang, “PPT: pre-trained prompt tuning for few-shot learning,” in _Proceedings of the Annual Meeting of the Association for Computational Linguistics_ , 2022, pp. 8410–8423. 

- [20] T. Li, A. K. Sahu, M. Zaheer, M. Sanjabi, A. Talwalkar, and V. Smith, “Federated optimization in heterogeneous networks,” in _Proceedings of Machine Learning and Systems_ , 2020. 

- [21] S. P. Karimireddy, S. Kale, M. Mohri, S. J. Reddi, S. U. Stich, and A. T. Suresh, “SCAFFOLD: stochastic controlled averaging for federated learning,” in _Proceedings of the International Conference on Machine Learning_ . PMLR, 2020, pp. 5132–5143. 

- [22] A. Fallah, A. Mokhtari, and A. E. Ozdaglar, “Personalized federated learning with theoretical guarantees: A model-agnostic meta-learning approach,” in _Advances in Neural Information Processing System_ , 2020. 

- [23] D. A. E. Acar, Y. Zhao, R. M. Navarro, M. Mattina, P. N. Whatmough, and V. Saligrama, “Federated learning based on dynamic regularization,” in _International Conference on Learning Representations_ , 2021. 

- [24] X. Li and D. Zhan, “Fedrs: Federated learning with restricted softmax for label distribution non-iid data,” in _KDD ’21: The ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ , 2021, pp. 995– 1005. 

- [25] J. Yi, F. Wu, C. Wu, R. Liu, G. Sun, and X. Xie, “Efficient-fedrec: Efficient federated learning framework for privacy-preserving news recommendation,” in _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ , 2021, pp. 2814–2824. 

- [26] L. Melis, C. Song, E. D. Cristofaro, and V. Shmatikov, “Exploiting unintended feature leakage in collaborative learning,” in _IEEE Symposium on Security and Privacy_ . IEEE, 2019, pp. 691–706. 

- [27] J. Geiping, H. Bauermeister, H. Dr¨oge, and M. Moeller, “Inverting gradients - how easy is it to break privacy in federated learning?” in _Advances in Neural Information Processing System_ , 2020. 

- [28] M. Abadi, A. Chu, I. J. Goodfellow, H. B. McMahan, I. Mironov, K. Talwar, and L. Zhang, “Deep learning with differential privacy,” in _Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Securit_ , 2016, pp. 308–318. 

- [29] R. C. Geyer, T. Klein, and M. Nabi, “Differentially Private Federated Learning: A Client Level Perspective,” p. arXiv:1712.07557, Dec. 2017. 

- [30] A. Triastcyn and B. Faltings, “Federated learning with bayesian differential privacy,” in _IEEE International Conference on Big Data (IEEE BigData)_ . IEEE, 2019, pp. 2587–2596. 

- [31] K. A. Bonawitz, V. Ivanov, B. Kreuter, A. Marcedone, H. B. McMahan, S. Patel, D. Ramage, A. Segal, and K. Seth, “Practical secure aggregation for privacy-preserving machine learning,” in _Proceedings of the ACM SIGSAC Conference on Computer and Communications Security_ , 2017, pp. 1175–1191. 

- [32] H. B. McMahan, D. Ramage, K. Talwar, and L. Zhang, “Learning differentially private recurrent language models,” in _International Conference on Learning Representations_ , 2018. 

- [33] M. Jere, T. Farnan, and F. Koushanfar, “A taxonomy of attacks on federated learning,” _IEEE Secur. Priv._ , vol. 19, no. 2, pp. 20–28, 2021. 

- [34] E. Bagdasaryan, A. Veit, Y. Hua, D. Estrin, and V. Shmatikov, “How to backdoor federated learning,” in _Artificial Intelligence and Statistics_ . PMLR, 2020, pp. 2938–2948. 

- [35] X. Yuan, P. He, Q. Zhu, and X. Li, “Adversarial examples: Attacks and defenses for deep learning,” _IEEE Trans. Neural Networks Learn. Syst._ , vol. 30, no. 9, pp. 2805–2824, 2019. 

- [36] A. Aldahdooh, W. Hamidouche, S. A. Fezza, and O. D´eforges, “Adversarial example detection for DNN models: a review and experimental comparison,” _Artif. Intell. Rev._ , vol. 55, no. 6, pp. 4403–4462, 2022. 

- [37] W. Du, Y. Zhao, B. Li, G. Liu, and S. Wang, “Ppt: Backdoor attacks on pre-trained models via poisoned prompt tuning,” in _IJCAI-22_ , 2022, pp. 680–686. 

- [38] M. Zampieri, S. Malmasi, P. Nakov, S. Rosenthal, N. Farra, and R. Kumar, “Semeval-2019 task 6: Identifying and categorizing offensive language in social media (offenseval),” in _Proceedings of the 13th International Workshop on Semantic Evaluation, SemEval@NAACLHLT 2019_ , 2019, pp. 75–86. 

- [39] A. Founta, C. Djouvas, D. Chatzakou, I. Leontiadis, J. Blackburn, G. Stringhini, A. Vakali, M. Sirivianos, and N. Kourtellis, “Large scale crowdsourcing and characterization of twitter abusive behavior,” in _Proceedings of the Twelfth International Conference on Web and Social Media_ , 2018, pp. 491–500. 

- [40] V. Metsis, I. Androutsopoulos, and G. Paliouras, “Spam filtering with naive bayes - which naive bayes?” in _CEAS_ , 2006. 

- [41] G. Sakkis, I. Androutsopoulos, G. Paliouras, V. Karkaletsis, C. D. Spyropoulos, and P. Stamatopoulos, “A memory-based approach to antispam filtering for mailing lists,” _Inf. Retr._ , vol. 6, no. 1, pp. 49–73, 2003. 

- [42] P. Rajpurkar, J. Zhang, K. Lopyrev, and P. Liang, “Squad: 100, 000+ questions for machine comprehension of text,” in _Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing_ , 2016, pp. 2383–2392. 

- [43] C. He, E. Ceyani, K. Balasubramanian, M. Annavaram, and S. Avestimehr, “Spreadgnn: Decentralized multi-task federated learning for graph neural networks on molecular data,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2022, pp. 6865–6873. 

- [44] Q. Li, B. He, and D. Song, “Model-contrastive federated learning,” in _IEEE Conference on Computer Vision and Pattern Recognition_ , 2021, pp. 10 713–10 722. 

- [45] A. Hilmkil, S. Callh, M. Barbieri, L. R. S¨utfeld, E. L. Zec, and O. Mogren, “Scaling federated learning for fine-tuning of large language models,” in _International Conference on Applications of Natural Language to Information Systems_ , 2021, pp. 15–23. 

- [46] P. Basu, T. S. Roy, R. Naidu, Z. M¨uft¨uoglu, S. Singh, and F. Mireshghallah, “Benchmarking differential privacy and federated learning for BERT models,” p. arXiv:2106.13973, 2021. 

