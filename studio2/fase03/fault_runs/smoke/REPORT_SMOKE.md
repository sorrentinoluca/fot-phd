# Smoke unico F1 — esecuzione e verifica

**PASS**, 2026-09-13. Eseguito **un solo run**, nessun retry e nessun altro fault;
**zero run del batch**. Piano e script erano già nel commit `55d442b`, test nel commit
`88eb34e`, specifica nel commit `c02111d`. Gli artefatti del run riportano l'HEAD di
esecuzione completo `88eb34e` e gli hash effettivi.

Piano: `plans/smoke.csv`; destinazione `smoke/f1_short_001/`; ID `smoke-F1-001`, stream
`30040`, F1. Burn-in 20 h, controllo [20,25), onset nominale 25 h, orizzonte post-fault
**ridotto a 0.1 h**, termine 25.1 h. Nessuna finestra post-fault completa o materiale
utilizzabile per insight/prototipi. Grezzo: **1507 × 54** (tempo, 41 XMEAS, 12 XMV).

## Riscontro dell'attivazione

Il log MEX registra il solo bit IDV(1), con prima osservazione attiva a
**25.000410376861183 h**: circa **1.47736 s** dopo il ritardo nominale di 25 h, meno del
periodo base dei controllori (1.8 s). La prima riga campionata attiva è a 25.0166666667 h.
Il campione esattamente a 25 h conserva il valore nominale. Il ritardo continuo e l'ordine
output/derivate non garantiscono una transizione osservata esattamente al numero reale 25.
Il parser, già committato prima dello smoke, ammette l'osservazione entro un intervallo di
salvataggio e il valore precedente al solo campione di frontiera. **Nessun campione è stato
spostato, cancellato o corretto; onset e finestre del piano restano invariati.** La stessa
risoluzione va dichiarata quando si interpreterà W1 nel batch: l'attivazione nominale non
va presentata come un istante osservato esatto.

Nelle **300 righe del controllo [20,25)** il bit è nullo e la composizione interna
A/B/C del flusso 4 è 48.5/0.5/51.0 %. Nei sei campioni successivi al tempo 25 h
(endpoint incluso), IDV(1)=1 e A/B/C=45.5/0.5/54.0 %: A −3 punti percentuali, C +3,
B invariato, come nel sorgente. È una verifica del forcing F1 e della registrazione,
non un risultato di separabilità o una prova statistica che tutto il processo sia stazionario.
La tolleranza numerica `1e-10` del controllo della composizione verifica queste costanti
implementate; non è una soglia scientifica di rilevazione.

Nessun trip o errore tecnico. Contatore finale Philox **152981172**. Il validatore
ricostruisce griglia, log, manifest e SHA-256: un manifest completo, `accepted=true`.
Il controllo si riesegue senza simulare con:

```bash
python3 /Users/luker/fot-tep/studio2/fase03/fault_runs/verify_smoke.py
```

Esito machine-readable: [SMOKE_CHECK.json](SMOKE_CHECK.json). Dati, diagnostiche, log
simulatore, manifest JSON, CSV aggregato ed eventi sono tutti conservati nel commit smoke.
Il file `attempt.json` conserva i metadati originari consegnati dal launcher al finalizzatore.

## Tempi misurati e proiezione

| Misura | Secondi |
| --- | ---: |
| Chiamata di simulazione MATLAB | 9.313331 |
| Run, con scrittura e finalizzazione fino al manifest | 9.599 |
| Processo MATLAB completo, avvio/preparazione/uscita inclusi | 33.043492 |
| Differenza processo meno run | 23.444492 |
| Proiezione sola simulazione: 40 × 9.313331 × 65/25.1 | 964.727501 |
| Proiezione run con scrittura: 40 × 9.599 × 65/25.1 | 994.318725 |
| Proiezione con un overhead di processo | 1017.763217 |

Stima operativa: **circa 16.6 minuti**, oppure **17.0 minuti includendo un avvio**.
È una proiezione lineare da un solo F1 breve, non una misura dei 40 run né un intervallo
predittivo. Compilazione/inizializzazione Simulink, fault diversi, logging, I/O e trip
non scalano necessariamente col tempo simulato. Nessun'altra simulazione è stata eseguita
per affinare la stima. Il costo di compilazione del MEX è precedente e non incluso.
Tempi esterni e comando esatto: [LAUNCH_TIMING.json](LAUNCH_TIMING.json).

## Ambiente e impronte

MATLAB R2025b nativo ARM, `maca64`, MEX `mexmaca64`, compilatore Xcode/Clang.
Il primo tentativo di sola compilazione sotto Rosetta è fallito prima di ogni simulazione;
il comando ARM ha compilato correttamente. Non è un run aggiuntivo.

- MEX strumentato: `834e2361915249402a1ec9074a4be04f22a6404deb841e5134bf34347dfde544`.
- Sorgente strumentato: `74bf641bcd16ce42093b3c78cf03887376d19561041f8746ccf01339042fb4c9`.
- Sorgente base invariato: `230086e7712e753bf48f3e9108cd0ce2f68aba97d9590ebb3c7593a47f8b6d25`.
- MEX della Fase 02 invariato: `6ae7e7be5394773f1854f1c53eddbd778ad7557b61fb05a93b3edb0552b1d11e`.

Il manifest per-run contiene modello base, override effettivi, script, piano, specifica e
ulteriori dipendenze per hash. Non si confonde il modello su disco con gli override in memoria.
Simulink segnala la vecchia versione di TElib e il buffer del ritardo, come nel percorso
qualificato; il log completo resta conservato. Nessun salvataggio del modello originale.

## Limiti della verifica

La verifica fisica reale riguarda **solo F1 breve**; i test dei trip usano log/prefissi
sintetici. Non è stata verificata su una simulazione aggiuntiva la concordanza numerica
base/strumentazione: il controllo statico dimostra che, rimosse le sole aggiunte diagnostiche,
si riottiene byte per byte il sorgente qualificato. Rimane opportuna la verifica indipendente
dell'harness prima dell'uso dei risultati batch. F14/F15 non sono stati osservati qui.
