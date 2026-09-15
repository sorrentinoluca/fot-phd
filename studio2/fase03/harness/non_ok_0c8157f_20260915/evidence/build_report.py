from pathlib import Path
import json,ast,hashlib
E=Path(__file__).resolve().parent;C=E.parent/'candidate';H=C/'studio2/fase03/harness'
def link(label,path,line=None):return f'[{label}]({path}'+(f':{line}' if line else '')+')'
def code(file,func):
    p=C/'studio2/fase03'/file
    n=next(n for n in ast.walk(ast.parse(p.read_text())) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==func)
    return link(file+' / '+func,p,n.lineno)
def proof(name):return link(name,E/name)
integrity=json.loads((E/'integrity.json').read_text());scope=json.loads((E/'scope_and_results.json').read_text())
matrix=[
('R01','CHIUSO nel candidato storico',code('harness/guards.py','require_execution')+'; '+code('run_pilot.py','Provider'),'N46; test_R01_* Python/CLI e Provider/server_contract; X17. UNDECIDED/SUSPENDED e coordinate ledger diverse rifiutati prima del trasporto. Nessun default storico eseguibile.'),
('R02','CHIUSO per gli attacchi verificati',code('harness/inputs.py','verify_conformance_inventory')+'; '+code('harness/inputs.py','_load_evidence')+'; '+code('harness/preparation.py','authenticate')+'; '+code('run_pilot.py','load_prepared'),'N30–33/36–38/41/47/49; test_R02_*; X12/X17. Pin 03.7/Normal/R4, JSON evidence, dipendenza prima degli invii, inventario canonico, handoff ricostruito dai raw e rigenerazione dei prompt. R4 alterato durante il ciclo ferma prima del secondo invio.'),
('R03','CHIUSO per il difetto originario',code('harness/inputs.py','build_inventory')+'; '+code('prepare_gate.py','prepare')+'; '+code('protocol.py','build_pilot_sample'),'N34/35/39; test_R03_*: label_space canonico rimane evaluator-side, presentazione separata. Pipeline positiva usa handoff stub autentico; pending rifiutato dagli ingressi ordinari. Nessuna approvazione reale dell’ordine.'),
('R04','PARZIALE — C01 aperto',code('harness/ledger.py','_ready')+'; '+code('harness/ledger.py','record_stage_outcome'),'N04–08/18; X04/X05/X07/X14. PASS su FAILED/ZERO senza recupero rifiutato, eventi normativi pubblici vietati, chiusura atomica e no retry tardivi sul primario. X01/X02 smentiscono il blocco globale quando l’alternativo è irrisolto.'),
('R05','CHIUSO per identità, retry e quote provati',code('harness/ledger.py','bind_stage')+'; '+code('harness/ledger.py','_insert_intent')+'; '+code('harness/ledger.py','reserve_probe_transport_triplet'),'N01–03/11–17; X06/X08/X09/X19/X21. Binding immutabile, unicità base e figlio retry; 12 writer reali; tre originali distinti, stesso gruppo; rollback quota, 8r+t≤15, quota7 sonda, 152/160, hardstop200 distinto. L’esito non chiude C01 sulle precedenze.'),
('R06','CHIUSO per il difetto originario',code('harness/ledger.py','authorize_remediation')+'; '+code('producer_probe.py','run')+'; '+code('harness/inputs.py','_insights'),'N09/10/40/45; test_R06_*; X20/X24. Diagnosi registrata, diff e template concreti approvati, primi binding alterati respinti, stessi otto casi, nessuna seconda remediation, handoff vecchio escluso. Timeout non convertito in difetto prompt.'),
('R07','PARZIALE — C02/C03 aperti',code('harness/runtime.py','execute_request')+'; '+code('harness/ledger.py','reconcile_zero_token')+'; '+code('harness/runtime.py','export_journal'),'N01/43/44/48/50/51; test_R07_*; X03/X15/X16/X21/X23. Raw, receipt e record durevoli; resume conservativo, prove esplicite e ricostruzione file senza invii. N48 non equivalente; riepilogo chiamate dopo retry errato.'),
('R08','CHIUSO per il difetto originario',code('harness/ledger.py','authenticate_frozen')+'; '+code('run_pilot.py','run_stability_stage'),'N52; test_R08_*; X18. Freeze autenticato con l’evento sonda e confronto dei byte; budget alterato o sola serializzazione alterata: zero invii aggiuntivi del gate.'),
('R09','CHIUSO per i mismatch provati',code('harness/guards.py','response_identity_valid')+'; '+code('harness/runtime.py','execute_request'),'N42/53; test_R09_*; X13/X22. Modello/fingerprint inattesi sospendono producer, sonda o gate; raw e consumo conservati. Nel caso X13 token totali 5 persistono. Null resta una disponibilità esplicitamente dichiarata, non un’identità inventata.'),
('R10','CHIUSO per le triplette false',code('harness/gate_rules.py','evaluate_stability_gate'),'N20–24; GateRevisions; X11. Campione richiesto, 40 hash distinti, 8 agenti, 8/16/16, ruoli/casi matched-transfer e context-stress, 120 ID, ripetizioni int 1–3, zero retry. Soglie e semantica valutatore passano; C02 riguarda l’alimentazione del valutatore dopo errori trasporto.'),
]
table='\n'.join('| '+' | '.join(r)+' |' for r in matrix)
report=f'''NON OK — candidato offline 0c8157f23bee49a3a5a2df648525c34706da29d7; nessun freeze o GO.

# Verbale autonomo di riverifica 03.10 — 15 settembre 2026

## Perimetro, identità e indipendenza

Verifica eseguita in una finestra distinta dalla preparatrice delle correzioni, sul solo candidato tecnico richiesto. Il verdetto riguarda questi byte e i tre rilievi C01–C03 sotto; non qualifica lo studio o il futuro recepimento D9. Non sono state apportate correzioni.

| Identità | Valore osservato |
| --- | --- |
| Review, task “Verifica harness offline 03.10” | sessione `01a0a1ec-35a4-7870-9c39-9bf922d36c85`; `gpt-6-astra`; effort registrato `high` |
| Preparazione correzioni, task “Correggi rilievi harness offline 03” | sessione distinta `01a0a204-abda-7a00-8466-f52f5bc84812`; `gpt-6-astra`; effort registrato `xhigh` |
| Runtime dei test | `/opt/anaconda3/bin/python3`, Python 3.13.9, arm64, SQLite 3.51.0 |

Fonte: campi `session_meta` e `turn_context` dei rollout locali, estratti in {proof('runtime_identity.json')}; identità dei task riscontrate anche nella UI dell’app. **La diversità di finestra è verificata; la diversità di modello non c’è.** `docs/prompts/Verifica_LLM.md` preferisce un altro modello e afferma che una verifica dello stesso modello è una rilettura: quel criterio aggiuntivo di indipendenza tra modelli non è soddisfatto. Questo limite è dichiarato: non si presenta la review come concordanza tra modelli diversi. Le prove sono state costruite ed eseguite autonomamente nella finestra distinta richiesta dall’utente; nessun esecutore è stato delegato. `high`/`xhigh` sono i valori runtime registrati, non deduzioni da nomi commerciali o misure del calcolo effettivamente consumato.

Letti e applicati MAINTENANCE della copia principale e del candidato, instradamento `Prompt_LLM.md`, regole `Verifica_LLM.md`, prompt originario e nuovo prompt di consegna. Per i vincoli scientifici prevalgono le fonti esatte improntate del piano rev.10, non il nuovo contratto scritto dall’esecutore. Nessuna modifica al walkthrough o ai lavori paralleli 03.8/D9.

## Identità Git, fonti e integrità

| Oggetto | Identità |
| --- | --- |
| Candidato tecnico verificato | `0c8157f23bee49a3a5a2df648525c34706da29d7` |
| Tree esatto | `a1573b49615a875f24ee97f9f1cd4bab399be93d` |
| Parent, acquisizione precedente NON OK | `ec012911444de6baf1751ae4bf4aee8e9c24adbb` |
| Base della consegna precedente | `288dc1926bfd7ab4ce43bb4377a9a0064313ad69` |
| Candidato respinto precedente | `59b6b93cd9c215e8b687e540f7cd579804b7c66a`, tree `cf08c14a8deb18145189afbe9722d7da46bc2f82` |
| Successore documentale, escluso dal candidato | `6268437b8b64288b50ad5f7c924e1fcab85b27d3` |
| Base pubblicata e main remoto osservato prima/dopo | `a00605862f627710347bd63c49f79a6d0a00135f` |

Il remoto verificato è `https://github.com/sorrentinoluca/fot-phd.git`, mediante `git ls-remote … refs/heads/main`; non il tracking branch del clone con origin locale. Il worktree sorgente è `/Users/luker/fot-tep-harness-0310-correzioni`, branch `codex/studio2-harness-0310-correzioni`, pulito sul successore documentale. La copia principale è rimasta sul branch `codex/studio2-soglie-normal`, HEAD `819b12e97fb94d501032655ec2f226139e6c5ca5`, con i suoi untracked preesistenti preservati.

La review usa `{C}`, clone locale separato, **detached sul candidato e pulito**. File di review e fixture stanno soltanto nel fratello `{E}`. Il clone usa un object store Git locale condiviso; working tree, indice e riferimenti sono separati. Nessun commit, tag, push o integrazione. Snapshot iniziale/finale: {proof('initial_identity.json')}, {proof('final_git_state.json')}. Stato e identità di principale, sorgente e precedente review coincidono prima/dopo.

Risultati dell’audit in {proof('integrity.json')} e {proof('scope_and_results.json')}:

- Manifest tecnico: SHA-256 `8ed9fbc37ee14d162ce65f55430159bb1e2507e95cf65aa8d72df3743170dbe1`, 11.662 byte, **44/44 membri** con hash/dimensione corrispondenti; checkout confrontato con il commit.
- Acquisizione precedente: **2.754 membri**, 1.471 acquisiti e 1.283 esterni, tutti riletti e verificati; confrontati anche gli originali preservati. Verbale precedente `fc9725d5412ff30b789977cf12e6ae4742f8063cce7b6e5e2242aeddb3d61547`; manifest precedente `0d25177f41ef9651ee246d5ad8610c020e43c931e168f3c18ba9098d871f0223`.
- Totale inventario audit: **5.655 registrazioni di controllo**, nessun mismatch. È un numero di confronti ripetuti/provenienza, non di test indipendenti.
- R4: target `3c64390bc4dd58c48cc4e1e388a38989b32b3143`, manifest `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`. Tag R4/03.7/baseline confrontati anche con remoto; baseline rev005 e fonti 03.7/03.9 rilette ai commit esatti.
- Evidence-v2: riusati solo i 1.283 membri già verificati, riletti per hash. Nessun download o rigenerazione scientifica. Il riferimento resta l’archivio `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf` della review precedente; i test del builder consumano CSV/JSON/text locali verificati.
- Nove moduli recuperati confrontati con `1ac06ebdc92f73d3b630ccca9bf75f413bea170b` e col candidato respinto: `logging_v1.py` e `sampling.py` restano byte-identici alla sorgente; `canary.py` e `ordering.py` mantengono gli adattamenti già verificati; `guards.py`, `producer.py`, `inputs.py`, `insight_adapter.py`, `render.py` hanno il delta esplicito di questa revisione. Tutte le impronte sono registrate; non si riutilizza la vecchia dichiarazione “byte-identico” per i file ora cambiati.
- Delta tecnico dal parent: **30 percorsi, +3.750/−1.195**. Il successore aggiunge soltanto report, prompt e manifest documentale; i due membri documentali sono verificati e acquisiti fuori candidato. I tre file metriche e i perimetri protetti sono invariati rispetto al candidato precedente; le metriche sono byte-identiche anche alla base pubblicata. Nessun import diretto `phase_b` nei 90 sorgenti Fase03 ispezionati; compilazione sintattica senza scrivere cache nel candidato.

## Prove eseguite e limiti dei conteggi

| Prova | Esito osservato | Evidenza |
| --- | --- | --- |
| Suite mirata richiesta | **82/82**, 0 failure, 0 errori | {proof('targeted.log')} |
| Discovery Fase03 | **117/117**, 0 failure, 0 errori | {proof('discovery.log')} |
| Wrapper dei metodi dichiarati applicabili | **14/14**: 12 metodi invariati, 2 con fixture/argomento | {proof('applicable/applicable.json')} |
| Originale completo, letterale, sul nuovo candidato | 50 eseguiti, 2 failure, 32 errori, 16 verdi; **incompatibilità fixture/API, non 34 difetti nuovi** | {proof('original_all_unadapted/evidence/negative_probes.json')} |
| Estensioni indipendenti X01–X24 | **24 metodi: 20 conformi, 4 assertion fallite, 0 errori di esecuzione validi**; quattro failure raggruppate in C01–C03 | {proof('extended.json')}, {proof('concurrency_rerun/concurrency.json')}, {proof('additional_edges/additional.json')} |
| Guardiano documentale | 35 test, **stesse 14 failure storiche**, 1 skip, 0 errori; **NON PASS** | {proof('documentation.log')}, confronto ID in {proof('scope_and_results.json')} |

Le suite si sovrappongono: non si sommano. I 20 metodi preesistenti di `test_harness_offline.py` restano 20; i 37 nuovi portano i conteggi precedenti 45/80 a 82/117. I nove test del raccordo metriche sono inclusi. Gli ID dei 32 metodi non conformi della riproduzione storica del respinto coincidono con la review precedente (34 failure di assertion, zero errori); ciò attesta l’acquisizione, non la chiusura del nuovo candidato.

**Trasparenza sulle prove del revisore:** nel primo run esteso X06/X07 hanno importato dal cwd principale nei subprocess e hanno fallito prima del controllo pertinente (`ModuleNotFoundError`). Non sono difetti del candidato. Conservati script iniziale, log e JSON; corretti soltanto i due `cwd` nello script esterno, rieseguiti **solo X06/X07**: 2/2, zero errori. Il risultato consolidato 24/20/4 sopra usa quel rerun. Una prima versione dello script di inventario assumeva erroneamente che il JSON storico fosse un oggetto anziché una lista: corretto il solo lettore del revisore e completati i confronti. Nessuna assertion del candidato è stata indebolita o corretta.

Le chiamate sono esclusivamente stub; socket proibiti nelle fixture. Gli SDK/server e il conteggio token sono sostituiti solo alle frontiere esterne. Nessuna API provider, inferenza, misura di servizio o simulazione scientifica. I test creano artefatti chiamati “frozen” soltanto nelle fixture sacrificabili: non sono un freeze scientifico.

## Matrice requisito → codice → prova e chiusura R01–R10

| Rilievo | Chiusura verificata | Codice candidato | Prova e limite |
| --- | --- | --- | --- |
{table}

La corrispondenza individuale dei **50 metodi**, con nomi completi, link al codice di prova, adattamenti e accorpamenti motivati, è in {proof('MATRICE_50_METODI.md')} e {proof('MATRICE_50_METODI.json')}. Non ci sono esclusioni implicite. I verdi letterali N22/N23/N24/N41 non contano come prova sufficiente perché possono fermarsi sul prerequisito nuovo sbagliato; sono sostituiti da fixture positive autentiche prima della singola alterazione. **N48 non è una semplice modifica di fixture: cambia il comportamento normativo e resta NON OK.**

## Rilievi aperti, riproducibili senza modificare il candidato

### C01 — P1 — La sonda può chiudere PASS con conformità alternativa irrisolta (residuo R04)

**Codice:** {link('ledger.py:221',H/'ledger.py',221)}–228, in `_ready`, verifica soltanto il successo del ciclo primario/remediation per la sonda e il successo della sonda per il gate. Non controlla l’alternativo già avviato. Per contro, righe 216–218 impediscono ogni ulteriore richiesta producer dopo l’avvio della sonda: il ciclo incompleto resta anche bloccato dal nuovo ordine.

**Prova X01:** otto conformità primarie completate; una richiesta alternativa in INTENT; riapertura del ledger; tre richieste sonda completate. Il candidato registra `outcome:budget_probe` e `frozen_gate`, consumo 12, con **un intento alternativo ancora irrisolto**. Nessun errore. **Prova X02 sul runner ordinario:** otto risposte primarie, timeout sulla prima alternativa, poi `run_budget_stage`; tre invii consumer e stato `FROZEN_FOR_STABILITY_GATE`, benché l’alternativo abbia una richiesta FAILED e nessun outcome.

La conformità alternativa è opzionale prima dell’avvio; queste prove la avviano esplicitamente nello stesso pilot. Non esiste un evento di esclusione/abbandono approvato che permetta di ignorarla. Non si sta anticipando la futura scelta del modello alternativo D9: il difetto riguarda lo stadio già offerto dal ledger. La regola dichiarata che i producer precedano sonda/gate e che gli irrisolti blocchino la transizione non è applicata a tutti gli stadi. Il contatore non si azzera; è la precedenza a essere aggirata.

**Evidenza:** osservazioni X01/X02 in {proof('extended.json')}; SQLite e artefatti completi in `extended_fixtures/test_X01_incomplete_alternate_blocks_probe/` e `extended_fixtures/test_X02_failed_alternate_blocks_real_consumer/runner/`. Chiusura R04 solo parziale.

### C02 — P1 — N48 è regredito: l’errore di trasporto non alimenta più T3/T6 (residuo R07)

**Codice:** {link('runtime.py:77',H/'runtime.py',77)}–80 marca FAILED e solleva sempre; {link('run_pilot.py:461',C/'studio2/fase03/run_pilot.py',461)}–466 interrompe il loop senza trasformare il tentativo in invalidità per il valutatore. `return_error_record` resta nella firma a riga 335 ma non è usato. {link('ledger.py:415',H/'ledger.py',415)} esige tutte foglie COMPLETED per PASS, anche per il gate, e non contempla l’invalidità di trasporto ammessa da T3.

**Fonte normativa esatta:** piano rev.10 a `6aaa5b3eebfed4ba502c25c0443caabd0051af21`, `PIANO_STATISTICO.md` riga 831: “Le invalidità, incluse quelle di trasporto, restano nel denominatore”; righe 871–875: zero ripetizioni del gate, invalidità in T3 e T6. Fonte conservata in {link('PIANO_STATISTICO.md',H/'non_ok_20260915/evidence/sources/6aaa5b3e_PIANO_STATISTICO.md',831)}. Un errore di trasporto non è una risposta grezza inventata: può essere un evento invalido esplicito, con raw assente e consumo conservato.

**Prova X03:** pipeline producer→prepare→sonda autentica con stub; timeout solo sul secondo tentativo gate. Osservati 13 intenti cumulativi (8+3+2), una sola risposta gate registrata, nessun riepilogo T3/T6. Il tentativo invalido rimane contabile ma **non entra nel denominatore della metrica**. Il risultato atteso del gate completo con gli altri 119 stub validi è T3 119/120 e divergenza nella tripletta interessata, `R3_REQUIRED_PENDING_FEASIBILITY`, senza retry o GO. La prova fallisce perché non viene prodotto alcun risultato.

**X23:** `--resume` non reinvia il tentativo incerto (corretto), ma anche dopo una riconciliazione zero-token esplicita il gate rimane senza outcome; il percorso non può completare la valutazione. I test sostitutivi dichiarati per N48 verificano contatore FAILED/assenza retry, non la semantica originaria. Il contratto nuovo e il report dichiarano l’interruzione, ma non forniscono una decisione normativa che autorizzi la sostituzione. I tre file metriche invariati non riparano il collegamento del runner. Chiusura R07 incompleta.

### C03 — P2 — Il riepilogo producer sottoconta le richieste dopo retry (residuo contabile R07)

**Codice:** {link('producer_probe.py:181',C/'studio2/fase03/producer_probe.py',181)}–183, `provider_requests=len(records)` conta le otto foglie valutate anziché tutti i tentativi dello stadio. Il riepilogo così prodotto viene anche vincolato all’outcome del ledger.

**Prova X15:** timeout alla seconda richiesta, prova zero-token locale di fixture, retry esplicito e completamento degli otto casi. Stub = **9 invii**; ledger = **9 richieste**, di cui **1 trasporto**; riepilogo `PASS` = **provider_requests: 8**. T9 può correttamente avere otto coppie valutabili dopo esclusione dell’errore zero-token, ma il denominatore separato delle chiamate deve conservarsi (piano rev.10, tabella T9 riga 834 e contabilità §11.1). `valid_first_attempts=8` non giustifica chiamare 8 il numero di richieste provider.

Le quote SQLite restano corrette: non è dimostrato un aggiramento della riserva tramite questo riepilogo. È dimostrata una discordanza nell’artefatto consumabile/reportabile. Evidenza X15 in {proof('extended.json')} e copia del summary/ledger nella fixture relativa.

## Consegna, limiti e stato finale

**Verdetto: NON OK limitato al candidato offline esatto.** R01/R02/R03/R05/R06/R08/R09/R10 hanno chiuso gli attacchi originari verificati entro il perimetro dichiarato; R04 e R07 restano parziali per C01–C03. Le prove positive dichiarate sono riproducibili, ma non autorizzano a dichiarare chiusi tutti i rilievi o equivalente N48. Nessun difetto è stato corretto in questa review.

D9 è **già decisa dall’autore**: 122B producer principale e consumer, 27B producer alternativo per una libreria completa di 16 insight, Terra soltanto storico descrittivo interno. La proposta Terra precedente è superata. Rimangono separati: recepimento **eseguibile** D9 sui propri byte, ordine label 1a ancora non approvato, insight reali, qualificazione servizi/tokenizer/identità/capienza, T5 con margine 20% e autorizzazione pilot. Il candidato storico deve restare UNDECIDED/SUSPENDED: lo è e i suoi ingressi eseguibili sono bloccati. Nessun trasferimento di OK al futuro delta o dal solo raccordo metriche; nessun freeze o GO.

File del verbale e prove: `{E}`. Comandi riproducibili in {proof('COMANDI.md')}. `SHA256SUMS` impronta i file regolari della consegna; `EVIDENCE_INVENTORY.json` distingue copie e symlink esterni. Gli hash del verbale e del manifest sono comunicati fuori dal verbale per evitare autoreferenze. Le snapshot delle fixture preservano i byte originali: alcuni riferimenti assoluti puntano ai temporanei del run, poi rimossi; la copia fedele è in `runner/`, e gli script ricreano nuove fixture per riprodurre. Non eseguire gli script storici nell’acquisizione tracciata o nelle prove originali.

Letture: codice e test pertinenti dell’harness/runner, manifest/inventari e fonti esatte R4/03.7/baseline/piano rev.10, prompt/regole e rapporti di consegna. Ordine di alcune centinaia di kB di testo pertinente; file voluminosi verificati meccanicamente per hash e identificativi. Nessuna rilettura integrale della letteratura, nuova analisi scientifica o incorporazione dei delta paralleli.
'''
(E/'VERIFICA_CORREZIONI_HARNESS_03_10.md').write_text(report)
print(len(report.encode()),'bytes')
