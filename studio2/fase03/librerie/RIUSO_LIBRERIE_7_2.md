# Controllo di riuso delle librerie insight — 7.2-PREP (A)

Offline, 2026-09-17. Runtime `pilot-03` letto in sola lettura (`mode=ro&immutable=1`, ledger
`93ff83a5a4132800c2973fe6687c8e0ffcdb07d33f293a8517ca715ff8dc4089`, invariato). Nessuna chiamata,
nessuna materializzazione. Codice: worktree `rem6-riconciliazione`, HEAD `540df7b`.
Esecutore: `claude-opus-5` (Claude Cowork), non `gpt-5.6-sol` indicato dal prompt.

## Proposta (decide l'autore)

| Producer | Libreria | Proposta | Motivo in una riga |
|---|---|---|---|
| 122B principale | `c2469737…` (remediation) | **RIUSABILE** | input, contratti, identità, schema e cap coincidono con quanto richiede lo studio finale; rivalidata offline 16/16 |
| 27B alternativo | `f860063b…` (alternate) | **RIUSABILE con un rilievo S19** | tutto coincide tranne il **template**: il 27B ha usato il template base, il 122B quello di remediation (una riga in più sugli identificatori canonici) |

La differenza di template non viola i criteri di parità di §8.4/S19, che riguardano **schema, numero
di insight, cap per elemento e token misurati**, tutti rispettati. È però un'asimmetria di
istruzioni fra i due bracci: va decisa e dichiarata, non lasciata implicita. Opzioni in §6.

## 1. `local_examples` — identici e di solo sviluppo

Le tre bindings producer (`producer_conformity`, `producer_remediation`, `alternate_conformity`)
portano lo stesso `inventory_sha256`
`d3605ae5f656606d2597cd7f06d69aab4ad2305c799db1f0b8b09b0722aea3b3`, uguale al digest canonico
dell'inventario autenticato `harness/PILOT_INPUT_SOURCES.pending.json` (pin
`7103482d6c7b8038944b0af63bac58548557c8d0b8f5d24e420346bd93fa304b`, verificato da
`inputs.verified_pending_inventory()`).

- 3 esempi per agente (8/8): due dal fault locale (batch 1 e 2, finestra 1) e uno `Normal`.
- Le 16 righe di `local_example_provenance` puntano tutte a `case_id` presenti fra i **320 casi di
  sviluppo** dell'inventario (`EVD-…`), dalla release `studio2-fase03-evidence-v2`
  (`6d724ca2…`); gli esempi `Normal` vengono da `baseline_numerica/NORMAL_DEV_HANDOFF.json`
  (03.9, pin `e2409c64…`).
- Nessun identificativo del lotto di test 03.11, nessun OOD, nessun canary: la ricerca di
  `EVD-\d+`, `S2-EXM-\d+`, `run_id`, `batch N`, `TEST`, `OOD`, `canary` nel testo delle due
  librerie non trova nulla.

Controllo più forte dell'uguaglianza degli hash: i prompt sono stati **ricostruiti** con
`producer.build_producer_prompt` a partire dall'inventario e dal template, e i loro SHA-256
coincidono con `prompt_sha256` delle otto richieste di ciascuno stage (8/8 per entrambi), insieme a
`case_sha256` e `contract_sha256`.

## 2. `fixed_contracts` — 16, uguali al protocollo

I 16 contratti dell'inventario (`insight_id`, `source_agent`, `pseudolabel`, `evidence_scope`,
`variable_ids`) compaiono invariati in entrambe le librerie: zero differenze campo per campo.
Otto agenti, due contratti ciascuno, pseudolabel dalle nove classi congelate in 03.7
(`S2-CLS-…`), schema R4 di 03.12 (`schema_commit` `3c64390b…`, `schema_manifest_sha256`
`d64e4d4b…`) dichiarato in entrambi gli handoff.

## 3. Template — **differenza**

| Producer | Template | SHA-256 file | Digest canonico del testo nel binding |
|---|---|---|---|
| 122B | `execution/producer_template_remediation_03_13.txt` | `4306c5da6f0ebefcbce75d26d585caf82cc05ff85d5e7e6639e3f65b2d66de12` | `304c858f828471e46ed915fba1eb79991f9cfe689bd524f20b504658b9d605c9` |
| 27B | `harness/producer.py::PRODUCER_TEMPLATE`, invariato | — (testo nel codice) | `156fd0e18274b8e8fc72c04527e741a83197daa8b21f3201a5a9496e6d87ed29` |

Il template di remediation differisce dal base per **una sola riga aggiunta** dopo la quarta:

> Use the exact canonical identifier form XMEAS(N) or XMV(N) everywhere, including free text; never
> write XMEAS-N or XMEAS N. Every variable cited in observed_pattern or anywhere else in the output
> must also appear in variable_ids, and vice versa.

I prompt del 27B **non** coincidono con quelli che si otterrebbero applicando il template di
remediation: l'asimmetria è reale e riguarda tutti e otto i casi.

## 4. Generazione e identità

| Voce | 122B | 27B |
|---|---|---|
| Modello restituito / fingerprint | `qwen3.5-122b` / `vllm-0.27.1-934a3247` | `fot-exp2-consumer` / `vllm-0.28.0-5fc21ed4` |
| Provider (file) | `04b2c948…` | rev2 `27295c25…` |
| `max_tokens` | 2560 | 2560 |
| `extra_body` | `chat_template_kwargs.enable_thinking=false` | `chat_template_kwargs.enable_thinking=false` |
| `temperature` / `seed` | assenti (regime 122B) | 0.0 / 20260829 |
| `thinking_token_budget` | assente | assente (rimosso nel rev2) |

Sono le identità e i controlli decisi per lo studio finale (handoff rev07 §1.3). La differenza su
`temperature`/`seed` è strutturale fra i due regimi di provider, non introdotta qui.

## 5. Rivalidazione offline e parità strutturale (S19)

Entrambe le librerie sono state rivalidate in questa sessione con
`schema_insight/validator.py` + `leakage_rules_v1.json` e il contatore R4 (tokenizer 27B
`017b9c7a…`, `transformers` 5.17.0): **PASS** per entrambe, nessuna eccezione.

| Misura | 122B | 27B |
|---|---:|---:|
| Insight validi | 16 | 16 |
| Agenti coperti × contratti | 8 × 2 | 8 × 2 |
| Campi per insight | gli stessi 6 dello schema R4 | idem |
| Voci `variable_ids` | 128 | 128 |
| Variabili distinte | 33 | 33 |
| Token `observed_pattern`: totale / media / mediana / min / max | 1.602 / 100,12 / 93,5 / 66 / 130 | 1.627 / 101,69 / 110,5 / 60 / 134 |
| Caratteri: totale / media / mediana / min / max | 6.817 / 426,06 / 423,5 / 321 / 525 | 6.471 / 404,44 / 424,0 / 235 / 576 |
| SHA-256 file | `1e97ddd3…eea09` | `c697e803…73c9` |
| SHA canonico libreria | `c2469737…d1a30` | `f860063b…a05f3` |

La parità richiesta da §8.4 è rispettata: stesso schema, stesso numero di insight, stesso cap per
elemento, token misurati e riportati per producer. Le medie sono a due token di distanza; il 27B è
più disperso (60–134 token, 235–576 caratteri) del 122B (66–130, 321–525). È una descrizione, non
un test.

## 6. Cosa resta da decidere

1. **Accettare l'asimmetria di template** e dichiararla nei metodi: il 122B ha ricevuto una riga in
   più sulle forme canoniche degli identificatori, aggiunta dopo il suo FAIL T9; il 27B non ne ha
   avuto bisogno. Costo zero, nessuna chiamata.
2. **Rigenerare la libreria 27B con il template di remediation**, per avere istruzioni identiche.
   Costo: 8 chiamate + margine di retry, **un nuovo target successore** di `pilot-03` (lo stage
   alternate è chiuso e la riserva del pilot è esaurita), quindi una modifica che tocca
   quota/accounting e che richiede la review di `b567`. Piano e numeri in
   [`RUNBOOK_7_2_LIBRERIE.md`](RUNBOOK_7_2_LIBRERIE.md), scritto come contingenza.
3. In entrambi i casi, il freeze delle librerie appartiene a 7.3 e non è stato eseguito qui.

Nessuna terza opzione è raccomandata: rigenerare anche il 122B con il template base rimetterebbe in
gioco il FAIL già osservato, e cambiare il template dopo l'osservazione è vietato dal protocollo.
