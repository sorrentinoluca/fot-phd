# Archivio importato — Federated Few-Shot Learning, luglio 2026

> **Questo non è il corpus corrente.** È l'istantanea di un lavoro precedente, importata nel
> repository l'11 settembre 2026 e lasciata intatta. Non aggiungere paper qui: i nuovi paper
> vanno in `papers/`.

## Provenienza

Materiale di un lavoro autonomo su **Federated Few-Shot Learning** condotto intorno al
**28 luglio 2026** (data dichiarata dai tre audit). Gli identificatori `P001`…`P067` sono
quelli di quel lavoro e provengono dal flusso di conversione di `papers/tools/`: non hanno
alcun significato nel progetto FoT-TEP e non vanno rinumerati.

## Contenuto

| Percorso | Cosa contiene |
| --- | --- |
| `P*.md` | 25 conversioni Markdown di paper sulla federazione con modelli linguistici |
| `audit/` | I tre audit **di quel lavoro** più la matrice di confronto |

Gli audit in `audit/` appartengono al lavoro di luglio. **Non sono audit di processo
FoT-TEP**: quelli stanno in `docs/audits/`. Non sono neppure rassegne della letteratura
corrente: quelle stanno in `docs/lit_review/`. Restano qui perché senza il proprio corpus
non sono verificabili.

## Limiti noti di questa importazione

- **Nessun PDF e nessuna cartella `_images/`.** Le conversioni citano immagini
  (`P005_images/…`) che non sono state importate: tutti i riferimenti figurali sono rotti.
  Il testo, gli algoritmi e le descrizioni sperimentali sono invece integri.
- **`audit/Fed_ICL_Comparison_Matrix_v5.xlsx` non è versionato**: `.gitignore` esclude
  `*.xlsx`. Esiste solo su disco locale.
- **`P067.md` è byte-identico a `papers/Federation_Over_text_paper.md`** (MD5
  `dd9da17a…`). La copia canonica, con il suo PDF, è quella in `papers/`. Questa è una
  duplicazione dell'istantanea, non un secondo documento.

## Dove sono finite le conclusioni

Per non rileggere l'archivio da capo: i 19 lavori rilevanti e le loro implicazioni sono già
assorbiti nel walkthrough v2, §14.1 (corpus), §14.2 (cinque schede estese) e §14.4
(perimetro ed esclusioni), e nel blueprint del paper (§2 corrente E, §5.5, tabella
riferimenti). I sei esclusi — FedPOB, FedPrompt, pFedPG, pFedMoAP, DP²FL, pFedRAG — sono
nominati in §14.4 con la motivazione.

Lavori di questo archivio citati dal lavoro corrente: **P067** (FoT, Yao et al.), **P042**
(FICAL), **P065** (SYNAPSE), **P041** (Fed-ICL), **P030** (FERA), **P031** (FedTextGrad),
**P001** (ACE), **P009** (FedDTPT), **P021** (PPFedIT), **P022** (F²L), **P023** (pFedFSL),
**P066** (DP-FPL).
