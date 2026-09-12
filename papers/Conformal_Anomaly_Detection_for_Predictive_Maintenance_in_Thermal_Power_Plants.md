
![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0001-00.png)


Received 30 January 2025, accepted 22 February 2025, date of publication 27 February 2025, date of current version 7 March 2025. _Digital Object Identifier 10.1109/ACCESS.2025.3546451_ 

# Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 

## OGNJEN KUNDACINA 1, VLADIMIR VINCAN 1, GORANA GOJIC 1, VUKAN NINKOVIC 1,2, AND DRAGISA MISKOVIC 1 

1The Institute for Artificial Intelligence Research and Development of Serbia, 21000 Novi Sad, Serbia 

2Faculty of Technical Sciences, University of Novi Sad, 21000 Novi Sad, Serbia 

Corresponding author: Ognjen Kundacina (ognjen.kundacina@ivi.ac.rs) 

This work was supported in part by The Institute for Artificial Intelligence Research and Development of Serbia, under the Seed Research Grant Program for Young Scientists (‘‘Detecting Subtle Anomalies in Thermal Power Plant Operation Using Conformal Prediction’’), through the financial support of Serbia Accelerating Innovation and Entrepreneurship (SAIGE) Project, a joint Investment by Republic of Serbia, Ministry of Science, Technological Development and Innovation, the World Bank and European Union; and in part by Serbian Ministry of Science, Technological Development and Innovation, through the Science and Technological Cooperation program Serbia–China, Research and Development Project under Grant 00101957 2025 13440 003 000 620 021. 

- **ABSTRACT** Thermal power plants are essential for maintaining a stable electricity supply but face high operational costs and potential economic losses due to unexpected equipment failures. Predictive maintenance (PM) aims to reduce these risks by detecting early anomalies, but existing anomaly detection methods lack statistical control over the false positive rate (FPR), leading to frequent false alarms and inefficient maintenance interventions. We hypothesize that a conformal anomaly detection (CAD)-based approach, incorporating calibration-conditional p-value adjustments, can effectively mitigate the issue of uncontrolled FPR by ensuring statistically valid anomaly detection for power plant PM, even when multiple dependent hypothesis tests are performed on operational data. We introduce a CAD framework for power plant PM, which integrates calibration-conditional validity adjustments to systematically control FPR while maintaining sensitivity to operational faults. The evaluation results of the proposed CAD framework for PM in thermal power plants show that it ensures statistically valid FPR control, significantly reducing false alarms while maintaining high sensitivity to faults and strong discriminative ability between normal and faulty operations. By providing automatic and statistically valid FPR control without manual threshold tuning, the proposed framework offers a robust and scalable solution for anomaly detection in thermal power plant PM, improving maintenance efficiency and reducing unnecessary interventions. 

- **INDEX TERMS** Machine learning, conformal prediction, anomaly detection, conformal anomaly detection, isolation forest, predictive maintenance, thermal power plants. 

### **I. INTRODUCTION** 

Thermal power plants are essential for ensuring a stable and reliable electricity supply, often serving both long-term and emergency power needs [1]. However, these plants face high operational and maintenance costs, and failures in critical components can lead to significant economic losses. To address these challenges, predictive maintenance (PM) has become a crucial strategy in managing plant efficiency, reducing downtime, and optimizing maintenance scheduling [2]. 

The associate editor coordinating the review of this manuscript and approving it for publication was Wai-Keung Fung . 

Enabled by Industry 4.0 technologies, PM leverages realtime and historical data to detect early signs of equipment anomalies and predict potential failures [3], allowing for proactive maintenance plans that minimize disruptions and associated costs. A wide range of PM approaches have been developed, with machine learning (ML) playing a significant role in leveraging operational data for early fault detection. In this section, we first review ML-based PM methods for power plants, categorizing them into regressionbased, classification-based, and anomaly detection-based approaches. Next, we focus on anomaly detection methods specifically for power plants, highlighting their ability to 

2025 The Authors. This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/ 

39738 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0002-01.png)


operate without labeled fault data but also noting that they lack statistical guarantees for false positive rate (FPR) control. To address this limitation, we then review applications of conformal prediction (CP) in PM, demonstrating its ability to provide statistical guarantees in other domains. However, as we will see, no existing work applies CP for anomaly detection in power plant PM, highlighting the research gap this study aims to address. 

### _A. MACHINE LEARNING-BASED POWER PLANT PM_ 

With the growing volume of collected historical data, MLbased PM methods are increasingly being applied across various industrial plants [4], including different types of power plants. These methods can broadly be categorized into three types, depending on the ML approach used: 

- Regression-based methods, which fall under supervised learning. 

- Classification-based methods, also a form of supervised learning. 

- Anomaly detection-based methods, which utilize unsupervised learning and are the focus of this paper. 

In this subsection, we briefly review the applications of regression- and classification-based approaches for PM in power plants. Since anomaly detection is the focus of this work, we provide a more detailed review of anomaly detection methods in a separate subsection. 

### 1) REGRESSION-BASED APPROACHES FOR POWER PLANT PM 

Regression-based remaining useful life (RUL) prediction has been applied to wind power plant equipment [5] and water pumps in nuclear power plants [6]. A deep neural network (DNN) has been used to estimate the reliability of brushes in hydroelectric generators [7], while [8] introduces a neuro-fuzzy inference model for thermal power plant generators that predicts vibration data under different loads, flagging inconsistencies when vibrations do not match appropriate load levels. In [9], a regression model is trained to predict the power output of photovoltaic (PV) systems, and faults are identified by comparing the predicted outputs with the actual ones. Similarly, [10] proposes identifying faults in PV power plants by integrating residuals between actual and predicted PV string currents over a predefined time frame. A probabilistic model based on Markov chains has been used to calculate reliability indicators and failure rates for PV power plants [11]. Another probabilistic approach, based on generalized renewal processes, estimates the failure likelihood of the circulating water system in nuclear power plants [12]. 

### 2) CLASSIFICATION-BASED APPROACHES FOR POWER PLANT PM 

Examples of classification methods used for power plant PM include ML-based corrosion detection in nuclear power plant piping [13]. In this study, multiple classification algorithms, 

including logistic regression, DNNs, random forest, and support vector machines (SVM), were compared, and feature importance was interpreted using Shapley additive explanation values. Another example is fault detection and failure mode prediction in PV power plants [14]. This approach monitors and analyzes the response of each inverter under maximal power tracking conditions using ML algorithms to identify potential faults. 

### _B. ANOMALY DETECTION-BASED POWER PLANT PM_ 

While supervised learning methods have been successfully applied to power plant PM, they rely heavily on labeled data, which is often limited and hard to obtain. In contrast, anomaly detection methods, which are based on unsupervised learning, can overcome this limitation by identifying deviations from normal operations without requiring labeled fault data [15]. These methods are typically trained on faultfree<sup>1</sup> operational data, allowing them to learn the patterns of normal behavior, and anomalies are detected when the system encounters abnormal, fault data. This makes anomaly detection methods particularly effective for implementing PM by detecting and reporting early signs of potential faults [16]. 

### 1) ANOMALY DETECTION FOR SOLAR AND HYDROPOWER PLANT PM 

Examples of applying anomaly detection methods to solar power plant operation include the use of isolation forest and spectral clustering methods [17], [18], a hierarchical framework that combines both local and global anomaly detection [19], and a one-class SVM approach for detecting anomalies in inverters of large PV power plants [20]. The minimum spanning tree method has been applied for anomaly detection in hydropower turbine operations, where it helps identify abnormal operating conditions by analyzing the structure of data clusters [21]. 

### 2) ANOMALY DETECTION FOR THERMAL POWER PLANT PM 

For thermal power plants, several anomaly detection methods have been proposed to enhance condition monitoring and improve maintenance strategies. For example, anomaly detection has been applied in nuclear thermal power plants, where a dedicated anomaly detection and quantification system has been developed for monitoring neutron data to ensure safe and efficient reactor operation [22]. This approach leverages the candidate anomaly pair concept to quantify anomaly severity by computing an intensity measure that reflects deviations from an extracted normal behavior model. A distance-from-normal-operation-based approach has been used to monitor the condition of thermal power plant equipment, helping to detect deviations that could signal potential failures [23]. An anomaly detection model based on support vector data description has been applied 

> 1For readability, the terms ‘‘normal’’ and ‘‘fault-free’’ will be used interchangeably in this work. 

39739 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0003-01.png)


to vibration data for monitoring rotating machinery, such as steam turbines and feed pumps, providing early warnings of mechanical issues [24]. In [25], distances between support vectors have been utilized for anomaly detection in coal mill operations, while [26] employs a method leveraging dimensionality reduction and Mahalanobis depth statistics to detect anomalies in combined cycle power plants. Lastly, a DNN-based framework has been developed to detect anomalies in smart grid environments, with various use cases including applications to power plants [27]. 

### 3) CHALLENGES IN ANOMALY DETECTION FOR PREDICTIVE MAINTENANCE 

All the discussed approaches to unsupervised anomaly detection share a similar core methodology, identifying deviations from normal operational data without the need for labeled fault data. However, a common concern in anomaly detection for PM systems is controlling the FPR, also known as the type I error [16]. Excessive false alarms can lead to unnecessary maintenance actions, overwhelming teams, increasing operational costs, and reducing system availability due to downtime from unneeded interventions. In the methods discussed above, false alarm control is typically performed manually by adjusting the detection threshold for anomaly scores, without any clear statistical guarantee. The aim of this work is to provide a CP-based statistically calibrated anomaly detection method for thermal power plants with automatic control of the FPR, without any manual adjustment. 

### _C. CONFORMAL PREDICTION-BASED PM_ 

The goal of CP is to provide statistically valid measures of uncertainty in predictions, ensuring error rates are controlled under predefined significance levels [28], [29], and it is most commonly applied to regression and classification tasks. CP is also distribution-free, meaning it makes no assumptions about the type of underlying data distribution, making it robust across a wide range of applications. The most widely used variant is split CP, which works by splitting the data into a proper training set and a calibration set to estimate confidence levels for new predictions. 

### 1) GENERAL APPLICATIONS OF CP IN PM 

CP has been applied to predictive maintenance tasks beyond anomaly detection. In [30], CP is used to generate statistically calibrated confidence intervals for RUL prediction of turbofan jet engines, while [31] introduces an active learning approach based on CP confidence intervals to select the most informative training samples for RUL prediction in a similar context. Additionally, [32] applies CP to provide confidence intervals for predicting railway track irregularities. 

### 2) CONFORMAL ANOMALY DETECTION FOR INDUSTRIAL FAULT DETECTION 

CP can also be extended to anomaly detection [33], where it is used to calibrate anomaly scores from traditional detection 

algorithms, resulting in a well-calibrated FPR; this method is known as conformal anomaly detection (CAD). CAD can be framed as a hypothesis testing problem [29], with the null hypothesis being that an individual data sample is not anomalous, and p-values are calculated using calibration test anomaly scores, while the desired FPR is interpreted as the statistical significance level _α_ . CAD is still in its early stages of application in industrial fault detection. Recent approaches [34], [35] have developed ensemble models of conformal anomaly detectors at unit and subgroup levels to monitor units in district heating substations. 

### 3) GAPS IN CP RESEARCH FOR POWER PLANT PM 

The CP applications for industrial maintenance mentioned above do not involve the power generation domain. Although there are some recent works that apply CP for statistically valid uncertainty quantification in wind [36] and solar [37] power forecasts, it has yet to be applied in the context of anomaly detection and maintenance within the power generation sector. 

### _D. CONTRIBUTIONS_ 

In summary, ML-based predictive maintenance methods that use regression and classification are widely applied in power plants but have limited applicability due to their reliance on labeled data. Anomaly detection techniques address this but require manual threshold tuning, which lacks statistical guarantees. CP methods provide a principled approach to uncertainty quantification, yet its application in anomaly detection for power generation remains unexplored. To the best of our knowledge, this work represents the first application of CAD in the context of power plant PM. While recent research [17], [20] has explored the use of isolation forests and one-class SVMs for anomaly detection in power plants, these methods rely on heuristic detection threshold tuning and lack the rigorous FPR control provided by CP. We used these recent approaches as a baseline for comparison to demonstrate the effectiveness of our proposed CAD-based method. The contributions of this work are threefold and can be summarized as follows: 

- We introduce a CP-based CAD method to control the FPR, marking the first application of CAD for predictive maintenance in the power generation domain, demonstrated through a case study of a thermal power plant. The proposed approach addresses key drawbacks identified in the literature, specifically the lack of statistically valid FPR control and the need for manual tuning of the detection threshold. By ensuring automatic FPR control without requiring manual adjustments, it provides a more reliable, self-calibrating, and easily integrable alternative to conventional anomaly detection methods for PM. Additionally, as this is the first work introducing CAD in this domain, we aim to raise awareness of its potential benefits and encourage further 

39740 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0004-01.png)


- research on its applicability to power plant anomaly detection. 

- Naively applying CAD to this problem yields marginally valid FPR control, meaning that while the expected FPR is controlled on average, dependencies among multiple hypothesis tests can still lead to an increased number of false positives as the number of tests grows. To address this, we apply and analyze three types of calibrationconditional p-value adjustments [38], marking the first application of such methodology in PM, resulting in more reliable anomaly detection. This approach not only enhances the validity of FPR control beyond marginal levels but also addresses the literature gaps regarding the need for automatic threshold tuning and the absence of statistically valid FPR control. 

- A thermal power plant simulation model has been developed to generate training and test data, simulating four types of faults. Our method demonstrated a significant reduction in the FPR, with only a marginal decrease in the overall discriminative ability between fault and normal operation. We compared our approach with recent research using anomaly detection for power plant PM [17], [20], demonstrating that it achieves statistically valid FPR control without requiring manual threshold tuning, further confirming its advantages over existing methods. 

This paper is organized as follows: Section II describes the power plant model, Section III presents the proposed approach, Section IV details the results and discussion, and Section V concludes the paper. 

### **II. POWER PLANT MODEL AND DATA GENERATING PROCESS** 

In this work, the thermal power plant model is based on the Rankine cycle [39], coupled with a synchronous generator, to simulate both normal and fault operation modes.<sup>2</sup> As shown in Fig. 1, the power plant elements considered in our model include the feed pump, boiler, steam turbine, synchronous generator, and condenser. 

The Rankine cycle is the fundamental operating cycle of all steam-based power plants, where working fluid is continuously evaporated and condensed [39]. It involves pressurizing water, heating it to produce superheated steam, expanding the steam through a turbine, cooling it to regenerate water, and returning it to the feed pump to start the cycle again. The first process involves the pump, where liquid water at low pressure from the condenser is compressed to a higher pressure. The mechanical power supplied to the feed pump for pressurizing the working fluid is given by 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0004-09.png)


2Although we demonstrate performance of the proposed approach on a simulation model, the methodology can also be applied to real-world data, as CP, the main building block of our approach, is flexible and does not assume any underlying data distribution. 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0004-11.png)



![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0004-12.png)


**FIGURE 1.** Diagram of the thermal power plant model, illustrating the key components: feed pump, boiler, steam turbine, synchronous generator, and condenser. 

where _m_ ˙ is the mass flow rate of the working fluid, _h_ 1 and _h_ 2 are the specific enthalpies before and after the compression process, and _v_ 1 is the specific volume of the liquid at the inlet of the pump. Next, _p_ 1 and _p_ 2 are the pressures before and after the pump, while _η_ pump is the isentropic efficiency of the pump, which accounts for how efficiently the pump converts mechanical energy into pressure increase in the fluid. After the pump, the fluid enters the boiler, where it is heated at constant pressure. The heat flow rate added to the fluid _Q_<sup>˙</sup> in can be expressed as: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0004-15.png)


with _h_ 2 and _h_ 3 representing the specific enthalpies of the fluid at the feed pump outlet and boiler exit, respectively. The steam then expands isentropically in the turbine, performing work on the surroundings. The mechanical power produced by the turbine _W_<sup>˙</sup> turbine is expressed by: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0004-17.png)


where _h_ 3 and _h_ 4 are the specific enthalpies before and after expansion in the turbine, and _η_ turbine is the isentropic efficiency of the turbine, quantifying how efficiently the turbine converts the enthalpy drop of the steam into mechanical power. After leaving the turbine, the steam enters the condenser, releasing heat to the surroundings and condensing back into liquid water. The heat flow rate rejected by the system _Q_<sup>˙</sup> out is given by: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0004-19.png)


where _h_ 1 and _h_ 4 are the specific enthalpies of the fluid before and after the condenser. The thermodynamic efficiency of the cycle _η_ therm, representing the net power output relative to the heat input, is expressed as: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0004-21.png)


39741 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0005-01.png)


Finally, the net electrical power output _P_ of the power plant is the difference between the power generated by the synchronous generator connected to the turbine and the power consumed by the pump, adjusted for the respective electrical efficiencies. The electrical power generated by the turbine is expressed by _P_ generator = _η_ generator _W_<sup>˙</sup> turbine, while the electrical _W_ ˙ <u>pump</u> power<sup>Thus,the</sup> required<sup>netelectrical</sup> by the feed<sup>power</sup> pump<sup>output</sup> is _P_<sup>_P_</sup> pump<sup>canbe</sup> = _η_ pump, elec.<sup>.</sup> written as: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0005-03.png)


To simulate the described Rankine cycle model and generate the necessary datasets, we used the _Thermal Engineering Systems in Python (TESPy)_ software [40], an open-source framework for thermodynamic modeling of energy conversion systems. _TESPy_ provides a modular approach to configuring power plant components, allowing us to define turbines, condensers, pumps, and heat exchangers with detailed thermodynamic properties. By solving the underlying system of energy and mass balance equations, the software computes state variables such as pressure, temperature, and enthalpy at each component interface, ensuring a physically consistent simulation of steady-state power plant operation. This setup enables controlled variations in operating conditions, facilitating the generation of both fault-free and faulty datasets for evaluating the proposed CAD framework. 

In addition to the Rankine cycle model described above, we also model the temperatures at various points in the power plant, along with the impact of the cooling water mass flow rate. These models are complex due to factors such as the processes of condensation and evaporation, as well as the influence of heat transfer rates between the working fluid and cooling water. The interaction between the working fluid and cooling system requires careful handling of thermal gradients and condensation effects, which adds to the overall complexity. For simplicity, we omit the description of these detailed models in this paper. For a comprehensive reference, we direct the reader to the Rankine cycle model implemented in the _TESPy_ software [40]. 

For the development and evaluation of the proposed CAD method, we simulate various operating conditions and record the results of selected key variables as measurement readings, which are also shown in Fig. 1.<sup>3</sup> These include: the mass flow rate _m_ ˙ ; the electric power output of the generator _P_ generator; the electric power consumed by the feed pump _P_ pump; the temperature at the boiler outlet _T_ boiler,out; the pressure at the turbine outlet _p_ turbine,out; the temperature at the turbine outlet _T_ turbine,out; the temperature at the pump outlet _T_ pump,out; the temperature of the cooling water at the condenser outlet _T_ water,out; and the lower terminal 

> 3The choice of measurements does not affect the generality of the proposed approach. 

temperature difference _TTD_ lower, calculated as the difference between the steam condensation temperature and the cooling water outlet temperature. 

To simulate various operating conditions and generate fault-free training and test datasets for the proposed approach, we vary two key parameters. The net power output _P_ of the power plant is adjusted to represent changes in external factors, such as demand in the power system, as well as the availability and quality of coal. Additionally, the cooling water inlet temperature _T_ water,in is varied to account for different ambient conditions. 

Next, to evaluate the specificity of the proposed approach in detecting abnormal operating conditions, we create fault datasets by simulating four types of faults. These faults are introduced by altering specific variables that were kept constant during fault-free simulations: 

- To simulate a gradual decrease in the efficiency of the feed pump, we incrementally reduce its isentropic efficiency _η_ pump, reflecting conditions that may occur in an aging or malfunctioning pump. 

- To model fouling in the condenser’s cooling water tubes, we increase the upper terminal temperature difference _TTD_ upper, which is the temperature difference between the steam condensation temperature and the cooling water inlet temperature. Fouling, caused by the buildup of deposits on tube surfaces, reduces heat transfer efficiency by creating an insulating layer. This results in a higher condensation temperature while the cooling water inlet temperature remains the same, thereby increasing _TTD_ upper. 

- To simulate blockages or issues within the cooling system, we gradually decrease the cooling water flow rate _m_ ˙ water. Reduced flow rate can result from obstructions or cooling water pump malfunctions and leads to less efficient heat removal, impacting the condenser’s ability to maintain the desired condensation temperature. 

- To simulate a superheater malfunction or excessive fuel combustion, we increase the steam temperature at the boiler outlet _T_ boiler,out. This fault represents conditions where the superheater may be delivering steam at temperatures above optimal levels, potentially stressing downstream components like the turbine. 

By simulating both fault-free and fault conditions across a range of operating scenarios, we can evaluate the proposed CAD method’s effectiveness, specifically assessing its sensitivity in detecting various faults and its specificity in distinguishing normal from abnormal operating states. 

### **III. PROPOSED APPROACH** 

In this section, we first introduce the necessary theoretical background, including anomaly detection, conformal prediction, and conformal anomaly detection, followed by a discussion of multiple hypothesis testing problem in anomaly detection. We then present the overall framework of the proposed approach. 

39742 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0006-01.png)


### _A. ANOMALY DETECTION_ 

Anomaly detection is an unsupervised learning approach that identifies unusual patterns in data without requiring any labeled samples. Let _X_ train = { **x** _i_ }<sup>_n_</sup> _i_ =<sup>train</sup> 1<sup>representthetraining</sup> dataset, where each sample **x** ∈ R<sup>_d_</sup> is a _d_ -dimensional feature vector. Typically, the training set is assumed to be anomalyfree, providing a baseline of normal behavior. During testing, we introduce a test set _X_ test which may contain anomalous samples. In many anomaly detection algorithms, an anomaly score _sa_ ( **x** ) is calculated for each test sample **x** , where higher scores generally indicate a greater likelihood of the sample being anomalous [15]. To classify a sample as anomalous or normal, we can set a threshold _τ_ on the anomaly score. If the anomaly score _sa_ ( **x** ) exceeds the threshold, the sample is flagged as an anomaly: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0006-04.png)


The threshold _τ_ can be adjusted to control the sensitivity of the anomaly detection, with lower thresholds identifying more potential anomalies but potentially increasing the number of false positives. 

In this paper, we consider three established anomaly detection algorithms: isolation forest [41], one-class SVM [42], and the local outlier factor (LOF) algorithm [43]. Isolation Forest isolates anomalies by recursively partitioning the data, creating a structure where anomalies are more isolated than normal points. One-class SVM, on the other hand, creates a boundary around normal data points in the feature space, with points lying outside this boundary considered anomalous. The LOF algorithm calculates the local density deviation of a given sample relative to its neighbors, detecting points that have lower density than their surrounding data. The first two of these approaches have recently been applied to fault detection in solar power plants and are considered state-ofthe-art data-driven approaches in this area [17], [20]. 

### _B. CONFORMAL PREDICTION_ 

Black-box ML models, which are increasingly used in various applications, cannot provide statistically valid uncertainties for their predictions [44]. For example, softmax probabilities, commonly used to indicate prediction certainty in classification problems, are often overconfident. CP addresses this limitation by providing rigorous uncertainty sets for classification tasks or prediction intervals for regression tasks, maintaining error rates within predefined significance levels [28], [29]. In this work, we focus on the split CP, also known as inductive CP [28, Section 4.2]. This approach divides the data into a training set _D_ train = {( **x** _i, yi_ )}<sup>_n_</sup> _i_ =<sup>train</sup> 1<sup>for model training and a separate calibration set</sup> _D_ cal = {( **x** _i, yi_ )}<sup>_n_</sup> _i_ =<sup>cal</sup> 1<sup>toderivepredictionintervalsorsetsfor</sup> unseen test points. Here, _yi_ denotes the label corresponding to each feature vector **xi** , and _n_ train and _n_ cal represent the sizes of the respective datasets. This division allows split CP to be applied efficiently without retraining the original ML model, 

making it suitable for real-time or large-scale applications. For reference, an alternative approach, full CP (also known as transductive CP) [28, Section 4.5], requires adding each new test point, paired with various candidate labels, to the training set. This process necessitates retraining the model with each new test point, offering strong statistical guarantees but at a significant computational cost, which limits its practicality in most applications. Therefore, in this work, we will refer to split CP simply as CP. 

We illustrate the basis of CP using a classification example, where we focus on constructing discrete prediction sets. A prediction set _Y_ ( **x** ) is a set of plausible labels for a given input sample **x** , containing all labels that are statistically likely to be correct with a specified significance level _α_ , i.e., with 1 − _α_ confidence level.<sup>4</sup> To define prediction sets, it is necessary to introduce a conformity score function _s_ ( **x** _, y_ ), which quantifies how well a test sample **x** with a possible label _y_ aligns (conforms) with the training data _D_ train, with higher values indicating better conformity.<sup>5</sup> A common choice of conformity score function for classification problems is the softmax probability of the true label, even though it may not be the class the model predicted. Higher scores indicate greater model confidence in the prediction, suggesting that the test sample aligns well with the training set. As mentioned, conformity scores calculated using softmax tend to be overconfident, and the goal of CP is to calibrate these scores for more reliable uncertainty estimates. 

To construct prediction sets, we use the calibration set _D_ cal to determine a threshold _sα_ on the conformity scores that aligns with the desired significance level _α_ . Specifically, for a new test sample, we compare conformity scores of its classes with those from the calibration set. We include in the prediction set all classes whose conformity scores exceed the threshold _sα_ , chosen so that only _α_ fraction of the calibration sample scores are lower. This ensures that prediction sets for new test samples include all classes likely to be correct with desired confidence, equal to 1 − _α_ . This method relies on the exchangeability assumption, meaning that the data distribution remains unchanged under permutations between the training and calibration sets, a condition more relaxed than the traditional assumption of independent and identically distributed data. 

Formally, given a significance level _α_ , CP provides prediction sets that cover the true value with probability 1− _α_ : 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0006-13.png)


To ensure this, the threshold _sα_ is set as the _q_ -quantile of the conformity scores in the calibration set _D_ cal, where _q_ is 

> 4In the CP context, the significance level _α_ represents the tolerated error rate, while the confidence level 1 − _α_ reflects the probability that the prediction set contains the true label. A typical value for the significance level can be _α_ = 0 _._ 1, providing a confidence level of 1 − _α_ = 0 _._ 9. 

> 5Alternatively, nonconformity scores are often used in CP literature, where higher values indicate greater deviation from the training set. 

39743 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0007-01.png)


defined as: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0007-03.png)


This formula rounds down the _α_ -quantile to account for the finite size of _D_ cal, ensuring that the prediction set achieves the desired coverage, whereas the term _n_ cal +1 adjusts for test point’s possible position within the sorted conformity scores. Using the introduced threshold _sα_ , the prediction set for a new test sample **x** test is defined as: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0007-05.png)


where _y_ represents a candidate target value associated with **x** test. The prediction set _Y_ ( **x** test) is larger if the model is generally uncertain or if the input data sample **x** test is inherently challenging. It is important to note that the property defined by (8), known as marginal coverage, holds on average across varying calibration sets and test points. 

Overall, this method is model-agnostic, meaning it does not depend on the model’s internal architecture and can be applied directly over any trained model without requiring retraining. Additionally, split CP is distribution-free, making no assumptions about the underlying data distribution and relying solely on the exchangeability of data points. This flexibility allows CP to work with small datasets and unconventional data distributions, providing reliable coverage guarantees across various domains [28], [29]. 

### _C. CONFORMAL ANOMALY DETECTION_ 

CP enhances anomaly detection by providing a statistically rigorous method to control the FPR [33]. CAD can be viewed as an application of CP for binary classification, where the objective is to determine whether a sample is normal or anomalous. To adapt CP for anomaly detection, we define a conformity score function _s_ ( **x** ) that measures how well a test sample **x** aligns with the fault-free training data, omitting _y_ as an argument since the labels are binary. The conformity score can be defined as the negative of the anomaly score: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0007-10.png)


where _sa_ ( **x** ) is the anomaly score provided by an anomaly detection algorithm. The conformity score _s_ ( **x** ) decreases as a sample becomes more anomalous, indicating lower alignment with the training data. 

CAD can also be framed as a hypothesis testing problem [28], enabling further refinement of the method using advanced statistical techniques, with the null hypothesis that the data is not anomalous.<sup>6</sup> Here, p-values are calculated based on the conformity scores from a calibration set to 

> 6Although CAD formulates anomaly detection as a hypothesis testing problem, it differs fundamentally from traditional statistical methods such as t-tests or chi-square tests, which assume specific data distributions and independent samples, making direct comparison impractical. The most appropriate way to evaluate CAD is through established anomaly detection performance metrics (e.g., FPR, precision, recall, accuracy, F1 score, etc.), which provide a comprehensive assessment of its ability to achieve FPR control while preserving sensitivity to anomalies. 

determine the likelihood of observing such data under the null hypothesis, with the FPR interpreted as the statistical significance level _α_ . Traditional, marginally valid p-values for a test sample **x** test are defined as: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0007-15.png)


where **1** (·) is the indicator function. The p-values defined in this manner apply a simple correction function over the ratio of calibration set conformity scores lower than _s_ ( **x** test) to prevent overconfident estimation [38], [45]. A low p- value suggests that the test sample is unlikely to conform to the fault-free data distribution, leading us to reject the null hypothesis and classify the sample as anomalous at the significance level _α_ . By setting a threshold on the p-values corresponding to the desired significance level _α_ , we ensure that, on average, the proportion of normal, fault-free samples **x** test, normal incorrectly flagged as anomalies (i.e., for which the null hypothesis is rejected) does not exceed _α_ : 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0007-17.png)


This statistical guarantee, although marginal, is valuable in PM applications, where the cost of false alarms can be significant. 

### _D. CONTROLLING THE FALSE POSITIVE RATE WITH CALIBRATION-CONDITIONAL VALIDITY_ 

Since data points are evaluated individually as they arrive, each test sample is treated as a separate hypothesis test (yielding a separate p-value), which increases the FPR as the number of tests grows [46]. The methodology discussed so far provides marginal validity, as given in (12) and (13), where probability is averaged over various calibration sets and test points. However, since we consider the case where all tests use the same fixed calibration dataset, they become mutually dependent, and the p-values obtained can still be overconfidently estimated [38], meaning they may be too small, increasing the likelihood of incorrectly rejecting the null hypothesis and identifying the data point as anomalous. 

To address this, we follow the methodology outlined in [38], which involves applying adjustments to the marginal p-values _p_<sup>marg</sup> val to achieve a stronger property called calibration-conditional validity for controlling the FPR. To formalize this, calibration-conditional valid (CCV) p-values _p_<sup>ccv</sup> val<sup>areintroducedbyapplyinganadjustment</sup> function _h_ : [0 _,_ 1] → [0 _,_ 1]: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0007-22.png)


which modifies the marginal p-values using reference thresholds derived from conformity scores in the specific calibration set. The adjustment function _h_ (·) must ensure that CCV p-values satisfy the following condition, representing calibration-conditional validity: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0007-24.png)


39744 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0008-01.png)


where _δ_ is the predefined tolerance level that the coverage guarantee might not hold. Using a fixed calibration set introduces a specific type of dependency among tests, known as positive regression dependence on subsets [38]. Intuitively, this means that larger scores in the calibration set cause p-values for all test points to decrease simultaneously, and vice versa. Accordingly, we apply three specific adjustment functions proposed in [38] that are well-suited for p-values exhibiting this type of dependence. 

Before introducing these three specific adjustments, we first present the general form of the adjustment function used to achieve CCV p-values, which is a piecewise constant function: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0008-04.png)


Here, _b_ = { _b_ 0 _, b_ 1 _, . . . , bn_ cal+1} defines a set of thresholds, where each _bi_ represents a cutoff value that adjusts marginal p-values to ensure they are conservative (large) enough to control the FPR at the desired significance level. The thresholds are set such that _b_ 0 = 0 and _bn_ cal+1 = 1, with all intermediate _bi_ values ordered to be monotonically non-decreasing. These thresholds are chosen to account for dependencies within the calibration set, so that the resulting adjusted p-values satisfy calibration-conditional validity. 

### 1) SIMES ADJUSTMENT 

Typically, small p-values are of primary interest in multiple testing, as they indicate potential rejections of the null hypothesis, while larger p-values are less influential. The Simes adjustment [47] accounts for this by providing smaller thresholds for smaller p-values, with larger p-values having thresholds up to a maximum value of one. The threshold values for the adjustment function in the Simes adjustment are calculated as follows: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0008-08.png)


The equation produces smaller thresholds for smaller indices _i_ (corresponding to smaller p-values), while incorporating the tolerance level _δ_ by scaling the subtraction term with _δ_<sup>2</sup><sup>_/n_cal</sup> . 

### 2) DVORETZKY–KIEFER–WOLFOWITZ–MASSART (DKWM) ADJUSTMENT 

This approach, based on the DKWM inequality <u>[48], defines</u> log(2 _<u>/δ</u>_ <u>)</u> each threshold _b_<sup>_d_</sup> _i_<sup>by adding a correction term</sup> ~~�~~ 2 _n_ cal to the rank fraction _<u>i</u>_<sup>where</sup><sup>_δ_controlsthetolerancelevel.The</sup> _n_ cal<sup>,</sup> resulting thresholds are then limited to a maximum value of one: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0008-12.png)


This adjustment provides broader coverage than the Simes adjustment, offering more conservative thresholds for smaller p-values. 

### 3) ASYMPTOTIC ADJUSTMENT 

The asymptotic adjustment enhances the statistical power of previous, finite-sample adjustments, particularly as the calibration set size grows. While methods like DKWM provide broad coverage, they can be overly conservative, especially for larger p-values. The asymptotic adjustment achieves a balance by providing bounds similar to Simes for small p-values, while offering tighter bounds for the remaining values [38]. The adjustment relies on the following formulas, where _cn_ cal( _δ_ ) is a constant that scales with the calibration set size _n_ cal and tolerance level _δ_ : 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0008-16.png)


Using this constant, the thresholds _b_<sup>_a_</sup> _i_<sup>are defined as:</sup> 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0008-18.png)


### _E. OVERALL FRAMEWORK_ 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0008-20.png)


**FIGURE 2.** Flowchart of the methodology steps followed in this study, illustrating the proposed CAD framework. 

The proposed framework consists of two main components: a training component and a testing component, as illustrated in the flowchart of methodology steps in Fig. 2. 

39745 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0009-01.png)


The training component is responsible for preparing the ML model and calibration data, while the testing component uses these resources to evaluate new data points for anomalies. In the training component, we first gather a historical (or simulated) dataset and define an input feature vector **x**<sup>_t_</sup> using measurements from Section II: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0009-03.png)


where _t_ denotes the time index at which each measurement was recorded. We note that feature selection as a preprocessing step is out of the scope of this work because the proposed CAD framework operates independently of the chosen feature set. Its primary role is to enhance the statistical reliability of any anomaly detection model by ensuring formal FPR control. However, feature selection remains important in real-world applications to improve model interpretability, reduce computational costs, and eliminate irrelevant or redundant features that may affect detection performance. 

In the preprocessing stage, fault data samples are filtered out, retaining only fault-free data to generate training and calibration datasets.<sup>7</sup> Subsequently, normalization is applied to each feature vector elementwise using the minimum and maximum values computed from the training set _D_ train: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0009-06.png)


This scaling, derived from the training set, is then applied consistently across all other data samples. 

Following preprocessing, an isolation forest model is trained on the fault-free training set. Once trained, the model is deployed to the testing component, where it is used to evaluate new data points. Additionally, we calculate conformity scores for the calibration set according to (11) using the trained model, which are then used in the testing component to compute and adjust p-values for CAD. 

The testing component processes new data in real time, beginning with data collection in either streaming or batch mode. This data undergoes preprocessing, where it is scaled according to (22) to ensure consistency with the training data. The trained isolation forest model is applied to calculate anomaly scores for each new data point. These scores are then used to compute conformity scores using (11), which, in turn, serve to derive marginal p-values according to (12). These marginal p-values are further adjusted using one of the selected adjustment functions from equations (17), (18), or (19), producing CCV p-values. Finally, these CCV p-values compared with the significance level _α_ to detect and report any confirmed anomalies in the data. 

> 7In a real-world scenario, this data filtering would be done with assistance from power plant operators, who can identify time periods when equipment functioned fault-free, such as after previous maintenance actions. In this work, we use a simulation model described in Section II, giving us control over the data generation process. 

### _F. COMPUTATIONAL COMPLEXITY ANALYSIS_ 

The overall computational complexity of the proposed CAD framework depends on both the precomputation phase and the inference phase. During precomputation, the marginal p-values require computing conformity scores for all calibration samples, which takes _O_ ( _n_ cal). The threshold values for the Simes, DKWM, and Asymptotic adjustments are precomputed once, each requiring _O_ ( _n_ cal) operations. Additionally, sorting the calibration conformity scores, which enables faster lookups during inference, requires _O_ ( _n_ cal log _n_ cal). Once computed, these values remain fixed for all test samples, making the inference phase more efficient. 

During inference, the marginal p-value computation requires comparing a test sample’s conformity score against all calibration samples, which takes _O_ ( _n_ cal) in a naive approach but can be optimized to _O_ (log _n_ cal) using binary search if the conformity scores are pre-sorted. The Simes, DKWM, and Asymptotic adjustments each involve a simple lookup operation, running in _O_ (1). Therefore, after precomputation, the overall computational complexity of the CAD framework during inference is _O_ ( _n_ cal), which can be improved to _O_ (log _n_ cal) with pre-sorted conformity scores, ensuring efficient real-time anomaly detection. 

### **IV. RESULTS AND DISCUSSION** 

This section presents the results of the study, including the simulation details for data generation, dataset description, and numerical evaluation of the proposed method. We describe how fault-free and faulty samples were generated, provide details on the dataset structure, and demonstrate the effectiveness of the proposed approach in controlling the FPR while maintaining high anomaly detection performance. 

### _A. SIMULATION DETAILS FOR DATASET CONSTRUCTION_ 

For this study, we simulated a smaller thermal power plant with a 20 MW generator, designing the simulation to closely reflect realistic operating conditions, as, to the best of our knowledge, no open-source datasets for anomaly detection in thermal power plants are available. All computational experiments in this study were conducted on a system with an 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz processor, 16 GB of RAM, and Ubuntu 20.04.6 LTS. Nonmeasured parameters that were held constant throughout the simulations include a boiler pressure ratio of 0 _._ 9, electrical efficiencies of _η_ generator = _η_ pump, elec. = 0 _._ 97 for both the generator and pump, and cooling water feed pressure of 120 kPa. Additionally, the turbine isentropic efficiency was set to _η_ turbine = 0 _._ 9 and a feed pump pressure ratio of 4000, respectively, with the steam pressure at the boiler outlet fixed at 150 MPa. 

As described in Section II, to generate fault-free training, calibration, and test data samples, we introduced controlled variations in two ambient parameters: the net power output _P_ of the power plant and the cooling water inlet temperature _T_ water,in. The net power output _P_ was adjusted to reflect 

39746 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0010-01.png)


changes in external factors, such as fluctuations in power demand and variations in coal quality and availability, while _T_ water,in represents ambient temperature conditions. Both _P_ and _T_ water,in were varied to incorporate expected daily changes, as well as random fluctuations. 

The net power output _P_ is modeled as a combination of two load levels, high during the day and low at night, with gradual transitions at predefined times, plus a cumulative random walk that introduces additional variability. The daily load variation _P_ base( _t_ ) is defined as: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0010-04.png)


where _P_ high and _P_ low incrementally sampled each day within intervals [17 _,_ 20] MW and [12 _,_ 15] MW, respectively, with small random steps from the previous day’s values. Here, _T_ am and _T_ pm are the randomly chosen start times for the first and second transition, respectively, while _T_ period is the transition duration, sampled from [60 _,_ 80] minute interval each day. To incorporate smooth, unpredictable variations in power demand, a cumulative random walk component _�P_ fluct.( _t_ ) is added: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0010-06.png)


where _N_<sup>_i_independentrandomsamplesfromthe</sup> _P_<sup>represents</sup> normal distribution _N_ (0 _, σP_<sup>2) with mean 0 and variance</sup><sup>_σ_</sup> _P_<sup>2=</sup> 1, taken at each time index _i_ . The scaling constant _KP_ = 10007 is chosen to keep cumulative values within realistic power output ranges, expressed in MW. The net power output _P_ ( _t_ ) at time _t_ is then given by: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0010-08.png)


The ambient temperature is modeled as a combination of daily sinusoidal changes and a cumulative random walk that introduces additional variability. The daily temperature variation is defined as: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0010-10.png)


where _T_ offset represents the baseline ambient temperature, and is incrementally sampled each day within the interval [18 _,_ 22]<sup>◦</sup> C with small random steps from the previous day’s value. The parameter _A_ = 3<sup>◦</sup> C controls the amplitude of daily temperature fluctuations, _T_ shift = 6 hours aligns the peak temperature to early afternoon, and _T_ day = 24 hours represents a full daily cycle. To incorporate additional 

variability, a cumulative random walk component _�T_ fluct.( _t_ ) is added to account for unpredictable, but smooth changes in ambient temperature. This component is defined as: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0010-13.png)


where _N_<sup>_i_independentrandomsamplesfromthe</sup> _T_<sup>represents</sup> normal distribution _N_ (0 _, σT_<sup>2)withmean0andvariance</sup> _σT_<sup>2=1,takenateachtimeindex</sup><sup>_i_.Thescalingconstant</sup> _KT_ = 1201<sup>ischosentoensurethatthecumulativevalues</sup> remain within realistic temperature ranges as the sum grows. Combining these components, the ambient, cooling water inlet temperature at time _t_ is given by: 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0010-15.png)


The test set contains both fault and fault-free samples. To evaluate the robustness of the proposed CAD approach to noise, we increased the noise level in the fault-free test samples by setting _KT_ and _KP_ to values 20% higher than those used in the training and calibration datasets. For fault test samples, we applied modifications to variables representing gradual declines in feed pump efficiency, increased fouling in condenser tubes, reduced cooling water flow rate, and increased steam temperatures at the boiler outlet to simulate different faults. Each fault was simulated individually over a designated time interval using linear interpolation between initial and final values for each parameter: 

- We decreased the isentropic efficiency of the pump, _η_ pump, from 0.75 to a final value of 0.63. 

- For fouling in the condenser, we increased the upper terminal temperature difference _TTD_ upper from an initial value of 4 to a final value of 15. 

- ˙ 

- • The cooling water flow rate _m_ water was reduced from an initial value of 490 to a final value of 300. 

- We increased the exhaust gas temperature from an initial value of 600 to a final value of 780. 

During fault simulation, ambient variables were adjusted in the same manner as when generating training samples. 

### _B. DATASET DESCRIPTION_ 

During the data generation process, we performed simulations at a one-minute resolution, resulting in the following dataset sizes: 

- Training set: 1 year of simulated data, producing 527,040 samples. 

- Calibration set: 31 days of simulated data, producing 44,640 samples. 

- Test set: 

   - Fault-free samples: 31 days of simulated data, resulting in 44,640 samples. 

   - Fault samples: 8 days of simulated data, producing 11,520 samples. 

   - Total test set size: 56,160 samples. 

39747 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0011-01.png)


All datasets include the following features: _m_ ˙<sup>_t_</sup> , _P_<sup>_t_</sup> generator<sup>,</sup> _P_<sup>_tT tptT tT tT t_</sup> pump<sup>,</sup> boiler,out<sup>,</sup> turbine,out<sup>,</sup> turbine,out<sup>,</sup> pump,out<sup>,</sup> water,out<sup>,</sup> _TTD_<sup>_t_</sup> lower<sup>, with their definitions provided in Section II.</sup> 

In Fig. 3, we visualize the distributions of generated data by reducing its dimensionality to two components using principal component analysis (PCA). The plot includes both training and test data points, while the calibration set is omitted due to overlap with the training set. A considerable number of fault samples lie closer to the training distribution than some of the furthest fault-free test samples, which could lead to false positives if the anomaly detector aims to identify all anomalies, as it would also classify a considerable amount of fault-free data as anomalies. It is common practice to manually tune the detection threshold, which sets the size of the decision boundary around the training set, creating a trade-off between FPR and detection sensitivity, but without providing a statistical guarantee on FPR. Note that some information is lost in this visualization due to the dimensionality reduction, whereas our analysis is conducted in the original feature space. 

summarized in Table 1, provide metrics for FPR, false negative rate (FNR), true positive rate (TPR) (i.e., recall), true negative rate (TNR), precision, accuracy, and F1 Score. Isolation forest achieved the lowest FPR and outperformed the other algorithms in precision, accuracy, and F1 Score. One-class SVM performs slightly better than the LOF algorithm but requires two orders of magnitude longer training time compared to both other algorithms. Given its superior results, we selected isolation forest as the base anomaly detection approach for the proposed CAD approach. It is important to note that default implementations of isolation forest, LOF, and one-class SVM in Scikit-learn use a predefined threshold that results in all positive cases being detected, leading to a recall of 1.00 but also a high FPR. In practice, this threshold is expected to be manually tuned to balance recall and precision based on specific application needs, but such tuning does not provide statistical guarantees on FPR control, confirming the need for CAD to achieve reliable and automatic anomaly detection. 

**TABLE 1.** Anomaly detection test set results. 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0011-06.png)


**FIGURE 3.** Visualization of training, fault, and fault-free test samples, reduced to two dimensions using PCA. 

### _C. NUMERICAL RESULTS_ 

To select a suitable anomaly detection algorithm as the foundation for the proposed CAD approach, we compared the performance of three established methods: isolation forest, one-class SVM, and LOF. From these three methods, isolation forest and SVM were recently used for power plant PM using anomaly detection [17], [20], therefore they can also serve as the baseline for comparison of our approaches with the current state of the art. We utilized Scikitlearn [49] implementations of these algorithms with default hyperparameters. We note that the proposed CAD framework is model-agnostic and does not require hyperparameter tuning or manual threshold selection, as it provides statistical control of the FPR independently of the chosen anomaly detection model. Each model was trained on the fault-free training set and evaluated on the described test set, which includes both fault and fault-free samples. Test set results, 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0011-10.png)


As mentioned, FPR control can be achieved by manually tuning the detection thresholds of these algorithms; however, this does not provide statistical guarantees on the test set. To address this, we apply the CAD approach described in detail in Section III-C, which enables us to obtain marginally valid p-values _p_<sup>marg</sup> val<sup>(</sup><sup>**x**test)foreachtestpoint</sup><sup>**x**test.The</sup> distribution of these marginal p-values is shown in Fig. 4. The most notable observation is the clear separation between fault and fault-free test samples, with the majority of fault samples concentrated near p-values close to zero. In other words, most fault test samples have p-values below 0 _._ 1, demonstrating the high detection sensitivity of the proposed approach for faulty conditions. On the other hand, the distribution of fault-free samples is uniform but not perfectly, exhibiting a mild skew toward lower p-values. This skew suggests that while CAD effectively distinguishes between faulty and normal conditions, some normal samples still receive relatively low p-values due to the increased noise introduced during test set generation. Rather than the strictly uniform distribution expected under ideal conditions, the fault-free distribution shows a slight downward slope, indicating that certain operational states occur more frequently than others. This highlights the challenge of defining a truly representative calibration set, as not all operational conditions are equally probable in practice. The overlap between the tail end of the fault-free distribution and the low p-value region also suggests that certain operational modes are more ambiguous, 

39748 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0012-01.png)


where the distinction between normal and faulty behavior is less clear. This could be attributed to transitional states in plant operation, where small shifts in system parameters temporarily resemble faulty conditions. 

To further analyze the performance of this approach, we conduct anomaly detection on the test set by comparing marginal p-values to a significance level of _α_ = 0 _._ 1. If the p- value for a given test point is below _α_ , an anomaly is detected for that point. The test set results are as follows: FPR = 0.1292, FNR = 0.1086, precision = 0.6382, recall = 0.8913, accuracy = 0.8750, and F1 Score = 0.7438. Comparing the detection results of the proposed CAD approach based on marginal p-values with the base isolation forest algorithm, we observe that, unlike isolation forest, the CAD approach maintains FPR closer to the significance level _α_ (with an error of close to 0 _._ 03), achieved without the need for manual adjustment of the detection threshold. Overall, FPR, precision, accuracy, and F1 score have significantly improved, with only a relatively small deterioration in recall and FNR. 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0012-04.png)


**FIGURE 4.** Distribution of marginal p-values for fault and fault-free test samples. Fault test samples primarily exhibit low p-values (below 0 **_._** 1), while fault-free samples show a more uniform distribution. 

Due to the multiple hypothesis testing problem, with tests mutually dependent on the calibration set as described in Section III-D, the CAD approach using marginal p-values results in an FPR that exceeds the significance level _α_ by approximately 0.03. To address this, we apply and compare three CCV adjustment functions—Simes, DKWM, and asymptotic adjustments—with the goal of reducing FPR by achieving calibration-conditional validity of p-values. By applying these adjustments to the marginal p-values, as described in equations (17), (18), and (19), we obtain three types of CCV p-values, whose distributions for test samples are shown in Fig. 5. Compared to the marginal p-value distribution in Fig. 4, Simes adjustment shows the most significant change, with p-values for fault-free samples becoming noticeably larger (i.e., more conservative), as indicated by the increase in the rightmost blue histogram bin. However, the fault data p-values also became slightly more conservative, visible as a small decrease in the leftmost 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0012-07.png)


**FIGURE 5.** Distribution of CCV p-values for fault and fault-free test data using three CCV adjustment methods: Simes adjustment (top), DKWM adjustment (middle), and asymptotic adjustment (bottom). 

red histogram bin. A key difference among the three adjustments is the extent to which they push p-values toward the conservative end of the distribution. DKWM and asymptotic adjustments produces a more gradual transformation, with fault-free p-values redistributed more evenly across the range, while exhibiting a slightly higher concentration at the rightmost bin compared to the marginal case. This difference suggests that while all three methods improve FPR control, they do so with varying degrees of conservativeness, which may impact the trade-off between maintaining a low FPR and preserving detection sensitivity. Additionally, the fact that fault p-values remain concentrated near zero across all three 

39749 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0013-01.png)


**TABLE 2.** Anomaly detection test set results for isolation forest, CAD based on marginal p-values, and CCV p-values with three different adjustment functions. 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0013-03.png)


methods confirms that CAD effectively preserves anomaly detection performance while refining statistical guarantees. 

To quantify and compare the performance of the three adjustment functions, we performed anomaly detection on the test set by comparing the three types of CCV p-values to a significance level of _α_ = 0 _._ 1. The test set results for these adjustments are presented in Table 2, along with the results of isolation forest and CAD based on marginal p-values, included for reference. The table displays several metrics: FPR, FNR, TPR (i.e., recall), TNR, precision, accuracy, F1 score, and the area under the receiver operating characteristic curve (AUROC), which measures the method’s ability to discriminate between positive and negative samples. 

Notably, the Simes adjustment achieves the best control over FPR, bringing it below the significance level of _α_ = 0 _._ 1 with an FPR of 0.0995. This FPR control is accomplished with only a marginal reduction in the method’s discriminative ability, as evidenced by the AUROC values, which remain high across all methods (around 0.933). The Simes adjustment also achieves the highest precision, accuracy, and F1 score among the adjustment methods, indicating that it enhances anomaly detection performance with minimal impact on recall, FNR, or AUROC. In contrast, both DKWM and asymptotic adjustments show slightly higher FPRs (around 0.126) and lower precision and F1 scores than the Simes adjustment, while maintaining similar AUROC values, indicating that Simes provides the best balance of FPR control, overall detection accuracy, and discriminative ability. 

The results in Table 2 highlight the importance of statistical FPR control when deploying anomaly detection methods in a real-world setting. While the default implementation of isolation forest achieves high recall, its large FPR renders it impractical for PM applications. By manually adjusting the detection threshold, the FPR can be reduced; however, this tuning process lacks automation and does not provide formal statistical guarantees. In contrast, CAD with CCV p-value adjustments significantly reduces FPR while preserving competitive precision, accuracy, and F1score, all without requiring manual threshold adjustment. The AUROC values remain high across all methods, reinforcing that the discriminative ability of the anomaly detection model is preserved. These findings demonstrate that the proposed CAD framework is capable of enhancing existing anomaly detection methods by providing formal statistical 

guarantees on FPR, a critical requirement in PM applications where reducing unnecessary interventions is essential for operational efficiency. 

### **V. CONCLUSION** 

This study introduced a CAD framework for PM in thermal power plants, ensuring statistically valid control over the FPR without requiring manual threshold tuning. The research objective of developing a statistically valid anomaly detection method for PM was successfully addressed by framing anomaly detection as a hypothesis testing problem, where marginal p-values were derived for each test sample. Due to the challenge of multiple hypothesis testing with dependent tests, the initial FPR exceeded the set significance level, necessitating the application of calibration-conditional p- value adjustments. We evaluated three types of adjustments and demonstrated that the best-performing approach reduced FPR from 0.6541 to 0.0995, with only a minor impact on discriminative ability, as evidenced by AUROC values remaining high (around 0.933). This approach enables early fault detection with reduced false alarms, thereby improving maintenance efficiency and minimizing unnecessary interventions. A key limitation of the study is that the framework was validated on simulated power plant data, necessitating further evaluation on real-world operational datasets. For cleaner production, the proposed method enhances operational efficiency by reducing unplanned downtimes and optimizing maintenance schedules, leading to more sustainable and cost-effective power plant operations. Importantly, the desired, statistically valid FPR was achieved without the need for manual threshold tuning, making the approach scalable and practical for industrial applications. 

### **ACKNOWLEDGMENT** 

The statements, opinions and data contained in this publication are solely those of the individual authors and contributors and not of the SAIGE Project. The SAIGE Project disclaims responsibility for any use that may be made of the information contained therein. 

### **REFERENCES** 

> [1] J. Wakiru, P. N. Muchiri, L. Pintelon, and P. Chemweno, ‘‘A cost-based failure prioritization approach for selecting maintenance strategies for thermal power plants: A case study context of developing countries,’’ _Int. J. Syst. Assurance Eng. Manage._ , vol. 10, no. 5, pp. 1369–1387, Oct. 2019. 

39750 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0014-01.png)


- [2] R. K. Mobley, _An Introduction To Predictive Maintenance_ (Plant Engineering), 2nd ed., Oxford, U.K.: Butterworth-Heinemann, 2002. 

- [3] A. Bousdekis, D. Apostolou, and G. Mentzas, ‘‘Predictive maintenance in the 4th industrial revolution: Benefits, Business opportunities, and managerial implications,’’ _IEEE Eng. Manag. Rev._ , vol. 48, no. 1, pp. 57–62, 1st Quart., 2020. 

- [4] T. P. Carvalho, F. A. A. M. N. Soares, R. Vita, R. D. P. Francisco, J. P. Basto, and S. G. S. Alcalá, ‘‘A systematic literature review of machine learning methods applied to predictive maintenance,’’ _Comput. Ind. Eng._ , vol. 137, Nov. 2019, Art. no. 106024. 

- [5] M. Yildirim, N. Z. Gebraeel, and X. A. Sun, ‘‘Integrated predictive analytics and optimization for opportunistic maintenance and operations in wind farms,’’ _IEEE Trans. Power Syst._ , vol. 32, no. 6, pp. 4319–4328, Nov. 2017. 

- [6] X. Liu, W. Cheng, J. Xing, X. Chen, Z. Zhao, L. Gao, B. Ding, K. Zhou, Y. Zhi, and R. Zhang, ‘‘Optimized online remaining useful life prediction for nuclear circulating water pump considering time-varying degradation mechanism,’’ _IEEE Trans. Ind. Informat._ , vol. 20, no. 9, pp. 11057–11068, Sep. 2024. 

- [7] E. M. De Assis, C. L. S. F. Filho, G. A. D. C. Lima, L. A. N. Costa, and G. M. De Oliveira Salles, ‘‘Machine learning and q-Weibull applied to reliability analysis in hydropower sector,’’ _IEEE Access_ , vol. 8, pp. 203331–203346, 2020. 

- [8] G. Falekas, I. Palaiologou, A. Karlis, and J. A. Antonino-Daviu, ‘‘Condition evaluation of steam turbine generator using minute-interval integrated vibration signals,’’ _IEEE J. Emerg. Sel. Topics Ind. Electron._ , vol. 4, no. 3, pp. 836–843, Jul. 2023. 

- [9] A. Livera, M. Theristis, L. Micheli, E. F. Fernández, J. S. Stein, and G. E. Georghiou, ‘‘Operation and maintenance decision support system for photovoltaic systems,’’ _IEEE Access_ , vol. 10, pp. 42481–42496, 2022. 

- [10] Y. Zhao, D. Li, T. Lu, Q. Lv, N. Gu, and L. Shang, ‘‘Collaborative fault detection for large-scale photovoltaic systems,’’ _IEEE Trans. Sustain. Energy_ , vol. 11, no. 4, pp. 2745–2754, Oct. 2020. 

- [11] S.-V. Oprea, A. Bâra, D. Preoţescu, and L. Elefterescu, ‘‘Photovoltaic power plants (PV-PP) reliability indicators for improving operation and maintenance activities. A case study of PV-PP Agigea located in Romania,’’ _IEEE Access_ , vol. 7, pp. 39142–39157, 2019. 

- [12] R. M. Spangler, V. Agarwal, and D. G. Cole, ‘‘A hybrid reliability model using generalized renewal processes for predictive maintenance in nuclear power plant circulating water systems,’’ _IEEE Access_ , vol. 11, pp. 136726–136740, 2023. 

- [13] K. A. Manjunatha, V. Agarwal, A. L. Mack, D. Koester, and D. E. Adams, ‘‘Total unwrapped phase-based diagnosis of wall thinning in nuclear power plants secondary piping structures,’’ _IEEE Access_ , vol. 10, pp. 113726–113740, 2022. 

- [14] M. Chang, K.-H. Chen, Y.-S. Chen, C.-C. Hsu, and C.-C. Chu, ‘‘Developments of AI-assisted fault detection and failure mode diagnosis for operation and maintenance of photovoltaic power stations in Taiwan,’’ _IEEE Trans. Ind. Appl._ , vol. 60, no. 4, pp. 5269–5281, Jul. 2024. 

- [15] V. Chandola, A. Banerjee, and V. Kumar, ‘‘Anomaly detection: A survey,’’ _ACM Comput. Surv._ , vol. 41, no. 3, pp. 1–58, 2009. 

- [16] J. Carrasco, D. López, I. Aguilera-Martos, D. García-Gil, I. Markova, M. García-Barzana, M. Arias-Rodil, J. Luengo, and F. Herrera, ‘‘Anomaly detection in predictive maintenance: A new evaluation framework for temporal unsupervised anomaly detection algorithms,’’ _Neurocomputing_ , vol. 462, pp. 440–452, Oct. 2021. 

- [17] S. Kabir, A. Shufian, and Md. S. R. Zishan, ‘‘Isolation forest based anomaly detection and fault localization for solar PV system,’’ in _Proc. 3rd Int. Conf. Robot., Electr. Signal Process. Techn. (ICREST)_ , Jan. 2023, pp. 341–345. 

- [18] W. Ma, M. Ma, Z. Zhang, J. Ma, R. Zhang, and J. Wang, ‘‘Anomaly detection of mountain photovoltaic power plant based on spectral clustering,’’ _IEEE J. Photovolt._ , vol. 13, no. 4, pp. 621–631, Apr. 2023. 

- [19] Y. Zhao, Q. Liu, D. Li, D. Kang, Q. Lv, and L. Shang, ‘‘Hierarchical anomaly detection and multimodal classification in large-scale photovoltaic systems,’’ _IEEE Trans. Sustain. Energy_ , vol. 10, no. 3, pp. 1351–1361, Jul. 2019. 

- [20] S. Roy, S. Tufail, M. Tariq, and A. Sarwat, ‘‘Photovoltaic inverter failure mechanism estimation using unsupervised machine learning and reliability assessment,’’ _IEEE Trans. Rel._ , vol. 73, no. 3, pp. 1418–1432, Sep. 2024. 

- [21] I. Ahmed, A. Dagnino, and Y. Ding, ‘‘Unsupervised anomaly detection based on minimum spanning tree approximated distance measures and its application to hydropower turbines,’’ _IEEE Trans. Autom. Sci. Eng. (from July 2004)_ , vol. 16, no. 2, pp. 654–667, Apr. 2019. 

- [22] Yogita, D. Toshniwal, P. K. Gupta, V. Khurana, and P. Upadhyay, ‘‘ADQ—Anomaly detection and quantification from delayed neutron monitoring data of nuclear power plants,’’ _IEEE Sensors J._ , vol. 23, no. 7, pp. 7207–7216, Apr. 2023. 

- [23] Y. Zhang, Z. Y. Dong, W. Kong, and K. Meng, ‘‘A composite anomaly detection system for data-driven power plant condition monitoring,’’ _IEEE Trans. Ind. Informat._ , vol. 16, no. 7, pp. 4390–4402, Jul. 2020. 

- [24] D. Hu, C. Zhang, T. Yang, and G. Chen, ‘‘An intelligent anomaly detection method for rotating machinery based on vibration vectors,’’ _IEEE Sensors J._ , vol. 22, no. 14, pp. 14294–14305, Jul. 2022. 

- [25] X. Hong, Z. Xu, and Z. Zhang, ‘‘Abnormal condition monitoring and diagnosis for coal mills based on support vector regression,’’ _IEEE Access_ , vol. 7, pp. 170488–170499, 2019. 

- [26] M. Lim, Y. Kim, S. Jin, S. Ha, S. Y. Chang, H. S. Kang, G. S. Park, M. Lee Joo, C.-S. Jung, Y. Cho, and S. J. Bae, ‘‘Depth-based condition monitoring and contributing factor analysis for anomalies in combined cycle power plant,’’ _IEEE Access_ , vol. 12, pp. 73400–73412, 2024. 

- [27] I. Siniosoglou, P. Radoglou-Grammatikis, G. Efstathopoulos, P. Fouliras, and P. Sarigiannidis, ‘‘A unified deep learning anomaly detection and classification approach for smart grid environments,’’ _IEEE Trans. Netw. Service Manage._ , vol. 18, no. 2, pp. 1137–1151, Jun. 2021. 

- [28] V. Vovk, A. Gammerman, and G. Shafer, _Algorithmic Learning in a Random World_ . Boston, MA, USA: Springer, 2022. 

- [29] A. N. Angelopoulos and S. Bates, ‘‘Conformal prediction: A gentle introduction,’’ _Found. Trends Mach. Learn._ , vol. 16, no. 4, pp. 494–591, 2023. 

- [30] A. Javanmardi and E. Hüllermeier, ‘‘Conformal prediction intervals for remaining useful lifetime estimation,’’ _Int. J. Prognostics Health Manage._ , vol. 14, no. 2, pp. 1–13, Jul. 2023. 

- [31] Z. Kharazian, T. Lindgren, S. Magnusson, and H. Boström, ‘‘CoPAL: Conformal prediction in active learning an algorithm for enhancing remaining useful life estimation in predictive maintenance,’’ in _Proc. 13th Symp. Conformal Probabilistic Predict. Appl._ , vol. 230, 2024, pp. 195–217. 

- [32] A. Plesner, A. P. Engsig-Karup, and H. True, ‘‘Detecting railway track irregularities using conformal prediction,’’ in _Proc. Int. Conf. Artif. Neural Netw. (ICANN)_ , Jan. 2024, pp. 295–309. 

- [33] R. Laxhammar and G. Falkman, ‘‘Inductive conformal anomaly detection for sequential detection of anomalous sub-trajectories,’’ _Ann. Math. Artif. Intell._ , vol. 74, nos. 1–2, pp. 67–94, Sep. 2013. 

- [34] S. Farouq, S. Byttner, M.-R. Bouguelia, and H. Gadd, ‘‘Mondrian conformal anomaly detection for fault sequence identification in heterogeneous fleets,’’ _Neurocomputing_ , vol. 462, pp. 591–606, Oct. 2021. 

- [35] S. Farouq, S. Byttner, M.-R. Bouguelia, and H. Gadd, ‘‘A conformal anomaly detection based industrial fleet monitoring framework: A case study in district heating,’’ _Expert Syst. Appl._ , vol. 201, Sep. 2022, Art. no. 116864. 

- [36] J. Jonkers, D. N. Avendano, G. Van Wallendael, and S. Van Hoecke, ‘‘A novel day-ahead regional and probabilistic wind power forecasting framework using deep CNNs and conformalized regression forests,’’ _Appl. Energy_ , vol. 361, May 2024, Art. no. 122900. 

- [37] Y. Renkema, N. Brinkel, and T. Alskaif, ‘‘Conformal prediction for stochastic decision-making of PV power in electricity markets,’’ _Electric Power Syst. Res._ , vol. 234, p. 110750, Sep. 2024. 

- [38] S. Bates, E. Candès, L. Lei, Y. Romano, and M. Sesia, ‘‘Testing for outliers with conformal p-values,’’ _Ann. Statist._ , vol. 51, no. 1, pp. 149–178, Feb. 2023. 

- [39] Y. Cengel, M. A. Boles, and M. Kanoglu, _Thermodynamics: An Engineering Approach_ . New York, NY, USA: McGraw-Hill, 2024. 

- [40] F. Witte and I. Tuschy, ‘‘TESPy: Thermal engineering systems in Python,’’ _J. Open Source Softw._ , vol. 5, no. 49, p. 2178, May 2020. 

- [41] F. T. Liu, K. M. Ting, and Z. Zhou, ‘‘Isolation forest,’’ in _Proc. 8th IEEE Int. Conf. Data Mining_ , Dec. 2008, pp. 413–422. 

- [42] B. Schölkopf, J. C. Platt, J. Shawe-Taylor, A. J. Smola, and R. C. Williamson, ‘‘Estimating the support of a high-dimensional distribution,’’ _Neural Comput._ , vol. 13, no. 7, pp. 1443–1471, Jul. 2001. 

- [43] M. M. Breunig, H.-P. Kriegel, R. T. Ng, and J. Sander, ‘‘LOF: Identifying density-based local outliers,’’ _ACM SIGMOD Rec._ , vol. 29, no. 2, pp. 93–104, Jun. 2000. 

39751 

VOLUME 13, 2025 

O. Kundacina et al.: Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0015-01.png)


- [44] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, ‘‘On calibration of modern neural networks,’’ in _Proc. 34th Int. Conf. Mach. Learn._ , Jul. 2017, pp. 1321–1330. 

- [45] H. Papadopoulos, K. Proedrou, V. Vovk, and A. Gammerman, ‘‘Inductive confidence machines for regression,’’ in _Proc. Eur. Conf. Mach. Learn._ , Jan. 2002, pp. 345–356. 

- [46] Y. Benjamini and Y. Hochberg, ‘‘Controlling the false discovery rate: A practical and powerful approach to multiple testing,’’ _J. Roy. Stat. Soc. B, Stat. Methodology_ , vol. 57, no. 1, pp. 289–300, Jan. 1995. 

- [47] S. K. Sarkar, ‘‘Generalizing Simes’ test and Hochberg’s stepup procedure,’’ _Ann. Statist._ , vol. 36, no. 1, pp. 337–363, Feb. 2008. 

- [48] P. Massart, ‘‘The tight constant in the Dvoretzky-Kiefer-Wolfowitz inequality,’’ _Ann. Probab._ , vol. 18, no. 3, pp. 1269–1283, Jul. 1990. 

- [49] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. J. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and É. Duchesnay, ‘‘Scikit-learn: Machine learning in Python,’’ _J. Mach. Learn. Res._ , vol. 12, pp. 2825–2830, Jan. 2012. 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0015-08.png)


OGNJEN KUNDACINA received the B.S., M.S., and Ph.D. degrees in electrical and computer engineering, specializing in electrical power systems from the University of Novi Sad, Serbia, in 2017, 2018, and 2023, respectively. 

Since 2022, he has been a Researcher with The Institute for Artificial Intelligence Research and Development of Serbia. Previously, he was a Software Engineer with Schneider Electric and ICodeFactory for several years. He is the author of three journal articles, has presented several papers at international conferences, and is the holder of two patents. His research interests include applying AI methods to monitor and optimize power system operations. 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0015-11.png)


VLADIMIR VINCAN received the B.S. and M.S. degrees in electrical and computer engineering, specializing in embedded systems from the University of Novi Sad, Serbia, in 2020 and 2021, respectively, where he is currently pursuing the Ph.D. degree in electrical and computer engineering. 

In Summer of 2018, he was an Embedded Engineering Intern with the Microsoft Development Center Serbia, and in Summer of 2019, he was a Computer Science Visiting Researcher with Rice University. Since 2023, he has been a Researcher with The Institute of Artificial Intelligence Research and Development of Serbia. Previously, he was a Teaching Assistant with the Faculty of Technical Sciences, University of Novi Sad. His current research interests include applying machine learning to signal processing and electrical engineering. 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0015-14.png)


GORANA GOJIC received the B.S. and M.S. degrees in electrical and computer engineering from the University of Novi Sad, Serbia, in 2015 and 2016, respectively, where she is currently pursuing the Ph.D. degree in electrical and computing engineering. 

In the Summer of 2017, she was a Research Intern with the Zuse Institute Berlin, Germany, and in 2023, she was a Visiting Ph.D. Student with the Technical University of Munich, Germany. Since 2022, she has been a Researcher with The Institute of Artificial Intelligence Research and Development of Serbia. Previously, she was a Teaching Assistant with the Faculty of Technical Sciences, University of Novi Sad. Her current research interest includes applied machine learning in various industries. 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0015-17.png)


VUKAN NINKOVIC received the B.S. and M.S. degrees in electrical and computer engineering with a major in communication systems from the University of Novi Sad, Serbia, in 2018 and 2019, respectively, where he is currently pursuing the Ph.D. degree in electrical and computer engineering. 

Since October 2021, he has been a Teaching Assistant with the Department of Power, Electronic, and Communication Engineering, Faculty of Technical Sciences, University of Novi Sad. In February 2024, he started working as a part-time Research Assistant with The Institute for Artificial Intelligence Research and Development of Serbia. His research interests include the application of machine learning across multiple domains in electrical engineering, such as wireless communication systems, information, and coding theory. 

Mr. Ninkovic received the Telenor Foundation ‘‘Professor Ilija Stojanovic’’ Award for ‘‘The Best Graduated B.S. Student’’ in the domain of communications and signal processing at the University of Novi Sad, in 2018. 


![](Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants_images/Conformal_Anomaly_Detection_for_Predictive_Maintenance_in_Thermal_Power_Plants.pdf-0015-21.png)


DRAGISA MISKOVIC received the Ph.D. degree in telecommunications and signal processing from the Faculty of Technical Sciences, University of Novi Sad, Novi Sad, Serbia, in 2017. 

He is currently a Senior Research Associate with The Institute for Artificial Intelligence Research and Development of Serbia, Novi Sad, where he leads the Human-Computer Interaction Group. Previously, he was a Research Associate with the Faculty of Technical Sciences, University of Novi Sad, in 2005. He has authored ten journal articles, presented numerous papers at international conferences, and holds five patents. His research interests include distributed machine learning and applied artificial intelligence. 

39752 

VOLUME 13, 2025 

