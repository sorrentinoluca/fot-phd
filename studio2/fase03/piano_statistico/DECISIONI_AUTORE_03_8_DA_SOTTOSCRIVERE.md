# Piano statistico 03.8 — documento da sottoscrivere

Documento preparato il **2026-09-14**. Autore delle decisioni: **Luca**.
Stato: **predisposto; firma materiale non acquisita**. Non è una copia modificata
della bozza storica e non costituisce attestazione di congelamento.

## 1. Approvazioni storiche già registrate

Fonte: [bozza storica](DECISIONI_AUTORE_03_8_bozza.md), approvazioni in conversazione
registrate il 14 settembre 2026; SHA-256
`66e04dd2d8dd00fcf0edf6076a9e3f60bb6fd1fdf8c1e86028a9f80c8754fafb`,
43.136 byte. Conservata nel commit `75bd14898e43f03f849c5d248d6c2481da55e245`.
Il contenuto della bozza, inclusi Allegati A e B, resta il riferimento completo.
Questa tabella ne riassume gli esiti senza riaprire le approvazioni.

| Decisione | Esito storico valido |
| --- | --- |
| D2 | 8 run per fault: 64 fault + 8 Normal primari, 72 complessivi |
| H1/H2 | Hoeffding su medie di cluster indipendenti in [−1,1]; livello finito, nessuna garanzia di potenza o indipendenza effettiva |
| H3 | Tango score, m=0,125 come perdita media netta massima dichiarata; α=0,05, sensibilità separata 0,025; A2-bis non adottato |
| Gerarchia | H1→H2→H3 con arresto al primo non-rifiuto; controllo complessivo approssimato per Tango |
| Reporting | guadagnati/persi/saldo per agente/fault; saldo≤−2 su 8 descrittivo |
| OOD | F6/F4 condizionati; F6→F5→F12 e F4→F11→F5; requisiti propri e distinzione dei due fault |
| D11 | {F1,F2}, {F14,F15}; run sigillati 1–3 |
| R, audit e canary | divergenza su coppia parsata o validità; audit 10%; 10 canary/giorno; sospensioni confermate |
| Pilot | T3–T6, T9, T11; conformità→eventuale remediation→sonda→gate |
| Remediation e riserva | una sola sul prompt, futura autorizzazione sul diff; riserva 15 unica; massimi 152/160; hard stop 200 |
| Bootstrap e scorte | seed 20260913, 10.000 repliche, namespace storico; 11 scorte tecniche pre-chiamata |
| Tetto storico | 3.700 confermato; vigente salvo successiva approvazione esplicita di A |

## 2. Nuove decisioni, separate dalle precedenti

Testo integrale delle proposte: [addendum A e B](ADDENDUM_DECISIONI_RESIDUE_03_8.md).

| Decisione nuova | Approvazione | Data effettiva e riferimento |
| --- | --- | --- |
| A: risorse e ramo R=3 | **pending** | da acquisire |
| B: ordine OOD e congelamento | **pending** | da acquisire |

La richiesta generale di chiusura e la dichiarazione del referente sui token non
sono approvazioni delle due nuove proposte. Prima della sottoscrizione finale,
registrare qui solo gli esiti realmente espressi; nessuna retrodatazione.

## 3. Condizioni operative e identificazione del candidato

Base scientifica: rev. 9 verificata; commit di stato
`0f1a9bae8b522f614720fa5efe7bd9d2577609ae`; manifest SHA-256
`2b6ad396307be634428d9355d4aa65144b4956d675ccb9e4b47536e4bdaf8d76`.
Verbale rev. 9 preservato al commit `29249a9305c44a44b96e6f49f94e978956ed0ac2`;
SHA-256 `289a74433d70e2bf911bdea893711ff7a294c75cf74d5e6fa0addbf3ede72a58`.

Il candidato definitivo successivo alla 9 non è ancora prodotto: dipende da A/B.
Prima di firmare, completare l'identificazione senza attribuire la firma a un file
futuro: revisione ______; commit candidato ______; manifest SHA-256 ______;
verbale indipendente e impronta ______. Il manifest candidato impronta il documento
non firmato; l'atto firmato acquisito viene conservato separatamente e improntato
nel successivo record di acquisizione, evitando auto-riferimenti.

Restano condizioni da provare: identità/configurazione del modello e decisione D9;
fattibilità misurata e calendario; implementazione 03.10 e prerequisiti del pilot;
generabilità/trip/ammissibilità OOD secondo l'ordine effettivamente approvato;
integrazione bibliografica, allineamenti, nuova verifica indipendente, integrazione
e pubblicazione seriali. La firma non trasforma questi pending in risultati.

La condizione bibliografica F6 è soddisfatta entro PHM. H={F3,F9,F15}, D1,
registro congelato e addendum F9–SPE sono preservati. Firma e verifica del delta
non autorizzano automaticamente chiamate sperimentali, nuove simulazioni o scelta D9.

## 4. Sottoscrizione materiale

Dichiaro di sottoscrivere le decisioni identificate sopra, con gli esiti e le
condizioni esplicite riportate, senza attestare come già eseguite le verifiche pendenti.

Autore: Luca

Luogo e data effettiva: ____________________

Firma dell'autore: ________________________

**Acquisizione effettiva: pending.** Percorso della copia sottoscritta, data di
ricezione e SHA-256 saranno registrati solo quando la firma sarà disponibile.
