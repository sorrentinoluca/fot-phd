# Correzione riverifica successor 122B — Qwen D9 03.13

## Esito

**READY FOR NEW INDEPENDENT REVIEW.** Sono stati corretti esclusivamente R1, R2, C1 e C2
segnalati dopo il candidato respinto `ef6d6ef550d59d11233f8f9dc4af6abd247dcff9`, tree
`47610aee32a3a1bfddc650edda4b81fc583a0155`, parent
`65dad03c7878b5ba1b3dc185861f93387bef78a0`.

Il verbale NON OK è conservato byte-identico in
`harness/reviews/VERIFICA_CORREZIONE_REVIEW_SUCCESSOR_122B_QWEN_D9_03_13.md`; sorgente e copia
hanno SHA-256 `790ceb1e49dde5fba926a8e7b6b450ce8600651c2f6b74b5cda013b5ddc853bc`.
Il manifest è `CORREZIONE_RIVERIFICA_SUCCESSOR_122B_QWEN_D9_03_13.manifest.json`, SHA-256
`acee4b3c2f06f0f37b89be41901b98fa072858b36586fe845626e9adb3d2f844`.

La consegna si ferma alla correzione locale: non autorizza materializzazione, authorization o
qualifica tecnica.

## Rosso differenziale sul candidato respinto

Gli stessi byte finali dei 16 metodi di `test_successor_recovery.py` sono stati sovrapposti a una
copia isolata di `ef6d6ef...` estratta dagli oggetti Git. Il runner ha riportato **10 failure
comportamentali attese e 0 errori**. Il rosso comprende:

- accettazione del target v2 successor privo dell'import S=5 nei percorsi diretto, preflight,
  restart, binding e prenotazione, con una scrittura che non doveva avvenire;
- accettazione, nel riuso chiuso, di mutazioni contabili internamente riallineate e conseguente
  creazione del binding successivo;
- assenza del rifiuto esplicito di `extra_body` nella qualifica tecnica;
- assenza dell'obbligo caller-specific del booleano esatto `false` nella conformità producer 122B.

Le failure sono quindi differenze di comportamento, non errori di ambiente, import o interfaccia.
I test F1/F2 precedenti e i relativi positivi sono rimasti nei medesimi byte finali.

## R1 — import S=5 obbligatorio nel percorso successor

`PilotLedger._validated_predecessor_lineage` mantiene il comportamento generico dei ledger v2/v3
soltanto quando nessun caller richiede riferimenti successor. Se il percorso passa esplicitamente
package o approval e non esistono ancora righe/evento di lineage, il validatore fallisce chiuso
prima di scrivere.

La stessa regola viene così riusata da validazione diretta, `require_pilot_ledger`, riapertura,
binding e prenotazione. I negativi confrontano il dump logico prima/dopo e verificano zero righe
in `requests`. Il positivo esegue l'import valido, riapre il ledger, supera il preflight, crea il
binding e prenota: predecessori 5, cumulativo 6. Nessuna regola globale basata sulla sola versione
è stata aggiunta.

## R2 — contratto contabile completo in acquisizione e riuso

`PilotLedger._validate_accounting_contract` è ora il contratto semantico unico applicato sia alla
prima acquisizione sia alla prova persistita riusata. Rivalida chiavi esatte, singolo messaggio
utente e relativo hash, legame col prompt della richiesta, versione artefatto, request ID e identità,
snapshot congelato, hash della risposta raw, conteggi locali/server/usage raw interi non negativi e
uguali, outcome e kwargs no-thinking dove richiesti.

Sette fixture alterano separatamente `messages`, conteggio locale, conteggio server, `snapshot`,
`request_identity_sha256`, `artifact_version` e `raw_response_sha256`, riallineando event digest,
request proof e record link. Same-instance e restart rifiutano sia `verify_stage_success` sia il
binding producer successivo senza nuovi effetti. Il positivo completa realmente il riuso chiuso e
crea il normale binding successivo.

## C1 e C2 — `extra_body` caller-specific

Il contratto e il provider della qualifica tecnica 122B usano un requisito esplicito che rifiuta
l'assenza di `extra_body`; il pin del file provider resta invariato. Nelle configurazioni successor,
la qualifica tecnica, la conformità e l'eventuale remediation del producer 122B accettano soltanto:

```json
{"chat_template_kwargs":{"enable_thinking":false}}
```

Assenza, `0`, `true`, chiavi aggiuntive e forme diverse sono rifiutate. Il validatore generico e il
producer alternativo 27B conservano il comportamento precedente; consumer, sonda e gate non sono
stati modificati.

## Verifiche finali

| Verifica | Risultato osservato |
|---|---|
| Test mirati finali | 16/16 PASS |
| Stessi byte su `ef6d6ef...` | 16 metodi, 10 failure comportamentali attese, 0 errori |
| Regressione focalizzata, 4 moduli | 54/54 PASS in 21,736 s |
| Regressione pertinente completa, 15 moduli | 193/193 PASS in 469,859 s |
| `git diff --check` | PASS |
| Guardian documentale storico | 35 test, 14 failure, 0 errori, 1 skip; NON PASS invariato |

La regressione completa comprende C01–C03, D01–D04, D9 e relative correzioni, runner offline,
riconciliazione storica, raccordo metrico, revisioni, successor recovery, accounting tokenizer,
execution guard e protocollo. I `ResourceWarning` SQLite già presenti in test storici non hanno
modificato il riepilogo.

## Invarianti e limiti

Non sono cambiati disegno scientifico, quote, ruoli 122B/27B, prompt scientifici, denominatori,
ordine degli stage o decisioni autoriali. Il massimo cumulativo resta 166, l'hard stop 200 e il
margine non spendibile 34. I rilievi originari F1/F2 restano chiusi e coperti.

Durante questa correzione non sono stati aperti, letti, hashati o modificati ledger e configurazioni
private; il loro stato non viene quindi ricertificato per inferenza. Non è stato creato il target
fresco. Sono state usate esclusivamente fixture locali e artefatti versionati.

Nessun provider o altro servizio esterno è stato contattato, zero token, nessun tunnel, nessuna
authorization e nessuna esecuzione scientifica. `server_enea.json` non è stato letto o stampato.
Nessun push, merge o tag. Commit, tree, parent e stato pulito del nuovo candidato sono riportati
nell'handoff finale dopo la finalizzazione degli artefatti, evitando riferimenti circolari.

Il solo passo successivo ammesso è una nuova review indipendente. La materializzazione del target
fresco resta esplicitamente disabilitata.
