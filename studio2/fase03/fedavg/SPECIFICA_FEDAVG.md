# Specifica FedAvg minimale — sotto-fase 03.14

**Stato:** specifica pre-addestramento congelata nel branch di lavoro il 2026-09-14; esecuzione
reale `pending` finché non è disponibile il lotto `normal_dev` di 03.9 e finché il piano
statistico 03.8 non riceve approvazione e verifica. Questa specifica non usa run di test.

## Perimetro e scopo

Il comparatore usa le firme 697-D di sviluppo di 03.6 e i Normal di sviluppo che saranno
pubblicati da 03.9. Gli otto client sono `F1`, `F2`, `F3`, `F8`, `F10`, `F13`, `F14`, `F15`;
ciascuno vede Normal e il proprio fault. Le etichette condivise, in quest'ordine, sono
`Normal`, `F1`, `F2`, `F3`, `F8`, `F10`, `F13`, `F14`, `F15`.

La scelta è FedAvg canonico (media dei parametri pesata per il numero di esempi; McMahan et al.,
2017). Questo riferimento è esterno al corpus corrente e va proposto alla successiva finestra
`Letteratura_LLM`; qui non viene aggiunto al corpus. Zhang et al. (2026) e Xu et al. (2026)
sono comparatori TEP da citare, non da riprodurre. OpenFedLLM/P030 e P041 motivano la presenza
di FedAvg; P065 mostra che il pavimento Local-Only è un comparatore già usato altrove.

## Ricetta congelata

| Voce | Valore |
| --- | --- |
| Input | firma `float64` di dimensione 697 |
| Normalizzazione | z-score per componente; media e deviazione calcolate solo sul fold di training di sviluppo, poi congelate; deviazioni `< 1e-8` poste a 1 |
| Rete | MLP `697 → 32 → 9`, ReLU, bias in entrambi gli strati |
| Inizializzazione | Glorot uniforme, generatore NumPy `PCG64`, seed `20260914` |
| Loss | cross-entropy pesata; nel perimetro di ogni training, peso classe `n/(K·n_k)` |
| Ottimizzatore | SGD senza momentum e senza weight decay |
| Learning rate | `0.05`, fisso |
| Batch | `32`; ultimo batch conservato |
| Epoche locali | `5` per round |
| Round | `40`, fissi; nessun early stopping |
| Partecipazione | tutti gli 8 client a ogni round |
| Aggregazione | media parametro per parametro, peso `n_client / Σ n_client` |
| Seed | `20260914`; shuffle derivato deterministicamente da modalità, round e client |
| Astensione | assente: `abstain=false` per ogni predizione |
| Selezione iperparametri | nessuna: ricetta unica, nessuna griglia e nessun accesso al test |

Lo sbilanciamento Normal/fault è trattato con i pesi di classe sopra, calcolati esclusivamente
sul training scope. I pesi non usano validation o test. La standardizzazione è globale sui soli
dati di sviluppo ammessi alla modalità: un'unica trasformazione per FedAvg e centralizzato;
nel pavimento ogni client stima la trasformazione sui propri dati di training.

## Tre modalità, stesso codice

1. **Pavimento locale (`local`)** — otto modelli indipendenti, inizializzazione e ricetta uguali.
   Per il client proprietario di `Fk` le sole classi visibili sono `Normal` e `Fk`. In inferenza
   i logit delle altre sette classi sono mascherati a `−∞`: non possono essere predette e ogni
   loro esempio è necessariamente errato. Non si inventano pesi o prototipi per classi assenti.
2. **FedAvg (`fedavg`)** — i nove output restano condivisi; ogni round parte dagli stessi pesi
   globali, addestra localmente tutti gli otto client e aggrega per numerosità.
3. **Soffitto centralizzato (`centralized`)** — la stessa rete e lo stesso numero complessivo di
   epoche (`40 × 5`) sui dati di sviluppo aggregati, senza federazione.

Il termine “soffitto” è operativo, non una garanzia matematica che il suo risultato superi
FedAvg in ogni campione.

## Fold tecnico e valutazione

Lo smoke reale, quando entrambi gli input esistono, è leave-one-batch-out: un identificativo
`batch` completo per fault e Normal viene escluso dal training e usato solo per il controllo
tecnico. Il fold è fissato prima dell'addestramento e non viene scelto in base al risultato.
Ogni run fisico è un cluster; tutte le finestre e tutti i client relativi allo stesso run restano
insieme. Lo smoke non è una stima di prestazione e non viene confrontato col braccio LLM.

Per ogni cluster e modalità si emettono gli stessi tre numeri del piano 03.8:

1. accuratezza su tutti i tentativi (primario);
2. tasso di astensione, **sempre 0 per costruzione**;
3. accuratezza sui non astenuti, quindi uguale al numero 1.

Il futuro confronto finale usa il bootstrap appaiato a cluster e stratificato per fault definito
da 03.8/03.10. Questa implementazione produce record compatibili ma non congela né reimplementa
il bootstrap mentre il piano 03.8 è ancora proposto. L'esecuzione sui run di test è vietata fino
alla conclusione di 03.11 e al congelamento del piano statistico.

## Integrità e determinismo

Il loader verifica SHA-256 del manifest e di ogni firma prima di leggerla, richiede esattamente
697 componenti finite e un join uno-a-uno con l'indice evaluator-side. Rifiuta percorsi con
componenti riservate a test/held-out. A parità di byte di input, configurazione, NumPy e seed,
l'hash canonico dei pesi deve coincidere. Il requisito runtime è `numpy==2.3.5`; la portabilità
bit-a-bit fra BLAS o versioni diverse non è rivendicata.

## Decisioni e dipendenze aperte

- 03.9 deve pubblicare formato, manifest e impronte di `normal_dev` e del formato comune.
- 03.8 resta `proposed_pending_author_decisions`: bootstrap seed/iterazioni e piano finale non
  sono assunti congelati.
- 03.11 deve congelare i run di test prima della valutazione finale.
- Nessun iperparametro richiede una decisione dell'autore: la ricetta è deliberatamente unica
  e minimale. Una modifica futura richiede nuova revisione della specifica prima del test.
