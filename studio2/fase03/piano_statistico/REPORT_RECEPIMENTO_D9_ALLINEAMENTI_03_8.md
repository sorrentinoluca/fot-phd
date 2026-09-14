# Report del recepimento D9 negli allineamenti 03.8

Studio 2 FoT-TEP, Fase 03, sottofase **03.8**. Data: **2026-09-15**, Europe/Rome.
**Acquisizioni completate e recepimento documentale locale preparato; nuova
review indipendente pending.** Non è un OK del nuovo delta, né una chiusura.

## Identità e commit separati

- Worktree: `/Users/luker/fot-tep-allineamenti-038-r1-r4`; repository comune `/Users/luker/fot-tep`.
- Branch: `codex/studio2-allineamenti-038-r1-r4`.
- Base iniziale di consegna: `16f227439357b07b7dc945f67ab5a4368c12b684`, pulita.
- Candidato R1–R4 verificato: `9a56d12d0633a0c9790c48792182f26fc6eb424a`, tree
  `e35e5ca661325657715dce6723e4e8ec09540101`.
- Acquisizione dell'OK R1–R4: `5b784219b08de1249636536ac98e9a546b4d4577`.
- Acquisizione selettiva D9 e **base immediata del recepimento**: `dc4d6560af73579300e33a0a81fc9c3b4316722d`.
- Fonte D9: `aaba893dff8c62f9f9281eec7423eee020235e03`, non un HEAD mobile.
- Origin/main e main remoto verificati: `a00605862f627710347bd63c49f79a6d0a00135f`.

Il nuovo candidato e il suo tree sono identificati nella successiva
`CONSEGNA_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md`, insieme al prompt. Questo report
e il manifest non contengono il proprio commit/hash: il record successivo li
identifica senza autoriferimenti. La review coprirà acquisizioni e nuovo delta,
non ripeterà R1–R4 o le verifiche di sottofasi chiuse.

La copia principale resta sul branch `codex/studio2-soglie-normal`, HEAD
`819b12e97fb94d501032655ec2f226139e6c5ca5`, con non tracciati preesistenti;
nessun checkout o integrazione è stato eseguito lì. Main locale osservato a
`4f98a2973d2e1ca7932f19c34e9dd4c0498b8b43`, non mosso. Worktree preparatore
idoneo e pulito prima delle scritture; copie revisore e D9 sorgente preservate.
Nessun candidato harness R01–R10 importato o modificato.

## Acquisizioni e limiti degli esiti storici

**OK R1–R4:** fonte assoluta
`/Users/luker/fot-tep-verifica-correzioni-allineamenti-03-8-rev10/studio2/fase03/piano_statistico/VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`.
20.816 byte, SHA-256
`9248c42572a20388ddf5af976840e68fdc908e545312a63234167778ce53a256`.
Copia byte-identica nel presente worktree, con
[record di acquisizione](ACQUISIZIONE_OK_CORREZIONI_ALLINEAMENTI_03_8_REV10.md).
Revisore documentato: gpt-6-astra, openai, high, sessione
`01a0a1d9-8ccd-7893-b504-4fde93380ea0`. Indipendente dal preparatore, ma stessa
sessione del precedente NON OK; non è una nuova task senza contesto o un secondo
modello. Il limite resta esplicito. L'OK riguarda 9a56d12, non la consegna
16f2274 o il recepimento D9 successivo. Nessuna firma, freeze o autorizzazione.

**D9:** tre file acquisiti negli stessi percorsi `studio2/fase03/`, dal commit
sorgente esatto e dalla copia viva risultata identica in
`/Users/luker/fot-tep-proposta-d9`. Nessun artefatto era già presente nel target.

| File | Byte | SHA-256 |
| --- | ---: | --- |
| DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md | 9083 | fcb113636de80cc87709905324436555e0ba103bd46de3ac079ce0ef7f60f1b8 |
| CONSEGNA_RECEPIMENTO_D9_2026-09-14.md | 13282 | 3ea739065f1011ed2fd17bface11231f8857dc3f5256d26eff7abcc1d1ef2c77 |
| IMPRONTE_DECISIONE_D9_2026-09-14.json | 11169 | 3b95d17ab3b467bebe5d0bda5fa84d8ab63f3ee13f87397e02caf396654af77b |

Byte confrontati con `git show aaba893:<path>`; due voci artifacts del JSON
confrontate con le impronte dichiarate. Il JSON non si auto-impronta; identità
propria nel [record di acquisizione D9](ACQUISIZIONE_D9_ALLINEAMENTI_03_8.md).
La proposta e le 17 fonti storiche del JSON non sono importate.

**Limite dei riferimenti ereditati:** il link alla proposta storica nel record
D9 non risolve nel checkout 03.8, perché quel file non appartiene alle tre
acquisizioni. È conservato senza alterare i byte; destinazione verificata nel
blob `95ff8571af02bab79094ed1a6be3f6a7b410c711:studio2/fase03/PROPOSTA_D9_RUOLI_MODELLI_2026-09-14.md`
(36.141 byte, SHA-256 `a47f42dda7ee9702c292e34ada6b116ac3c85e42ec3a50e68af97c159f0d0f9d`).
Il record di acquisizione fornisce il comando di recupero e la sede originale.
Il rinvio assoluto alla vecchia proposta harness è anch'esso storico e non
attesta lo stato dell'harness in correzione. Nessun nuovo link introdotto dal
recepimento punta a un file assente.

## Matrice file → modifica → motivazione → controllo

Percorsi relativi alla radice del worktree, salvo i cinque nuovi documenti nella
cartella `studio2/fase03/piano_statistico/` indicati col solo nome.

| File | Modifica | Motivazione | Controllo |
| --- | --- | --- | --- |
| docs/paper/FoT_TEP_Review_Piano_Sperimentale.md | intestazione, §0.1, swap §8.4, D9 e checklist: record acquisito e recepimento locale; fonte aaba893 e SHA; label 1a distinta | superare l'attesa del registro senza attribuire D9 alla rev.10 o qualificare i servizi | diff circoscritto e ricerca D9/ruoli/acquisizione; stesso P=C=122B/P_alt=27B, nessuna variazione del disegno |
| studio2/fase03/APERTURA_SOTTOFASI_FASE03.md | OK R1–R4 acquisito, nuova review D9 pending; link al record, matrice e consegna successive | aggiornare lo stato corrente e separare i cinque stadi | coerenza col piano e con la fonte D9, riferimenti risolti |
| MATRICE_RESIDUI_03_8_DOPO_D9.md | matrice successiva: scelta/acquisizione/recepimento documentale/eseguibile/qualifica; residui distinti | la matrice precedente è già improntata e resta storica | confronto con record e consegna D9; nessuna riapprovazione dei ruoli o dipendenza circolare |
| CONSEGNA_TECNICA_03_8_D9_PER_03_10.md | aggiornamento documentale della consegna 03.8, per la sola D9 | preservare la consegna tecnica improntata; non toccare file harness | ruoli, 16 insight, consumer fisso, contatore R4, contabilità e confini delle autorizzazioni; nessuna configurazione nuova |
| REPORT_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md | questo rapporto distinto | non riscrivere rapporti già verificati | catena, fonti, perimetro, stati e residui verificabili |
| CONTROLLI_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json | identità, preservazione, link e guardiano prima/dopo | evidenza documentale del preparatore | identificativi e subtest confrontati, non autocertificazione |
| MANIFEST_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json | sei file del delta e fonti pinnate, senza se stesso | fissare l'oggetto della nuova review | byte/SHA-256 e validità JSON |

I rapporti precedenti, la matrice rev.10 e la consegna tecnica rev.10 restano
byte-identici; i nuovi record ne aggiornano lo stato con link espliciti dal piano
corrente e da APERTURA. Nessuna fonte verificata viene riscritta per cancellare
un pending storico. Il NON OK su 4503cb6 e l'OK su 9a56d12 restano entrambi intatti.

## Cinque stati e residui

1. **Ruoli approvati:** P=C=122B; P_alt=27B, libreria completa di 16 insight;
   consumer 122B invariato nello swap, medesimi casi del disegno. Terra soltanto
   storico descrittivo interno separato dalle nuove stime, senza nuove chiamate.
2. **Record acquisito localmente:** tre blob esatti di aaba893, con provenienza.
3. **Recepimento documentale locale preparato:** piano, APERTURA, matrice,
   consegna tecnica; nuova review indipendente da svolgere.
4. **Recepimento eseguibile pendente:** compete al cantiere harness R01–R10;
   nessun suo avanzamento è attestato o importato qui.
5. **Dati/qualifica/fattibilità pendenti:** identità esatte, pesi/revisioni,
   quantizzazione, endpoint/serving, tokenizer/template, configurazione e limiti
   effettivi; misure di capienza, conformità, stabilità, latenza e T5.

Restano separate **ordine label 1a non approvato**, firma materiale 03.8,
qualificazione dei servizi e autorizzazioni di esecuzione. Nessun 27B consumer
fallback o accesso Terra è approvato. Collocazione della conformità alternativa,
`a`, riusi, X/Q, calendario e quartetto dello swap non si deducono dalla D9:
vale il rintraccio nelle fonti e, solo per scelte realmente mancanti/necessarie,
il passo dell'autore previsto nella consegna D9. Nessuna scelta fatta qui.

La contabilità vigente resta intatta, aggregando richieste distinte per P=C=122B
senza duplicarle. Non si stanziano budget, retry o quote aggiuntive e non si
azzera il ledger. Nessun calendario o metadato nuovo viene inventato.

## Controlli, preservazione e limiti

- Acquisizioni verificate per byte, dimensione e SHA-256 sulle fonti esatte.
- Tutti i file preesistenti della cartella statistica al commit 16f2274
  preservati; 19 files +6 inputs del manifest rev.10 verificati con le impronte
  e i blob della consegna `51782e8c40069c0a2310afafc36907a61d517ff6`.
- Guardiano `python3 docs/test_explanation.py`: prima/dopo **35 test,
  14 fallimenti storici, 1 skip, 0 errori, exit 1**, stessi identificativi e
  sottocasi; **non PASS**. Non prova la correttezza del recepimento D9.
- Link introdotti risolti; unico rinvio relativo ereditato non locale alla
  proposta storica documentato e recuperabile dal pin Git, senza modificarne
  il record. Dettagli e conteggi nei controlli JSON.
- `git diff --check` sul nuovo delta pulito; JSON validi e manifest senza
  autoriferimenti. Nessuna coppia MD/HTML modificata.
- Nessun test scientifico, simulazione, inferenza, pilot o API; nessuna nuova
  review delle sottofasi chiuse. A/B, FAR, U3, 03.5, 03.9 e 03.12 non riaperti.

Letti il mandato allegato, MAINTENANCE corrente, verbale OK e i tre artefatti D9;
riusate le regole fase/verifica/documentazione/commit già lette, previa identità
dei byte. Letti i paragrafi correnti interessati, matrice/consegna pregresse e
manifest di preservazione. Costo: letture documentali nell'ordine di alcune
migliaia di parole; nessuna nuova ricerca o lettura dei paper. Preparatore:
Codex nella stessa task degli allineamenti; nessun revisore/subagente coinvolto.

## Consegna e prossimo passo

Nessun push, merge su main, tag, firma o freeze. Candidato solo locale, non
integrato/pubblicato; 03.8 e Fase 03 aperte. Dopo il commit selettivo del delta,
una consegna documentale successiva riporterà candidato/tree e prompt, impronte
e stato Git finale, incluso questo report committato. Le acquisizioni restano
nei due commit separati sopra identificati.

Prossimo passo: review indipendente delle acquisizioni e del solo nuovo delta
D9. L'OK storico R1–R4 non si ripete e non si trasferisce automaticamente.
Poi acquisizione del nuovo verbale e raccordi documentali autorizzati in passi
separati, con firma effettiva, integrazione e freeze secondo i propri requisiti.
Harness, paper 03.15 e walkthrough restano alle rispettive finestre. Non far
diventare harness o 03.11 prerequisiti circolari del freeze statistico:
**freeze statistico → 03.11 e controlli OOD → chiamate dopo gli altri GO**.
Non serve alcuna nuova approvazione dell'autore per completare il presente delta.
