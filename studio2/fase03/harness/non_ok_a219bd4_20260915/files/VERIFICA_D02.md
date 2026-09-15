NON OK — candidato offline a219bd469bbd280f56b7fa9cb56cda115b0975ed. D02 originario chiuso nelle prove riprodotte; distinto D03 aperto sulla riconferma delle prove zero-token. Nessun freeze o GO.

# Verbale autonomo D02 — 15 settembre 2026

## Identità, isolamento e indipendenza

| Oggetto | Identità verificata |
| --- | --- |
| Candidato tecnico | `a219bd469bbd280f56b7fa9cb56cda115b0975ed` |
| Tree tecnico | `3fb8e50c189b85b447503b8a1ac99c1741904a5b` |
| Parent, acquisizione separata | `5b45cdcabe40aa64b0aecd1b5fe9d09c92ce5bb4` |
| Base documentale | `7afbf41632aa8117c85274b5f471abca0a655462` |
| Successore documentale, escluso dall'esecuzione | `e9b60c5db77edfd3c06a29857e6ba5f61ebe139a` |
| Tree documentale | `5460dad38b8321ea0d820937fb2b506580e6e3c1` |
| Respinto precedente | `edb37f359f29c461c5a507c1027c4bf411654130`, tree `56d98666e1d18c7958ac8d3631ae6d5b8ec04bf9` |
| Main remoto effettivo prima/dopo | `a00605862f627710347bd63c49f79a6d0a00135f` |

Prima delle scritture verificati branch, HEAD/tree/parent, indice/status, worktree e `git ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main`. Sorgente `/Users/luker/fot-tep-harness-0310-d02`, branch `codex/studio2-harness-0310-d02`, pulita sul successore documentale. Quest'ultimo aggiunge solo i quattro documenti di consegna, acquisiti con git show. Non è stato eseguito in luogo del tecnico.

Review in `/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate`, clone detached sul tecnico esatto. Working tree, indice e riferimenti separati; oggetti Git locali condivisi in lettura. Output esclusivamente nel fratello `/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence`. Nessuna modifica o correzione al candidato, nessun commit/tag/push/integrazione.

| Esecutore | Runtime osservato |
| --- | --- |
| Revisore, questa finestra | sessione `01a0a1ec-35a4-7870-9c39-9bf922d36c85`; modello `gpt-6-astra`; effort `high` |
| Preparatrice | sessione distinta `01a0a204-abda-7a00-8466-f52f5bc84812`; modello `gpt-6-astra`; effort `xhigh` |
| Test | `/opt/anaconda3/bin/python3`, Python 3.13.9, arm64, SQLite 3.51.0 |

Fonte: campi session_meta/turn_context riletti dai rollout locali, in [runtime.json](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/runtime.json). Effort è il valore registrato, non una misura del calcolo consumato. La finestra è distinta; **il modello coincide**. Il criterio aggiuntivo di indipendenza tra modelli auspicato da Verifica_LLM non è soddisfatto e non viene rivendicato. Nessuna delega.

Applicati MAINTENANCE principale/candidato e regole pertinenti già lette nei cicli precedenti; ricontrollata la differenza esatta di MAINTENANCE, conservata in maintenance_candidate.diff. Letti mandato/report D02, verbale precedente integrale acquisito, delta ledger/contratto, test e inventari. Il verbale precedente è quello autonomo scritto in questa finestra e conservato byte-identico. Fonti normative e artefatti usati a commit esatto; nessuna incorporazione dei lavori paralleli. Ordine di grandezza delle letture: alcune centinaia di kB pertinenti, oltre ai confronti meccanici degli inventari; nessuna nuova analisi scientifica o di letteratura.

## Integrità e provenienza

✅ [integrity.json](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/integrity.json): **6.735 confronti, zero mismatch**. Sono confronti di integrità anche ripetuti, non metodi comportamentali distinti.

| Oggetto | Verifica autonoma |
| --- | --- |
| Manifest tecnico | **70/70** membri, 17.729 byte, SHA-256 `fb8474c6e71d63fbb54b83d46e63ae4238a7fb4b20d6c988866e27085d8db9a9`; membri confrontati anche con blob HEAD |
| Acquisizione precedente | **1.822 file**: 100 copie byte-identiche e 1.722 esterni recuperabili, riletti per dimensione/hash |
| Riproduzioni preparatrice | **1.841 file**: 44 copie byte-identiche e 1.797 esterni; verificato anche ogni membro del relativo SHA256SUMS |
| Prima evidence indipendente | 2.754 file riletti, inclusi i 1.283 membri della reference evidence-v2 già scaricata e verificata nella catena precedente |
| R4/baseline/input/piano | 18 membri R4, 17 pin baseline, quattro pin input e tre fonti piano riletti dai Git blob esatti; tre tag R4/baseline/03.7 ricontrollati sul remoto effettivo |
| Moduli recuperati | Nove moduli invariati nel delta, confrontati con la sorgente `1ac06ebdc92f73d3b630ccca9bf75f413bea170b` e col precedente candidato |
| Metriche qualificate | Tre file byte-identici anche alla base pubblicata; nove test inclusi nelle suite |
| Sintassi/import | **92 sorgenti live** compilati via AST senza cache; nessun import diretto phase_b; esclusi alberi forensi |

Verbale acquisito SHA-256 `2806ce5c15d51c917e3e19cc77a935c37ffe09134b485fa257401f6b85ad2fd6`; manifest precedente `dceb4ae6bd4c177002c0bbc1c942333590f114218d1499ebab0ae6475459dffd`. Verificati originali, copie ed esterni prima dell'uso. Le prove sono lanciate in contenitori nuovi, mai nell'acquisizione tracciata o nelle evidence precedenti.

R4 resta al target `3c64390bc4dd58c48cc4e1e388a38989b32b3143`, manifest `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`; il piano rev.10 è a `6aaa5b3eebfed4ba502c25c0443caabd0051af21`. Pin baseline rev005, 03.7 e Normal conservati. Solo logging_v1.py e sampling.py restano identici alla sorgente recuperata; gli altri sette sono adattamenti già dichiarati, invariati in questo delta. Non si promuove una vecchia dichiarazione di identità byte a file adattati.

✅ Diff tecnico dal parent: **52 percorsi**, un runtime (ledger.py, +124/−54), un nuovo modulo test, tre documenti/manifest e 47 file di prove/inventari. Elenchi in technical_paths.txt e documentary_paths.txt; delta esaminato in technical.diff. I tre file metriche e i runtime C02/C03 esterni al ledger sono invariati. Perimetri protetti senza differenze dalla base documentale: docs/walkthrough, phase_b, code, icl/ablation, piano statistico, pseudolabel, schema, baseline, soglie Normal, APERTURA, preflight e inventario pending. Nessuna rigenerazione di input o risultati scientifici.

## Prove e copertura

| Prova | Esito osservato | Evidenza |
| --- | --- | --- |
| Mirati completi | ✅ **111/111**, zero failure/errori | [targeted.log](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/targeted.log) |
| Discovery completa | ✅ **146/146**, zero failure/errori | [discovery.log](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/discovery.log) |
| Otto D02 e sette D01 | ✅ Tutti passano, già inclusi nei totali | log mirato, test_d02_predecessors e test_d01_replay |
| Originali applicabili | ✅ **14/14**, 12 letterali e due con sola fixture/argomento | [applicable.log](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/applicable/applicable.log) |
| Z01–Z05 letterali | ✅ **5/5**, D02 originario chiuso | [chain_probes.json](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/z_original/evidence/chain_probes.json) |
| Y01–Y07 letterali | ✅ **7/7** | [edge_probes.json](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/y_original/evidence/edge_probes.json) |
| X01–X18 letterali | ✅ **18/18** | literal/evidence/extended.log |
| X19–X24 letterali | Cinque PASS, **una failure X23 obsoleta**, zero errori | literal/evidence/additional_edges/additional.log |
| Solo X23 già adattato | ✅ **1/1**, nessun nuovo adattamento | x23_adapted/evidence/additional_edges/additional.log |
| Nuove W01–W04 | ❌ **Due PASS, due failure, zero errori**, un solo D03 | [retry_proof_probes.json](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/retry_proof_probes.json) e log omonimo |
| Guardiano documentale | **NON PASS: 35 test, stessi 14 identificativi falliti, 1 skip**, zero errori | [documentation_comparison.json](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/documentation_comparison.json) e documentation.log |

Suite e sottocasi non si sommano. Le 29 esecuzioni preliminari della preparatrice includevano 21 fixture TestCase importate; non sono 29 regressioni nuove. Il suo primo X23 senza modulo sibling è un errore di setup conservato, non un difetto candidato. Qui X23 è stato predisposto con entrambi i moduli byte-identici e non ha incontrato tale errore.

X23 letterale pretende l'interruzione difettosa C02: la failure resta nel log. Il consolidamento è **23 letterali più X23 già adattato**, non 24/24 del file immutato. L'adattamento conserva sempre TimeoutError e richiede 120 INVALID, T3/T6 falliti e 40 triplette non valutabili, dati non osservati null, riconciliazione immutabile e nessun reinvio. Nessuna assertion X/Y/Z modificata qui; copie confrontate per hash con la precedente evidence.

La [matrice nominativa dei 50 metodi](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/MATRICE_50_METODI.md), con JSON omonimo, collega ogni metodo originale a una prova corrente passata, log e motivazione dell'adattamento/accorpamento. Restano 12 letterali, due con sola fixture/argomento, 35 adattati/accorpati e N48 equivalente alla regola C02 della nuova API. Nessuna esclusione implicita o pretesa 50/50 letterali. I vecchi falsi verdi N22–24/N41 non sono usati: le prove pertinenti partono da fixture positive complete. [MATRICE_ESTENSIONI.md](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/MATRICE_ESTENSIONI.md) distingue tutti gli X/Y/Z/W.

## Chiusura D02 e regressioni conservate

✅ Z01/Z02: dopo un positivo, raw/record primari, alternativi e sonda corrotti, dati mancanti o copertura incompleta vengono respinti dagli ingressi normativi. Z03 nel runner rifiuta il raw alternativo corrotto senza nuovi invii. Le regressioni D02 verificano anche CLI budget/stability --resume: zero chiamate aggiuntive allo stub/server, **139 intenti conservati**, stessi byte degli output e stesso database logico dopo il rifiuto. La lettura forense degli eventi non diventa conferma normativa.

✅ Validatore condiviso: perdita di response/record, prefisso sonda 9→6, record alterato con solo hash locale ricalcolato, artefatto/evento/freeze incoerente, identità richiesta alterata, perdita della prova di un antenato retry, remediation attiva corrotta e riconferma del proprio binding chiuso sono respinti. Un nuovo ingresso sonda non supera un producer con raw corrotti. I controlli sono pertinenti, non eccezioni di setup.

✅ Concorrenza: Z04 e la regressione D02 tentano un vero BEGIN IMMEDIATE da un altro processo durante la conferma, anche dentro la lettura dei record del predecessore. I quattro ingressi tengono il lock fino al ritorno; dopo il rilascio il processo lo acquisisce. W03/W04 verificano anche l'assenza di cache persistenti: dopo conferma valida, nella stessa istanza, perdita di prova intermedia o nuovo raw corrotto vengono rilevati.

✅ Positivi conservati: catene legacy valide con/ senza alternativo, sonda rimaterializzata dopo gate, summary mancante rigenerato identico, remediation valida, retry producer con **nove intenti e otto coppie**, catena di due retry con **dieci intenti e otto coppie**, nessun nuovo invio/evento/azzeramento per la sola conferma. D01 usa sempre il vecchio codice esatto/pulito 0c8157f in subprocess per generare la precedenza storica, senza SQL artificiale; le vecchie catene con alternativo non PASS sono rifiutate.

✅ C02: un timeout completa **120 primi tentativi**, 119 validi, una tripletta divergente e R3_REQUIRED_PENDING_FEASIBILITY; tre timeout sul medesimo prompt rendono T6 non valutabile, sette distribuiti falliscono T3, tutti i timeout danno 120 INVALID e NO_GO tecnico. Fonte: piano rev.10 righe 831/871–875. Atomicità FAILED+evento, crash prima/dopo commit/raw, morte reale di un processo, errore journal, riconciliazione esplicita e ripresa in un altro processo conservano dati/contatori senza reinvii. Z05 mantiene FAIL e 120 INVALID senza promuovere a PASS. Nessun retry gate.

✅ C03: nove richieste provider/ledger/summary distinte da otto coppie T9 e 16 insight. Y07 verifica anche l'alternativo: nove richieste dello stadio contro 17 cumulative del pilot, summary eliminato e rigenerato identico, stesso outcome e nessun invio. I contatori restano prudenziali: un INTENT non dimostra ricezione remota dopo un crash incerto.

## Matrice requisito → codice → prova

| Requisito | Codice pertinente | Esito e prove |
| --- | --- | --- |
| R01 | [guards.py:93](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/guards.py:93) | ✅ Barriere storiche conservate: N46, test_R01_*, X17, Y05. UNDECIDED/SUSPENDED rifiutati; nessun default abilitato. |
| R02 | [inputs.py:155](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/inputs.py:155), [preparation.py:11](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/preparation.py:11) | ✅ Attacchi input/pin/handoff ricontrollati: N30–33/36–38/41/47/49, test_R02_*, X12/X14/X17, Z01/Z03. |
| R03 | [inputs.py:230](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/inputs.py:230), protocol.py | ✅ Label evaluator-side/presentazione separati: N34/35/39, test_R03_*, X17. Ordine reale pending. |
| R04 / D01 / D02 | [ledger.py:208](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:208), [ledger.py:550](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:550) | ✅ D01/D02 originari chiusi: N04–08/18, X01/02/04/05/07/14, Y01/Y02, Z01–Z05 e D01/D02 suite. ❌ La conferma complessiva dei retry resta limitata da D03. |
| R05 | [ledger.py:273](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:273), [ledger.py:509](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:509) | ✅ Quote/identità/unicità e catene: N01–03/11–17, X06–09/19/21, Y06, W03; 12 writer, rollback tripletta, 8r+t≤15, 152/160 e hard stop 200 distinto. ❌ D03 sulla prova zero-token persistita. |
| R06 | [ledger.py:626](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:626), producer_probe.py | ✅ N09/10/40/45, test_R06_*, X10/20/24, D01/D02 remediation: diagnosi, diff/template concreti, otto casi, nessuna seconda remediation/libreria parziale. |
| R07 / C02 / C03 | [runtime.py:41](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/runtime.py:41), [producer_probe.py:181](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/producer_probe.py:181) | ✅ C02/C03 conservati: N01/43/44/48/50/51, test_R07_*/C02_*/C03_*, X03/15/16/21/23 adattato, Y03–07, Z05. ❌ D03 è distinto dal denominatore corretto C03 e limita la riconciliazione durevole. |
| R08 | [ledger.py:619](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:619) | ✅ Freeze/provenienza/predecessori D02: N52, test_R08_*, X18, Z01/Z02/Z04, test_D02_probe*/record*. D03 riguarda la validità della prova di retry nella catena, non il budget congelato. |
| R09 | [guards.py:107](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/guards.py:107), [ledger.py:473](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:473) | ✅ N42/53, test_R09_*, X13/X22, Y03/Y05, D02 identità. Raw e consumo conservati, mismatch sospende; INVALID non maschera risposte ricevute. |
| R10 | [gate_rules.py:51](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/gate_rules.py:51) | ✅ N20–24, GateRevisions, X11, C02, Z05: 40×3, 120 ID, ripetizioni intere 1–3, otto agenti, 8/16/16 e ruoli del campione; nessun retry. |

## D03 — P2 — Prova zero-token persistita accettata dopo alterazione di campi obbligatori

❌ Il nuovo validatore dei tentativi controlla solo parte della prova che giustifica un retry. La riconferma può accettare un antenato ZERO_TOKEN_PROVEN con evidenza persistita che contiene token positivi, token mancanti/booleani o campi obbligatori vuoti. Questo è un rilievo distinto dalle manifestazioni D02 già corrette.

**Requisito:** [contratto:122](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md:122) e [contratto:178](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md:178): conservare la prova registrata, tre contatori esplicitamente zero, ricevuta/evidenza provider e autore/approvazione. Il mandato D02 richiede di verificare le catene complete di retry e le prove durabili dopo nuovi fault.

**Codice:** in [reconcile_zero_token:495](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:495) la prima acquisizione rifiuta contatori diversi da interi zero, ricevuta/evidenza provider assenti e autore assente. In [_validate_attempts:527](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:527), invece, la riconferma confronta esistenza dell'evento, stringhe hash, ID/identità, disposition, decision e assenza di raw, ma omette quei controlli di contenuto. Le vecchie stringhe hash restano uguali tra loro anche se si altera il contenuto di detail_json. Il validatore non rileva queste inconsistenze.

**W01:** catena inizialmente valida con un retry producer, nove intenti nello stadio, poi sonda e gate. In sette copie separate si altera solo l'evento di riconciliazione: prompt_tokens=1, total_tokens=1, completion_tokens mancante, total_tokens=False, provider_request_id vuoto, provider_evidence vuoto oppure author vuoto. Restano intatti hash registrati, identità, raw, record, status e outcome. Binding gate, verify_stage_success(gate), replay outcome gate, authenticate_frozen e binding del producer già chiuso **accettano tutti e sette i casi**. Nessuna scrittura delle conferme nel database logico. Sette sottocasi × cinque ingressi sono un metodo, non 35 test distinti.

**W02, runner ordinario:** timeout sulla seconda richiesta producer, prova zero-token valida, retry esplicito e chiusura con nove richieste/otto coppie; prepare, sonda e gate validi. Poi si cambia soltanto la prova persistita a prompt_tokens=1 e total_tokens=1 (completion_tokens resta zero), senza aggiornare alcuna impronta. Riaperto il ledger, `run_stability_stage(..., resume=True)` restituisce ancora **PASS_R1_PENDING_T5_AND_OTHER_PREREQUISITES**, 120/120, T3/T4/T6 veri, identico all'esito precedente al fault. **132 intenti conservati** (9+3+120), zero nuovi invii; viene raggiunta una interrogazione dello stub server. `go_final` resta false. Il contenuto della prova che la catena ripropone come zero-token non è più conforme.

**Evidenza:** [retry_proof_probes.py](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/retry_proof_probes.py), JSON/log omonimi; copie in `retry_proof_fixtures/test_W01_changed_zero_token_proof_must_not_reconfirm_closed_chain/` e `test_W02_real_runner_rejects_positive_tokens_in_durable_retry_proof/captured/`. Il JSON conserva prova prima/dopo, impronta invariata, risposte delle conferme e contatori. Due assertion pertinenti fallite, zero errori di setup: stesso difetto D03.

**Limiti:** i token positivi sono un fault iniettato nella sola copia dell'evento; non sono una misura reale del provider. La riconciliazione iniziale era lecita. Non è dimostrato un retry spontaneo, un azzeramento, una nuova inferenza o un GO. Nessun hash/outcome è riscritto per rendere coerente l'intero database: non si richiede resistenza crittografica contro una riscrittura arbitraria completa. Si richiede coerenza locale dei contenuti obbligatori che il codice acquisisce e dichiara di riconfermare. Il difetto non riapre il conteggio C03, che rimane corretto.

La chiusura richiede una riconferma adeguata anche della prova zero-token persistita, mantenendo replay leciti, contatori e letture forensi. Nessuna correzione applicata in questa review.

## Consegna e confini

**NON OK sul solo candidato tecnico esatto.** D01/D02 originari sono chiusi nelle riproduzioni; C02/C03 restano corretti nei percorsi verificati. D03 impedisce di dichiarare completa la verifica delle prove di retry. I conteggi dichiarati delle suite sono stati confermati; il guardiano documentale rimane NON PASS.

D9 è già approvata: **122B producer principale e consumer, 27B alternativo per 16 insight, Terra soltanto storico descrittivo interno**. La proposta Terra precedente è superata; nessuna nuova decisione sui ruoli richiesta. Restano separati il recepimento eseguibile D9, ordine label 1a ancora non approvato, insight reali, qualificazioni servizi/tokenizer/identità/capienza, T5 e autorizzazione pilot. Storico preflight UNDECIDED/SUSPENDED invariato. Nessun trasferimento del giudizio ai futuri byte D9, nessun freeze o GO.

[Stato Git finale](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/final_git_state.json): candidato detached pulito; principale, cinque sorgenti e quattro candidati precedenti preservati rispetto allo snapshot iniziale. La principale conserva branch codex/studio2-soglie-normal, HEAD `819b12e97fb94d501032655ec2f226139e6c5ca5` e gli untracked preesistenti. Nessun commit/tag/push/merge, modifica al walkthrough, provider API, inferenza o simulazione scientifica. La rete è usata soltanto per le letture Git richieste; trasporti e tokenizer delle prove sono stub.

[COMANDI.md](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/COMANDI.md) rende riproducibile il lavoro. [EVIDENCE_INVENTORY.json](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/EVIDENCE_INVENTORY.json) distingue file e symlink; [SHA256SUMS](/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/SHA256SUMS) impronta i file regolari senza seguire symlink e senza autoreferenza. Le copie delle fixture conservano riferimenti ai temporanei originari, anche quando rimossi dal cleanup. Per riprodurre creare nuove directory sacrificabili; non eseguire in-place le prove tracciate o sovrascrivere le evidence conservate. Hash del verbale e manifest comunicati esternamente.
