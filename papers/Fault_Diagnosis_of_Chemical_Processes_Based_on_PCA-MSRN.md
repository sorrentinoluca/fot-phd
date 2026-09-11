2026 7th International Conference on Artificial Intelligence and Electromechanical Automation (AIEA) 

# Fault Diagnosis of Chemical Processes Based on PCA-MSRN 

1<sup>st</sup> Shuo Sun 

_Faculty of Intelligence Technology Shanghai Institute of Technology_ ShangHai,China 1574332742@qq.com 

**_Abstract—_ To address the challenge of insufficient feature extraction from nonlinear and multi-scale industrial process data, this paper proposes a fault diagnosis model that integrates Principal Component Analysis (PCA) with a Multi-Scale Residual Network (MSRN). The proposed method first applies PCA to the Tennessee Eastman Process dataset for dimensionality reduction and feature decoupling, thereby eliminating redundant information among variables. Subsequently, the processed features are fed into a multi-scale residual network, where parallel multi-scale convolutional layers capture fault characteristics at different scales, while residual connections mitigate the degradation problem in deep networks, enabling accurate fault type classification. Experimental results on the standard TE process dataset demonstrate that the proposed PCA-MSRN model achieves statistically significant improvements in multiple performance metrics, including accuracy and F1-score, over conventional models such as CNN, LSTM, and SVM, validating its superiority.** 

**_Key Words—Fault Diagnosis, Tennessee Eastman Process, Principal Component Analysis, Multi-Scale Residual Network, Deep Learning_** 

## I. INTRODUCTION 

With the increasing complexity and automation of modern industrial systems, there is a growing demand for enhanced reliability and safety in production processes. Real-time and accurate detection and diagnosis of process faults are essential to prevent significant economic losses and safety incidents[1]. The Tennessee Eastman Process, developed by the Eastman Chemical Company in the United States, is a well-established and highly complex chemical process simulation benchmark. Its dataset is widely used to evaluate the performance of process monitoring and fault diagnosis algorithms[2].Traditional fault diagnosis methods, such as Support Vector Machines, often rely on manual feature engineering when handling highdimensional and nonlinear industrial data, which limits their diagnostic performance[3]. Deep learning approaches represented by CNN and LSTM can automatically learn features from data; however, standard CNNs struggle to effectively capture features across different temporal or spatial scales, while LSTMs require substantial computational resources and are prone to overfitting[4].To address the aforementioned challenges, this paper proposes a fault diagnosis model that integrates Principal Component Analysis with a Multi-Scale Residual Network[5]. The introduction of PCA aims to preprocess high-dimensional process data by extracting principal directions of variation, thereby simplifying the input to the subsequent network[6]. The MSRN, on the other 

hand, employs parallel pathways with convolutional kernels of different sizes to effectively extract multi-scale local features along the sequence of principal components, thereby capturing diverse dependency patterns among process variables. By incorporating residual learning mechanisms, it enables the construction of deeper networks, thereby enhancing the model's representational capacity[7]. 

## II. BASED ON THE PCA-MSRN FAULT DIAGNOSIS MODEL 

## _A. Principal Component Analysis_ 

When employing the PCA method for dimensionality reduction, it is necessary to standardize the data into a standard normal distribution with a mean of 0 and a variance of 1. This can be achieved through zero-mean (z-score) standardization,which is mathematically expressed as: 

𝑋�<sup>𝑌�𝜇</sup> �1� 𝜎 where 𝑌 represents the original dataset,𝜇 denotes the mean of 𝑌, 𝜎signifies the standard deviation of 𝑌, and 𝑋 indicates the preprocessed dataset[8]. 

PCA projects high-dimensional process data into an orthogonal low-dimensional subspace while preserving essential process information. Geometrically, this operation performs a rotation of the coordinate system formed by the samples through linear combinations, where the new coordinate axes represent directions of maximum variance. For the preprocessed dataset 𝛸 , the principal component space is determined through covariance matrix decomposition. The covariance matrix 𝑆 is computed as follows: 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0001-15.png)


In PCA-based fault diagnosis, monitoring results are characterized by the 𝑇<sup>�</sup> and 𝑆𝑃𝐸 statistics along with their corresponding control limits . The 𝑇<sup>�</sup> statistic, also known as Hotelling's 𝑇<sup>�</sup> , is employed to quantify the variation of 𝑋 within the principal component subspace. Its mathematical formulation is given by: 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0001-17.png)


where 𝛬�𝑑𝑖𝑎𝑔�𝜆�, 𝜆�, . . . , 𝜆�� is a diagonal matrix consisting of the eigenvalues associated with the retained principal components; and 𝑇�� represents the upper control limit for the 𝑇<sup>�</sup> statistic at a confidence level α; 𝑃 is the loading matrix, which is composed of the eigenvectors of the S matrix. 

979-8-3195-1971-9/26/$31.00 ©2026 IEEE 

630 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:16:10 UTC from IEEE Xplore.  Restrictions apply. 

The Squared Prediction Error (𝑆𝑃𝐸) statistic, also referred to as the Q statistic, is utilized to quantify the variation of 𝑋 in the residual space. It measures the deviation between the original sample and its projection onto the principal component subspace, thereby capturing the extent to which the sample deviates from the PCA model[9]. The mathematical expression for the 𝑆𝑃𝐸 statistic is given by: 

𝑆𝑃𝐸�‖�𝐼�𝑃⋅𝑃<sup>�</sup> �⋅𝑋‖<sup>�</sup> �𝛿�� �4� Where 𝐼represents the identity matrix, and 𝛿�� denotes the 𝑆𝑃𝐸 control limit at a confidence level of 𝛼. 

## _B. Multi-Scale Residual Network_ 

The Multi-Scale Residual Network (MSRN) builds upon the deep residual network architecture by incorporating the concept of multi-scale feature extraction. Whereas traditional residual networks employ fixed-size convolutional kernels within individual residual blocks to extract features, the MSRN deploys multiple paralle convolution branches with different kernel sizes inside a single residual block. This design enables the capture of feature interactions at varying spans within the same network layer. By convolving over the ordered sequence of principal components, the network learns local patterns that involve different numbers of adjacent components. Thereby, this structure is particularly suitable for handling fault data in chemical processes, where complex inter-variable relationships often manifest at multiple scales. 

The primary objective of a convolutional layer is to extract features from input feature maps. This operation can be mathematically formulated as follows: 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0002-05.png)


where 𝑋 denotes the input feature map, 𝑊 represents the convolution kernel, 𝑏 indicates the bias term, and 𝑌 corresponds to the output feature map. The indices 𝑖, 𝑗, and 𝑘 represent the height, width, and channel indices of the input feature map respectively, while 𝑚, 𝑛, and 𝑜 denote the height of the convolution kernel, width of the convolution kernel, and channel indices of the output feature map respectively. 

The model employs the Rectified Linear Unit (ReLU) activation function. This activation function is mathematically defined as: 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0002-08.png)


During the training of neural networks, the issue of internal covariate shift may occur, which forces the network to continually adapt to new distributions, thereby slowing down the training process. Batch Normalization (BN) is a normalization method designed to address the problem of internal covariate shift, and it can be expressed as: 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0002-10.png)



![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0002-11.png)


In the equation, 𝑥� and 𝑦� represent the input and output of the Batch Normalization (BN) layer, respectively; 𝑚 denotes the batch size; 𝜇 and σ correspond to the batch mean and batch standard deviation, respectively; ε is a constant approaching zero; 𝑥�� signifies the normalized input value; while 𝛾 and β are the parameters to be trained. 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0002-13.png)


Fig. 1. Proposed Multi-Scale Residual Block. 

In Figure 1, it is shown that the proposed multi-scale residual block adopts a parallel multi-branch feature extraction architecture combined with residual connections. Specifically, the input feature sequence, consisting of 45 principal components, is fed into three parallel 1D convolutional branches with different receptive fields, namely 3×1, 5×1, and 7×1 Conv1D layers. These branches simultaneously capture local correlations spanning three, five, and seven adjacent principal components, respectively.Subsequently, outputs of three branches are concatenated along the channel dimension for multi-scale feature fusion. A 1×1 Conv1D layer with BN is then utilized to compress channel dimensions and enhance crosschannel feature interaction.Finally, the refined fused feature is added to the original input via element-wise residual shortcut connection, followed by a ReLU activation to produce the final block output. This design effectively captures multi-scale information while alleviating gradient vanishing in deep networks. 

This study proposes an intelligent hybrid fault diagnosis methodology integrating Principal Component Analysis (PCA) with a Multi-Scale Residual Network (MSRN). The core conceptual framework operates through two sequential phases: 

631 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:16:10 UTC from IEEE Xplore.  Restrictions apply. 

initially, PCA is employed to perform dimensionality reduction and noise suppression on raw high-dimensional industrial process data, extracting the most representative principal components to streamline model inputs. Subsequently, the refined features are fed into the MSRN architecture, which leverages its robust multi-scale feature extraction capability and deep residual learning mechanism to automatically discover deep nonlinear characteristics correlated with fault patterns, ultimately achieving high-accuracy fault classification. This hybrid paradigm synergistically combines PCA's advantage in feature compression with MSRN's superior performance in complex pattern recognition, creating a complementary integration of strengths[10-13]. 

## III. SIMULATION EXPERIMENTS 

The dataset generated by the Tennessee Eastman (TE) process platform was selected as the data source to validate the performance of the PCA-MSRN fault diagnosis method. 

## _A. The Tennessee Eastman (TE) Process_ 

The Tennessee Eastman Process (TEP) is a simulation system established based on an actual industrial chemical process from Eastman Chemical Company[14-15]. As a publicly available dataset in the industrial chemical domain, the data generated by TEP exhibits pronounced nonlinearity and strong coupling characteristics. Consequently, it has been extensively adopted for performance evaluation of various fault detection and diagnosis algorithms.As shown in Table 1, the dataset comprises 21 distinct fault types. Each fault dataset contains 52 observed variables. 

<mark>The raw Tennessee Eastman (TE) process data consists of 52 continuous process variables. To reduce the input dimensionality of the model and eliminate redundancy among variables, PCA is first applied to reduce the feature space to 45 dimensions. In the experiments, these 45 principal components achieve a cumulative variance contribution rate of 91.4%,</mark> thereby retaining the vast majority of the process information. 

<mark>After dimensionality reduction, each sample is represented by a 45-dimensional feature vector. To leverage the ability of one-dimensional convolutional neural networks to capture local correlations among features, this study arranges the 45 principal components in a fixed order and reshapes them into a singlechannel sequence of length 45. Consequently, the shape of the input tensor to the MSRN model is (batch_size, 45, 1), where 45 denotes the sequence length (corresponding to the 45 principal components) and 1 indicates the number of channels. This sequence does not carry temporal information; instead, it</mark> treats the PCA-reduced feature space as a structured space. 

<mark>Within each multi-scale residual block, three types of onedimensional convolution kernels with different receptive fields (sizes 3×1, 5×1, and 7×1) are deployed in parallel. These kernels slide along the principal component sequence to capture local feature combination patterns spanning 3, 5, and 7 adjacent principal components, respectively, thereby learning faultrelated deep nonlinear representations at different granularities. This design is fundamentally different from traditional timewindow-based sequential convolution methods. Its advantage lies in the fact that it does not require a preset window length and can directly mine discriminative patterns from the static structured feature space.</mark> 

TABLE I. TENNESSEE-EASTMAN PROCESS FAULTS 

|**_Fault ID_**|**_Fault Description_**|**_Fault Type _**|
|---|---|---|
|DV1 ~ 3|Material composition change|Step|
|IDV4|Reactor cooling water temperature<br>change|Step|
|IDV5|Condenser cooling water<br>temperature change|Step|
|IDV6|Material loss|Step|
|IDV7|Materialpressure loss|Step|
|IDV8|Material temperature variation|Random|
|IDV9,10|Feed temperature change|Random|
|IDV11|Reactor cooling water temperature<br>change|Random|
|IDV12|Condenser cooling water<br>temperature change|Random|
|IDV13|Reaction kineticsparameter change|Drift|
|IDV14,15,21|Stickingvalve|Sticky|
|IDV16~ 20|Unknown|Unknown|



## _B. Model Training_ 

All code in this study was implemented using the Python programming language, leveraging the Scikit-learn and TensorFlow frameworks. Regarding parameter configuration, the batch size was set to 128 and the training was conducted for 200 epochs. For dataset partitioning, a stratified sampling method was adopted to divide the dataset into training and testing sets in a 7:3 ratio, ensuring balanced distribution of samples across all classes. 

The accuracy curves of the PCA-MSRN,MSRN, PCA-CNN, and PCA-LSTM models on both the training and validation sets are presented in Figure 2, Figure 3,Figure 4 and Figure 5, respectively. All models approximately reached convergence after 150 training epochs. In terms of diagnostic performance, the PCA-MSRN model demonstrates superior accuracy curves compared to the other three models, confirming the effectiveness of both PCA preprocessing and the multi-scale residual architecture. 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0003-13.png)


Fig. 2. Training and Validation Accuracy Curves of the PCA-MSRN Model. 

632 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:16:10 UTC from IEEE Xplore.  Restrictions apply. 

𝐹� �2 �<sup>𝑝𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛⋅𝑟𝑒𝑐𝑎𝑙𝑙</sup> �11� 𝑝𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛�𝑟𝑒𝑐𝑎𝑙𝑙 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0004-01.png)


Fig. 3. Training and Validation Accuracy Curves of the MSRN Model. 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0004-03.png)


Fig. 4. Training and Validation Accuracy Curves of the PCA-CNN Model. 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0004-05.png)


Fig. 5. Training and Validation Accuracy Curves of the PCA-LSTM Model. 

Therefore, the PCA-MSRN-based method demonstrates significantly superior accuracy on both the training and validation sets compared to the PCA-CNN and PCA-LSTM approaches. 

To validate the performance of the proposed PCA-MSRN algorithm, we applied PCA-CNN, PCA-LSTM, and SVM models to the Tennessee Eastman (TE) process for comparative testing. The F1-score was adopted as a comprehensive evaluation metric, calculated as follows: 

where 𝑝𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛 denotes the classification precision rate, and 𝑟𝑒𝑐𝑎𝑙𝑙 represents the recall rate. 

TABLE II. F1-SCORE PERFORMANCE OF DIFFERENT METHODS 

|**_Fault Type_**|**_PCA-MSRN_**|**_PCA-CNN_**|**_PCA-LSTM_**|**_SVM _**|
|---|---|---|---|---|
|1|0.9753|0.9064|0.9537|0.8700|
|2|0.9787|0.9787|0.9466|0.8434|
|3|0.6468|0.6236|0.0659|0.1205|
|4|0.7637|0.7228|0.2432|0.7323|
|5|0.8800|0.6738|0.1340|0.6407|
|6|1.0000|0.9965|0.9896|0.8785|
|7|0.9965|0.9896|0.9441|0.9091|
|8|0.9014|0.8188|0.6087|0.1765|
|9|0.6158|0.4964|0.0672|0.1012|
|10|0.7447|0.5451|0.5246|0.0768|
|11|0.7983|0.4436|0.1544|0.1046|
|12|0.8683|0.8041|0.5333|0.2985|
|13|0.9273|0.8754|0.8104|0.2349|
|14|0.8283|0.7601|0.6197|0.1204|
|15|0.7622|0.1863|0.0661|0.1071|
|16|0.5592|0.5630|0.2056|0.2443|
|17|0.6689|0.6920|0.4409|0.7595|
|18|0.8487|0.6794|0.8308|0.2152|
|19|0.8036|0.6965|0.2243|0.1399|
|20|0.7296|0.6105|0.5833|0.6574|
|21|0.4291|0.3431|0.1992|0.0305|
|Macro-average|0.7965|0.6860|0.4831|0.3934|



Table 2 presents a detailed comparison of the F1-scores achieved by different models across 21 fault types. The results indicate that the PCA-MSRN model attains a macro-average F1-score of 0.7965, which is significantly higher than those of PCA-CNN (0.6860), PCA-LSTM (0.4831), and SVM (0.3934), thereby validating the overall superiority of the proposed method. 

For individual fault types, PCA-MSRN achieves either the best or the second-best performance on the majority of faults, with particularly notable improvements over other methods on Fault 5 and Fault 21. However, it should also be noted that on Fault 16, the F1-score of PCA-MSRN (0.5592) is slightly lower than that of PCA-CNN (0.5630), while on Fault 17, its performance (0.6689) falls below that of SVM (0.7595). This indicates that there is still room for improvement in the proposed model when addressing certain specific fault patterns. Overall, the PCA-MSRN architecture, which integrates multiscale feature extraction with residual connections, demonstrates stronger feature learning capability and robustness when handling complex nonlinear, multi-mode process data such as those from the TE process. 

## _C. Visualization Analysis_ 

To investigate the feature representations learned by the model, we fed the original data into the trained network and extracted the outputs from the hidden layer. These representations were subsequently projected into a twodimensional space using t-SNE for visualization. The results are presented in Figure 5. In contrast to the visualization of the initial data, the hidden-layer features after model training exhibit distinct category clustering in the 2D space: samples of the same category form more compact clusters, while those of different categories become clearly separated. This 

633 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:16:10 UTC from IEEE Xplore.  Restrictions apply. 

demonstrates that the model has effectively learned discriminative features that facilitate accurate classification. As shown in Figure  6, the raw data exhibit substantial overlap among different fault categories, indicating poor separability in the original feature space. Figure 7 demonstrates that the PCA-MSRN model yields the most discriminative feature distribution, with most fault classes forming tight and well-separated clusters. In comparison, the PCA-CNN (Figure 8) and PCA-LSTM (Figure 9) achieve moderate separation but still show noticeable mixing among several fault types. These results confirm that the proposed PCA-MSRN model effectively learns more distinguishable features for chemical process fault diagnosis. 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0005-01.png)


Fig. 6. T-SNE Visualization of Raw Data. 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0005-03.png)


Fig. 7. T-SNE Visualization of Feature Representations Learned by the PCAMSRN Model. 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0005-05.png)


Fig. 8. T-SNE Visualization of Feature Representations Learned by the PCACNN Model. 


![](Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN_images/Fault_Diagnosis_of_Chemical_Processes_Based_on_PCA-MSRN.pdf-0005-07.png)


Fig. 9. T-SNE Visualization of Feature Representations Learned by the PCALSTM Model. 

## CONCLUSION 

The PCA-MSRN fault diagnosis model demonstrates superior fault classification accuracy compared to conventional algorithms such as PCA-CNN, PCA-LSTM, and SVM. This diagnostic algorithm exhibits distinctly advantageous performance in fault detection and identification, representing a cutting-edge solution for industrial fault diagnosis applications.Although the PCA-MSRN model achieves superior diagnostic performance on the Tennessee Eastman (TE) benchmark dataset compared to the baseline methods, this study still has certain limitations. The model assumes that the training and test data are independent and identically distributed (i.i.d.), without accounting for the strong time-varying noise, dynamic 

634 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:16:10 UTC from IEEE Xplore.  Restrictions apply. 

operating condition drifts, and multi-modal operating conditions commonly encountered in real-world chemical processes. Furthermore, while the multi-scale residual structure enhances feature extraction capability, it also introduces higher computational complexity, which hinders lightweight online deployment. Future work will be pursued in two directions: first, exploring model lightweighting approaches based on knowledge distillation or network pruning; second, incorporating domain adaptation or transfer learning mechanisms to enhance the model's generalization performance under varying operating conditions and across different processes, thereby laying a more solid foundation for practical industrial applications. 

## REFERENCES 

- [1] Q. Song and P. Jiang, "A multi-scale convolutional neural network based fault diagnosis model for complex chemical processes," Process Safety and Environmental Protection, vol. 164, pp. 391-403, 2022. 

- [2] R. Arunthavanathan, F. Khan, S. Ahmed, et al., An analysis of process fault diagnosis methods from safety perspectives, Computers and Chemical Engineering, 145: 107197, 2021. 

- [3] J. Xie, L. Zhang, H. Wang, and Y. Li, "TE Process Fault Diagnosis Based on Optimized Progressive Neural Network," in Journal of Physics: Conference Series, 2025, vol. 2567, no. 1, p. 012034. 

- [4] X. Li, Q. Ding, and J. Q. Sun, Remaining useful life estimation in prognostics using deep convolution neural networks, Reliability Engineering and System Safety, 172: 1–11, 2018. 

- [5] Y. Gao, P. Gong, and L. X. Li, An end-to-end model based on CNNLSTM for industrial fault diagnosis and prognosis, in *Proceedings of 2018 International Conference on Network Infrastructure and Digital Content (IC-NIDC)*, Guiyang, 2018: 274–278. 

- [6] X. Liu, Y. Zhang, and W. Chen, "A Novel Fault Detection and Diagnosis Scheme Based on Independent Component Analysis-Statistical Characteristics," SICE Journal of Control, Measurement, and System Integration, vol. 14, no. 1, pp. 45-53, 2021. 

- [7] G. Siddan and P. Palraj, Foetal neurodegenerative disease classification using improved deep ResNet classification based VGG-19 feature extraction network, Multimedia Tools and Applications, 81(2): 2393– 2408, 2022. 

- [8] H. Chen and Z. Li, "Fault detection using multiscale recursive principal component analysis for chemical process systems," International Journal of Dynamics and Control, vol. 13, no. 2, pp. 123-136, 2025. 

- [9] W. S. Lai, J. B. Huang, N. Ahuja, and M. H. Yang, Deep laplacian pyramid networks for fast and accurate super-resolution, in Proceedings of IEEE Conference on Computer Vision and Pattern Recognition, 2017: 5. 

- [10] Y. Tai, J. Yang, and X. Liu, Image super-resolution via deep recursive residual network, in Proceed[ings of the IEEE Conference on Computer Vision and Pattern Recognition, 2017: 5. 

- [11] B. Lim, S. Son, H. Kim, S. Nah, and K. M. Lee, Enhanced deep residual networks for single image super-resolution, in The IEEE conference on computer vision and pattern recognition workshops, 2017: 4. 

- [12] K. He, X. Zhang, S. Ren, and J. Sun, Deep residual learning for image recognition, in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016: 770–778. 

- [13] L. Wang and C. Zhao, "Multiple Component Analysis and Its Application in Process Monitoring With Prior Fault Data," Journal of Process Control, vol. 105, pp. 78-89, 2021. 

- [14] X. Li, Y. Wang, and L. Zhang, “Attention-based multi-scale convolutional neural network for fault diagnosis of Tennessee Eastman process,” IEEE Transactions on Instrumentation and Measurement, vol. 73, pp. 1–12, 2024. 

- [15] J. Chen, H. Liu, and Q. Zhao, “Federated transfer learning for decentralized fault diagnosis in Tennessee Eastman process with data privacy protection,” Control Engineering Practice, vol. 145, Article no. 105876, 2025. 

635 

Authorized licensed use limited to: Universita degli Studi di Napoli Federico II. Downloaded on September 11,2026 at 16:16:10 UTC from IEEE Xplore.  Restrictions apply. 

