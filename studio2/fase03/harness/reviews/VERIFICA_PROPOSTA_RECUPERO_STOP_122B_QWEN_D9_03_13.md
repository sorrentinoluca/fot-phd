# Verifica indipendente proposta di recupero STOP 122B — Qwen D9 03.13

Review read-only eseguita nella worktree indipendente `/Users/luker/.codex/worktrees/b567/fot-tep`
(HEAD staccato `15e56a89`) sul candidato in `/Users/luker/.codex/worktrees/dd86/fot-tep`.
Ledger predecessore aperto solo con SQLite `mode=ro&immutable=1`. Nessuna implementazione,
correzione, tunnel, chiamata, modifica di ledger o JSON privati. Nessun raw, URL o credenziale
riportato. Le verifiche git hanno usato solo comandi sugli oggetti (`cat-file`, `diff-tree`,
`ls-tree`, `hash-object`); nessun `index.lock` residuo.

## Verdetto

**OK CON SCELTA AUTORE PENDENTE.** La proposta è strutturalmente e contabilmente ammissibile come
base non autorizzata: usa solo evidenza durevole già acquisita, non propone remediation del prompt,
non rende gratuita né riutilizza la chiamata consumata, e i budget dei due rami sono corretti al
ricalcolo indipendente. La classificazione T9 non è determinata dal contratto congelato e resta
una decisione normativa dell'autore; questo verbale indica la via scientificamente preferibile
(§4) senza sostituirsi a tale decisione. Nessuna implementazione o chiamata è autorizzata.

## 1. Commit, tree, delta, hash

| Controllo | Osservato |
|---|---|
| HEAD dd86 | `6e15fe59fe7b2f69c3e74e0bbf344985fa696c36` ✅ («docs: propose reviewed recovery for 122B stop») |
| tree | `7f5ba92c81bda1eaa0e13b42bc9da807d472d2c5` ✅ |
| parent | `0523c9279a3e760bd001daf399267c642deda02d` ✅ (commit STOP verificato in V2) |
| delta `0523c92..6e15fe5` | esattamente 3 file aggiunti (772 righe), nessuna modifica/cancellazione ✅ |
| proposta MD (worktree = blob nel tree) | `496e4ac70eb3b6a28ff3f960eba0a9d207d58decd04e3ef3ba09cdfad8283778` ✅ |
| proposta JSON | `77d72204d53e4706d7e93dc579532a9f148175e3d7daff75d0467c93eee03624` ✅ |
| copia review V2 in `reviews/` | `f19da5e4ec332a386fad8780dbf1db44188353fc9180ba1c0eae87d073ec924f` = sorgente in b567 ✅ |
| `.py`/`.json`/`.jinja` di fase03 nel worktree vs tree `7f5ba92c` | identici (nessun file di codice o configurazione toccato) ✅ |
| ledger predecessore | `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`, mtime 01:28:45Z, WAL 0 byte, invariati prima/dopo ✅ |
| JSON privati `execution/` | mtime 00:28 (provider/servizi) e 01:23 (config/autorizzazione), tutti anteriori allo STOP; nessun nuovo file ✅ |
| autorizzazioni | nessuna nuova (`authorization_created=false`, nessun file nuovo in `execution/`) ✅ |

## 2. Uso dell'evidenza già acquisita

Ogni campo della tabella «Campo durevole» è stato riconfrontato con il ledger: request/stage/quota,
`COMPLETED`, alias, fingerprint atteso `null` e osservato, `reasoning` 8 670 caratteri **e** 8 670
byte UTF-8 (ricalcolato), `content` null, `finish_reason=length`, uso 1 395/2 560/3 955, classe
`structure` con «JSON value is empty or not text», accounting locale = server ✅. Gli hash raw,
record, commitment e binding coincidono con quelli verificati in V2 ✅. Il digest canonico
dell'oggetto `qualification_supplement_candidate` ricalcolato con `canonical_json` è
`d180061348b15bb0322cb75ae700bb97b1328994c8d572c98741455d5b0ef579` = dichiarato ✅.

La proposta distingue correttamente: fingerprint come valore opaco osservato una volta (nessuna
inferenza su versione vLLM «nonostante il testo del valore», served revision, quantizzazione,
parser); campo `reasoning` osservato come fatto strutturale senza lettura semantica; capacità
**locale** del template pin-nato; supporto **server** dichiarato `NOT_PROVEN` ✅. Le versioni
dell'ambiente locale (Python 3.13.9, transformers 4.57.6, openai 1.109.1) non sono riverificabili
dall'ambiente di questa review; Python 3.13.9 coincide con i manifest precedenti. Non bloccante.

## 3. Controllo statico template e client

- `chat_template.jinja` dello snapshot `a099dee7…` (SHA-256 `a4aee8af…f715`, ricalcolato ✅), righe
  147–153: con `add_generation_prompt` il prefisso è `<think>\n` per default e
  `<think>\n\n</think>\n\n` se `enable_thinking is defined and enable_thinking is false`.
  La capacità locale è reale e deterministica ✅. Il comportamento di `apply_chat_template` con
  kwargs non è stato rieseguito qui (transformers assente), ma il template lo prevede.
- `producer_probe.provider_config` respinge qualunque chiave oltre a
  `{name, base_url, model, max_tokens, expected_max_model_len, identity_sha256, expected_response,
  tokenizer}` più `{temperature, seed, thinking_token_budget, tokenizer_accounting}`: `extra_body`
  è rifiutato ✅. `d9.generation_kwargs` ammette solo `max_tokens/seed/thinking_token_budget`
  (+ `temperature` per 27B) e produce `extra_body` solo per `thinking_token_budget` ✅. Il trasporto
  invia `messages` strutturati con `response_format json_schema strict` e nessun controllo thinking ✅.
  Quindi `extra_body.chat_template_kwargs.enable_thinking=false` è oggi **non eseguibile**, come
  dichiarato ✅.
- `TokenizerAccountingGuard.validate_producer_response` renderizza con
  `apply_chat_template(messages, tokenize=True, add_generation_prompt=True)` senza kwargs: con un
  server che applicasse `enable_thinking=false` il conteggio locale differirebbe da `usage.prompt_tokens`
  e il guard produrrebbe `FATAL_ACCOUNTING_ERROR` con STOP durevole. La richiesta della proposta
  (stessa kwarg nel guard, legata a binding e commitment) è corretta e necessaria ✅.

## 4. Classificazione T9

Testi congelati controllati: PIANO_STATISTICO §11 (T9: 16 insight in 8 chiamate al primo tentativo;
una sola remediation per classi 1–4; «denominatore chiamate conservato separatamente») e §11.1;
DECISIONI_AUTORE_03_8 (classi 1–5, regola B2-bis, divieto di riclassificare per un diff
«plausibile»); CONTRATTO_ESECUZIONE_E_RIPRESA («una risposta con identità mancante/errata resta una
risposta ricevuta e sospende il pilot, con raw conservato»; «la sospensione per cambio d'identità non
ha uno sblocco automatico»); SPECIFICA_HARNESS §4 («identità, …, limiti e fingerprint devono essere
congelati dopo una decisione esplicita e qualificati sul servizio reale»).

Constatazioni:

- Il testo congelato prevede una sola esclusione esplicita dal denominatore T9 (classe 5 con prova
  zero-token) e non dice se una risposta ricevuta ma respinta dal guard d'identità entri o no nel
  denominatore. La proposta lo afferma correttamente: **non univoco** ✅.
- Sequenza durevole confermata: binding immutabile → intent → risposta completa e addebitata →
  `identity_valid=false` → evento `suspended` create-once; nessun evento `outcome:*` ✅.
- `ANTECEDENT_QUALIFICATION_CONFIGURATION_FAILURE`: coerente con SPECIFICA_HARNESS §4 (il fingerprint
  fu congelato a `null` da una qualificazione non generativa che lo elencava come `not_exposed`, cioè
  non «qualificato sul servizio reale») e con la sequenza (il guard d'identità è una precondizione
  logicamente anteriore alla valutazione dell'output). La chiamata resta in S e non è gratuita ✅.
- `FIRST_INVALID_T9_OBSERVATION`: coerente con la lettura letterale «risposta ricevuta»; conduce però
  a un vicolo cieco già riconosciuto: la remediation richiede un difetto del prompt dimostrato (qui
  l'evidenza è di interfaccia) e il harness richiede `outcome:producer_conformity` FAIL, assente.
  L'esito residuo sarebbe la decisione D9 sull'esito negativo del producer 122B.
- Post hoc: la scelta avviene inevitabilmente dopo l'osservazione; non è per convenienza se poggia su
  una regola pre-esistente (qualificazione richiesta) e non sul contenuto dell'output, se la
  chiamata resta addebitata ed esclusa dalle librerie, se il prompt resta invariato e se la decisione
  è scritta prima di ogni nuova materializzazione. La proposta rispetta queste condizioni ✅.

Giudizio del verificatore: la via **scientificamente preferibile è l'antecedente di
qualificazione/configurazione**, perché l'osservazione non è stata prodotta sotto la configurazione
congelata e qualificata che il protocollo esige (fingerprint non qualificato generativamente, canale
reasoning non esposto né controllato); trattarla come osservazione T9 attribuirebbe al prompt o al
modello un difetto dell'interfaccia. La scelta resta normativa dell'autore e va messa per iscritto
con la motivazione, la conservazione della chiamata nel denominatore «conservato separatamente» e
il riporto nel paper.

## 5. Nessuna remediation del prompt; invarianti

`remediation_t9_001_created=false`, `prompt_diff_proposed_for_thinking=false`; il diff candidato
tocca solo documentazione servizio, `identity_sha256`, `expected_response.system_fingerprint` e
`extra_body` del provider ✅. Schema, validatore, input, otto casi, ordine, prompt e
`max_tokens=2560` dichiarati e verificati invariati (nessun file di codice/schema nel delta) ✅.
La chiamata consumata: `completed_122b_retry_eligible=false`, non `ZERO_TOKEN_PROVEN`, inclusa in
S=5, riuso e accettazione retroattiva sotto nuova identità esplicitamente vietati ✅.

## 6. Vie ledger

- Il meccanismo esistente di storico esterno è cablato a **esattamente 4 righe** (`d9.py`: «mapping
  must contain exactly four requests»; `ledger._validated_external_history`: `len(rows) != 4`,
  `count: 4`, riga 1 obbligatoriamente `HISTORICAL_OUTCOME_UNCERTAIN`). Un lineage S=5 richiede
  quindi la modifica harness dichiarata dalla proposta ✅. `ledger.snapshot().planned_maximum` =
  152/160 + storiche: con 5 storiche dà 157/165, coerente con §7 ✅.
- `_prerequisites` rifiuta ogni stage in presenza di `suspended:`; non esiste codice di ripresa.
  La disposizione overlay nello stesso ledger richiederebbe di toccare prerequisiti, outcome e guardie
  remediation attorno a un binding immutabile con fingerprint `null` e a un record invalido
  completato: l'audit dovrebbe distinguere due contratti d'identità nello stesso contenitore. Il
  successore con predecessore forense immutabile, import exactly-once di 5 identità/disposizioni
  legato a pilot id e SHA-256 del predecessore, con divieto di import selettivo/duplicato/transitivo
  e di reset, è effettivamente più auditabile ✅. La lista `forbidden` copre update/cancellazione
  eventi, rebinding, reset, copia selettiva, azzeramento quote, riuso come retry, reinterpretazione
  del raw ✅.

## 7. Ricalcolo indipendente dei budget

Input congelati (`call_budget`): conformità 8, alternativo 8, sonda 3–9, gate 120, riserva
`8·r + t ≤ 15` con `r ∈ {0,1}`, sonda ≤ 7 trasporti cumulativi, gate 0 retry, hard stop 200, S=5.

| Voce | Antecedente (A) | Prima invalidità T9 (B) |
|---|---:|---:|
| base futura con alternativo | 8+8+(3–9)+120 = **139–145** | 0+8+(3–9)+120 = **131–137** |
| base futura senza alternativo | **131–137** | **123–129** |
| remediation | opzionale 8 | obbligatoria 8 (oggi bloccata) |
| futuro senza trasporto (con alternativo) | 139–145 (r=0) / 147–153 (r=1) | 139–145 |
| trasporto massimo con remediation preservata/usata | 7 | 7 |
| massimo futuro con / senza alternativo | 145+15 = **160** / **152** | 137+8+7 = **152** / **144** |
| cumulativo con S=5, con / senza alternativo | **165** / **157** | **157** / **149** |
| margine su 200 | **35** / **43** | **43** / **51** |

Tutti i valori della proposta coincidono con il ricalcolo ✅. Rilievi non bloccanti sull'aritmetica:

1. Nel ramo A il massimo cumulativo passa da **164** (prespecificato:
   `cumulative_planned_max_with_historical_and_shared_reserve`) a **165**: la chiamata invalida non è
   né base (la conformità viene rieseguita per intero) né riserva (non è zero-token, non è
   remediation). È di fatto una quinta voce «addebitata una volta», analoga alle storiche, ma con
   modello nominale 122B mentre `historical_nominal_model` recita `27B`. La proposta lo tratta
   correttamente via S=5, ma la revisione esplicita dei campi prespecificati (`historical_…_charged_once`
   4→5 o nuovo campo di lineage, massimi cumulativi 164→165) deve far parte della decisione scritta
   dell'autore e della configurazione materializzata, non restare implicita.
2. Nel ramo B le 7 chiamate base di conformità non eseguite sono perse, non trasferibili: la
   proposta lo implica (base primaria 0) ma dovrebbe dichiararlo.
3. Nel ramo B, se la remediation resta bloccata, il futuro del producer 122B è 0 e l'esito passa alla
   decisione D9; la riga «139–145» vale solo se la remediation viene sbloccata da un difetto del
   prompt dimostrato, oggi assente.
4. Rinuncia esplicita alla remediation nel ramo A: fino a 15 trasporti solo in conformità e solo per
   `ZERO_TOKEN_PROVEN`; sonda ≤ 7, gate 0. Coerente con §11.1 ✅.

## 8. Sufficienza dei blocker

I sei blocker (decisione T9, prova server no-thinking, materializzazione con hash derivati, harness
lineage/no-thinking/accounting con test offline, review indipendente, nuovo ACCEPT e nuova
autorizzazione) sono necessari e nel loro insieme coprono il perimetro. Integrazioni raccomandate,
non bloccanti per questo verdetto ma da chiudere prima di qualunque chiamata:

- **Prova non generativa**: la proposta non identifica il meccanismo. Il fingerprint è esposto solo da
  `/chat/completions` (la qualificazione da `/models` lo elenca `not_exposed`) e non è riverificabile
  senza generazione: la prima chiamata del successore è inevitabilmente il test d'identità, fail-closed
  e addebitata. Per `chat_template_kwargs` la configurazione 122B è stata acquisita «senza /tokenize»;
  se non esiste un endpoint non generativo che applichi la kwarg, il blocker va riformulato dall'autore
  (che cosa vale come prova, e che la prima chiamata addebitata possa fallire per identità o kwarg).
- **Perimetro del controllo no-thinking**: P e C condividono il servizio 122B e `validate_config`
  impone `expected_response` identico; la documentazione `thinking` del servizio deve dichiarare che
  `enable_thinking=false` si applica al solo producer e che il consumer (sonda/gate, candidati di
  thinking budget) resta invariato, per non alterare T4 e il freeze della sonda.
- **Adozione del valore osservato una volta come contratto esatto**: scelta fail-closed corretta, ma
  va dichiarata come tale, con la conseguenza che un cambio di fingerprint lato server produce un
  nuovo STOP addebitato.
- **Disposizione riesaminata del predecessore**: il pacchetto di lineage con approvazione scritta è la
  «nuova disposizione riesaminata» richiesta dal contratto; deve dirlo esplicitamente e citare SHA-256
  del predecessore, di questa proposta e delle review.

## Esito

Proposta ammissibile come base non autorizzata; verdetto **OK CON SCELTA AUTORE PENDENTE**.
Questo verbale non autorizza implementazione, materializzazione, sonde o chiamate. Nessun commit,
push, merge o tag; unica scrittura questo file, non tracciato, nella worktree b567.
