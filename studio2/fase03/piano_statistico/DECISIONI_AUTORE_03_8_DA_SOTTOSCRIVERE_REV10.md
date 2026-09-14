# Piano statistico 03.8, revisione 10 — documento da sottoscrivere

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
| Tetto storico | 3.700 era confermato; sostituito dalla nuova decisione A del 14 settembre 2026 |

## 2. Nuove decisioni, separate dalle precedenti

**A e B approvate senza modifiche da Luca il 14 settembre 2026.**
Testo esatto: [addendum A/B](ADDENDUM_DECISIONI_RESIDUE_03_8.md) al commit
`526561feabeb6b4083170b1817b8abdac1a2a4c7`, SHA-256
`6035967ceb390de69e63cac9f828b17386ab8a76bb1999db524597770fc782f8`.
Fonte della risposta: [record di approvazione](APPROVAZIONE_ADDENDUM_03_8.md),
con messaggio dell'autore trascritto e data effettiva, distinto dalla bozza storica.

| Decisione nuova | Esito effettivo | Limite |
| --- | --- | --- |
| A — Risorse e ramo R=3 | **APPROVATA senza modifiche** | conteggio completo e fattibilità temporale misurata +20%; invariati trigger R, hard stop 200 e riserva; tempi e D9 non ancora verificati |
| B — Ordine OOD e congelamento | **APPROVATA senza modifiche** | candidati/criteri/catene prima dei run; controlli 03.11 prima delle chiamate, sostituti verificati e distinti, sospensione dei casi non risolti |

## 3. Candidato e condizioni ancora da provare

Revisione oggetto del recepimento: **10**. Piano: `PIANO_STATISTICO.md`, SHA-256
`675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`. Manifest candidato: `PIANO_STATISTICO_FREEZE.json`, revisione 10,
ancora senza freeze. Prima della firma, verificare questo hash e identificare
commit e manifest esatti nel record di acquisizione sottostante; nessuna firma
su un testo futuro indeterminato.

La firma non attesta controlli non eseguiti. Restano: nuova verifica indipendente,
allineamenti normativi e integrazione bibliografica seriali, documentazione e
pubblicazione del candidato; identità/configurazione del modello, D9, fattibilità
misurata e implementazione verificata 03.10 prima dell'esecuzione pertinente;
generabilità/trip/ammissibilità OOD in 03.11 dopo freeze e prima delle chiamate.
I due OOD rimangono distinti. La condizione bibliografica F6 entro PHM non è
prova tecnica. H, D1, registro congelato e addendum F9–SPE restano preservati.
La firma non autorizza automaticamente chiamate sperimentali o una nuova scelta D9.

Identificazione da completare al momento della sottoscrizione:
commit candidato ______; manifest SHA-256 ______; verbale indipendente e hash ______.
La copia sottoscritta verrà acquisita separatamente: il manifest candidato impronta
questo documento non firmato; il successivo record di acquisizione impronterà
l'atto effettivo, evitando auto-riferimenti e qualunque firma apposta dal preparatore.

## 4. Sottoscrizione materiale

Dichiaro di sottoscrivere le decisioni identificate sopra, con gli esiti e le
condizioni esplicite riportate, senza attestare come già eseguite le verifiche pendenti.

Autore: Luca

Luogo e data effettiva: ____________________

Firma dell'autore: ________________________

**Acquisizione effettiva: pending.** Percorso della copia sottoscritta, data di
ricezione e SHA-256 saranno registrati solo quando la firma sarà disponibile.
