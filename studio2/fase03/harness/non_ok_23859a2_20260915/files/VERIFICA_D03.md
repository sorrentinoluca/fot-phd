NON OK — candidato offline 23859a29225ccd9cd6f47e4a0b6e36258831dbab. D03 originario chiuso nelle prove riprodotte; distinto D04 aperto sulle quote degli stadi ancora aperti. Nessun freeze o GO.

# Verbale autonomo D03 — 15 settembre 2026

## Identità e indipendenza

| Oggetto | Identità verificata |
| --- | --- |
| Candidato tecnico | `23859a29225ccd9cd6f47e4a0b6e36258831dbab` |
| Tree tecnico | `fe66025f4925e27676b0be16428475e3fcaee060` |
| Parent contratto/test-first | `567881abf06572812c00ccc0ed817d169b68fee6` |
| Acquisizione separata | `efa9f6f94194985104047d831c0b087dc460532d` |
| Base documentale | `e9b60c5db77edfd3c06a29857e6ba5f61ebe139a` |
| Successore documentale escluso dall'esecuzione | `97868f9d6ef281c2dd4ab1c6ffb67e2477ee5715` |
| Tree documentale | `30af2de32f357eee0e983f82cf529cbe58cdd617` |
| Respinto precedente, usato solo per prove rosse | `a219bd469bbd280f56b7fa9cb56cda115b0975ed`, tree `3fb8e50c189b85b447503b8a1ac99c1741904a5b` |
| Main GitHub effettivo prima/dopo | `a00605862f627710347bd63c49f79a6d0a00135f` |

✅ Prima delle scritture verificati branch, HEAD/tree/parent, status, worktree e remoto effettivo `https://github.com/sorrentinoluca/fot-phd.git` con ls-remote. Source `/Users/luker/fot-tep-harness-0310-d03`, branch `codex/studio2-harness-0310-d03`, pulito sul successore. Il successore aggiunge esattamente i quattro documenti di consegna, acquisiti via git show; non sostituisce il tecnico.

Review in `/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate`, clone detached dell'esatto tecnico, con working tree/indice/riferimenti propri e oggetti Git locali condivisi in lettura. Tutti gli output nel fratello `/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence`. Nessuna scrittura al candidato, ai source, alla principale o alle prove precedenti. Fixture, copie SQL e subprocess sono sacrificabili e separati dagli input scientifici.

| Esecutore | Runtime osservato |
| --- | --- |
| Revisore, questa finestra | sessione `01a0a1ec-35a4-7870-9c39-9bf922d36c85`, `gpt-6-astra`, effort `high` |
| Preparatrice | sessione distinta `01a0a204-abda-7a00-8466-f52f5bc84812`, `gpt-6-astra`, effort `xhigh` |
| Python | `/opt/anaconda3/bin/python3`, 3.13.9, arm64, SQLite 3.51.0 |

Fonte: session_meta/turn_context dei rollout locali riletti in [runtime.json](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/runtime.json). Effort è il valore registrato, non la misura del calcolo consumato. **Finestra distinta, modello coincidente**: diversità di modello assente e non rivendicata. Nessuna delega. Non è dimostrato un nesso causale tra famiglia del modello e difetti; cambiare modello non garantisce di eliminarli. Contratto e prove sono valutati sul codice.

Letti MAINTENANCE principale, differenze esatte della copia candidata, Prompt_LLM/Verifica_LLM pertinenti, mandato/report D03, contratto iniziale e corrente, verbale D02 acquisito integralmente, delta runtime/test, inventario N/F, generatore e fonti delle prove. Nessun AGENTS.md trovato nei perimetri o negli antenati. I contratti già letti dei precedenti cicli restano applicati; le fonti sono fissate a commit esatto. Letture pertinenti dell'ordine di alcune centinaia di kB, oltre ai confronti meccanici. Nessun nuovo audit scientifico o bibliografico.

## Integrità, provenienza e cronologia

✅ [integrity.json](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/integrity.json): **7.098 confronti, zero mismatch**. I confronti ripetuti non sono metodi di test aggiuntivi.

| Oggetto | Verifica autonoma |
| --- | --- |
| Manifest tecnico | 83 membri, 20.826 byte, SHA-256 `483c7db5ad4a763a8f41d084538c7a2cce6b2a7d799a5ba11d57da852cee3828`; tutti i membri confrontati anche con blob HEAD |
| Acquisizione D02 | 1.869 file effettivi: 116 copie byte-identiche, 1.753 esterni; hash e dimensioni riletti |
| Riproduzioni D03 | 1.909 file: 61 copie byte-identiche, 1.848 esterni; verificati anche tutti i membri del SHA256SUMS corrente |
| Evidence originaria | Riletti 2.754 file, inclusi 1.283 membri della reference evidence-v2 già scaricata e verificata nel primo ciclo |
| R4/baseline/input/piano | 18 membri R4, 17 pin baseline, quattro input e tre fonti piano ricontrollati su blob esatti; tre tag ricontrollati sul remoto effettivo |
| Moduli recuperati | Nove moduli confrontati con sorgente `1ac06ebdc92f73d3b630ccca9bf75f413bea170b` e candidato precedente; sette adattamenti dichiarati, solo logging_v1.py e sampling.py byte-identici alla sorgente |
| Perimetro | 176 file protetti byte-identici alla base documentale; tre metriche qualificate anche identiche alla base pubblicata |
| Sintassi/import | 93 sorgenti live compilati in memoria, senza cache; nessun import diretto phase_b; alberi forensi esclusi |

Verbale D02 acquisito SHA-256 `b88f046592ac9d1b0f784c1d127f83ea3cc609c93bd547bbc91c7541cfd0223f`; suo manifest `4ed360ee40d521e989e38fa2a2a68d5a5c461a5a6397c94dd34a598300141776`. Copie, originali e coordinate esterne verificati prima dell'uso e al termine. R4 rimane `3c64390bc4dd58c48cc4e1e388a38989b32b3143`, manifest `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`; piano rev.10 `6aaa5b3eebfed4ba502c25c0443caabd0051af21`. Nessuna modifica parallela incorporata.

✅ Contratto/test-first precedono il runtime nella storia Git. Verificati gli hash TEST_FIRST sui blob `567881ab…`: runtime ancora identico ad a219bd4; test iniziale SHA-256 `02c93b4c31e93d7d9b75ba440fab23a7f6a1839505d43723473850e7933f6682`. Il test finale ha SHA-256 `28d0a19fa18b2d83b74a4eb99e6640cb13e73e7f3388fb9ae34bf5dd042e7582`; [test_first_final.diff](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/test_first_final.diff) mostra soltanto il rafforzamento della guardia sui nuovi campi annidati. Non si confondono i due hash. Le vecchie prove rosse e le intermedie sono preservate, non sommate.

✅ Delta dal parent: 71 percorsi; dall'acquisizione: 76. Solo runtime modificato: ledger.py, +100/−22. Il test-first aggiunge sei file. Tre metriche, runtime C02/C03 esterni al ledger, sette D01 e otto D02, docs/walkthrough, phase_b, code, icl/ablation, piano, pseudolabel, schema, baseline, soglie Normal, APERTURA, preflight e inventario pending preservati. Nessuna esecuzione o rigenerazione scientifica.

## Risultati e corrispondenze

| Prova | Esito osservato | Evidenza |
| --- | --- | --- |
| Mirati completi | ✅ 120/120, zero failure/errori | [targeted.log](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/targeted.log) |
| Discovery completa | ✅ 155/155, zero failure/errori | [discovery.log](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/discovery.log) |
| Nove D03 finali sul respinto | Nove metodi, otto failure pertinenti, zero errori | red_contract.json/log |
| Stesso file D03 sul corretto | ✅ 9/9 | green_contract.json/log |
| W01–W04 byte-identici | ✅ 4/4, D03 originario corretto | w_original/evidence/retry_proof_probes.json/log |
| Y01–Y07 / Z01–Z05 byte-identici | ✅ 7/7 e 5/5 | y_original e z_original/evidence |
| Originali applicabili | ✅ 14/14, 12 letterali + N20/N21 sola fixture/argomento | applicable/applicable.json/log |
| X01–X18 letterali | ✅ 18/18 | literal/evidence/extended.json/log |
| X19–X24 letterali | Cinque PASS, una failure X23 obsoleta, zero errori | literal/evidence/additional_edges |
| X23 già adattato | ✅ 1/1, nessuna nuova assertion adattata | x23_adapted/evidence/additional_edges |
| Nuove V01–V06 | Quattro PASS, due failure pertinenti a D04, zero errori | [independent_d03_probes.json](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/independent_d03_probes.json) e log omonimo |
| Guardiano documentale | NON PASS: 35 metodi, stessi 14 identificativi falliti, 1 skip, zero errori | documentation.log e documentation_comparison.json |

Le suite sono sovrapposte: sette D01, otto D02 e nove D03 sono già nei totali. Non si sommano metodi, sottocasi, righe di matrice o tentativi. X23 letterale pretende il vecchio comportamento C02 errato e resta visibile come failure; il consolidamento è 23 letterali più X23 già adattato. Quest'ultimo conserva TimeoutError, verifica 120 INVALID, T3/T6, 40 triplette non valutabili, dati ignoti null, riconciliazione immutabile e nessun reinvio. Nessuna pretesa 24/24 del file immutato.

[MATRICE_50_METODI.md](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/MATRICE_50_METODI.md), con JSON omonimo: **50 nomi espliciti**, fonti/riga, codice, log corrente passato e motivazioni degli adattamenti/accorpamenti. Dodici letterali, due fixture/argomento, 35 adattati/accorpati, N48 equivalente a C02 nella nuova API. Nessuna esclusione implicita, nessun 50/50 letterali. [MATRICE_ESTENSIONI.md](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/MATRICE_ESTENSIONI.md) distingue X/Y/Z/W/V e limiti di ciascuna prova.

Il guardiano è non bloccante per questo delta e non viene dichiarato PASS. Il primo confronto locale usava l'ordine degli identificativi, diverso dalla lista precedente: corretto il solo comparatore a insiemi/liste ordinate, stessi 14 identificativi. Non è una nuova failure candidata. L'errore di import iniziale della preparatrice rimane storia conservata; qui il target è esplicito in entrambe le invocazioni dirette D03.

## Invariante D03 e presidio N/F

✅ [ledger.py:493](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:493) centralizza gli undici controlli. La guardia osserva gli stessi undici controlli effettivamente superati in acquisizione, antenato retry e gate riconciliato. Le 37 varianti sui campi, in tre percorsi, rifiutano identità sbagliate, token positivi/negativi/mancanti/bool/stringa, ricevuta/evidenza/autore vuoti e binding errato. Le prove con digest locali riallineati verificano la semantica: non sono dichiarate resistenza a una riscrittura crittografica completa.

✅ [ledger.py:532](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:532) ricalcola contenuti e legame separato. Hash originali dei file distinti dai digest `digest(canonical_json(value))`, formula letterale del contratto. Quattordici alterazioni plausibili e dodici rimozioni degli involucri rifiutate. V02 conferma parsing/hash degli stessi byte letti una volta, anche con formattazione non canonica, e rifiuto di una modifica annidata dentro provider_evidence.

✅ V01: morte reale del processo dopo il primo evento, dopo il secondo e dopo stato/INVALID ancora prima del commit: rollback integrale dei dati logici, poi riconciliazione lecita. Morte dopo commit: stato, due eventi e INVALID durabili, nessuna risposta inventata, 12 intenti/11 risposte conservati. V03: vero scrittore di un altro processo bloccato durante la validazione e libero dopo; conferma dentro la stessa transazione. W03/W04 e V02/V03 rilevano nuovi fault nella stessa istanza, senza cache tra transazioni.

✅ Gate INTENT riconciliato e FAILED già INVALID poi riconciliato: entrambi verificati. V03 conserva l'INVALID originario, byte/artefatto invariati e nessuna riga response; una nuova prova alterata viene rifiutata. C02 mantiene 120 tentativi, FAIL/INVALID e denominatori, mai una promozione a risposta. Z05 e X23 adattato preservano replay FAIL e 120 INVALID; retry gate vietato.

✅ Runner/CLI budget e stability --resume con prova alterata: quattro rifiuti HarnessError, `server_mock.assert_not_called()`, zero nuovi invii, 132 intenti, stessi output/database logico. V04 verifica anche producer ancora aperto: prova alterata rifiutata prima della costruzione del client e del nuovo retry. D01/D02 conservano rifiuto di predecessori corrotti/incompleti, 139 intenti e assenza di scritture/invii nelle loro riproduzioni.

✅ Nuovo requisito storico: digest o marker mancanti bloccano riconferma, retry e gate senza backfill. La nuova prova usa davvero 0c8157f esatto e pulito in subprocess per creare una catena allora valida con retry: rifiuto corrente e **132 intenti invariati**. Le Y senza riconciliazioni di quel tipo restano positive. Le catene nuove con retry nove intenti/otto coppie e multi-hop dieci/otto restano valide, come remediation, sonda rimaterializzata dopo gate e summary rigenerato identico.

✅ Inventario: 69 voci, 33 colonne SQLite, undici campi prova/approvazione e 25 payload. **56 voci con nuove mutazioni, 13 collegate a contratti storici**, non nuove mutazioni individuali. La [matrice rigenerata](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/generated_fields/MATRICE_D03_CAMPI.json) usa le osservazioni rosse/verdi di questa review: JSON e Markdown coincidono byte per byte con i candidati, verificato in field_matrix_comparison.json. La guardia segnala nuove colonne e chiavi nominate evidence/approval come DA_COPRIRE. Payload opachi improntati ereditano N; note, timestamp/catture esterne e duplicati forensi non alterano le decisioni nei positivi esercitati.

⚠️ L'inventario classifica strutture, non tutte le combinazioni valore/ruolo/stadio. In particolare la prova SQL candidata muta quota_kind dell'antenato in una catena già chiusa; non dimostra il controllo prima di una nuova riserva in uno stadio aperto. **V05/V06 smentiscono quest'ultima proprietà**, descritta sotto. Il presidio è utile ma incompleto per R05.

## Matrice requisito → codice → prova

| Requisito | Codice corrente | Prova e chiusura |
| --- | --- | --- |
| R01 | guards.py:93, ledger.py:243 | ✅ Test R01, X17, Y05; UNDECIDED/SUSPENDED bloccati e nessun default eseguibile |
| R02 | inputs.py:155, preparation.py:11 | ✅ N30–33/36–38/41/47/49, R02, X12/X14/X17; pin/input/handoff/raw producer autenticati |
| R03 | inputs.py:230, protocol.py | ✅ N34/35/39, R03, X17; label evaluator-side separata dall'ordine di presentazione ancora non approvato |
| R04 / D01 / D02 | ledger.py:211, 628 | ✅ Y/Z e D01/D02 completi: prerequisiti storici, raw, record, copertura/order, freeze/outcome; chiusi nelle manifestazioni originarie |
| R05 | [ledger.py:306](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:306), [ledger.py:606](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:606) | ❌ D04 aperto. N11–17/R05/X06–09/X19/X21 passano nei casi originari; V05/V06 trovano un superamento negli stadi aperti |
| R06 | ledger.py:704, producer_probe.py | ✅ R06, X10/X20/X24, remediation D01/D02: diff/template/diagnosi/casi concreti, una libreria completa, nessuna seconda remediation |
| R07 / C02 / C03 / D03 | runtime.py:41, producer_probe.py:181, ledger.py:493 | ✅ W 4/4, D03 9/9, V01–V04: contenuti e legami corretti; crash/restart; C02 invalidità in T3/T6; C03 nove richieste contro otto coppie. Distinto D04 sulle quote prima dell'invio |
| R08 | ledger.py:697 | ✅ R08, X18, Z01/Z02/Z04, D02; freeze/sonda/predecessori autenticati in transazione |
| R09 | guards.py:107, ledger.py:480 | ✅ R09, X13/X22, Y03/Y05; raw/consumo conservati, mismatch sospende, INVALID non maschera risposta |
| R10 | gate_rules.py:51 | ✅ N20–24, GateRevisions, X11, C02, Z05: 40×3, 120 ID, ripetizioni intere, agenti/condizioni/ruoli, zero retry gate |

Le righe sintetiche si collegano alle corrispondenze nominative e ai log nelle due matrici estese. Metriche qualificate: tre file invariati, nove metodi di raccordo passati. Non si trasferisce il giudizio a input reali, servizi o altri byte.

## D04 — P2 — Quota alterata nello stadio aperto permette un ottavo retry senza waiver

❌ **Requisito:** mandato D03 punti 4 e 7; contratto quote 8r+t≤15 e oltre sette trasporti solo con rinuncia esplicita; quota_kind deve coincidere con ruolo base/remediation/retry. Il campo è classificato N dall'inventario.

**Causa:** il nuovo controllo [ledger.py:606](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:606) viene applicato da `_validate_attempts` nella chiusura/riconferma di outcome. Nel [binding già esistente ma aperto:165](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:165) si verificano le riconciliazioni ZERO_TOKEN_PROVEN, senza quella coerenza di quota. La [nuova riserva:306](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:306) somma i quota_kind persistiti senza verificarne il ruolo. L'autenticità delle prove zero-token non implica l'autenticità del classificatore usato per consumare la riserva.

**V05, ledger pubblico:** un originale e sette retry, ciascun predecessore riconciliato lecitamente con il nuovo legame. Prima del fault, l'ottavo retry è rifiutato e il database rimane identico; nessun remediation_waived. Si cambia **un solo campo SQL**, quota_kind del primo retry da transport a base, lasciando retry_of, identità, prove, digest, link ed eventi intatti. Dopo restart il binding aperto e la nuova riserva accettano l'ottavo retry. Risultato: nove intenti, otto archi retry_of ma transport_calls=7; inserito un nuovo INTENT, nessun rifiuto preventivo.

**V06, producer ordinario:** stessa sequenza con timeout dello stub e sette retry esplicitamente selezionati. Il controllo senza fault blocca l'ottavo senza invii o nuove righe. Dopo la sola alterazione quota_kind e restart, `producer(resume=True, retry_requests=[ultimo])` effettua **un nuovo invio allo stub**, l'ottavo retry, senza waiver. Il successivo HarnessError è «transport failed; uncertain outcome needs explicit reconciliation»: è il timeout **dopo** l'invio, non un successo del controllo preventivo. Passaggio da otto a nove intenti; stato finale FAILED, transport_calls=7 contro otto retry effettivamente registrati. Database modificato, zero risposte ricevute nella fixture.

**Prove:** [independent_d03_probes.py:101](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/independent_d03_probes.py:101), JSON/log omonimi e `independent_fixtures/test_V05_open_stage_quota_fault_cannot_authorize_eighth_retry/`, `test_V06_real_runner_quota_fault_cannot_send_eighth_retry/captured/`. Due assertion pertinenti fallite, zero errori di setup. Non si fa affidamento sul solo exit code.

**Limiti:** guasto locale iniettato, non perdita spontanea dimostrata; nessuna impronta riallineata o riscrittura coerente dell'intera catena. Il nuovo invio è osservato solo sullo stub offline, con retry esplicitamente richiesto; nessuna inferenza reale o retry spontaneo. La chiusura completa dello stadio dispone del nuovo controllo ma arriva dopo la decisione di riserva/invio. Non viene dimostrato un PASS del producer, un GO, un azzeramento del totale o un superamento del hard stop 200. Il difetto è la sottocontabilizzazione normativa e il superamento della soglia sette senza rinuncia.

La chiusura richiede che la coerenza quota/ruolo protegga anche le decisioni negli stadi aperti, prima delle nuove riserve e degli invii, conservando i positivi e i contatori. **Nessuna correzione applicata.** D03 sui contenuti/legami delle prove rimane chiuso nelle riproduzioni; D04 limita separatamente R05.

## Consegna e confini

**NON OK limitato al tecnico esatto.** Conteggi dichiarati confermati; D01/D02/D03 originari passano; D04 resta aperto. [Stato Git finale](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/final_git_state.json): candidato detached pulito, dodici repository con HEAD/tree invariati; undici con status identico. Nel source D03 è comparso durante la review un file non tracciato `VERIFICA_D03.md` (13.529 byte, SHA-256 `bc3ee96afb2bd890d0b326ca4965d03c46d241f288a30c5ee1455a0c8ec9a47f`). Non è stato creato o modificato da questa sessione; sono stati letti solo identità e incipit per identificare la differenza, senza incorporarne il giudizio. Il file è stato lasciato intatto; source HEAD/tree e contenuti tracciati invariati. Dettaglio in external_git_changes.json. Principale con HEAD `819b12e97fb94d501032655ec2f226139e6c5ca5`, branch codex/studio2-soglie-normal e untracked preesistenti preservati. Nessun commit/tag/push/merge/integrazione o modifica al walkthrough. Rete soltanto per letture Git richieste; nessuna provider API, inferenza o simulazione scientifica.

D9 è già approvata: **122B producer principale e consumer, 27B alternativo per una libreria completa di 16 insight, Terra storico descrittivo interno**. La vecchia proposta Terra è superata; nessuna nuova decisione sui ruoli richiesta. Restano separati recepimento eseguibile D9, ordine label 1a ancora non approvato, insight reali, qualificazioni servizi/tokenizer/identità/capienza, T5 e autorizzazione pilot. Preflight storico UNDECIDED/SUSPENDED invariato. Nessun trasferimento del giudizio a un delta futuro, nessun freeze o GO.

[COMANDI.md](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/COMANDI.md), [inventario](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/EVIDENCE_INVENTORY.json), [SHA256SUMS](/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/SHA256SUMS). L'inventario distingue file regolari e symlink senza seguirli; nessuna autoreferenza. Hash del verbale e del manifest comunicati esternamente. Le fixture catturate conservano riferimenti ai temporanei originari poi rimossi dal cleanup; per riprodurre usare nuove directory, mai sovrascrivere prove conservate o eseguire script tracciati con output in-place.
