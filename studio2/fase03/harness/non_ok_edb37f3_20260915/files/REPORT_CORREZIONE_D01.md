# Correzione del residuo D01 / C01 / R04 — candidato locale

15 settembre 2026. **Implementazione da sottoporre a nuova review indipendente.**
Il replay degli esiti ora verifica anche la catena dei predecessori. Le due riproduzioni
Y01/Y02 prima fallite passano senza modificare lo script del revisore. C02/C03 restano
invariati nei file di esecuzione pertinenti e nelle prove rieseguite. Il NON OK sul
candidato precedente resta il verdetto acquisito; nessun freeze o GO viene dichiarato.

## Identità e commit

| Ruolo | Identità |
| --- | --- |
| Remoto effettivo | `https://github.com/sorrentinoluca/fot-phd.git` |
| main remoto prima del lavoro | `a00605862f627710347bd63c49f79a6d0a00135f` |
| Respinto | `9e18bcbd06fa2c54202c8eeda079c112dbfcefcd` |
| Tree respinto | `5d1fd7924c4e1e46346f367590e6aa1977a6ba75` |
| Base documentale nuova | `52e13e1ed540e1ad076474398bf850445c9a4a00` |
| Acquisizione separata | `89b016a728bdbf5d2d8b438416e6133b050683da` |
| **Candidato tecnico** | **`edb37f359f29c461c5a507c1027c4bf411654130`** |
| **Tree tecnico** | **`56d98666e1d18c7958ac8d3631ae6d5b8ec04bf9`** |
| Branch | `codex/studio2-harness-0310-d01` |
| Worktree isolato | `/Users/luker/fot-tep-harness-0310-d01` |
| Manifest v4 | 62 file diretti, 15815 byte |
| SHA-256 manifest | `c823cb669fb408080b46311e6c753be4b5243764d76e88ed67273f3c213c4fd8` |

Il worktree era **pulito dopo il commit tecnico**, prima di questo report. Report,
prompt, consegna JSON e audit appartengono a un **successore documentale**: il suo HEAD
non deve essere eseguito al posto del candidato tecnico. L'identità del successore è
ricavabile dal commit che contiene i documenti; non è scritta autoreferenzialmente qui.
Stati delle copie preservate e controllo finale del remoto sono nel DELIVERY_AUDIT_D01.json.

## Acquisizione e riproduzione

Fonte: `/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence`.
Acquisiti [verbale](non_ok_9e18bcb_20260915/evidence/VERIFICA_C01_C03.md), matrici, script,
log e tutte le nuove fixture Y01–Y07. SHA-256 verbale
`35e047834ec957a8008db7b82c375d3022cbcfeb7a8d2fb80143f44e9cabfe42`;
manifest `29385ea6589286e7a551c13ee61c8588b7b5792dabba7fa5d3ebebcd090a34ea`.

Verificati prima dell'uso e prima del commit **1.788 membri più il manifest**. **171 copie
byte-identiche**, **1.618 file esterni** recuperabili; inventario di percorsi, hash,
dimensioni, motivi e symlink in
[ACQUISITION_INVENTORY.json](non_ok_9e18bcb_20260915/ACQUISITION_INVENTORY.json).
Il commit di acquisizione ha 175 file includendo i quattro documenti di provenienza,
inventario/stato iniziale e script. I duplicati delle vecchie fixture N/X restano esterni;
non si riscrivono path, newline o whitespace delle prove.

Lo stesso `edge_probes.py` è eseguito in due sandbox nuovi, con il candidato esplicito:

| Codice eseguito | Y01–Y07 | Osservazione Y01/Y02 |
| --- | --- | --- |
| 9e18bcb respinto | 5 PASS, **2 failure**, 0 errori | Gate irregolare riconfermato; nessuna eccezione; 132 intenti |
| Nuovo candidato | **7/7**, 0 failure/errori | Rifiuto `alternate_conformity has no successful closed outcome`; 132 intenti conservati |

Y01 costruisce l'intera pipeline con il vecchio **0c8157f** in un subprocess e la riapre
col codice nuovo; Y02 usa le API ledger. Sono due prove dello stesso D01. Non si modifica
via SQL il ledger per costruire quel difetto, né si usa un errore di dipendenza come prova.
Il vecchio codice è letto da un checkout esatto e pulito; tutti i trasporti sono stub.

## Modifica eseguita

Il **solo file live di esecuzione modificato è `harness/ledger.py`**.

- `_prerequisites` separa i controlli della catena dai vincoli propri delle nuove
  transizioni. Verifica sospensione, autorizzazione remediation, alternativo avviato,
  producer attivo e sonda; `_successful` lo applica ricorsivamente ai risultati riutilizzati.
- Il binding identico verifica i prerequisiti prima di ritornare. Il replay dello stesso
  hash/outcome verifica predecessori, copertura, record durevoli e criteri dello stadio;
  soltanto dopo può rigenerare file, senza creare eventi o richieste nuovi.
- `verify_stage_success` e `authenticate_frozen` verificano dentro una sola transazione
  `BEGIN IMMEDIATE`. L'autenticazione del freeze richiede anche il successo conforme della
  sonda. Le verifiche non osservano letture intercalate da uno scrittore concorrente.
- `_ready` mantiene i limiti delle mutazioni: niente riapertura di stadi o ritorno al
  producer dopo la sonda. Il riuso valido di un producer/sonda già chiuso resta possibile
  anche dopo il gate; non è una nuova transizione.

Un alternativo bound, INTENT, FAILED, ZERO_TOKEN_PROVEN, completato senza outcome o FAIL
impedisce la riconferma di sonda/gate, anche se un vecchio ledger v2 ne conserva PASS.
Il rifiuto precede interrogazioni del server, nuovi invii e rigenerazione degli artefatti
nei runner e nelle CLI. Database logico e byte dei file finali restano invariati nelle prove.

Le letture `event`, `binding`, `request`, `stage_records`, `snapshot` restano disponibili
per l'ispezione forense. Un evento storico PASS può essere letto come dato senza diventare
una conferma di validità. Non si elimina la storia né si migra lo schema v2. Una catena
storica valida con alternativo assente o PASS è ancora accettata; il replay conserva anche
l'invalidità C02 e il ciclo di remediation valido.

## Verifiche

| Controllo | Esito |
| --- | --- |
| Sette nuove regressioni D01 | **7/7** |
| Mirati completi | **103/103** = 96 precedenti + 7 nuove |
| Discovery completa | **138/138** = 131 precedenti + 7 nuove |
| Originali applicabili | **14/14**: 12 letterali, 2 con i precedenti adattamenti fixture/argomento |
| Y01–Y07 del revisore | **7/7**, script byte-identico |
| Estensioni X | **23 letterali + X23 adattato**, tutti conformi nei termini già verificati dal revisore |
| X23 letterale | La **failure obsoleta resta nel log**; non viene dichiarato 24/24 sul file immutato |
| Compilazione live | **91 sorgenti**, nessun errore, esclusi alberi forensi |
| Perimetro protetto | **174 file byte-identici** alla base documentale |
| Guardiano documentale | **NON PASS: 35 test, stessi 14 ID falliti, 1 skip**, nessun peggioramento |

Le suite si sovrappongono. Le sette nuove regressioni sono già nei 103 e 138; gli assert
sui sei stati × sette ingressi non vengono dichiarati 42 metodi distinti. La matrice
[MATRICE_R01_R10_D01.md](MATRICE_R01_R10_D01.md) collega ogni metodo alla proprietà testata
e mantiene il rimando nominativo ai 50 metodi originari acquisiti integralmente.

Le nuove regressioni comprendono:

1. tutti i sei stati alternativi non conformi sui sette ingressi di conferma;
2. controlli positivi storici, con e senza alternativo, e divieto di riaprire richieste;
3. runner e CLI budget/stability reali su fixture legacy: zero invii e interrogazioni server,
   stesso database logico e stessi byte degli artefatti dopo il rifiuto;
4. rigenerazione del summary mancante per un vecchio gate valido, senza invio;
5. replay dopo remediation valida con un INVALID C02, conservando contatori e zero retry;
6. rifiuto di raw deliberatamente alterato in una fixture distinta anche con hash outcome uguale;
7. due ingressi di conferma che escludono uno scrittore concorrente reale fino al rilascio
   della transazione.

I processi legacy verificano HEAD/tree/pulizia di 0c8157f. C02/C03 sono nuovamente coperti
dalle suite e da Y03–Y07. I relativi runtime, gate_rules, producer_probe e run_pilot sono
byte-identici; il raccordo qualificato mantiene intatti i tre file e i suoi nove test.

Un primo audit locale di perimetro aveva confrontato la base documentale con la lista dei
soli file della correzione, incontrando così anche l'acquisizione autorizzata. È stato
fermato prima dei confronti protetti, poi corretto separando le due basi. Il fatto è
registrato in `d01_evidence/scope_initial_issue.json`; non è un difetto candidato o un test
comportamentale fallito. I controlli finali di scope/compilazione sono completi.

## Prove conservate e confini

[d01_evidence/COMANDI.md](d01_evidence/COMANDI.md) documenta i comandi e i sandbox.
**41 file** di script/log/osservazioni copiati byte-identici, **1.852 file** di fixture
esterni, tutti verificati per dimensioni e hash nell'inventario. I tre file aggiuntivi
RESULTS, REPRODUCTION_INVENTORY e SHA256SUMS portano a **44 file di prove tracciati**.
Radice esterna recuperabile: `/Users/luker/fot-tep-harness-0310-d01-checks`.

Verificati prima del commit tecnico 62 file diretti del manifest, tutti i membri del
manifest nuove prove, 1.789 originali/copie/esterni dell'acquisizione e 1.893 file della
riproduzione. Questi sono conteggi di integrità, non nuovi metodi di test. Le fixture
sono deliberatamente sintetiche o alterate; non sono fonti o approvazioni scientifiche.

Nessuna modifica a piano generale/statistico, APERTURA, D9, walkthrough, 03.7/03.9/03.12,
A/B, FAR o U3. Nessun lavoro parallelo importato. Principale, tre sorgenti precedenti e
candidati delle review sono preservati, con stati prima/dopo nell'audit documentale.
Nessun push, merge, tag, freeze, GO, API provider, inferenza o simulazione scientifica.

## Finestra e seguito

Preparatrice: task `01a0a204-abda-7a00-8466-f52f5bc84812`, **gpt-6-astra, effort xhigh**.
I metadati `session_meta`/`turn_context` del turno corrente sono stati riletti dal rollout
locale dopo il commit tecnico e riportati nel successore `DELIVERY_AUDIT_D01.json`.
Il file runtime nel manifest tecnico registra lo stato conoscitivo precedente a tale
lettura; non è stato riscritto retroattivamente. La review acquisita attesta una finestra
distinta, stesso modello gpt-6-astra con effort high. Non è indipendenza fra modelli e
questi controlli della preparatrice non costituiscono una review indipendente.

D9 è già approvata: 122B producer principale e consumer; 27B producer alternativo per la
libreria completa di 16 insight; Terra storico interno. Il recepimento eseguibile D9,
l'ordine reale delle label, gli insight reali e le qualifiche servizio/tokenizer/T5 restano
separati. Il preflight storico non è abilitato. Nessuna riapprovazione dei ruoli richiesta.

Passo successivo: [PROMPT_VERIFICA_D01.md](PROMPT_VERIFICA_D01.md), nuova finestra e candidato
tecnico esatto. Il NON OK non viene autonomamente chiuso da questa implementazione.

## Perimetro esatto del commit tecnico

**49 file**: un runtime modificato, un nuovo modulo di test, tre documenti/manifest,
44 file di prove e inventari. Acquisizione di 175 file nel commit precedente; successore
documentale di quattro file distinto. Ogni file tecnico:

- `studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md`
- `studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json`
- `studio2/fase03/harness/MATRICE_R01_R10_D01.md`
- `studio2/fase03/harness/d01_evidence/COMANDI.md`
- `studio2/fase03/harness/d01_evidence/REPRODUCTION_INVENTORY.json`
- `studio2/fase03/harness/d01_evidence/RESULTS.json`
- `studio2/fase03/harness/d01_evidence/SHA256SUMS`
- `studio2/fase03/harness/d01_evidence/acquire.py`
- `studio2/fase03/harness/d01_evidence/after/console.log`
- `studio2/fase03/harness/d01_evidence/after/evidence/edge_probes.json`
- `studio2/fase03/harness/d01_evidence/after/evidence/edge_probes.log`
- `studio2/fase03/harness/d01_evidence/after/evidence/edge_probes.py`
- `studio2/fase03/harness/d01_evidence/applicable/applicable.json`
- `studio2/fase03/harness/d01_evidence/applicable/applicable.log`
- `studio2/fase03/harness/d01_evidence/applicable/evidence/negative_probes.py`
- `studio2/fase03/harness/d01_evidence/applicable_console.log`
- `studio2/fase03/harness/d01_evidence/before/console.log`
- `studio2/fase03/harness/d01_evidence/before/evidence/edge_probes.json`
- `studio2/fase03/harness/d01_evidence/before/evidence/edge_probes.log`
- `studio2/fase03/harness/d01_evidence/before/evidence/edge_probes.py`
- `studio2/fase03/harness/d01_evidence/compile.json`
- `studio2/fase03/harness/d01_evidence/d01.log`
- `studio2/fase03/harness/d01_evidence/discovery.log`
- `studio2/fase03/harness/d01_evidence/documentation_after.log`
- `studio2/fase03/harness/d01_evidence/documentation_before.log`
- `studio2/fase03/harness/d01_evidence/documentation_comparison.json`
- `studio2/fase03/harness/d01_evidence/literal/additional_console.log`
- `studio2/fase03/harness/d01_evidence/literal/evidence/additional_edges.py`
- `studio2/fase03/harness/d01_evidence/literal/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d01_evidence/literal/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d01_evidence/literal/evidence/extended.json`
- `studio2/fase03/harness/d01_evidence/literal/evidence/extended.log`
- `studio2/fase03/harness/d01_evidence/literal/evidence/extended_probes.py`
- `studio2/fase03/harness/d01_evidence/literal/extended_console.log`
- `studio2/fase03/harness/d01_evidence/package_evidence.py`
- `studio2/fase03/harness/d01_evidence/runtime.json`
- `studio2/fase03/harness/d01_evidence/scope.json`
- `studio2/fase03/harness/d01_evidence/scope_audit.py`
- `studio2/fase03/harness/d01_evidence/scope_initial_issue.json`
- `studio2/fase03/harness/d01_evidence/targeted.log`
- `studio2/fase03/harness/d01_evidence/update_manifest.py`
- `studio2/fase03/harness/d01_evidence/worktrees_before.txt`
- `studio2/fase03/harness/d01_evidence/x23_adapted/console.log`
- `studio2/fase03/harness/d01_evidence/x23_adapted/evidence/additional_edges.py`
- `studio2/fase03/harness/d01_evidence/x23_adapted/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d01_evidence/x23_adapted/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d01_evidence/x23_adapted/evidence/extended_probes.py`
- `studio2/fase03/harness/ledger.py`
- `studio2/fase03/harness/test_d01_replay.py`
