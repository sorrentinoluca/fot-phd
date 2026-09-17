# Verifica indipendente 03.13-REV27B (finestra `b567`)

Candidato: commit `studio2(fase03): revisione approvata config, riqualifica 27B e ripresa alternate`
sul branch `codex/studio2-riconciliazione-stop-contabile`, parent `3952fb4`. Offline; nessuna
chiamata; il ledger reale `pilot-03` si apre solo in sola lettura (`immutable=1`), SHA atteso
`3872029001346913f3722928b350813c8daaef349c5d4fbe98b770200c893fa0`.

Leggi `studio2/fase03/PROMPT_REV27B_RIQUALIFICA_27B_E_RIPRESA_PILOT_03_03_13.md`, il report
`harness/REPORT_REVISIONE_CONFIG_RIQUALIFICA_27B_03_13.md` (decisioni dell'autore e deviazioni
dichiarate) e il diff. Verifica, con prove eseguibili e non per lettura:

1. **Revisione**: solo le chiavi dichiarate cambiano; approvazione legata ai due SHA; catena
   ri-autenticata a ogni uso; una config non registrata o superata viene rifiutata.
2. **Sospensione**: riconciliabile solo per identità; identità osservata = raw = record e accettata
   dalla revisione; rifiutata se esistono request successive; `suspended:` e il record invalido
   restano; una nuova sospensione blocca.
3. **Ripresa**: rebinding solo alternate → testa, solo il cambio provider 27B approvato; le request
   precedenti restano valide; `agent_1` si reinvia solo con `--resume --retry-request`.
4. **Quota requalification**: massimo 1 nel ledger, fuori da 8r+t≤15, dentro 200; massimo
   pianificato 167 su `pilot-03`; nessuna deroga per gli altri 7 casi.
5. **Provider 27B rev2**: `enable_thinking=false` esatto, fingerprint, `max_tokens=2560`; la
   rimozione di `thinking_token_budget` è accettabile?
6. **Script** `revise_pilot_config.py`: nessuna scrittura senza `--execute`, rifiuto prima di
   scrivere, idempotenza, originali intatti, preflight completo.
7. **Runbook** `RUNBOOK_RIPRESA_27B_PILOT_03.md`: comandi ed esiti coerenti col codice.

RED/GREEN: esegui `test_config_revision` sul parent (atteso RED, tranne REV0) e sul candidato.
Esegui su una **fixture che riproduce il ledger reale**: una copia del ledger `pilot-03` con i
percorsi `/Users/...` risolvibili; esegui lo script sulla copia e verifica `stage_runs`,
`requalification` e snapshot 167. Suite a 17 moduli con `FOT_HARNESS_TEST_EVIDENCE`, guardian
separato (baseline 14 failure).

Verbale `harness/VERIFICA_REVISIONE_CONFIG_RIQUALIFICA_27B_03_13.md`: verdetto in prima riga
(`CONFIRMED` / `NOT CONFIRMED`), modello e finestra dichiarati, rilievi con file:riga e prova.
Nessun push, merge o tag.
