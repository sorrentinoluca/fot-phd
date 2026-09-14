# Report delle correzioni R1–R4 — allineamenti 03.8 rev.10

Sottofase **03.8**, Studio 2 FoT-TEP, Fase 03. Preparazione iniziata il
2026-09-14 e completata il **2026-09-15**, Europe/Rome.
**Candidato locale corretto, DA VERIFICARE indipendentemente.** Non è un OK.
03.8 e Fase 03 restano aperte. Nessuna esecuzione scientifica autorizzata.
Preparatore: Codex, finestra corrente di preparazione; nessun revisore o
sottoagente coinvolto nella correzione. Il presente report non autocertifica il delta.

## Identità e storia

- Repository comune: `/Users/luker/fot-tep`.
- Worktree esclusivo: `/Users/luker/fot-tep-allineamenti-038-r1-r4`.
- Branch: `codex/studio2-allineamenti-038-r1-r4`.
- Base pubblicata verificata tramite ref locale e `git ls-remote`: `a00605862f627710347bd63c49f79a6d0a00135f`.
- Candidato respinto: `4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8`, tree
  `1eb1d7df58e55a546931711f0a1cf9d800e02e3e`, parent `70c84e3a573951171813add26a46167cbc6c7203`.
- Successore di sola consegna/prompt: `2520e7abc1cd68785f2789448b509dea5e55ee7d`, tree
  `37f246174c9fecb6e623873c5487de04ec65b400`.
- Acquisizione separata del NON OK e **base immediata del nuovo delta**: `1a21fd260ad2df6a3b04ffb6fa5e2d642a3f63b1`.
- Candidato statistico immutato: `6aaa5b3eebfed4ba502c25c0443caabd0051af21`;
  consegna con verbale OK: `51782e8c40069c0a2310afafc36907a61d517ff6`.

Il commit e il tree del nuovo candidato saranno identificati nel record successivo
`CONSEGNA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`, insieme al prompt indipendente.
Report e manifest non includono il commit che li contiene, evitando autoriferimenti.
La review deve confrontare acquisizione → nuovo candidato e verificare le
prescrizioni risultanti delle quattro classi, anche oltre le righe già segnalate.
L'OK sul recepimento A/B della rev.10 resta storico; il NON OK su 4503cb6 resta
integro. Nessuno dei due è sostituito dalla presente preparazione.

Il worktree sorgente consegna `/Users/luker/fot-tep-piano-statistico-chiusura`
era pulito a 2520e7a, branch effettivo
`codex/studio2-piano-statistico-chiusura-rev10`. Per preservarlo si è creata
questa copia dall'esatto commit, senza importare modifiche delle altre finestre.
La copia principale conserva branch `codex/studio2-soglie-normal`, HEAD
`819b12e97fb94d501032655ec2f226139e6c5ca5` e i suoi non tracciati.
Main locale osservato: `4f98a2973d2e1ca7932f19c34e9dd4c0498b8b43`, non mosso.
La catena completa fino a 2520e7a è documentata nell'acquisizione.

## Mandato dell'autore, fonte della sola assegnazione dei ruoli

Fonte: messaggio dell'autore in questa task, «Prosegui lo Studio 2 FoT-TEP,
Fase 03, nella finestra preparatrice degli allineamenti 03.8», ricevuto il
2026-09-14. Estratto trascritto, non un registro D9 né una firma:

> Aggiornamento dell'autore, già approvato:
>
> - 122B producer principale e consumer;
> - 27B producer alternativo, libreria completa di 16 insight, consumer 122B fisso nello swap;
> - Terra soltanto riferimento storico descrittivo interno, separato dalle nuove stime.
>   Questa approvazione viene registrata da un'altra finestra. Puoi riportarla con provenienza dal presente mandato, distinguendola dal registro ancora in acquisizione. Non attendere né importare file non committati della finestra parallela.

La trascrizione è l'evidenza locale del mandato usata per l'allineamento;
non pretende di avere un commit sorgente o un hash del messaggio originale.
La scelta è approvata; il **registro formale resta in acquisizione** nella finestra
proprietaria. Identità complete, revisioni/quantizzazione, configurazioni,
endpoint, tokenizer, capienza e stabilità restano da qualificare. Operatività
dichiarata del 122B non equivale a qualifica. Nessuna firma materiale 03.8,
approvazione dell'ordine label o autorizzazione al pilot deriva da D9.
Nessun file della proposta o del registro D9 è letto o modificato qui.

## Matrice rilievo → fonte → correzione → controllo

| Rilievo | Fonti primarie pinnate nel manifest | Correzione e perimetro | Controllo del preparatore |
| --- | --- | --- | --- |
| R1 | Piano rev.10 §§7.2, 10.2; budget rev.10, blocchi e finestra; coordinamento §2 | §7 e §8.7: nucleo 1.728/5.184, nessuna durata non misurata; calendario ipotetico distinto da fattibilità 1,20×T≤W. §8.8: tetti e scenari storici marcati localmente, nessuna percentuale del ledger non fissato | Aritmetica 1.344+192+192=1.728 e ×3=5.184; ricerca estesa di 1.296, durate, tetti, percentuali e raffronto con le fonti |
| R2 | Piano rev.10 §§1, 7.3–7.4, 9.2 e 16; budget | §6.9/§8.1/D2: 64+8 primari, +6 OOD +11 scorte=89; scorte soltanto sostitutive. §8.3: 64+84=148, ×3=444. §5 G2, §8.5, D3 e confronto SWaT: 64 cluster/8 run correnti. §8.8/§8.12/§13: freeze statistico prima del primo run, distinto dal freeze E5 | Aritmetica e ricerca 6/8, 48/64, 54/72, 132/148; conservati soltanto confronti storici espliciti. Ricerca di generazione anticipata e controllo delle precedenze |
| R3 | Piano rev.10 §§8, 9, 15–16; catalogo D1; pubblicazione/manifest R4 in main; chiusura 03.5 | §6.10/§8.6/§8.9/D11/D12/§11: OOD F6/F4 condizionati; catene F6→F5→F12 e F4→F11→F5; D11 coppie e run 1–3; schema R4 pubblicato, adapter e controlli tecnici futuri distinti. S4 già chiusa, non una dipendenza futura da 03.11 | Lettura di stato pubblicato; controlli tecnici dopo freeze, verifiche proprie dei sostituti, collisione F5→sospensione/autore, nessuna dipendenza circolare. T11 non diventa blocco automatico |
| R4 | Mandato sopra; MAINTENANCE §8; fonti rev.10 per ruoli e contabilità | §§0.1, 2.1, 5 G5, 6.8/6.12, 7, 8.1/8.4/8.7/8.10, D9 e §11: prescrizioni per ruoli; 122B principale/consumer, 27B alternativo 16 insight, consumer fisso. Nessun Qwen-2.4T corrente, surrogato consumer 27B o fallback Terra; storia recuperabile senza cancellare gli esiti | Ricerca estesa di Qwen/Terra/2.4T/D9/opzioni; controllo locale della distinzione decisione/acquisizione/qualifica. Nessuna chiamata, ordine label o firma inferiti |

Raccordo strettamente necessario in **APERTURA**: stato D9 dal mandato,
assenza di surrogato 27B assegnato, Terra solo interno e nota sulla nuova review.
Non sono modificati implementazione harness, proposta/registro D9, sezioni
paper 03.15 o walkthrough. §8.12 cambia solo conteggi/stato storico e precedenza
dei run rispetto ai freeze; nessuna scelta E5, A/B, margine, FAR o U3 è riaperta.
La nota su 03.5 corregge una checklist che la lasciava aperta, senza ricalcolo.

## File e conservazione

File normativi modificati:

- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` — correzioni R1–R4 estese alle prescrizioni correnti;
- `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` — solo raccordo dello stato D9.

Nuovi file nel presente delta, tutti in `studio2/fase03/piano_statistico/`:

- `REPORT_CORREZIONI_ALLINEAMENTI_03_8_REV10.md` — questo report;
- `MANIFEST_CORREZIONI_ALLINEAMENTI_03_8_REV10.json` — impronte degli altri sei file, fonti pinnate e stato;
- `CONTROLLI_CORREZIONI_ALLINEAMENTI_03_8_REV10.json` — controlli e identificativi/subtest;
- `GUARDIANO_PRIMA_CORREZIONI_03_8_REV10.log` e `GUARDIANO_DOPO_CORREZIONI_03_8_REV10.log` — stdout+stderr delle esecuzioni, senza tre spazi finali di unittest per log; impronte grezze e righe 34/41/52 registrate nei controlli per ricostruzione esatta.

L'acquisizione precedente contiene soltanto `VERIFICA_ALLINEAMENTI_03_8_REV10.md`
e `ACQUISIZIONE_NON_OK_ALLINEAMENTI_03_8_REV10.md`. Verbale NON OK originale:
`/Users/luker/fot-tep-verifica-allineamenti-03-8-rev10/studio2/fase03/piano_statistico/VERIFICA_ALLINEAMENTI_03_8_REV10.md`,
**22.063 byte**, SHA-256 `52944646527d0e73d6508ae53669f47f5e8661050ff777c75a448ca535ca9c13`.
La copia acquisita ha identici byte ed è nella cartella del presente report.

**38/38 file preesistenti della cartella statistica** restano byte-identici ai blob
2520e7a, inclusi report/manifest/consegna del candidato respinto e matrice residui.
Sono fotografie storiche: gli stati D9 «non scelta» e review pending di quei file
non prevalgono sul mandato e sul nuovo report. Il loro NON OK riguarda l'allineamento,
non l'OK rev.10. Non si aggiornano impronte di documenti già verificati.
**19/19 file +6/6 input** del manifest rev.10 coincidono per byte, dimensione e
SHA-256 con le voci attese e i blob della consegna 51782e8. Piano, manifest,
verbale OK, atto da firmare, budget e delta harness restano intatti.

## Verifiche eseguite e limiti

- `python3 docs/test_explanation.py`, prima e dopo: **35 test, 14 fallimenti
  storici, 1 skip, 0 errori; exit 1**. Confrontati gli identificativi completi
  dei fallimenti, inclusi parametri dei subtest, e lo skip: coincidenti.
  Ripartizione storica 1/1/9/3 nei quattro metodi UnifiedConversationChecks.
  **Non PASS**: invariato, e non certifica l'allineamento scientifico.
- `git diff --check`: pulito. Link Markdown locali e riferimenti di sezione
  pertinenti verificati; esiti dettagliati nei controlli JSON.
- Manifest nuovo non autoreferenziale; impronte delle fonti lette confrontate
  con i blob agli esatti commit, senza HEAD mobili impliciti.
- Aritmetica documentale: 1.728/5.184, 148/444, 72+6+11=89 e somma delle quattro
  misure 2.244 a R=1. Nessuna stima di prestazione, potenza o durata nuova.
- Rilettura delle prescrizioni correnti §§0.1, 5–11, 13 e raccordi in §14,
  ricerche mirate nell'intero piano; qualificati localmente confronti storici,
  senza sostituzioni numeriche globali. Confronto con il NON OK e le fonti rev.10.

Non rieseguiti test statistici, griglia, bootstrap, review bibliografica,
download di dati o test dei servizi: si preservano gli artefatti verificati.
Nessuna simulazione, inferenza, API sperimentale, harness o pilot. Nessun
walkthrough modificato, quindi nessuna nuova parità MD/HTML da attestare.
Letture: contratto/prompts pertinenti, fonti/prevalenze walkthrough, verbale NON OK,
consegne/manifest, paragrafi statistici pertinenti e piano generale nelle aree
R1–R4 (ordine di decine di migliaia di parole); nessuna nuova lettura dei paper.

## Stato operativo e prossimo passo

| Oggetto | Stato effettivo al nuovo candidato |
| --- | --- |
| Allineamenti R1–R4 | preparati e controllati localmente; **review indipendente pending** |
| A/B e statistica rev.10 | approvate, recepite e già verificate; byte preservati |
| Ruoli D9 | approvati dal mandato; acquisizione formale parallela distinta e non importata |
| Qualifica D9 / 03.10 / T5 | identità e configurazioni, adapter, input reali, capienza, conformità, latenze e calendario restano alle finestre proprietarie |
| 03.5 / 03.9 / schema 03.12 R4 | stati chiusi/pubblicati già documentati; non riaperti |
| Firma materiale 03.8 | non acquisita qui; atto da sottoscrivere preservato |
| Ordine label | non approvato da D9 e non deciso qui |
| Freeze statistico | non efficace, nessun tag creato; precede 03.11 |
| OOD tecnici | futuri, dopo freeze e prima delle chiamate, con sostituti verificati singolarmente |
| Walkthrough e documentazione di chiusura | passo distinto dopo OK indipendente |
| Integrazione/pubblicazione | nessun merge su main, push o tag; nuovo candidato soltanto locale |

Prossimo passo: nuova task di verifica su copia isolata dell'esatto candidato
indicato nella consegna successiva, col relativo prompt. Verificare il nuovo
delta e le prescrizioni risultanti, senza ripetere la vecchia review o cambiare
il verbale NON OK. Dopo l'OK: acquisizione byte-identica del nuovo verbale,
coordinamento della documentazione, firma effettiva dell'autore e integrazione
seriale autorizzata, con verifica di eventuali nuovi raccordi prima del freeze.
Non sostituire mai main con questo snapshot se nel frattempo è avanzato.

Non occorre una nuova scelta dell'autore per completare R1–R4. Restano una firma
e le decisioni organizzative eventuali per incompatibilità 1,20×T≤W o impedimenti
irrisolti; per collisione OOD F5 resta la decisione esplicita prevista in rev.10 §16.
Nessuna di queste è sostituita dal preparatore. 03.8 e Fase 03 rimangono aperte.

Stato Git pianificato della consegna: acquisizione e delta in commit separati;
record successivo con candidato/tree e prompt in terzo commit. Lo stato finale
esatto, incluso il report committato, è riportato in quella consegna dopo il
controllo selettivo. Nessun file della copia principale viene incluso.
