VERDETTO: OK

# Verifica indipendente del nuovo delta d'integrazione del raccordo metriche

Il verdetto è limitato al delta
`e82b5a08bf642ad45f77e71832958207beb1181c..3360867751c66a39e819247f86dab8e936f8cbb3`.
Non ripete la review tecnica di `caf5bfb`, non chiude 03.9/03.10, non rende efficace alcun
freeze e non qualifica l'harness completo.

## Identificazione della verifica

- Data: 2026-09-14, fuso Europe/Rome.
- Revisore: OpenAI Codex, modello basato su GPT-5.
- Provider/prodotto: OpenAI, Codex desktop.
- Reasoning: non esposto in modo verificabile.
- ID sessione/task: non esposto; non inventato.
- Worktree sorgente indicato:
  `/Users/luker/fot-tep/.worktrees/integrazione-raccordo-metriche`.
- Copia isolata usata per la verifica:
  `/tmp/verifica-integrazione-raccordo-metriche.g7zshq/candidato`, ottenuta con `git archive`
  dall'oggetto commit; non contiene `.git`, `.worktrees` o symlink verso checkout fratelli.
- Base: `e82b5a08bf642ad45f77e71832958207beb1181c`.
- Commit candidato verificato: `3360867751c66a39e819247f86dab8e936f8cbb3`.
- Catena verificata: `fae8ae82a8ed295feb79ebc554190cc046166d74` →
  `f4bca454bcbc84ab66a432140a9b2e9a5cc42f11` →
  `f890a3d691258be5f2abd3bb34d8e327346cedac` →
  `3360867751c66a39e819247f86dab8e936f8cbb3`.

La verifica è stata svolta in sola lettura sul contenuto del candidato. Non sono stati eseguiti
commit, merge, push, tag, chiamate API, simulazioni o run finali. Il solo file prodotto è questo
verbale esterno al commit certificato.

## 1. Import byte-identico

Esito: **PASS**.

I nove file importati da `fae8ae8` corrispondono byte per byte alle rispettive fonti dichiarate:

- `common.py`, `metric_adapter.py`, `metrics.py`, `__init__.py`, `SPECIFICA_HARNESS.md` e
  `CONTRATTO_RACCORDO_METRICHE.md` coincidono con `caf5bfb`;
- `REPORT_RACCORDO_METRICHE.md`, `METRIC_INTERFACE_CANDIDATE.json` e
  `PROMPT_VERIFICA_RACCORDO_METRICHE.md` coincidono con `1ac06eb`.

I quattro file acquisiti da `f4bca45` coincidono byte per byte con `6c51330`:
`VERIFICA_RACCORDO_METRICHE.md`, `CONSEGNA_RACCORDO_METRICHE_03_10.md`,
`CONSEGNA_VERIFICA_RACCORDO_METRICHE.md` e `REGISTRO_OK_RACCORDO_METRICHE.md`.

Impronte ricalcolate e preservate:

- verbale: `0d90779981871b8c9ceaf2a729f97b371abb7297fb804dc4335ddf0f1bec0e80`;
- report: `8ab3ac62b9fc066259fb00afb1b8d96a6954d8355a4af1e40559d56b7d201c2e`;
- contratto: `5c81586f30ddfe8f39f99b313a30e2dad84346821750e93c11f4d5eecc1e7480`.

Il manifest conserva `independent_verification.status: PENDING` e
`reviewer_identity: null`; non è stato aggiornato in luogo. I quattro file pinnati della baseline
03.9 (`baseline.py`, `SPECIFICA_BASELINE_NUMERICA.md`, `INTERFACE_CHECK.json` e
`BASELINE_FREEZE_rev003.json`) hanno gli stessi blob in `c486eee` ed `e82b5a0` e le quattro
SHA-256 dichiarate nel manifest coincidono.

## 2. Chiusura delle dipendenze

Esito: **PASS**.

La chiusura runtime effettiva è `common` + `metric_adapter` + `metrics`, oltre alla sola stdlib.
Il test mirato importa esclusivamente questi tre moduli del package. Non risultano import o accessi
runtime a canary, guards, inputs, insight_adapter, logging_v1, producer, sampling, ordering,
render o al `test_harness.py` completo; non risultano manipolazioni di `sys.path`, percorsi assoluti,
subprocess, rete o riferimenti a checkout fratelli.

L'analisi AST rileva 7 definizioni in `common.py`, 6 in `metric_adapter.py` e 18 in `metrics.py`,
senza corpi vuoti/pass/ellipsis. `__init__.py` contiene una docstring di package e non è uno stub
runtime. La compilazione dei quattro file Python interessati passa.

`LABELS` coincide con `test_harness.py@caf5bfb`, righe 33–43; `AGENTS` coincide con
`inputs.py@caf5bfb`, riga 25.

## 3. Comportamento sul checkout effettivo

Esito: **PASS**.

Comando eseguito nella copia isolata:

```text
python3 -m unittest studio2.fase03.harness.test_metric_raccordo -v
```

Risultato: **9 test eseguiti, 9 OK, 0 skip, 0 failure, 0 error**. La copia non contiene checkout
fratelli né collegamenti verso di essi.

I casi verificano mapping e identità numerica, adattamento di tutte le foglie consumer, conteggi e
denominatori, astensioni, input invalidi, insieme vuoto, insieme tutto astenuto, invalidi inclusi
nel denominatore non-astenuti, rifiuti fail-closed per sorgenti incoerenti/estranee e gate SHA-256.

## 4. Fedeltà del test estratto

Esito: **PASS**.

La sequenza completa di 248 righe di `MetricTests` da `test_harness.py@caf5bfb`, righe 103–350,
compare una volta e byte-identica alle righe 55–302 di `test_metric_raccordo.py`. Nessuna
asserzione, soglia o corpo di test è stato alterato. Il `test_harness.py` completo non è presente
nel candidato.

## 5. Documentazione

Esito: **PASS**.

La sezione §4.10 è presente sia in Markdown sia in HTML con anchor univoco
`harness-raccordo-metriche-0310`. Il confronto del testo visibile normalizzato produce la stessa
sequenza di 1.015 token nelle due rappresentazioni. Tutti i link della sezione risolvono: anchor
§4.9, report, contratto, verbale tecnico e registro OK.

La nota di stato distingue correttamente:

- il delta tecnico `5116087..caf5bfb`, già verificato OK;
- il nuovo candidato d'integrazione su `e82b5a0`, dichiarato non ancora verificato nel contenuto
  candidato;
- `common.py` e il test mirato come dipendenze/lavoro aggiunto da verificare.

La formulazione non attribuisce l'OK tecnico all'harness completo e mantiene espliciti i lavori
residui.

## 6. Guardiano documentale

Esito: **PASS**.

`python3 docs/test_explanation.py` è stato eseguito separatamente nella copia di `e82b5a0` e in
quella di `3360867`. Entrambe le esecuzioni restituiscono **35 test, 14 failure, 1 skip**. I 14
identificativi, inclusi tutti i subtest parametrizzati, coincidono esattamente; nessun nuovo
fallimento è introdotto dal candidato.

## 7. Perimetro preservato

Esito: **PASS**.

Il diff contiene soltanto la nuova directory selettiva `studio2/fase03/harness/` e la coppia
MD/HTML del walkthrough. Non modifica D9, ruoli dei modelli, configurazione canonica, piano
statistico, pin 03.12, endpoint, input pending, ledger o `run_pilot`. L'ordine canonico delle label
non è modificato; la costante nel test è una copia fedele usata soltanto dal test.

## 8. Dipendenza rev. 10

Esito: **PASS con limite di raggiungibilità**.

La dipendenza `studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md` è soltanto citata con il
riferimento Git stabile `6aaa5b3eebfed4ba502c25c0443caabd0051af21`. Le verifiche ricalcolano:

- blob Git `780e08ae9e176a819a745ab2054a2e6ae79a8a9a`;
- SHA-256 contenuto `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`.

Il file non esiste nell'albero del candidato e il delta non modifica `piano_statistico/`. La sua
raggiungibilità dipende quindi dal riferimento Git esterno stabile: questo è un limite residuo
dichiarato, non un difetto del candidato d'integrazione.

## Conclusione

Il nuovo delta importa correttamente e senza alterazioni il raccordo e i relativi record, chiude il
solo grafo runtime necessario, aggiunge un test fedele che passa 9/9 nel checkout isolato e mantiene
invariato il guardiano documentale. Documentazione e perimetro sono coerenti; la dipendenza rev. 10
resta solo citata e costituisce il limite di raggiungibilità richiesto.

**VERDETTO: OK**, esclusivamente per `e82b5a0..3360867`.
