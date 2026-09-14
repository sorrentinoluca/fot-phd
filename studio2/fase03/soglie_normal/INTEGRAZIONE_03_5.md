# Chiusura e pubblicazione della sotto-fase 03.5

Stato al 2026-09-14: **03.5 chiusa, integrata e pubblicata**. La Fase 03 resta aperta.
Mandato dell'autore in questa sessione: «Nel frattempo chiudiamo 3.5 e 3.9».

- Candidato: `b64ff387b8abad063a08885ac77e8a8f9621c3a8`.
- Merge pubblicato in `origin/main`: `98d958d870a10ada0d095893af9edb05a68ebc67`.
- Tag annotato pubblicato: `studio2-fase03-soglie-normal-frozen-001`, sul merge sopra.
- Oggetto tag: `199c71b5f49537f2d77e5e4473446ab4a5509ecd`.
- Presenza remota e destinazione del tag controllate con `git ls-remote`.

Il tag identifica la consegna finale verificata, compreso C4. Non retrodata il freeze
scientifico della soglia, già registrato in `950714389f92e559eac922a09404742a71c74346`
prima dell'analisi FAR. `THRESHOLD_FREEZE.json`, risultati, decisione FAR e verbali sono
byte-identici al candidato. Non sono state eseguite simulazioni o inferenze sperimentali.

L'integrazione conserva la documentazione già presente in main. La sezione della provenienza
03.5 passa da §9/§9.1 a §10/§10.1; nel report cambiano soltanto i due relativi rinvii.
Il walkthrough passa da §4.4 a §4.5, perché §4.4 è già occupata dal perimetro Q8.
Gli hash dei verbali descrivono gli snapshot verificati: l'originale del report con i vecchi
rinvii è recuperabile dal candidato, ora antenato di main.

Controlli di integrazione: **8/8 test PASS**; guardiano documentale **35 test, 14 fallimenti
preesistenti e 1 skip**, con gli stessi identificativi prima/dopo. Confrontati tutti i file
del pacchetto con il candidato; unica differenza del merge nel pacchetto: i due rinvii del
report. Gli spazi finali storici nei log, nella specifica e nella decisione FAR sono
conservati per non alterare le evidenze; nessun nuovo errore di whitespace nel delta di
integrazione. Questi controlli non sono una nuova verifica scientifica indipendente.

La [release normal-v1](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-normal-v1)
resta invariata. Riutilizzata la verifica per riscaricamento già acquisita: 515/515 file,
zero mismatch, archivio SHA-256
`bbcfd0c43a5fbda624deba62fea746150dda4a6d649e6372b8e118270277ac1d`.
L'asset remoto è ancora presente con 943.793.152 byte. In questa integrazione non è stato
eseguito un nuovo download del lotto Normal storico.

Worktree sorgente e file non tracciati del checkout principale preservati. Nessuna
operazione sulle decisioni statistiche 03.8. Il branch di integrazione è
`codex/studio2-chiusura-035-039`.
