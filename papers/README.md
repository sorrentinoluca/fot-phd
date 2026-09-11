# Paper della letteratura

Questa cartella contiene **solo paper trovati in letteratura**. Regole:

- un paper sta qui in una copia sola, come `<nome>.pdf` + `<nome>.md` + `<nome>_images/`;
- una conversione `.md` senza il suo PDF e le sue immagini non è archiviata, è orfana;
- `tools/` contiene il convertitore PDF -> Markdown, non è materiale di letteratura;
- `archive/` contiene istantanee importate da lavori precedenti: **non sono il corpus
  corrente** e hanno un proprio README di provenienza.

La tabella riporta solo ciò che `ls` non dice: titolo esteso, autori, venue, DOI e le
disambiguazioni fra omonimi. Va aggiornata quando si aggiunge un paper, non dopo.

| Nome file | Descrizione |
| --- | --- |
| `A_Novel_Feature_Extraction_Approach_for_Mechanical_Fault_Diagnosis_Based_on_ESAX_and_BoW_Model.pdf` | "A Novel Feature Extraction Approach for Mechanical Fault Diagnosis Based on ESAX and BoW Model": estrazione di feature per diagnosi di guasti meccanici tramite rappresentazione simbolica ESAX e modello Bag-of-Words. |
| `Bridging_time_series_and_large_language_models_via_symbolic_representation_for_human_activity_recognition_2026.pdf` | "Bridging time series and large language models via symbolic representation for human activity recognition" (Elsevier, 2026): rappresentazione simbolica come interfaccia fra serie temporali e LLM per il riconoscimento di attività umane. |
| `FD_LLM_2024.pdf` | "FD-LLM: Large Language Model for Fault Diagnosis of Machines" — Qaid et al., arXiv 2024 (DOI 10.48550/arXiv.2412.01218). Diagnosi di guasti su macchine tramite LLM; omonimo ma distinto da `FD_LLM_LINN_2025.pdf`. |
| `FD_LLM_LINN_2025.pdf` | "FD-LLM: Large language model for fault diagnosis of complex equipment" — Lin et al., Advanced Engineering Informatics 2025 (DOI 10.1016/j.aei.2025.103208). Diagnosi di guasti su impianti complessi tramite LLM. |
| `Federation_Over_text_paper.pdf` | "Federation over Text: Insight Sharing for Multi-Agent Reasoning": condivisione di insight in linguaggio naturale come canale di federazione per il ragionamento multi-agente. Riferimento concettuale del progetto FoT. |
| `Truth_Conditional_Captions_Jhamtani_2021.pdf` | "Truth-Conditional Captions for Time Series Data" — Jhamtani & Berg-Kirkpatrick, EMNLP 2021 (DOI 10.18653/v1/2021.emnlp-main.55). Generazione di descrizioni testuali di serie temporali orientata alla correttezza fattuale. |
| `CAN_LLMS_UNDERSTAND_TIME_SERIES_ANOMALIES.pdf` | "Can LLMs Understand Time Series Anomalies?" — Zhou et al. Valutazione critica della capacità dei modelli linguistici di riconoscere anomalie in serie temporali. |
| `Decoupling_Perception_from_Description.pdf` | "Decoupling Perception from Description: Computation-Grounded Representation Alignment between Multivariate Time Series and Language". Percezione statistica separata dalla descrizione; braccio `CGTIME_STATS` del confronto delle rappresentazioni. |
| `EXPLORING_LLM_BASED_FRAMEWORKS_FOR_FAULT_DIAGNOSIS.pdf` | "Exploring LLM-based Frameworks for Fault Diagnosis" — Lee, Vidyaratne, Farahat, Gupta. Rassegna di architetture LLM applicate alla diagnosi di guasto. |
| `FaultExplainer_Leveraging_Large_Language_Models_for_Interpretable_Fault_Detection_and_Diagnosis.pdf` | "FaultExplainer: Leveraging Large Language Models for Interpretable Fault Detection and Diagnosis". Diagnosi interpretabile con LLM; riferimento di dominio sul TEP. |
| `S2S_FDD_Bridging_Industrial_Time_Series_and_Natural_Language_for_Explainable_Zero-shot_Fault_Diagnosis.pdf` | "S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis". Diagnosi zero-shot spiegabile da serie temporali industriali a linguaggio naturale. |
| `representing_time_series_as_structured_programs.pdf` | "Representing Time Series as Structured Programs for LLM Reasoning": rappresentazione di serie temporali come programmi strutturati a supporto del ragionamento degli LLM. |

## Sottocartelle

| Percorso | Contenuto |
| --- | --- |
| `tools/` | Convertitore PDF -> Markdown arricchito (era `pdf_to_md_converter/`). |
| `archive/fed_fsl_2026-07/` | Istantanea di un lavoro di luglio 2026 su Federated Few-Shot Learning: 25 conversioni `P*.md` e i suoi audit. Vedi il README della cartella. |
