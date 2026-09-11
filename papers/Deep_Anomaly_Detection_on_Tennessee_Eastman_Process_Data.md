# Deep Anomaly Detection on Tennessee Eastman Process Data 

Fabian Hartung<sup>1,2</sup> , Billy Joe Franks<sup>1</sup> , Tobias Michels<sup>1</sup> , Dennis Wagner<sup>1</sup> , Philipp Liznerski<sup>1</sup> , Steffen Reithermann<sup>1</sup> , Sophie Fellenz<sup>1</sup> , Fabian Jirasek<sup>1</sup> , Maja Rudolph<sup>3</sup> , Daniel Neider<sup>4</sup> , Heike Leitte<sup>1</sup> , Chen Song<sup>5</sup> , Benjamin Kloepper<sup>5</sup> , Stephan Mandt<sup>6</sup> , Michael Bortz<sup>7</sup> , Jakob Burger<sup>8</sup> , Hans Hasse<sup>1</sup> and Marius Kloft<sup>1,∗</sup> 

> 1Technische Universit¨at Kaiserslautern, Germany 

> 2BASF SE, Gas Treatment Technology, Germany 

> 3Bosch AI, USA 

> 4Technische Universit¨at Dortmund, Germany 

> 5ABB Corporate Research Center Ladenburg, Germany 

> 6University of California Irvine, USA 

> 7Fraunhofer ITWM, Germany 

> 8Technische Universit¨at M¨unchen, Germany Email corresponding author: kloft@cs.uni-kl.de 

## Abstract 

This paper provides the first comprehensive evaluation and analysis of modern (deep-learning) unsupervised anomaly detection methods for chemical process data. We focus on the Tennessee Eastman process dataset, which has been a standard litmus test to benchmark anomaly detection methods for nearly three decades. Our extensive study will facilitate choosing appropriate anomaly detection methods in industrial applications. 

Keywords: Anomaly detection, Chemical Process Data, Benchmark, Tennessee Eastman process, Time series 

## 1 Introduction 

Anomaly detection, i.e., detecting data that deviates from normality, is a fundamental method in machine learning and artificial intelligence. It is significant in many application domains, from detecting fake reviews in online shopping portals and bots in social networks to tumor detection and industrial fault detection. Anomaly detection is especially significant in safety-critical applications. While an undetected fake review in an online shopping portal may be harmless, failing to recognize anomalies in a chemical plant or a self-driving car may put lives at stake. In chemical plants, most data is recorded during regular or problem-free operation—the normal data. Anomalies, in contrast, occur very rarely, and they can appear to the process or control engineers to be nominal behavior. Here, computing methodology naturally comes into play. Machine learning enables searching 

massive datasets and accurately detects anomalies, even when they are rare [Garg et al., 2017]. There is a large body of literature on detecting anomalies in chemical processes using machine learning [Chadha et al., 2019; Monroy et al., 2009; Song and Suh, 2019]. Over the past three decades, the Tennessee Eastman process (TEP) has arisen as a litmus test for learning anomaly detection on chemical process data. Virtually any newly proposed method is benchmarked by default on the TEP dataset, originally recorded by Downs and Vogel [1993] using a model TEP simulator for data generation. For the following survey a modiefied version will be used [TEP]. 

However, except for some [Chadha et al., 2021; Spyridon and Boutalis, 2018; Plakias and Boutalis, 2022; Yang and Feng, 2019; Neub¨urger et al.; Chadha et al., 2019], all papers evaluate shallow unsupervised anomaly detection methods (not including neural networks) on the TEP dataset. But shallow machine learning is not adequate for complex, structured data, such as the time series occurring in chemical plants and the TEP. On such data, most of the many seminal advances in artificial intelligence during the last decade have been enabled by deep neural networks. 

In 2018, Ruff et al. [2018] provided one of the earliest general-purpose deep learning approaches to anomaly detection. The paper triggered a wave of follow-up work, resulting in the new field of ‘deep anomaly detection’ [Ruff et al., 2021]. Over the past four years, the detection error of unsupervised anomaly detection methods has been reduced drastically, from 35% (best shallow method, 2017) to 1% (best deep method, 2021) on CIFAR-10-AD, a standard anomaly detection benchmark dataset [Ruff et al., 2018; Liznerski et al., 2022]. Since then, deep anomaly detection approaches have been widely adopted in industrial practice. Most recent 

breakthroughs in modern anomaly detection have been achieved on image data. However, the data in chemical plants—and particularly the TEP—are time series. Time series exhibit intriguing temporal interdependencies, well-suited for deep learning. Very recently, the first deep anomaly detection methods on time-series data were introduced, and their high potential tested on various benchmarks [Qiu et al., 2021]. To date, there exist some 30 methods based on neural networks for anomaly detection on time series. 

However, the research on the TEP has not caught up yet with these highly significant advances in unsupervised deep anomaly detection on time series. There exists no compelling up-to-date comparison of modern methods, most of which have been developed within the last two years. Thus it is unclear which methods should ideally be used on such data to achieve maximal detection performance. Using inferior detection methods may lead to unnecessary errors or even put lives at risk when using them for real operation in plants. 

With the present work, we intend to change this. This paper evaluates and compares all 27 unsupervised deep anomaly detection methods for time series existing to date, regarding their detection accuracy on the TEP data. The analysis represents the first—and by far the most comprehensive—comparison of modern unsupervised anomaly detection methods on chemical process data. Our analysis also yields insights into which anomaly detection methods might be most suitable for application to real chemical process data. Establishing deep anomaly detection in real chemical processes would open the route for new, yet unexplored, ways to control these processes—with a perspective to advance autonomously running chemical processes. 

## 2 Related Work 

Early papers on deep anomaly detection (AD) on times series were based on either reconstruction or forecasting objectives. Reconstruction approaches train an autoencoder (AE) on mostly normal training data so that the AE learns to compress and reconstruct normal data well. Samples not reconstructed well are considered anomalous. The deviation from the reconstruction to the input is the anomaly score [Hasan et al., 2016; Luo et al., 2017; Malhotra et al., 2016; Mirza and Cosan, 2018; Zhang et al., 2019; Audibert et al., 2020; Thill et al., 2020; Kim et al., 2022; Hua et al., 2023; Zhan et al., 2022]. Forecasting models extrapolate a series’s current and past data to predict future time steps. The anomaly score is the difference between the predicted and the actual future data [Malhotra et al., 2015; Filonov et al., 2016; Munir et al., 2018; He and Zhao, 2019; Deng and Hooi, 2021]. Typically, both reconstruction and forecasting methods reconstruct each time step and aggregate their anomaly scores for an anomaly score of the entire time series. 

Another branch of AD methods is based on generative models such as variational autoencoders (VAEs) 

[S¨olch et al., 2016; Xu et al., 2018; Park et al., 2018; Guo et al., 2018; Su et al., 2019; Li et al., 2020] and generative adversarial neural networks (GANs) [Zhou et al., 2019; Li et al., 2019; Niu et al., 2020; Geiger et al., 2020; Sabokrou et al., 2018; Liu et al., 2018]. GANs jointly train two networks: a discriminator network to distinguish between accurate and generated data and a generator network to create samples that fool the discriminator. Anomaly scores are either based on the discriminator or are the deviation between the test sample and the bestfitting generated data sample. Some methods combine the above mentioned methods to get the best parts from all worlds [Said Elsayed et al., 2020; Zhao et al., 2020]. 

Inspired by the success of supervised classifiers, there is also a paradigm called ”one-class classification” [Ruff et al., 2018]. This work trains a network to map normal samples to a hypersphere [Ruff et al., 2018] or hyperplane [Sch¨olkopf et al., 2001] and anomalous data away from them. This paradigm has recently been used for AD on time series [Said Elsayed et al., 2020; Shen et al., 2020]. A more direct application of classifiers for AD requires anomalous training samples. Since AD is typically unsupervised, these samples are not available. One approach to solve this issue is using random internet data as auxiliary anomalies during training. This approach is termed outlier exposure and is successful on images [Liznerski et al., 2022; Hendrycks et al., 2018]. However, pertinent data is unavailable for time series, so Goyal et al. [2020] proposed to train a network to distinguish between normal training data and synthetically generated anomalies. The classifier’s certainty for the anomalous class defines the anomaly score for test samples. The most recent approach to time series AD uses self-supervised learning [Qiu et al., 2021]. This method designs an auxiliary training objective. Normal data samples are transformed, and the network has to predict which type of transformation has been applied. Since, for anomalous data, a correct prediction will be difficult, the value of the method’s decision certainty is the anomaly score for test samples. 

## 3 Benchmarking Deep Time-Series Anomaly Detection on TEP 

In this section, a more detailed explanation of the evaluation follows. First, we present the TEP data and explain the metrics used for the review. Finally, the implementation and evaluation protocol is presented. 

### 3.1 TEP dataset 

TEP was based on an existing plant and the processes running in it. The data itself is synthetic, i.e., a simulation of the plant. It consists of five main modules, each a two-stage reactor, a condenser, a vapor-liquid separator, a stripper, and a reboiler, as well as 11 pneumatic valves, two pumps, and a compressor [Manca, 2020]. 

The version of the TEP data used here is available online [TEP] and is referenced in Rieth et al. [2018]. In addition to error-free data on which the algorithms are 

to be trained, it contains 20 different types of erroneous data sets and their complete simulation. Of these 21 data sets, there are 500 other runs, each of which is initialized with a different random value. The time points in each sample are generated every three minutes for 25 hours for the training data and 48 hours for the test data with 53 parameters. 

### 3.2 Metrics 

To compare and evaluate the examined algorithms with each other, a metric is necessary that measures the quality of the methods. Work on AD uses different evaluation metrics depending on the data. Some metrics, like the F1-score, require a binary decision; i.e., model outputs in {0, 1} where 0 denotes normal and 1 anomalous. Others, like the receiver operator characteristic or precision-recall curve, work with continuous anomaly scores. For AD on time series, the F1-score and are under the precision-recall curve are the most commonly used metrics, which is why we evaluate the methods in this paper using both. 

An anomaly detector generates an anomaly score for each point in time of a time series. If this value exceeds a certain threshold, the respective method determines this point in time as an anomaly. The F1-score considers four options of evaluation for each time point: true positive (TP - a correctly detected anomaly), false negative (FN - an anomaly that was not detected), true negative (TN - a correctly identified normal point), and false positive (FP - a normal point mistakenly detected as an anomaly). With these four classes, two metrics can be calculated. One is precision, the proportion of TP among all detected anomalies (TP+FP), and the other is recall, the balance of TP anomalies among all true anomalies (TP+FN). Intuitively, precision describes the accuracy with which a detected anomaly is anomalous, and recall describes the accuracy with which the model detects true anomalies. The F1-score combines precision and recall in one metric, which can be calculated at every point of the time series: 


![](Deep_Anomaly_Detection_on_Tennessee_Eastman_Process_Data_images/Deep_Anomaly_Detection_on_Tennessee_Eastman_Process_Data.pdf-0003-04.png)


These F1-scores are averaged over the whole time series to receive the total F1-Score. 

The area under the precision-recall curve (AUPRC) can be used as a second metric for comparing methods. For every threshold, its respective recall and precision are calculated. As the threshold decreases, the recall increases to 1, which is plotted on the x-axis. The precision is plotted on the y-axis and can be arbitrary but generally decreases as the recall increases. The AUPRC measures the model’s overall performance for any threshold. In essence, the higher the AUPRC, the higher the precision for any recall. In practice, there is a real-world cost associated with both FN and FP. Generally, the cost 

for undetected anomalies (FN) is higher than the cost of falsely detecting an anomaly (FP). However, the specific costs need to be defined case-by-case; therefore, the optimal threshold depends on the particular use case. The AUPRC is a good metric in case the specific costs are unknown since the higher AUPRC is, the lower these associated costs are expected to be. 

### 3.3 Evaluation and implementation 

For an equal and fair evaluation of the considered methods, all methods were implemented in the same Python environment and were trained and evaluated using PyTorch [Paszke et al., 2019]. Since some methods require an unlabeled validation set to adjust the parameters of the anomaly detector, a quarter of the training dataset was separated for this purpose. The test dataset was divided into five folds of equal size to adjust the hyperparameters of each method by optimizing them on each fold and evaluating the performance of the best model with the remaining folds. To avoid time dependencies, directly neighboring folds were excluded. Finally, all folds were averaged, the methods were compared using the best F1-score, and AUPRC received the best grid parameters. For better comparability, the size of the parameter grid of each method was chosen so that each one had a training and evaluation time of 24 hours. In total, the evaluation contains 27 methods listed below. As proposed from Kim et al. [2022], we added an Untrained-LSTM-AE as a baseline. 

### 3.4 Results 

Table 1 shows the experiments’ results, implemented methods, and a reference to their original publications. The methods are ranked according to performance, and the results are rounded to four decimal places. The rankings are computed with the exact results. With few exceptions, both metrics and their associated rankings show similar results. It can only be observed for GMMGRU-VAE, LSTM-AE-OC-SVM, and TCN-S2S-P differences of more than ten places in their order. The BeatGAN, TCN-S2S-AE, and Dense-AE methods score best. The weakest performers are GDN, LSTM-2S2-P, and THOC. It should be noted that Untrained-LSTMAE, proposed above as a baseline, ends up in the upper 

## 4 Discussion and Conclusion 

Even though a generative model was ranked first in these experiments, you can conclude that the reconstruction methods performed best on average, followed by the forecasting and, finally, the generative models. Even the proposed baseline, which belongs to the reconstruction methods, achieved an above-average ranking. 

For future work, a few more things need to be investigated. On the one hand, it has to be considered that the TEP data are synthetic. Despite the simulation’s quality, chemical processes are multifaceted, and, especially with real data, other parameters may play a role that 


![](Deep_Anomaly_Detection_on_Tennessee_Eastman_Process_Data_images/Deep_Anomaly_Detection_on_Tennessee_Eastman_Process_Data.pdf-0004-00.png)


|Method|Method Type|F1-<br>Score|F1-<br>Score<br>Ranking|AUPRC|AUPRC<br>Ranking|Total<br>Ranking|
|---|---|---|---|---|---|---|
|BeatGAN [Zhou et al., 2019]|Generative-GAN|0.9699|1|0.9896|2|1|
|TCN-S2S-AE [Thill et al., 2020]|Reconstruction|0.9632|3|0.9914|1|2|
|Dense-AE [Audibert et al., 2020]|Reconstruction|0.9631|4|0.9880|3|3|
|LSTM-AE [Malhotra et al., 2016]|Reconstruction|0.9506|5|0.9861|4|4|
|LSTM-P [Malhotra et al., 2015]|Forecasting|0.9693|2|0.9824|8|5|
|MSCRED [Zhang et al., 2019]|Reconstruction|0.9353|7|0.9842|5|6|
|Donut [Xu et al., 2018]|Generative-VAE|0.9450|6|0.9829|7|7|
|LSTM-VAE [S¨olch et al., 2016]|Generative-VAE|0.9334|11|0.9831|6|8|
|OmniAnomaly [Su et al., 2019]|Generative-VAE|0.9336|9|0.9808|12|9|
|SIS-VAE [Li et al., 2020]|Generative-VAE|0.9335|10|0.9790|14|10|
|Untrained-LSTM-AE [Kim et al., 2022]|Reconstruction|0.9333|13|0.9792|13|11|
|LSTM-DVAE [Park et al., 2018]|Generative-VAE|0.9333|16|0.9811|11|12|
|USAD [Audibert et al., 2020]|Reconstruction|0.9333|12|0.9779|16|13|
|GMM-GRU-VAE [Guo et al., 2018]|Generative-VAE|0.9291|21|0.9815|10|14|
|TCN-S2S-P [He and Zhao, 2019]|Forecasting|0.9172|23|0.9821|9|15|
|LSTM-MAX-AE [Mirza and Cosan, 2018]|Reconstruction|0.9333|18|0.9786|15|16|
|LSTM-AE-OC-SVM [Said Elsayed et al., 2020]|Hybrid|0.9337|8|0.9511|26|17|
|LSTM-VAE-GAN [Niu et al., 2020]|Generative-GAN|0.9333|14|0.9735|20|17|
|GenAD [Hua et al., 2023]|Reconstruction|0.9333|19|0.9755|19|19|
|TadGAN [Geiger et al., 2020]|Generative-GAN|0.9333|15|0.9690|23|19|
|STGAT-MAD [Zhan et al., 2022]|Reconstruction|0.9267|22|0.9767|17|21|
|Mad-GAN [Li et al., 2019]|Generative-GAN|0.9333|17|0.9621|24|22|
|MTAD-GAT [Zhao et al., 2020]|Hybrid|0.9097|25|0.9758|18|23|
|DeepANT/TCN-P [Munir et al., 2018]|Forecasting|0.9114|24|0.9712|22|24|
|GDN [Deng and Hooi, 2021]|Forecasting|0.9078|26|0.9722|21|25|
|LSTM-2S2-P [Filonov et al., 2016]|Forecasting|0.9327|20|0.9171|27|25|
|THOC [Shen et al., 2020]|Hybrid|0.9074|27|0.9618|25|27|




![](Deep_Anomaly_Detection_on_Tennessee_Eastman_Process_Data_images/Deep_Anomaly_Detection_on_Tennessee_Eastman_Process_Data.pdf-0004-02.png)


Table 1: This table shows the performance of all evaluated methods. For each method, the table lists its reference, the achieved best F1-score, and best AUPRC. The table also lists the ranking according to F1-score, AUPRC, and their mean. The methods are sorted according to the best mean of F1-score and AUPRC. 

cannot be simulated this way. All methods have yielded high scores. That could be related to the studied synthetic data with defined synthetic faults introduced in a fault-free run. The task will be considerably more challenging for actual chemical process data, but the present study is a starting point to tackle this problem. The challenge here will be in uncovering the data and correctly labeling the anomalies in that data. On the other hand, additional metrics should be taken into account. The F1-score and AUPRC are a reasonable basis for comparison but cannot assess longer periods and interdependent points, as with time series [Kim et al., 2022; Doshi et al., 2022]. 

The benchmarking in this paper can guide further research and practitioners in selecting a suitable method for anomaly detection on chemical time series. 

## Acknowledgement 

Part of this work was conducted within the DFG research unit FOR 5359 on Deep Learning on Sparse Chemical Process Data and the BMWK project KEEN (01MK20014U,01MK20014L). 

## References 

- Julien Audibert, Pietro Michiardi, Fr´ed´eric Guyard, S´ebastien Marti, and Maria A Zuluaga. Usad: Unsupervised anomaly detection on multivariate time series. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pages 3395–3404, 2020. 

- Gavneet Singh Chadha, Arfyan Rabbani, and Andreas Schwung. Comparison of semi-supervised deep neural networks for anomaly detection in industrial processes. In 2019 IEEE 17th international conference on industrial informatics (INDIN), volume 1, pages 214–219. IEEE, 2019. 

- Gavneet Singh Chadha, Intekhab Islam, Andreas Schwung, and Steven X Ding. Deep convolutional clustering-based time series anomaly detection. Sensors, 21(16):5488, 2021. 

- Ailin Deng and Bryan Hooi. Graph neural network-based anomaly detection in multivariate time series. In Proceedings of the AAAI conference on artificial intelligence, volume 35, pages 4027–4035, 2021. 

- Keval Doshi, Shatha Abudalou, and Yasin Yilmaz. Tisat: time series anomaly transformer. arXiv preprint arXiv:2203.05167, 2022. 

- James J Downs and Ernest F Vogel. A plant-wide industrial process control problem. Computers & chemical engineering, 17(3):245–255, 1993. 

- Pavel Filonov, Andrey Lavrentyev, and Artem Vorontsov. Multivariate industrial time series with cyber-attack simulation: Fault detection using an lstm-based predictive data model. arXiv preprint arXiv:1612.06676, 2016. 

- Sahil Garg, Amritpal Singh, Shalini Batra, Neeraj Kumar, and Mohammad S Obaidat. Enclass: Ensemblebased classification model for network anomaly detection in massive datasets. In GLOBECOM 2017-2017 IEEE Global Communications Conference, pages 1–7. IEEE, 2017. 

- Alexander Geiger, Dongyu Liu, Sarah Alnegheimish, Alfredo Cuesta-Infante, and Kalyan Veeramachaneni. Tadgan: Time series anomaly detection using generative adversarial networks. In 2020 IEEE International Conference on Big Data (Big Data), pages 33– 43. IEEE, 2020. 

- Sachin Goyal, Aditi Raghunathan, Moksh Jain, Harsha Vardhan Simhadri, and Prateek Jain. Drocc: Deep robust one-class classification. In International conference on machine learning, pages 3711–3721. PMLR, 2020. 

- Yifan Guo, Weixian Liao, Qianlong Wang, Lixing Yu, Tianxi Ji, and Pan Li. Multidimensional time series anomaly detection: A gru-based gaussian mixture variational autoencoder approach. In Asian Conference on Machine Learning, pages 97–112. PMLR, 2018. 

- Mahmudul Hasan, Jonghyun Choi, Jan Neumann, Amit K Roy-Chowdhury, and Larry S Davis. Learning temporal regularity in video sequences. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 733–742, 2016. 

- Yangdong He and Jiabao Zhao. Temporal convolutional networks for anomaly detection in time series. In Journal of Physics: Conference Series, volume 1213, page 042050. IOP Publishing, 2019. 

- Dan Hendrycks, Mantas Mazeika, and Thomas Dietterich. Deep anomaly detection with outlier exposure. arXiv preprint arXiv:1812.04606, 2018. 

- Xiaolei Hua, Lin Zhu, Shenglin Zhang, Zeyan Li, Su Wang, Chao Deng, Junlan Feng, Zhao Zhang, and Wei Wu. Genad: General unsupervised anomaly detection using multivariate time series for largescale wireless base stations. Electronics Letters, 59(1):e12683, 2023. 

- Siwon Kim, Kukjin Choi, Hyun-Soo Choi, Byunghan Lee, and Sungroh Yoon. Towards a rigorous evaluation of time-series anomaly detection. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 36, pages 7194–7201, 2022. 

- Dan Li, Dacheng Chen, Baihong Jin, Lei Shi, Jonathan Goh, and See-Kiong Ng. Mad-gan: Multivariate anomaly detection for time series data with generative adversarial networks. In Artificial Neural Networks and Machine Learning–ICANN 2019: Text and Time Series: 28th International Conference on Artificial Neural Networks, Munich, Germany, September 17–19, 2019, Proceedings, Part IV, pages 703–716. Springer, 2019. 

- Longyuan Li, Junchi Yan, Haiyang Wang, and Yaohui Jin. Anomaly detection of time series with smoothness-inducing sequential variational autoencoder. IEEE transactions on neural networks and learning systems, 32(3):1177–1191, 2020. 

- Wen Liu, Weixin Luo, Dongze Lian, and Shenghua Gao. Future frame prediction for anomaly detection–a new baseline. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 6536– 6545, 2018. 

- Philipp Liznerski, Lukas Ruff, Robert A Vandermeulen, Billy Joe Franks, Klaus-Robert M¨uller, and Marius Kloft. Exposing outlier exposure: What can be learned from few, one, and zero outlier images. arXiv preprint arXiv:2205.11474, 2022. 

- Weixin Luo, Wen Liu, and Shenghua Gao. Remembering history with convolutional lstm for anomaly detection. 

In 2017 IEEE International Conference on Multimedia and Expo (ICME), pages 439–444. IEEE, 2017. 

- Pankaj Malhotra, Lovekesh Vig, Gautam Shroff, Puneet Agarwal, et al. Long short term memory networks for anomaly detection in time series. In ESANN, volume 2015, page 89, 2015. 

- Pankaj Malhotra, Anusha Ramakrishnan, Gaurangi Anand, Lovekesh Vig, Puneet Agarwal, and Gautam Shroff. Lstm-based encoder-decoder for multi-sensor anomaly detection. arXiv preprint arXiv:1607.00148, 2016. 

- Gianluca Manca. ‘tennessee-eastman-process’ alarm management dataset. IEEE DataPort, 2020. 

- Ali H Mirza and Selin Cosan. Computer network intrusion detection using sequential lstm neural networks autoencoders. In 2018 26th signal processing and communications applications conference (SIU), pages 1–4. IEEE, 2018. 

- Isaac Monroy, Gerard Escudero, and Mois`es Graells. Anomaly detection in batch chemical processes. In Computer Aided Chemical Engineering, volume 26, pages 255–260. Elsevier, 2009. 

- Mohsin Munir, Shoaib Ahmed Siddiqui, Andreas Dengel, and Sheraz Ahmed. Deepant: A deep learning approach for unsupervised anomaly detection in time series. Ieee Access, 7:1991–2005, 2018. 

- Felix Neub¨urger, Yasser Saeid, and Thomas Kopinski. Variational-autoencoder architectures for anomaly detection in industrial processes. 

- Zijian Niu, Ke Yu, and Xiaofei Wu. Lstm-based vae-gan for time-series anomaly detection. Sensors, 20(13):3738, 2020. 

- Daehyung Park, Yuuna Hoshi, and Charles C Kemp. A multimodal anomaly detector for robot-assisted feeding using an lstm-based variational autoencoder. IEEE Robotics and Automation Letters, 3(3):1544– 1551, 2018. 

- Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, et al. Pytorch: An imperative style, high-performance deep learning library. Advances in neural information processing systems, 32, 2019. 

- Spyridon Plakias and Yiannis S Boutalis. A novel information processing method based on an ensemble of auto-encoders for unsupervised fault detection. Computers in Industry, 142:103743, 2022. 

- Chen Qiu, Timo Pfrommer, Marius Kloft, Stephan Mandt, and Maja Rudolph. Neural transformation learning for deep anomaly detection beyond images. In International Conference on Machine Learning, pages 8703–8714. PMLR, 2021. 

- Cory A Rieth, Ben D Amsel, Randy Tran, and Maia B Cook. Issues and advances in anomaly detection evaluation for joint human-automated systems. In Advances 

in Human Factors in Robots and Unmanned Systems: Proceedings of the AHFE 2017 International Conference on Human Factors in Robots and Unmanned Systems, July 17- 21, 2017, The Westin Bonaventure Hotel, Los Angeles, California, USA 8, pages 52–63. Springer, 2018. 

- Lukas Ruff, Robert Vandermeulen, Nico Goernitz, Lucas Deecke, Shoaib Ahmed Siddiqui, Alexander Binder, Emmanuel M¨uller, and Marius Kloft. Deep one-class classification. In International conference on machine learning, pages 4393–4402. PMLR, 2018. 

- Lukas Ruff, Jacob R Kauffmann, Robert A Vandermeulen, Gr´egoire Montavon, Wojciech Samek, Marius Kloft, Thomas G Dietterich, and Klaus-Robert M¨uller. A unifying review of deep and shallow anomaly detection. Proceedings of the IEEE, 109(5):756–795, 2021. 

- Mohammad Sabokrou, Mohammad Khalooei, Mahmood Fathy, and Ehsan Adeli. Adversarially learned oneclass classifier for novelty detection. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 3379–3388, 2018. 

- Mahmoud Said Elsayed, Nhien-An Le-Khac, Soumyabrata Dev, and Anca Delia Jurcut. Network anomaly detection using lstm based autoencoder. In Proceedings of the 16th ACM Symposium on QoS and Security for Wireless and Mobile Networks, pages 37–45, 2020. 

- Bernhard Sch¨olkopf, John C Platt, John Shawe-Taylor, Alex J Smola, and Robert C Williamson. Estimating the support of a high-dimensional distribution. Neural computation, 13(7):1443–1471, 2001. 

- Lifeng Shen, Zhuocong Li, and James Kwok. Timeseries anomaly detection using temporal hierarchical one-class network. Advances in Neural Information Processing Systems, 33:13016–13026, 2020. 

- Maximilian S¨olch, Justin Bayer, Marvin Ludersdorfer, and Patrick van der Smagt. Variational inference for on-line anomaly detection in high-dimensional time series. stat, 1050:23, 2016. 

- Bomi Song and Yongyoon Suh. Narrative texts-based anomaly detection using accident report documents: The case of chemical process safety. Journal of Loss Prevention in the Process Industries, 57:47–54, 2019. 

- Plakias Spyridon and Yiannis S Boutalis. Generative adversarial networks for unsupervised fault detection. In 2018 European Control Conference (ECC), pages 691–696. IEEE, 2018. 

- Ya Su, Youjian Zhao, Chenhao Niu, Rong Liu, Wei Sun, and Dan Pei. Robust anomaly detection for multivariate time series through stochastic recurrent neural network. In Proceedings of the 25th ACM SIGKDD international conference on knowledge discovery & data mining, pages 2828–2837, 2019. 

- TEP-DATA additional tennessee eastman process simulation data for anomaly detection evaluation. https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/6C3JR1. Accessed: 202211-04. 

- Markus Thill, Wolfgang Konen, and Thomas B¨ack. Time series encodings with temporal convolutional networks. In Bioinspired Optimization Methods and Their Applications: 9th International Conference, BIOMA 2020, Brussels, Belgium, November 19–20, 2020, Proceedings 9, pages 161–173. Springer, 2020. 

- Haowen Xu, Wenxiao Chen, Nengwen Zhao, Zeyan Li, Jiahao Bu, Zhihan Li, Ying Liu, Youjian Zhao, Dan Pei, Yang Feng, et al. Unsupervised anomaly detection via variational auto-encoder for seasonal kpis in web applications. In Proceedings of the 2018 world wide web conference, pages 187–196, 2018. 

- Xin Yang and Dajun Feng. Generative adversarial network based anomaly detection on the benchmark tennessee eastman process. In 2019 5th International conference on control, automation and robotics (ICCAR), pages 644–648. IEEE, 2019. 

- Jun Zhan, Siqi Wang, Xiandong Ma, Chengkun Wu, Canqun Yang, Detian Zeng, and Shilin Wang. Stgatmad: Spatial-temporal graph attention network for multivariate time series anomaly detection. In ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pages 3568–3572. IEEE, 2022. 

- Chuxu Zhang, Dongjin Song, Yuncong Chen, Xinyang Feng, Cristian Lumezanu, Wei Cheng, Jingchao Ni, Bo Zong, Haifeng Chen, and Nitesh V Chawla. A deep neural network for unsupervised anomaly detection and diagnosis in multivariate time series data. In Proceedings of the AAAI conference on artificial intelligence, volume 33, pages 1409–1416, 2019. 

- Hang Zhao, Yujing Wang, Juanyong Duan, Congrui Huang, Defu Cao, Yunhai Tong, Bixiong Xu, Jing Bai, Jie Tong, and Qi Zhang. Multivariate time-series anomaly detection via graph attention network. In 2020 IEEE International Conference on Data Mining (ICDM), pages 841–850. IEEE, 2020. 

- Bin Zhou, Shenghua Liu, Bryan Hooi, Xueqi Cheng, and Jing Ye. Beatgan: Anomalous rhythm detection using adversarially generated time series. In IJCAI, volume 2019, pages 4433–4439, 2019. 

## A Supporting Information: Methods 

To identify a data point as normal or anomaly, the core element of a method is calculating an anomaly score. In most cases, this involves evaluating the current point using only knowledge about the previous points and, in some cases, using individual time windows. The following is an overview of the most relevant methods for calculating the anomaly score in recent years and shows the implementations of the methods in this evaluation. 

### A.1 Reconstruction-based methods 

The basic idea of autoencoders (AE) is to project input data onto a latent space of lower dimension and then project it back into the input space. In this process, the network must learn to preserve the information in the best possible way but cannot learn an identity function due to the dimensionality differences of the spaces. Since the training is done exclusively on normal data, the projection of an anomaly should produce a more significant reproduction error. They can use the mean squared error as the anomaly score and the training itself. 

LSTM-AE [Malhotra et al., 2016] uses an LSTM network as an encoder and decoder. The encoder LSTM gives its final hidden state to the decoding LSTM as an initial hidden state and reconstructs the input in reverse order. It uses real data as inputs in training and its predictions during testing. 

LSTM-Max-AE [Mirza and Cosan, 2018] proposes some changes by using the mean or maximum of the hidden states of the encoder. During reconstruction, the latent representation is used as an input for all time steps. Here, the inputs are reconstructed in the same order. 

MSCRED [Zhang et al., 2019] doesn’t use the raw inputs but creates signature matrices by capturing the correlation of time series segments. A fully 2Dconvolutional network is applied, and the output is fed into a 2D-convolutional LSTM encoder and decoder. USAD [Audibert et al., 2020] introduced two AE with a shared encoder. The training splits into two phases: First, train both AE to minimize the reconstruction error. Second, let the AE compete against each other. At the same time, the second AE aims to distinguish actual samples from those generated by the first AE, which tries to fool the other. A combination of reconstruction and adversarial loss yields the anomaly score for each point. 

Dense-AE [Audibert et al., 2020] is the same fullyconnected encoder and decoder from USAD but used in a regular AE without the second decoder and additional adversarial objective. The MSE between input and reconstruction is used for both the anomaly score and the training loss. 

TCN-S2S-AE [Thill et al., 2020] proposes a temporal convolutional network (TCN) in the encoder and a transposed TCN in the decoder. This fully convolutional AE architecture uses the LogCosh loss as a training objective. They propose to fit a Gaussian on the errors over the test set during testing. So, this method is unusable 

in online settings. To be comparable to other methods in this context, the Gaussian is fitted to a held-out validation set. 

Untrained-LSTM-AE [Kim et al., 2022] is proposed as a baseline for better comparison to newly developed methods. Therefore, an untrained autoencoder with a single-layer LSTM is used for that. The initialization is random. 

GenAD [Hua et al., 2023] proposes to split an input time series into five folds of equal size. Then it selects 20% of N-dimensions to be masked in one fixed fold. The left 80% unmasked dimensions in this fold and all dimensions in the other four folds are then used to reconstruct the 20% masked series. Since this choice is random, the model needs to learn correlations and temporal patterns to minimize the loss. The implementation masks each feature in the input time series once and lets the model compute its reconstruction. The reconstruction error is measured by the LogCosh metric and considers the feature anomalous when exceeding some threshold. The entire time series is considered anomalous at a certain point if more than a predetermined fraction of the input features is anomalous at this point. 

STGAT-MAD [Zhan et al., 2022] applies several 1D-convolutional layers with varying kernel sizes on an input time series. The resulting sequences are passed parallelly through several graph attention and convolutional layers. Afterward, their concatenated outputs are fed to a bi-LSTM decoder attempting to reconstruct the input. The squared error is used for both training loss and anomaly score. 

### A.2 Forecasting-based methods 

Instead of reconstructing a given input and measuring its quality, another method to detect anomalies is to predict the next time series step(s). These predictions can be compared with the following original time series steps. The point is marked anomalous if the difference exceeds a specified threshold, calculated mainly by the MSE or the mean absolute error (MAE). The number of predicted steps k ≥ 1 is called the prediction horizon. By training these methods on normal data, the networks should be able to give well predictions to normal test data and produce higher prediction errors for anomalous data. 

LSTM-P [Malhotra et al., 2015] proposes using a multilayer LSTM to extract features and generate l- steps predictions with an FC NN. They use MSE loss for training and fit a multivariate Gaussian to the errors of the held-out validation set. After learning the distribution, the anomaly score corresponds to the negative log-likelihood. LSTM-2S2-P [28] uses a multilayer LSTM similarly but predicts the forecast with the hidden features at each time step. By doing this, the model is a sequence-to-sequence predictor, and the anomaly score is yielded by an exponentially weighted moving average of the reconstruction error. 

DeepANT/TCN-P [Munir et al., 2018] chains a max pooling TCN with an MLP in a row to predict the following k points from the input window w. The 

model is trained with MAE and the anomaly score yield by MSE between a prediction and its original time series point. If k ≥ 1, the average of all predictions for a single time step is used to calculate the anomaly score with MSE. 

TCN-S2S-P [He and Zhao, 2019] proposes to pass the input window through a dilated causal TCN. The outputs of the last three layers along the feature dimension are concatenated and given to a final convolutional layer, kernel size one, and D filters. By doing this, the output is a size w x D window and is shifted by one step. Again, the MSE loss is used during training, and a Gaussian distribution is fitted to the prediction errors. Only the last point in the prediction window can be used for this method in an online setting. 

GDN [Deng and Hooi, 2021] builds a graph with features as nodes and edges as relations between features. An Embedding vector for each feature is trained and directed edges from each feature to the top m ∈ N features based on cosine similarity between the feature embeddings. The graph is dynamically recreated for each input batch. The prediction is yielded by applying a graph attention mechanism (Petar Vel˘ıckovi’c, Graph attention networks 2018) and passing the outputs- to an MLP. The authors’ way of calculating the anomaly score as two statistics over the test set, MSE for training, and MAE for anomaly score, make GDN an offline method. The unscaled MSE is used as the anomaly score to change that to an online use case. 

### A.3 Generative Methods 

Generative methods model the data-generating distribution directly. They train a generative model on some latent space with a predefined prior, producing samples close to the real data. Usually, those models offer some way of computing the marginal likelihood of a data point under the model they learned, which can be used to derive anomaly scores. 

#### VAE-Based Methods 

LSTM-VAE [S¨olch et al., 2016] sets likelihood and the posterior approximation to be Gaussian and chooses all NNs to be single-layer LSTMs. In each time step, the encoder returns a mean and covariance component. They produce µ = (µ1, . . . , µt) by another LSTM and use a Gaussian normal distribution with that mean and the identity matrix as covariance matrix as a prior. The anomaly score is calculated with the negative ELBO. 

Donut [Xu et al., 2018] uses MLPs as encoders and decoders. They set some time steps in the input to zero to mask them and train by maximizing a modified version of ELBO that accounts for the input masking. As an anomaly score, they propose the so-called ”reconstruction probability,” although combining it with elaborate mechanisms to reconstruct missing data. Since the TEP data do not include missing data, this is irrelevant to this work. Since the original version of Donut only supports univariate time series, extend it to a multivariate case by applying MLPs to the flattened multivariate input win- 

dow and masking only random features in random time steps instead of entire-time steps. 

LSTM-DVAE [Park et al., 2018] does the same as LSTM-VAE with three changes. First, apply zero-mean Gaussian noise to any input. Second, computing their prior mean for each time step as 


![](Deep_Anomaly_Detection_on_Tennessee_Eastman_Process_Data_images/Deep_Anomaly_Detection_on_Tennessee_Eastman_Process_Data.pdf-0010-10.png)


With learnable parameters v1, vT ∈ R<sup>D</sup> . Finally, as an anomaly score, they use the reconstruction probability. 

GMM-GRU-VAE [Guo et al., 2018] chooses GRUs for their encoder and decoder. For their variational posterior approximation, they use a Gaussian mixture distribution with K components and a Gaussian mixture with learnable parameters for each component. The chosen anomaly score is the reconstruction probability. 

OmniAnomaly [Su et al., 2019] also uses an encoder and decoder on a GRU basis. The encoder defines parameters for multivariate normal distribution. After sampling latent variable z from it, they apply a planar normalizing flow. For the prior is a Kalman filter, a linear Gaussian state space model, chosen. The reconstruction probability is again used as the anomaly score. 

SIS-VAE [Li et al., 2020] proposes a GRU-based VAE to reconstruct smooth time series. They add a KL-divergence term to the ELBO between adjacent time steps. This encourages the distribution of the predicted time series for two close points to be similar. Usually, the reconstruction probability is used as an anomaly score. 

#### GAN-based methods 

BeatGAN [Zhou et al., 2019] uses a TCN-based AE as the generator, training a minimization of the MSE between input and its reconstruction and the MSE between their feature maps in the discriminator’s second-to-last layer. A TCN-based discriminator is trained on the standard GAN loss. As an anomaly score, the MSE of the AE is used. 

Mad-GAN [Li et al., 2019] uses a GAN-based approach LSTMs as both a generator and discriminator. In addition to the usual discriminator score, they also use a reconstruction score. Starting with a latent variable and passing it through the generator, they use a Gaussian/RBF kernel to compute the similarity between this generated sample and the current original input. They use the difference between 1 and this similarity as a reconstruction error. With gradient-based methods, they minimize this error down to a certain threshold. The MAE yielded the anomaly score between the reconstructed and original input and the discriminator’s output. 

LSTM-VAE-GAN [Niu et al., 2020] set up a GAN using a decoder of an LSTM-based VAE as the generator and an LSTM as the discriminator. The original and reconstructed sequences are passed through all but the last layer of the discriminator. Since the discriminator should also be able to detect transformed samples generated from the posterior approximation, besides the ones 

from the standard normal distribution, its loss has an additional term to detect these samples. The anomaly score is, together with the negative discriminator score, a convex combination of the MAE between x and its reconstruction. 

TadGAN [Geiger et al., 2020] uses bidirectional LSTMs for an AE. Considering these decoders and encoders as generators for two Wasserstein GANs, one GAN uses the decoder LSTM as its generator. This maps random samples from an ordinary standard distribution to the input data space. A TCN-based discriminator learns to decide whether the data was a real input or a generated sample. The encoder LSTM is the generator of the second GAN mapping data points to the latent space. This GAN’s TCN discriminator must now decide if its input is an encoded data point or a random sample from the standard normal distribution. The loss function contains the reconstruction error of the AE measured by MSE. Additionally, the discriminator score is calculated and normalized by their means and standard deviations in the test set. The final anomaly score is a convex combination of both absolute values. This method is turned into an online method by computing the statistics of both scores on a held-out part of the training set instead. 

### A.4 Hybrid Methods 

Some methods share principles of different classes from above and combine them in new ways. This is a list of these Hybrid methods. 

LSTM-AE OC-SVM [Said Elsayed et al., 2020] proposes an AE with multilayer LSTMs. Typically, the anomaly score is based on the reconstruction error of an AE, but the authors train an OC-SVM [Sch¨olkopf et al., 2001] on the latent vectors. These are produced by applying the encoder to the held-out clean validation set instead. To make this method more comparable, return the raw scores, i.e., signed distances instead of predictions, and the same architecture as for LSTM-Max-AE. 

tionMTAD-GATmodules (Petar [ZhaoVelietˇckovi’c,al., 2020] use two graph atten-Graph attention networks 2018) and applies them on top of a TCN. One takes features as nodes, and the other time points in a window as nodes. Their output is concatenated and fed into a GRU. They use a fully connected graph as the input. The final hidden state serves as the new input for an MLP for the prediction of the next time point and, simultaneously, as the latent variable for a VAE with an MLP decoder. The model is trained by additively combining the MSE of the prediction and the VAE’s ELBO loss. MSE and the reconstruction probability of the VAE under the usage of a trade-off coefficient between 0 and 1 are combined. 

