VERDETTO: NON OK — limitato al candidato offline 59b6b93cd9c215e8b687e540f7cd579804b7c66a.

# Verifica indipendente dell’harness offline 03.10 — Studio 2 FoT-TEP

Verbale autonomo del 15 settembre 2026, Europe/Rome; attività iniziata il 14 settembre. Nessuna correzione del candidato. I risultati positivi delle suite consegnate sono riprodotti, ma non coprono i difetti di integrazione, persistenza e controllo degli stadi descritti sotto. Non è una verifica scientifica dei servizi o dei risultati dello studio.

## 1. Identità, indipendenza e isolamento

| Voce | Riscontro |
| --- | --- |
| Revisore | Codex, modello runtime **gpt-6-astra**, effort **high** |
| Sessione del revisore | **01a0a1ec-35a4-7870-9c39-9bf922d36c85**, task «Verifica harness offline 03.10», agente `/root` |
| Preparazione | Task «3.10», sessione **01a0a1c3-4692-7e23-a478-48045278950a**, modello **gpt-5.6-sol**, effort **high** |
| Prova runtime | `session_meta` e `turn_context` dei rollout locali; estratti limitati ai metadati in `initial_identity.json` e `preparer_runtime_metadata.json`. Modello ed effort sono valori registrati dal runtime; non si inferiscono pesi effettivi, routing interno o budget non esposti. Nessun sottoagente impiegato. |
| Candidato tecnico | `59b6b93cd9c215e8b687e540f7cd579804b7c66a` |
| Tree tecnico | `cf08c14a8deb18145189afbe9722d7da46bc2f82` |
| Parent immediato | `f2f5c5c13edb8251b8dc4fc764bd098d2206b7b8` |
| Base del delta | `a00605862f627710347bd63c49f79a6d0a00135f`; è un antenato, non il parent immediato |
| Consegna successiva | `288dc1926bfd7ab4ce43bb4377a9a0064313ad69`, tree `833c10f98f79b203cec385ff1aec0437b679bcc5`; cambia soltanto rapporto e prompt, 7 inserimenti/7 rimozioni. Letta come consegna, esclusa dal candidato tecnico. |
| Copia verificata | `/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate`, clone locale con oggetti condivisi in sola lettura, **detached HEAD pulito** sul candidato |
| Verbale e prove | `/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence`, cartella sorella esterna al tree candidato |
| Sorgente recupero | `/Users/luker/fot-tep/.worktrees/studio2-harness`, branch `codex/studio2-harness`, commit `1ac06ebdc92f73d3b630ccca9bf75f413bea170b` |
| Worktree consegna | `/Users/luker/fot-tep-harness-0310-offline`, branch `codex/studio2-harness-0310-offline`, HEAD `288dc192…`, pulito prima e dopo |
| Copia principale | `/Users/luker/fot-tep`, branch `codex/studio2-soglie-normal`, HEAD `819b12e97fb94d501032655ec2f226139e6c5ca5`; contenuti non tracciati preesistenti preservati |
| Remoto effettivo | `https://github.com/sorrentinoluca/fot-phd.git`, `refs/heads/main` verificato con `git ls-remote` prima delle scritture e a fine prove: **a00605862f627710347bd63c49f79a6d0a00135f** |

La copia isolata conserva come `origin` il percorso locale `/Users/luker/fot-tep`: il suo `origin/main=4f98a297…` fotografa il branch locale `main` del repository clonato e **non rappresenta il main GitHub**. Tutte le verifiche normative usano commit completi; il remoto GitHub è interrogato esplicitamente. Nessun fetch o checkout di modifiche parallele, nessun commit, tag, push, merge o integrazione.

Le regole lette sono `docs/MAINTENANCE.md` nella copia principale richiesta e nel candidato, `docs/prompts/Verifica_LLM.md` e l’instradamento pertinente di `Prompt_LLM.md`. Applicate preservazione degli artefatti congelati, fonti esatte, distinzione preparazione/verifica/documentazione e verbale fuori dal contenuto verificato secondo l’istruzione specifica dell’autore. Il contratto del candidato aggiunge rispetto alla copia principale le restrizioni sul codice congelato del primo studio; anche queste sono rispettate.

## 2. Fonti primarie e impronte

Letture normative: prompt e rapporto della consegna `288dc192…`; manifest interno del candidato; handoff rev02 pubblicato e conservato nella base; pubblicazioni successive di raccordo metriche, schema R4 e baseline 03.9 presenti nella base; §§10–11 e rinvii pertinenti del piano rev.10, relativo manifest e delta a `6aaa5b3e…`; `CONSEGNA_REV10.md` al commit documentale esatto `dac458609a642bb317bc48b8c2d000a340e163ed`; contratto/schema/validatore R4 a `3c64390…`; manifest baseline rev.3/rev.5 e handoff Normal; nove moduli del package originario letti a `1ac06eb…`. Non sono recepite le correzioni parallele 03.8 o D9. Nessuna nuova lettura bibliografica o di dati test/OOD.

| Artefatto | SHA-256 ricalcolato |
| --- | --- |
| Manifest harness candidato | `751b95a8bce62c4f8acbf907ba1cbfcf01850538711ae9dfe6928f62ebd430d3` |
| Piano rev.10 | `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` |
| `PIANO_STATISTICO_FREEZE.json` rev.10 | `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8` |
| Delta harness rev.10 | `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`; blob `780e08ae9e176a819a745ab2054a2e6ae79a8a9a` |
| Manifest R4 | `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12` |
| Validatore R4 | `cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508` |
| Handoff Normal | `e2409c64ad4e36e0f3b597a5e0b9745d866af72f4da717fc7a128b25753c166a` |
| Baseline rev.3, pin del raccordo | `0312f416dfdbaf8984b2063df2c2e9d00e1737321b9a65dd7e32b0295a937ec8` |
| Baseline rev.5, efficacia successiva | `c52c7231021f52fc7b60b3b55eb67b5205854176395eb809db4d20227978b7cc` |
| Pseudolabel | `b0ce81d53f11038ddf51c9ec964a1e838a7045e2e57b8ac3368f05e9a215bbc6` |
| Assignment | `df7434230dcd1d5460cd19e0d27e909efd40289f64d89a4b3fee2a0e55b79fcf` |
| Derangement | `34350c7e49b11d29b885da128d4b34ce3df31cd41df7c521cb66421aa1b9d001` |
| Evidence manifest / evaluator index | `5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020` / `b966cdd3d579efaf595fd48c4b9baa70747ba584522926520840a1e914dbf69c` |
| Archivio evidence v2, 62.185.472 byte | `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf` |

Tag verificati sia localmente sia sul remoto, oggetto annotato **e** peeled:

| Tag | Oggetto | Peeled |
| --- | --- | --- |
| `studio2-fase03-schema-insight-frozen-001` | `4d15c4fb915ea9db9f7425225d231746778f0ba1` | `3c64390bc4dd58c48cc4e1e388a38989b32b3143` |
| `studio2-fase03-baseline-numerica-frozen-001` | `124262f5a6172a20965d019f220ff93954284922` | `38cb5f5eaa2e5a7dddfd53564a7d020b6b50fa1e` |
| `studio2-fase03-pseudolabel-frozen-001` | `6854c49b4034c16b8df3b11d45dd759a343463e2` | `c16b533016db4617deb1ba96853253f117e8e32b` |

`check_integrity.py` produce **1.364 riscontri, zero difformità**: 21 file candidati con hash/dimensioni, 9 confronti di recupero, 18 membri del manifest R4 alle rispettive fonti storiche, 17 pin/catene baseline, 4 pin input, 3 file metriche invariati, 3 pin rev.10, 3 tag, manifest harness, archivio, 1.283 membri scientifici dell’archivio e ricostruzione dell’inventario.

`guards.py`, `logging_v1.py`, `producer.py`, `sampling.py` sono byte-identici alla sorgente. `canary.py`, `inputs.py`, `insight_adapter.py`, `ordering.py`, `render.py` sono adattati; i nove diff sono conservati in `recovery_*.diff`. Non sono ripristinati vecchi `HARNESS_FREEZE.json`, `INTEGRATION_STATUS.json` o report del package. Il delta di 24 percorsi resta nella fase03: non modifica piano 03.8, APERTURA, walkthrough, `metric_adapter.py`, `metrics.py` o `test_metric_raccordo.py`.

L’archivio è la copia locale già esistente in `/private/tmp/fot-tep-evidence-v2-redownload-curl-001/studio2-fase03-evidence-v2.tar`: ne sono ricalcolati hash, 1.283 percorsi, dimensioni e contenuti; i byte verificati sono conservati in `evidence/reference/`. Non è stato effettuato un nuovo download e non si presenta questa prova come nuova verifica di recuperabilità remota secondo §8.5. La pubblicazione e il precedente riscaricamento restano attestati dai record storici esatti. Non è una nuova produzione di evidence.

La ricostruzione dell’inventario dai byte verificati coincide con il candidato: **320** finestre fault development, **16** esempi fault locali, **8** Normal, **16** contratti; `INCOMPLETE`, unico requisito mancante `16 real schema-valid producer insights`, nessun manifest eseguibile risultante in assenza di handoff insight. Non sono stati prodotti insight scientifici.

## 3. Prove eseguite e ambiente

Comandi dal percorso assoluto della copia `candidate`:

```text
python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol
/opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
python3 -m compileall -q studio2/fase03
git diff --check a00605862f627710347bd63c49f79a6d0a00135f..59b6b93cd9c215e8b687e540f7cd579804b7c66a
python3 docs/test_explanation.py
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 ../evidence/check_integrity.py
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 ../evidence/negative_probes.py
```

Il launcher `run_baseline_checks.py` registra comandi, tempi, return code e log completi; `PYTHONPYCACHEPREFIX` dirige la compilazione fuori dal candidato. La suite indipendente disabilita `socket.socket`; l’SDK e il trasporto sono sostituiti da oggetti stub in memoria. I conti token fittizi verificano esclusivamente flusso e contratti: nessuna inferenza, simulazione scientifica, chiamata API o qualifica della capienza. Il test del limite 200 prepopola esplicitamente una **fixture SQLite sacrificabile** con intenti storici; non dimostra raggiungibilità del 200 tramite quote normali.

| Verifica | Esito |
| --- | --- |
| Suite mirata consegnata | **45/45 OK**, inclusi 9 test del raccordo metriche |
| Discovery Fase03 | **80/80 OK** |
| Compilazione e diff check | OK |
| Guardiano documentale | 35 test, **14 fallimenti storici**, 1 skip, 0 errori; corrispondono al riferimento dichiarato. Documentazione e test non cambiano fra base e candidato. |
| Integrità | **1.364/1.364 riscontri conformi** |
| Prove indipendenti aggiuntive | **50 metodi**, 18 soddisfano il requisito, **32 lo smentiscono**; unittest registra 34 failure perché un metodo contiene 3 sottocasi, **0 errori**. Questi numeri non equivalgono a 34 difetti distinti: i rilievi sono raggruppati sotto. |

Il `python3` di sistema è `/usr/local/bin/python3`, 3.11.5 x86_64, SQLite 3.42.0. La prima esecuzione aggiuntiva incontrava il modulo `rpds` arm64 incompatibile e quindi non consentiva validazione R4 reale: log conservati separatamente come `initial_system_python_negative_probes.*`, **non usati per classificare i difetti del candidato**. Le prove definitive impiegano `/opt/anaconda3/bin/python3`, **3.13.9 arm64**, SQLite 3.51.0, senza errori di dipendenza. Il 45/45 su Python di sistema non esercita la validazione completa di una coppia R4; perciò non intercettava tale differenza d’ambiente.

## 4. Rilievi riproducibili

Priorità: **P1** = blocca la qualifica offline del percorso di esecuzione; **P2** = controllo contrattuale incompleto che consente un risultato tecnico improprio. Tutti i riferimenti codice sono relativi al candidato esatto; i link puntano alla sua copia pulita. I nomi `test_NN_*` rimandano a `negative_probes.py`, log e JSON con le osservazioni. Le prove non alterano codice candidato: patch in memoria soltanto ai confini esterni o alla directory dei risultati.

### R01 — P1: `UNDECIDED` non blocca il consumer storico

In [run_pilot.py:410](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/run_pilot.py:410) il runner carica il preflight e passa direttamente a `server_contract(config)`. [config/pilot_preflight.json:7](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/config/pilot_preflight.json:7) dichiara `UNDECIDED`, ma `candidate` contiene ancora alias `fot-exp2-consumer`, root `Qwen/Qwen3.8-27B-FP8`, endpoint locale e vecchio fingerprint. Il CLI non esige un nuovo provider consumer approvato e non controlla lo stato suspended/D9 prima dell’ingresso nel runner.

**Prova 46:** con `load_prepared` sostituito da fixture e il primo contatto server intercettato prima della rete, il candidato `UNDECIDED` raggiunge proprio quella configurazione storica. Il rifiuto senza provider esplicito esiste nel producer (`provider_config(None)`) ma non assicura la stessa proprietà al consumer. Va introdotto un blocco eseguibile del record storico; questo rilievo non richiede di inserire D9 nel candidato.

### R02 — P1: pin e provenienza verificati nei dati consegnati, ma non imposti lungo tutti gli ingressi

[inputs.py:204](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/inputs.py:204) legge mapping, assignment e derangement senza confrontarli con i pin congelati; più avanti registra l’hash dei byte ricevuti. [inputs.py:161](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/inputs.py:161) usa JSON evidence per costruire i campi fissi senza verificarne `json_sha256`. `_load_evidence` protegge i testi e i due CSV, non quei JSON.

[producer_probe.py:74](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/producer_probe.py:74) accetta gli esempi locali dell’inventario senza ricalcolare provenienza/hash contro le fonti; a [riga 106](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/producer_probe.py:106) carica un tokenizer arbitrario senza invocare le guardie dei byte. R4 è caricato e controllato solo nella validazione **dopo** il trasporto, a riga 160. Un mismatch viene trattato come errore della risposta e il ciclo continua.

**Prove 37–38:** un byte aggiunto a ciascuna fonte 03.7 o ai JSON evidence è accettato. **32/49:** sostituire un esempio locale con testo non verificato lascia passare la conformità e produce una libreria `validated=true` in fixture. **41:** validatore alterato, **8 chiamate stub** prima del FAIL, invece di zero. **33:** `_insights` accetta anche sedici oggetti vuoti purché `validated=true` e hash autoconsistente; tale handoff non prova né origine reale né R4. La presenza di `load_validator`, `verify_files` e `verify_tokenizer` corretti isolatamente non sostituisce il loro collegamento agli ingressi.

Un’ulteriore rottura è [run_pilot.py:313](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/run_pilot.py:313): `load_prepared` verifica piano, prompt e preflight, ma poi rilegge `plan['source_manifest']` per `label_space` senza verificare l’hash già registrato. **47:** la modifica successiva del manifest sorgente passa.

### R03 — P1: separazione label corretta nel renderer nuovo, aggirata dalla pipeline ordinaria

[inputs.py:382](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/inputs.py:382) assegna `displayed` a `executable['label_space']`, sostituendo l’ordine canonico evaluator-side. Contemporaneamente l’inventario resta con `author_decision='pending'`, ma il manifest eseguibile è già marcato `FROZEN_FOR_PHASE03_PRE_GATE`.

[prepare_gate.py:115](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/prepare_gate.py:115) continua a chiamare il vecchio `build_pilot_sample`, senza passare da `build_real_pilot_sample` e quindi senza il controllo dell’approvazione e la validazione R4 integrale del nuovo renderer. Il file `prepare_gate.py` è preesistente, ma è l’ingresso corrente che consuma il manifest del delta.

**35:** la libreria di fixture fa produrre `label_space` nell’ordine 1a, diverso dal file congelato 03.7. **39:** lo stesso percorso produce **40 prompt** con stato `READY_FOR_PRE_GATE_GENERATION_PROBE` mentre l’ordine resta **pending**. **34** e il test consegnato passano soltanto per l’adapter chiamato direttamente. Mapping/assignment/derangement tracciati restano intatti: il difetto è nel manifest risultante e nel percorso di consumo.

### R04 — P1: esiti e transizioni del ledger non sono fail-closed né atomici

[ledger.py:173](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:173) controlla cardinalità e assenza di `INTENT`, poi registra l’evento in una transazione separata. Non distingue `FAILED`, `ZERO_TOKEN_PROVEN` senza retry riuscito e risultati valutabili; `PASS` è un argomento libero. [Righe 250–260](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:250) leggono l’evento di PASS senza ricontrollare richieste irrisolte o chiusura dello stadio precedente.

**04–05:** una conformità con timeout terminale o zero token mai recuperato può ricevere PASS. **06–07:** dopo un PASS ottenuto con retry completato, si può aggiungere un altro retry sul vecchio originale; riaprendo SQLite resta **1 intento irrisolto**, ma parte la sonda. **18:** interposizione deterministica di un writer fra controllo e `record_event` produce lo stesso stato incoerente, dimostrando la finestra di concorrenza senza dipendere dal timing.

**08:** l’API pubblica [record_event:131](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:131) può inserire direttamente `outcome:budget_probe=PASS` su ledger vuoto e consentire il gate. Questa è una prova al confine dell’API del ledger, non una modifica diretta del database né un comportamento del CLI ordinario. Gli eventi normativi devono avere transizioni validate; l’assenza attuale di tale barriera impedisce di qualificare il ledger come macchina a stati autonoma.

### R05 — P1: identità logica e catene di retry aggirabili

L’indice univoco [ledger.py:79](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:79) include `stage_run`. **03:** dopo un intento persistito, stesso `logical_id` con nuovo request ID, producer/alias e `stage_run` è accettato come nuova base. Nei runner `stage_run` dipende da hash di inventario/provider; cambiare questi valori può far consumare base per lo stesso agente anziché obbligare a una ripresa o a un retry tracciato. Il totale non si azzera, ma identità, quota e copertura delle otto chiamate diventano scorrette.

[reserve_transport_retry:328](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:328) verifica lo stato zero-token dell’originale, senza escludere un retry già aperto/riuscito né vincolare tutti i dati della richiesta. **11:** lo stesso originale finanzia due retry contemporaneamente irrisolti. [reserve_probe_transport_triplet:359](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:359) controlla tre logical ID e tre stringhe condition, ma non tre originali distinti e coerenti. **12:** basta un solo originale zero-token ripetuto tre volte con le etichette A/B-LF/E-LF.

L’atomicità SQL e il limite numerico della tripletta sono corretti (**13**), ma non dimostrano che la tripletta rappresenti le tre richieste autorizzate. Serve preservare l’identità logica fra alias/directory/restart e validare la catena dei tentativi.

### R06 — P1: remediation non vincolata a diagnosi, diff, template e stessi otto casi

[ledger.py:142](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:142) verifica la forma di tre hash e la presenza di `FAIL`, senza vincolare la classe diagnosticata. **10:** un timeout senza prova zero token può diventare la premessa di una remediation. **09:** otto richieste riferite alla stessa identità logica, ciascuna con stage_run diverso, soddisfano il conteggio remediation e ricevono PASS.

Nel runner [producer_probe.py:108](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/producer_probe.py:108) il prompt è sempre costruito da `build_producer_prompt`; non esiste confronto con `template_sha256`, `diff_sha256`, casi o contratti del primo ciclo. **45:** approvazione della fixture con template SHA-256 tutto zero, prompt effettivo `ffebfd052f4a12a1ab04442c3fbbe9a04669c9db803c91460ad24faeb770aba7`, e la remediation produce comunque **PASS**. Non c’è acquisizione di approvazione reale: la prova dimostra esclusivamente che il codice non lega l’artefatto registrato ai byte usati.

Sono verificati il massimo 8, l’unicità dell’evento di autorizzazione e il rifiuto dopo sonda/gate; mancano le proprietà qualitative della remediation prescritta. Gli output iniziali sono separati per nome, ma l’handoff insight non lega una libreria al ciclo attivo del ledger e non impedisce di presentare una precedente libreria autocertificata.

### R07 — P1: contatore durevole, raw volatili e ripresa dei runner incompleta

[producer_probe.py:121](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/producer_probe.py:121), [run_pilot.py:419](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/run_pilot.py:419) e [run_pilot.py:636](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/run_pilot.py:636) accumulano record in memoria e scrivono il JSONL solo alla fine dello stadio. Il logger append/fsync recuperato non viene usato dai runner.

**43:** successo producer al primo invio e timeout al secondo lasciano **2 richieste conteggiate e nessun file raw**. **44:** il riavvio riparte dall’agente 1 e si ferma con `duplicate request or logical attempt`. **50:** crash dopo il primo esito di sonda, secondo intento persistito: contatore sonda 2, unresolved 1, nessun raw. **51:** analogo nel gate: contatore gate 2, unresolved 1, solo configurazione congelata, nessun raw.

**01** prova con processo reale e `os._exit(23)` che l’intento SQLite sopravvive; **02** prova che due processi con la stessa identità esatta non duplicano la riga. Queste proprietà positive non risolvono la perdita delle risposte e la ripresa. I runner non collegano inoltre le funzioni di retry del ledger: dopo un errore marcato `FAILED`, `complete_request` non permette una riconciliazione successiva a zero-token e il CLI non riprende lo stadio dal tentativo recuperabile. Non va introdotto un retry automatico: occorre una ripresa esplicita, conservativa e documentata.

### R08 — P1: il gate non autentica il budget congelato dalla sonda

[run_pilot.py:456](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/run_pilot.py:456) registra l’outcome sonda con hash dei record, non un legame verificato alla configurazione finale. [Righe 618–637](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/run_pilot.py:618) controllano alcuni campi del file `frozen_gate_config.json`, ma non il suo hash contro un riferimento immutabile dello stadio concluso, né la corrispondenza del `generation` ai record della sonda.

**52:** dopo una sonda stub passata con `max_tokens=2560`, si cambia soltanto il file sacrificabile a `max_tokens=9999`; il gate esegue **120 nuove chiamate stub**. Calcolare uno stage_run dal file appena riletto non autentica i suoi byte. Il primo gate può quindi usare un budget mai sondato. È distinto dal corretto rifiuto di un secondo gate con stage_run diverso dopo che il primo è già iniziato.

### R09 — P1: identità restituita inattesa registrata ma non sospesa

[producer_probe.py:178](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/producer_probe.py:178) salva `returned_model` e `system_fingerprint`, ma non li confronta con l’identità attesa. Il consumer [run_pilot.py:292](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/run_pilot.py:292) fa lo stesso; il controllo server precedente non intercetta da solo un cambiamento durante le richieste.

**42:** tutte le risposte producer arrivano da `UNEXPECTED-MODEL`/`UNEXPECTED-FINGERPRINT`, ma la conformità conclude **PASS**. **53:** risposte consumer con identità errata conducono a `PASS_R1_PENDING_T5_AND_OTHER_PREREQUISITES`. `go_final=false` resta corretto, ma non sostituisce la sospensione richiesta per cambio d’identità. `verify_endpoint` e `canary.suspension_required` passano isolatamente (**36/60**) e non sono collegati a questo controllo per risposta.

### R10 — P2: il gate accetta triplette formalmente false

[gate_rules.py:32](/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate/studio2/fase03/harness/gate_rules.py:32) impone 120 righe e 40 gruppi di tre, ma non verifica ripetizioni `{1,2,3}`, stessa condition entro prompt, identità/hash coerenti o distribuzione congelata 8/16/16 prompt.

**22:** tutte le righe con `repetition=1` vengono accettate; **23:** un gruppo può mescolare A e B-LF; **24:** il campione 7/17/16 passa ugualmente. Con record altrimenti validi l’esito è un PASS tecnico pending. Il runner ordinario genera indici 1–3, ma l’evaluatore autonomo e gli ingressi da artefatti non rifiutano duplicazione/corruzione. Le corrette soglie numeriche non bastano a certificare quaranta triplette autentiche.

## 5. Matrice requisito → codice → prova

`Nxx` indica il metodo `test_xx_*` della suite indipendente. ✅ = requisito verificato sul perimetro indicato; ❌ = smentito; ⚠️ = limite o condizione non verificabile offline.

| Requisito | Codice/fonte | Prova ed esito |
| --- | --- | --- |
| Commit, parent, tree, base e consegna distinti | Git oggetti esatti | ✅ `initial_identity.json`, `final_identity.json`, delta 24 file, consegna solo 2 documenti |
| 21 hash/dimensioni e hash manifest | `HARNESS_OFFLINE_CANDIDATE.json` | ✅ 21/21, manifest atteso, `integrity.json` |
| Recupero selettivo nove moduli | `1ac06eb…` → candidato | ✅ 4 identici, 5 adattati; nove diff; vecchi freeze/report non importati |
| R4, baseline, rev.10, 03.7 e Normal esatti | manifest, blob, tag object/peeled | ✅ 18 membri R4, 17 baseline, pin tabulati e 3 tag remoti |
| Integrità evidence conservata | archive + conservazione | ✅ 1.283 file, 320 unità; nuovo riscaricamento remoto non svolto ⚠️ |
| Pin imposti prima del consumo | `inputs`, `producer_probe`, `load_prepared` | ❌ N32/37/38/41/47/49, R02 |
| Input conformità indipendenti dalla libreria | `build_inventory`, `_conformance_inputs` | ✅ inventario rigenerato identico, libreria assente; N40 esercita 8 coppie senza libreria iniziale |
| 16 fault locali, 8 Normal, 16 contratti, niente test/OOD nei byte candidati | inventario e fonti development | ✅ ricostruzione e hash; barriera a una sostituzione successiva ❌ N49 |
| Ogni coppia producer validata R4 | `validate_produced_pair` | ✅ N31 e N40: ID, campi fissi, cap, leakage; una coppia malformata → 7/8 richieste valide, FAIL, nessuna libreria |
| Nessuna libreria prima di 16/16 output reali | handoff + builder | ✅ assente nel candidato; ❌ autocertificazione handoff e provenienza non imposta, N33/49 |
| Separazione ordine prompt/evaluator | `render`, `protocol`, `inputs` | ✅ parametro renderer; ❌ builder riscrive `label_space`, N35 |
| Approva 1a, permutazione esatta, Normal ultimo | `ordering`, `render`, `prepare_gate` | ✅ guardie dirette N34 e test consegnati; ❌ percorso ordinario N39 |
| Storico UNDECIDED, nessun default eseguibile | preflight, provider/runner | ✅ stringa e producer senza default; ❌ consumer storico N46 |
| Intent-before-transport e conteggio dopo crash | `PilotLedger`, `_tracked_call`, producer | ✅ N01, stub controlla contatore prima del trasporto; N50/51 mantengono intenti |
| Unicità concorrente e cambio directory/alias | indice SQLite, stage_run | ✅ N02 su due processi esatti; ❌ N03 con nuovo stage_run |
| Stadi completi, guasti e restart fail-closed | outcome/eventi/riserva | ❌ N04–08/18; outcome e inserimento non atomici |
| Una sola remediation, 8 complete, diff e approvazione | ledger + producer | ✅ cardinalità massima, seconda autorizzazione e dopo gate rifiutati; ❌ N09/10/45, R06 |
| Retry remediation imputato a trasporto | quota_kind | ✅ test consegnato e N16; quota remediation=8, trasporto=7, equazione=15 |
| 8r+t≤15, preserva 8, waiver oltre settimo | ledger quote | ✅ N13/14/16: 15 consentito, 16 rifiutato, waiver richiesto, rollback senza consumo parziale |
| Nessun finanziamento da quota alternativo | stage/quota separati | ✅ N14/N16, alternativi aumentano solo blocco proprio e massimo 160 |
| Nessun retry automatico, timeout senza prova bloccato | max_retries=0, metodi retry | ✅ test consegnato, N40/43/48; ❌ riconciliazione e ripresa runner mancanti, R07 |
| Triplette sonda atomiche e semanticamente complete | `reserve_probe_transport_triplet` | ✅ N13 quota/rollback; ❌ N12 stesso originale tre volte; N11 catena concorrente |
| Gate create-once, zero retry gate | `_insert_intent`, runner | ✅ N15; ❌ autenticità configurazione prima del primo gate N52 |
| Massimi 152/160 e hard stop 200 distinto | ledger e preflight | ✅ N16 raggiunge 152/160 con quote corrette; N17 blocca riga 201 su fixture storica; nessuna disponibilità aggiuntiva autorizzata |
| Persistenza forense e crash/resume | runner vs logger | ✅ logger recuperato N61; ❌ runner N43/44/50/51 |
| Differenze raw/JSON/testo/finish senza coppia diversa | `semantic_signature` | ✅ N21 e suite: zero divergenza; coppia/validità diversa divergono |
| T3 114/120, 113 no e astensione per condizione | `evaluate_stability_gate` | ✅ N20; 114 passa solo T3; astensione mancante fallisce |
| T4 separato, almeno un length fallisce | `evaluate_stability_gate` | ✅ N21, test consegnato |
| Tripletta mista diverge; tutta invalida T6 non valutabile | `evaluate_stability_gate` | ✅ N21 e suite; ❌ autenticità delle triplette N22–24 |
| R3 pending fattibilità, nessun GO finale | gate output | ✅ `R3_REQUIRED_PENDING_FEASIBILITY`, `go_final=false`, T5 non misurato |
| Identità cambiata sospende | guardie vs runner | ✅ guardie isolate N36/N60; ❌ runner N42/N53 |
| Canary/audit deterministici, raw solo forense | sampling e canary | ✅ N60: 10 canary, 8 agenti, 2/4/4 condizioni; audit 10%; cambio coppia e sospensione |
| Metriche e denominatori preservati | tre file raccordo | ✅ invariati da base, 9/9 test del raccordo; invalidi non diventano astensioni |

T11 resta distinto da T3: il piano lo definisce descrittivo/esplorativo; l’evaluatore attuale non restituisce un campo T11 autonomo. Non ne è stata inferita una qualifica OOD né è stato eseguito alcun controllo OOD scientifico. Nessun bootstrap di risultati reali è stato svolto.

## 6. Decisione D9 successiva e limiti del verdetto

L’autore ha **già approvato** 122B producer principale e consumer; 27B producer alternativo per una **libreria completa di 16 insight**; Terra soltanto storico descrittivo interno. Non resta da chiedere la scelta dei ruoli. Il testo storico `DECISIONE_D9_ORDINE_LABEL_PENDING.md` e il rapporto, che propongono Terra alternativo e 27B fallback, sono **superati da quella decisione**. Non sono corretti in questa review del candidato esatto.

Il futuro recepimento D9 deve essere un delta separato da verificare sui propri byte. Il mantenimento storico di `study_model_decision=UNDECIDED` è riscontrato; la barriera eseguibile è insufficiente secondo R01. Non si trasferisce alcun OK — neppure quello del raccordo metriche — al futuro delta D9. **L’ordine label 1a resta non approvato**; le accettazioni nei file di fixture non hanno valore autorizzativo.

Capacità effettivamente verificate offline: integrità/provenienza dei byte, inventario development corrente, controllo R4 isolato e per coppia, contabilità numerica e transazioni delle riserve, permanenza degli intenti, guardie dirette, semantica T3/T4/T6 su record ben formati, regressione metriche. La review respinge la qualifica complessiva del loro collegamento nei runner.

Restano da provare successivamente, fuori da questo mandato: recepimento D9 e revisioni esatte; ordine label; **insight reali** e loro provenienza; qualificazione dei due servizi e dei ruoli; tokenizer/chat template e capienza effettivi; identità/fingerprint osservati e continuità durante i run; conformità reale delle due librerie, eventuale remediation autorizzata, sonda e gate reali; latenza e fattibilità **T5** con margine temporale del 20%; prerequisiti scientifici/operativi e autorizzazione del pilot. La disponibilità di un servizio non equivale alla sua qualifica.

**Nessun freeze, nessun GO, nessuna chiusura della 03.10 o della Fase 03.** Prima di acquisire un OK servirà un nuovo candidato corretto e una nuova verifica indipendente sui delta, includendo le riproduzioni qui fallite. Nessuna modifica al walkthrough è stata eseguita o autorizzata da questo verbale.

## 7. Consegna e stato Git

Le sole scritture del revisore sono nel contenitore isolato `fot-tep-verifica-harness-0310-01a0a1ec`: clone e `evidence/`. I file di prove sono esterni al candidato. `fixtures/` è interamente sacrificabile e marcata da `FIXTURES_ONLY.md`; contiene anche artefatti volutamente falsi o alterati, mai promossi a input scientifici. `reference/` conserva byte development autenticati.

`final_identity.json` registra HEAD/tree invariati e `git status --porcelain` vuoto del candidato. Le istantanee di stato di copia principale, sorgente e consegna coincidono con quelle iniziali, inclusi i non tracciati preesistenti. Questo constata lo stato Git; non attribuisce al revisore le eventuali attività interne di altre finestre. Il revisore non vi ha scritto.

Le impronte di verbale, script, log, fonti copiate e fixture sono in `SHA256SUMS`, generato alla fine, esclusi sé stesso e le cache Python. Il suo hash è comunicato nella consegna finale; il manifest non contiene hash autoreferenziali. `integrity.json` contiene il dettaglio completo dei confronti e `negative_probes.json` tutte le failure e le osservazioni. Lettura svolta: regole e consegne pertinenti, moduli coinvolti, sezioni normative e manifest; circa 200–300 KB di testo pertinente ispezionato oltre ai file letti meccanicamente per hash. Non è una lettura integrale della letteratura o del piano scientifico generale.
