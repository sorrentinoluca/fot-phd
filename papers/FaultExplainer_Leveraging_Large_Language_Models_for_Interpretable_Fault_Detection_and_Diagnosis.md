# Highlights 

## **_FaultExplainer_ : Leveraging Large Language Models for Interpretable Fault Detection and Diagnosis** 

Abdullah Khan, Rahul Nahar, Hao Chen, Gonzalo E. Constante Flores, Can Li 

- _FaultExplainer_ is an LLM-based natural language system for fault detection, diagnosis, and explanation. 

- _FaultExplainer_ integrates PCA and _T_<sup>2</sup> statistics with process decriptions for grounded fault explanations. 

- _FaultExplainer_ provides a web interface for real-time monitoring and user-friendly interaction. 

- Results show _FaultExplainer_ has reasonable performance in diagnosing unseen faults. 

# : _FaultExplainer_ Leveraging Large Language Models for Interpretable Fault Detection and Diagnosis 

Abdullah Khan<sup>a</sup> , Rahul Nahar<sup>a</sup> , Hao Chen<sup>a</sup> , Gonzalo E. Constante Flores<sup>a</sup> , Can Li<sup>a,</sup><sup>_∗_</sup> 

> _aDavidson School of Chemical Engineering, Purdue University, 480 W. Stadium Ave, West Lafayette, 47907, IN, USA_ 

## **Abstract** 

Machine learning algorithms are increasingly being applied to fault detection and diagnosis (FDD) in chemical processes. However, existing data-driven FDD platforms often lack interpretability for process operators and struggle to identify root causes of previously unseen faults. This paper presents _FaultExplainer_ , an interactive tool designed to improve fault detection, diagnosis, and explanation in the Tennessee Eastman Process (TEP). _FaultExplainer_ integrates real-time sensor data visualization, Principal Component Analysis (PCA)-based fault detection, and identification of top contributing variables within an interactive user interface powered by large language models (LLMs). We evaluate the LLMs’ reasoning capabilities in two scenarios: one where historical root causes are provided, and one where they are not to mimic the challenge of previously unseen faults. Experimental results using GPT-4o and o1-preview models demonstrate the system’s strengths in generating plausible and actionable explanations, while also highlighting its limitations, including reliance on PCA-selected features and occasional hallucinations. 

_Keywords:_ Fault detection and diagnosis, Large language models, Explainable AI 

> _∗_ Corresponding author at: Davidson School of Chemical Engineering, Purdue University, USA. _Email address:_ `canli@purdue.edu` (Can Li) 

_Preprint submitted to Computers & Chemical Engineering_ 

_December 20, 2024_ 

## **1. Introduction** 

Fault Detection and Diagnosis (FDD) are critical components in ensuring the reliability and safety of chemical processes. Fault detection involves recognizing the occurrence of a fault in the system, while fault diagnosis ascertains the root cause of the fault. In the chemical industry, where processes are complex and highly integrated, early and accurate FDD can prevent significant economic losses, environmental harm, and safety hazards. Effective FDD systems enhance operational efficiency by minimizing downtime and maintenance costs, thereby ensuring the continuous and safe operation of chemical plants. 

Various approaches have been developed for FDD, broadly categorized into model-based and data-driven methods (Chiang et al., 2001). Modelbased methods rely on the expertise and experience of operators and engineers and physics-based equations, often implemented through expert systems (Venkatasubramanian et al., 2003c,a). These methods can be highly effective in systems where physical models are well understood and can provide detailed explanations of fault mechanisms. However, they require extensive domain knowledge and may not adapt well to changes in the process. 

Data-driven methods, on the other hand, utilize historical and real-time process data to detect and diagnose faults (Venkatasubramanian et al., 2003b). Traditional statistical methods such as Principal Component Analysis (PCA) have been widely used for FDD due to their ability to handle multivariate data. However, these methods assume linearity and Gaussian distribution of data, which limits their applicability to more complex, non-linear processes commonly found in chemical industries. Recent advances in machine learning, particularly deep learning, have introduced more robust data-driven FDD techniques. Deep learning methods, such as Recurrent Neural Networks (RNNs), autoencoders, deep belief networks, and variants (Sun et al., 2020; Zhang and Qiu, 2022; Zhang and Zhao, 2017), can model complex non-linear relationships and temporal dependencies in process data. 

While deep learning methods offer superior modeling capabilities, they also come with challenges. One of the primary disadvantages is their lack of interpretability; understanding the reasoning behind a model’s predictions can be difficult, which poses a challenge to gaining trust in these systems. To make the deep learning models interpretable for FDD, recent works by Bhakte et al. (2022, 2023) have leveraged techniques in explainable artificial intelligence (XAI) such as Shapley value (Hart, 1989) to attribute the pre- 

2 

dictions of deep learning model to the contributions of each process variable. These XAI approaches are more interpretable than the deep learning models alone but they can only provide quantitative metrics and statistics of the models. 

To make FDD more interpretable, ideally, one would prefer to develop a natural-language-based explanation and query systems such that the process operators can have more intuitive interpretations of monitoring data using their domain knowledge. Such a natural language-based system for FDD was not possible until the recent advances in large language models (LLMs) such as GPT-4 (OpenAI, 2023) and Llama-2 (Touvron et al., 2023). However, the limitation of the LLMs is that they tend to “hallucinate”, meaning that they could generate text that is incorrect, nonsensical, or not real. This is problematic for a safety-critical application like FDD. 

Another limitation of data-driven fault diagnosis methods is their inability to diagnose the root causes of faults that have never been encountered. In practice, data-driven models often classify unseen faults as “unknown” without providing meaningful explanations(Chiang et al., 2001). Addressing these novel scenarios requires domain knowledge and potentially model-based approaches. Whether LLMs can leverage observed variations in measured and manipulated variables to infer causes of unseen faults remains an open question. 

To address these challenges, we develop _FaultExplainer_ , a first-of-itskind natural language-based system for intuitive fault detection and diagnosis (FDD) in chemical plants. In this work, we demonstrate a novel integration of LLMs with traditional statistical learning methods to generate explanations and root cause analyses for faults detected in the Tennessee Eastman Process (TEP) (Downs and Vogel, 1993). To mitigate the hallucinations of LLMs, we propose a method that leverages their capabilities while grounding their explanations in a detailed TEP process description, PCA, and feature importance analysis, ensuring that the resulting explanations are both accurate and interpretable for chemical process engineers. We evaluate the LLMs’ reasoning capabilities in two scenarios: one where historical root causes are provided, and one where they are not to mimic the challenge of previously unseen faults. _FaultExplainer_ is released as an open-source package with video demonstrations, available at `https://github.com/li-group/FaultExplainer` . 

The rest of the paper is organized as follows: Section 2 presents the necessary background and related literature. Section 3 provides an overview 

3 

of _FaultExplainer_ ’s capabilities. The methodologies are detailed in Section 4. Section 5 evaluates _FaultExplainer_ using the 15 known faults from the TEP process. Finally, conclusions are drawn in Section 6. 

## **2. Background and Literature Review** 

Fault Detection and Diagnosis (FDD) methods can be broadly classified into two main categories: model-based and data-driven approaches. Modelbased methods rely on physical and chemical models of the process and can be further divided into quantitative and qualitative methods (Venkatasubramanian et al., 2003c,a). Quantitative methods use mathematical models to represent the process. Diagnostic observers (Watanabe and Himmelblau, 1983b,a) are algorithms that compare the actual process outputs with the outputs of a mathematical model to detect discrepancies that indicate faults. Parity relations (Gertler and Monajemy, 1995; Yin and Liu, 2017) generate residuals by comparing measurements to their estimated values based on mathematical models, and faults are detected when these residuals exceed a certain threshold. Kalman filters (Welch et al., 1995) estimate the state of a process in real-time and use the discrepancies between the predicted and actual states to identify faults. Parameter estimation (Jiang et al., 2008; Alanqar et al., 2017) involves estimating the parameters of a process model, where significant deviations from normal parameter values indicate potential faults. 

Qualitative methods use non-numeric models to describe the process. Causal models including Digraphs (Vedam and Venkatasubramanian, 1997), fault trees (Geymayr and Ebecken, 1995), and qualitative physics models (Sacks, 1988), have been used to represent and analyze the cause-effect relationships within a process. Digraphs, or directed graphs, visually depict the cause-effect relationships between variables in a system, allowing for the identification of fault propagation paths. Fault trees utilize logic gates to model the sequences of events and conditions that can lead to system failures. Qualitative physics models use qualitative reasoning to represent the physical and functional relationships within a system to facilitate the understanding and diagnosis of faults based on causal interactions. 

Data-driven methods utilize statistical techniques and machine learning algorithms to identify patterns and anomalies in process data (Venkatasubramanian et al., 2003b). Principal Component Analysis (PCA) (Choi et al., 2005) reduces the dimensionality of process data by identifying the principal 

4 

components that capture the most variance, helping in detecting anomalies by highlighting deviations from the normal data patterns. Partial Least Squares (PLS) (Jia and Zhang, 2016) is used for modeling relationships between input and output variables in a process and can detect faults by identifying deviations in these relationships. Deep learning models including RNNs (Sun et al., 2020), autoencoders (Zhang and Qiu, 2022), deep belief networks (Zhang and Zhao, 2017), and Bayesian networks (Kumari et al., 2022a,b), are recently used for fault detection. Despite their effectiveness, data-driven methods often suffer from a lack of interpretability, making it difficult for domain experts to understand and trust the results. 

Explainable artificial intelligence (XAI) is an area that has attracted significant attention in the machine learning community, aiming to improve the interpretability of deep learning models. Broadly speaking, the current XAI methods can be classified into two main categories (Murdoch et al., 2019; Mittelstadt et al., 2019). Model-based approaches construct machine learning models with the goal of explainability in mind, resulting in simple, easier-to-interpret models. For example, one can use straightforward models such as linear/logistic regression (Bursac et al., 2008), decision trees (Quinlan, 1987), and K-nearest neighbor (Peterson, 2009). On the other hand, post hoc analysis refers to interpreting the model after it has been trained. This is usually applied to black-box machine learning models, such as neural networks, where the practitioner analyzes a trained model to provide insights into the learned relationships. An example of post hoc analysis is the linear approximation of the black-box model around a reference point, allowing the weights of the linear model to be directly interpreted as sensitivity measures. This indicates how much the classifier will respond as a particular feature changes. Examples of linear approximation include LIME (Ribeiro et al., 2016). Another popular local approach is contrastive/counterfactual explanation (CFE) (Wachter et al., 2017), where the idea is to explain to the practitioner how the features would have to change for the model to predict an alternative outcome. Recently, XAI methods have been applied to fault detection and diagnosis (FDD) applications. For instance, Hale et al. (2022) use symbolic regression to generate explainable mathematical functions for FDD. Additionally, Harinarayan and Shalinie (2022) applied counterfactual explanation to deep learning-based models. Techniques in XAI, such as the Shapley value (Hart, 1989), have also been leveraged by Bhakte et al. (2022, 2023) to attribute the predictions of deep learning models to the contributions of each process variable. 

5 

However, ideally, one would like to have natural language-based systems to explain faults, root causes, and answer follow-up questions raised by users. Large Language Models (LLMs), such as GPT-4 (OpenAI, 2023) and Llama2 (Touvron et al., 2023), which excel at qualitative natural language tasks such as biology and bar exams. However, these models struggle with more quantitative tasks such as answering math questions. Recently, OpenAI’s o1 model (OpenAI, 2024b) enhances reasoning abilities, particularly in complex tasks like mathematics and coding, by employing extended “thinking” time before responding, which improves accuracy and reliability. These recent advances make LLM a promising tool for improving the interpretability of ML models in chemical engineering. 

To the best of our knowledge, an LLM-based agent for FDD has not yet been built. The closest work in this space is TalkToModel (Slack et al., 2023), a recently developed chatbot that explains ML models by combining LLMs with external tools, such as counterfactual explanations. However, TalkToModel is restricted to small ML models and does not provide domain knowledge and context to the user. OptiChat(Chen et al., 2024) is an LLM-powered natural language dialogue system for explaining optimization models. In chemical process design, LLM has been applied to flowsheet and control structure generation (Balhorn et al., 2024; Hirtreiter et al., 2024). LLMs have also been applied to explaining biomedical data, like in scChat (Lu et al., 2024), LLaVA-Med (Li et al., 2023), and Med-PaLM (Tu et al., 2024). 

We use the Tennessee Eastman Process (TEP)(Downs and Vogel, 1993) to demonstrate our method. TEP is a widely recognized benchmark for process control research and simulates an industrial plant with five major units and eight components. The process includes a reactor, condenser, compressor, separator, and stripper, producing liquid products through exothermic reactions. TEP features 41 measured and 12 manipulated variables, including feed rates, pressures, temperatures, and valve positions. Fault detection is critical in TEP, which has 21 preprogrammed faults, such as step changes in process variables or changes in reaction kinetics. Among these, 15 of the faults have known root causes. Faults are generated through a simulation program that operates under closed-loop conditions with a plant-wide control scheme. This setup allows for a realistic evaluation of fault detection methods, making TEP an ideal testbed for assessing various process monitoring techniques. 

6 

## **3. Overview of** **_FaultExplainer_ ’s Capabilities** 

To facilitate the practical application of our methodology and to make our findings accessible to a wider audience, we developed an interactive web interface for fault diagnosis and explanation within the Tennessee Eastman Process (TEP). Figure 1 provides a visual overview of the capabilities of _FaultExplainer_ that can be accessed from the web interface. It enables users to quickly identify and diagnose faults, and understand their underlying causes. This interface offers three key features corresponding to the three windows shown in Figure 1: 

- **Real-Time Sensor Data Visualization:** Users can monitor realtime data from all TEP sensors, enabling them to observe and track the behavior of the 41 measured variables and the 12 manipulated variables. The sensor data are generated from the TEP simulator. The user can introduce fault to the process by using the “Fault” dropdown button, e.g., changing the system from “Normal Operation” to a fault such as “step change in A/C feed ratio”. All the faults described in (Downs and Vogel, 1993) are available. 

- **Fault History with** _T_<sup>2</sup> **Plot:** A dedicated “Fault History” page displays a real-time _T_<sup>2</sup> plot, along with a history of previously detected faults. This allows users to visualize the progression of faults over time and correlate them with changes in sensor data. The details of this method will be described in Section 4. After a fault is introduced, one can observe the change in _T_<sup>2</sup> statics in this window. When the _T_ 2 statistics exceed the fault triggering threshold, the color in the _T_<sup>2</sup> plot will change from green to red. The historical fault reports contain the analysis of the major changes in sensor measurement, root cause deduction, and how the root cause propagates through the process. 

- **Interactive Chat Interface:** A chat interface provides a convenient way for users to inquire about specific faults or seek explanations for observed anomalies. Users can interact with the system using natural language, and the interface will generate grounded explanations based on the methodology presented in Section 4. The users can ask followup qualitative questions related to the process and the faults such as “how to prevent the previous fault from occurring?”. 

7 


![](FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis_images/FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis.pdf-0009-00.png)



![](FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis_images/FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis.pdf-0009-01.png)



![](FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis_images/FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis.pdf-0009-02.png)


Figure 1: Interactive Web Interface for _FaultExplainer_ . From top to bottom are the process monitoring window, fault history tracker, and the interactive chat interface. 

8 


![](FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis_images/FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis.pdf-0010-00.png)


Figure 2: Overview of the Methods in _FaultExplainer_ 

## **4. Methods** 

To alleviate the hallucinations of the LLMs, we propose an approach by adapting classical approaches for fault detection and feature importance analysis to enhance fault explanation in the Tennessee Eastman Process (TEP). The approach combines Principal Component Analysis (PCA) for identifying deviations in process data with _T_<sup>2</sup> contribution analysis to pinpoint relevant process variables. The outputs from these rigorous methods together with a detailed description of the TEP are used as input to the LLM. An overview of the proposed method is shown in Figure 2. In what follows, we provide detailed explanations of the approach. 

## _4.1. Fault Detection and Feature Importance_ 

Faults in the Tennessee Eastman Process (TEP) are detected using a Principal Component Analysis (PCA)-based approach. PCA is a classical statistical learning technique used to reduce the dimensionality of a dataset while retaining most of the variability present in the data (Chiang et al., 2000). To make this paper self-contained, we provide a brief background of PCA. Mathematically, PCA involves several steps. First, the normal operating condition data is standardized by centering it (subtracting the mean of each variable) and scaling it (dividing by the standard deviation). The resulting _n_ scaled data points is represented by the matrix _X ∈R_<sup>_n×m_</sup> . Then, the covariance matrix of the standardized data is computed. Eigendecomposition is performed on this covariance matrix to obtain the eigenvalues and eigenvectors. 


![](FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis_images/FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis.pdf-0010-06.png)


where the diagonal matrix Λ _∈R_<sup>_m×m_</sup> contains the non-negative real 

9 

eigenvalues of decreasing magnitude ( _λ_ 1 _≥ λ_ 2 _≥· · · ≥ λm ≥_ 0 ). _V_ is the matrix that contains all the eigenvectors. 

The eigenvectors corresponding to the largest eigenvalues form the principal components. In the PCA model, the original data matrix _X_ can be decomposed into three matrices: _X_ = _TP_<sup>_T_</sup> + _E_ . Here, _T_ = _XP_ is the score matrix, which represents the projections of the original data onto the principal components. _P ∈R_<sup>_m×a_</sup> is the loading matrix, containing the loading vectors (principal components) associated only with the _a_ largest eigenvalues. _E_ is the residual matrix, capturing the variations not explained by the principal components. 

PCA can be used for fault identification through the _T_<sup>2</sup> statistic: 


![](FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis_images/FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis.pdf-0011-03.png)


where _x ∈R_<sup>_m_</sup> represents the scaled real-time sensor measurement, i.e., we assume the measurement has been standardized by the mean and standard deviation estimated from the normal operating condition data. Λ _a_ represents the diagonal matrix that contains the _a_ largest eigenvalues. The _T_<sup>2</sup> statistic threshold is set to be, 


![](FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis_images/FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis.pdf-0011-05.png)


where _α_ is the probability threshold, which corresponds to the false alarm probability. _F_ represents the F-ratio distribution. When _T_<sup>2</sup> _> Tα_<sup>2,afault</sup> alarm will be triggered. 

To discern the most influential variables contributing to these detected faults, we conducted a _T_<sup>2</sup> contribution analysis. This analysis quantifies the individual contributions of each variable to the overall _T_<sup>2</sup> statistic, allowing us to select the top contributing variables as candidates for further investigation. 

The contribution of _xj_ can be calculated as 


![](FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis_images/FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis.pdf-0011-09.png)


where _pj,i_ is the ( _j, i_ )th element of the loading matrix _P_ . _ti_ is the _i_ th element of the score _t_ = _P_<sup>_T_</sup> _x_ , _λi_ is the _i_ th largest eigenvalue. 

By decomposing the _T_<sup>2</sup> statistic this way, we can identify how much each variable _xj_ contributes to the overall _T_<sup>2</sup> value, which helps in pinpointing 

10 

which variables are contributing the most to the detected fault. This detailed analysis assists in diagnosing the source of faults and taking targeted corrective actions. 

## _4.2. TEP Process Description and Prompt Engineering_ 

To effectively use the LLM for fault explanation in the Tennessee Eastman Process (TEP), we first provide a detailed description of the process, including its unit operations, streams, and variables. This description clarifies the relationships among reactants, products, and byproducts, the role of each stream, and the monitored variables in the process. We explicitly distinguish between measured variables, which are recorded by sensors but cannot be directly manipulated, and manipulated variables, which can be actively adjusted by the control algorithm. This distinction allows the LLM to reason about process dynamics and the control system’s responses to deviations. Additionally, the top six PCA contributing features (variables) calculated by Equation (3) and their deviations from their mean values during normal operating conditions are provided as inputs to guide the LLM in identifying significant deviations and their potential explanations. 

Two different prompts are developed to support fault diagnosis. The first prompt includes a predefined list of 15 root causes shown in the first column of Table 1, retrieved from the original TEP paper (Downs and Vogel, 1993). This list acts as a constrained search space for the LLM, mimicking the scenario where the faults lie within historically encountered faults. The second prompt is named _Root Causes-Included Prompt_ . The second prompt assumes no prior knowledge of the potential fault causes, allowing the LLM to generate hypotheses based solely on the feature deviations and process description, which is to mimic the scenario of encountering unseen faults. This prompt is called _General Reasoning Prompt_ . Both prompts are designed to elicit deterministic and consistent explanations by systematically analyzing the deviations, hypothesizing root causes, and connecting the identified faults to the observed feature changes. These carefully constructed prompts enable the LLM to leverage domain knowledge effectively while remaining grounded in the provided data and process details. 

When the PCA identifies that a fault has occurred in the plant, the process description, the deviations of the top six contributing features from the normal operating condition, and one of the explanation prompts can be combined as inputs to the LLM. The LLM will generate a report describing what has been observed, the possible root causes of the faults, and how these 

11 

root causes are propagated in the plant causing the variables to deviate. All the prompts are shown in the supplementary text. 

## **5. Results** 

## _5.1. Experiment Setup_ 

The time series data for the normal operating conditions and the 15 known faults of the TEP are obtained from Rieth et al. (2017). These data include 41 measured and 12 manipulated variables, with each time series containing 500 time steps. The normal operating time series is used to train the PCA model to extract principal components that capture 90% of the data variance. The _T_<sup>2</sup> statistic threshold in Equation 2 is set to _α_ = 0 _._ 01, controlling the probability of a false fault report to 1%. _FaultExplainer_ triggers a fault only when six consecutive _T_<sup>2</sup> values exceed the threshold. Assuming independent observations, this corresponds to a false alarm rate of 0 _._ 01<sup>6</sup> = 1 _×_ 10<sup>_−_12</sup> . Once a fault is detected, we select the six features (variables) with the largest contribution values at the last time step. The values of these features are compared to their mean values during normal operation, and the value comparisons and percentage changes are incorporated into the prompts for the LLM. 

We evaluate _FaultExplainer_ using two settings described in Section 4.2. In the _Root Causes-Included Prompt_ setting, the LLM is provided with a predefined list of 15 known root causes and must identify and explain the top three most likely causes based on the top six feature changes. In the _General Reasoning Prompt_ setting, the LLM is not restricted to predefined root causes and must independently infer and explain three potential root causes using its reasoning capabilities. The latter reflects real-world scenarios where faults may not have been previously encountered, testing the flexibility and robustness of the tool. 

We test OpenAI’s GPT-4o (OpenAI, 2024a) and o1-preview (OpenAI, 2024b) models. The GPT-4o model, a multimodal system, excels at general natural language tasks, while the o1-preview model incorporates improved reasoning capabilities. These experiments are designed to evaluate the models’ accuracy, reasoning ability, and the quality of their explanations across both prompt settings. All outputs from both models for diagnosing the 15 faults under the two prompt settings are provided in the supplementary material. 

12 

## _5.2. Results of the Root Causes-Included Prompt_ 

We test the _Root Causes-Included Prompt_ over the 15 faults. Both LLMs are asked to give the top three possible fault classifications. 

## _5.2.1. Quantitative evaluation of the classification accuracy_ 

Table 1 summarizes the fault classification results of the GPT-4o and o1-preview models when prompted with the 15 predefined root causes. The numbers in bold indicate correct classifications. For certain faults, such as Faults 1 and 8, the contributing features alone cannot distinguish between random variations and step changes in the same features. These faults are considered aliases and are treated as correct as long as the model classifies the fault or its alias correctly. Faults that cannot be detected by PCA are marked with backslashes in the table. 

Among the 11 faults that can be identified using PCA, GPT-4o correctly classifies 7 faults, while o1-preview correctly classifies 9 faults. This aligns with o1-preview’s improved reasoning capabilities, allowing it to better utilize the provided descriptions and contributing features. Neither model is able to correctly diagnose Faults 5 (Condenser Cooling Water Inlet Temperature & Step) and 10 (C Feed Temperature (Stream 4) & Random Variation). This failure is mainly because the LLMs find alternative ways to explain the deviations of the top six features, which will be discussed in detail in the qualitative evaluation of the fault reports. 

## _5.2.2. Qualitative evaluation of the explanations_ 

In this subsection, we pick a fault where both models find the correct root cause and one fault where neither model finds the correct root cause to demonstrate the advantages and limitations of the two models. The rest of the fault reports follow a similar pattern and can be found in the supplementary material. 

The results for Fault 7, where both GPT-4o and o1-preview identify the correct root cause (C Header Pressure Loss - Reduced Availability in Stream 4), shown in Figure 3, demonstrate the plausibility and coherence of the explanations provided by both models. Both models accurately link the observed decreases in the reactor, product separator, and stripper pressures, as well as the reduced A and C feed flow rate, to the loss in header pressure. They also correctly attribute the control system’s compensatory behavior—namely, the increase in the A and C feed load—to the attempt to counteract the pressure loss. Furthermore, the explanations addressed the 

13 

Table 1: Summary of GPT-4o and o1-preview’s top three fault classification when prompted with the 15 root faults. The correct classifications are denoted in bold. The backslashes mean the corresponding faults cannot be detected by the PCA. 

|Faults|GPT-4o|o1-preview|
|---|---|---|
|Fault 1 A/C Feed Ratio, B Composition Constant (Stream 4) & Step (alias 8)|6,7,4|6,**1**,7|
|Fault 2 B Composition, A/C Ratio Constant (Stream 4) & Step (alias 8)|6,1,**8**|**2**,6,7|
|Fault 3 D Feed Temperature (Stream 2) & Step (alias 9)|_\_|_\_|
|Fault 4 Reactor Cooling Water Inlet Temperature & Step (alias 11,14)|_\_|_\_|
|Fault 5 Condenser Cooling Water Inlet Temperature & Step (alias 12,15)|3,4,6|4,7,1|
|Fault 6 A Feed Loss (Stream 1) & Step|**6**,7,4|**6**,7,1|
|Fault 7 C Header Pressure Loss - Reduced Availability (Stream 4) & Step|**7**,6,8|**7**,6,1|
|Fault 8 A, B, C Feed Composition (Stream 4) & Random Variation (alias 1,2)|6,7,4|6,7,**1**|
|Fault 9 D Feed Temperature (Stream 2) & Random Variation (alias 3)|_\_|_\_|
|Fault 10 C Feed Temperature (Stream 4) & Random Variation|6,1,4|13,1,7|
|Fault 11 Reactor Cooling Water Inlet Temperature & Random Variation (alias 4,14)|**4**,5,6|**4**,3,**14**|
|Fault 12 Condenser Cooling Water Inlet Temperature & Random Variation (alias 5, 15)|4,**5**,6|2,13,**5**|
|Fault 13 Reaction Kinetics & Slow Drift|4,6,**13**|3,**13**,6|
|Fault 14 Reactor Cooling Water Valve & Sticking (alias 4, 11)|**4**,6,5|**4**,**14**,7|
|Fault 15 Condenser Cooling Water Valve & Sticking (alias 5, 15)|_\_|_\_|



14 

decrease in compressor work as a consequence of reduced flow rates and vapor generation. 

### **Top six feature changes** 

We analyze the percentage changes in the top six contributing features during the fault compared to normal operation. The **Stripper Pressure** decreased by 3 _._ 00%, the **A and C Feed** flow rate decreased by 8 _._ 90%, the **Reactor Pressure** decreased by 3 _._ 49%, and the **Product Separator Pressure** decreased by 3 _._ 69%. The manipulated variable **A and C Feed Load** increased by 13 _._ 12%, and the **Compressor Work** decreased by 3 _._ 58%. 

### **GPT-4o explanation** 

**IDV(7) C Header Pressure Loss - Reduced Availability (Stream 4) & Step:** This root cause can explain the decrease in the A and C feed, as a pressure loss in the C header would directly reduce the availability of C, leading to a lower feed rate. The control system might respond by increasing the A and C feed load to compensate, explaining the observed increase in the feed load. The reduced availability of C could also lead to lower reaction rates, causing a decrease in reactor pressure and subsequently affecting the pressures in the stripper and product separator. The reduced flow rates could also lead to decreased compressor work. 

### **o1-preview explanation** 

**IDV(7): C Header Pressure Loss - Reduced Availability (Stream 4) & Step** A sudden loss in the C header pressure would reduce the availability of component C in Stream 4. This reduction directly causes the **A and C Feed** flow rate to decrease by 8 _._ 90%, as observed. In response, the control system increases the **A and C Feed Load** by 13 _._ 12% in an attempt to maintain the flow rate, but due to the pressure loss, the flow cannot be restored to normal levels. The decreased feed rate leads to lower pressures in the **Reactor** , **Product Separator** , and **Stripper** , explaining the 3% to 3 _._ 7% decreases in pressures. The reduction in overall flow rates causes a decrease in vapor generation and thus a decrease in **Compressor Work** by 3 _._ 58%. Therefore, this root cause explains all six of the top feature deviations. 

Figure 3: An illustrative example where both models are able to identify the correct root causes. The top six feature changes and the explanation of GPT-4o and o1-preview to the top six feature changes of Fault 7 (C Header Pressure Loss - Reduced Availability (Stream 4) & Step) when the 15 root causes are provided. 

Both models succeed in providing consistent and plausible interpretations of the observed feature changes, effectively connecting the root cause to the system’s response and the measured deviations. The explanations also align well with the expected behavior of the TEP control system, which adjusts manipulated variables to maintain operational stability. Notably, o1-preview 

15 

### **Top six feature changes** 

The **Stripper Temperature** increased by 2 _._ 45%, the **A Feed Load** increased by 43 _._ 90%, and the **A Feed Rate** increased by 43 _._ 63%. Meanwhile, the **E Feed Rate** decreased by 2 _._ 38%. The **Stripper Steam Valve** position increased by 14 _._ 59%, and the **Stripper Steam Flow** increased by 9 _._ 93%. 

### **GPT-4o explanation** 

**IDV(6) A Feed Loss (Stream 1) & Step** : This root cause could explain the significant increase in the A feed load and A Feed, as the control system might compensate for a perceived loss by increasing the feed rate. _The increase in A feed could lead to changes in the reactor’s operation, affecting the stripper temperature and steam flow as the system attempts to maintain product quality._ However, this root cause does not directly explain the decrease in E Feed. Therefore, this root cause can explain 5 out of the 6 feature deviations. 

### **o1-preview explanation** 

The most plausible root cause is **IDV(13): Reaction Kinetics & Slow Drift** . A gradual deterioration of reaction kinetics, possibly from catalyst deactivation or fouling, would reduce the conversion rates of reactants to products. To maintain the desired production levels, the control system responds by increasing the **A feed load** and **A Feed** , supplying more reactant A to the reactor. This explains the significant increases in these features. The slight decrease in **E Feed** may result from an accumulation of unreacted E in the reactor due to slower reaction rates, prompting the control system to reduce its feed rate. The reduced reaction efficiency leads to higher concentrations of unreacted reactants in the reactor effluent. Consequently, the control system increases the **Stripper steam valve** opening and the **Stripper Steam Flow** to enhance the removal of residual reactants from the product stream. This accounts for the observed increases in these features. The increased steam flow raises the **Stripper Temperature** , aligning with the observed temperature rise. All six of the top features can be explained by **IDV(13)** . 

Figure 4: An illustrative example where neither model is able to identify the correct root cause. The top six feature changes and the explanation of GPT-4o and o1-preview to the top six feature changes of Fault 10 C Feed Temperature (Stream 4) & Random Variation when the 15 root causes are provided. The hallucinated explanations are shown in italics. 

offered a more detailed sequence of events, explicitly tying each feature deviation to the control system’s response and providing a clear causal pathway for fault propagation. This demonstrates o1-preview’s advantage in reasoning and generating deterministic, system-oriented explanations, although both models were successful in this case. 

Figure 4 shows the failure of both GPT-4o and o1-preview to identify 

16 

the correct root cause (Fault 10: C Feed Temperature Random Variation). It highlights important limitations in both the LLMs’ reasoning and the feature selection process. GPT-4o’s explanation lacked quantitative rigor and causal clarity, failing to explicitly connect the observed feature changes to the hypothesized root cause. Instead, it provides a vague connection between the increase in A feed load and A feed rate to the changes in stripper steam flow and temperature, which appears to be a hallucination rather than a reasoned deduction. This hallucinated explanation is highlighted in italics in Figure 4. This lack of precision resulted in an incomplete and unconvincing explanation that do not account for all observed feature changes. 

On the other hand, o1-preview produced a plausible and systematic explanation based on chemical engineering knowledge, attributing the deviations to reaction kinetics and slow drift (IDV(13)). However, despite its coherence, this explanation was incorrect because the identified features—such as the stripper steam flow and A Feed—are not directly related to the actual root cause (C Feed Temperature Random Variation). The model’s reasoning was limited by the feature set provided by PCA, which failed to capture variables directly linked to the root cause. Consequently, o1-preview attempted to construct an alternative causal pathway to explain the deviations, ultimately leading to a misclassification. This failure underscores the dual challenges in fault diagnosis: (1) the need for the LLM to reason effectively even when feature relationships to the root cause are indirect, and (2) the limitations of PCA in identifying features that are strongly tied to the true root cause. Addressing these issues requires improving both feature selection methodologies and LLM reasoning capabilities to ensure robust and accurate fault explanations. 

## _5.3. Results of the General Reasoning Prompt_ 

Similarly, the _General Reasoning Prompt_ is used to generate the top three root causes with explanations. 

## _5.3.1. Quantitative evaluation of the classification accuracy_ 

The results of _General Reasoning Prompt_ , summarized in Table 2, highlight the performance of GPT-4o and o1-preview when not restricted to the 15 predefined root causes. The root causes generated by the LLMs that are related to the ground truth of the faults are highlighted in bold in Table 2. Both models identified the correct or related root cause in 8 out of the 11 faults identified by the PCA. This demonstrates their capacity to generalize 

17 

Table 2: A summary of the top three root causes generated by GPT-4o and o1-preview using the general reasoning prompt. The root causes related to the ground truth of each fault are highlighted in bold. 

|Faults|GPT-4o|o1-preview|
|---|---|---|
|1|**Malfunction in the Feed System A**<br>Control System Malfunction<br>**Process Stream Disturbance**|**Increased Component C in Feed Stream 4**<br>Malfunction in the Recycle Stream<br>**Partial Blockage in Component A Feed Line**|
|2|Increased Reactor Pressure or Flow Rate<br>Malfunction in the Vapor-Liquid Separator<br>Change in Feed Composition or Quality|**Increased Ingress of Inert B into the System**<br>Condenser Inefciency Leading to Reduced Condensation<br>Compressor Malfunction Leading to Reduced Recycle Flow|
|3|_\_|_\_|
|4|_\_|_\_|
|5|Increased Reaction Temperature<br>**Malfunction in Cooling System**<br>Feed Composition Change|Decrease in E Feed Supply<br>**Cooling Inefciency in the Separator Condenser**<br>Decrease in Component C Supply to Reactor|
|6|**Malfunction in A Feed Control System**<br>Mechanical Issue in Compressor<br>Supply Issue with Reactant E|Compressor Recycle Valve Malfunction<br>Compressor Underperformance Due to Mechanical Fault<br>**Partial Blockage in A Feed Line**|
|7|**Feed Supply Disruption**<br>Reactor Catalyst Deactivation<br>Cooling System Malfunction|**Partial Blockage in A and C Feed Line**<br>**Malfunctioning A and C Feed Control Valve**<br>Leak in the Reactor System|
|8|**Malfunction in the A Feed System**<br>**Control System Malfunction**<br>Issue with the Recycle Compressor|**Decrease in Component C Feed**<br>Catalyst Deactivation in Reactor<br>Instrumentation Error in Component C Measurements|
|9|_\_|_\_|
|10|Increased A Feed Rate<br>Control System Malfunction<br>Stripper Performance Issue|Decrease in E Feed Rate Due to Supply Limitation<br>Increase in A Feed Setpoint<br>Operational Issue in the Stripper|
|11|**Increased Reaction Rates Due to Temper-**<br>**ature Rise**<br>Inefcient Cooling in the Separator<br>Feed Composition Imbalance|Increase in D Feed Rate<br>**Blockage in Reactor Cooling Water Valve**<br>Increase in D Feed Temperature|
|12|**Inefcient Heat Removal in the Separator**<br>Change in Feed Composition<br>Reactor Operating Conditions|Increase in Inert Component B in Feed Stream 4<br>Decrease in A or C Concentration in Feed Stream 4<br>Decreased Reactor Catalyst Activity|
|13|Feed Composition Change<br>Reactor Malfunction<br>Control System Malfunction|Decrease in D Feed Rate (Stream 2)<br>Blockage or Restriction in D Feed Line<br>Malfunctioning Controller Decreasing D Feed Load|
|14<br>15|**Cooling System Malfunction**<br>Feed Composition Change<br>Reaction Kinetics Shift<br>_\_|**Decreased Reactor Cooling Efciency**<br>Increase in Inert Component B Feed to Reactor<br>Decrease in Component C Feed to Reactor<br>_\_|



18 

reasoning beyond fixed fault lists, which is critical in practical scenarios where previously unseen faults may arise. However, neither model is able to identify the correct root causes for Faults 10 and 13, illustrating a key limitation. In these cases, the inability to correlate the observed feature deviations with the ground truth highlights the challenge of linking indirect feature changes to the actual fault mechanism. We will discuss these limitations in detail in our qualitative evaluation. 

## _5.3.2. Qualitative evaluation of the explanations_ 

Similar to Section 5.2.2, we choose two faults to demonstrate the advantages and limitations of the two models. The rest of the fault reports follow a similar pattern and can be found in the supplementary material. 

Figure 5 shows how GPT-4o and o1-preview explain Fault 2 when the 15 predefined root causes are not provided. GPT-4o’s explanation lacks specificity and tends toward vague reasoning. While it proposes a scenario involving an increased reactor pressure or flow rate, it does not identify the affected components or streams precisely. Furthermore, it fails to establish a clear causal relationship between the proposed root cause and the observed feature changes. For example, it claims that an increase in reactor flow rate _results in_ more component B being flowed to the reactor. This is problematic because component B itself represents the reactor’s inflow, making the proposed causal linkage nonsensical. Furthermore, it claims that “The increase in A and E feed loads could be a response to maintain reaction rates and product output under the new conditions.” However, it does not explain why the new conditions make the A and E feed loads increase. The response suggests that GPT-4o may be compensating for insufficient reasoning with overly general statements. 

In contrast to GPT-4o, o1-preview provides a thorough, causally grounded explanation that aligns closely with both the observed data and fundamental chemical engineering principles. As shown in the figure, o1-preview pinpoints an increased ingress of inert Component B into the system. The increase in B causes the rise of B in the recycle loop, prompting the control system to mitigate the accumulation of B by increasing the Purge Valve opening and consequently the Purge Rate and the concentration of B in the purge. The explanation also addresses the reactive species balance within the reactor. With inert B diluting the reactor, the control system compensates by increasing the feed loads of reactants A and E. o1-preview is able to explain all the six feature deviations from the normal operating conditions. Overall, the 

19 

### **Top six feature changes** 

The **Component B in Purge** increased by 5 _._ 63%, the **Purge Rate** by 20 _._ 96%, and the **Purge Valve** by 20 _._ 86%. Additionally, **Component B to Reactor** increased by 4 _._ 17%, the **E Feed Load** by 1 _._ 67%, and the **A Feed Load** showed the most significant increase at 30 _._ 74%. 

### **GPT-4o explanation** 

**Root Cause 1: Increased Reactor Pressure or Flow Rate:** An increase 

in reactor pressure or flow rate could lead to higher purge rates and changes in the composition of the purge stream. The control system might respond by increasing the purge valve opening to manage the pressure, leading to the observed increase in purge rate and component B in the purge. _The increased flow rate could also result in more component B being carried over to the reactor, ex-_ 

_plaining the increase in component B to the reactor. The increase in A and E feed loads could be a response to maintain reaction rates and product output under the new conditions._ This root cause can explain all six feature deviations. 

### **o1-preview explanation** 

**Root Cause 1: Increased Ingress of Inert** **_B_ into the System** An unexpected increase in the influx of inert Component _B_ into the process could explain the observed feature deviations. This may result from contamination in one of the feed streams, particularly Stream 4, which includes a mixture of _A_ , _B_ , and _C_ . If the concentration of _B_ in this stream increases, more inert _B_ enters the reactor feed, leading to an elevated mole percentage of Component _B_ to the Reactor (Feature 4), as observed (+4.17%). The accumulation of inert _B_ in the process causes higher concentrations of _B_ in the recycle loop. To prevent excessive buildup of inert gas, the control system responds by increasing the Purge Valve opening (Feature 3, +20.86%) to remove the excess inert. This action increases the Purge Rate (Feature 2, +20.96%) and results in higher concentrations of Component _B_ in the Purge stream (Feature 1, +5.63%). The increased presence of inert _B_ in the reactor feed dilutes the concentrations of reactive species, potentially reducing the overall reaction rates. The control system compensates for this by increasing the feed rates of reactants _A_ and _E_ . This is evidenced by the significant increase in _A_ Feed Load (Feature 6, +30.74%) and the smaller increase in _E_ Feed Load (Feature 5, +1.67%). Since _A_ participates in all reactions and is more critical, a larger increase in its feed rate is justified. Therefore, this root cause explains all six observed feature deviations. **Features explained:** 6/6. 

Figure 5: The top six feature changes and the explanation of GPT-4o and o1-preview to the top six feature changes of Fault 2 (B Composition, A/C Ratio Constant (Stream 4) & Step) when the 15 root causes are not provided. The hallucinated explanations are highlighted in italics. 

20 

o1-preview’s explanation is more granular, causal, and coherent compared with GPT-4o. 

### **Top six feature changes** 

The **Stripper Pressure** increased by 1 _._ 58%, the **Reactor Pressure** increased by 1 _._ 84%, and the **Product Separator Pressure** increased by 1 _._ 92%. In contrast, the **Component D in Purge** decreased by 17 _._ 85%, the **Component D to Reactor** decreased by 3 _._ 31%, and the **Component F in Purge** decreased by 2 _._ 17%. 

### **GPT-4o explanation** 

### **Root Cause 1: Feed Composition Change** 

- A change in the feed composition, particularly a reduction in component D, could explain several of the observed deviations. The decrease in compo- 

- nent D to the reactor and in the purge stream suggests that less D is available for reaction, potentially due to a feed supply issue or a change in the feed stream composition. _This could lead to increased reactor pressure as_ 

- _the reaction rates are affected, causing a buildup of unreacted gases. The in-_ 

- _creased pressure in the reactor could propagate downstream, affecting the product separator and stripper pressures._ This root cause can explain the deviations in the reactor pressure, product separator pressure, component D in purge, and component D to reactor, accounting for 4 out of the 6 features. 

### **o1-preview explanation** 

- **Root Cause 1: Decrease in D Feed Rate (Stream 2)** A decrease in the D feed rate through Stream 2 directly leads to a reduction in the amount of Component 

- D entering the reactor, explaining the 3.31% decrease in Component D to Reactor. With less D fed into the reactor, there is less unreacted D available to exit via the purge stream, accounting for the significant 17.85% decrease in Component D in Purge. The shortage of D affects Reactions 1 and 4, which consume D, resulting in decreased reaction rates. This decrease leads to an accumulation of unreacted gaseous reactants, such as A and C, increasing the reactor pressure by 1.84%. 

- The elevated reactor pressure propagates downstream, causing increases in the 

- product separator pressure by 1.92% and stripper pressure by 1.58%. Additionally, the reduced availability of D diminishes the production of byproduct F through Reaction 4 (3D _→_ 2F), explaining the slight 2.17% decrease in Component F in Purge. Therefore, this root cause explains all six observed feature deviations. 

Figure 6: An illustrative example where neither model is able to identify the correct root cause. The top six feature changes and the explanation of GPT-4o and o1-preview to the top six feature changes of Fault 13 Reaction Kinetics & Slow Drift when the 15 root causes are not provided. The hallucinated explanations are highlighted in italics. 

Figure 6 showcases a scenario where neither GPT-4o nor o1-preview is able to identify the correct root cause for Fault 13 (Reaction Kinetics & Slow Drift). The top six feature changes, primarily related to pressure deviations 

21 

and changes in Component D and F concentrations, are misattributed to alternative root causes by both models. 

GPT-4o attributes the deviations to a D feed increase, providing an explanation for four out of the six feature changes. However, its explanation lacks justification and shows signs of hallucination. The hallucinated sentences are highlighted in italics. For example, it claims that the decrease in feed D to the reactor “could lead to increased reactor pressure as the reaction rates are affected” but fails to justify why the reactor pressure gets increased due to the decrease in feed D. It further claims that “The increased pressure in the reactor could propagate downstream, affecting the product separator and stripper pressures” but does not reason explicitly how the separator and stripper pressures can be affected. 

o1-preview provides a more plausible explanation by hypothesizing that a decrease in the D feed rate (Stream 2) is the root cause. It attributes the reduction in reactor pressure to a shortage of D, which affects two of the reactions and leads to the accumulation of unreacted gaseous reactants and thus increased reactor pressure. The increase in reactor pressure propagates downstream, raising the pressures in the separator and stripper. The reduced availability of D also explains the reduction in the production of byproduct F through one of the reactions, accounting for the observed decrease in F in the purge stream. In summary, o1-preview concludes with the same root cause as GPT-4o (decrease in D feed) but is able to provide an explanation with stronger causal links. 

The failure of both models underscores a limitation in the general reasoning prompt setting: the inability of the PCA-selected features to capture the subtle dynamics of reaction kinetics changes. Both models rely on indirect indicators (e.g., feed changes or pressure increases) to construct plausible but incorrect explanations. This highlights the importance of integrating richer domain knowledge or alternative feature selection methods to better represent complex root causes, particularly those involving gradual or non-obvious changes like reaction kinetics drift. 

## **6. Conclusions** 

In this paper, we present _FaultExplainer_ , a tool for diagnosing and explaining faults in the Tennessee Eastman Process (TEP). _FaultExplainer_ combines real-time sensor data visualization, _T_<sup>2</sup> fault detection and feature 

22 

contribution analysis, and an interactive chat interface powered by large language models (LLMs). Users can monitor sensor data, introduce faults into the process, and visualize their progression through _T_<sup>2</sup> plots. The interactive chat interface provides grounded explanations based on process data and allows users to ask qualitative questions about fault causes and mitigation strategies, making advanced diagnostic methods more accessible to engineers and operators. 

_FaultExplainer_ offers several advantages. First, its integration of realtime sensor data and fault detection enhances situational awareness, enabling users to observe and understand deviations in process behavior as they occur. Second, the use of LLMs allows the system to provide explanations that are both grounded in process data and tailored to the user’s queries, bridging the gap between raw statistical analysis and actionable insights. Third, its ability to accommodate both predefined root causes and general reasoning makes it flexible for diagnosing faults that may not have been previously encountered. 

Despite these strengths, _FaultExplainer_ has limitations. The tool relies on Principal Component Analysis (PCA) for feature selection, which may fail to capture subtle or indirect relationships between process variables and root causes, as seen in certain faults where neither model correctly identified the root cause. Furthermore, while LLMs can generate plausible explanations, they sometimes produce overly generalized or hallucinated responses, especially when feature data do not directly relate to the fault mechanism. 

Future improvements to _FaultExplainer_ could address these limitations. First, integrating advanced feature selection techniques, such as domaininformed feature engineering or causal inference, could enhance the model’s ability to detect faults linked to complex root causes. Second, incorporating fine-tuned LLMs trained on chemical process data could improve the specificity and reliability of explanations. These enhancements would further solidify _FaultExplainer_ ’s role as a powerful tool for real-time fault diagnosis and explanation in industrial processes. 

## **7. Acknowledgements** 

The authors gratefully acknowledge the Purdue Process Safety and Assurance Center (P2SAC) for providing financial support for this work. 

23 

## **References** 

- Alanqar, A., Durand, H., Christofides, P.D., 2017. Fault-tolerant economic model predictive control using error-triggered online model identification. Industrial & Engineering Chemistry Research 56, 5652–5667. doi: `10.1021/ acs.iecr.7b00576` . 

- Balhorn, L.S., Degens, K., Schweidtmann, A.M., 2024. Graph-to-sfiles: Control structure prediction from process topologies using generative artificial intelligence. arXiv preprint arXiv:2412.00508 . 

- Bhakte, A., Chakane, M., Srinivasan, R., 2023. Alarm-based explanations of process monitoring results from deep neural networks. Computers & Chemical Engineering 179, 108442. 

- Bhakte, A., Pakkiriswamy, V., Srinivasan, R., 2022. An explainable artificial intelligence based approach for interpretation of fault classification results from deep neural networks. Chemical Engineering Science 250, 117373. 

- Bursac, Z., Gauss, C.H., Williams, D.K., Hosmer, D.W., 2008. Purposeful selection of variables in logistic regression. Source Code for Biology and Medicine 3, 17. doi: `10.1186/1751-0473-3-17` . 

- Chen, H., Constante-Flores, G.E., Li, C., 2024. Diagnosing infeasible optimization problems using large language models. INFOR: Information Systems and Operational Research 62, 573–587. 

- Chiang, L.H., Russell, E.L., Braatz, R.D., 2000. Fault detection and diagnosis in industrial systems. Springer Science & Business Media. 

- Chiang, L.H., Russell, E.L., Braatz, R.D., 2001. Fault Detection and Diagnosis in Industrial Systems. Springer London. doi: `10.1007/ 978-1-4471-0347-9` . 

- Choi, S.W., Martin, E.B., Morris, A.J., Lee, I.B., 2005. Fault detection based on a maximum-likelihood principal component analysis (pca) mixture. Industrial & engineering chemistry research 44, 2316–2327. 

- Downs, J.J., Vogel, E.F., 1993. A plant-wide industrial process control problem. Computers & Chemical Engineering 17, 245–255. 

24 

- Gertler, J.J., Monajemy, R., 1995. Generating directional residuals with dynamic parity relations. Automatica 31, 627–635. 

- Geymayr, J.A.B., Ebecken, N.F.F., 1995. Fault-tree analysis: a knowledgeengineering approach. IEEE Transactions on Reliability 44, 37–45. 

- Hale, W.T., Safikou, E., Bollas, G.M., 2022. Inference of faults through symbolic regression of system data. Computers & Chemical Engineering 157, 107619. doi: `10.1016/j.compchemeng.2021.107619` . 

- Harinarayan, R.R.A., Shalinie, S.M., 2022. Xfddc: explainable fault detection diagnosis and correction framework for chemical process systems. Process Safety and Environmental Protection 165, 463–474. doi: `10.1016/ j.psep.2022.07.019` . 

- Hart, S., 1989. Shapley value, in: Game theory. Springer, pp. 210–216. 

- Hirtreiter, E., Schulze Balhorn, L., Schweidtmann, A.M., 2024. Toward automatic generation of control structures for process flow diagrams with large language models. AIChE Journal 70, e18259. 

- Jia, Q., Zhang, Y., 2016. Quality-related fault detection approach based on dynamic kernel partial least squares. Chemical Engineering Research and Design 106, 242–252. 

- Jiang, T., Khorasani, K., Tafazoli, S., 2008. Parameter estimation-based fault detection, isolation and recovery for nonlinear satellite models. IEEE Transactions on control systems technology 16, 799–808. 

- Kumari, P., Bhadriraju, B., Wang, Q., Kwon, J.S.I., 2022a. A modified bayesian network to handle cyclic loops in root cause diagnosis of process faults in the chemical process industry. Journal of Process Control 110, 84–98. doi: `10.1016/j.jprocont.2021.12.011` . 

- Kumari, P., Wang, Q., Khan, F., Kwon, J.S.I., 2022b. A direct transfer entropy-based multiblock bayesian network for root cause diagnosis of process faults. Industrial & Engineering Chemistry Research doi: `10.1021/ acs.iecr.2c02320` . 

- Li, C., Wong, C., Zhang, S., Usuyama, N., Liu, H., Yang, J., Naumann, T., Poon, H., Gao, J., 2023. Llava-med: Training a large language-and-vision assistant for biomedicine in one day. arXiv preprint arXiv:2306.00890 . 

25 

- Lu, Y.C., Varghese, A., Nahar, R., Chen, H., Shao, K., Bao, X., Li, C., 2024. scchat: A large language model-powered co-pilot for contextualized single-cell rna sequencing analysis. bioRxiv , 2024–10. 

- Mittelstadt, B., Russell, C., Wachter, S., 2019. Explaining explanations in AI, in: FAT* 2019 - Proceedings of the 2019 Conference on Fairness, Accountability, and Transparency, Association for Computing Machinery, Inc. pp. 279–288. doi: `10.1145/3287560.3287574` . 

- Murdoch, W.J., Singh, C., Kumbier, K., Abbasi-Asl, R., Yu, B., 2019. Definitions, methods, and applications in interpretable machine learning. Proceedings of the National Academy of Sciences of the United States of America 116, 22071–22080. doi: `10.1073/pnas.1900654116` . 

OpenAI, 2023. Gpt-4 technical report . 

- OpenAI, 2024a. Hello gpt-4o. URL: `https://openai.com/index/ hello-gpt-4o/` . accessed: 2024-12-17. 

- OpenAI, 2024b. Openai o1. URL: `https://openai.com/o1/` . accessed: 2024-12-17. 

- Peterson, L., 2009. K-nearest neighbor. Scholarpedia 4, 1883. doi: `10.4249/ scholarpedia.1883` . 

- Quinlan, J., 1987. Simplifying decision trees. International Journal of ManMachine Studies 27, 221–234. doi: `10.1016/S0020-7373(87)80053-6` . 

- Ribeiro, M.T., Singh, S., Guestrin, C., 2016. ”Why should i trust you?” Explaining the predictions of any classifier, in: Proceedings of the ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, Association for Computing Machinery. pp. 1135–1144. doi: `10.1145/ 2939672.2939778` . 

- Rieth, C.A., Amsel, B.D., Tran, R., Cook, M.B., 2017. Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation. URL: `https://doi.org/10.7910/DVN/6C3JR1` , doi: `10.7910/DVN/ 6C3JR1` . 

- Sacks, E., 1988. Qualitative analysis by piecewise linear approximation. Artificial Intelligence in Engineering 3, 151–155. 

26 

- Slack, D., Krishna, S., Lakkaraju, H., Singh, S., 2023. Explaining machine learning models with interactive natural language conversations using TalkToModel. Nature Machine Intelligence 2023 , 1–11URL: `https://www.nature.com/articles/s42256-023-00692-8` , doi: `10.1038/s42256-023-00692-8` . 

- Sun, W., Paiva, A.R.C., Xu, P., Sundaram, A., Braatz, R.D., 2020. Fault detection and identification using bayesian recurrent neural networks. Computers & Chemical Engineering 141, 106991. 

- Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhosale, S., Bikel, D., Blecher, L., Ferrer, C.C., Chen, M., Cucurull, G., Esiobu, D., Fernandes, J., Fu, J., Fu, W., Fuller, B., Gao, C., Goswami, V., Goyal, N., Hartshorn, A., Hosseini, S., Hou, R., Inan, H., Kardas, M., Kerkez, V., Khabsa, M., Kloumann, I., Korenev, A., Koura, P.S., Lachaux, M.A., Lavril, T., Lee, J., Liskovich, D., Lu, Y., Mao, Y., Martinet, X., Mihaylov, T., Mishra, P., Molybog, I., Nie, Y., Poulton, A., Reizenstein, J., Rungta, R., Saladi, K., Schelten, A., Silva, R., Smith, E.M., Subramanian, R., Tan, X.E., Tang, B., Taylor, R., Williams, A., Kuan, J.X., Xu, P., Yan, Z., Zarov, I., Zhang, Y., Fan, A., Kambadur, M., Narang, S., Rodriguez, A., Stojnic, R., Edunov, S., Scialom, T., 2023. Llama 2: Open Foundation and Fine-Tuned Chat Models . 

- Tu, T., Azizi, S., Driess, D., Schaekermann, M., Amin, M., Chang, P.C., Carroll, A., Lau, C., Tanno, R., Ktena, I., et al., 2024. Towards generalist biomedical ai. NEJM AI 1, AIoa2300138. 

- Vedam, H., Venkatasubramanian, V., 1997. Signed digraph based multiple fault diagnosis. Computers & Chemical Engineering 21, S655–S660. doi: `10.1016/S0098-1354(97)87577-1` . 

- Venkatasubramanian, V., Rengaswamy, R., Kavuri, S.N., 2003a. A review of process fault detection and diagnosis: Part ii: Qualitative models and search strategies. Computers & Chemical Engineering 27, 313–326. 

- Venkatasubramanian, V., Rengaswamy, R., Kavuri, S.N., Yin, K., 2003b. A review of process fault detection and diagnosis: Part iii: Process history based methods. Computers & Chemical Engineering 27, 327–346. 

27 

- Venkatasubramanian, V., Rengaswamy, R., Yin, K., Kavuri, S.N., 2003c. A review of process fault detection and diagnosis: Part i: Quantitative model-based methods. Computers & Chemical Engineering 27, 293–311. 

- Wachter, S., Mittelstadt, B., Russell, C., 2017. Counterfactual Explanations without Opening the Black Box: Automated Decisions and the GDPR . 

- Watanabe, K., Himmelblau, D., 1983a. Fault diagnosis in nonlinear chemical processes. part ii. application to a chemical reactor. AIChE Journal 29, 250–261. 

- Watanabe, K., Himmelblau, D.M., 1983b. Fault diagnosis in nonlinear chemical processes. part i. theory. AIChE Journal 29, 243–249. doi: `10.1002/ aic.690290211` . 

- Welch, G., Bishop, G., et al., 1995. An introduction to the kalman filter . 

- Yin, X., Liu, J., 2017. Distributed output-feedback fault detection and isolation of cascade process networks. AIChE Journal 63, 4329–4342. doi: `10.1002/aic.15791` . 

- Zhang, S., Qiu, T., 2022. A dynamic-inner convolutional autoencoder for process monitoring. Computers & Chemical Engineering 158, 107654. 

- Zhang, Z., Zhao, J., 2017. A deep belief network based fault diagnosis model for complex chemical processes. Computers & Chemical Engineering 107, 395–407. 

28 

