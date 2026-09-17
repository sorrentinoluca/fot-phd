# Report di sotto-fase 03.13 — capability pilot Qwen su `pilot-03`

Data: 2026-09-17, Europe/Rome. Report di sotto-fase secondo `docs/MAINTENANCE.md` §8.6. Il verbale
di verifica della sotto-fase sarà `studio2/fase03/pilot/VERIFICA_PILOT_03_13.md` (finestra `b567`):
**non esiste ancora**, e fino al suo OK questo report è una proposta dell'autore della chiusura.
Esecutore: `claude-opus-5` (Claude Cowork), non `gpt-5.6-sol` indicato dal prompt di chiusura.

## 1. Esito

| Voce | Valore | Fonte |
|---|---|---|
| Esito tecnico del pilot | **PASS**, confermato in modo indipendente | [`VERIFICA_ESITO_PILOT_03_13.md`](VERIFICA_ESITO_PILOT_03_13.md), SHA-256 `1ce0a466586a65993d1269476f9de8a4812b9f64a20eae71cd9aec7e8bee4b70`, copia byte-identica del verbale `b567` |
| Gate 40×3 | 120 richieste, 119 valide al primo tentativo, 0 troncamenti; T3 PASS, T4 PASS, T6 valutabile | ledger, `outcome:stability_gate` |
| Divergenza | 1/40, `S2-P03-002`: **di validità** (una ripetizione su tre senza risposta per `APIConnectionError`, unico primo tentativo non valido del gate); le due risposte ricevute concordano su astensione e pseudolabel. Non è una divergenza semantica | verbale `b567` §6.1 |
| R | **R = 3**, obbligatorio per il piano statistico §10.3 | verbale `b567` §8 |
| T5 | **PASS** con W = 7 giorni: `1,20 × T` = 62,69 h (media) e 87,67 h (p95) su 168 h | §6 |
| Decisione dell'autore | **GO del pilot con R = 3**, definitivo dal 2026-09-17 | §7 |
| Fase 03 | **non chiusa** | — |

Il campo durevole `go_final=false` del summary del gate non cambia: il GO è una decisione
dell'autore registrata qui, non una riscrittura dell'artefatto.

## 2. Indice della catena, da `79ce7da` a oggi

Branch `codex/studio2-riconciliazione-stop-contabile` (worktree
`/Users/luker/fot-tep/.worktrees/rem6-riconciliazione`), preceduto dal lavoro nella worktree `dd86`.
I verbali stanno nella worktree `b567` (`/Users/luker/.codex/worktrees/b567/fot-tep/studio2/fase03/harness/`),
fuori da Git; qui ne sono citati nome e SHA-256 al 2026-09-17.

| Commit | Data (ora locale) | Oggetto | Verbale `b567` | SHA-256 verbale | Verdetto |
|---|---|---|---|---|---|
| `79ce7da` | 16/09 20:19 | chiude i bloccanti della materializzazione successor | `VERIFICA_CANDIDATO_79CE7DA_…` | `46a6d426…2f0f` | READY ONLY AFTER FRESH TARGET ID/PATH UPDATE AND RE-REVIEW |
| `a199d6f` | 16/09 20:36 | target fresco `pilot-03` e chiusura deterministica del ledger | `VERIFICA_CANDIDATO_A199D6F_…` | `b4c6a5ec…2581` | ACCEPT WITH NON-BLOCKING FINDINGS |
| `59293f9` | 16/09 23:21 | materializza `pilot-03` ed evidenza offline | `VERIFICA_POST_MATERIALIZZAZIONE_…`; `VERIFICA_AUTHORIZATION_…` | `2e4be510…843e`; `fd2ff243…8867` | OK CON LIMITI — REVIEW PARZIALE; AUTHORIZATION OK |
| `8d8ac60`, `294f154` | 17/09 00:30–00:45 | qualifica tecnica 122B (1 chiamata) | `VERIFICA_ESITO_QUALIFICA_TECNICA_…` | `f4ee983b…1db0` | TECHNICAL PASS CONFIRMED |
| `2a135c2` | 17/09 01:12 | conformità producer 122B (T9) | `VERIFICA_ESITO_T9_PRODUCER_122B_…` | `6f0b5c85…58ff` | T9 PRODUCER STOP CONFIRMED — 2/8 |
| `98dc2b8` | 17/09 09:26 | diagnosi post-FAIL per la remediation | `VERIFICA_FIX_DIAGNOSI_POST_FAIL_03_13.md` | `33375ac9…4279` | ACCEPT WITH NON-BLOCKING FINDINGS |
| `72e20d8` | 17/09 10:02 | primo tentativo di remediation: STOP contabile spurio | `VERIFICA_ESITO_REMEDIATION_…` (versione del mattino) | `f0b9ca37…7552` | NOT CONFIRMED |
| `82a4179` | 17/09 10:30 | corregge lo scoping contabile e la durabilità della diagnosi | `VERIFICA_CORREZIONE_REMEDIATION_…` | `5047a773…a6ff` | OK |
| `4ab1e2e` | 17/09 09:55 | riconciliazione durevole dello STOP spurio (REM-6) | `VERIFICA_RICONCILIAZIONE_STOP_CONTABILE_03_13.md` | `45da4136…51fa` | ACCEPT |
| — | 17/09 12:47 | remediation eseguita dal terminale (fine run; verbale alle 13:02) | `VERIFICA_ESITO_REMEDIATION_…` (versione corrente, stesso nome) | `749dae73…99c2` | REMEDIATION PASS CONFIRMED |
| `3952fb4` | 17/09 11:58 | accettazioni dell'autore e preflight pre-gate (ACC) | nessun verbale dedicato; coperto come parent dalla review REV27B | — | — |
| `20ecfd8` | 17/09 13:16 | revisione approvata della config, riqualifica 27B (REV27B) | `VERIFICA_REVISIONE_CONFIG_RIQUALIFICA_27B_03_13.md` | `70faa3a0…7f99` | NOT CONFIRMED (E4, E20, E26) |
| `d3f8f84` | 17/09 16:03 | rifiuta retry di altro stage e binding su revisione superata | `VERIFICA_FIX_REV27B_E20_E4_03_13.md` | `314665f9…d8cf` | CONFIRMED (E26 dichiarato, non corretto) |
| — | 17/09 18:26 | esito del pilot (sonda + gate) | `VERIFICA_ESITO_PILOT_03_13.md` | `1ce0a466…4b70` | PILOT TECHNICAL PASS CONFIRMED — R3 REQUIRED; T5 NOT ESTABLISHED |

SHA-256 completi dei verbali: `46a6d426aa05f44fda1ea994a89f3d04cede01331ebdc4866be37fd34b252f0f`,
`b4c6a5ec397084d8a787488c3b9f0c2bb3d66d0d56a4cccb1da2e048ed8f2581`,
`2e4be510591e78c4138839442b39c3d08c721846809f0c17dbb9e9381028843e`,
`fd2ff24390fc677bce3c2752f198e12dba48b0ef6bf0e39a419dc19af9998867`,
`f4ee983b9c0f9f7974d06a39f955c67db88a9f57eb29a0a8d0e4182634101db0`,
`6f0b5c850c91fec7945aae0db8f18c3cdf698cbc976e4a280e0b90adc04158ff`,
`33375ac96fcf22d49e2bc91216268eff9d2eb6b4a4b761064882375c72f84279`,
`f0b9ca37d0ab61a37ad0f69fbaee250047725467f0eb21819122b81c78747552` (citato dal manifest di `82a4179`; il file è stato poi sovrascritto),
`5047a773da51fa57ad2a70c896bd83624f4bddeec3a749ef00bcf8ac8880a6ff`,
`45da4136c9e0a3c40f9c4e278dbec24b4853339fb9f46f24752e75a0113a51fa`,
`749dae73fd464a6a9887b7a7cb98c9c9f8ab9aa2a9c3fc90b232171f001a99c2`,
`70faa3a0f7dd7acda459bfe7e723d7f686ef3e443ebd7685a3b3adb44ec27f99`,
`314665f9b5a8dffa7508d303940da34ad95857ae760d2ad7bfa2dfab4aa2d8cf`,
`1ce0a466586a65993d1269476f9de8a4812b9f64a20eae71cd9aec7e8bee4b70`.
La prima chiamata 122B del predecessore è documentata in `VERIFICA_STOP_PRIMA_CHIAMATA_PRODUCER_QWEN_D9_03_13_V2.md`,
SHA-256 `f19da5e4ec332a386fad8780dbf1db44188353fc9180ba1c0eae87d073ec924f`.

Nota: la verifica `b567` usa due volte lo stesso nome file per la remediation; i due SHA sopra
distinguono il verbale NOT CONFIRMED sul candidato `72e20d8` da quello PASS CONFIRMED sull'esecuzione.

### Decisioni dell'autore

| Data (UTC dove registrata) | Decisione | Traccia |
|---|---|---|
| 2026-09-16 | Recupero dello STOP 122B con un ledger successor fresco, lineage S=5 importata una volta, qualifica tecnica separata (1 chiamata), **no-thinking sul producer 122B**, massimo 166/200 | `harness/ACQUISIZIONE_DECISIONE_AUTORE_RECUPERO_SUCCESSOR_122B_QWEN_D9_03_13.json` |
| 2026-09-16 22:04 | Autorizzazione della sola qualifica tecnica | `execution/technical_execution_authorization_03_13.private.json` (`7dcec105…`) |
| 2026-09-17 07:44 | Diagnosi `identifiers` sul FAIL T9 | evento `diagnosis:producer_conformity`, approvazione `3bfba0d7…` |
| 2026-09-17 07:45 | Remediation autorizzata sul diff del template | evento `remediation_authorized`, `5469d14c…` |
| 2026-09-17 10:33 | Riconciliazione dello STOP contabile come difetto dell'harness | evento `stop_reconciled:tokenizer_accounting`, approvazione `2b0f28dc…` |
| 2026-09-17 10:42–11:17 | Sette prove zero-token (2 HTTP 401, 5 errori di connessione) | eventi `reconciled:<id>` |
| 2026-09-17 (pomeriggio) | **Decisione A**: il 27B resta nel pilot; fingerprint riqualificato a `vllm-0.28.0-5fc21ed4`; producer 27B con `enable_thinking=false` e `max_tokens=2560`; consumer invariato | prompt `PROMPT_REV27B_…` e sessione REV27B |
| 2026-09-17 (pomeriggio) | Quota `requalification` (massimo 1) e documentazione del servizio 27B in rev2 | sessione REV27B; report `harness/REPORT_REVISIONE_CONFIG_RIQUALIFICA_27B_03_13.md` |
| 2026-09-17 14:21 | Revisione della config e riconciliazione della sospensione | eventi `config_revision:1` (`a8fb92b1…`), `suspension_reconciled:19a9b372…` (`e5f277cb…`) |
| 2026-09-17 14:35 | Accettazioni pre-gate | `execution/PRE_GATE_ACCEPTANCE_03_13.private.json` |
| 2026-09-17 | **GO del pilot con R = 3**, in applicazione della decisione 11, finestra operativa **W = 7 giorni** | §7 |

## 3. Configurazione finale

| Ruolo | Modello restituito / fingerprint | Controlli di generazione | Note |
|---|---|---|---|
| Producer principale | `qwen3.5-122b` / `vllm-0.27.1-934a3247` | `enable_thinking=false`, `max_tokens` 2560; accounting token esatto | provider `04b2c948…` |
| Producer alternativo | `fot-exp2-consumer` (Qwen3.8-27B-FP8, revisione `017b9c7a…`) / `vllm-0.28.0-5fc21ed4` | `enable_thinking=false`, `max_tokens` 2560, temperature 0, seed 20260829; `thinking_token_budget` rimosso | provider rev2 `27295c25…` |
| Consumer | `qwen3.5-122b` / `vllm-0.27.1-934a3247` | seed 20260829, `thinking_token_budget` 2048, `max_tokens` 2560 (primo candidato della sonda) | `frozen_gate` `de1f59ce…` |

Config finale `c22dca7c70d7e4d8d6044ef9de0c1e4ec03c22059e31e830386b1161b7962075`
(digest contenuto `4b3e3ae6…`), authorization rev2 `3d9f4dae…`, `alternate_placement=pilot`.
Quote: base, `technical` 1, riserva `8r+t ≤ 15` interamente consumata (8+7), `requalification` 1.
Massimo pianificato 167, hard stop 200; consumo cumulativo **161** (156 native + 5 di lineage).

## 4. Esiti (numeri dal ledger)

Dettaglio per richiesta, token, latenze ed eventi in
[`harness/EVIDENZA_PILOT_03_ESECUZIONE_FINALE_03_13.md`](../harness/EVIDENZA_PILOT_03_ESECUZIONE_FINALE_03_13.md).

| Stage | Richieste native | Esito | Numeri |
|---|---:|---|---|
| Qualifica tecnica 122B | 1 | PASS | 42/10 token |
| Conformità producer 122B (T9) | 8 | FAIL | 6/8 valide; 2 classe `identifiers` |
| Remediation 122B | 10 | PASS | 8/8 valide; `agent_1` al terzo tentativo dopo due HTTP 401 zero-token; 16 insight, libreria `c2469737…` |
| Alternate 27B | 14 | PASS | 8/8 valide sui leaf; `agent_1`: 5 zero-token, 1 risposta sospesa (`finish_reason=length`, 2047/2560 reasoning token, JSON troncato), 1 requalification valida; latenza media dei leaf 34,043 s; 16 insight, libreria `f860063b…` |
| Sonda budget | 3 | PASS | primo candidato 2048/2560; 3/3 validi, `stop` |
| Gate 40×3 | 120 | PASS tecnico | 119 valide; astensioni A 6/24, B-LF 18/47, E-LF 12/48; 0 troncamenti; latenza media 26,209 s (120 righe) |

Le due librerie hanno la stessa struttura (16 insight, 128 voci `variable_ids`, 33 variabili
distinte) e lunghezze simili; il confronto è descrittivo (verbale `b567` §4.2) e non è un claim.

## 5. Nota metodi integrata

La bozza `studio2/fase03/NOTA_METODI_03_13_PILOT_QWEN.md` (fuori da Git, nella radice del repository)
è integrata qui con i numeri e con le correzioni segnate; non va riscritta altrove.

**Configurazione dei modelli.** Il pilot usa due producer Qwen serviti da vLLM: un 122B
(`qwen3.5-122b`, fingerprint `vllm-0.27.1-934a3247`, endpoint remoto) e un 27B locale
(`fot-exp2-consumer`, fingerprint `vllm-0.28.0-5fc21ed4`). Entrambi i producer generano **senza fase
di ragionamento** (`chat_template_kwargs.enable_thinking=false`) con `max_tokens=2560`; prompt,
schema JSON, otto casi e ordine sono congelati prima dell'esecuzione. Il consumer 122B mantiene il
ragionamento con budget 2048, selezionato dalla sonda. La scelta per i producer segue due
osservazioni dirette: la prima chiamata 122B del predecessore ha consumato l'intero cap nel canale
di ragionamento (`finish_reason=length`, `content` nullo; verbale `VERIFICA_STOP_PRIMA_CHIAMATA_…_V2`)
e la prima risposta 27B ha speso 2047 dei 2560 token in ragionamento, con JSON troncato. Con il
ragionamento attivo il budget effettivo di inferenza diventa una variabile nascosta, diversa fra
modelli e casi; disattivarlo rende la risposta funzione di prompt, modello e cap e isola l'effetto
della condivisione degli insight. Il confronto 122B/27B è quindi fra **pipeline configurate**, non
fra capacità dei modelli a parità di ragionamento; l'effetto del budget di ragionamento sui producer
non è esplorato in questo studio ed è lavoro futuro.

> *Correzione alla bozza:* il rimando alla sensitivity 1024→3072 «dell'esperimento precedente»
> (91,7 % → 95 %) è stato tolto. Viene dal primo studio, che non si cita nel paper
> (`MAINTENANCE.md` §3.1), e il numero non è stato ritrovato in un artefatto durante questa chiusura.

**Contabilità delle chiamate.** Ogni richiesta è registrata in un ledger append-only con richiesta,
risposta grezza, token e hash. Il consumo cumulativo è 161 intent: 5 del predecessore (lineage S=5,
fra cui la prima chiamata 122B troncata), 1 qualifica tecnica, 8 conformità 122B, 10 remediation,
14 alternate 27B, 3 sonda e 120 gate. Sono conteggiate anche le richieste non valutabili: 7 prove
zero-token (due HTTP 401 per chiave del producer assente, cinque errori di connessione verso il 27B),
la risposta 27B sospesa e la richiesta del gate fallita per errore di connessione.

> *Correzione alla bozza:* le richieste zero-token **consumano quota** (una base, una remediation,
> cinque transport) e restano nel conteggio; la bozza diceva il contrario.

**Conformità dei producer e remediation.** Il 122B ha dato 6/8 risposte valide al primo tentativo;
le due non valide riguardavano la forma degli identificatori nel testo libero (`XMEAS-39` invece di
`XMEAS(39)`; una variabile citata ma non dichiarata in `variable_ids`). Come previsto (una sola
remediation, diagnosi registrata, diff del template approvato e vincolato per hash), il template è
stato integrato con una riga sulle forme canoniche e sulla corrispondenza fra testo e
`variable_ids`, senza toccare schema, cardinalità, cap, casi o ordine; la remediation ha dato 8/8.
La libreria del 122B usata nel gate è quella della remediation. Il 27B, con la stessa configurazione
senza ragionamento, ha dato **8/8 risposte valide al primo tentativo** e una libreria completa di 16
insight, senza remediation.

**Deviazioni post-osservazione.**

1. `enable_thinking=false` sui producer, deciso dopo le due troncature osservate; `max_tokens` non
   modificato, per non cambiare anche il cap dopo l'osservazione.
2. Riqualifica dell'identità del 27B: la configurazione qualificata prevedeva fingerprint assente
   (`null`), il servizio ha restituito `vllm-0.28.0-5fc21ed4`. La revisione della configurazione è
   registrata e approvata; le richieste precedenti restano legate alla revisione in cui sono state
   eseguite.

   > *Correzione alla bozza:* la bozza attribuiva il cambio a un aggiornamento «vLLM 0.27.1→0.28.0».
   > Gli artefatti non lo mostrano: 0.27.1 è la versione del 122B e la documentazione del 27B
   > dichiarava già vLLM 0.28.0. La causa del fingerprint non è documentata.
3. Due riconciliazioni di stati bloccanti prodotti da difetti dell'harness, non del modello: uno
   STOP contabile spurio e la sospensione per identità; entrambe con approvazione durevole e con lo
   stato originario conservato.
4. Quota `requalification` (1 chiamata) e massimo pianificato da 166 a 167 su 200: unica deroga al
   massimo pianificato, motivata dal cambio di identità del servizio 27B.

Nessuna deviazione modifica prompt, schema, casi, ordine o cap; nessuna risposta scientifica è stata
reinviata o scartata dopo la lettura del contenuto. La risposta 27B reinviata era invalida per
identità **e** troncata: il reinvio è stato deciso sulla base dell'identità, e il suo contenuto
resta nel ledger.

**Gate.** 120 richieste (40 prompt × 3), 119 valide al primo tentativo, zero troncamenti, almeno
un'astensione in ogni condizione. Un prompt (`S2-P03-002`) diverge per validità: una delle tre
ripetizioni non ha ricevuto risposta (errore di connessione). Per il piano statistico §10.3 questo
attiva **R = 3** per l'intero studio.

## 6. T5 — fattibilità temporale con W = 7 giorni

Formula del piano (`piano_statistico/BUDGET_RISORSE_REV10.md`): `T = Σ N_(blocco,modello) ×
latenza_media_(blocco,modello)`, esecuzione sequenziale, criterio `1,20 × T ≤ W`. Il pilot è già
eseguito e non entra in T. Latenze misurate sulla configurazione effettiva: gate 122B (120 righe)
media 26,209 s, p95 36,661 s; leaf finali 27B media 34,043 s, p95 37,167 s. Per i parametri non
ancora congelati si usa il **valore più sfavorevole** ammesso dal prospetto.

| Blocco (R = 3) | Modello | Richieste | Parametro |
|---|---|---:|---|
| Nucleo 5.184 + producer-swap 672 + ablation 444 + OOD 432 | 122B | 6.732 | `2244·R` |
| Audit aggiuntivo | 122B | 0 | nullo a R = 3 |
| E5 corrotto `16S` | 122B | 192 | S = 12, accantonamento prudenziale |
| E5 FULL non riusabile `8U` | 122B | 64 | U = 8, massimo |
| Canary `10d` | 122B | 70 | d = 7, l'intera finestra |
| Libreria principale `G_P` | 122B | 8 | senza riuso |
| Libreria alternativa `G_A` | 27B | 8 | senza riuso |
| Verifiche tecniche `X` | 122B | 100 | ipotesi prudenziale storica |
| Retry `Q` | 122B | 0 | vedi margine sotto |
| **Totale** | | **7.174** | 7.166 sul 122B, 8 sul 27B |

| Latenza usata | T | 1,20 × T | W | Esito | Margine |
|---|---:|---:|---:|---|---:|
| media | 52,25 h | **62,69 h** | 168 h | **PASS** | 105,31 h |
| p95 | 73,06 h | **87,67 h** | 168 h | **PASS** | 80,33 h |

Il margine assorbe fino a 12.053 retry `Q` aggiuntivi alla latenza media (6.573 al p95). Il solo
nucleo R = 3 vale 45,29 h con il 20 % (verbale `b567` §7), coerente con la tabella.
Assunzioni: esecuzione sequenziale come nel pilot; latenze del gate rappresentative degli altri
blocchi consumer (stessi template e ordini di grandezza dei prompt); nessuna attesa per
remediation (librerie già prodotte e valide). Il batch può essere eseguito a tratti con `--resume`:
W è un criterio di accettazione, non un impegno continuo dei server. Con d = 7 il calendario è
conservativo, perché l'esecuzione stimata occupa meno di tre giorni.

**T5 = PASS.** Il verbale `b567` lo lasciava `NOT ESTABLISHED` perché mancavano W e il conteggio
completo: entrambi sono ora fissati qui.

## 7. Decisione GO

Il 2026-09-17 l'autore ha deciso il **GO del pilot con R = 3** per le fasi successive (§7.2 libreria
e batch principale), in applicazione della decisione 11 dopo la divergenza di validità su
`S2-P03-002`. La decisione era sospesa a due condizioni del verbale `b567`: T5 compatibile e
divergenza non dovuta a invalidità intermittente. Il verbale ha confermato la natura della
divergenza (di validità, da errore di trasporto) e la regola la tratta comunque come divergenza;
T5 è PASS con W = 7 giorni (§6). **Il GO con R = 3 è quindi definitivo dal 2026-09-17.**

Resta subordinato all'OK di `VERIFICA_PILOT_03_13.md` sulla correttezza di questo report.

## 8. Debito tecnico registrato

Non bloccante per l'esito del pilot, da non dimenticare prima dell'esecuzione principale:

| Id | Descrizione | Fonte |
|---|---|---|
| P2-03 | `d9.validate_binding` accetta binding diretti senza `execution_config`: l'API ledger è più permissiva dei runner | `VERIFICA_MIRATA_RILIEVI_CLAUDE_03_13.md` §6 (`ada613c3…`) |
| P2-04 | la forma no-thinking è accettata nel contratto contabile anche dove non è richiesta (consumer 122B) | idem |
| P2-05 | `authorize_remediation` non applica il guard STOP/sospensione né riconferma l'outcome; `waive_remediation` accetta solo un hash | idem |
| P2-06 | regex di leakage al singolare con `\b`: i plurali non sono intercettati; estenderle cambia una regola congelata | idem |
| P2-10 | `_record_consumed_fields` non ricalcola i flag semantici passati dal chiamante | idem |
| P3 | identità del provider su SHA del file anziché sul digest canonico; materializzazione non transazionale; storico v3 non riautenticato; eventi orfani prima dell'import; stage tecnico ammesso su ledger generico; request 122B `FAILED` con raw senza accounting | idem §7 |
| lock-close | diagnosi del rilascio dei lock SQLite alla chiusura, da registrare/correggere separatamente | `VERIFICA_CANDIDATO_A199D6F_…` |
| E26 | finestra fra la sostituzione della config e l'evento `config_revision`: mitigata da STOP operativo e rilancio idempotente, non atomica | `VERIFICA_FIX_REV27B_E20_E4_03_13.md` |
| Guardian | `docs/test_explanation.py`: 14 fallimenti storici (walkthrough v1), invariati | `MAINTENANCE.md` §5 |
| Operativo | la VM del client Cowork tiene aperti i ledger se il runtime è collegato; le review vanno fatte da shell nativa | sessione |
| Operativo | la config punta all'approvazione di presentazione nella worktree `dd86` (`0f9f7b7f…`): non va potata; copia identica in `execution/presentation_order_approval.private.json` | 03.13-ACC |

## 9. Cosa resta

- **Verifica di sotto-fase** `VERIFICA_PILOT_03_13.md` (`b567`) su questo report, sull'evidenza e sul §4.13.
- **Conservazione**: caricamento dell'archivio `studio2-fase03-pilot-v1` su `fot-tep-data`, dopo la
  verifica di pubblicabilità dei file `*.private.json`, e verifica per riscaricamento (§10).
- **Freeze e tag** del pilot: decisione dell'autore dopo l'OK.
- **Integrazione in `main`** del branch `codex/studio2-riconciliazione-stop-contabile`.
- **Per l'esecuzione principale** (piano §11, fuori da questa sotto-fase): set canary congelato (T8),
  librerie congelate per entrambi i producer (S5), prompt e condizioni congelati (S8), diff B↔E (S18),
  parità strutturale dei producer (S19), parametri S/U/d/X/Q effettivi da confrontare con §6.

## 10. Artefatti e riproducibilità

| Artefatto | Posizione | SHA-256 |
|---|---|---|
| Ledger finale | runtime, `ledger.sqlite3` | `93ff83a5a4132800c2973fe6687c8e0ffcdb07d33f293a8517ca715ff8dc4089` |
| Evidenza di esecuzione | [`harness/EVIDENZA_PILOT_03_ESECUZIONE_FINALE_03_13.md`](../harness/EVIDENZA_PILOT_03_ESECUZIONE_FINALE_03_13.md) e manifest | nel manifest |
| Log dei run | [`harness/logs_pilot_03_finale/`](../harness/logs_pilot_03_finale/) | `REDACTION_INDEX.json` |
| Summary del gate | runtime, `results/stability_summary.json`; digest record `bd9713ec…` | nel manifest di conservazione |
| Config congelata del gate | runtime, `results/frozen_gate_config.json` | file `709ae340…`, contenuto `de1f59ce…` |
| Prompt | runtime, `prepared/pilot_prompts.jsonl` | `efd43620…` |
| Librerie | runtime, `results/validated_insight_library_*` | canoniche `c2469737…` (122B), `f860063b…` (27B) |
| Manifest di conservazione | [`MANIFEST_CONSERVAZIONE.csv`](MANIFEST_CONSERVAZIONE.csv) | 77 file |
| Record di conservazione | [`ARTIFACT_STORAGE.json`](ARTIFACT_STORAGE.json) | `prepared_not_published` |
| Archivio locale | `/Users/luker/fot-tep/downloads/studio2-fase03-pilot-v1/studio2-fase03-pilot-v1.tar` (ignorato da Git) | `30cdd5ca5715695bae4cc61c3b3919d3949f471c768d008d87395430d9c2c3b8`, 9.021.440 byte |
| Verbale d'esito | [`VERIFICA_ESITO_PILOT_03_13.md`](VERIFICA_ESITO_PILOT_03_13.md) | `1ce0a466…4b70` |

L'archivio contiene ledger, `execution/` (nessuna credenziale trovata), `lineage/`, `qualification/`,
`prepared/`, `results/` e `MATERIALIZATION_SUMMARY.private.json`; esclude `tokenizers/`, pinnati per
revisione e hash nella config. `lineage/` e `qualification/` non erano nell'elenco del prompt: servono
a `require_execution` per ricostruire la verifica.

Comandi per il caricamento (a cura dell'autore, dopo il controllo di pubblicabilità):

```bash
cd /Users/luker/fot-tep/downloads/studio2-fase03-pilot-v1
shasum -a 256 -c studio2-fase03-pilot-v1.tar.sha256
gh release create studio2-fase03-pilot-v1 studio2-fase03-pilot-v1.tar studio2-fase03-pilot-v1.tar.sha256 \
  --repo sorrentinoluca/fot-tep-data --title "studio2-fase03-pilot-v1" \
  --notes "Studio 2, fase 03, sotto-fase 03.13: runtime pilot-03 (ledger, results, prepared, execution, lineage, qualification). SHA-256 30cdd5ca5715695bae4cc61c3b3919d3949f471c768d008d87395430d9c2c3b8"
mkdir -p /tmp/pilot-v1-check && cd /tmp/pilot-v1-check
gh release download studio2-fase03-pilot-v1 --repo sorrentinoluca/fot-tep-data --pattern 'studio2-fase03-pilot-v1.tar*'
shasum -a 256 -c studio2-fase03-pilot-v1.tar.sha256 && tar -xf studio2-fase03-pilot-v1.tar
```

Il confronto file per file con `MANIFEST_CONSERVAZIONE.csv` va poi registrato in
`ARTIFACT_STORAGE.json` (`verification`), come per le altre release.
