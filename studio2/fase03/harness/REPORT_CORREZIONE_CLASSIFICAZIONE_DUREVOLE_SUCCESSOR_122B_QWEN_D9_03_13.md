# Correzione classificazione durevole successor 122B — Qwen D9 03.13

## Esito

**READY FOR NEW INDEPENDENT REVIEW.** È stato corretto esclusivamente il rilievo sulla
classificazione successor/generic e sull'ordine della relativa autenticazione nel candidato
respinto `72fb93c6d26ceb220ed2cece1dac2ef6614c791f`, tree
`08577a5d86c4b2731a0d48ccd83ca48d916c37fa`, parent
`66f3cbfc1e294c8250c6c2102120705a0c3771dc`.

Il verbale NON OK è conservato byte-identico in
`harness/reviews/VERIFICA_RIVERIFICA_CONTRATTO_CONTABILE_PRODUCER_SUCCESSOR_122B_QWEN_D9_03_13.md`;
sorgente e copia hanno SHA-256
`53231569fe36abdda9b5a7916150a38d8173c244ca1921b535f71b1f45e0564c`.
Il manifest è
`CORREZIONE_CLASSIFICAZIONE_DUREVOLE_SUCCESSOR_122B_QWEN_D9_03_13.manifest.json`, SHA-256
`0df1ec0f433f8b5487880867376a61656eb2bec428c7810beb32c19acadb3558`.

La consegna non abilita materializzazione, authorization o esecuzione scientifica.

## Difetto riprodotto sugli stessi byte

Il file finale `test_successor_recovery.py`, SHA-256
`f81801af9803e6dba0051e9be05bbb8e49adfe3464e31e0bf0ded8d4d84c2f6f`, è stato eseguito sia
contro il candidato respinto sia contro la correzione. Sul commit `72fb93c...`, estratto in un
archivio Git isolato, i 23 metodi hanno prodotto **8 failure comportamentali e 0 errori di
ambiente**.

Le failure mostrano che il candidato respinto accetta:

- il downgrade durevole v4→v2 con cinque righe ed evento successor ancora presenti nei percorsi
  contabile diretto, rebind, prenotazione, quota e snapshot;
- un riuso contabile diretto dopo downgrade persistito del modello 122B→27B;
- un riuso contabile diretto dopo modifica persistita dello stage.

Il controllo v3 conferma inoltre il bypass diretto della prova contabile. I positivi successor
nominale, generic v2, consumer e producer 27B continuano a passare sul candidato respinto: il
rosso è differenziale e non dipende da errori di importazione o fixture.

## Classificazione durevole corretta

`PilotLedger._classified_successor_lineage` è ora il percorso condiviso di classificazione. Esso
ispeziona righe `predecessor_lineage`, eventi `successor_lineage:*`, `user_version` e riferimenti
richiesti dal caller D9. Se almeno uno di questi elementi indica o richiede un successor, esegue
la validazione completa già esistente del lineage e rifiuta ogni incoerenza di versione, evento,
righe o artefatti approvati.

Un ledger è classificato generic soltanto se:

1. la versione è realmente v2 o v3;
2. non esistono righe o eventi successor;
3. il caller non richiede package o approval successor.

`_quota_context` riusa questa classificazione per predecessori, prenotazione e conteggi. Lo stesso
percorso è chiamato da prerequisiti, snapshot e preflight D9; non esiste più un dispatcher di
quota che possa ignorare artefatti successor sulla base del solo `PRAGMA`.

## Ordine del contratto contabile

`PilotLedger._requires_no_thinking_accounting` classifica prima l'inventario durevole e poi carica
il binding normativo dello stage. Prima di decidere se il requisito no-thinking si applica,
confronta `stage_run`, identità completa, modello e producer della richiesta con l'unica specifica
del binding. Una discordanza fallisce chiuso; non può ricadere nel percorso generic.

Per conformità e remediation del producer successor 122B resta obbligatorio il valore esatto:

```json
{"chat_template_kwargs":{"enable_thinking":false}}
```

Il validatore semantico condiviso resta `_validate_accounting_contract`, usato sia alla prima
acquisizione sia nel riuso. C1, F1/F2, i controlli R2 e la validazione provider C2 restano chiusi.

## Copertura avversariale e positiva

I nuovi test coprono separatamente:

- `user_version` 2 e 3 in presenza di righe/evento successor;
- modello, stage, `stage_run`, identità e producer persistiti difformi dal binding;
- API contabile diretta, same-instance/restart, rebind, prenotazione, quota, snapshot e preflight;
- invarianza del dump logico sul rifiuto e assenza di nuovi intent;
- conteggio positivo di cinque predecessori e cumulativo 7 dopo qualifica più prima richiesta;
- positivi successor, generic v2, consumer 122B e producer alternativo 27B.

## Verifiche finali

| Verifica | Risultato osservato |
|---|---|
| Stessi byte su `72fb93c...` | 23 metodi, 8 failure comportamentali attese, 0 errori, 4,431 s |
| Test mirati corretti | 23/23 PASS in 4,407 s |
| Regressione focalizzata, 4 moduli | 61/61 PASS in 22,227 s |
| Regressione pertinente completa, 15 moduli | 200/200 PASS in 441,608 s |
| `git diff --check` | PASS |
| Guardian documentale storico | 35 test, 14 failure, 0 errori, 1 skip; NON PASS invariato |

La regressione completa comprende C01–C03, D01–D04, D9 e correzioni, runner offline,
riconciliazione storica, raccordo metrico, revisioni, successor recovery, accounting tokenizer,
execution guard e protocollo. I `ResourceWarning` SQLite storici non modificano il riepilogo del
runner. Il guardian documentale è mantenuto separato e non viene riclassificato come PASS.

## Invarianti e limiti

Non sono cambiati disegno scientifico, quote, ruoli 122B/27B, prompt scientifici, denominatori,
ordine degli stage o decisioni autoriali. Il massimo cumulativo resta 166, l'hard stop 200 e il
margine non spendibile 34.

Durante la correzione non sono stati aperti, letti, hashati o modificati ledger e configurazioni
runtime private; il loro stato non viene ricertificato per inferenza. Non è stato creato né
materializzato il target fresco. Sono state usate soltanto fixture, sorgenti e artefatti locali
versionati.

Nessun provider o servizio esterno è stato contattato: zero token, nessun tunnel, nessuna
authorization e nessuna esecuzione scientifica. `server_enea.json` non è stato letto o stampato.
Nessun push, merge o tag. Commit, tree, parent e stato pulito del nuovo candidato sono riportati
nell'handoff finale dopo la finalizzazione degli artefatti, evitando riferimenti circolari.

Il solo passo successivo ammesso è una nuova review indipendente. La materializzazione del target
fresco resta esplicitamente disabilitata.
