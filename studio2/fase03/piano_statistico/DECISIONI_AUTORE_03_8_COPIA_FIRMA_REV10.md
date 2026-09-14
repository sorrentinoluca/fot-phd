# Piano statistico 03.8, revisione 10 — copia materiale proposta

Questa copia separata deriva dall'atto originario
`DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md`, 4.974 byte, SHA-256
`4a0a4e1fc2797ee7a81439110e164d43159c745007136c9dda7bed7759471cc8`.
Autore delle decisioni: **Luca**. Stato: **proposta corretta non firmata; verifica
indipendente del presente delta necessaria prima della sottoscrizione**. L'atto
originario e la bozza storica restano immutati. Questa copia non costituisce
firma, pubblicazione o congelamento.

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
| A — Risorse e ramo R=3 | **APPROVATA senza modifiche** | conteggio completo e fattibilità temporale misurata +20%; invariati trigger R, hard stop 200 e riserva; tempi e fattibilità non ancora verificati; ruoli D9 approvati successivamente e separati dalla qualifica tecnica |
| B — Ordine OOD e congelamento | **APPROVATA senza modifiche** | candidati/criteri/catene prima dei run; controlli 03.11 prima delle chiamate, sostituti verificati e distinti, sospensione dei casi non risolti |

## 3. Oggetto esatto e catena di verifica

La sottoscrizione vincola le decisioni delle sezioni 1–2 ai seguenti byte della
revisione 10, senza riscriverne lo stato storico:

| Oggetto | Identità materiale |
| --- | --- |
| Candidato statistico rev.10 | commit `6aaa5b3eebfed4ba502c25c0443caabd0051af21`, tree `24847ce0cc4ff7b6defea4d65f3f41cb9ccd1c1a` |
| Piano | `PIANO_STATISTICO.md`, 81.490 byte, SHA-256 `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` |
| Manifest storico del candidato | `PIANO_STATISTICO_FREEZE.json`, 25.894 byte, SHA-256 `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`; `freeze_effective=false`, `freeze_tag=null` |
| Verifica indipendente rev.10 | `VERIFICA_PIANO_STATISTICO_REV10.md`, 12.478 byte, SHA-256 `d269e26d8cb4e23370577e1e193d90d9357d66f7c739e9d0669970edf71b0066`; acquisita nel commit `51782e8c40069c0a2310afafc36907a61d517ff6` |

Il manifest conserva correttamente la fotografia del candidato, inclusa la
review allora `pending`: i verbali e i record successivi documentano gli esiti
senza alterarlo. La catena successiva pertinente è:

- allineamenti corretti nel candidato `9a56d12d0633a0c9790c48792182f26fc6eb424a`;
  verbale OK `VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`, 20.816 byte,
  SHA-256 `9248c42572a20388ddf5af976840e68fdc908e545312a63234167778ce53a256`,
  acquisito nel commit `5b784219b08de1249636536ac98e9a546b4d4577`;
- record D9 acquisito nel commit `dc4d6560af73579300e33a0a81fc9c3b4316722d`
  e recepito documentalmente nel candidato
  `8a20c125bd294191c67ebdbf571832b1e32ac0f1`;
- verbale OK D9 `VERIFICA_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md`, 21.644 byte,
  SHA-256 `bb8555792c5dad78fc3ffeaf5f797e3da427ef79ec1d3ebe7c840810f77c53e3`,
  acquisito nel commit `8a3f7ba706570201c5b622c4e0fc79529b1c8cfd`.

D9 ha già assegnato 122B come producer principale e consumer e 27B come producer
alternativo per una libreria completa di 16 insight; Terra resta soltanto storico
descrittivo interno. Questa sottoscrizione non riapprova D9 e non approva
l'ordine label 1a. Non attesta identità/configurazioni dei servizi, qualifiche,
fattibilità T5, implementazione harness o controlli OOD non ancora eseguiti e non
autorizza chiamate, inferenze, simulazioni o pilot.

Dopo la firma restano distinti: acquisizione e impronta dell'artefatto firmato;
raccordo documentale applicabile; integrazione/pubblicazione nel main remoto;
manifest finale non autoreferenziale e tag di freeze. I controlli tecnici OOD
restano in 03.11 dopo il freeze e prima delle chiamate sui test; l'harness e gli
altri GO operativi restano necessari prima dei rispettivi stadi, senza creare una
dipendenza circolare dal congelamento statistico.

## 4. Sottoscrizione materiale

Dichiaro di sottoscrivere le decisioni identificate sopra, con gli esiti e le
condizioni esplicite riportate, senza attestare come già eseguite le verifiche pendenti.

Autore: Luca

Luogo e data effettiva: ____________________

Firma dell'autore: ________________________

**Acquisizione effettiva: pending.** La copia sottoscritta sarà restituita come
`DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.md`; data di ricezione, dimensione e
SHA-256 saranno registrati soltanto quando l'artefatto firmato sarà disponibile.
