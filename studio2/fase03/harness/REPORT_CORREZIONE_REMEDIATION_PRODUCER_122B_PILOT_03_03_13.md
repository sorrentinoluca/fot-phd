# Correzione remediation producer 122B `pilot-03` — 03.13

## Esito

**READY FOR INDEPENDENT REVIEW (author).** Sono stati corretti offline i due difetti emersi
dalla review indipendente e dalla nota dell'autore sul candidato
`72e20d84fdc1a3251df98fe00b1bbd9026fc37ed`, tree
`b340794ca9ca370121fb7154804a3d500d2670f5`.

La review sorgente è
`/Users/luker/.codex/worktrees/b567/fot-tep/studio2/fase03/harness/VERIFICA_ESITO_REMEDIATION_PRODUCER_122B_PILOT_03_03_13.md`,
SHA-256 `f0b9ca37d0ab61a37ad0f69fbaee250047725467f0eb21819122b81c78747552`,
verdetto `NOT CONFIRMED`.

Questa correzione non rimuove né modifica lo STOP reale e non autorizza o riesegue la
remediation scientifica.

## Scoping contabile `stage + logical_id`

`validate_tokenizer_accounting_evidence` richiede ora che una mappa di messaggi attesi sia
accompagnata dallo stage esatto. La sostituzione del messaggio persistito avviene soltanto se
entrambi coincidono:

```text
request.stage == expected_stage
request.logical_id in expected_messages
```

Gli eventi degli altri stage vengono rivalidati esclusivamente con i messaggi durevoli
incorporati nel loro evento contabile. Di conseguenza i prompt remediation `agent_1`–`agent_8`
non possono più sostituire i prompt T9 omonimi. Un mismatch nello stesso stage continua invece
a produrre lo STOP durevole previsto.

I due caller che forniscono messaggi correnti dichiarano esplicitamente il proprio stage:

- `producer_probe.run`: lo stage richiesto (`producer_conformity`, `producer_remediation` o
  `alternate_conformity`);
- `technical_qualification_122b.run`: `technical_qualification_122b`.

Non sono stati indeboliti autenticazione del binding, identità della request, riconteggio locale,
controllo `enable_thinking=false`, raw binding o persistenza dello STOP.

## Durabilità dell'approval diagnosi

Le nuove diagnosi incorporano nel ledger:

- path e SHA-256 del file approval;
- contenuto JSON approvato;
- byte UTF-8 esatti del file.

In riuso, il ledger ricostruisce i byte incorporati, ne ricalcola lo SHA-256, rilegge il JSON e
verifica che coincida con il contenuto incorporato e con diagnosi, autore, decisione e
`records_sha256`. Eliminare il file sorgente dopo una diagnosi valida non impedisce più una
successiva `authorize_remediation`.

L'unico formato storico già registrato su `pilot-03`, che contiene soltanto path e hash, resta
compatibile ma fail-closed: continua a richiedere il file esterno. Non è stato backfillato né
riscritto. Nel ledger reale l'authorization remediation era già stata registrata prima dello
STOP, quindi questa compatibilità non altera la storia.

## RED/GREEN

Gli stessi tre test finali sul candidato respinto hanno prodotto tre errori attesi:

1. approval non incorporato (`KeyError: content`);
2. API `expected_stage` assente nel caso cross-stage;
3. API `expected_stage` assente nel controllo negativo same-stage.

Sul candidato corretto gli stessi tre test passano. Il controllo positivo dimostra che
`producer_remediation/agent_1` non altera la verifica di
`producer_conformity/agent_1`; il controllo negativo dimostra che un messaggio diverso nello
stesso stage continua a persistere `stop:tokenizer_accounting`.

## Verifiche

| Verifica | Risultato osservato |
|---|---|
| RED sul candidato respinto | 3 errori attesi in 0,119 s |
| GREEN mirata | 3/3 PASS in 0,121 s |
| Successor completa | 39/39 PASS in 5,464 s |
| Regressione esplicita, 15 moduli | 212/212 PASS in 447,244 s |
| `py_compile` dei moduli modificati | PASS |
| `git diff --check` | PASS |

La regressione ha emesso i `ResourceWarning` SQLite storici, senza failure o errori. Il guardian
documentale resta separato sul baseline noto: 35 test, 14 failure, 1 skip, 0 errori in 0,074 s.

## Stato runtime e limiti

Il ledger reale `pilot-03` non è stato aperto con SQLite né modificato e conserva SHA-256
`3690ccfac8a0807d20f1be581325748f392ed777a206ee7c2e8954106df19779`, incluso lo STOP
contabile. `pilot-001` resta a
`4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`.
Il controllo `lsof` finale è vuoto.

Nessuna rete, chiamata provider, remediation, retry, resume, 27B, alternate o probe è stata
eseguita. Nessun push, merge o tag. Una futura esecuzione richiede review indipendente del nuovo
candidato e una disposizione separata sullo STOP reale; non è inclusa in questa correzione.
