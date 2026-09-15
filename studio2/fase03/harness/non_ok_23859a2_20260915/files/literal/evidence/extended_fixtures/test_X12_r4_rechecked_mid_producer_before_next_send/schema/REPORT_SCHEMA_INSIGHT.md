Formato pseudolabel CONFERMATO: `S2-CLS-[A-Z0-9]{5}`; 03.7 non deve rigenerare per questa sotto-fase.

# Revisione 4 — correzione del contratto della label `Normal`

Data 2026-09-14. Profilo implementativo; esecutore: Codex, agente basato su GPT-5,
in questa finestra. Stato: **pending di verifica indipendente**; non è stato eseguito R4-V
e non viene emesso alcun verbale di approvazione.

## R4.1 Risultato

`validator.py::context_check` valida ora le sole otto chiavi di `owners` con la regex
`S2-CLS-[A-Z0-9]{5}`, mantenendo l’assegnazione biunivoca a `agent_1`…`agent_8`, e richiede
separatamente `normal_label == "Normal"`. Prima applicava la regex anche alla nona label e
accettava soltanto un sentinel opaco, in conflitto con 03.7. Tutti gli altri controlli del
contesto sono invariati.

La fixture non inventa più nove sentinel: carica `PSEUDOLABEL_MAP.json` e
`AGENT_ASSIGNMENT.json` reali dal commit di `main`
`a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155`, verifica che il tag congelato 03.7 sia
peeled a `c16b533016db4617deb1ba96853253f117e8e32b`, che questo ne sia antenato, che i byte
coincidano col tag e che le impronte siano rispettivamente `b0ce81d…` e `df74342…`.
Sono coperti: PASS del contesto reale; FAIL per sentinel opaco, `normal`, `NORMAL`, `Normal `
e owner `Normal`; uso di `Normal` nel campo metadata `pseudolabel` dello scanner.

Lo scanner resta confinato ai record insight e non scansiona il dizionario di contesto.
Nel record, `pseudolabel` è escluso dal controllo lessicale di neutralità, mentre la narrativa
continua a vietare `Normal`; lo schema dell’insight rifiuta comunque `Normal` come pseudolabel.
Restano quindi 16 insight: due per ciascuna delle otto classi fault, nessuno per Normal.

## R4.2 Test effettivi

- Suite completa 03.12 in venv Python 3.13.15/jsonschema 4.26.0: **25 PASS, 0 FAIL,
  1 SKIP su 26**. Lo SKIP è `test_real_offline_qwen`, perché manca lo snapshot pinnato.
- Regressioni `studio2/fase03/tests`: **16 PASS, 0 FAIL, 0 SKIP**.
- Primo tentativo con Python di sistema: non qualificante, **46 FAIL, 6 ERROR, 1 SKIP su 26**,
  causati dall’incompatibilità x86_64/arm64 dell’estensione `rpds`; registrato senza
  trasformarlo in un esito del contratto.
- `docs/test_explanation.py` prima e dopo la modifica: **14 FAIL, 1 SKIP su 35**,
  con gli stessi identificativi; nessuna regressione documentale.

Il log R4 è `TEST_RESULTS_rev004.txt`. La precedente qualifica Qwen della revisione 3 resta
storica e non qualifica R4. Comando riproducibile sul server:

```bash
QWEN_TOKENIZER_SNAPSHOT=/percorso/snapshots/017b9c7af6b5689d5dd426a76e0bc077eb5ca20a /percorso/python -m unittest studio2.fase03.schema_insight.test_validator -v
```

## R4.3 Perimetro, residui e freeze

Modificati per R4: `validator.py`, `test_validator.py`, `TEST_RESULTS_rev004.txt`, questa
decisione, questo report, `SCHEMA_FREEZE.json` e `PROPOSTA_TAG_SCHEMA_INSIGHT.md`.
Non sono stati modificati schema JSON, cap, regex, leakage rules, scanner, diff, harness,
artefatti 03.7, piano, walkthrough o artefatti del primo studio. Il prompt non tracciato
`sottofase_3_12_verifica.md` è preesistente, preservato e fuori dal commit.

Manifest revisione 5, contratto revisione 4, stato
`frozen_pending_independent_verification`; `previous_manifest_sha256` è l’impronta dei byte
del manifest rev. 4: `d6ef52de0f573edf3e5d6eb5ad3530400c5f63e6bcfa6579a93f21fdfb8865b5`.
Il vecchio target `e058cb0` è superato. I nuovi artefatti sono identificati dal manifest rev. 5;
lo SHA del commit che li contiene viene riportato nella consegna e nella futura riverifica,
senza auto-riferimenti circolari in questi documenti.

Resta necessaria la verifica indipendente R4-V. Resta inoltre da eseguire sul server il test
col tokenizer pinnato aggiornato; non è attestato in questa revisione. Nessun push, merge, tag,
produzione di insight, inferenza o simulazione è stato eseguito.

---

# Report sotto-fase 03.12 — schema degli insight

## 1. Riassunto e risultati

Eseguito il prompt trovato in `studio2/fase03/schema_insight/sottofase_3_12.md` della copia
principale: il percorso richiesto `piano_statistico/sottofase_3_12.md` non esisteva.
Worktree `/Users/luker/fot-tep-schema-insight`, branch `codex/studio2-schema-insight`,
base `d815ce9` perché origin/main osservato (`b7f359f`) non conteneva quel commit.
La copia principale e il batch MATLAB non sono stati modificati.

Ordine eseguito: decisione pre-specificata → implementazione e test → manifest delle impronte.
Schema v1.0.0: stessi sei campi, tutti obbligatori; 2 insight/fault, 16 globali, 14 peer.

| Campo | Tipo | Origine | Cap | Fonte |
| --- | --- | --- | --- | --- |
| insight_id | string | verbalizzatore | S2-INS- seguito da 3 cifre (10 caratteri) | preflight; scelta di progetto |
| source_agent | string | verbalizzatore | agent_1…agent_8 (7 caratteri) | preflight; piano §8.1 |
| pseudolabel | string | verbalizzatore | 12 caratteri, regex confermata | interfaccia preflight/03.7; D10 |
| evidence_scope | string non vuota | verbalizzatore | 240 caratteri, 64 token | 240: preflight; 64: scelta di progetto |
| variable_ids | array di stringhe uniche | verbalizzatore | 1–8 ID; XMEAS(1…41), XMV(1…12), massimo 9 caratteri/ID | preflight; limiti TEP, scelta di progetto |
| observed_pattern | string non vuota | producer | 800 caratteri e 192 token | PREFLIGHT_03_0, scelta di progetto motivata da §8.9 |

Limite record canonico: 1400 caratteri/384 token; tutti i cap token usano Qwen revisione
`017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, encode senza special token.
I valori nuovi sono scelte di progetto, non soglie validate empiricamente.
Rispetto allo schema corrente: limiti TEP sugli ID, controllo whitespace, cap scope/record,
confronto dei campi fissi con manifest fidato, anti-leakage, ID narrativi dichiarati e letterali,
metriche per producer/condizione e diff su file canonici B→E con hash e offset dei byte modificati.
Il significato scientifico della narrativa non è verificato dal controllo strutturale.

Interfaccia 03.7: owner, Normal e mapping E sono input esterni; nessuna assegnazione creata.
Interfaccia 03.10: adottare schema/validatore dopo verifica, aggiornare hash di preflight,
collegare manifest dei campi fissi, validare librerie omogenee, applicare E dopo filtro peer,
registrare raw/log per insight e metadati API, rimisurare capienza sui prompt reali.
`protocol.py`, `run_pilot.py`, `prepare_gate.py` e gli schemi correnti non sono modificati.

## 2. File toccati

- `studio2/fase03/schema_insight/DECISIONE_SCHEMA_INSIGHT.md`: decisione, fonti, cap e integrazione proposta.
- `studio2/fase03/schema_insight/insight_v1.schema.json`: nuovo schema strutturale versionato.
- `studio2/fase03/schema_insight/validator.py`: libreria e CLI, tokenizer offline, diff B/E e metriche.
- `studio2/fase03/schema_insight/leakage_rules_v1.json`: dizionario D1, meccanismi e nomi fisici vietati.
- `studio2/fase03/schema_insight/test_validator.py`: fixture sintetiche e test degli invarianti.
- `studio2/fase03/schema_insight/requirements.txt`: dipendenze allineate al preflight.
- `studio2/fase03/schema_insight/TEST_RESULTS.txt`: esiti storici della prima verifica locale, invariati.
- `studio2/fase03/schema_insight/TEST_RESULTS_qwen.txt`: log originale della qualifica sul server.
- `studio2/fase03/schema_insight/SCHEMA_FREEZE.json`: versione, commit, catalog tag e impronte.
- `studio2/fase03/schema_insight/REPORT_SCHEMA_INSIGHT.md`: questo report, senza replica HTML prevista.
- `studio2/PROVENIENZA.md`: sola nuova sezione in coda, fonti originali con commit e SHA-256.

## 3. Esecutore e profili

Codex, agente basato su GPT-6, questa finestra; profilo decisionale per il contratto,
implementativo per codice e test. Nessun subagente o verificatore indipendente invocato.
Non è disponibile un identificativo più specifico del modello da attestare nel report.

## 4. Fuori perimetro e limiti

Zero chiamate LLM e zero simulazioni. Nessuna produzione insight, selezione di valori delle
pseudolabel, owner o derangement scientifici. Nessun push, merge, tag o aggiornamento walkthrough.
Lo scanner lessicale non dimostra l'assenza di qualsiasi parafrasi; richiede revisione indipendente
su copertura e falsi positivi. Non verifica supporto empirico/EFT né opacità dell'assegnazione.
Il contatore Qwen controlla le due impronte tokenizer del preflight prima del caricamento,
usa local_files_only=True e trust_remote_code=False. Lo snapshot non è disponibile su questo
computer: nella prima esecuzione locale il test reale era saltato. Il successivo test sul server
albireo, eseguito dall’autore sul commit 924ec3d, è riuscito: log originale conservato senza modifiche
in `TEST_RESULTS_qwen.txt` (20 PASS, zero skip, 4,107 secondi).
Le prove esatte ai confini dei cap usano tuttora un contatore iniettato. Il test Qwen reale
valida la libreria sintetica contro gli asset pinnati: non prova l’ottimalità scientifica dei cap
né la capienza dei prompt reali. Modello e tokenizer non hanno effettuato inferenze.

## 5. Decisioni e verifiche ancora necessarie

Verifica indipendente in altra finestra di decisione, implementazione, scanner e impronte.
Qualifica col tokenizer pinnato completata sul server dall’autore. Comando per ripeterla:

```bash
QWEN_TOKENIZER_SNAPSHOT=/percorso/snapshots/017b9c7af6b5689d5dd426a76e0bc077eb5ca20a python -m unittest studio2.fase03.schema_insight.test_validator -v
```

Uso CLI, dalla radice del worktree:

```bash
python -m studio2.fase03.schema_insight.validator library libreria.json --context contesto.json --tokenizer-snapshot /percorso/snapshot
python -m studio2.fase03.schema_insight.validator insight insight.json --context contesto.json --tokenizer-snapshot /percorso/snapshot
python -m studio2.fase03.schema_insight.validator diff B.json --after E.json --mapping mapping.json --agent agent_1 --context contesto.json --tokenizer-snapshot /percorso/snapshot
python -m studio2.fase03.schema_insight.validator metrics eventi.json --context contesto.json --tokenizer-snapshot /percorso/snapshot
```

`contesto.json` contiene `owners` (label fault → agente), `normal_label` e `fixed`
(lista dei 16 record di soli cinque campi deterministici). `libreria.json` è un array.
B/E devono essere i byte di `canonical(array)`, senza newline finale; omettere `--agent`
soltanto per un audit globale a 16 insight. `eventi.json` segue il contratto della decisione.
Gli errori CLI sono JSON tipizzati, exit 1; esito valido exit 0. L'help non carica il tokenizer.

All'autore resta l'autorizzazione al tag proposto `studio2-fase03-schema-insight-frozen-001`
dopo OK indipendente e qualifica del tokenizer; eventuali correzioni richiedono nuova revisione.
L'adozione in 03.10 e la verifica di capienza reale precedono il pilot scientifico.
La Fase 03 non è chiusa e il manifest pending non autorizza produzione di insight.

## 6. Verifiche

Prima esecuzione sul Mac: **19 PASS, 1 SKIP**, zero fallimenti.
Qualifica successiva su albireo: **20 PASS, zero SKIP**, in 4,107 secondi;
`test_real_offline_qwen` eseguito e riuscito. L’autore ha fornito il log originale allegato;
il commit 924ec3d è attestato dall’output di checkout condiviso nella conversazione, non dal solo log unittest.
Ambiente dichiarato nel comando: `/home/luca/fot-exp2/env-vllm/bin/python`;
checkout `/home/luca/fot-phd-schema-insight`. Nessun accesso remoto da questa finestra.
16 test di regressione dell'harness: **16 PASS**.
`python3 docs/test_explanation.py`: prima **14 fallimenti/35 test, 1 skip**;
dopo **14 fallimenti/35 test, 1 skip**, con gli stessi 14 nomi di test falliti.
Questo test non copre §14 né i file v2 e non sostituisce i test nuovi.
Il primo tentativo sul Python di sistema era fallito per rpds di architettura incompatibile;
risolto con venv isolato Python 3.13.9 e jsonschema 4.26.0, senza cambiare l'ambiente principale.
`git diff --check` passato. Nessuna coppia MD/HTML normativa toccata.

Letture mirate: Prompt_LLM, Fase_LLM, Commit_LLM, MAINTENANCE; piano §§8.1/8.4/8.7/8.9
integrale e D10/D12; schede ACE/Fed-ICL/SYNAPSE/EviFDD nel corpus; preflight, stato implementazione,
config, schema insight/output, funzioni insight e tokenizer, test protocollo, catalog D1,
perimetro Q8, apertura sotto-fasi; walkthrough studio2 per orientamento e storico insight nelle
due esposizioni del primo studio. Costo indicativo delle letture: circa 25–35 mila token;
nessuna ricerca web o lettura in blocco dei paper.

## 7. Commit e freeze

Commit decisione: `b6441e9` — `studio2(fase03): pre-specifica lo schema insight e le interfacce 03.12`.
Commit implementazione: `43eadb6` — `studio2(fase03): implementa validazione insight diff byte e metriche offline`.
Terzo commit `924ec3d`: `studio2(fase03): registra freeze pending e report dello schema insight`;
contiene questo report e SCHEMA_FREEZE.json. Il suo hash si ricava da Git senza auto-riferimenti.

Stato del manifest: `frozen_pending_independent_verification`.
Commit sorgente e checkout qualificato: `924ec3d446bb6860123b82c8685bbdcbfc8f90a0`.
Manifest revisione 2: include il log Qwen e conserva l’impronta del manifest precedente.
Commit della qualifica: `studio2(fase03): qualifica i cap token dello schema col tokenizer pinnato`
(hash reperibile dalla storia Git, per evitare auto-riferimenti).
SHA-256 del manifest: `472f1b01b09f189e724a1fb11b96ab28b303b1914b4601b576cf5de91292428c`.

| Artefatto | SHA-256 |
| --- | --- |
| `DECISIONE_SCHEMA_INSIGHT.md` | `205805572ea2828e77d077b460f62d3bc3711c4c1662dbbc4da2a89749fe10c3` |
| `insight_v1.schema.json` | `15e0d29e033c1d699d4f1114b5fdf378ad1cea8398c89b133403a92983229de6` |
| `validator.py` | `3af8625d39132fe4fe07cc6d7cdb313e64c96b061f635b5fb82b631bbbb0fc7f` |
| `test_validator.py` | `3818308ef6be6b766b409e869cc2e58bde7be1a4995d52cc534819403a68ef0e` |
| `leakage_rules_v1.json` | `2aba741047afa99830605227a5ed4e7e8553b3c48bf819f86ec123eb8b814f4b` |
| `requirements.txt` | `1e53672145c42bd48e9e2f8540d89a224be2b6d8665599272ccb7506c238de86` |
| `TEST_RESULTS.txt` | `9c8c7d51149cb033e584166ced334ee233a27622314d99192b4b8649640ae0b0` |
| `TEST_RESULTS_qwen.txt` | `7113bf87d758e2dd0bbb3fed5fecfac7aa0a4629825db69c5046ebef5db233e0` |

Le impronte sono dei byte su disco e sono ripetibili; report e manifest sono esclusi dal proprio
manifest per evitare dipendenze circolari. Nessun tag creato; verifica indipendente ancora pendente.
