# Correzione D02 — nuovo candidato locale, verifica indipendente richiesta

15 settembre 2026. Incarico implementativo; non è un verbale di review e non chiude il NON OK.

## Risultato e causa

La riconferma usa ora lo stesso validatore completo della chiusura, anche per ciascun
predecessore della sonda/gate. Il vecchio ramo `_successful` si fidava di PASS/COMPLETED
senza verificare copertura, raw/record e artefatto: il nuovo `_closed_outcome` rilegge le
prove e le autentica tramite `_validate_outcome`, nella transazione già aperta.
Le tre manifestazioni di D02 riprodotte da Z01–Z03 vengono rifiutate senza modifiche a database/artefatti
o nuovi invii. Z04/Z05 restano validi. D01 originario è chiuso **dal revisore**, così come
C02/C03 nei percorsi del verbale acquisito; D02 resta da sottoporre alla sua nuova review.

## Identità e catena locale

| Oggetto | Identificatore |
| --- | --- |
| Branch | `codex/studio2-harness-0310-d02` |
| Worktree isolato | `/Users/luker/fot-tep-harness-0310-d02` |
| Base documentale verificata | `7afbf41632aa8117c85274b5f471abca0a655462` |
| Candidato respinto | `edb37f359f29c461c5a507c1027c4bf411654130` |
| Tree respinto | `56d98666e1d18c7958ac8d3631ae6d5b8ec04bf9` |
| Acquisizione separata | `5b45cdcabe40aa64b0aecd1b5fe9d09c92ce5bb4` |
| **Nuovo candidato tecnico** | **`a219bd469bbd280f56b7fa9cb56cda115b0975ed`** |
| **Nuovo tree tecnico** | **`3fb8e50c189b85b447503b8a1ac99c1741904a5b`** |
| Manifest corrente | 70 file diretti, 17729 byte |
| SHA-256 manifest | `fb8474c6e71d63fbb54b83d46e63ae4238a7fb4b20d6c988866e27085d8db9a9` |
| Main remoto effettivo letto | `a00605862f627710347bd63c49f79a6d0a00135f` |

Il candidato tecnico era pulito prima della scrittura di questa consegna. Il successore
aggiunge esclusivamente REPORT_CORREZIONE_D02.md, PROMPT_VERIFICA_D02.md, CONSEGNA_D02.json
e DELIVERY_AUDIT_D02.json. Il suo HEAD non è il candidato tecnico; il report non include
l’hash del proprio commit. I commit sono locali, senza push/merge/tag.

## Acquisizione prima delle correzioni

[Verbale originale](non_ok_edb37f3_20260915/files/VERIFICA_D01.md),
[manifest originale](non_ok_edb37f3_20260915/files/SHA256SUMS) e prove provengono da
`/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence`.

- SHA-256 verbale: `2806ce5c15d51c917e3e19cc77a935c37ffe09134b485fa257401f6b85ad2fd6`.
- SHA-256 manifest: `dceb4ae6bd4c177002c0bbc1c942333590f114218d1499ebab0ae6475459dffd`.
- Verificati **1.821 membri + il manifest**, prima dell’uso e nuovamente prima della consegna.
- **100 copie byte-identiche**, comprese le nuove fixture Z; **1.722 file esterni** recuperabili
  con percorso, hash, dimensione e motivazione. Cinque symlink registrati separatamente.
- [Inventario](non_ok_edb37f3_20260915/ACQUISITION_INVENTORY.json) e
  [provenienza](non_ok_edb37f3_20260915/PROVENIENZA.md) distinguono le fixture alterate.

Il source 7afbf41 e il clone detached edb37f3 sono stati verificati prima delle scritture;
il source 7afbf41 differisce dal precedente tecnico edb37f3 solo nei quattro documenti di consegna. Le riproduzioni
usano nuovi sandbox. Nessun guasto è stato applicato al candidato, alla principale o
alle prove precedenti. I fault SQL avvengono dopo una chiusura valida, esclusivamente
nelle copie sacrificabili. Non sono fonti o risultati scientifici.

## Delta implementato

Solo `ledger.py` cambia il comportamento eseguibile. I runner ereditano il controllo
attraverso gli ingressi comuni, prima di interrogare il server o scrivere output.

1. `_closed_outcome` valida l’evento persistito e il suo `records_sha256`, poi riusa
   `_validate_outcome` per copertura, identità, raw/record, digest e criteri di esito.
2. `_successful` applica tale validazione dopo i prerequisiti ricorsivi. Il replay di un
   binding già chiuso verifica anche il proprio esito; un matching hash non salta le prove.
3. `_validate_attempts` confronta ogni tentativo con il piano, inclusi gli antenati retry:
   collegamenti, identità, stage_run e prova zero-token. Rileva tentativi orfani.
4. `_frozen` autentica anche i byte frozen persistiti. La sonda conserva il contratto del
   primo gruppo riuscito: 3/6/9 basi legittime; un prefisso residuo dopo perdita di record
   non riconferma l’artefatto della chiusura precedente.
5. `_evaluated_record` verifica nuovamente identità della richiesta/prompt e hash raw/record.
   I controlli di chiusura e conferma condividono una connessione `BEGIN IMMEDIATE`.

Non vengono aggiunti cache fra transazioni, migrazioni, nuovi invii, riparazioni automatiche,
riscritture di eventi o azzeramenti. `event`, `binding`, `request` e `snapshot` restano
letture forensi; non dichiarano la validità normativa. `stage_records` continua a rilevare
dati incoerenti. FAIL/BLOCKED vengono riconfermati secondo i requisiti della loro chiusura;
`verify_stage_success` richiede sempre PASS. I record C02 rimangono INVALID, non risposte.

## Risultati delle prove

| Prova | Risultato |
| --- | --- |
| Mirati finali | **111/111**, zero failure/errori |
| Discovery finale | **146/146**, zero failure/errori |
| Nuove regressioni D02 | **8/8**, già incluse nei due totali |
| Originali applicabili | **14/14**: 12 letterali e due adattamenti fixture/argomento preesistenti |
| Z01–Z05 sul respinto | Cinque metodi, **tre failure D02**, zero errori |
| Z01–Z05 sul nuovo codice, script identico | **5/5** |
| Y01–Y07 letterali | **7/7**; D01/C02/C03 preservati |
| X01–X18 letterali | **18/18** |
| X19–X24 letterali | Cinque PASS, una failure X23 obsoleta, zero errori |
| X23 già adattato | **1/1**, nessun nuovo adattamento |
| Guardiano documentale | **NON PASS**: 35 test, stessi 14 identificativi falliti, 1 skip, zero errori |
| Sintassi | 92 file Python live, zero errori |
| Perimetro protetto | 175 file confrontati byte per byte con la base, invariati |

Le suite si sovrappongono e non si sommano. I precedenti 103/138 restano i conteggi della
revisione edb37f3, ora aumentati di otto. Le 50 corrispondenze nominative sono conservate
nella [matrice acquisita](non_ok_edb37f3_20260915/files/MATRICE_50_METODI.md); non si dichiara
50/50 letterali. [Matrice corrente R01–R10/D02](MATRICE_R01_R10_D02.md) lega il delta ai test.
Il consolidamento X è 23 letterali + il solo X23 già adattato, non 24/24 sul file immutato.

Le otto regressioni aggiunte coprono raw/record corrotti, copertura/risposte/valutazioni
mancanti, prefisso sonda ridotto, artefatti/frozen incoerenti, retry con antenato mancante,
remediation, nuovi ingressi e runner/CLI --resume. Il positivo con retry conserva nove
intenti; i quattro ingressi di conferma sono controllati con un processo SQLite realmente
concorrente durante la lettura del predecessore. Il runner conserva 139 intenti e i file,
con zero nuovi invii/interrogazioni server dopo il fault. Le regressioni D01 conservano
le fixture legacy generate dal vecchio codice 0c8157f e i replay leciti con/ senza alternativo.

[RESULTS.json](d02_evidence/RESULTS.json), [comandi](d02_evidence/COMANDI.md),
[inventario riproduzioni](d02_evidence/REPRODUCTION_INVENTORY.json) e
[impronte](d02_evidence/SHA256SUMS) conservano log completi e provenienza:
44 copie byte-identiche e 1797 file di fixture esterni,
tutti recuperabili e verificati. Le fixture grandi non vengono replicate in Git.

Gli inconvenienti di setup sono separati in [setup_notes.json](d02_evidence/setup_notes.json):
chiave dimensione del precedente manifest corretta prima delle scritture; prova preliminare
29/29 con 21 TestCase importati oltre agli otto nuovi, import corretto prima delle suite finali;
X23 inizialmente privo del modulo sibling, poi copiato byte-identico e rieseguito senza cambiare
assertion. Le sole whitespace preesistenti nei file acquisiti/log restano preservate.
Nessun errore di setup è contato come difetto o come PASS del candidato.

## Modello, letture e limiti

Task preparatore `01a0a204-abda-7a00-8466-f52f5bc84812`, modello **gpt-6-astra**, effort
**xhigh**, osservati nel turn_context locale; Python/SQLite e fonte in
[runtime.json](d02_evidence/runtime.json). Il precedente revisore usa una finestra distinta
`01a0a1ec-35a4-7870-9c39-9bf922d36c85`, stesso modello, effort high. Diversità di modello
assente; non si rivendica indipendenza per le prove di implementazione. Nessuna delega.

Letti mandato, MAINTENANCE, prompt pertinenti, verbale autonomo completo, script e log/JSON
pertinenti, contratto, ledger e fixture/test; ordine di grandezza alcune centinaia di kB,
con verifica meccanica dei file voluminosi. Nessuna nuova lettura/audit scientifico o di
letteratura, nessun download di dati o qualifica dei servizi.

La principale e gli otto source/candidati precedenti vengono confrontati con lo stato
iniziale in DELIVERY_AUDIT_D02.json. Il solo runtime modificato è ledger.py; metric_adapter.py,
metrics.py, test_metric_raccordo.py e i runner/criteri C02/C03 rimangono byte-identici.
Piano generale e rev.10, APERTURA, record D9, walkthrough, A/B, FAR, U3 e freeze restano nel
loro perimetro, senza importare modifiche parallele.

D9 è già decisa: 122B producer principale e consumer; 27B alternativo con libreria completa
16 insight; Terra storico interno. Il recepimento eseguibile D9, l’ordine label reale e le
qualificazioni servizi/tokenizer/identità/capienza/T5 restano separati. Il preflight storico
rimane bloccato. Nessun freeze, GO, push, merge, tag, API provider, inferenza o simulazione.
Non si rivendica protezione crittografica da riscrittura coerente arbitraria dell’intero
ledger e delle impronte. Serve la verifica indipendente del nuovo commit/tree esatti.

## File del commit tecnico (52)

- `studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md`
- `studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json`
- `studio2/fase03/harness/MATRICE_R01_R10_D02.md`
- `studio2/fase03/harness/d02_evidence/COMANDI.md`
- `studio2/fase03/harness/d02_evidence/REPRODUCTION_INVENTORY.json`
- `studio2/fase03/harness/d02_evidence/RESULTS.json`
- `studio2/fase03/harness/d02_evidence/SHA256SUMS`
- `studio2/fase03/harness/d02_evidence/after/console.log`
- `studio2/fase03/harness/d02_evidence/after/evidence/chain_probes.json`
- `studio2/fase03/harness/d02_evidence/after/evidence/chain_probes.log`
- `studio2/fase03/harness/d02_evidence/after/evidence/chain_probes.py`
- `studio2/fase03/harness/d02_evidence/applicable.console.log`
- `studio2/fase03/harness/d02_evidence/applicable/applicable.json`
- `studio2/fase03/harness/d02_evidence/applicable/applicable.log`
- `studio2/fase03/harness/d02_evidence/applicable/evidence/negative_probes.py`
- `studio2/fase03/harness/d02_evidence/before/console.log`
- `studio2/fase03/harness/d02_evidence/before/evidence/chain_probes.json`
- `studio2/fase03/harness/d02_evidence/before/evidence/chain_probes.log`
- `studio2/fase03/harness/d02_evidence/before/evidence/chain_probes.py`
- `studio2/fase03/harness/d02_evidence/compile.json`
- `studio2/fase03/harness/d02_evidence/d02.log`
- `studio2/fase03/harness/d02_evidence/discovery.log`
- `studio2/fase03/harness/d02_evidence/documentation_after.log`
- `studio2/fase03/harness/d02_evidence/documentation_before.log`
- `studio2/fase03/harness/d02_evidence/documentation_comparison.json`
- `studio2/fase03/harness/d02_evidence/extension_commands.json`
- `studio2/fase03/harness/d02_evidence/literal/additional_edges.py.console.log`
- `studio2/fase03/harness/d02_evidence/literal/evidence/additional_edges.py`
- `studio2/fase03/harness/d02_evidence/literal/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d02_evidence/literal/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d02_evidence/literal/evidence/extended.json`
- `studio2/fase03/harness/d02_evidence/literal/evidence/extended.log`
- `studio2/fase03/harness/d02_evidence/literal/evidence/extended_probes.py`
- `studio2/fase03/harness/d02_evidence/literal/extended_probes.py.console.log`
- `studio2/fase03/harness/d02_evidence/run_extensions.py`
- `studio2/fase03/harness/d02_evidence/runtime.json`
- `studio2/fase03/harness/d02_evidence/scope.json`
- `studio2/fase03/harness/d02_evidence/scope_audit.py`
- `studio2/fase03/harness/d02_evidence/setup_notes.json`
- `studio2/fase03/harness/d02_evidence/targeted.log`
- `studio2/fase03/harness/d02_evidence/x23_adapted/additional_edges.py.console.log`
- `studio2/fase03/harness/d02_evidence/x23_adapted/evidence/additional_edges.py`
- `studio2/fase03/harness/d02_evidence/x23_adapted/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d02_evidence/x23_adapted/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d02_evidence/x23_adapted/evidence/extended_probes.py`
- `studio2/fase03/harness/d02_evidence/x23_adapted/setup_missing_dependency.log`
- `studio2/fase03/harness/d02_evidence/y_original/edge_probes.py.console.log`
- `studio2/fase03/harness/d02_evidence/y_original/evidence/edge_probes.json`
- `studio2/fase03/harness/d02_evidence/y_original/evidence/edge_probes.log`
- `studio2/fase03/harness/d02_evidence/y_original/evidence/edge_probes.py`
- `studio2/fase03/harness/ledger.py`
- `studio2/fase03/harness/test_d02_predecessors.py`
