# Integrazione finale configurazione D9 Qwen 03.13

Esito: **READY_FOR_INDEPENDENT_REVIEW**. Il candidato privato è tecnicamente
completo e supera i controlli offline, ma non contiene una
`execution_authorization`: non autorizza chiamate, pilot o gate.

## Candidato e confine dei segreti

La configurazione è in
`/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/execution/pilot_d9_execution_candidate_03_13.private.json`,
SHA-256 `fcf4ec0bb3c77193f3aaaaa5204faf34b7c589ed8c558b4fac54601e1ce58710`.
Lo SHA-256 canonico senza `execution_authorization`, utilizzabile da una successiva
decisione indipendente dell'autore, è
`1305c158a98c40cb57e45b43e8d872d3d66e4d6d050d1d167c91b23e0a2fccc8`.

La directory privata è `0700` e i cinque JSON sono `0600`. L'URL completo 122B
compare soltanto negli artefatti privati che devono usarlo. API key, password e
utente SSH non sono presenti nei cinque file; il record riservato originale non è
stato copiato né improntato. Il repository conserva soltanto questo rapporto e il
manifest redatto.

## Chiusura dei quattro blocker di `56779e2`

1. **Identità 122B chiusa.** La qualifica non generativa finale è legata ai byte
   `4e7e2b67…`, all'alias `qwen3.5-122b`, al root
   `Qwen/Qwen3.5-122B-A10B-FP8` e al contesto 131072. Revisione, fingerprint,
   versione, parser e altri campi non esposti restano dichiarati `NOT_EXPOSED`;
   `expected_response.system_fingerprint` è esplicitamente `null`.
2. **Producer config distinte chiuse.** Il 122B usa `max_tokens=2560` senza
   temperatura, seed o thinking budget e con accounting `exact_prompt_tokens`.
   Il 27B usa la proposta prespecificata `2560 / 0.0 / 20260829 / 2048`. I due
   file hanno hash distinti e sono entrambi nella allowlist del candidato.
3. **Snapshot 27B/R4 chiuso.** I tre file locali della revisione
   `017b9c7a…` corrispondono ai pin R4 e superano `verify_tokenizer`.
4. **Identità 27B chiusa.** La qualifica finale `ebf01ced…` lega alias, root,
   revisione, vLLM 0.28.0, contesto 16384 e snapshot locale. La configurazione usa
   il loopback prescritto sulla porta 18001; il tunnel non è stato aperto.

Gli STOP intermedi restano nei precedenti artefatti e non sono stati sostituiti o
reinterpretati come evidenza finale.

## Verifiche offline

- `validate_config`: PASS con ruoli 122B/122B/27B, alternate nel pilot,
  `d9.status=DOCUMENTED_FOR_AUTHORIZED_STAGE` e nessun requisito mancante.
- `require_execution`: rifiuto atteso esclusivamente perché manca la distinta
  execution authorization.
- Tokenizer guard: PASS per 122B e 27B/R4.
- Storia esterna e ledger: PASS read-only; S=4, native=0, receipts=0, stages=0,
  hard-stop event=0. SHA del ledger prima e dopo:
  `02ce8df46d04300b9eb19b0fbc3345c5edd41e7ea17bd1391f22c53f7a6d9d61`.
- Producer 122B: parsing/validazione PASS; 8/8 prompt fittano offline, massimo
  1395 token input e margine minimo 127117.
- Producer 27B: parsing/validazione PASS; 8/8 prompt fittano offline, massimo
  1437 token input e margine minimo 12387.
- Dry-plan dei due producer e del consumer:
  `PLAN_ONLY_NO_PROVIDER_CALLS`; nessun bind di stage o intent.
- Il piano consumer resta 3/6/9 e il budget resta non congelato finché il probe
  reale A/B-LF/E-LF non soddisfa la regola prespecificata.
- Gli input autorizzati restano sviluppo Study 2 e Normal-dev; nessun dato 03.11
  final-test, OOD o scorta entra nel pilot.

## Piano cumulativo

Il 122B conta 8 chiamate producer, 3–9 consumer budget e 120 gate: 131–137 future.
Il 27B conta 8 chiamate alternate future. Lo storico S=4 è contato una sola volta:
totale base cumulativo 143–149. Con la riserva condivisa
`8*remediation+transport<=15`, il massimo pianificato futuro è 160 e quello
cumulativo 164; hard stop 200, margine 36.

Contabilità dell'integrazione: **zero chiamate provider, zero token, zero nuovi
intent, ledger invariato**. Nessun tunnel, producer, pilot o gate è stato avviato.
