# **TableTime: Reformulating Time Series Classification as Training-Free Table Understanding with Large Language Models** 

Jiahao Wang 

State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China 

Hefei, Anhui Province, China SA24229078@mail.ustc.edu.cn 

Yitong Zhou 

State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China Hefei, Anhui Province, China yitong.zhou@mail.ustc.edu.cn 

Mingyue Cheng<sup>∗</sup> 

State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China Hefei, Anhui Province, China mycheng@ustc.edu.cn 

## Daoyu Wang 

State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China Hefei, Anhui Province, China wdy030428@mail.ustc.edu.cn 

## Qingyang Mao 

State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China Hefei, Anhui Province, China maoqy0503@mail.ustc.edu.cn 

## Qi Liu 

State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China Hefei, Anhui Province, China qiliuql@ustc.edu.cn 

## Feiyang Xu 

Artificial Intelligence Research Institute, iFLYTEK Co., Ltd Hefei, Anhui Province, China fyxu2@iflytek.com 

### **Abstract** 

Large language models (LLMs) have shown promise in multivariate time series classification (MTSC). To effectively adapt LLMs for MTSC, it is crucial to generate comprehensive and informative data representations. Most methods utilizing LLMs encode numerical time series into the model’s latent space, aiming to align with the semantic space of LLMs for more effective learning. Despite effectiveness, we highlight three limitations that these methods overlook: (1) they struggle to incorporate temporal and channel-specific information, both of which are essential components of multivariate time series; (2) aligning the learned representation space with the semantic space of the LLMs proves to be a significant challenge; (3) they often require task-specific retraining, preventing training-free inference despite the generalization capabilities of LLMs. To bridge these gaps, we propose TableTime, which reformulates MTSC as a table understanding task. Specifically, TableTime introduces the following strategies: (1) utilizing tabular form to unify the format of time series, facilitating the transition from the model-centric approach to the data-centric approach; (2) representing time series in text format to facilitate seamless alignment with the semantic 

∗Mingyue Cheng is the corresponding author. 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea._ 

© 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 979-8-4007-2040-6/2025/11 https://doi.org/10.1145/3746252.3761056 

## Xin Li 

State Key Laboratory of Cognitive Intelligence, University of Science and Technology of China Hefei, Anhui Province, China leexin@ustc.edu.cn 

space of LLMs; (3) designing a knowledge-task dual-driven reasoning framework, TableTime, integrating contextual information and expert-level reasoning guidance to enhance LLMs’ reasoning capabilities and enable training-free classification. Extensive experiments conducted on 10 publicly available benchmark datasets from the UEA archive validate the substantial potential of TableTime to be a new paradigm for MTSC. The code is publicly available<sup>1</sup> . 

### **CCS Concepts** 

- **Mathematics of computing** → **Time series analysis** . 

### **Keywords** 

Multivariate Time Series Classification, Table Understanding, Large Language Models 

#### **ACM Reference Format:** 

Jiahao Wang, Mingyue Cheng, Qingyang Mao, Yitong Zhou, Daoyu Wang, Qi Liu, Feiyang Xu, and Xin Li. 2025. TableTime: Reformulating Time Series Classification as Training-Free Table Understanding with Large Language Models. In _Proceedings of the 34th ACM International Conference on Information and Knowledge Management (CIKM ’25), November 10–14, 2025, Seoul, Republic of Korea._ ACM, New York, NY, USA, 11 pages. https://doi.org/10.1145/3746252.3761056 

### **1 Introduction** 

Multivariate time series [13, 16] are commonly encountered in various domains, consisting of sequences of events collected over time, where each event includes observations recorded across multiple attributes. For example, the electrocardiogram (ECG) [34] signals in electronic health records (EHRs) capture various aspects of heart 

1https://github.com/realwangjiahao/TableTime 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

Jiahao Wang et al. 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0002-02.png)



![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0002-03.png)



![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0002-04.png)


**Figure 1: Illustrating the core idea of TableTime: transforming time series into tabular representations for universal classification in a data-centric paradigm.** 

function through multiple sensors. Comprehensive analysis of such data can facilitate decision-making in real applications [32], such as human activity recognition, healthcare monitoring, and industry detection. Particularly, as a fundamental problem in time series analysis, multivariate time series classification (MTSC) has attracted significant attention both in academia and industry [17]. 

Over the years, various approaches have been developed to address the MTSC task [17, 29, 35]. Traditional methods like Dynamic Time Warping (DTW) [22] with nearest neighbor classifiers [28] align time series of varying lengths but struggle to capture hidden features, leading to inaccurate modeling. Machine learning methods, such as Support Vector Machines [9] and Random Forests [3], rely on handcrafted features and assume stationarity, which hinders their effectiveness in handling dynamic and diverse time series data. Deep learning [18] has since reduced the need for feature engineering, with CNN-based [6, 33] and transformer-based [42, 48] approaches gaining significant attention. However, deep learning methods rely on a large amount of labeled data, limiting their application in practical scenarios. 

Recent studies have demonstrated that large language models (LLMs) exhibit robust pattern recognition and reasoning abilities over complex sequences [31], which has spurred growing interest in their application to time series analysis [14, 37]. LLM-based methods for time series analysis can generally be classified into two categories: prompt-based methods and retraining-based methods. Prompt-based methods, exemplified by PromptCast [25, 45], directly apply LLMs to downstream tasks by constructing tasks in a sentence-to-sentence format. In contrast, retraining-based methods involve modifying some or all parameters of the LLMs to adapt them to specific tasks [4, 21]. Both approaches enable LLMs to leverage their advanced pattern recognition and reasoning capabilities, utilizing pre-trained knowledge to capture temporal dependencies and make more accurate and generalizable predictions. 

While LLM-based methods have demonstrated effectiveness, several bottlenecks remain when applying them to time series classification [20]. First, a mismatch exists between numerical time series and the textual semantic space of LLMs, which restricts their capacity to process numeric data effectively. Second, they struggle to capture temporal dynamics and channel-specific features, which are crucial for accurate modeling. Third, extensive fine-tuning incurs high computational costs, particularly in resource-intensive applications. Lastly, they struggle to fully release the reasoning capabilities of LLMs. These challenges highlight the need for more efficient, generalizable, and domain-adaptive approaches for MTSC. 

An effective LLM-based method for MTSC, in our view, should possess several key attributes. First, it should align the numerical 

time series with the textual semantic space of LLMs, since LLMs are designed to process text-based inputs. Second, it should be capable of extracting both temporal consistency and inter-channel features from the time series data. Third, the method should enable training-free classification, leveraging the world knowledge acquired during the pre-training phase of the LLM. Finally, LLMbased models should possess strong reasoning abilities to handle complex tasks that require understanding both logical relationships and intricate dependencies within the data. 

To this end, we propose TableTime, a training-free classification framework based on table understanding for MTSC task. We convert the numeric time series into tabular format, preserving both temporal consistency and channel-specific information. To align the tabular time series with the semantic space of LLMs, we introduce table encoding, which converts the tabular time series into a textual representation. For training-free classification, we adopt a table understanding approach, which reformulates the MTSC task in a way that enables LLMs to classify without task-specific retraining. To maximize the reasoning potential of the LLMs, we develop a prompt incorporating neighbor-assisted enhancement and multi-path reasoning, aiming to fully leverage the LLMs’ reasoning capabilities. As shown in Figure 1, TableTime provides a new paradigm for MTSC. To summarize, our contributions include: 

- We propose the table understanding paradigm for MTSC and provide detailed explanations of how it helps alleviate the bottlenecks of most existing methods. 

- Under our proposed paradigm, we design a training-free framework called TableTime, which aims to leverage the reasoning capability of LLMs for time series classification. 

- We conduct comprehensive experiments on ten benchmark multivariate time series datasets, validating the effectiveness of table understanding paradigm and TableTime framework. 

### **2 Related Work** 

### **2.1 Time Series Classification** 

Time series classification has attracted considerable attention in both academia and industry [17, 27]. Early approaches primarily relied on distance-based methods, such as Dynamic Time Warping (DTW) [22] in combination with K-Nearest Neighbors (K-NN), which are effective in addressing temporal distortions in time series data. To overcome the limitations of these methods, ensemble techniques were introduced to improve classification accuracy. For instance, HIVE-COTE [23] is an ensemble learning algorithm that enhances performance by combining multiple feature transformations and classifiers through hierarchical voting, offering a more comprehensive and robust representation of time series characteristics. With the advent of deep learning, more sophisticated models began to surpass traditional methods by automatically learning hierarchical features from raw data. Early deep learning architectures, such as fully convolutional networks [39] and recurrent neural networks [15], demonstrated notable improvements in capturing local and sequential dependencies. More recently, models like InceptionTime [19] have employed deeper networks with multi-scale convolutions, significantly improving the ability to recognize complex patterns across varying time scales. Additionally, Transformer-based models [5, 48] have emerged as powerful alternatives, excelling at 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

TableTime: A Table Understanding Paradigm for Time Series Classification 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0003-02.png)


**Figure 2: Illustration of the TableTime, i.e., a paradigm for MTSC based on table understanding. (Left): TableTime implements classification through neighbor retrieval and context information modeling. (Right): Multi-path ensemble enhancement.** 

capturing long-range dependencies and global context, and further pushing the boundaries of time series classification performance across diverse application domains. 

### **2.2 LLMs in Time Series Analysis** 

Given the impressive capabilities of LLMs, researchers are increasingly exploring their applications in time series analysis [4, 49]. LLM-based approaches can be divided into two categories: finetuning and generative modeling. Fine-tuning methods, such as Linear Fine-Tuning, combine pre-trained LLMs with time seriesspecific encoders, leveraging their linguistic capabilities to identify patterns. Generative models, like GPT-based forecasting, predict future time series sequences, while models like TEMPO integrate domain knowledge to enhance performance. 

Despite effectiveness, LLMs in time series analysis encounter several significant challenges [36, 43, 46]. First, they struggle to capture temporal dependencies and channel-specific features, which are essential for accurate modeling. Second, a misalignment exists between numerical time series data and LLMs’ semantic space, which complicates processing. Third, fine-tuning these models is computationally expensive, particularly for large-scale applications. Lastly, LLMs fail to fully leverage their reasoning capabilities, limiting their potential. To address these issues, we propose TableTime, a paradigm for time series analysis through table understanding. 

dataset and task. Let _𝑃_ denote the prompt, the model’s output can be summarized as follows: _𝑇_<sup>_𝑖_</sup> = LLM( _𝑃,𝑋_<sup>_𝑖_</sup> ) where _𝑇_<sup>_𝑖_</sup> is the text generated by the large language model in response to the prompt and the input time series _𝑋_<sup>_𝑖_</sup> . To predict the label _𝑦_<sup>_𝑖_</sup> for each instance, we apply one regular expression to match _𝑇_<sup>_𝑖_</sup> and extract ˆ the classification result _𝑦_<sup>_𝑖_</sup> . 

### **3.2 Large Language Models** 

Recent advancements in LLMs have unveiled a broad range of powerful capabilities, allowing for addressing a variety of complex tasks. In this context, we propose leveraging LLMs to enhance MTSC. Several key advantages arise from utilizing LLMs to advance classification techniques: 

- _World Knowledge_ : Pre-trained on vast amounts of textual data from various domains, LLMs can integrate general knowledge into generations, enabling LLMs to provide contextual insights. 

- _Reasoning_ : LLMs exhibit advanced reasoning and pattern recognition abilities, which can potentially improve classification accuracy by capturing higher-level concepts. 

- _Training-Free Inference_ : LLMs have demonstrated remarkable training-free inference capabilities, showcasing their potential to generalize across domains without task-specific retraining. 

- _Text Generation_ : LLMs solve the problem in the paradigm of text generation, which provides more possibilities for enhancing the interpretability of classification results. 

### **3 Preliminaries** 

### **3.1 Problem Definitions** 

Let D = �( _𝑋_<sup>1</sup> _,𝑦_<sup>1</sup> ) _,_ ( _𝑋_<sup>2</sup> _,𝑦_<sup>2</sup> ) _, ...,_ ( _𝑋_<sup>_𝑛_</sup> _,𝑦_<sup>_𝑛_</sup> )� be a dataset consisting of _𝑛_ pairs<sup>�</sup> _𝑋_<sup>_𝑖_</sup> _,𝑦_<sup>_𝑖_�</sup> , where each _𝑋_<sup>_𝑖_</sup> ∈ R<sup>_𝑡_×</sup><sup>_𝑚_</sup> represents a multivariate time series with _𝑡_ time steps and _𝑚_ features, and _𝑦_<sup>_𝑖_</sup> ∈{ _𝑐_ 1 _,𝑐_ 2 _, . . . ,𝑐𝑘_ } is the corresponding label. The goal of the classification task is to learn a classifier on D that maps the input space _𝑋_ to a probability distribution over the class _𝑦_ . In the context of TableTime, we propose using prompt engineering based on the characteristics of the 

### **4 The Proposed TableTime** 

### **4.1 Model Architecture Overview** 

An overview of the TableTime is shown in Figure 2. TableTime introduces an innovative approach to multivariate time series classification (MTSC) by leveraging large language models (LLMs). To enhance reasoning capabilities, we first employ neighbor retrieval to identify relevant neighbors, improving the understanding of LLMs. These raw numerical time series are then converted into 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

Jiahao Wang et al. 

tabular format, preserving both temporal and channel information. To guide the LLM’s reasoning process, we design a comprehensive prompt that includes domain context information, neighbor knowledge, and task decomposition. In the final step, TableTime applies reasoning capability to classify the test sample. 

### **4.2 Context Information Modeling** 

_4.2.1 Reformulating Time Series as Tabular Data._ LLM-based models either learn time series embeddings directly in their latent space or align outputs from external models, often resulting in significant information loss, including temporal dependencies and channel relationships. The inherent mismatch between numerical time series and textual semantic spaces introduces inefficiencies and limits the LLMs’ ability to capture complex patterns in time series data. 

To address these challenges, we propose table encoding, which reformulates time series as tabular format. Table serves as a natural representation of time series, allowing for the preservation of both temporal and channel-specific information. Through table encoding, the original multivariate time series are converted into a structured tabular form, which is then serialized into text for further processing. This process can be formalized as follows: 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0004-06.png)


where C<sup>⊤</sup> =<sup>�</sup> _𝑐_ 1 _𝑐_ 2 _. . . 𝑐𝑚_ � denotes the channel-specific in- _𝑇_ formation and T =<sup>�</sup> _𝑡_ 1 _𝑡_ 2 _. . . 𝑡𝑡_ � denotes the timestamps. 

Subsequently, we convert the tabular time series data into a serialized textual format suitable for input. The process is formalized as follows: Text = Serialize( _𝑋_<sup>′</sup> ), where Text represents the · serialized text, and Serialize( ) refers to the serialization function, such as DFLoader or MarkDown [12]. Reformulating time series data into tabular format provides key advantages by preserving temporal dependencies and representing each channel separately, thereby enhancing both interpretability and compatibility. In this format, each row corresponds to a timestamp, and each column represents a channel, enabling independent feature processing while maintaining sequential relationships. 

_4.2.2 Domain Context Information._ While LLMs acquire extensive task-specific knowledge during pretraining, they remain sensitive to prompt design. Without explicit and well-structured instructions, they may misinterpret task intent, generate irrelevant content, or deviate from expected behavior. To address this, we incorporate domain context into the prompt, embedding key domain information to guide reasoning more effectively. 

The domain context follows a structured template to ensure clarity, consistency, and semantic alignment with the task. It contains three components: (1) task definition — a concise description of the task within its domain; (2) dataset description — details of the dataset’s structure, length, and properties; and (3) class description — definitions and scopes of each label. This structured approach reduces ambiguity, aligns model reasoning with task constraints, and improves output consistency and reliability. 

**4.3 Neighbor-Assisted In-Context Reasoner** A major challenge in training-free MTSC with LLMs is the lack of prior exposure to test samples, leading to semantic ambiguity and limiting reasoning over complex temporal patterns. To address this, we propose a neighbor retrieval–augmented framework, termed neighbor-assisted in-context reasoning, which retrieves semantically relevant training examples and embeds them in the prompt to provide inductive cues. These include positive samples with similar dynamics and negative samples with contrasting behavior, helping the model anchor its predictions. We employ two retrieval strategies: positive sample guidance and contrast enhancement. 

_4.3.1 Positive Sample Guidance._ To retrieve positive samples, we apply the k-nearest neighbors (KNN) algorithm to identify the set of _𝑘_ closest samples from the training dataset D<sup>_𝑡𝑟𝑎𝑖𝑛_</sup> for each test sample _𝑋_<sup>_𝑡𝑒𝑠𝑡_</sup> . Formally, the positive sample set is defined as: 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0004-13.png)


where TopK(·) selects the _𝑘_ samples with the nearest distances to _𝑋_<sup>_𝑡𝑒𝑠𝑡_</sup> , _𝐹𝑑𝑖𝑠𝑡_ is a chosen distance metric such as Euclidean distance, and _𝑋_<sup>_𝑖_</sup> ∈ D<sup>_𝑡𝑟𝑎𝑖𝑛_</sup> denotes the _𝑖_ -th training sample. 

_4.3.2 Contrast Enhancement._ To further assist LLMs in classification, we introduce contrast enhancement mechanism that incorporates negative samples into the model’s reasoning process. We begin by clustering the training dataset D<sup>_𝑡𝑟𝑎𝑖𝑛_</sup> using K-means to obtain a set of clusters { _𝐶𝑘_ } _𝑘_<sup>_𝐾_</sup> =1<sup>, which is defined by the following</sup> optimization problem: 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0004-16.png)


where _𝜇𝑘_ = | _𝐶_ <u>1</u> _𝑘_ | � _𝑋𝑖_ ∈ _𝐶𝑘_<sup>_𝑋_</sup> _𝑖_<sup>denotes the centroid of cluster</sup><sup>_𝐶_</sup> _𝑘_<sup>.</sup> Given a test sample _𝑋_<sup>_𝑡𝑒𝑠𝑡_</sup> , we assign it to the cluster whose centroid is nearest: 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0004-18.png)


To construct negative samples for _𝑋_<sup>_𝑡𝑒𝑠𝑡_</sup> , we select from all clusters except the _𝑗_ -th cluster: 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0004-20.png)


where TopM(·) denotes selecting the top _𝑀_ samples with the largest distances to _𝑋_<sup>_𝑡𝑒𝑠𝑡_</sup> , measured by a chosen distance metric (e.g., Euclidean distance) and _𝑋_<sup>_𝑖_</sup> ∈ D<sup>_𝑡𝑟𝑎𝑖𝑛_</sup> denotes the _𝑖_ -th training sample. This ensures that the negative samples are sufficiently dissimilar from the test sample, enhancing contrastive learning. 

### **4.4 Task Decomposition Mechanism** 

Previous prompts often lack the structured guidance needed for LLMs to handle complex tasks effectively. This absence of clear instructions forces LLMs to interpret the task independently for each sample, which may result in inconsistencies or irrelevant reasoning. Recently, step-by-step reasoning significantly improves the reasoning ability of LLMs [40]. Based on this insight, we introduce task decomposition, which breaks MTSC into a series of smaller and manageable steps, allowing for more effective reasoning. 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

TableTime: A Table Understanding Paradigm for Time Series Classification 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0005-02.png)



![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0005-03.png)



![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0005-04.png)



![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0005-05.png)



![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0005-06.png)


**Figure 3: Prompt template of TableTime. There are three components of input from top to bottom.** 

Instead of manually crafting the task decomposition strategy, we leverage a separate _Planning LLM_ to generate it. Given a single labeled MTSC example, the Planning LLM is prompted to explain the classification process step by step. This self-derived reasoning path is then abstracted into a general decomposition template. During inference, a different _Reasoning LLM_ which has no access to labels uses this structured prompt to perform classification. This separation ensures that the reasoning process aligns with the model’s internal logic while preserving training-free conditions. 

### **4.5 Multi-Path Ensemble Enhancement** 

Ensemble methods have demonstrated effectiveness for MTSC [10, 23]. When utilizing LLMs for MTSC, it cannot be ignored that the inherent stochasticity in LLM outputs makes direct classification challenging. In the meanwhile, self-consistency [38] leverages multiple outputs from one single LLM, selecting the most consistent response to enhance coherence and accuracy. 

Building on the aforementioned considerations, we propose the multi-path ensemble enhancement strategy. Specifically, we perform multiple inferences on the input _𝑋_<sup>_𝑡𝑒𝑠𝑡_</sup> under a set of distinct parameters of LLMs { _𝑇𝑖_ } _𝑖_<sup>_𝑀_</sup> =1<sup>,whereeachparameter</sup><sup>_𝑇𝑖_inducesa</sup> different reasoning trajectory within the LLM. The classification from the _𝑖_ -th parameter is denoted as _𝑓𝑇𝑖_ ( _𝑋_<sup>_𝑡𝑒𝑠𝑡_</sup> ). The final result is obtained by aggregating the results via majority voting: 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0005-12.png)


where _𝑦𝑖_ denotes the predicted labels of _𝑓𝑇𝑖_ (·) classifier and I(·) is the indicator function. This approach leverages the diversity introduced by varying parameters to sample multiple plausible reasoning paths, thereby mitigating randomness from any single inference and improving robustness and accuracy on complex multivariate time series classification tasks. 

**Table 1: Statistics of each dataset in the experiments.** 

|Dataset|Train Size|Test Size|Dimensions|Length|Classes|
|---|---|---|---|---|---|
|AWR|275|300|9|144|25|
|AF|15|15|2|640|3|
|BL|500|450|4|510|2|
|CR|108|72|6|1,197|12|
|ER|30|270|4|65|6|
|FD|5890|3524|144|62|2|
|FM|316|100|28|50|2|
|SRS2|200|180|7|1,152|2|
|SWJ|12|15|4|2500|3|
|UWG|120|320|3|315|8|



### **4.6 Prompt Construction** 

In TableTime, a structured prompt is crucial to achieve trainingfree classification. As the template shown in Figure 3, the prompt includes three parts: (1) **domain context information** which provides LLMs with professional knowledge to warm up, (2) **neighbor information** which provides crucial context by linking the test sample to similar or unsimilar labeled examples from the training dataset and (3) **task decomposition** that guides LLMs to implement step-by-step reasoning to generate the final results. 

### **4.7 Remark and Discussion** 

In the following, we summarize the characteristics of TableTime and discuss its relations to Table, Dist and LLM-based models. 

- _Relation to Table-based Methods._ Unlike traditional tabular models relying on handcrafted features, TableTime uses tables as semantic prompts, enabling direct reasoning over temporal structures. 

- _Relation to Dist-based Methods._ While distance-based methods are interpretable but noise-sensitive, TableTime preserves interpretability and improves robustness via LLM-driven inference. 

- _Relation to LLM-based Methods._ Unlike costly LLM-based approaches with external embeddings, TableTime encodes raw time series into prompt-friendly tables, supporting training-free classification without representation loss. 

### **5 Experiments** 

### **5.1 Experimental Setup** 

_5.1.1 Datasets._ We conduct experiments on ten representative datasets from the well-known UEA MTSC archive [1]. The UEA archive has become one of the most widely used multivariate time series benchmarks. Due to computational constraints, we use a set of 10 multivariate datasets from the UEA archive, which exhibit diverse characteristics in terms of the number and length of time series samples, as well as the number of categories. Specifically, we use the following datasets: ArticularyWordRecognition (AWR), AtrialFibrillation (AF), Blink (BL), Cricket (CR), Ering (ER), FaceDetection (FD), FingerMovements (FM), StandWalkJump (SWJ), SelfRegulationSCP2 (SRS2), , UWaveGestureLibrary (UWG). In these original dataset, training and testing set have been well processed. We do not take any processing for a fair comparison. We summarize the main characteristics of dataset in Table 1. 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

Jiahao Wang et al. 

**Table 2: Multivariate time series classification performance of TableTime and baseline models across ten datasets. The best are highlighted in bold, while the second-best are underlined. "Best" indicates the frequency of achieving the highest accuracy.** 

|Model|AWR|AF|BL|CR|ER|FD|FM|SRS2|SWJ|UWG|Average|Best|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|nn-DTW|0.9667|0.3333|0.5667|0.9654|0.9333|0.5184|0.5400|0.4889|0.2000|0.8906|0.6403|0|
|HIVE_COTE V1|0.9756|0.2667|**0.9978**|0.9547|0.9430|0.5376|0.4900|0.5222|0.6000|0.8875|0.7175|1|
|HIVE_COTE V2|0.9233|0.2000|0.9956|0.9306|0.9222|0.5474|0.5300|0.5278|0.4000|0.8725|0.6849|0|
|MLP|0.9822|0.3556|0.7259|0.9954|0.7642|0.6690|0.5933|0.5611|0.4889|0.6281|0.6764|0|
|MiniRocket|0.9433|0.4444|0.8793|0.9537|**0.9728**|0.6065|0.5567|0.5370|0.6444|**0.9365**|0.7475|2|
|InceptionTime|0.9807|0.4533|0.9165|**0.9972**|0.8859|**0.6818**|0.5985|0.5789|0.5733|0.8956|0.7562|2|
|MCNN|0.9767|0.3778|0.9556|0.9259|0.9222|0.6747|0.5567|0.5648|0.5333|0.8563|0.7344|0|
|MCDCNN|0.9789|0.4444|0.9763|0.9583|0.9358|0.5000|0.5800|0.5407|0.6000|0.8552|0.7370|0|
|TCN|0.9033|0.4000|0.7904|0.9537|0.5667|0.6801|0.5100|0.5148|0.3778|0.7531|0.6450|0|
|ConvTimeNet|**0.9844**|0.4444|0.9544|0.9769|0.8111|0.6613|0.6100|0.5852|0.3333|0.8635|0.7225|1|
|AutoFormer|0.5733|0.4667|0.5881|0.7917|0.6296|0.5749|0.5600|0.5167|0.4444|0.4906|0.5636|0|
|Informer|0.9811|0.2889|0.9378|0.9444|0.9432|0.5936|0.5867|0.5611|0.4667|0.8656|0.7169|0|
|TimesNet|0.9800|0.3333|0.9474|0.9213|0.9185|0.6109|0.5700|0.5574|0.4222|0.8656|0.7127|0|
|GPT4TS|0.9778|0.3778|0.9296|0.9352|0.9358|0.5821|0.5867|0.5611|0.4444|0.8542|0.7185|0|
|CrossTimeNet|0.9367|0.3333|0.9521|0.9761|0.8296|0.5649|0.6058|0.5709|0.4667|0.7750|0.7011|0|
|Time-LLM|0.7333|0.4000|0.5556|0.7083|0.7519|0.5482|0.6000|0.5667|0.6000|0.4438|0.5908|0|
|Time-FFM|0.9733|0.3333|0.6911|0.9415|0.8667|0.5963|0.5600|0.5722|0.4000|0.8688|0.6803|0|
|TableTime|0.9733|**0.6667**|0.9222|0.9822|0.9518|0.6771|**0.6400**|**0.5889**|**0.7333**|0.8906|**0.8026**|**5**|



**Table 3: Experimental results of ablation results for five key modules. Evaluated by accuracy.** 

|Variants|AWR|AF|CR|FM|SRS2|Average|IMP(%)|
|---|---|---|---|---|---|---|---|
|TableTime|**0.9733**|**0.6667**|**0.9822**|**0.6400**|**0.5889**|**0.7627**|–|
|_w/o_timestamps|0.9700|0.5333|0.9583|0.5500|0.5388|0.7101|-7.81|
|_w/o_channel information|0.9633|0.5333|0.9444|0.5700|0.5500|0.7122|-7.53|
|_w/o_timestamps & channel information|0.9633|0.5333|0.9444|0.4200|0.5000|0.6722|-12.73|
|_w/o_domain context information|0.9700|0.4000|0.9722|0.6000|0.5278|0.6940|-9.90|
|_w/o_negative samples|0.9433|0.3867|0.9213|0.5334|0.5114|0.6592|-14.41|



_5.1.2 Baselines._ To conduct a comprehensive and fair comparison, we use baseline methods which is highly related to TableTime. **Distance-based** methods: nn-DTW [22]. **Hybrid** methods: HIVECOTE V1 [24], HIVE-COTE V2 [30]. **Deep learning-based** methods: MLP [17], MiniRocket [10], InceptionTime [19], MCNN [44], MCDCNN [47], TCN [2], ConvTimeNet [8], AutoFormer [42], Informer [48] and TimesNet [41]. **LLM-based** methods: GPT4TS [49], CrossTimeNet [7], Time-LLM [21] and Time-FFM [26]. 

_5.1.3 Implement Details._ For nn-DTW and HIVE-COTE V1 and V2, we adopt the code in<sup>2</sup> . For the MCDCNN, MCNN, MiniRocket, MLP, TCN and InceptionTime, we adopt the publicly available code in<sup>3</sup> . For other baseline methods, we directly adopt the official implementation code. For a fair comparison, all models are trained on the training set and report the accuracy score on the testing set. We use DTW as the neighbor retrieval methods. We use GPT-4o to generate the task decomposition and we use Llama-3.1-70b-instruct to tackle inference task. Temperature, top-p, max-tokens is setting 

> 2https://github.com/aeon-toolkit/aeon 

> 3https://github.com/timeseriesAI/tsai 

to 0.2, 0.7 and 4096. Each experiment is repeated three times to minimize the uncertainty of the generated content of LLMs. All experiments in this paper set the number of inference paths to 3, and different inference paths come from different temperature settings, which are 0.1, 0.2, and 0.3. 

### **5.2 Classification Results Analysis** 

Table 2 summarizes the classification accuracy of all compared methods, and Figure 5 reports the critical difference diagram as presented in [11]. Compared to other baseline models, the experimental results demonstrate that our proposed TableTime achieves competitive performance and notable advantages on several datasets. For each dataset, the performance of TableTime is either the most accurate one or very close to the best one. This all demonstrates the powerful capabilities of TableTime in MTSC tasks. 

We observe that TableTime surpasses other baselines by a large margin on datasets like AF and SWJ, where both training and testing sets are small, highlighting the strong training-free classification ability of LLMs in data-scarce scenarios. Our method also consistently outperforms GPT4TS, Time-LLM, and Time-FFM, confirming 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

TableTime: A Table Understanding Paradigm for Time Series Classification 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0007-02.png)



![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0007-03.png)


**Figure 4: (Left) : Experimental results of four different neighbor retrieval methods: DTW, ED, SED, MAN. (Right) : Classification accuracy results under different neighbor number settings.** 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0007-05.png)


**Table 4: Comparison of four table formats on four datasets. DFLoader contributes the best encoding method.** 

|Table Format|AWR|AF|FM|UWG|
|---|---|---|---|---|
|DFLoader|**0.9733**|**0.6667**|**0.6400**|**0.8906**|
|HTML|0.9233|0.4867|0.5621|0.8241|
|JSON|0.9567|0.5433|0.5786|0.8564|
|MarkDown|0.9654|0.5574|0.5984|0.8746|



**Figure 5: Critical difference diagram over the mean ranks of TableTime, baseline models.** 

its effective use of LLM reasoning for superior classification. However, TableTime lags behind optimal methods on BL and UWG, likely because their large scale enables deep learning models to capture richer features. 

### **5.3 Study of Context Information Modeling** 

_5.3.1 Effectiveness of Timestamps and Channel Information._ To assess the importance of timestamps and channel information, we conduct three ablation experiments: ablation of timestamps, ablation of channel information, and ablation of both. As shown in Table 3, it is evident that both timestamps and channel information play a crucial role in the performance of TableTime. Among these, the former is more important, which further confirms the importance of temporal information for time series modeling. 

_5.3.2 Effectiveness of Domain Context Information._ To assess the effectiveness of domain context information in TableTime, we conduct its ablation study. As shown in Table 3, we reveal the importance of it in assisting LLM reasoning, which is an integral part for TableTime to make inferences that conform to domain rules. 

_5.3.3 Various Table Formats._ Table format influences performance in two ways: (1) different encodings yield different token counts, and (2) they lead to varied LLM outputs due to differing levels of structural information. We evaluate several encoding methods by computing the mean accuracy of all neighbors under each format (Table 4). DFLoader performs best, likely because it represents each channel separately, avoiding feature mixing. In contrast, JSON 

encodes values per time step, limiting comprehension; HTML introduces many irrelevant characters that may hinder reasoning; and MarkDown blurs the distinction between time indices and feature channels, affecting interpretation. 

### **5.4 Analysis of Neighbor-Assisted Strategy** 

_5.4.1 Analysis of Neighbor Retrieval Methods._ Although no distance function achieves SOTA on all datasets, our analysis (Figure 4) shows that retrieval choice strongly impacts TableTime’s performance. Dynamic Time Warping (DTW) outperforms Manhattan (MAN), Euclidean (ED), and Standardized Euclidean (SED), likely due to its robustness in high-dimensional time series by flexibly aligning sequences to handle temporal distortions and shifts. The advantage is most pronounced on the AF dataset, while the gap narrows on larger datasets, suggesting smaller datasets are more sensitive to retrieval choice. 

_5.4.2 Study of the Number of Positive Samples._ In order to further explore the impact of the number of nearest neighbors on the final classification accuracy, we count the classification accuracy under different neighbor samples. As shown in Figure 4, the accuracy initially increases as the number of nearest neighbors (K) increases, and it begins to decline beyond a certain point. This pattern suggests that while a moderate increase in neighbors can enhance performance by providing relevant context, too many neighbors may introduce noise, leading to decreased accuracy. We attribute this decline to potential "model hallucination," where excessive contextual information makes it challenging for the model to filter out irrelevant data, thus reducing classification accuracy. 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

Jiahao Wang et al. 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0008-02.png)



![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0008-03.png)


**Figure 6: (Left) : Effectiveness of task decomposition mechanism in TableTime framework. (Right) : TableTime classification performance when the number of inference paths is 1, 3, 5, and 7.** 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0008-05.png)



![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0008-06.png)


**Figure 7: Result of nearest neighbor consistency analysis. The results show the classification results when the nearest neighbor is selected and not selected.** 

_5.4.3 Study of Negative Samples._ By retrieving negative samples, we can provide negative examples to the LLM and guide it to perform comprehensive reasoning. In this section, we verify whether negative samples are really effective for classifying TableTime. Specifically, we remove these negative samples in the prompt and only keep the positive samples in the prompt. 

As the results shown in the Table 3, the removal of negative samples results in a 14.41% drop in classification performance. This outweighs the performance degradation caused by removing timestamps and channel information. This proves the irreplaceable role of negative samples in TableTime classification, which can help LLMs achieve deeper feature extraction during classification. 

### **5.5 Analysis of Reasoning Strategy** 

_5.5.1 Effectiveness of Task Decomposition Mechanism._ Task decomposition systematically breaks down MTSC task into smaller and manageable steps, ensuring that the LLMs could effectively process the input timeseries and evaluate the temporal and channel-specific features for decision making. To evaluate the impact of task decomposition, we conduct ablation experiments by removing this component from the prompt. As shown in Figure 6, results indicate 

that removing this mechanism leads to noticeable drops in accuracy, particularly on datasets with high-dimensional and complex temporal patterns. The structured reasoning enabled by problem decomposition not only enhances interpretability but also strengthens the model’s ability to generalize, demonstrating its critical role in achieving robust and reliable performance. 

_5.5.2 Analysis of Multi-path Ensemble Module._ The multi-path ensemble module aims to enhance classification robustness and accuracy by aggregating predictions from diverse inference paths generated through varying the temperature of the LLM. In this part, we explore the classification results for different number of temperature combinations. As shown in Figure 6, multi-path ensemble reasoning improves classification performance over a single path, demonstrating its effectiveness. However, performance gains do not scale linearly with more paths. While increasing the number of inference paths from 1 to 3 and 5 improves accuracy on most datasets, using 7 paths leads to a performance drop and higher inference cost. This indicates a trade-off between performance and computational efficiency. 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

TableTime: A Table Understanding Paradigm for Time Series Classification 


![](TableTime_Reformulating_Time_Series_Classification_as_Training-Free_Table_Understanding_with_Large_Language_Models_images/conv_1a5224b814480c23.pdf-0009-02.png)


##### LLM Input 

Task Definition: You are an expert in electroencephalogram (EEG) signal analysis, neuroscience, and clustering analysis. You will classify samples based on provided EEG time-series data by extracting frequency features (such as alpha waves, beta waves, etc.) and using these features. Below is a detailed description of the dataset. Class Definition: There are two classes: `0` indicates an upcoming left-hand movement, and `1` indicates an upcoming right-hand movement.’ Channel Information: Frontal Area (F region): Located in the frontal lobe, involved in decision-making, motor preparation, working memory, and attention. The Fz channel is particularly associated with motor control and the planning phase of task execution. 

Test Sample: <data_encoding> Neighbors: <positive_samples1> <label1>, <positive_samples2> <label2>, <positive_samples3> <label3>, <positive_samples4> <label4>, <negative_samples1> <label1>, <negative_samples2> <label2> 

Task Decomposition: 

Step1: Frequency Analysis Requirements: You need to perform a Short-Time Fourier Transform (STFT) or Wavelet Transform on the EEG data for each sample to calculate the power in different frequency bands for each channel Step 2: Training Set Data and Their Labels: Here are some sample data from the training set. Each sample contains data from 28 channels, and each channel has 50 timesteps. Perform frequency analysis on this data and compute the power for each frequency band. 

LLM Output Final result: 1 

**Figure 8: Comparison of classification performance of TableTime under tabular and natural language input.** 

### **5.6 In-Depth Evaluation w.r.t the Performance of TableTime** 

This study examines the relationship between LLM predictions and the labels of their nearest neighbors, shedding light on the model’s dependence on neighbor information and its robustness when discrepancies occur. We categorize results into cases where predictions match or differ from neighbor labels and analyze correctness within each group. As shown in Figure 7, TableTime maintains strong performance: even with inconsistent neighbors, accuracy remains above 50% (60.0% for FM, 58.3% for SRS2). These results suggest that while consistent neighbors improve accuracy, the model can still rely on LLM reasoning to deliver robust predictions despite noisy or incorrect references. 

### **5.7 Tabular vs. Natural Language Inputs** 

We investigate why tabular inputs are preferred over natural language. Although both formats encode the same data, tabular prompts explicitly align variables and values, whereas natural language embeds numbers in prose. Experiments on five datasets, replacing tabular input with sentences like “The channel is ... and its value is ...”, show that tabular formatting consistently achieves higher accuracy (Figure 8). This indicates that structural alignment, rather than semantics alone, facilitates cross-variable and temporal reasoning, while prose descriptions add unnecessary parsing burden. 

### **5.8 Case Study** 

Figure 9 shows one example of how TableTime tackles time series classification task. From this we can clearly see that TableTime’s classification selection is not an ordinary clustering, but reflects rigorous multi-step reasoning thinking. In this example, we input four positive samples and two negative samples. Although the first three positive samples are opposite to the correct answer, TableTime can still give the correct classification result. This further proves the effectiveness of TableTime. At the same time, we can see that the input results of TableTime are very logical, which further confirms the effectiveness of the task decomposition mechanism. 

Training dataset labels: Sample1: 0, Sample2: 0, Sample3: 0,ample4: 1, Sample5: 0, Sample6: 1 Rationale and Reasoning: To classify the test sample, we need to analyze the frequency features of each channel and compare them with the training dataset. Since the training dataset labels are provided, we can identify patterns and correlations between the frequency features and the labels Analyzing the frequency features of the test sample, we can observe that: The alpha band power is relatively high in channels F3, F1, and Fz, indicating relaxation and decreased cortical activity. Comparing these frequency features with the training dataset, we can observe that… Therefore, based on the frequency features and the labels of the training dataset, we can classify the test sample as 1. 

**Figure 9: A case study of how TableTime tackles time series classification. This example shows how TableTime utilizing task decomposition to this task.** 

### **6 Conclusion and Limitation** 

In this work, we highlight the critical importance of explicitly modeling temporal and channel-specific information in raw time series data. By converting time series into tabular time series, we naturally preserve the two information. Then we designed a reasoningenhanced prompt to stimulate the reasoning ability of LLMs to training-free classification. From this perspective, we naturally reformulate the multivariate time series classification(MTSC) problem as a table understanding problem, providing a new paradigm for MTSC. We propose the TableTime, a training-free time series classification reasoning framework. The classification results on 10 datasets demonstrate the superior performance of our method and the possibility to become a new paradigm in the field of MTSC. 

Despite the strengths of our model, we acknowledge several limitations that warrant further investigation. First, it is important to explore efficient methods for encoding tabular time series within our framework. As discussed earlier, certain encoding techniques may hinder the interpretability of LLMs. Second, the nearest neighbor retrieval process presents opportunities for optimization. Beyond performing retrieval directly on the original time series data, an alternative approach involves embedding the original data first and then conducting nearest neighbor retrieval. This method allows for a more comprehensive exploration of the features, enabling deeper insights. 

### **Acknowledgments** 

This research was supported by grants from the National Natural Science Foundation of China (No. 62502486), the grants of Provincial Natural Science Foundation of Anhui Province (No. 2408085QF193), the Fundamental Research Funds for the Central Universities of China (No. WK2150110032). 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

Jiahao Wang et al. 

### **GenAI Usage Disclosure** 

In the preparation of this manuscript, the authors employed generative AI tools solely for language editing purposes, such as correcting grammar, spelling, and improving sentence clarity. No generative AI technologies were used in the conception, experimental design, data analysis, or content generation of this paper. All intellectual contributions remain the sole work of the human authors. According to the ACM Policy on Authorship, such usage does not require disclosure; however, we include this statement for transparency. 

### **References** 

- [1] Anthony Bagnall, Hoang Anh Dau, Jason Lines, Michael Flynn, James Large, Aaron Bostrom, Paul Southam, and Eamonn Keogh. 2018. The UEA multivariate time series classification archive, 2018. _arXiv preprint arXiv:1811.00075_ XXXX, XXXX (2018). 

- [2] Shaojie Bai, J Zico Kolter, and Vladlen Koltun. 2018. An empirical evaluation of generic convolutional and recurrent networks for sequence modeling. _arXiv preprint arXiv:1803.01271_ (2018). 

- [3] Leo Breiman. 2001. Random forests. _Machine learning_ 45 (2001), 5–32. 

- [4] Mingyue Cheng, Yiheng Chen, Qi Liu, Zhiding Liu, Yucong Luo, and Enhong Chen. 2025. InstrucTime: Advancing Time Series Classification with Multimodal Language Modeling. In _Proceedings of the Eighteenth ACM International Conference on Web Search and Data Mining_ (Hannover, Germany) _(WSDM ’25)_ . Association for Computing Machinery, New York, NY, USA, 792–800. https://doi.org/10. 1145/3701551.3703499 

- [5] Mingyue Cheng, Qi Liu, Zhiding Liu, Zhi Li, Yucong Luo, and Enhong Chen. 2023. FormerTime: Hierarchical Multi-Scale Representations for Multivariate Time Series Classification. In _Proceedings of the ACM Web Conference 2023_ (Austin, TX, USA) _(WWW ’23)_ . Association for Computing Machinery, New York, NY, USA, 1437–1445. https://doi.org/10.1145/3543507.3583205 

- [6] Mingyue Cheng, Zhiding Liu, Qi Liu, Shenyang Ge, and Enhong Chen. 2022. Towards Automatic Discovering of Deep Hybrid Network Architecture for Sequential Recommendation. In _Proceedings of the ACM Web Conference 2022_ (Virtual Event, Lyon, France) _(WWW ’22)_ . Association for Computing Machinery, New York, NY, USA, 1923–1932. https://doi.org/10.1145/3485447.3512066 

- [7] Mingyue Cheng, Xiaoyu Tao, Qi Liu, Hao Zhang, Yiheng Chen, and Defu Lian. 2025. Cross-Domain Pre-training with Language Models for Transferable Time Series Representations. In _Proceedings of the Eighteenth ACM International Conference on Web Search and Data Mining_ (Hannover, Germany) _(WSDM ’25)_ . Association for Computing Machinery, New York, NY, USA, 175–183. https://doi.org/10.1145/3701551.3703498 

- [8] Mingyue Cheng, Jiqian Yang, Tingyue Pan, Qi Liu, Zhi Li, and Shijin Wang. 2025. ConvTimeNet: A Deep Hierarchical Fully Convolutional Model for Multivariate Time Series Analysis. In _Companion Proceedings of the ACM on Web Conference 2025_ (Sydney NSW, Australia) _(WWW ’25)_ . Association for Computing Machinery, New York, NY, USA, 171–180. https://doi.org/10.1145/3701716.3715214 

- [9] Corinna Cortes and Vladimir Vapnik. 1995. Support-Vector Networks. _Mach. Learn._ 20, 3 (Sept. 1995), 273–297. https://doi.org/10.1023/A:1022627411411 

- [10] Angus Dempster, Daniel F. Schmidt, and Geoffrey I. Webb. 2021. MiniRocket: A Very Fast (Almost) Deterministic Transform for Time Series Classification. In _Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining_ (Virtual Event, Singapore) _(KDD ’21)_ . Association for Computing Machinery, New York, NY, USA, 248–257. https://doi.org/10.1145/3447548.3467231 

- [11] Janez Demšar. 2006. Statistical comparisons of classifiers over multiple data sets. _The Journal of Machine learning research_ 7 (2006), 1–30. 

- [12] Xi Fang, Weijie Xu, Fiona Anting Tan, Jiani Zhang, Ziqing Hu, Yanjun (Jane) Qi, Scott Nickleach, Diego Socolinsky, "SHS" Srinivasan Sengamedu, and Christos Faloutsos. 2024. Large language models (LLMs) on tabular data: Prediction, generation, and understanding — a survey. _Transactions on Machine Learning Research_ (2024). https://www.amazon.science/publications/large-language-models-llmson-tabular-data-prediction-generation-and-understanding-a-survey 

- [13] Ge Gao, Qitong Gao, Xi Yang, Miroslav Pajic, and Min Chi. 2022. A Reinforcement Learning-Informed Pattern Mining Framework for Multivariate Time Series Classification. In _Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence, IJCAI-22_ , Lud De Raedt (Ed.). International Joint Conferences on Artificial Intelligence Organization, 2994–3000. https: //doi.org/10.24963/ijcai.2022/415 Main Track. 

- [14] Nate Gruver, Marc Finzi, Shikai Qiu, and Andrew Gordon Wilson. 2023. Large language models are zero-shot time series forecasters. In _Proceedings of the 37th International Conference on Neural Information Processing Systems_ (New Orleans, LA, USA) _(NIPS ’23)_ . Curran Associates Inc., Red Hook, NY, USA, Article 861, 14 pages. 

- [15] Michael Hüsken and Peter Stagge. 2003. Recurrent neural networks for time series classification. _Neurocomputing_ 50 (2003), 223–235. 

- [16] Md Amirul Islam, Sen Jia, and ND Bruce. 2001. How much position information do convolutional neural networks encode? arXiv 2020. _arXiv preprint arXiv:2001.08248_ (2001). 

- [17] Hassan Ismail Fawaz, Germain Forestier, Jonathan Weber, Lhassane Idoumghar, and Pierre-Alain Muller. 2019. Deep learning for time series classification: a review. _Data mining and knowledge discovery_ 33, 4 (2019), 917–963. 

- [18] Hassan Ismail Fawaz, Germain Forestier, Jonathan Weber, Lhassane Idoumghar, and Pierre-Alain Muller. 2019. Deep learning for time series classification: a review. _Data mining and knowledge discovery_ 33, 4 (2019), 917–963. 

- [19] Hassan Ismail Fawaz, Benjamin Lucas, Germain Forestier, Charlotte Pelletier, Daniel F Schmidt, Jonathan Weber, Geoffrey I Webb, Lhassane Idoumghar, PierreAlain Muller, and François Petitjean. 2020. Inceptiontime: Finding alexnet for time series classification. _Data Mining and Knowledge Discovery_ 34, 6 (2020), 1936–1962. 

- [20] Yushan Jiang, Zijie Pan, Xikun Zhang, Sahil Garg, Anderson Schneider, Yuriy Nevmyvaka, and Dongjin Song. 2024. Empowering time series analysis with large language models: a survey. In _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence_ (Jeju, Korea) _(IJCAI ’24)_ . Article 895, 9 pages. https://doi.org/10.24963/ijcai.2024/895 

- [21] Ming Jin, Shiyu Wang, Lintao Ma, Zhixuan Chu, James Y. Zhang, Xiaoming Shi, Pin-Yu Chen, Yuxuan Liang, Yuan-Fang Li, Shirui Pan, and Qingsong Wen. 2024. Time-LLM: Time Series Forecasting by Reprogramming Large Language Models. In _The Twelfth International Conference on Learning Representations_ . https://openreview.net/forum?id=Unb5CVPtae 

- [22] Rohit J Kate. 2016. Using dynamic time warping distances as features for improved time series classification. _Data mining and knowledge discovery_ 30 (2016), 283– 312. 

- [23] Jason Lines, Sarah Taylor, and Anthony Bagnall. 2018. Time series classification with HIVE-COTE: The hierarchical vote collective of transformation-based ensembles. _ACM Transactions on Knowledge Discovery from Data (TKDD)_ 12, 5 (2018), 1–35. 

- [24] Jason Lines, Sarah Taylor, and Anthony Bagnall. 2018. Time series classification with HIVE-COTE: The hierarchical vote collective of transformation-based ensembles. _ACM Transactions on Knowledge Discovery from Data (TKDD)_ 12, 5 (2018), 1–35. 

- [25] Haoxin Liu, Zhiyuan Zhao, Jindong Wang, Harshavardhan Kamarthi, and B. Aditya Prakash. 2024. LSTPrompt: Large Language Models as Zero-Shot Time Series Forecasters by Long-Short-Term Prompting. In _Findings of the Association for Computational Linguistics: ACL 2024_ , Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 7832–7840. https://doi.org/10.18653/v1/2024.findings-acl.466 

- [26] Qingxiang Liu, Xu Liu, Chenghao Liu, Qingsong Wen, and Yuxuan Liang. 2025. TIME-FFM: towards LM-empowered federated foundation model for time series forecasting. In _Proceedings of the 38th International Conference on Neural Information Processing Systems_ (Vancouver, BC, Canada) _(NIPS ’24)_ . Curran Associates Inc., Red Hook, NY, USA, Article 2996, 27 pages. 

- [27] Zhiding Liu, Jiqian Yang, Mingyue Cheng, Yucong Luo, and Zhi Li. 2024. Generative Pretrained Hierarchical Transformer for Time Series Forecasting. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ (Barcelona, Spain) _(KDD ’24)_ . Association for Computing Machinery, New York, NY, USA, 2003–2013. https://doi.org/10.1145/3637528.3671855 

- [28] Vivek Mahato, Martin O’Reilly, and Pádraig Cunningham. 2018. A Comparison of k-NN Methods for Time Series Classification and Regression.. In _AICS_ . 102–113. 

- [29] Matthew Middlehurst, Ali Ismail-Fawaz, Antoine Guillaume, Christopher Holder, David Guijo-Rubio, Guzal Bulatova, Leonidas Tsaprounis, Lukasz Mentel, Martin Walter, Patrick Schäfer, et al. 2024. aeon: a Python toolkit for learning from time series. _Journal of Machine Learning Research_ 25, 289 (2024), 1–10. 

- [30] Matthew Middlehurst, James Large, Michael Flynn, Jason Lines, Aaron Bostrom, and Anthony Bagnall. 2021. HIVE-COTE 2.0: a new meta ensemble for time series classification. _Machine Learning_ 110, 11 (2021), 3211–3243. 

- [31] Shervin Minaee, Tomas Mikolov, Narjes Nikzad, Meysam Chenaghlu, Richard Socher, Xavier Amatriain, and Jianfeng Gao. 2024. Large language models: A survey. _arXiv preprint arXiv:2402.06196_ (2024). 

- [32] Beanbonyka Rim, Nak-Jun Sung, Sedong Min, and Min Hong. 2020. Deep learning in physiological signal data: A survey. _Sensors_ 20, 4 (2020), 969. 

- [33] Alejandro Pasos Ruiz, Michael Flynn, James Large, Matthew Middlehurst, and Anthony Bagnall. 2021. The great multivariate time series classification bake off: a review and experimental evaluation of recent algorithmic advances. _Data Mining and Knowledge Discovery_ 35, 2 (2021), 401–449. 

- [34] Pritam Sarkar and Ali Etemad. 2020. Self-supervised ECG representation learning for emotion recognition. _IEEE Transactions on Affective Computing_ 13, 3 (2020), 1541–1554. 

- [35] Gian Antonio Susto, Angelo Cenedese, and Matteo Terzi. 2018. Chapter 9 - TimeSeries Classification Methods: Review and Applications to Power Systems Data. In _Big Data Application in Power Systems_ , Reza Arghandeh and Yuxun Zhou (Eds.). Elsevier, 179–220. https://doi.org/10.1016/B978-0-12-811968-6.00009-7 

CIKM ’25, November 10–14, 2025, Seoul, Republic of Korea. 

TableTime: A Table Understanding Paradigm for Time Series Classification 

- [36] Mingtian Tan, Mike A. Merrill, Vinayak Gupta, Tim Althoff, and Thomas Hartvigsen. 2025. Are language models actually useful for time series forecasting?. In _Proceedings of the 38th International Conference on Neural Information Processing Systems_ (Vancouver, BC, Canada) _(NIPS ’24)_ . Curran Associates Inc., Red Hook, NY, USA, Article 1922, 30 pages. 

- [37] Xiaoyu Tao, Tingyue Pan, Mingyue Cheng, and Yucong Luo. 2024. Hierarchical Multimodal LLMs with Semantic Space Alignment for Enhanced Time Series Classification. _arXiv preprint arXiv:2410.18686_ (2024). 

- [38] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 2023. Self-Consistency Improves Chain of Thought Reasoning in Language Models. In _The Eleventh International Conference on Learning Representations_ . https://openreview.net/forum? id=1PL1NIMMrw 

- [39] Zhiguang Wang, Weizhong Yan, and Tim Oates. 2017. Time series classification from scratch with deep neural networks: A strong baseline. In _2017 International joint conference on neural networks (IJCNN)_ . IEEE, 1578–1585. 

- [40] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ 35 (2022), 24824–24837. 

- [41] Haixu Wu, Tengge Hu, Yong Liu, Hang Zhou, Jianmin Wang, and Mingsheng Long. 2022. Timesnet: Temporal 2d-variation modeling for general time series analysis. _arXiv preprint arXiv:2210.02186_ (2022). 

- [42] Haixu Wu, Jiehui Xu, Jianmin Wang, and Mingsheng Long. 2021. Autoformer: Decomposition transformers with auto-correlation for long-term series forecasting. _Advances in neural information processing systems_ 34 (2021), 22419–22430. 

- [43] Mingzhe Xing, Rongkai Zhang, Hui Xue, Qi Chen, Fan Yang, and Zhen Xiao. 2024. Understanding the weakness of large language model agents within a complex android environment. In _Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ . 6061–6072. 

- [44] Guangyuan Xu, Weiyuan Sun, Hanhan Xue, and Xianzhou Feng. 2023. Time Series Classification Method Based on Multi-Scale Convolution with LSTM. In _2023 IEEE 11th Joint International Information Technology and Artificial Intelligence Conference (ITAIC)_ , Vol. 11. 1738–1744. https://doi.org/10.1109/ITAIC58329.2023. 10408824 

- [45] Hao Xue and Flora D Salim. 2024. PromptCast: A New Prompt-Based Learning Paradigm for Time Series Forecasting. _IEEE Transactions on Knowledge & Data Engineering_ 36, 11 (2024), 6851–6864. 

- [46] Yifan Yao, Jinhao Duan, Kaidi Xu, Yuanfang Cai, Zhibo Sun, and Yue Zhang. 2024. A survey on large language model (llm) security and privacy: The good, the bad, and the ugly. _High-Confidence Computing_ 4, 2 (2024), 100211. 

- [47] Yi Zheng, Qi Liu, Enhong Chen, Yong Ge, and J. Leon Zhao. 2014. Time Series Classification Using Multi-Channels Deep Convolutional Neural Networks. In _Web-Age Information Management_ , Feifei Li, Guoliang Li, Seung-won Hwang, Bin Yao, and Zhenjie Zhang (Eds.). Springer International Publishing, Cham, 298–310. 

- [48] Haoyi Zhou, Shanghang Zhang, Jieqi Peng, Shuai Zhang, Jianxin Li, Hui Xiong, and Wancai Zhang. 2021. Informer: Beyond efficient transformer for long sequence time-series forecasting. In _Proceedings of the AAAI conference on artificial intelligence_ , Vol. 35. 11106–11115. 

- [49] Tian Zhou, Peisong Niu, Liang Sun, Rong Jin, et al. 2023. One fits all: Power general time series analysis by pretrained lm. _Advances in neural information processing systems_ 36 (2023), 43322–43355. 

