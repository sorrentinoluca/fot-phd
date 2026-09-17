# Criteri di accettazione delle librerie insight — 7.2-R

Verificabili offline, uno per riga, senza chiamate. Valgono per ciascun producer (122B principale,
27B alternativo), sia in caso di riuso sia in caso di rigenerazione.

| # | Criterio | Come si verifica | Esito atteso |
|---|---|---|---|
| A1 | **Validità 16/16** contro lo schema congelato R4 | `schema_insight/validator.py` sulla libreria, con `schema_commit` `3c64390b…` e `schema_manifest_sha256` `d64e4d4b…` | nessuna eccezione |
| A2 | **Copertura** 8 agenti × 2 contratti | `source_agent` distinti = 8; `insight_id` distinti = 16; ogni `insight_id` dei contratti presente una volta | esatto |
| A3 | **Contratti invariati** | `source_agent`, `pseudolabel`, `evidence_scope`, `variable_ids` uguali a `fixed_insight_contracts` dell'inventario autenticato (`d3605ae5…`) | zero differenze |
| A4 | **Leakage zero** | `leakage_rules_v1.json` v1 via `insight_adapter.validate_library`; più ricerca di identificativi di run di test, OOD o canary (`EVD-\d+`, `S2-EXM-\d+`, `run_id`, `batch N`, `TEST`, `OOD`, `canary`) nel testo | nessun riscontro |
| A5 | **Cap per elemento** | cap token e caratteri dello schema applicati dal validatore con il contatore R4 (tokenizer 27B `017b9c7a…`, `chat_template=False`) | rispettato da tutti e 16 |
| A6 | **Parità S19** | stesso schema, stesso numero di insight, stesso cap; tabella token/caratteri per producer (totale, media, mediana, min, max) nel report | tabella presente, cap uguali |
| A7 | **Token effettivi riportati** | valore per singolo insight in `LIBRERIE_FINALI_CANDIDATE.json` | 16 valori per producer |
| A8 | **Provenienza ricostruibile dal ledger** | per ogni agente: `request_id`, stage, `quota_kind`, `prompt_sha256`, `case_sha256`, `contract_sha256`, `binding_sha256`; `library_sha256` canonico uguale alla ricostruzione dai raw del ledger (`inputs._insights`) | tutto risolve |
| A9 | **Identità del modello** | ogni risposta usata: 122B `qwen3.5-122b`/`vllm-0.27.1-934a3247`; 27B `fot-exp2-consumer`/`vllm-0.28.0-5fc21ed4` | 8/8 per producer |
| A10 | **Controlli di generazione** | `enable_thinking=false` e `max_tokens=2560` nel binding di entrambi gli stage | presenti |
| A11 | **Template dichiarato** | SHA-256 o digest canonico del template per producer, con la differenza fra i due dichiarata esplicitamente | dichiarato |
| A12 | **Input di solo sviluppo** | `inventory_sha256` del binding = digest dell'inventario autenticato; provenienza degli esempi dentro i 320 casi di sviluppo | uguale |
| A13 | **Niente scelta post-hoc** | una sola libreria per producer, nessun output scartato dopo la lettura del contenuto; eventuali retry dichiarati con motivo di trasporto | dichiarato nel report |

Un criterio non soddisfatto è un rilievo bloccante per 7.2-R; A11 e A13 sono dichiarativi e si
verificano sul report, non sul contenuto degli insight.
