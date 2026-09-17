# VERIFICA_LIBRERIE_7_2 — 7.2-R, accettazione indipendente delle librerie insight (`G_P` 122B, `G_A` 27B)

Finestra `b567` (reviewer indipendente), Claude (Cowork), offline e in sola lettura. Nessuna
chiamata, nessuna modifica a codice, ledger o runtime; nessun push, merge, tag. `api_key.json` e
`server_enea.json` non letti. Runtime letto dalla shell nativa del Mac
(`/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03`), non via bridge.

Oggetto: commit `c284523badefdf6b4f4e131e99ba4dfbda31300c` (verificato come HEAD della worktree),
worktree `/Users/luker/fot-tep/.worktrees/rem6-riconciliazione`, cartella
`studio2/fase03/librerie/` (`REPORT_7_2_PREP.md`, `RIUSO_LIBRERIE_7_2.md`,
`LIBRERIE_FINALI_CANDIDATE.json`, `CRITERI_ACCETTAZIONE_7_2.md`). Ledger invariato durante e dopo
la verifica: `93ff83a5a4132800c2973fe6687c8e0ffcdb07d33f293a8517ca715ff8dc4089` (confermato per byte
prima e dopo). Decisione dell'autore recepita: asimmetria di template accettata e dichiarata nei
metodi, nessuna rigenerazione.

## Esito

| Producer | Libreria | Esito |
|---|---|---|
| 122B principale (remediation) | `c2469737…d1a30` | **OK** |
| 27B alternativo (alternate_conformity) | `f860063b…a05f3` | **OK con rilievi** (rilievo R1, non bloccante) |

Tutti e 13 i criteri di `CRITERI_ACCETTAZIONE_7_2.md` sono stati rifatti in modo indipendente e
risultano soddisfatti per entrambi i producer. Il rilievo R1 riguarda la coppia (non un criterio
fallito) e nasce dall'approfondimento richiesto sull'asimmetria di template (mandato, punto 2).

## Tabella dei 13 criteri

| # | Criterio | Esito | Evidenza indipendente |
|---|---|---|---|
| A1 | Validità 16/16 (R4) | **PASS** | `validator.py` (hash-pin verificato: `cd523d3105e0…`/`15e0d29e033c…`/`1cf035b5d5e7…`/`d64e4d4be32a…` tutti coincidenti) ricostruito ed eseguito su entrambe le librerie con il contesto ricavato dall'inventario: `validate_library` PASS, nessuna eccezione, per 122B e 27B |
| A2 | Copertura 8×2 | **PASS** | 8 `source_agent` distinti, 16 `insight_id` distinti in entrambe le librerie; ogni contratto presente una volta |
| A3 | Contratti invariati | **PASS** | confronto campo per campo (`source_agent`, `pseudolabel`, `evidence_scope`, `variable_ids`) di tutti e 32 i record contro `fixed_insight_contracts` dell'inventario: 0 differenze |
| A4 | Leakage zero | **PASS** | `scan()` del validatore (incluso nel PASS di A1) + ricerca esplicita di `EVD-\d+`, `S2-EXM-\d+`, `run_id`, `batch\s*\d+`, `TEST`, `OOD`, `canary` sul testo di entrambe le librerie: 0 riscontri |
| A5 | Cap per elemento | **PASS** | enforcement nel validatore (192 token narrativa, 64 token evidence_scope, 384 token record, 1400 caratteri record): nessun superamento, incluso nel PASS di A1 |
| A6 | Parità S19 | **PASS** | statistiche token ricalcolate dal validatore: 122B totale 1602, media 100,12, mediana 93,5, min 66, max 130; 27B totale 1627, media 101,69, mediana 110,5, min 60, max 134 — identiche a quelle dichiarate in `RIUSO_LIBRERIE_7_2.md` e nel candidato |
| A7 | Token effettivi riportati | **PASS** | i 16+16 valori `tokens_per_insight`/`chars_per_insight` di `LIBRERIE_FINALI_CANDIDATE.json` ricalcolati uno per uno (token con lo stesso tokenizer R4, caratteri come lunghezza di `observed_pattern`): 0 scostamenti su 32 |
| A8 | Provenienza dal ledger | **PASS** | per tutti e 16 gli agenti: `request_id`, `prompt_sha256`, `case_sha256`, `contract_sha256` ricostruiti da `requests.identity_json` nel ledger e confrontati byte-per-byte col candidato (0 scostamenti); `binding_sha256` di entrambi gli stage confrontato con `stages.binding_sha256` (coincide); `library_canonical_sha256` ricalcolato con la stessa canonicalizzazione del validatore (`json.dumps(...,sort_keys=True,separators=(',',':'))`) sui 16 record `library` di ciascun file: coincide byte-per-byte col dichiarato per entrambi i producer |
| A9 | Identità del modello | **PASS** | per le 8 richieste finali di ciascun producer, `responses.record_json.returned_model`/`system_fingerprint` letti dal ledger: 8/8 `qwen3.5-122b`/`vllm-0.27.1-934a3247` per il 122B, 8/8 `fot-exp2-consumer`/`vllm-0.28.0-5fc21ed4` per il 27B |
| A10 | Controlli di generazione | **PASS** | `stages.binding_json` per entrambi gli stage: `provider.max_tokens=2560` e `provider.extra_body.chat_template_kwargs.enable_thinking=false` presenti in entrambi; `temperature=0.0`/`seed=20260829` solo sul 27B, assenti sul 122B — coerente col regime dichiarato |
| A11 | Template dichiarato | **PASS** (vedi rilievo R1) | SHA-256 del testo del template estratto da `binding_json` di ciascuno stage: 122B `4306c5da…` (= dichiarato), 27B `e7e80d59…` (= dichiarato); digest canonico anch'esso coincidente (`304c858f…`, `156fd0e1…`). Diff riga-per-riga: **esattamente una riga aggiunta** dopo la quarta, nessun'altra differenza (confermato con `diff`, non solo per hash) |
| A12 | Input di solo sviluppo | **PASS** | `inventory_sha256` ricalcolato come digest canonico di `PILOT_INPUT_SOURCES.pending.json` = `d3605ae5…` (= dichiarato in entrambe le librerie); tutti i 16 `case_id` di `local_example_provenance` presenti fra i 320 `development_cases` (batch 1–2, finestra 1, 8 fault distinti); esempi `Normal` da `NORMAL_DEV_HANDOFF.json` (pin `e2409c64…`, dichiarato); nessun identificativo di test/OOD/canary nel testo (vedi A4) |
| A13 | Niente scelta post-hoc | **PASS** | ricostruito dal ledger l'intero albero dei tentativi per stage: `producer_conformity` (base 122B) FALLISCE con `valid_first_attempts=6/8`, diagnosi `identifiers` su agent_2/agent_3 (`malformed variable identifier`, `literal references required and must be declared` — errori strutturali, non di contenuto); la remediation è autorizzata da Luca con `diagnosis=identifiers` e aggiunge la riga sugli identificatori (A11); tutti i retry di trasporto sul 122B (`7bbd56ff…`, `dde658fd…`) e sul 27B (5 retry dell'agent_1) hanno **zero token generati** (`disposition=not_generated`, HTTP 401 / connection refused / connection reset — nessun contenuto da scartare); la sospensione `19a9b372…` sul 27B è per **identità di risposta cambiata** (`identity_valid=false`, nuovo `system_fingerprint` vLLM 0.28.0) *e* per troncamento (`finish_reason=length`, JSON non parsificabile, "Unterminated string") — motivi strutturali verificati sul contenuto grezzo, non un content-based discard; Luca approva la revisione di configurazione (`config_revision:1`) e una nuova chiamata (`quota_kind=requalification`, `26919ef2…`) sostituisce quella sospesa: una sola libreria per producer, nessuna risposta valida scartata |

## Rilievi

**R1 — non bloccante, gravità bassa-media.** La riga aggiunta al template di remediation del 122B
non riguarda solo la forma degli identificatori: chiede esplicitamente che «every identifier in
variable_ids must be cited in observed_pattern» (copertura bidirezionale), ma il validatore
verifica solo `refs ⊆ variable_ids`, non il viceversa. Verificando la copertura bidirezionale
effettiva sui 16+16 insight: il 122B la raggiunge in **6/16** insight (37,5%), il 27B in **0/16**.
La differenza di istruzioni fra i due bracci quindi non è puramente sintattica: correla con una
copertura descrittiva delle variabili diversa fra i due producer, un potenziale confondente per il
confronto producer-swap se l'ampiezza informativa della narrativa è rilevante a valle. Non fa
fallire nessuno dei 13 criteri (che riguardano forma, cap e token, non ampiezza descrittiva), ma la
formulazione attualmente proposta in `RIUSO_LIBRERIE_7_2.md` §3 ("una riga aggiunta... sulle forme
canoniche degli identificatori") la sottostima: è difendibile in review solo se integrata.

## Testo proposto

**Metodi (2–3 righe):**
> Al producer 122B, dopo il fallimento di validità sulla forma degli identificatori riscontrato in
> due agenti su otto (regime senza remediation), è stata aggiunta un'unica riga al template che
> impone la forma canonica XMEAS(N)/XMV(N) e la citazione di ogni variabile dichiarata nella
> narrativa; il 27B ha usato il template base, invariato. La differenza è dichiarata e non
> ricalcolata a posteriori. Il validatore impone solo che le variabili citate siano un sottoinsieme
> di quelle dichiarate, non il viceversa: la riga aggiunta correla con una copertura bidirezionale
> più alta ma incompleta nel 122B (6/16 insight) contro nessuna nel 27B (0/16), un effetto che va
> oltre la sola sintassi degli identificatori.

**Threats to validity (1 riga):**
> Il confronto producer-swap 122B/27B usa librerie generate con template che differiscono di una
> riga (identificatori canonici, presente solo nel 122B dopo la sua remediation); oltre alla
> sintassi, questa riga correla con una copertura variable_ids↔observed_pattern più ampia nel 122B
> (6/16 contro 0/16 insight), un possibile confondente se l'ampiezza descrittiva della narrativa
> influenza l'uso a valle degli insight.

## Rischio di influenza sul gate del pilot (mandato, punto 4)

Nessuna evidenza trovata. Lo stage `stability_gate` (gate 120, `binding_sha256`
`d87e8ac1f6ecda1a490e77b22c7623749b1acc62d3d3775e0fecc7dcb768a233`) e il suo
`frozen_gate_config.json` sono artefatti distinti dai due stage delle librerie
(`producer_remediation`/`alternate_conformity`, binding `ad9ed8ae…`/`7cb32fb9…`): nessuno dei due
SHA canonici delle librerie (`c2469737…`, `f860063b…`) o dei nomi dei file di libreria compare in
`frozen_gate_config.json`. L'esito del gate 120 (119/120 validi, un solo divergente
`S2-P03-002`, stato `R3_REQUIRED_PENDING_FEASIBILITY`, GO con R=3) risulta dai documenti di sessione
già deciso e congelato prima della preparazione 7.2 di oggi, ed è di natura numerica (soglie/T3/T4/
T6), non testuale: nessun accoppiamento con il contenuto delle librerie insight.

## Limiti della verifica

- Non è stato possibile ricalcolare in modo indipendente `provider_file_sha256` a partire dal file
  di configurazione grezzo sul disco per il 27B: il percorso plausibile ricade sotto file esclusi
  dal mandato (`server_enea.json`), quindi il controllo è stato limitato alla coerenza interna del
  ledger (`stages.binding_json.provider_file_sha256` = valore dichiarato nel candidato, per
  entrambi i producer) più la verifica indipendente dell'unico file di provider leggibile
  (`config/qwen_122b_api_primary_d9.json`, che però non corrisponde byte-per-byte al file
  referenziato dal binding — verosimilmente per revisioni di config successive non tracciate in
  quel file; non bloccante perché il ledger resta la fonte auditata e il suo SHA-256 è invariato).
- Il conteggio dei token usa il tokenizer R4 pinnato (`017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`,
  `transformers` 5.17.0 installato in questa sessione per la verifica), lo stesso usato dal
  validatore, non quello del servizio.
- Verifica dei soli quattro file indicati nel mandato più il ledger e i file schema/harness
  referenziati da essi; `RUNBOOK_7_2_LIBRERIE.md` non è stato verificato nel merito perché è una
  contingenza non eseguita (nessuna chiamata aggiuntiva, riserva `alternate_producer_conformance_
  deferred=8` intatta).
