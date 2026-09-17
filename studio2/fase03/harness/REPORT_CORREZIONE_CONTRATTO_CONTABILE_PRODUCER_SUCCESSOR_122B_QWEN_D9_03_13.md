# Correzione contratto contabile producer successor 122B — Qwen D9 03.13

## Esito

**READY FOR NEW INDEPENDENT REVIEW.** È stato corretto esclusivamente il rilievo residuo sul
contratto contabile del producer successor 122B del candidato respinto
`66f3cbfc1e294c8250c6c2102120705a0c3771dc`, tree
`e44ed15f74123331ef2a103e69ffc8457a7f3e79`, parent
`ef6d6ef550d59d11233f8f9dc4af6abd247dcff9`.

Il verbale NON OK è conservato byte-identico in
`harness/reviews/VERIFICA_RIVERIFICA_FINALE_SUCCESSOR_122B_QWEN_D9_03_13.md`; sorgente e copia
hanno SHA-256 `a44d1ea92de25d5628f3b50ab7367ed4b9127a605fca556d1fe0fb1829a11e8e`.
Il manifest è
`CORREZIONE_CONTRATTO_CONTABILE_PRODUCER_SUCCESSOR_122B_QWEN_D9_03_13.manifest.json`, SHA-256
`e956ec2ed3b0ebe69cae80e903da48d3c09215ef4f33367fbab0f1212f8e2c04`.

La consegna non abilita materializzazione, authorization o esecuzione scientifica.

## Difetto riprodotto sugli stessi byte

I 20 metodi finali di `test_successor_recovery.py` sono stati eseguiti in un archivio Git isolato
del candidato `66f3cbf...`. Il runner ha riportato **6 failure comportamentali e 0 errori**. Le
failure dimostrano che il candidato respinto:

- acquisisce come valida una prova `producer_conformity` 122B senza kwargs;
- accetta dopo restart una prova priva del controllo, anche con digest e link riallineati;
- consente il rebind dello stage e la prenotazione successiva;
- acquisisce nello stesso modo una prova `producer_remediation` 122B non conforme.

Il controllo positivo per ledger generico, consumer e producer 27B passa anche sul candidato
respinto: il differenziale non dipende da un cambiamento dei percorsi che devono restare invariati.

## Contratto contabile corretto

`PilotLedger._validate_accounting_contract` resta l'unico validatore semantico usato durante la
prima acquisizione e in ogni riuso. Il nuovo helper interno
`_successor_122b_producer_accounting` non introduce flag diagnostici: deriva l'obbligo da stato e
contenuti durevoli già presenti.

Il requisito è vero soltanto quando coincidono:

1. ledger successor v4 con lineage importato;
2. stage `producer_conformity` o `producer_remediation`;
3. modello contabile 122B;
4. `stage_run`, identità, modello e producer della richiesta con il binding immutabile autenticato.

In quel contesto il contratto accetta esclusivamente
`{"chat_template_kwargs":{"enable_thinking":false}}`. Assenza, numero `0`, booleano `true`,
chiavi aggiuntive e strutture diverse sono rifiutati. La stessa decisione viene applicata prima di
persistire il commitment e quando il record viene riaperto.

L'inventario condiviso rivalida inoltre ogni record 122B completato prima di rebind e prenotazioni.
Una prova legacy o alterata viene quindi rifiutata nella stessa transazione della decisione, prima
di una nuova riga persistente. I test confrontano il dump logico con la baseline incoerente e
verificano che resti una sola richiesta producer.

## Copertura positiva e confini

Il percorso positivo con il booleano esatto `false` completa accounting, record e richiesta,
riapre il ledger, rivalida il record e prenota correttamente l'indice successivo. La remediation
122B raggiunge la vera frontiera di acquisizione dopo otto richieste di conformità, outcome FAIL
diagnosticato e autorizzazione locale della remediation.

Restano invariati e coperti positivamente:

- ledger generico v2 con producer 122B senza kwargs;
- consumer 122B in `budget_probe` senza kwargs;
- producer alternativo 27B senza accounting 122B.

R1, C1 e gli F1/F2 originari restano chiusi. Restano inoltre verdi i sette campi R2 già coperti e
la validazione provider C2.

## Verifiche finali

| Verifica | Risultato osservato |
|---|---|
| Test mirati finali | 20/20 PASS in 4,403 s |
| Stessi byte su `66f3cbf...` | 20 metodi, 6 failure comportamentali attese, 0 errori |
| Regressione pertinente completa, 15 moduli | 197/197 PASS in 472,861 s |
| `git diff --check` | PASS |
| Guardian documentale storico | 35 test, 14 failure, 0 errori, 1 skip; NON PASS invariato |

La regressione completa comprende C01–C03, D01–D04, D9 e correzioni, runner offline,
riconciliazione storica, raccordo metrico, revisioni, successor recovery, accounting tokenizer,
execution guard e protocollo. I `ResourceWarning` SQLite storici non hanno modificato il
riepilogo del runner.

## Invarianti e limiti

Non sono cambiati disegno scientifico, quote, ruoli 122B/27B, prompt scientifici, denominatori,
ordine degli stage o decisioni autoriali. Il massimo cumulativo resta 166, l'hard stop 200 e il
margine non spendibile 34.

Durante la correzione non sono stati aperti, letti, hashati o modificati ledger e configurazioni
runtime private; il loro stato non viene ricertificato per inferenza. Non è stato creato il target
fresco. Sono state usate soltanto fixture locali, sorgenti e artefatti versionati.

Nessun provider o servizio esterno è stato contattato, zero token, nessun tunnel, nessuna
authorization e nessuna esecuzione scientifica. `server_enea.json` non è stato letto o stampato.
Nessun push, merge o tag. Commit, tree, parent e stato pulito del candidato sono riportati
nell'handoff finale dopo la finalizzazione degli artefatti, evitando riferimenti circolari.

Il solo passo successivo ammesso è una nuova review indipendente. La materializzazione del target
fresco resta esplicitamente disabilitata.
