Available online at www.sciencedirect.com 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0001-01.png)


# **ScienceDirect** 

IFAC PapersOnLine 59-10 (2025) 536–541 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0001-04.png)


## **<mark>Uncertainty-Aware Fault Diagnosis with Conformal Prediction</mark>** 

**<mark>Amine Heddoub</mark>**<sup>*****</sup> **<mark>, Abdoul Rahime Diallo</mark>**<sup>*****</sup> **<mark>, Lazhar Homri</mark>**<sup>*****</sup> **<mark>, Jean-Yves Dantan</mark>**<sup>*****</sup> **<mark>, Ali Siadat</mark>**<sup>***, ****</sup> 

_*Arts et Metiers Institute of Technology, Université de Lorraine, LCFC, F-57070 Metz, France_ 

_** Arts et Métiers Campus de Rabat, Technopolis, Campus UM6P, Sala Al Jadida, Morocco_ 

<u>(e-mail : firstname.name@ensam.eu).</u> 

**Abstract** : In modern process industries, ensuring reliable fault diagnosis is essential for maintaining product quality, operational safety, and cost efficiency. Traditional data-driven classification methods perform well under stable conditions but do not provide any mechanisms to quantify uncertainty when the model lacks confidence in its predictions, which is critical in real-world industrial environments. Conformal prediction addresses this limitation by providing rigorous uncertainty sets of these classification techniques. This paper compares classical classification methods with their conformal counterparts using two widely recognized benchmark datasets: the Tennessee Eastman Process (TEP) and a Continuous Stirred Tank Reactor (CSTR). We focus on identifying fault types and evaluate each approach in terms of accuracy, misclassification rate and coverage. Our findings demonstrate that conformal prediction improves the confidence and robustness of fault diagnosis, providing classifier with a more reliable and uncertaintyaware diagnostic framework for dynamic industrial environments. 

Copyright © 2025 The Authors. This is an open access article under the CC BY-NC-ND license (https://creativecommons.org/licenses/by-nc-nd/4.0/) 

_Keywords_ : Process monitoring, Fault diagnosis, Uncertainty quantification, Conformal prediction, Machine learning 

### 1. INTRODUCTION 

In manufacturing industries, there is a growing need to improve product quality, reduce rejection rates, and comply with strict safety and environmental standards. Practices that were once considered sufficient are no longer adequate. To meet these higher standards, modern industrial systems rely on monitoring multiple interconnected variables to ensure operational efficiency and respect regulations (Chiang et al., 2001). This increasing complexity calls for advanced monitoring approaches to guarantee safe and efficient operations. Process monitoring typically involves four steps: detecting when something is wrong (fault detection), identifying where the problem is (fault isolation), and determining the type of fault (fault identification). Fault isolation and identification together make up fault diagnosis, which is followed by system recovery. These steps are essential to prevent faults from escalating into failures that could disrupt production, incur financial losses, or harm the environment (Isermann and Ball, 1997). 

The key steps of process monitoring are often grouped under the term Fault Detection and Diagnosis (FDD). FDD methods are classified into three categories: model-based, knowledgebased, and data-driven (Chiang et al., 2001). Model-based methods rely on mathematical models to predict normal system behavior and compare it with the actual behavior, while knowledge-based approaches use predefined rules and expert knowledge. However, these methods often struggle with the complexity of modern industrial systems. In contrast, datadriven methods have become increasingly popular because they utilize large volumes of data, which are now widely available (Adil et al., 2016). The advent of Industry 4.0 has further amplified the capabilities of data-driven methods. The advancement of technologies like the Internet of Things (IoT) and artificial intelligence has facilitated real-time monitoring of industrial systems. These technologies also allow for the analysis of vast amounts of data from interconnected devices, 

improving the efficiency and reliability of industrial operations (Ciancio et al., 2022). Among data-driven techniques, reconstruction-based approaches like Principal Component Analysis (PCA), Independent Component Analysis (ICA) and Autoencoder have been widely used for FDD, particularly in scenarios with limited historical fault data (Lakshmi Priya Palla and Kumar Pani, 2023; Li et al., 2020). Fisher Discriminant Analysis (FDA), widely applied in fault diagnosis, was shown to outperform PCA because it maximizes the separation between multiple classes. Chiang et al., 2001 highlighted its advantages in this context. Later, Lou et al., 2022 demonstrated the effectiveness of FDA and its variants, including Quadratic Discriminant Analysis (QDA), in fault diagnosis, reporting promising results. Machine learning algorithms like Random Forest (RF) further enhance diagnostic accuracy, especially when integrated with optimization techniques like genetic algorithms (Yang et al., 2008) . Despite these advancements, traditional data-driven methods often fail to provide a measure of uncertainty in their predictions, a critical limitation in high-stakes industrial environments. Conformal Prediction (CP), as introduced by Vovk et al., (2005), addresses this issue by generating confidence sets for predictions, thereby enhancing their reliability. By integrating CP with classification methods, it becomes possible to improve fault diagnosis while providing robust uncertainty quantification. 

This paper examines the application of CP in fault diagnosis using two widely recognized benchmark datasets. It compares conventional diagnostic methods (FDA, QDA, and RF) with their CP-enhanced counterparts to evaluate improvements in accuracy, reliability, and uncertainty quantification. 

This is how the rest of the paper is structured. Some traditional data-driven techniques are described in Section 2 with a background of uncertainty quantification in fault diagnosis. The proposed CP approach is presented in Section 3. Section 4 presents the application results to the two benchmark 

2405-8963 Copyright © 2025 The Authors. This is an open access article under the CC BY-NC-ND license. Peer review under responsibility of International Federation of Automatic Control. 10.1016/j.ifacol.2025.09.092 

_Amine Heddoub  et al. / IFAC PapersOnLine 59-10 (2025) 536–541_ 

537 

datasets, CSTR and TEP. The conclusion and perspectives are finally summed up in Section 5. 

### 2. RELATED WORK 

### _2.1 Fault diagnosis:_ 

Fault diagnosis is generally a classification problem, where the goal is to identify faults based on patterns in online data. This review focuses on some data-driven approaches used in this context. 

Some works showed the effectiveness of discriminant analysis, which has inherent superiority in fault classification tasks due to its structured and statistical foundation (Lou et al., 2022). As a supervised classification technique, it employs a discriminant function to calculate a confidence score, indicating how well a data point belongs to a specific class (Atoui and Cohen, 2021). Within this framework, quadratic discriminant analysis (QDA) is a widely used variant for fault diagnosis. Other extensions, such as Fisher discriminant analysis (FDA) and kernel Fisher discriminant (KFD), further enhance the ability to identify low-dimensional representations of data while maintaining discriminative power. 

Other works highlighted the utility of RF classifiers, which are ensemble-based machine learning algorithms that classify data by building multiple decision trees during training. Every tree votes for a certain class, and the final prediction is determined by the proportion of trees favoring a class. RF has been widely used in various fault diagnosis tasks. For instance, it has demonstrated effectiveness in gas turbine fault diagnosis(Pei et al., 2022). Enhanced RF, which integrate static and dynamic information (Deng et al., 2022), have also shown superior performance in diagnosing faults in complex industrial processes. 

Meanwhile, several researchers focused on deep learning models, which excel at extracting features from raw data, making them ideal for complex datasets like images or timeseries signals. These methods have been applied to fault diagnosis with high success, especially in tasks involving unstructured data, such as diagnosing faults in bearings using frequency spectrum (Li et al., 2023). However, deep learning models often underperform on tabular data, which is common in industrial systems (Shwartz-Ziv and Armon, 2021). 

### _2.2 Uncertainty quantification in fault diagnosis:_ 

Uncertainty quantification (UQ) is essential to fault diagnosis, as it ensures reliability and safety by addressing ambiguities inherent in diagnostic predictions. Without proper UQ, misclassifications can lead sometimes to catastrophic failures in industrial systems. Advanced fault diagnosis frameworks rely on UQ to align predictions with confidence measures that support critical decision-making processes. The necessity of UQ has been underscored by Zio, (2018), who emphasized its role in achieving dependable industrial process monitoring. Conventional UQ methods have established a diverse range of approaches, including evidential theory, Bayesian methods, and ensemble techniques. Evidential theory, grounded in Dempster-Shafer Theory (DST), excels at combining uncertain evidence from various sources, offering flexibility in 

dealing with incomplete data. However, it suffers from computational complexity and lacks the intuitive probabilistic interpretation often desired in real-time applications (Zhou et al., 2023). Bayesian methods model uncertainty probabilistically, with techniques like Monte Carlo dropout providing vision into the uncertainty of deep learning models. While effective, these methods require computational resources and rely heavily on prior assumptions, which may introduce biases (Lin and Li, 2024). Ensemble methods, another prominent category, combine outputs from multiple models to estimate uncertainty. These approaches effectively capture both aleatoric and epistemic uncertainties but are often constrained by their high computational demands and storage requirements (Lakshminarayanan et al., 2017). A major limitation of these uncertainty quantification techniques is the absence of formal guarantees (Karimi and Samavi, 2023). 

A promising alternative, CP, has been proposed to address some of the limitations of existing uncertainty quantification methods. CP constructs prediction sets with theoretical coverage guarantees at predefined confidence levels, making it an interesting approach for handling uncertainty, irrespective of the underlying model (Angelopoulos and Bates, 2022). Its model-agnostic nature enables smooth integration with any classifier, and its ability to produce set-valued predictions in uncertain scenarios makes it valuable for fault diagnosis. In this study, we integrate CP into conventional fault diagnosis classifiers and evaluate its impact using benchmark datasets from the Tennessee Eastman Process (TEP) and a Continuous Stirred Tank Reactor (CSTR). We compare classification accuracy, misclassification rates, and coverage, demonstrating that the incorporation of CP enhances the reliability and robustness of fault diagnosis in dynamic industrial settings. 

### 3. PROPOSED METHODOLOGY 

In traditional classification methods, a model outputs a single class prediction based on the highest confidence score. These scores represent the model's confidence in its prediction, where higher values indicate greater confidence. However, this interpretation may fail to capture uncertainty in ambiguous cases, leading to potential misclassifications. 

In contrast, the proposed classification framework leverages CP to produce prediction sets based on non-conformity scores. These scores quantify how well an observation conforms to a given class, where smaller scores indicate better conformity. The CP framework uses these scores to construct prediction sets at a predefined confidence level, ensuring the true class is included in the set based on a theoretical guarantee of coverage. The size of the set reflects the model's certainty: a smaller set implies higher confidence, while a larger set indicates increased uncertainty. 

The methodology adopted in this article follows the CP framework presented by (Angelopoulos and Bates, 2022), it provides a statistically valid guarantee of coverage. This means that the prediction set generated will contain the true class with a probability of at least 1 −𝛼𝛼. This guarantee is based on the properties of the calibration step and does not rely on assumptions about the data distribution. 

_Amine Heddoub  et al. / IFAC PapersOnLine 59-10 (2025) 536–541_ 

538 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0003-02.png)


Figure 1 : Flowchart for the proposed method 

1. Receive a new observation 𝐱𝐱. 

### _3.1 Conformal prediction approach_ 

To implement this framework in fault diagnosis task, we proceed in three stages: first, CP introduces a non-conformity score to measure how different an observation is to a given class, lower scores indicate higher conformity to the class, and the specific calculation depends on the base model used for classification. Next, we reserve a moderate amount of data for each class, unseen during training, to serve as a calibration set. The size of this set is chosen as a fraction of the total dataset, ensuring that it is large enough to provide stable statistical estimates while preserving sufficient data to train the model. This set is then used to compute non-conformity scores. These scores are sorted, and the quantile 𝑞𝑞ˆ is determined based on the desired confidence level 1 −𝛼𝛼. Specifically, 𝑞𝑞ˆ is computed as the value at the index: 

𝑞𝑞ˆ =<sup>⌈(𝑛𝑛+ 1)(1 −𝛼𝛼)⌉</sup> 𝑞 𝑞𝑞𝑛𝑛𝑞 𝑞 𝑜 𝑞𝑞ℎ𝑞𝑞𝑐𝑐𝑞 𝑞𝑞𝑐 𝑞 𝑞𝑞𝑜𝑜𝑛𝑛𝑠𝑠𝑐𝑐𝑜𝑜𝑐𝑐𝑞𝑞𝑠𝑠 𝑛𝑛 

where 𝑛𝑛 is the number of calibration scores, ⌈⋅⌉ represents the ceiling function, and 𝛼𝛼 is the user-selected error rate in the range of 0 and 1. This quantile acts as a threshold for forming prediction sets. Finally, for a new observation, the framework forms a prediction set containing classes whose nonconformity scores are less than or equal to 𝑞𝑞̂: 

𝑃𝑃𝑐𝑐𝑞𝑞𝑟𝑟𝑞𝑞𝑐𝑐𝑞 𝑜𝑜𝑛𝑛𝑆𝑆𝑞 = {𝐶𝐶𝑘𝑘 : 𝑆𝑆𝑘𝑘(𝑥𝑥) ≤𝑞𝑞̂}. 

if the prediction set contains only one class, the model is confident about its prediction, but if the set contains multiple classes, it indicates uncertainty, and we have a guarantee of 1 −𝛼𝛼 that the true label is in this set. 

### _3.2 The proposed classification scheme:_ 

The proposed classification scheme incorporates CP to provide uncertainty-aware predictions. The flowchart of the proposed scheme is illustrated in Figure 1. This approach ensures that the true fault class is included in the prediction set with a predefined confidence level 1 −𝛼𝛼. The workflow can be summarized as follows: 

### **Offline phase** 

1. Split faulty data into training and calibration sets. 

2. Train the base classifier on the training set. 3. Calibration: 

- Use the calibration set to compute the non-conformity scores for each fault class based on the trained classifier. 

- Sort the non-conformity scores for each class. 

- Determine the quantile 𝑞𝑞ˆ𝑘𝑘 for each class by: 

- 𝑞𝑞ˆ = Quantile at ⌈(𝑛𝑛+1)(𝑛𝑛1−𝛼𝛼)⌉ of the calibration scores {𝑠𝑠1, 𝑠𝑠2, … , 𝑠𝑠𝑛𝑛}. 

- **Online phase** 

2. Compute the non-conformity score 𝑆𝑆𝑘𝑘(𝐱𝐱) for each fault class 𝐶𝐶𝑘𝑘 using the trained classifier. 

3. Prediction set formation: Compare 𝑆𝑆𝑘𝑘(𝐱𝐱) with the precomputed threshold 𝑞𝑞ˆ𝑘𝑘 for each class. 

- Include 𝐶𝐶𝑘𝑘 in the prediction set if 𝑆𝑆𝑘𝑘(𝐱𝐱) ≤𝑞𝑞ˆ𝑘𝑘, otherwise, exclude it. 

### _3.3 Performance metrics:_ 

To evaluate the proposed classification scheme, we use metrics that quantify both prediction accuracy and uncertainty. These metrics, adapted from the literature, are useful for understanding prediction uncertainty and reliability (Angelopoulos and Bates, 2022; Arrieta-Ibarra et al., 2022): 

- 1- Classification Coverage Score (CCS) measures the proportion of samples where the prediction set contains the true label. It is calculated as: 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0003-26.png)


Where 𝑁𝑁, 𝑦𝑦𝑖𝑖 𝑞𝑞𝑛𝑛𝑟𝑟𝐶𝐶𝑖𝑖 are the total number of samples, the true label for the 𝑞𝑞-th sample and the prediction set for the 𝑞𝑞-th sample respectively. The operator 𝟙𝟙{⋅} is the indicator function, which equals 1 if 𝑦𝑦𝑖𝑖 ∈𝐶𝐶𝑖𝑖, and 0 otherwise. This metric quantifies how often the true label is included in the predicted set. A higher CCS indicates better coverage and confidence in the predictions, as it ensures the true label is rarely missed. 

- 2- Classification Mean Width Score (CMWS) calculates the average size of the prediction sets across all samples. It is 1 

- defined as: CMWS = 𝑁𝑁 ∑<sup>𝑁𝑁</sup> 𝑖𝑖=1<sup>|𝐶𝐶</sup> 𝑖𝑖<sup>|</sup> 

Where |𝐶𝐶𝑖𝑖| is the size of the prediction set for the 𝑞𝑞-th sample. This metric assesses how prediction reliability and prediction set size are traded off. A lower CMWS signifies that the model is confident in its predictions. 

- 3- Size-Stratified Coverage (SSC) evaluates the proportion of correctly covered samples for a given prediction set size k. It is calculated as: SSC(𝑘𝑘) = ∑𝑖𝑖∈𝐺𝐺𝑘 𝟙𝟙{𝑦𝑦𝑖𝑖∈𝐶𝐶𝑖𝑖} |𝐺𝐺𝑘𝑘| 

Where 𝐺𝐺𝑘𝑘 = {𝑞𝑞: |𝐶𝐶𝑖𝑖| = 𝑘𝑘} is the set of indices of samples with prediction set size 𝑘𝑘, and |𝐺𝐺𝑘𝑘| is the total number of samples in 𝐺𝐺𝑘𝑘. This metric helps identify how well the model performs for samples with specific prediction set sizes. 

### 4. CASE STUDY 

In this section, the proposed scheme is applied to the two benchmark datasets: the Tennessee Eastman Process (TEP) 

_Amine Heddoub  et al. / IFAC PapersOnLine 59-10 (2025) 536–541_ 

539 

and the Continuous Stirred Tank Reactor (CSTR) datasets. They are widely used in FDD research. The non-conformity scores used in both cases: 

- QDA/FDA: the opposite of the discriminant function value 

- RF:  1 −𝑝𝑝𝑘𝑘, where 𝑝𝑝𝑘𝑘 is the proportion of trees voting for class 𝑘𝑘 

### _4.1 Continuous Stirred Tank Reactor:_ 

The Continuous Stirred Tank Reactor (CSTR) is a common unit operation in chemical plants. It is widely employed in research fields such as simulation, control, and FDD (Botre et al., 2016). Pilario and Cao, (2018) developed a specific CSTR benchmark in SIMULINK, modeling an exothermic first-order reaction A→B using the following mathemat ical framework: 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0004-07.png)


Where, [𝑑𝑑𝑖𝑖, 𝑑𝑑𝑖𝑖, 𝑑𝑑𝑐𝑐𝑖𝑖] represent the inputs, while [C, T, 𝑑𝑑𝑐𝑐, 𝑄𝑄𝑐𝑐] represent the outputs of the model. These variables are the parameters to be monitored. All types of faults are analyzed, as detailed in Table 1. These faults, labeled as Faults from 1 to 12, are classes to be predicted (K = 12). Each class is represented by datasets for training, calibration, and testing, containing 500, 300, and 500 observations respectively. Comprehensive information regarding the CSTR can be found in (Montesuma et al., 2022) and (Li et al., 2020). In this study, FDA, QDA, and RF were trained on the training subset. FDA and QDA estimated class means and covariance matrices, while RF utilized an ensemble of 150 decision trees. Nonconformity scores were calculated from the calibration subset to determine quantile thresholds 𝑞𝑞ˆ𝑘𝑘 for each fault class, ensuring a confidence level of 99% (𝛼𝛼= 0.01). 

Table 1 : Fault scenarios of CSTR process 

|Fault|Description||𝛿|
|---|---|---|---|
|1|Catalyst decay|𝑎= 𝑎0exp(−𝛿𝑑)|0.004|
|2|Heat transfer fouling|𝑏= 𝑏0exp(−𝛿𝑑)|0.005|
|3|Sensor bias|𝑑𝑖 = 𝑑𝑖+ 𝛿𝑑|0.005|
|4|Sensor bias|𝑑𝑖 = 𝑑𝑖+ 𝛿𝑑|0.1|
|5|Sensor bias|𝑑𝑐𝑖 = 𝑑𝑐𝑖+ 𝛿𝑑|0.1|
|6|Sensor bias|𝑑 = 𝑑+ 𝛿𝑑|0.005|
|7|Sensor bias|𝑑 = 𝑑+ 𝛿𝑑|0.1|
|8|Sensor bias|𝑑𝑐 = 𝑑𝑐+ 𝛿𝑑|0.1|
|9|Sensor bias|𝑄𝑐 = 𝑄𝑐+ 𝛿𝑑|-0.2|
|10|Reactant concentration|Δ𝑑𝑖~𝑁(0, 𝛿)|0.005|
|11|Reactant temperature|Δ𝑑𝑖~𝑁(0, 𝛿)|5|
|12|Coolant temperature|Δ𝑑𝑐𝑖~𝑁(0, 𝛿)|5|



The performance of the three methods and their conformal counterparts across 12 fault classes is summarized in Table 2, Figure 3, Figure 3 and Figure 4. The traditional classifiers QDA, FDA, and RF achieve accuracy levels of 89%, 88%, and 84%, respectively, with misclassification rates of 10%, 12%, and 15%, while these models perform 

reasonably well, they lack the ability to handle uncertainty, which limits their reliability in real world fault classification scenarios. 

When CP is applied, the CP-enhanced models QDA-CP, FDACP, and RF-CP demonstrate an improvement, their accuracies increase to 99%, 99%, and 99%, respectively, in cases where the prediction set size is 1. The CCS, which measures how often the true fault is included in the prediction set, is very high, with scores of 98% for QDA-CP, 98% for FDA-CP, and 99% for RF-CP. As uncertainty increases, the prediction set size grows to accommodate samples with uncertainty. Most samples are assigned a set size of 1, but smaller groups receive sets of size 2, or larger. in these cases, the SSC remains high, often exceeding 98% for set sizes up to 6 or 7. Rare cases with a set size of 0 for the two discriminant analysis models, where the model cannot produce any valid prediction, typically correspond to samples that are far from any fault based on the classifier. Additionally, misclassification rates drop to 1.1% for QDA-CP, 1.3% for FDA-CP, and 0.9% for RF-CP, which is very low compared to the traditional methods. 

Table 2 : Metrics of different methods on CSTR 

|Metric|QDA|FDA|RF|QDA-<br>CP|FDA-<br>CP|RF-<br>CP|
|---|---|---|---|---|---|---|
|Accuracy (%)||||99.52|99.505|99.85|
|CCS (%)|89,65|88.06|84.76|98.88|98.65|99.05|
|CMWS|1|1|1|3.147|3.191|2.649|
|Misclassification<br>rate (%)|10|12|15|1.1|1.3|0.9|




![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0004-16.png)


Figure 3 : Prediction set size distribution and coverage for QDA-CP 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0004-18.png)


Figure 3 : Prediction set size distribution and coverage for FDA-CP 

_Amine Heddoub  et al. / IFAC PapersOnLine 59-10 (2025) 536–541_ 

540 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0005-02.png)


Figure 4 : Prediction set size distribution and coverage for RF-CP 

### _4.2 Tennessee Eastman Process:_ 

The Tennessee Eastman Process (TEP) is a widely used benchmark in FDD. Developed by Downs and Vogel, (1993), it simulates a chemical process with five main units: a reactor, a condenser, a compressor, a separator, and a stripper. Gaseous reactants A, D, E, C are converted into liquid products G, H, which pass through various processing stages. The dataset includes 52 variables with training and testing data under both normal and faulty conditions, covering 21 predefined faults. We selected faults 1, 4, 9, 10, and 11, as faults 4, 9, and 11 are commonly used to compare FDD methods due to their classification difficulty (Lou et al., 2022). Each fault class includes a training set of 480 observations and a test set of 800 observations. The details are presented in Table 3. 

Table 3 : Fault scenarios of TEP 

|Fault|Description|Type|
|---|---|---|
|1<br>4<br>9|A/C feed ratio, B composition constant<br>Reactor cooling water inlet temperature<br>D feed temperature|Step<br>Step<br>Random variation|
|10|C feed temperature|Random variation|
|11|Reactor cooling water inlet temperature|Random variation|



The results of the TEP highlight the comparative performance of traditional classifiers and their CP-enhanced counterparts. The metrics summarized in Table 3 Figure 5, Figure 6 and Figure 7 and reveal some differences in accuracy, coverage, and prediction reliability between these approaches. Traditional QDA, FDA, and RF achieve accuracy levels of 84%, 74.78%, and 82.98%, respectively. By incorporating CP, the models greatly improve performance. The accuracy for single-label predictions rises to 92% - 93%, this represents a great improvement, especially for FDA-CP, which jumps from 74% to 93%. The CCS further demonstrates the reliability of the CP-enhanced models, with values of 96% for QDA-CP, 95% for FDA-CP, and 93% for RF-CP. These scores indicate that the true fault is included in the prediction set in most cases. The CP-enhanced models also produce prediction sets with a small average size. QDA-CP and FDA-CP have a mean width (CMWS) of 2.48 and 2.51, while RF-CP achieves the smallest average set size at 1.78. This shows that RF-CP provides the most compact prediction sets while maintaining high coverage, making it the most efficient of the three CP-enhanced classifiers. 

Misclassification rates for the CP-enhanced models are lower than their traditional counterparts, at 3.73% for QDA-CP, 4.40% for FDA-CP, and 6.21% for RF-CP. 

Table 4 : Metrics of different methods on TEP 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0005-11.png)



![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0005-12.png)


Figure 5 : Prediction set size distribution and coverage for QDA-CP 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0005-14.png)


Figure 6 : Prediction set size ditribution and coverage for FDA-CP 


![](Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction_images/Uncertainty-Aware_Fault_Diagnosis_with_Conformal_Prediction.pdf-0005-16.png)


Figure 7 : Prediction set size distribution and coverage for RF-CP 

_Amine Heddoub  et al. / IFAC PapersOnLine 59-10 (2025) 536–541_ 

541 

### 5.  CONCLUSION AND PERSPECTIVES 

The classification in fault diagnosis is a well-studied problem in the literature, yet uncertainty quantification has often been overlooked. This study addressed this gap by integrating CP with some traditional classifiers to enhance FDD in industrial processes. CP-based methods provide statistical guarantees and dynamically adjust prediction sets, making them useful in real-world scenarios where incorrect classifications or missed faults can lead to costly or dangerous outcomes. 

Experiments on the CSTR and TEP datasets demonstrated that CP-enhanced models achieved high coverage and reduced misclassification rates compared to traditional methods. These improvements, combined with manageable prediction set sizes, make CP-based methods well-suited for complex industrial environments where uncertainty is inherent. Among the models, RF-CP showed the best balance between coverage and efficiency, while QDA-CP and FDA-CP also delivered strong performance across multiple fault scenarios. Despite these advances, further research is needed to fully realize the potential of CP-based fault diagnosis. Future efforts could focus on adapting these methods to real-case problems. 

### REFERENCES 

- A Gentle Introduction to Conformal Prediction and DistributionFree Uncertainty Quantification, 2022. 

- Adil, M., Abid, M., Khan, A.Q., Mustafa, G., Ahmed, N., 2016. Exponential discriminant analysis for fault diagnosis. Neurocomputing 171, 1344–1353. 

- Angelopoulos, A.N., Bates, S., 2022. A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification. 

- Arrieta-Ibarra, I., Gujral, P., Tannen, J., Tygert, M., Xu, C., n.d. Metrics of Calibration for Probabilistic Predictions. 

- Atoui, M.A., Cohen, A., 2021. Coupling data-driven and modelbased methods to improve fault diagnosis. Computers in Industry 128, 103401. 

- Botre, C., Mansouri, M., Nounou, M., Nounou, H., Karim, M.N., 2016. Kernel PLS-based GLRT method for fault detection of chemical processes. Journal of Loss Prevention in the Process Industries 43, 212–224. 

- Chiang, L.H., Russell, E.L., Braatz, R.D., 2001. Fault Detection and Diagnosis in Industrial Systems, Advanced Textbooks in Control and Signal Processing. Springer London, London. 

- Ciancio, V., Homri, L., Dantan, J.-Y., Siadat, A., Convain, P., 2022. Development of a flexible predictive maintenance system in the context of Industry 4.0. IFAC-PapersOnLine 55, 1576–1581. 

- Deng, Z., Han, T., Liu, R., Zhi, F., 2022. A fault diagnosis method in industrial processes with integrated feature space and optimized random forest, in: 2022 IEEE 31st International Symposium on Industrial Electronics (ISIE). Presented at the 2022 IEEE 31st International Symposium on Industrial Electronics (ISIE), pp. 1170–1173. 

   - Lakshmi Priya Palla, G., Kumar Pani, A., 2023. Independent component analysis application for fault detection in process industries: Literature review and an application case study for fault detection in multiphase flow systems. Measurement 209, 112504. 

   - Lakshminarayanan, B., Pritzel, A., Blundell, C., 2017. Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles, in: Advances in Neural Information Processing Systems. Curran Associates, Inc. 

   - Li, W., Gu, S., Zhang, X., Chen, T., 2020. Transfer learning for process fault diagnosis: Knowledge transfer from simulation to physical processes. Computers & Chemical Engineering 139, 106904. 

   - Li, Z., Wang, H., Chen, J., Zhou, Z., Chen, W., 2023. Research on Rolling Bearing Fault Diagnosis Based on DRS Frequency Spectrum Image and Deep Learning. The International Journal of Acoustics and Vibration 28, 211– 219. 

   - Lin, Y.-H., Li, G.-H., 2024. Uncertainty-Aware Fault Diagnosis Under Calibration. IEEE Transactions on Systems, Man, and Cybernetics: Systems 54, 6469–6481. 

   - Lou, C., Atoui, M.A., Li, X., 2022. Novel online discriminant analysis based schemes to deal with observations from known and new classes: Application to industrial systems. Engineering Applications of Artificial Intelligence 111, 104811. 

   - Montesuma, E.F., Mulas, M., Corona, F., Mboula, F.-M.N., 2022. Cross-domain fault diagnosis through optimal transport for a CSTR process. IFAC-PapersOnLine 55, 946–951. 

   - Pei, H., Peng, D., Yin, D., Zhang, T., 2022. Fault Diagnosis of Gas Turbine Control System Based on Optimal Random Forest Algorithm, in: 2022 7th International Conference on Power and Renewable Energy (ICPRE). Presented at the 2022 7th International Conference on Power and Renewable Energy (ICPRE), pp. 514–519. 

   - Pilario, K.E.S., Cao, Y., 2018. Canonical Variate Dissimilarity Analysis for Process Incipient Fault Detection. IEEE Trans. Ind. Inf. 14, 5308–5315. 

   - Shwartz-Ziv, R., Armon, A., 2021. Tabular Data: Deep Learning is Not All You Need. 

   - Vovk, V., Gammerman, A., Shafer, G. (Eds.), 2005. Algorithmic Learning in a Random World, SpringerLink Bücher. Springer Science+Business Media, Inc, Boston, MA. 

   - Yang, B.-S., Di, X., Han, T., 2008. Random forests classifier for machine fault diagnosis. J Mech Sci Technol 22, 1716– 1725. 

   - Zhou, H., Chen, W., Cheng, L., Liu, J., Xia, M., 2023. Trustworthy Fault Diagnosis With Uncertainty Estimation Through Evidential Convolutional Neural Networks. IEEE Transactions on Industrial Informatics 19, 10842–10852. 

   - Zio, E., 2018. The future of risk assessment. Reliability Engineering & System Safety 177, 176–190. 

- Downs, J.J., Vogel, E.F., 1993. A plant-wide industrial process control problem. Computers & Chemical Engineering, Industrial challenge problems in process control 17, 245– 255. 

- Isermann, R., Ball, P., n.d. TRENDS IN THE APPLICATION OF MODEL-BASED FAULT DETECTION AND DIAGNOSIS OF TECHNICAL PROCESSES. 

- Karimi, H., Samavi, R., 2023. Quantifying Deep Learning Model Uncertainty in Conformal Prediction. AAAI-SS 1, 142– 148. 

