# Letteratura — corpus FoT-TEP

> **Luogo unico della letteratura.** Questo file e la sua replica `letteratura.html` sono
> l'unico posto in cui vive il corpus bibliografico del progetto: nessun altro documento
> contiene letteratura. Regola stabilita in `MAINTENANCE.md` §3.
>
> **Perché la numerazione parte da 14.1.** Il corpus e' nato come §14 di
> `fot_walkthrough_conversazione_v2.md` ed e' stato spostato qui il 2026-09-12, senza
> rinumerare: decine di riferimenti sparsi nel repository citano «§14.1», «§14.2», «§14.5».
> Cambiare i numeri li spezzerebbe tutti. I riferimenti alle sezioni §1–§13 e §15 puntano
> al walkthrough del **primo studio**, che resta la loro fonte.
>
> **La letteratura non appartiene a nessuno dei due studi.** Vale per il primo, per lo
> studio 2 e per quelli successivi. Entrambi i walkthrough rimandano qui.

---

Questa sezione unifica i materiali di `docs/lit_review`, il workbook bibliografico e i paper convertiti in `papers/`. Sono inclusi i lavori che incidono su almeno uno degli assi dell'esperimento: oggetto federato, classi localmente non osservate, trasformazione da serie temporale a testo, diagnosi mediante modelli linguistici.

Al corpus originario si aggiungono i **venticinque lavori di federazione con modelli linguistici** raccolti in [`papers/archive/fed_fsl_2026-07/`](../papers/archive/fed_fsl_2026-07) e verificati sul testo integrale dall'audit di prior art conservato nella stessa cartella. Di questi, **diciannove** incidono su almeno uno degli assi e compaiono in §14.1; **sei** riguardano federated prompt learning parametrico su benchmark visivi, sono stati esaminati e lasciati fuori perimetro. L'esclusione è documentata in §14.4, non implicita.

**Il corpus si è allargato oltre i quattro assi.** I trentacinque lavori entrati nel settembre 2026 — diagnosi e monitoraggio centralizzati sul Tennessee Eastman, calibrazione conforme, soglie statistiche — **non toccano nessuno degli assi**. Entrano perché condividono il banco di prova e documentano il perimetro consultato. **Nessuno di essi è 🟢**: nessuno incide sul disegno e nessuno vieta un'affermazione di questo documento, quindi nessuno ha una scheda in §14.2.

Le schede estese, in §14.2, riguardano soltanto i lavori che **influenzano direttamente il disegno**. Per gli altri, la tabella e i file in `docs/lit_review` sono sufficienti.

### 14.1 Corpus completo

La tabella è divisa per categoria: apri quella che ti serve, richiudila con la **✕** nell'intestazione o con il pulsante in fondo al pannello. La colonna **Vicinanza** dice quanto il lavoro tocca questo esperimento.

| Icona | Significato | Che cosa comporta |
| :---: | --- | --- |
| 🟢 | **Vicino** | Incide sul disegno o delimita un claim: va citato e discusso, non solo elencato |
| 🟡 | **Adiacente** | Condivide un asse — dominio, regime non-IID o payload — ma non cambia le nostre scelte: citazione di contesto |
| 🔴 | **Distante** | Sfondo del campo: serve a mostrare il perimetro consultato, non richiede discussione |

Complessivamente: **117 lavori**, di cui 34 🟢, 47 🟡, 36 🔴.

Autori e anno provengono da fonti già verificate nel repository: l'audit di prior art, la gap analysis e la scansione del related work. Un trattino **—** significa che il dato **non è stato verificato su fonte ufficiale**: è 1 lavoro su 117, e va confermato prima di usarli in bibliografia.

<details>
<summary><strong>Federazione testuale</strong> · 14 lavori · 🟢 7 · 🟡 5 · 🔴 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Federation over Text: Insight Sharing for Multi-Agent Reasoning | Yao, Rabbani, Zaheer, Li, 2026 | 🟢 |
| Federated In-Context LLM Agent Learning (FICAL) | Wu, Li, Nan, Wang, 2024 | 🟢 |
| SYNAPSE: Federated Tool Routing via Typed Compendium Artifacts | Chakraborty, Shah, Gupta, 2026 | 🟢 |
| Federated In-Context Learning: Iterative Refinement for Improved Answer Quality (Fed-ICL) | Wang, Wang, Huang, Wang, Yu, Yao, Lui, Zhou, 2025 | 🟢 |
| FERA: Uncertainty-Aware Federated Reasoning for Large Language Models | Wang, Huang, Wang, Wu, Wang, Yu, McAuley, Yao, Zhou, 2026 | 🟢 |
| Can Textual Gradient Work in Federated Learning? (FedTextGrad) | Chen, Jin, Deng, Chen, Huang, Yu, Li, 2025 | 🟢 |
| Time-FFM: LM-Empowered Federated Foundation Model for Time Series Forecasting | Liu et al., 2024 | 🟢 |
| Implicit Federated In-Context Learning for Task-Specific LLM Fine-Tuning (IFed-ICL) | Li, Chen, Zhou, Li, Xian, Liu, Li, 2025 | 🟡 |
| AsynDBT: Asynchronous Distributed Bilevel Tuning for Efficient In-Context Learning | Ma, Dou, Liu, Xing, Feng, Pi, 2026 | 🟡 |
| Fed-SE: Federated Self-Evolution for Cross-Environment Knowledge Transfer | Chen, Shi, Lan, Qiu, Wang, Gu, Yan | 🟡 |
| Social Learning: Towards Collaborative Learning with LLMs | Mohtashami et al., 2023 | 🟡 |
| FedCoT: Communication-Efficient Federated Reasoning Enhancement for LLMs | Li et al., 2025 | 🟡 |
| Federation of Agents: A Semantics-Aware Communication Fabric for Large-Scale Agentic AI | Giusti et al. (CERN) | 🔴 |
| FedSRD: Communication-Efficient Federated LLM Fine-Tuning via Sparsify-Reconstruct-Decompose | Yan et al., 2026 | 🔴 |

</details>

<details>
<summary><strong>FL disgiunto per classe</strong> · 9 lavori · 🟢 7 · 🟡 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| FedMD: Heterogeneous Federated Learning via Model Distillation | Li & Wang, 2019 | 🟢 |
| FedProto: Federated Prototype Learning across Heterogeneous Clients | Tan et al., 2022 | 🟢 |
| FedCKD: Knowledge Distillation with Label-Exclusive Clients | Le, Le, Le, Truong-Huu, 2026 | 🟢 |
| FedMeta-FFD: Federated Meta-Learning for Fault Diagnosis | Chen, Tang, Li, 2023 | 🟢 |
| Federated Zero-Shot Learning with Mid-Level Semantic Knowledge Transfer | Sun, Si, Wu, Gong, 2024 | 🟢 |
| Federated Meta-Learning with Transformer Fusion for Few-Shot Multi-Condition Fault Diagnosis | Zhang et al., 2026 | 🟢 |
| Federated Learning Based on Fuzzy Fusion Rules for Chemical Production Process Fault Diagnosis | Xu et al., 2026 | 🟢 |
| FedMAPS: A Federated Meta-Learning Framework with Adaptive Cross-Domain Contrastive Learning for Few-Shot Fault Diagnosis | Sun, Lu, Chen, Xiang, Hu, 2026 | 🟡 |
| FedAPA-FD: Class-Sensitive Personalized Federated Learning for Non-IID Bearing Fault Diagnosis | Yu, Li, Zhou, 2026 | 🟡 |

</details>

<details>
<summary><strong>Contesto e memoria testuale</strong> · 4 lavori · 🟢 1 · 🟡 2 · 🔴 1</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models (ACE) | Zhang, Hu, Upasani et al., Zou, Olukotun, 2026 | 🟢 |
| FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast | Bogdanov, Lung, Kunz, Taylor, Gao, Zaman, 2026 | 🟡 |
| Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory | Wei, Sachdeva et al. (Google DeepMind), 2026 | 🟡 |
| TextGrad: Automatic "Differentiation" via Text | Yuksekgonul, Bianchi, Boen, Liu, Huang, Guestrin, Zou, 2024 | 🔴 |

</details>

<details>
<summary><strong>Federated few-shot e privacy</strong> · 5 lavori · 🟢 2 · 🟡 3</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Privacy-Preserving Personalized Federated Prompt Learning for Multimodal LLMs (DP-FPL) | Tran, Sun, Patterson, Milanova, 2025 | 🟢 |
| FedDTPT: Federated Discrete and Transferable Prompt Tuning for Black-Box LLMs | Wu, Chen, Yang et al. | 🟢 |
| Federated Few-shot Learning (F²L) | Fu, Wang, Ding, Chen, Chen, Li, 2023 | 🟡 |
| Personalized Federated Few-Shot Learning (pFedFSL) | Zhao, Yu, Wang, Domeniconi, Guo, Zhang, Cui, 2024 | 🟡 |
| PPFedIT: Towards Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples | Zhang, Zhang, Huang et al., 2026 | 🟡 |

</details>

<details>
<summary><strong>TS→testo fedele</strong> · 7 lavori · 🟢 4 · 🟡 1 · 🔴 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Truth-Conditional Captions for Time Series Data | Jhamtani & Berg-Kirkpatrick, 2021 | 🟢 |
| Representing Time Series as Structured Programs for LLM Reasoning (T2SP) | Kim et al., 2026 | 🟢 |
| CGTime: Decoupling Perception from Description in Time-Series Reasoning | Feng, Xie, Zhang, Li, Ling, Li, Liu | 🟢 |
| S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis | Li & Zhao, 2025 | 🟢 |
| An On-the-Fly Signals-to-Semantics Storytelling Framework for Explainable Industrial Maintenance Decisions | Yue, Zhao, Cheng, 2026 | 🟡 |
| A Fuzzy Approach to Data-to-Text for Time Series | Ramos-Soto, Janeiro, Alonso, Bugarín et al., 2017 | 🔴 |
| ICA2TEXT: Data-to-Text for Air-Quality Time Series | Cascallar-Fuentes et al., 2022 | 🔴 |

</details>

<details>
<summary><strong>Rappresentazioni simboliche</strong> · 4 lavori · 🟢 1 · 🟡 1 · 🔴 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Bridging Time Series and Large Language Models via Symbolic Representation for HAR | Pappa, Karvelis & Stylios, 2026 | 🟢 |
| A Novel Feature Extraction Approach for Mechanical Fault Diagnosis Based on ESAX and BoW | Zhao et al., 2022 | 🟡 |
| HSQP: Hierarchical Symbolic Quantization Prompting for Time-Series Forecasting | Abdullahi et al., 2026 | 🔴 |
| LLM-ABBA: Understanding Time Series via Symbolic Approximation | Chen, Carson, Kang, 2026 | 🔴 |

</details>

<details>
<summary><strong>LLM per fault diagnosis</strong> · 10 lavori · 🟢 3 · 🟡 5 · 🔴 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Evidence-Traceable LLM Reporting for Industrial Process Fault Detection and Diagnosis (EviFDD-Agent) | Chen, Peng, Zhang, Zhu, Hu, Zhai et al., 2026 | 🟢 |
| Exploring LLM-based Agentic Frameworks for Fault Diagnosis | Lee, Vidyaratne, Farahat, Gupta, 2025 | 🟢 |
| FaultExplainer: Leveraging Large Language Models for Interpretable Fault Detection and Diagnosis | Khan, Nahar, Chen, Constante-Flores, Li, 2025 | 🟢 |
| FD-LLM: Large Language Model for Fault Diagnosis of Machines | Qaid et al., 2024 | 🟡 |
| FD-LLM: Large Language Model for Fault Diagnosis of Complex Equipment | Lin et al., 2025 | 🟡 |
| LLM-TSFD: Industrial Time-Series Human-in-the-Loop Fault Diagnosis | Zhang, Xu, Li, Sun, Bao, Zhang, 2024 | 🟡 |
| A Large Language Model Enhanced Fault Diagnosis Framework for Chemical Processes | Liang & Sin, 2026 | 🟡 |
| Enhanced Fault Diagnosis Using Large Language Models and Probabilistic Label Fusion | Chen, Yao, Wang, Shi, Qin, Li et al., 2025 | 🟡 |
| CL-LLMOps: Fuzzy-Gated Verification of LLM Agents for Industrial Fault Diagnosis | Xiao, Xu, Li, Ding, Huang (identità da confermare), 2026 | 🔴 |
| DML–LLM Hybrid Architecture for Fault Detection and Diagnosis in Sensor-Rich Industrial Systems | Hu, Marandi, Modarres, 2026 | 🔴 |

</details>

<details>
<summary><strong>Calibrazione e predizione conforme</strong> · 18 lavori · 🟢 6 · 🟡 9 · 🔴 3</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Class-Conditional Conformal Prediction for Reliable Open-Set Fault Diagnosis in Safety-Critical Industrial Systems | Heddoub et al., 2026 | 🟢 |
| Testing for Outliers with Conformal p-values | Bates, Candès, Lei, Romano, Sesia, 2023 | 🟢 |
| Conditional validity of inductive conformal predictors | Vovk, 2012 / 2013 | 🟢 |
| Conformal Prediction via Transported Beta Laws | Ramos, Graziadei, Cabezas, 2026 | 🟢 |
| Universal distribution of the empirical coverage in split conformal prediction | Marques F., 2025 | 🟢 |
| Training-conditional coverage for distribution-free predictive inference | Bian & Barber, 2023 | 🟢 |
| Uncertainty-Aware Fault Diagnosis with Conformal Prediction | Heddoub, Diallo, Homri, Dantan, Siadat, 2025 | 🟡 |
| RBC-AD: conformal anomaly detection with explicit false-alarm control for the Tennessee Eastman Process | Mudasir, Asiri, Ameer, Al Reshan, Almansour, Awan, Shaikh, 2026 | 🟡 |
| Reducing false alarms in fault detection: a comparative analysis between conformal prediction and classical methods applied to PCA and autoencoders | Diallo, Homri, Dantan, 2025 | 🟡 |
| Quantifying and mitigating alarm fatigue caused by fault detection systems | Diallo, Homri, Boeuf, Dantan, Bonnet, 2026 | 🟡 |
| Conformal machine learning for reliable anomaly detection in industrial cyber-physical systems | Yuan, Li, Wang, Zhang, 2026 | 🟡 |
| Adaptive Conformal Anomaly Detection with Time Series Foundation Models for Signal Monitoring | Martinez Gil, O'Donncha, Gifford, Zhou, Patel, Vaculin, 2026 | 🟡 |
| Semi-supervised concept drift detection and adaptation based on conformal martingale framework | Zhang, Zhou, Zhang, Lu, Chai, 2025 | 🟡 |
| Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants | Kundačina, Vincan, Gojić, Ninković, Mišković, 2025 | 🟡 |
| The Tight Constant in the Dvoretzky–Kiefer–Wolfowitz Inequality | Massart, 1990 | 🟡 |
| CODiT: Conformal Out-of-Distribution Detection in Time-Series Data for Cyber-Physical Systems | Kaur, Sridhar, Park, Yang, Jha, Roy, Sokolsky, Lee, 2023 | 🔴 |
| Out-of-distribution Detection in Dependent Data for Cyber-physical Systems with Conformal Guarantees (estensione di CODiT) | Kaur, Yang, Sokolsky, Lee, 2024 | 🔴 |
| Between Resolution Collapse and Variance Inflation: Weighted Conformal Anomaly Detection in Low-Data Regimes | Hennhöfer & Preisach, 2026 | 🔴 |

Le sette voci 🟡 aggiunte nel 2026-09 calibrano o controllano esplicitamente l'errore **su TEP o su processi industriali**: è il terreno che questo studio non presidia, perché [§6.3](fot_walkthrough_conversazione_v2.md#sez-6-protocollo-di-valutazione) conta l'astensione come errore e [§12.2](fot_walkthrough_conversazione_v2.md#sez-12-che-cosa-il-framework-mostra-e-che-cosa) dichiara non verificato il funzionamento in mondo aperto. Le tre 🔴 riguardano domini ciberfisici estranei al processo chimico o sono puramente metodologiche. Nessuna vieta un'affermazione di questo documento. Le tre entrate del 2026-09-12 non sono applicative ma **fondazionali**, e cambiano il registro della categoria: sono le fonti primarie su cui poggia la calibrazione delle soglie di Fase B, e dicono con quali ipotesi ciascuna garanzia vale. Sono perciò le prime 🟢 teoriche del corpus. Massart (1990) entra invece come 🟡 e non 🟢: è la fonte della costante che rende DKW utilizzabile, quindi va citato **se** si riportano numeri DKW, ma non delimita alcuna affermazione di questo studio. Le due entrate del 2026-09-11 spostano leggermente il perimetro: Kundačina et al. controllano il tasso di falsi positivi su un impianto reale senza taratura manuale della soglia, e Zhang et al. usano gli intervalli conformi per **selezionare gli pseudolabel affidabili** prima di riaddestrare. Quest'ultimo è l'alternativa di principio a ciò che qui si fa di proposito — consumare gli pseudolabel opachi senza filtrarli — e va citato quando si giustifica la condizione E invece di un pesaggio per affidabilità.

</details>

<details>
<summary><strong>Allineamento TS–linguaggio</strong> · 9 lavori · 🟢 1 · 🟡 2 · 🔴 6</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| TableTime: Reformulating Time Series Classification as Training-Free Table Understanding with LLMs | Wang, Cheng, Mao, Zhou, Wang, Liu et al., 2025 | 🟢 |
| FD-Zero: LLM-Based Diagnosis Framework for Zero-Shot Mechanical Time-Domain Signals | Ran, Li, Li, Li, Wang, Chu et al., 2025 | 🟡 |
| Towards Generalizable Fault Diagnosis via LLM-Driven Hierarchical Cross-Modal Alignment (HCMA_GPT) | Wang, Sun, Zhang, Shao, Xiao, Liu, 2026 | 🟡 |
| T3: Domain-Agnostic Neural Time-Series Narration | Sharma, Brownstein & Ramakrishnan, 2021 | 🔴 |
| Repr2Seq: Time Series Representation to Sequence | Li et al., 2023 | 🔴 |
| TADACap: Time-Series Image Retrieval for Domain-Aware Captioning | Fons et al., 2024 | 🔴 |
| CLaSP: Contrastive Language–Signal Pretraining | Ito, Dohi & Kawaguchi, 2025 | 🔴 |
| TSLM: Time Series Language Model for Descriptive Caption Generation | Trabelsi, Boyd, Cao, Uzunalioğlu, 2025 | 🔴 |
| Towards Semantically Faithful Text-to-Time Series Generation via Agents and Spectral Conditioning | Wu, Lu, Zheng, Liu, Zhang, 2026 | 🔴 |

</details>

<details>
<summary><strong>Survey e benchmark</strong> · 8 lavori · 🟢 2 · 🟡 2 · 🔴 4</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Federated Reasoning LLMs: A Survey | Wei, Tong, Zhou, Xu, Gao, Tu et al., 2025 | 🟢 |
| Can LLMs Understand Time Series Anomalies? | Zhou & Yu, 2025 | 🟢 |
| BEDTime: A Unified Benchmark for Automatically Describing Time Series | Sen, Gottesman, Qiu, Bruss, Nguyen, Hartvigsen, 2025 | 🟡 |
| Data-Driven Fault Detection and Diagnosis in Industrial Process Systems: A Systematic Review and Perspective | Zhao, Yang, Kareck, Khan, Wang, 2025 | 🟡 |
| Empowering Time Series Analysis with Large Language Models: A Survey | Jiang et al., 2024 | 🔴 |
| Time-Series Large Language Models: A Systematic Review | Abdullahi et al., 2025 | 🔴 |
| Large Language Models for Time-Series Reasoning: A TMLR Survey | — | 🔴 |
| A Review of Fault Diagnosis Methods: From Traditional Machine Learning to Large Language Model Fusion Paradigm | Nie, Geng, Liu, 2026 | 🔴 |

</details>

<details>
<summary><strong>Diagnosi e monitoraggio di processo centralizzati su TEP</strong> · 24 lavori · 🟡 15 · 🔴 9</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| TopoCausFormer (TCF-STAE): spatio-temporal representation learning per la diagnosi in processi industriali complessi | Peng, Tang, Li, Simani, Dong, 2026 | 🟡 |
| A novel deep learning based fault diagnosis approach for chemical process with extended deep belief network | Wang, Pan, Yuan, Yang, Gui, 2020 | 🟡 |
| A novel fault diagnosis method based on CNN and LSTM and its application in fault diagnosis for complex systems | Huang, Zhang, Tang, Zhao, Lu, 2022 | 🟡 |
| HDLCNN-SHAP: hierarchical dilated CNN order-invariant e interpretabile per rilevazione e diagnosi chimica | Li, Peng, Wang, Wang, 2023 | 🟡 |
| DACN: dual adversarial and contrastive network per single-source domain generalization nella diagnosi | Li, Atoui, Li, 2025 | 🟡 |
| ES-QLSTM: entropy space quantum-behaved dung beetle optimized LSTM per la diagnosi di processo | Ao, Ma, Liu, Li, Han, 2026 | 🟡 |
| SAEDLPP: improved discrimination locality preserving projections integrate con sparse autoencoder | He, Li, Zhang, Xu, Zhu, 2021 | 🟡 |
| Fault Diagnosis of Chemical Processes Based on PCA-MSRN | Sun, 2026 | 🟡 |
| Improving Accuracy and Interpretability of CNN-Based Fault Diagnosis through an Attention Mechanism | Huang, Zhang, Liu, Zhao, 2023 | 🟡 |
| Inception-SECA-BiLSTM: estrazione multi-scala con attenzione per la diagnosi di processo | Lv, Wang, Gao, Zhang, 2026 | 🟡 |
| MDGCN: multichannel dynamic graph convolutional network, applicato all'altoforno | Wu, Wang, Gao, Zhang, Lou, Yang, 2023 | 🟡 |
| TDLN-trees: three-layer deep learning network random trees per la produzione chimica | Lu, Gao, Zou, Chen, Li, 2024 | 🟡 |
| Deep Anomaly Detection on Tennessee Eastman Process Data | Hartung et al., 2023 | 🟡 |
| Comparison of autoencoder architectures for fault detection in industrial processes | Spina et al., 2024 | 🟡 |
| Early-warning industrial fault detection based on physics-guided residual learning and calibrated CRNNs | Khan et al., 2026 | 🟡 |
| Automated feature learning for nonlinear process monitoring – stacked denoising autoencoder e regola k-NN | Zhang, Jiang, Li, Yang, 2018 | 🔴 |
| MSLKPCA: multi-block statistics local kernel PCA per il rilevamento non lineare | Zhou & Gu, 2020 | 🔴 |
| CVKA: Nonlinear Dynamic Process Monitoring Using Canonical Variate Kernel Analysis | Li, Yang, Cao, 2023 | 🔴 |
| Temporal-Spatial Neighborhood Enhanced Sparse Autoencoder per il monitoraggio dinamico non lineare | Li, Shi, Song, Tao, 2020 | 🔴 |
| TceOne: temporal CapsNet encoder con classificatore one-class per le industrie di processo | Wang, Zhao, Han, Wang, 2023 | 🔴 |
| Incipient Fault Detection Using Sliding Window K-Means Shared Dictionary Learning | Shen, Chen, Shang, Zhu, Hu, 2026 | 🔴 |
| Real-time incipient fault detection con KSVD a finestra scorrevole e limiti di controllo adattativi | Wang, Zhou, Liu, 2026 | 🔴 |
| DAE-PCA: learnable faster kernel-PCA per il rilevamento non lineare, realizzazione con deep autoencoder | Ren, Jiang, Yang, Tang, Zhang, Yu, 2024 | 🔴 |
| Odiowei & Cao: CVA con stime di densità kernel per il monitoraggio dinamico non lineare | Odiowei & Cao, 2010 | 🔴 |

Categoria aperta nel 2026-09. **Nessuno di questi lavori è federato e nessuno usa modelli linguistici**: entrano perché condividono il banco di prova, non perché incidano sul disegno. 🟡 quelli che affrontano la **diagnosi multi-classe** su TEP — lo stesso compito delle condizioni A/B/E — o che sono **benchmark comparativi**, e come tali sostengono la lettura di [§9.2](fot_walkthrough_conversazione_v2.md#sez-9-confronti-esterni-e-riferimenti) e [§12.4](fot_walkthrough_conversazione_v2.md#sez-12-che-cosa-il-framework-mostra-e-che-cosa) secondo cui il benchmark è facilmente separabile. 🔴 quelli di **sola rilevazione** o monitoraggio statistico, che restano sfondo del campo. La voce del 2026-09-11 (Khan et al., 2026) è la prima della categoria a riportare **probabilità calibrate, ECE e intervalli bootstrap** sul TEP: rafforza la lettura di §9.2 sulla separabilità del banco — circa 99% di accuratezza con macro-F1 0,93 su split a livello di run — e mostra quale forma di governo della soglia la letteratura centralizzata considera ormai attesa.

</details>

<details>
<summary><strong>Rilevamento di anomalie e soglie statistiche</strong> · 5 lavori · 🔴 5</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Anomaly Detection in Streams with Extreme Value Theory (SPOT/DSPOT) | Siffer, Fouque, Termier, Largouët, 2017 | 🔴 |
| Anomaly Detection in Streaming Nonstationary Temporal Data (oddstream) | Talagala, Hyndman, Smith-Miles, Kandanaarachchi, Muñoz, 2019 | 🔴 |
| SHNN-CAD: Online Learning and Sequential Anomaly Detection in Trajectories | Laxhammar & Falkman, 2014 | 🔴 |
| One-class classification-based control charts for multivariate process monitoring | Sukchotrat, Kim, Tsung, 2010 | 🔴 |
| Structure-Aware Unsupervised Anomaly Detection for Spacecraft Telemetry with Adaptive EVT Thresholding | Alcarria, Sánchez, Sempere et al., 2026 | 🔴 |

Categoria aperta nel 2026-09. Sfondo metodologico su soglie statistiche e rilevamento sequenziale, su domini estranei al processo chimico: flussi generici, traiettorie di sorveglianza, carte di controllo, telemetria satellitare. Nessuno tocca gli assi dell'esperimento; servono a documentare il perimetro consultato, non richiedono discussione.

</details>

Le stringhe di ricerca che hanno prodotto ciascuna voce sono conservate in [`docs/lit_review`](lit_review), insieme alle schede complete.

### 14.2 Schede estese: i lavori che influenzano il disegno

Le schede riguardano i lavori che **influenzano direttamente il disegno**. Stessa modalità di §14.1: apri la categoria che ti serve e richiudila con la **✕** o con il pulsante in fondo.

> **Le schede sono 29, i 🟢 di §14.1 sono 34.** Una scheda riguarda un 🔴 (FedSRD), quindi i vicini con scheda sono 28 e **sei** restano senza: FICAL, DP-FPL, FedDTPT, T2SP, TableTime e la rassegna sui federated reasoning LLM. È un arretrato dichiarato, non una svista. EviFDD-Agent è uscito dall'arretrato nel 2026-09: delimita §8.9–§8.10 del piano sperimentale e non poteva restare senza scheda. FaultExplainer non è mai entrato nell'arretrato: individuato l'11 settembre 2026 come **assente da §14.1** durante la riconciliazione con `papers/`, è stato inserito già con la sua scheda. Lo stesso vale per le tre 🟢 fondazionali sulla predizione conforme, entrate il 2026-09-12 con la scheda contestuale.

<details>
<summary><strong>Federazione testuale</strong> · 7 schede</summary>

**Federation over Text: Insight Sharing for Multi-Agent Reasoning**  
*Yao, Rabbani, Zaheer, Li, 2026*

Agenti locali trasformano traiettorie in insight; un server li raggruppa, distilla e ridistribuisce senza condividere esempi o gradienti.

**Rapporto con questo lavoro** — *Somiglianza:* gli insight in linguaggio naturale come oggetto federato. *Differenza:* il lavoro originale è multi-round, basato su server e cross-task; qui il trasferimento è a colpo singolo, fra pari e disgiunto per classe. *Implicazione:* è il precedente obbligatorio; il contributo è l'adattamento e la valutazione controllata.

**SYNAPSE: Federated Tool Routing via Typed Compendium Artifacts**  
*Chakraborty, Shah, Gupta, 2026*

Propone artefatti federati **tipizzati**: oggetti validati da schema il cui insieme di campi dichiarato rende la privacy per campo, la fusione e il trasferimento fra architetture diverse operazioni definite invece che approssimazioni euristiche. Un unico compendio viene consumato da quattro famiglie di modelli congelati con una perdita di circa due punti.

**Rapporto con questo lavoro** — *Somiglianza:* payload testuale strutturato fra client con modelli congelati ed eterogenei, e trasferimento dello stesso artefatto a consumatori diversi. *Differenza:* il compito è il routing di strumenti, non il riconoscimento di condizioni temporali; il nostro insight non è tipizzato da schema e non porta garanzie formali. *Implicazione:* è il **precedente diretto della portabilità lato consumatore** di [§10.1](fot_walkthrough_conversazione_v2.md#sez-10-verifiche-di-robustezza). Che un artefatto testuale congelato sopravviva al cambio di modello non è una scoperta di questo lavoro, e va detto. Rende inoltre esplicito ciò che il nostro insight non offre: nessuna struttura a campi su cui far leva per privacy o risoluzione dei conflitti.

**Federated In-Context Learning: Iterative Refinement (Fed-ICL)**  
*Wang, Wang, Huang, Wang, Yu, Yao, Lui, Zhou, 2025*

I client conservano gli esempi, il server coordina più round di raffinamento delle risposte, nessun parametro viene trasmesso; la convergenza è dimostrata su compiti di question answering.

**Rapporto con questo lavoro** — *Somiglianza:* nessuna trasmissione di parametri, la conoscenza utile resta in forma di contesto. *Differenza:* multi-round con server aggregatore su QA, contro trasferimento a colpo singolo fra pari su evidenza temporale disgiunta per classe. *Implicazione:* è il riferimento canonico che colloca questo lavoro dentro la ICL federata. Delimita anche il contributo: il nostro protocollo è **più povero** — un round, nessuna aggregazione — e questo va dichiarato come scelta di disegno, non presentato come semplificazione neutra.

**FERA: Uncertainty-Aware Federated Reasoning**  
*Wang, Huang, Wang, Wu, Wang, Yu, McAuley, Yao, Zhou, 2026*

Framework senza addestramento in cui il server non può ispezionare i dati dei client e l'affidabilità di ciascun contributo dipende dalla richiesta; i client emettono tracce di ragionamento con stime di incertezza e il server le sintetizza pesandole.

**Rapporto con questo lavoro** — *Somiglianza:* affronta la stessa domanda della condizione E, cioè che cosa accade quando la conoscenza federata è inaffidabile. *Differenza:* FERA gestisce l'inaffidabilità pesando per incertezza; qui l'inaffidabilità è **indotta deliberatamente** dalla permutazione congelata dei pseudolabel e misurata. *Implicazione:* rende meno isolato il controllo B/E — il problema è riconosciuto in letteratura — e indica l'estensione naturale: pesare gli insight peer invece di consumarli tutti alla pari.

**Can Textual Gradient Work in Federated Learning? (FedTextGrad)**  
*Chen, Jin, Deng, Chen, Huang, Yu, Li, 2025*

Studia sistematicamente l'aggregazione testuale in federated learning: i client caricano prompt ottimizzati localmente e il server li riassume. Mostra che il riassunto di contributi eterogenei perde dettaglio e degrada le prestazioni.

**Rapporto con questo lavoro** — *Somiglianza:* il testo come oggetto aggregato in un protocollo federato. *Differenza:* là il server riassume, qui i sei insight peer arrivano al ricevente **integri e con la propria provenienza**. *Implicazione:* sostiene a posteriori la scelta di [§4](fot_walkthrough_conversazione_v2.md#sez-4-produzione-e-trasferimento-degli-insight) di non aggregare, e fornisce l'argomento con cui rispondere a chi chiederà perché non si riassume.

**Time-FFM: LM-Empowered Federated Foundation Model for Time Series Forecasting**  
*Liu et al., 2024*

Adatta un backbone linguistico al forecasting federato di serie temporali con moduli condivisi e teste personalizzate.

**Rapporto con questo lavoro** — *Somiglianza:* federazione, foundation model e serie temporali. *Differenza:* forecasting parametrico contro diagnosi con insight. *Implicazione:* **vieta** qualsiasi claim di «primo FL+LLM per serie temporali».

**FedSRD: Communication-Efficient Federated LLM Fine-Tuning via Sparsify-Reconstruct-Decompose**  
*Yan et al., 2026*

Yan et al., WWW 2026. DOI `10.1145/3774904.3792144`. Sparsifica gli aggiornamenti LoRA, ricostruisce e decompone per ridurre il payload nel fine-tuning federato.

**Rapporto con questo lavoro** — *Somiglianza:* affronta il costo comunicativo della federazione con modelli linguistici. *Differenza:* scambia gradienti compressi, non insight testuali. *Implicazione:* è la ragione per cui §11 misura byte e token, e insieme la ragione per cui non se ne può dedurre un vantaggio di efficienza senza confronto diretto.

</details>

<details>
<summary><strong>FL disgiunto per classe</strong> · 7 schede</summary>

**FedMD: Heterogeneous Federated Learning via Model Distillation**  
*Li & Wang, 2019*

Scambia predizioni su dati pubblici per distillare modelli eterogenei.

**Rapporto con questo lavoro** — *Somiglianza:* l'oggetto federato non sono i pesi. *Differenza:* logit e dati pubblici contro insight in linguaggio naturale. *Implicazione:* precedente della catena FedMD → FedProto → trasferimento testuale, che è la traiettoria dell'oggetto federato richiamata in §13.

**FedProto: Federated Prototype Learning across Heterogeneous Clients**  
*Tan et al., 2022*

Condivide prototipi di classe nello spazio di embedding per dati non-IID.

**Rapporto con questo lavoro** — *Somiglianza:* conoscenza compatta specifica per classe. *Differenza:* vettori appresi contro testo citabile. *Implicazione:* è l'ispirazione dichiarata della baseline numerica di §9.1, che però **non implementa** l'algoritmo originale.

**FedCKD: Knowledge Distillation with Label-Exclusive Clients**  
*Le, Le, Le, Truong-Huu, 2026*

Studia la distillazione fra client con insiemi di etichette esclusivi.

**Rapporto con questo lavoro** — *Somiglianza:* classi non locali. *Differenza:* logit e parametri su immagini contro evidenza testuale da serie temporali. *Implicazione:* il regime disgiunto per classe **non è nuovo**; è una ragione per cui il contributo va circoscritto alla combinazione.

**Federated Zero-Shot Learning with Mid-Level Semantic Knowledge Transfer**  
*Sun, Si, Wu, Gong, 2024*

Trasferisce attributi semantici intermedi per riconoscere classi visive mai viste.

**Rapporto con questo lavoro** — *Somiglianza:* semantica condivisa per classi non osservate. *Differenza:* attributi strutturati su immagini contro insight liberi da serie temporali. *Implicazione:* rende distintivo il controllo B/E, non lo zero-shot in sé.

**FedMeta-FFD: Federated Meta-Learning for Fault Diagnosis**  
*Chen, Tang, Li, 2023*

Meta-apprendimento federato per adattare la diagnosi a nuove categorie di guasto con pochi esempi.

**Rapporto con questo lavoro** — *Somiglianza:* diagnosi federata con categorie nuove. *Differenza:* few-shot parametrico contro trasferimento di conoscenza testuale. *Implicazione:* è il vicino più prossimo sull'asse della diagnosi.

**Federated Meta-Learning with Transformer Fusion for Few-Shot Multi-Condition Fault Diagnosis**  
*Zhang et al., 2026*

Zhang et al., *Knowledge-Based Systems*, 2026. DOI `10.1016/j.knosys.2026.116739`. Combina meta-learning federato e fusione di feature via transformer, testato anche su TEP.

**Rapporto con questo lavoro** — *Somiglianza:* stesso benchmark, classi distribuite. *Differenza:* scambio di rappresentazioni intermedie, non di insight linguistici. *Implicazione:* è un comparatore numerico diretto sullo stesso processo, e la sua esistenza rende più visibile la lacuna registrata in §12.2.

**Federated Learning Based on Fuzzy Fusion Rules for Chemical Production Process Fault Diagnosis**  
*Xu et al., 2026*

Xu et al., *Sensors*, 2026. DOI `10.3390/s26113545`. Applica regole di fusione fuzzy all'aggregazione federata su processi chimici, incluso il TEP.

**Rapporto con questo lavoro** — *Somiglianza:* federated learning più TEP, stessa piattaforma sperimentale. *Differenza:* aggregazione parametrica, nessun layer testuale. *Implicazione:* comparatore diretto sull'asse dell'accuratezza in contesto federato.

</details>

<details>
<summary><strong>Contesto e memoria testuale</strong> · 1 schede</summary>

**Agentic Context Engineering (ACE)**  
*Zhang, Hu, Upasani et al., Zou, Olukotun, 2026*

Tratta il contesto come un manuale che si accumula e si organizza, e nomina due modalità di fallimento della sua costruzione: il *brevity bias*, per cui il riassunto conciso scarta il dettaglio di dominio, e il *context collapse*, per cui la riscrittura iterativa erode l'informazione.

**Rapporto con questo lavoro** — *Somiglianza:* il problema di produrre testo che conservi il dettaglio utile invece di comprimerlo. *Differenza:* ACE ottimizza il contesto con un ciclo di generazione, riflessione e curazione; qui il verbalizzatore è deterministico e gli insight sono prodotti una volta e congelati. *Implicazione:* dà un nome alle due patologie che [§3](fot_walkthrough_conversazione_v2.md#sez-3-dalla-serie-temporale-al-testo) e [§4](fot_walkthrough_conversazione_v2.md#sez-4-produzione-e-trasferimento-degli-insight) devono evitare, ed è il riferimento da citare quando si giustifica perché l'interfaccia testuale è deterministica e verificabile invece che riassuntiva.

</details>

<details>
<summary><strong>TS→testo fedele</strong> · 3 schede</summary>

**Truth-Conditional Captions for Time Series Data**  
*Jhamtani & Berg-Kirkpatrick, 2021*

Compone programmi di pattern e genera una didascalia solo quando il programma ne rende vere le condizioni; i moduli restano appresi.

**Rapporto con questo lavoro** — *Somiglianza:* enfasi sulla fedeltà della descrizione. *Differenza:* didascalia neurale monovariata contro renderer deterministico multivariato. *Implicazione:* serve a definire con precisione che cosa significa «fedele per costruzione» in §3.

**CGTime: Decoupling Perception from Description in Time-Series Reasoning**  
*Feng, Xie, Zhang, Li, Ling, Li, Liu*

Propone un approccio a percezione statistica separata dalla descrizione.

**Rapporto con questo lavoro** — *Implicazione:* è il braccio `CGTIME_STATS` del confronto delle rappresentazioni di §10.4, nella versione adattata.

**S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis**  
*Li & Zhao, 2025*

Li, B. & Zhao, C., *2025 CAA Symposium on Fault Detection, Supervision and Safety for Technical Processes (SAFEPROCESS)*, IEEE. DOI `10.1109/safeprocess67117.2025.11268252`; preprint arXiv `2603.08048`. Un operatore Signal-to-Semantic converte segnali di sensori multivariati in descrizioni in linguaggio naturale che catturano trend, periodicità e deviazione rispetto a una baseline normale costruita su 500 campioni; un metodo di diagnosi multi-turno ad albero interroga poi documenti di manutenzione e richiede dinamicamente altri segnali. 76,92% di accuratezza sul multiphase flow di Cranfield, **senza alcun dato di guasto**.

**Rapporto con questo lavoro** — *Somiglianza:* è la stessa catena — segnale numerico → descrizione testuale → diagnosi di una condizione mai osservata — sulle stesse tre famiglie di descrittori che usa il verbalizzatore V2. *Differenza:* è centralizzato e mono-agente, non c'è federazione né trasferimento fra pari; il banco è il multiphase flow, non il TEP; e la descrizione è generata da un LLM, non da un renderer deterministico. *Implicazione:* è il **precedente centralizzato più vicino alla catena FoT**, e delimita un claim. Impedisce di sostenere che costruire un artefatto testuale a partire da una modalità numerica per diagnosticare una classe non vista sia un problema non affrontato: lo è, fuori dal contesto federato. La rivendicazione va quindi ancorata al regime federato e al confronto controllato B/E, mai formulata «in generale».

</details>

<details>
<summary><strong>Rappresentazioni simboliche</strong> · 1 schede</summary>

**Bridging Time Series and Large Language Models via Symbolic Representation for HAR**  
*Pappa, Karvelis & Stylios, 2026*

Codifica simbolica di segnali da sensori per il consumo da parte di un modello linguistico.

**Rapporto con questo lavoro** — *Implicazione:* è il braccio `SAX_SYMBOLIC` del confronto delle rappresentazioni di §10.4.

</details>

<details>
<summary><strong>LLM per fault diagnosis</strong> · 3 schede</summary>

**Evidence-Traceable LLM Reporting for Industrial Process Fault Detection and Diagnosis (EviFDD-Agent)**  
*Chen, Peng, Zhang, Zhu, Hu, Zhai et al., 2026*

Preprint sottomesso a *Computers & Chemical Engineering*. Un *Evidence Citation Schema* lega i campi strutturati di un report diagnostico alle uscite dei tool che li hanno prodotti; tre metriche — Evidence Field Traceability, Untraceable Report Rate e un Report Actionability Score preliminare — misurano quanto il testo generato sia riconducibile a quelle uscite. Valutato sul TEP su sette configurazioni, n = 210, con intervalli di Wilson.

**Rapporto con questo lavoro** — *Somiglianza:* è l'unico lavoro del corpus che **misuri e pubblichi** la conformità di un artefatto testuale a uno schema, sullo stesso banco di prova. *Differenza:* misura la tracciabilità dei campi del **reporter** verso un evidence record già prodotto da tool deterministici; §8.9 del piano misura la validità dello schema lato **producer**, insieme a retry, troncamenti e token. Sono grandezze complementari, non equivalenti. *Implicazione:* delimita il claim di §8.10 punto 7, che non può dire «l'unica tabella del suo genere fra i lavori comparabili». Porta inoltre due indicazioni operative: i fallimenti di conformità si concentrano negli **identificatori di variabile** parafrasati (URR 77,1% nel prompt passivo, campi numerici a zero errori), e le configurazioni in cui i campi critici sono serializzati da una struttura deterministica raggiungono URR = 0. Con due modelli della stessa famiglia, il più grande risulta il meno conforme (URR 19,5% contro 1,4%) e 11,8× più lento.

**Exploring LLM-based Agentic Frameworks for Fault Diagnosis**  
*Lee, Vidyaratne, Farahat, Gupta, 2025*

Lee, X.Y., Vidyaratne, L., Farahat, A. & Gupta, C., *Annual Conference of the PHM Society* 17(1), 2025. DOI `10.36001/phmconf.2025.v17i1.4350`. ⚠️ Il titolo esatto contiene **«Agentic»**, che il nome del file omette. Confronta configurazioni di agenti LLM su dati di sensori grezzi: rappresentazione dell'ingresso (dati grezzi, statistiche descrittive, entrambe), presenza e forma dei dati di riferimento normali, architettura singolo-LLM contro multi-LLM, e apprendimento continuo da feedback.

**Rapporto con questo lavoro** — *Somiglianza:* mette a confronto **rappresentazioni** dello stesso segnale in ingresso a un LLM, che è ciò che fa §10.4, e contrappone un agente LLM a una baseline statistica, che è ciò che fa §9.1. *Differenza:* non è federato, non è sul TEP, e il compito primario è la rilevazione binaria più una classificazione a poche classi. *Implicazione:* delimita tre affermazioni. Primo, la superiorità della rappresentazione descrittiva sui dati grezzi è già pubblicata (F1 0,84 contro 0,79; accuratezza 0,73 contro 0,67): §10.4 la conferma su un altro dominio, non la scopre. Secondo, la baseline a regole ottiene F1 0,85 in rilevazione — **più di ogni configurazione LLM** — ma precision, recall e F1 pari a zero in classificazione: è il precedente pubblicato dello scenario di rischio di §9.3, e permette di riportarlo come pattern noto invece che come sconfitta. Terzo, gli LLM non migliorano con il feedback accumulato in contesto, il che sostiene §5 G4 senza chiuderne la domanda.

**FaultExplainer: Leveraging Large Language Models for Interpretable Fault Detection and Diagnosis**  
*Khan, Nahar, Chen, Constante-Flores, Li, 2025*

Khan, A., Nahar, R., Chen, H., Constante-Flores, G.E. & Li, C., *Computers & Chemical Engineering* (2025). DOI `10.1016/j.compchemeng.2025.109152`; preprint arXiv `2412.14492` (2024). La rilevazione è PCA con statistica T²; l'analisi dei contributi seleziona le sei variabili più deviate, che insieme a una descrizione testuale del TEP entrano nel prompt di GPT-4o e o1-preview, chiamati a proporre tre ipotesi di causa radice. Due condizioni: con la lista dei 15 guasti di Downs & Vogel (*Root Causes-Included Prompt*) e senza (*General Reasoning Prompt*), quest'ultima costruita per imitare un guasto mai incontrato.

**Rapporto con questo lavoro** — *Somiglianza:* è la stessa catena — poche feature deviate più una descrizione di processo → LLM congelato → ipotesi di causa per un guasto fuori dal repertorio — sullo stesso banco di prova. *Differenza:* è centralizzato e mono-agente, senza federazione né trasferimento fra pari; l'uscita è una spiegazione in prosa valutata qualitativamente guasto per guasto, non una classificazione con accuratezza e astensione misurate su una popolazione; e le feature vengono dalla PCA, non da un verbalizzatore deterministico. *Implicazione:* **delimita il claim sul guasto non visto**. Non si può sostenere che interrogare un LLM congelato sulla causa di un guasto TEP mai osservato sia un problema non affrontato: lo è, dal 2024, fuori dal contesto federato. La rivendicazione va ancorata al regime federato e al contrasto B/E, mai formulata in generale. Porta inoltre un avvertimento diretto su §8.6: quando le feature selezionate non contengono il meccanismo del guasto (casi 10 e 13), entrambi i modelli costruiscono una catena causale **plausibile e sbagliata** invece di astenersi. È la forma che prende l'«evidence quasi vuota» segnalata in S13, ed è una ragione in più per misurare l'astensione invece di darla per acquisita.


</details>

<details>
<summary><strong>Allineamento TS–linguaggio</strong> · 1 schede</summary>

**Can LLMs Understand Time Series Anomalies?**  
*Zhou & Yu, 2025*

Zhou, Z. & Yu, R. Il frontespizio riporta *Published as a conference paper at ICLR 2025*; i cataloghi registrano solo il preprint arXiv `2410.05440` (DOI `10.48550/arXiv.2410.05440`), quindi la sede non è confermata su catalogo. Studio controllato su quattro ipotesi: gli LLM capiscono le serie temporali meglio come **immagini** che come testo; **non** migliorano quando sono sollecitati a ragionare esplicitamente, e spesso peggiorano; la loro comprensione non deriva da bias di ripetizione o da abilità aritmetiche; il comportamento varia molto fra modelli.

**Rapporto con questo lavoro** — *Somiglianza:* è la domanda che sta sotto all'intera catena di §3 — che cosa un LLM sia effettivamente in grado di fare su una serie temporale. *Differenza:* presenta serie grezze o immagini, non testo verbalizzato da un renderer deterministico, e il compito è rilevazione di anomalie, non diagnosi multi-classe. *Implicazione:* sostiene indirettamente la scelta della verbalizzazione — se il numerico grezzo è un ingresso povero, tradurlo è la mossa giusta — e allo stesso tempo **impedisce di trattarla come contributo**. Delimita inoltre §8.7 e §10.2: che un budget di ragionamento più ampio migliori il risultato non è un'assunzione neutra, perché su serie temporali il ragionamento esplicito è documentato come non migliorativo. Su ingresso verbalizzato il risultato può non trasferirsi, ma l'assunzione va dichiarata e il capability pilot è il luogo dove il dato esiste già senza costo aggiuntivo.

</details>

<details>
<summary><strong>Calibrazione e predizione conforme</strong> · 6 schede</summary>

**Class-Conditional Conformal Prediction for Reliable Open-Set Fault Diagnosis in Safety-Critical Industrial Systems**  
*Heddoub et al., 2026*

Heddoub et al., *Journal of Process Control*, 2026. DOI `10.1016/j.jprocont.2026.103701`. Estende la predizione conforme al contesto open-set: diagnosticare i guasti noti e rifiutare le classi mai viste, con garanzie per classe.

**Rapporto con questo lavoro** — *Somiglianza:* il caso open-set visto dal singolo nodo assomiglia al regime disgiunto per classe; l'astensione su classi non note è il punto di contatto. *Differenza:* approccio statistico su feature, non linguistico. *Implicazione:* è il quadro di riferimento naturale per il limite registrato in §12.2 sull'astensione mai provata su guasti fuori catalogo.

**Testing for Outliers with Conformal p-values**  
*Bates, Candès, Lei, Romano, Sesia, 2023*

Bates, S., Candès, E., Lei, L., Romano, Y. & Sesia, M., *The Annals of Statistics* 51(1), 2023. DOI `10.1214/22-AOS2244`; preprint arXiv `2104.08279` (2021). P-value conformi per il rilevamento di outlier, in ottica di test multiplo. La **§1.1** fissa le ipotesi — punti **IID** e score con distribuzione continua — e la distinzione che qui conta: i p-value conformi sono indipendenti fra loro **solo condizionatamente al set di calibrazione**, mentre sono validi **solo marginalmente** su di esso. La **§3.1** enuncia il tasso di falsi positivi realizzato a soglia fissata come variabile aleatoria: FPR(α; D) ∼ Beta(ℓ, n+1−ℓ) con ℓ = ⌊(n+1)α⌋, e la garanzia marginale E[FPR] ≤ α ne è la **media**. Il risultato è attribuito a Vovk (2012), non rivendicato.

**Rapporto con questo lavoro** — *Somiglianza:* è la stessa struttura della calibrazione delle soglie di Fase B — score congelato, insieme di calibrazione, soglia realizzata, e un FAR che da quella soglia dipende. *Differenza:* il compito è test multiplo di outlier con controllo dell'FDR, non diagnosi multi-classe; nulla di federato né di linguistico. *Implicazione:* è la fonte primaria delle **tre garanzie da enunciare separatamente** — marginale, Beta condizionale alla calibrazione, proporzione a soglia congelata — ciascuna con le sue ipotesi. Vieta di scrivere «FAR garantito al 5%» per la soglia realizzata: con n = 350 e k = 334 la Beta(17, 334) dà P(FAR > 5%) = 41,68%. Impone inoltre di **dichiarare** la continuità dello score invece di darla per acquisita: nessun pareggio osservato non la dimostra.

**Conditional validity of inductive conformal predictors**  
*Vovk, 2012 / 2013*

Vovk, V., *Machine Learning* 92(2–3), 349–376, 2013. DOI `10.1007/s10994-013-5355-6`. Versione di conferenza: ACML 2012, PMLR 25:475–490 — **è questa che Bates cita** come fonte della legge Beta. In `papers/` ci sono ora **entrambe le versioni**: `…_ACML2012.pdf` sono gli atti (JMLR W&CP 25:475–490, editor Hoi e Buntine) e `…_predictors.pdf` è l'estesa su arXiv `1209.2673` del 10 agosto 2018. ✅ Confronto eseguito il 2026-09-12: **la numerazione coincide** — proposizione 2a, proposizione 2b, stesso enunciato, stessa condizione (7), stessa ipotesi IID nella §3. «Vovk (2012), proposizione 2b» è quindi citabile così com'è. La §3 lavora esplicitamente su esempi **IID** («we consider a canonical probability space in which Zᵢ … are i.i.d. random examples»). La proposizione 2a è il limite PAC ottenuto con Hoeffding; la **2b** è la versione esatta che si ferma prima di quel passaggio: Γ^ε è (E, δ)-valido se bin_{n,E}(⌊ε(n+1)−1⌋) ≤ δ, e **se e solo se** quando lo score è continuo. L'appendice A la riconduce alle regioni di tolleranza di Wilks (1941).

**Rapporto con questo lavoro** — *Somiglianza:* è il risultato che la decisione sulla calibrazione usa due volte — la legge Beta del FAR e il limite di tolleranza binomiale. *Differenza:* è teoria della predizione conforme, senza dominio industriale e senza federazione. *Implicazione:* precisa in che senso la 2b sia un'«alternativa» a DKW. Le due letture **non danno numeri diversi**: con n = 350 e k = 340, `Beta(11, 340).sf(0,05)` e `bin_{350; 0,05}(10)` valgono entrambe 3,526974%, perché sono la stessa quantità letta come coda oppure come coppia (E, δ). La conservatività in più si paga **spostando k**, non cambiando formula: k = 340 porta il FAR marginale da 4,843% a 3,134%. Secondo punto: anche la 2b poggia su **IID**, non sulla sola scambiabilità — non è una scorciatoia per evitare l'ipotesi che la Beta richiede.

**Conformal Prediction via Transported Beta Laws**  
*Ramos, Graziadei, Cabezas, 2026*

Ramos, T. R., Graziadei, H. & Cabezas, L. M. C. (Federal University of São Carlos; USP; Inria / Université Grenoble Alpes). Preprint in formato JMLR, **15 maggio 2026** (data di creazione del PDF). ⚠️ **Nessun DOI, nessun identificatore arXiv, assente da OpenAlex, Crossref e arXiv** alla verifica del 2026-09-12: i metadati non sono confermabili su fonte ufficiale e vanno riverificati prima della bibliografia. Prende la legge Beta della copertura condizionale alla calibrazione come **oggetto di riferimento a campione finito** e misura gli scostamenti da essa con distanze di Wasserstein su [0,1], separando due sorgenti distinte di comportamento non-IID: lo shift lato test agisce come mappa di trasporto sulla scala della copertura, mentre la dipendenza dentro la calibrazione cambia la legge delle statistiche d'ordine. Istanziato nei casi scale-shift, clusterizzato e stazionario mixing.

**Rapporto con questo lavoro** — *Somiglianza:* è esattamente la domanda che la calibrazione di Fase B lascia aperta — che cosa resta della Beta quando le unità di calibrazione non sono indipendenti. *Differenza:* lavoro teorico, nessun banco industriale, nessun LLM. *Implicazione:* attenua due formule e ne chiarisce una terza. Primo, il suo related work mostra un campo **attivo** — Marques F. (2025, *Statistics and Probability Letters*), Gazin (2024), la linea conformal + optimal transport — quindi «vuoto reale» e «unico lavoro del suo genere» non sono sostenibili. Secondo, e più utile: dichiara che l'ipotesi IID «can be relaxed to exchangeability» **nel senso di Marques F. (2025)**, dove la copertura *empirica* su un campione di test scambiabile converge quasi certamente a una legge Beta per de Finetti. Non è lo stesso oggetto del FAR condizionale a calibrazione fissata e test finito, che è ciò di cui parla il controesempio *U*, 1−*U*. I due enunciati convivono e vanno tenuti distinti nel testo: la scambiabilità basta per il **limite empirico**, non per la legge a campione finito.

**Universal distribution of the empirical coverage in split conformal prediction**  
*Marques F., 2025*

Marques F., P. C. (Insper, São Paulo), *Statistics & Probability Letters* 219 (2025) 110350. DOI `10.1016/j.spl.2024.110350`. Due teoremi, entrambi sotto **sola scambiabilità** dei dati e con funzione di conformità regolare (pareggi esclusi quasi certamente). **Teorema 1:** la copertura empirica di un lotto **finito** di m osservabili futuri soddisfa m·Cₘ ∼ Beta-Binomiale(⌈(1−α)(n+1)⌉, ⌊α(n+1)⌋). **Teorema 2:** per m → ∞, Cₘ converge **quasi certamente** a C∞ ∼ Beta(⌈(1−α)(n+1)⌉, ⌊α(n+1)⌋), per rappresentazione di de Finetti. Entrambe le leggi sono *universali*: dipendono solo da α e da n.

**Rapporto con questo lavoro** — *Somiglianza:* sono esattamente i due oggetti che la calibrazione di Fase B calcola — la beta-binomiale del conteggio di falsi allarmi e la Beta del FAR. *Differenza:* teoria pura, nessun banco, nessuna diagnosi. *Implicazione:* **scioglie l'apparente contraddizione** fra «serve IID» e «basta la scambiabilità», che senza questo lavoro resta un'obiezione aperta in review. La scambiabilità basta per la legge della copertura **empirica** — lotto finito, e limite quasi certo su lotto infinito. Non basta per l'oggetto diverso su cui poggia il controesempio *U*, 1−*U*: la probabilità di errore **condizionale alla calibrazione** per un singolo punto di test. Il teorema 2 chiede una successione scambiabile **infinita**, e *U*, 1−*U* è una coppia finita non estendibile: i due enunciati non si contraddicono, parlano di cose diverse. Conseguenza pratica: la beta-binomiale del registro può essere enunciata sotto scambiabilità; la frase sul FAR condizionale no. Resta intatto il problema vero, che è **la dipendenza fra le unità di calibrazione** — cinque blocchi contigui dello stesso tratto non sono né IID né dimostratamente scambiabili con il test.

**Training-conditional coverage for distribution-free predictive inference**  
*Bian & Barber, 2023*

Bian, M. & Barber, R. F., *Electronic Journal of Statistics* (2023). DOI `10.1214/23-EJS2145`; preprint arXiv `2205.03647`, 19 gennaio 2023. Ipotesi: punti di addestramento **IID**. Il loro **teorema 1 è dichiaratamente «Vovk [2012, Proposition 2a]»**, riportato per il solo split conformal. Il contributo proprio è **negativo**: per full conformal e jackknife+ la copertura condizionale all'addestramento è *impossibile* da garantire senza ipotesi aggiuntive (la stabilità algoritmica, che Liang & Barber 2025 mostrano essere sufficiente).

**Rapporto con questo lavoro** — *Somiglianza:* riguarda la stessa garanzia che la Fase B invoca, cioè che *la maggior parte* delle calibrazioni dia una soglia accettabile, non solo la media. *Differenza:* è regressione distribution-free, nessun dominio industriale. *Implicazione:* sostiene per esclusione la scelta di disegno. Lo split conformal non è la variante più debole per pigrizia: **è l'unica delle famiglie esaminate a portare con sé una garanzia condizionale all'addestramento senza ipotesi ulteriori**, e questo va scritto come argomento, non taciuto. Delimita però anche l'attribuzione: descriverlo come co-proprietario del risultato Beta insieme a Vovk è impreciso — per lo split conformal *riporta* Vovk. Se si cita la garanzia, la fonte è Vovk; Bian & Barber si citano per ciò che è **impossibile** altrove.



</details>

### 14.3 Riferimenti metodologici e di dominio

I seguenti riferimenti sostengono affermazioni presenti in questo documento e sono stati verificati su Crossref, OpenAlex, DataCite e PMLR quanto a titolo, autori, anno e sede.

| Riferimento | Che cosa sostiene, qui |
| --- | --- |
| Downs, J.J. & Vogel, E.F. (1993), *A plant-wide industrial process control problem*, Computers & Chemical Engineering 17(3). DOI `10.1016/0098-1354(93)80018-I` | La tassonomia dei meccanismi di guasto su cui si fonda la selezione di F1, F8, F10 e F13 (§2.5) |
| Bathelt, A., Ricker, N.L. & Jelali, M. (2015), *Revision of the Tennessee Eastman Process Model*, IFAC-PapersOnLine. DOI `10.1016/j.ifacol.2015.08.199` | La distinzione fra i 21 guasti standard del processo e i 28 ingressi di disturbo esposti dal simulatore modificato (§2.5) |
| Rieth, C.A., Amsel, B.D., Tran, R. & Cook, M.B. (2017), *Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation*, Harvard Dataverse. DOI `10.7910/DVN/6C3JR1` | La prassi consolidata di generare realizzazioni simulate indipendenti, che è ciò che fa la replica di §8 |
| Chiang, L.H., Russell, E.L. & Braatz, R.D. (2001), *Fault Detection and Diagnosis in Industrial Systems*, Springer. DOI `10.1007/978-1-4471-0347-9` | Il contesto in cui leggere il 36/36 della baseline numerica e i riferimenti centralizzati di §9 |
| McMahan, B., Moore, E., Ramage, D., Hampson, S. & Agüera y Arcas, B. (2017), *Communication-Efficient Learning of Deep Networks from Decentralized Data*, AISTATS, PMLR 54, 1273–1282 | Il termine di paragone rispetto al quale §12.2 dichiara **non** equivalenza |
| Wang, Z., Dai, Z., Póczos, B. & Carbonell, J. (2019), *Characterizing and Avoiding Negative Transfer*, CVPR. DOI `10.1109/CVPR.2019.01155` | Il quadro in cui collocare la degradazione sui guasti già noti di §8.5 e la variante local-first di §10.3 |
| Holm, S. (1979), *A Simple Sequentially Rejective Multiple Test Procedure*, Scandinavian Journal of Statistics 6(2), 65–70 | La correzione per confronti multipli usata nel confronto delle rappresentazioni (§10.4) |
| Field, C.A. & Welsh, A.H. (2007), *Bootstrapping Clustered Data*, JRSS-B. DOI `10.1111/j.1467-9868.2007.00593.x` | Il fondamento del bootstrap appaiato per cluster descritto in §6.5 |

### 14.4 Perimetro del corpus consultato

Le ricerche sono state eseguite su OpenAlex, arXiv, Scopus e Crossref, e sono state integrate da un **audit sul testo integrale** dei venticinque lavori raccolti in [`papers/archive/fed_fsl_2026-07/`](../papers/archive/fed_fsl_2026-07).

**Prima interrogazione — resta senza risultati.** L'intersezione fra trasferimento federato di conoscenza *testuale* e serie temporali non produce precedenti: nessuno dei venticinque lavori tocca serie temporali, diagnosi di guasto o dati industriali. È la lacuna su cui poggia la formulazione prudente di [§1.4](fot_walkthrough_conversazione_v2.md#sez-1-obiettivo-e-domanda-scientifica).

**Le altre due interrogazioni non sono più vuote, e la dichiarazione precedente va corretta.** La specificità semantica in apprendimento in contesto è affrontata, in forma diversa dalla nostra, da ACE, che nomina *brevity bias* e *context collapse* come modalità di degradazione del contesto, e da FedTextGrad, che misura la perdita di dettaglio nell'aggregazione testuale. L'affidabilità della conoscenza condivisa fra agenti è affrontata da FERA, con pesatura per incertezza, e da SYNAPSE, con risoluzione dei conflitti per campo.

**Nessuno di questi lavori usa però un controllo ad associazione corrotta a parità di contenuto e ordine.** La condizione E di [§7](fot_walkthrough_conversazione_v2.md#sez-7-studio-principale) resta, nel corpus consultato, senza equivalenti: gli altri mitigano l'inaffidabilità, non la inducono per misurarne l'effetto.

Questo **delimita il corpus consultato, non prova l'assenza di precedenti**. Sostiene una formulazione prudente sulla combinazione studiata, del tipo *to the best of our knowledge* — ora su un perimetro più ampio e verificato sul testo integrale, non soltanto su interrogazioni bibliografiche.

⚠️ **Correzione del 2026-09: la prima interrogazione va riletta in modo più stretto.** «L'intersezione fra trasferimento federato di conoscenza *testuale* e serie temporali non produce precedenti» resta vera per l'intersezione a **tre** assi, ed è su quella che poggia §1.4. Non è invece vera se si toglie il federato: S2S-FDD (Li & Zhao, 2025) costruisce descrizioni in linguaggio naturale da segnali industriali multivariati e diagnostica zero-shot senza dati di guasto, e T2SP e CGTime lavorano sul verbalizzatore. La formula da usare nomina quindi tutti e tre gli assi insieme, e non la sola coppia testo + serie temporali.

**Come è stata condotta la ricerca.** Fonti: arXiv, OpenReview e gli atti NeurIPS/ICML/ICLR, ACM DL, IEEE Xplore, Springer, Elsevier/ScienceDirect, Semantic Scholar, OpenAlex, Crossref, Scopus e DBLP. Intervallo fino a settembre 2026, con enfasi sul 2020–2026. Alle interrogazioni dirette si è aggiunto il *citation chaining*: all'indietro dalle referenze di Yao et al., in avanti dai vicini verso i lavori che li citano. Le stringhe esatte sono conservate in [`docs/lit_review`](lit_review).

**Esclusioni documentate.** Sei dei venticinque lavori — FedPOB, FedPrompt, pFedPG, pFedMoAP, DP²FL, pFedRAG — sono stati esaminati e lasciati fuori perimetro: aggiornano parametri, scambiano payload numerici (prompt continui, parametri di bandit, pesi di embedding) e in gran parte lavorano su benchmark visivi. Non hanno un corrispettivo testuale con cui confrontarsi.

### 14.5 I lavori più vicini

Cinque lavori sono abbastanza vicini da poter essere scambiati per il nostro. Per ciascuno conta sapere **quale affermazione ci impedisce** e quale resta possibile.

| Lavoro | Perché è vicino | Claim che ci vieta | Claim che resta |
| --- | --- | --- | --- |
| **Federation over Text** (Yao et al., 2026) | È il metodo che applichiamo | «proponiamo FoT» — qualsiasi rivendicazione di invenzione del metodo | Prima applicazione controllata a diagnosi su serie temporali multivariate con esperienza non-IID disgiunta per classe e controllo di specificità |
| **FICAL** (2024) | Stesso oggetto federato: testo in linguaggio naturale prodotto da un LLM, dati che restano locali | «primi a federare conoscenza testuale con dati locali via LLM» | Applicazione alla diagnosi con valutazione controllata del trasferimento su classi non viste |
| **FedCKD** | Struttura non-IID a classi esclusive quasi identica alla nostra | «la struttura disgiunta per classe è la novità» | L'oggetto federato è testo interpretabile e il trasferimento avviene in contesto, non via parametri |
| **FedMeta-FFD** (IEEE TNSE 2023) | Il vicino più diretto sull'asse diagnosi: federazione più nuove categorie di guasto | «primo trasferimento cross-client verso nuove classi di guasto» | Nessun esempio etichettato della classe non vista, oggetto testuale, nessun modello aggregato |
| **Federated zero-shot con trasferimento semantico di medio livello** (2024) | Federazione più semantica più classi non viste | «primo trasferimento semantico a classi non viste in FL» | La semantica è linguaggio naturale generato da un LLM, il dominio è la diagnosi, e c'è il controllo di corruzione |

**Sintesi.** Ogni singolo asse ha un vicino stretto. Nessuno dei cinque combina serie temporali multivariate, LLM in contesto, scambio testuale, classi localmente non viste, assenza di scambio di dati grezzi e controllo di specificità. La novità vive **nell'intersezione e nel disegno di valutazione**, non nei componenti.

> **Un sesto vicino, individuato dopo.** Questa analisi precede l'esame del corpus federato di §14.1. **SYNAPSE** va aggiunto come vicino sull'asse che qui non compare: la portabilità dello stesso artefatto testuale fra famiglie di modelli diverse. Vieta di presentare la portabilità cross-model di [§10.1](fot_walkthrough_conversazione_v2.md#sez-10-verifiche-di-robustezza) come capacità inedita; lascia possibile presentarla come conferma lato consumatore su evidenza temporale.

> **Un settimo vicino, aggiunto nel 2026-09.** **S2S-FDD** (Li & Zhao, 2025) è vicino sull'asse che gli altri sei non toccano: la catena segnale numerico → descrizione testuale → diagnosi di una condizione mai osservata, su un processo industriale reale. *Claim che ci vieta:* qualunque formulazione per cui tradurre una modalità numerica in testo diagnostico per riconoscere una classe non vista sarebbe un problema aperto. *Claim che resta:* la stessa catena in regime **federato**, con esperienza disgiunta per classe fra pari, controllo di specificità B/E e misura della degradazione sulle classi già note — nessuna delle quali compare in S2S-FDD, che è centralizzato, mono-agente e senza controllo a informazione corrotta.

> **Un ottavo vicino, aggiunto il 2026-09-11.** **FaultExplainer** (Khan, Nahar, Chen, Constante-Flores & Li, 2025) è vicino sull'asse più scomodo: interroga un LLM congelato sulla **causa di un guasto TEP non presente nel repertorio fornito**, sul nostro stesso banco di prova. *Claim che ci vieta:* qualunque formulazione per cui chiedere a un LLM di ragionare sulla causa di un guasto mai visto sul TEP sarebbe un problema aperto o inedito. *Claim che resta:* il regime federato, il trasferimento di insight fra pari con esperienza disgiunta per classe, il controllo B/E e la misura dell'astensione su una popolazione — FaultExplainer è centralizzato, mono-agente, con feature scelte dalla PCA, e valuta la spiegazione in prosa guasto per guasto invece di misurare accuratezza e astensione.

### 14.6 Tenuta della novità

**Tentativo di falsificazione.** La ricerca è stata condotta *contro* la nostra tesi, cercando un lavoro che combinasse tutti gli assi insieme. A criteri pieni non ne è emerso alcuno. Rilassando i criteri uno alla volta compaiono i vicini, e mostrano dove la nostra posizione è fragile:

- togliendo *serie temporali* → FoT e FICAL, equivalenti sul paradigma ma non sul dominio;
- togliendo *LLM e testo* → FedCKD e il trasferimento semantico zero-shot, equivalenti sulla struttura non-IID e sull'idea di classi non viste, ma non sull'oggetto testuale;
- togliendo *classi non viste* → Time-FFM, che è federazione parametrica su serie temporali;
- tenendo *serie temporali, diagnosi e LLM* ma togliendo la federazione → la famiglia FD-LLM, centralizzata, e **FaultExplainer**, che è centralizzato ma gira **sul TEP stesso**.

**La novità non è a livello di componente.** È una novità di combinazione, dominio e disegno di valutazione:

| Livello | Tenuta |
| --- | --- |
| Componente — verbalizzazione, insight testuali, federazione non parametrica, classi disgiunte | **Bassa.** Tutti noti singolarmente |
| Combinazione — l'unione di testo-LLM, serie temporali multivariate, classi disgiunte, non viste, nessun dato grezzo | **Moderata.** Il livello più difendibile |
| Valutazione — A/B/E con permutazione pre-registrata, freeze, held-out, pseudolabel opachi | **Moderata/alta.** Il pezzo migliore: il controllo B−E, cioè specificità semantica a parità di testo, è raro in questo filone |
| Dominio — prima applicazione documentata di un approccio FoT-like alla diagnosi su TEP | **Moderata, rivista al ribasso nel 2026-09.** Reale ma applicativa, e non più isolata: S2S-FDD porta la catena segnale→testo→diagnosi zero-shot su un processo industriale, sebbene centralizzata e su un altro banco; e FaultExplainer (Khan et al., 2025) porta un LLM congelato sulla causa di un guasto non visto **sul TEP stesso**, pur restando centralizzato e limitato alla spiegazione |
| Metodologia — la catena evidenza deterministica → ragionamento locale → trasferimento testuale | **Bassa/moderata.** Composizione di tecniche note, resa rigorosa |

La raccomandazione che ne segue è puntare il paper su **combinazione e valutazione**, non su componente e metodologia. La formula sicura, da usare così com'è:

> *To the best of our knowledge, we did not identify a prior method that federates locally-derived textual knowledge across agents with class-disjoint temporal experience to recognize locally unseen fault conditions, under a preregistered semantic-specificity control.*

Mai *no such method exists*.

### 14.7 Priorità bibliografica

Quindici riferimenti sono obbligatori. Non perché siano i più citati, ma perché ciascuno **delimita** qualcosa che non possiamo rivendicare.

| Riferimento | Che cosa delimita |
| --- | --- |
| Yao et al., *Federation over Text*, arXiv:2604.16778 | Il metodo che applichiamo: attribuzione obbligatoria |
| McMahan et al., *FedAvg*, AISTATS 2017 | La radice del FL, e il contrasto «noi non aggreghiamo parametri» |
| Li & Wang, *FedMD*, NeurIPS 2019 WS | Sposta l'oggetto federato ai logit |
| Lin et al., *Ensemble Distillation (FedDF)*, NeurIPS 2020 | Distillazione federata lato server |
| Tan et al., *FedProto*, AAAI 2022 | Prototipi invece di gradienti: l'analogo numerico dell'insight per classe |
| Zhu, Hong, Zhou, *FedGen*, ICML 2021 | Federazione di conoscenza sintetica |
| *Federated In-Context LLM Agent Learning*, arXiv:2412.08054 | Il vicino più pericoloso: federazione testuale con dati locali |
| Mohtashami et al., *Social Learning*, arXiv:2312.11441 | Il ponte fra distillazione e linguaggio naturale |
| Liu et al., *Time-FFM*, NeurIPS 2024 | FL più foundation model più serie temporali: vieta il primato su «FL+LLM per TS» |
| Li et al., *FedCoT*, arXiv:2508.10020 | Ragionamento federato parametrico |
| Kim et al., *T2SP*, arXiv:2606.12481 | Rappresentazione deterministica TS→LLM già attiva: blocca ogni novità sul verbalizzatore |
| Jhamtani & Berg-Kirkpatrick, *TRUCE*, EMNLP 2021 | Testo fattuale su serie temporali |
| Li et al., *Non-IID Data Silos*, ICDE 2022 | La tassonomia label-subset skew, cioè il nome esatto del nostro regime |
| Zhu et al., *FL on Non-IID Data*, Neurocomputing 2021 | L'inquadramento non-IID |
| He et al., *FedGKT*, NeurIPS 2020 | Trasferimento di conoscenza edge-server |

A questi si aggiungono i lavori del corpus federato di §14.1 che incidono sul disegno: SYNAPSE, Fed-ICL, FedTextGrad, FERA e ACE, con il ruolo descritto nelle schede di §14.2.

Dal 2026-09-12 se ne aggiungono altri due, su un asse diverso — quello di **ciò che si può affermare sul FAR della soglia calibrata**: **Bates et al. (2023)** per la distinzione fra garanzia marginale e legge Beta condizionale alla calibrazione, e **Vovk (2012/2013)** perché ne è la fonte e fornisce il limite di tolleranza binomiale esatto. **Ramos et al. (2026)** va citato solo se il testo afferma qualcosa sulla Beta sotto dipendenza, e finché i suoi metadati non sono confermati va trattato come preprint non verificato.

---
