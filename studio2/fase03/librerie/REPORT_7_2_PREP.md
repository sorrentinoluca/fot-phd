# 7.2-PREP — preparazione delle librerie insight

Offline, 2026-09-17. Worktree `rem6-riconciliazione`, HEAD `540df7b` (contiene 03.13-PUB).
Runtime `pilot-03` in sola lettura, ledger `93ff83a5…` invariato prima e dopo. Nessuna chiamata,
materializzazione, push, merge o tag. **Quota, accounting e ledger non toccati** (nessuna modifica
di codice in questo commit). Esecutore: `claude-opus-5` (Claude Cowork).

## A — Esito del controllo di riuso

| Producer | Proposta | Motivo |
|---|---|---|
| **122B principale** (`c2469737…`) | **RIUSABILE** | input, contratti, identità, cap e schema coincidono con il protocollo finale; rivalidata offline 16/16 |
| **27B alternativo** (`f860063b…`) | **RIUSABILE, con un rilievo S19** | tutto coincide tranne il template: il 27B ha usato quello base, il 122B quello di remediation (una riga sugli identificatori canonici) |

Verificato campo per campo in [`RIUSO_LIBRERIE_7_2.md`](RIUSO_LIBRERIE_7_2.md): stesso inventario
autenticato (`d3605ae5…`, solo dati di sviluppo 03.6 + `Normal` 03.9, nessun run di test, OOD o
canary), 16 contratti invariati, identità e controlli di generazione attesi
(`enable_thinking=false`, `max_tokens=2560`), prompt ricostruiti e uguali agli hash del ledger 8/8
per entrambi gli stage, rivalidazione con `validator.py` + leakage v1 + cap con il contatore R4:
PASS per entrambe. Parità S19 rispettata (16 insight, stesso schema e cap; token medi 100,12 contro
101,69; il 27B è più disperso).

La decisione sull'asimmetria di template è dell'autore: accettarla e dichiararla nei metodi
(nessuna chiamata), oppure rigenerare la libreria 27B con lo stesso template (8 chiamate + margine,
nuovo target successore, quota e accounting toccati → review `b567`).

## B — Candidato di freeze (preparato, non congelato)

[`LIBRERIE_FINALI_CANDIDATE.json`](LIBRERIE_FINALI_CANDIDATE.json): per ciascun producer path e SHA
del file, SHA canonico della libreria, `records_sha256`, `binding_sha256`, `inventory_sha256`,
schema, modello e fingerprint, provider e parametri, template (sorgente e digest), token e caratteri
per singolo insight, e la provenienza per agente (`request_id`, `quota_kind`, `prompt_sha256`,
`case_sha256`, `contract_sha256`). Nessuna copia dei file del runtime è stata fatta: solo
riferimenti. Il freeze appartiene a 7.3.

## C — Rigenerazione (solo se l'autore la sceglie)

[`RUNBOOK_7_2_LIBRERIE.md`](RUNBOOK_7_2_LIBRERIE.md), scritto come contingenza e **non eseguibile
così com'è**: lo stage alternate di `pilot-03` è chiuso e la riserva è esaurita, quindi servirebbe un
target successore con quota dedicata (8 + 4 di margine), e il runner rifiuta un template diverso da
quello congelato fuori dalla remediation. Entrambi i punti richiedono una decisione dell'autore e la
review di `b567`; il runbook li mette in testa, poi dà comandi, rimedi standard e la regola
pre-registrata sui reinvii (un solo reinvio per agente e solo per cause di trasporto documentate;
una risposta ricevuta e non valida chiude lo stage in FAIL).

Nessun codice è stato modificato, quindi non è stato eseguito nessun dry-run né una nuova corsa dei
test: la suite resta quella verde di `540df7b`.

## D — Criteri di accettazione

[`CRITERI_ACCETTAZIONE_7_2.md`](CRITERI_ACCETTAZIONE_7_2.md): 13 criteri verificabili offline
(validità 16/16, copertura 8×2, contratti invariati, leakage zero, cap, parità S19, token riportati,
provenienza dal ledger, identità, controlli di generazione, template dichiarato, input di solo
sviluppo, nessuna scelta post-hoc).

## Limiti

- Il conteggio dei token usa il contatore R4 (tokenizer 27B `017b9c7a…`) con `transformers` 5.17.0
  installato nella VM di questa sessione: stesso contatore usato dal validatore, non quello del
  servizio.
- `lsof` non è eseguibile da qui; il ledger è stato solo letto (`immutable=1`) e il suo SHA non è
  cambiato.
- Le proposte di §A non sono decisioni: 7.2-RUN serve solo se l'autore sceglie di rigenerare.
