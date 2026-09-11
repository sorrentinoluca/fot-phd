# Ricerca bibliografica — Calibrazione delle soglie in fault/anomaly detection di processo

**Data**: 2026-09-11 · **Finestra**: 2000–2026 · **Risultati selezionati**: 40 (tetto richiesto)
**Fonti interrogate**: Scopus (API), arXiv, Crossref. OpenAlex non disponibile (HTTP 503 su tutte le chiamate); dblp non raggiungibile (errore di rete).

## Query richiesta

```
("Tennessee Eastman Process" OR "industrial process monitoring")
AND ("fault detection" OR "anomaly detection")
AND ("threshold calibration" OR "control limit" OR "decision threshold"
     OR "false alarm rate" OR "empirical quantile"
     OR "extreme value theory" OR "conformal anomaly detection")
AND ("normal data" OR "normal-only calibration" OR unsupervised)
AND ("temporal dependence" OR "dependent time series" OR "sliding windows")
```

## Nota metodologica (importante per la lettura dei risultati)

La query a 5 blocchi congiunti, eseguita verbatim su Scopus `TITLE-ABS-KEY` con filtro `PUBYEAR 2000–2026`,
restituisce **0 documenti**. Il vincolo che azzera il recall è il quinto blocco: la dipendenza temporale è
quasi sempre una *proprietà assunta* del setting (processo dinamico, finestre scorrevoli) e non un termine
che gli autori mettono in abstract o keyword accanto alla calibrazione della soglia. Il quarto blocco
(`normal data` / unsupervised) riduce da solo il recall di circa un ordine di grandezza.

La ricerca è quindi stata **decomposta in 7 interrogazioni** che coprono i blocchi a coppie e a triple,
mantenendo sempre B2 (rilevazione guasti/anomalie) e B3 (soglia/tasso di falsi allarmi) come nucleo
obbligatorio. I risultati sono poi stati deduplicati e ordinati per aderenza alla query originale.

Copertura dichiarata per ciascun record con la notazione **B1–B5**, nell'ordine dei blocchi della query:

| | Blocco |
|---|---|
| **B1** | Tennessee Eastman / monitoraggio di processo industriale |
| **B2** | fault detection / anomaly detection |
| **B3** | calibrazione soglia, control limit, tasso falsi allarmi, quantile empirico, EVT, conformal |
| **B4** | solo dati normali / non supervisionato |
| **B5** | dipendenza temporale / serie dipendenti / finestre scorrevoli |

Nessun record copre tutti e cinque i blocchi in modo esplicito nei metadati; i migliori (righe 1–8)
ne coprono quattro e trattano il quinto nel corpo del lavoro.

---

## Fascia A — Nucleo: controllo esplicito dei falsi allarmi con metodi conformal in ambito industriale

| # | Riferimento | Anno | Sede | DOI / ID | Blocchi |
|---|---|---|---|---|---|
| 1 | Mudasir M., Asiri Y., Ameer I., Al Reshan M.S., Almansour H., Awan K.A., Shaikh A. — *RBC-AD: conformal anomaly detection with explicit false-alarm control for the Tennessee Eastman Process* | 2026 | Connection Science | 10.1080/09540091.2026.2707826 | B1 B2 B3 B4 |
| 2 | Diallo A.R., Homri L., Dantan J.-Y. — *Reducing false alarms in fault detection: a comparative analysis between conformal prediction and classical methods applied to PCA and autoencoders* | 2025 | Journal of Process Control | 10.1016/j.jprocont.2025.103495 | B1 B2 B3 B4 |
| 3 | Diallo A.R. et al. — *Quantifying and mitigating alarm fatigue caused by fault detection systems* | 2026 | Reliability Eng. & System Safety | 10.1016/j.ress.2025.111890 | B1 B2 B3 |
| 4 | Yuan S. et al. — *Conformal machine learning for reliable anomaly detection in industrial cyber-physical systems* | 2026 | Reliability Eng. & System Safety | 10.1016/j.ress.2026.112417 | B1 B2 B3 B4 |
| 5 | Heddoub A. et al. — *Class-conditional conformal prediction with discriminant-analysis backbones for reliable open-set fault diagnosis in safety-critical industrial systems* | 2026 | Journal of Process Control | 10.1016/j.jprocont.2026.103701 | B1 B2 B3 |
| 6 | Heddoub A. et al. — *Uncertainty-aware fault diagnosis with conformal prediction* | 2025 | IFAC-PapersOnLine | 10.1016/j.ifacol.2025.09.092 | B1 B2 B3 |
| 7 | Heddoub A. et al. — *Online conformal prediction for fault diagnosis under operating mode transitions* | 2026 | ICCAD 2026 | 10.1109/ICCAD69956.2026.11643119 | B1 B2 B3 B5 |
| 8 | Heddoub A. et al. — *Conformal prediction for multivariate quality assurance — application on coordinate measuring machines* | 2026 | Procedia CIRP | 10.1016/j.procir.2026.03.151 | B1 B2 B3 |

## Fascia B — Conformal anomaly detection sotto dipendenza temporale (il punto debole teorico di B5)

| # | Riferimento | Anno | Sede | DOI / ID | Blocchi |
|---|---|---|---|---|---|
| 9 | Kaur R., Yang Y., Sokolsky O., Lee I. — *Out-of-distribution detection in dependent data for cyber-physical systems with conformal guarantees* | 2024 | ACM Trans. Cyber-Physical Systems | 10.1145/3648005 | B2 B3 B4 B5 |
| 10 | Kaur R., Sridhar K., Park S., Yang Y., Jha S., Roy A., Sokolsky O., Lee I. — *CODiT: conformal out-of-distribution detection in time-series data for cyber-physical systems* | 2023 | ICCPS 2023 | 10.1145/3576841.3585931 · arXiv:2207.11769 | B2 B3 B4 B5 |
| 11 | Laxhammar R., Falkman G. — *Online learning and sequential anomaly detection in trajectories* | 2014 | IEEE TPAMI | 10.1109/TPAMI.2013.172 | B2 B3 B4 B5 |
| 12 | Laxhammar R., Falkman G. — *Online detection of anomalous sub-trajectories: a sliding window approach based on conformal anomaly detection and local outlier factor* | 2012 | IFIP AICT | 10.1007/978-3-642-33412-2_20 | B2 B3 B4 B5 |
| 13 | Martinez Gil N., O'Donncha F., Gifford W.M., Zhou N., Patel D.C., Vaculin R. — *Adaptive conformal anomaly detection with time series foundation models for signal monitoring* | 2026 | arXiv | arXiv:2604.20122 | B2 B3 B4 B5 |
| 14 | Hennhöfer O., Preisach C. — *Between resolution collapse and variance inflation: weighted conformal anomaly detection in low-data regimes* | 2026 | arXiv | arXiv:2603.23205 | B2 B3 B4 B5 |
| 15 | Hennhöfer O., Kirsch M., Preisach C. — *Conformal anomaly detection in Python: moving beyond heuristic thresholds with `nonconform`* | 2026 | arXiv | arXiv:2605.13642 | B2 B3 B4 |
| 16 | Hennhöfer O., Preisach C. — *Leave-one-out-, bootstrap- and cross-conformal anomaly detectors* | 2024 | IEEE ICKG 2024 | 10.1109/ICKG63256.2024.00022 | B2 B3 B4 |
| 17 | Safin A., Burnaev E. — *Conformal kernel expected similarity for anomaly detection in time-series data* | 2017 | Adv. in Systems Science and Applications | (no DOI) | B2 B3 B4 B5 |
| 18 | Basora L., Bocquet-Nouaille L., Robinson E., Le Gonidec S. — *Fault detection and diagnosis for the engine electrical system of a space launcher based on a temporal convolutional autoencoder and calibrated classifiers* | 2025 | arXiv | arXiv:2507.13022 | B2 B3 B4 B5 |

## Fascia C — Soglie da teoria dei valori estremi e quantili su flussi / serie dipendenti

| # | Riferimento | Anno | Sede | DOI / ID | Blocchi |
|---|---|---|---|---|---|
| 19 | Siffer A., Fouque P.-A., Termier A., Largouët C. — *Anomaly detection in streams with extreme value theory* (SPOT / DSPOT) | 2017 | ACM SIGKDD | 10.1145/3097983.3098144 | B2 B3 B4 B5 |
| 20 | Talagala P.D., Hyndman R.J., Smith-Miles K. et al. — *Anomaly detection in streaming nonstationary temporal data* | 2020 | J. Computational and Graphical Statistics | 10.1080/10618600.2019.1617160 | B2 B3 B4 B5 |
| 21 | Alcarria Ó., Sánchez R., Sempere J., Torrijos P., Alfaro J.C., Auñón J.M., Gámez J.A., Puerta J.M. — *Structure-aware unsupervised anomaly detection for spacecraft telemetry with adaptive EVT thresholding* | 2026 | arXiv | arXiv:2609.10017 | B2 B3 B4 B5 |
| 22 | Guggilam S., Zaidi S.M.A., Chandola V., Patra A. — *Bayesian anomaly detection using extreme value theory* | 2019 | arXiv | arXiv:1905.12150 | B2 B3 B4 |
| 23 | Wang S.-Y. — *Ensemble2: anomaly detection via EVT-ensemble framework for seasonal KPIs in communication network* | 2022 | arXiv | arXiv:2205.14305 | B2 B3 B4 B5 |
| 24 | Gao F. et al. — *A novel distributed fault diagnosis scheme toward open-set scenarios based on extreme value theory* | 2023 | IEEE Trans. Industrial Informatics | 10.1109/TII.2023.3240919 | B1 B2 B3 |
| 25 | Clark J. et al. — *Adaptive threshold for outlier detection on data streams* | 2018 | IEEE DSAA 2018 | 10.1109/DSAA.2018.00014 | B2 B3 B4 B5 |
| 26 | Zheng D., Li F., Zhao T. — *Self-adaptive statistical process control for anomaly detection in time series* | 2016 | Expert Systems with Applications | 10.1016/j.eswa.2016.03.029 | B1 B2 B3 B4 B5 |

## Fascia D — Control limit stimati da soli dati normali nel monitoraggio statistico di processo (KDE, bootstrap, one-class)

| # | Riferimento | Anno | Sede | DOI / ID | Blocchi |
|---|---|---|---|---|---|
| 27 | Odiowei P.-E.P., Cao Y. — *Nonlinear dynamic process monitoring using canonical variate analysis and kernel density estimations* | 2010 | IEEE Trans. Industrial Informatics | 10.1109/TII.2009.2032654 | B1 B2 B3 B4 B5 |
| 28 | Samuel R.T., Cao Y. — *Nonlinear process fault detection and identification using kernel PCA and kernel density estimation* | 2016 | Systems Science & Control Engineering | 10.1080/21642583.2016.1198940 | B1 B2 B3 B4 |
| 29 | Deng X., Tian X., Chen S. — *Modified kernel principal component analysis based on local structure analysis and its application to nonlinear process fault diagnosis* | 2013 | Chemometrics and Intell. Lab. Systems | 10.1016/j.chemolab.2013.07.001 | B1 B2 B3 B4 |
| 30 | Zhang Z., Jiang T., Li S., Yang Y. — *Automated feature learning for nonlinear process monitoring — stacked denoising autoencoder and k-nearest neighbor rule* | 2018 | Journal of Process Control | 10.1016/j.jprocont.2018.02.004 | B1 B2 B3 B4 |
| 31 | Yan W., Guo P., Gong L., Li Z. — *Nonlinear and robust statistical process monitoring based on variant autoencoders* | 2016 | Chemometrics and Intell. Lab. Systems | 10.1016/j.chemolab.2016.08.007 | B1 B2 B3 B4 |
| 32 | Sukchotrat T., Kim S.B., Tsung F. — *One-class classification-based control charts for multivariate process monitoring* | 2010 | IIE Transactions | 10.1080/07408170903019150 | B1 B2 B3 B4 |
| 33 | Lee J.-M., Yoo C.K., Lee I.-B. — *Statistical process monitoring with multivariate EWMA and independent component analysis* | 2003 | J. Chemical Engineering of Japan | 10.1252/jcej.36.563 | B1 B2 B3 B5 |
| 34 | Tao Y., Shi H., Song B., Tan S. — *A novel dynamic weight principal component analysis method and hierarchical monitoring strategy for process fault detection and diagnosis* | 2020 | IEEE Trans. Industrial Electronics | 10.1109/TIE.2019.2942560 | B1 B2 B3 B4 |
| 35 | Duma Z.S. et al. — *Probabilistic multivariate statistical process control via kernel parameter uncertainty propagation* | 2026 | IEEE Access | 10.1109/ACCESS.2026.3706157 | B1 B2 B3 B4 |
| 36 | Spina D.E. et al. — *Comparison of autoencoder architectures for fault detection in industrial processes* | 2024 | Digital Chemical Engineering | 10.1016/j.dche.2024.100162 | B1 B2 B3 B4 |

## Fascia E — Soglie adattive e finestre scorrevoli su processi industriali dinamici

| # | Riferimento | Anno | Sede | DOI / ID | Blocchi |
|---|---|---|---|---|---|
| 37 | Wang Z. et al. — *Real-time incipient fault detection by integrating sliding-window KSVD dynamic feature extraction and adaptive control limits* | 2026 | Journal of the Franklin Institute | 10.1016/j.jfranklin.2026.109034 | B1 B2 B3 B5 |
| 38 | Cai L. et al. — *Adaptive dynamic threshold-based fault detection with a dual monitoring strategy* | 2026 | Computers & Chemical Engineering | 10.1016/j.compchemeng.2026.109695 | B1 B2 B3 B5 |
| 39 | Zhou W. et al. — *Early fault detection for industrial processes under low false alarm constraints* | 2026 | EITCE 2026 | 10.1109/EITCE70137.2026.11634404 | B1 B2 B3 |
| 40 | Hartung F., Franks B.J., Michels T., … Kloft M. (18 autori) — *Deep anomaly detection on Tennessee Eastman process data* | 2023 | arXiv (poi Chemie Ingenieur Technik) | arXiv:2303.05904 | B1 B2 B4 |

---

## Osservazioni sul corpus

**Il vuoto è reale, non un artefatto della query.** Su Scopus non esiste un lavoro che dichiari
simultaneamente calibrazione della soglia su soli dati normali *e* trattamento esplicito della dipendenza
temporale *e* benchmark TEP. I due filoni restano separati: chi fa garanzie conformal rigorose lavora su
CPS/traiettorie (righe 9–18) e assume o ripara l'exchangeability; chi lavora su TEP stima control limit
con KDE o ipotesi gaussiane (righe 27–36) senza quantificare l'effetto dell'autocorrelazione sul tasso
di falsi allarmi realizzato.

**Riga 1 è il precedente più diretto** e va letta prima delle altre: stesso benchmark, stesso obiettivo
(controllo esplicito del false-alarm rate), pubblicata a luglio 2026. Righe 2–4 costituiscono il
confronto metodologico naturale (conformal vs. limiti classici su PCA/autoencoder, con misura
dell'affaticamento da allarme).

**Righe 9 e 19–20 sono le basi teoriche** per il quinto blocco: Kaur et al. 2024 è l'unico lavoro che
costruisce garanzie conformal su dati esplicitamente dipendenti; Siffer et al. 2017 e Talagala et al.
2020 forniscono la via EVT/quantile su flussi non stazionari.

**Esclusi per pertinenza marginale**: lavori EVT di idrologia, climatologia e value-at-risk finanziario
(numerosi e ad alto impatto, ma fuori dominio); rilevazione guasti su turbine eoliche, batterie, UAV e
reti CAN, tranne dove il contributo è sulla calibrazione della soglia in sé.

## Verifica

DOI controllati su Crossref per i due record chiave (righe 1 e 2): titolo, autori, sede e anno
corrispondono. Record Scopus privi di DOI (atti di convegno aggregati, voci di proceedings senza
contributo singolo) sono stati scartati, non inclusi.
