# Specifica pre-generazione — lotto Normal di sviluppo `normal_dev`

**Data:** 2026-09-14  
**Base di lavoro:** `origin/main` a `46c0b62`  
**Fonte di piano:** revisione 7, commit `a572d1c`, §6.2  
**Stato:** decisione dell'autore del 2026-09-13 attuata nella specifica; nessuna simulazione eseguita.

Questa è un'integrazione pre-specificata del disegno rispetto al nuovo lotto. La revisione 7 del
piano distingue i Normal eliminati dalla revisione 5 — destinati a baseline, calibrazione e
verifica — dalle nuove osservazioni di sviluppo necessarie al prototipo Normal, agli esempi locali
e ai client FedAvg. Il piano è la fonte: questa specifica non ne riscrive il contenuto.

## Disegno e assegnazione

- 40 run Normal nuovi, cinque assegnati in esclusiva a ciascuno degli otto agenti nel piano CSV
  prima della generazione;
- stesso generatore Normal, modello, MEX base e configurazione qualificati in Fase 02 e riusati
  nella 03.5; Mode 1, `Ts_base=0.0005 h`, uscita ogni minuto, Philox4x32-10, chiave
  `0x464f545445503032`, stream uguale all'indice uint64;
- stream 60000–60039, disgiunti dai piani di Fase 02, dai pilot 1000–1009, dai fault
  30000–30039, da `cal_thr` 40000–40349, dagli smoke 49900–49901 e da `far_ver`
  50000–50149;
- 65 h per run: `[0,20)` burn-in escluso, `[20,25)` controllo escluso, otto finestre half-open
  da 5 h in `[25,65)` ammesse allo sviluppo; il campione all'endpoint 65 h non appartiene a una
  finestra;
- 320 finestre da 40 run. Le otto finestre dello stesso run sono dipendenti e non sono otto
  repliche indipendenti.

Il piano immutabile è `plans/normal_dev.csv`, namespace
`fot-tep/fase03/normal_dev/v1`. L'ordine è `agent_1` … `agent_8`, poi indice 1 … 5; lo stream è
`60000 + 5*(agent_index-1) + (run_index-1)`.

## Ruoli ammessi ed esclusi

Uso ammesso: prototipo Normal globale e locale della 03.9, esempio locale Normal della 03.10 e
classe Normal dei client della 03.14 (inclusi pavimento e soffitto). Uso vietato: fit della
normalizzazione, scelta o calibrazione di soglie, verifica FAR, selezione del protocollo e test.

Le evidence passano dalle stesse funzioni congelate e dalle stesse guardie di impronta della 03.6.
Usano N1–N5 e le soglie V2 soltanto nella destinazione U3: normalizzazione e flag del
verbalizzatore. `normal_dev` separa le osservazioni di sviluppo dai dati che definiscono la
trasformazione, ma non elimina questa dipendenza; se R2 decade o si passa a `baseline_fit_new`, le
evidence Normal vanno rigenerate con la stessa regola fail-closed della 03.6.

## Selezione pre-specificata dell'esempio locale Normal

Per ogni agente la 03.10 usa **il run locale con `agent_run_index=1`, finestra 1 `[25,30)`**.
Nessun criterio sui valori, sulla separabilità o sulla qualità può sostituire questa selezione.
Se il run non è tecnicamente valido, non si sceglie post-hoc un altro esempio: serve una procedura
di sostituzione pre-specificata e autorizzata prima di osservare output del modello.

## Manifest, errori e accettazione

Il launcher delega al generatore qualificato di Fase 02 e produce un workbook e una riga di
`generation_manifest.csv` per run. Sono obbligatori almeno identità, stream, algoritmo e chiave
RNG, contatori, impronte MEX/modello, tempi, stato, percorso, SHA-256, righe e colonne. Piano,
specifica, commit di esecuzione e assegnazione agente devono essere aggiunti al record di
conservazione prima della pubblicazione proposta `studio2-fase03-normal-dev-v1`.

Un trip Normal o un errore tecnico arresta il lotto. Non sono ammessi retry automatici,
sostituzioni, padding o sovrascritture. Si conservano il tentativo e il log; una ripresa richiede
revisione esplicita, nuova destinazione e tracciamento di tutti i tentativi.

Accettazione: 40/40 run completi, stream e assegnazioni identici al piano, griglia fino a 65 h,
otto finestre complete per run e hash verificati. Solo dopo audit e conservazione le 320 evidence
possono alimentare prototipi, esempi o FedAvg.

## Contabilità

Il lotto simula `40 × 65 = 2.600 h`. Con la misura della 03.5
`0,2067275 s/h`, la proiezione è `537,49 s`, cioè **8,96 min** di simulazione; sono esclusi avvio,
audit, estrazione, hashing e pubblicazione. È una proiezione, non uno SLA.

## Vincoli verso altre sottofasi

- 03.10 riceve la regola dell'esempio locale sopra e non vede identificatori F-number;
- 03.14 riceve 320 finestre Normal contro 40 per ciascun fault: la ricetta FedAvg deve fissare il
  trattamento dello sbilanciamento prima dell'addestramento; questa specifica non lo decide;
- il lotto non è lanciabile finché `origin/main` non contiene `a572d1c`.
