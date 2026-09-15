# Consegna — configurazione D9 122B senza `/tokenize`

Stato: **CANDIDATO LOCALE COMMITTATO, NON QUALIFICATO E NON AUTORIZZATO ALL'ESECUZIONE**.

È stato aggiunto `studio2/fase03/config/qwen_122b_api_primary_d9.json`. Conserva letteralmente
i dati acquisiti: servizio, modello/alias, root osservata, contesto 131072, soli endpoint
`/v1/chat/completions` e `/v1/models`, hash dei tre raw e snapshot client congelata
`Qwen/Qwen3.5-122B-A10B-FP8@a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9`.
Non introduce endpoint ulteriori, parametri server non osservati, credenziali, URL completo,
autorizzazione esecutiva o riconciliazione/applicazione dello storico S. Il parametro
`temperature` non compare né nella configurazione né nel contratto del payload 122B.

Il runtime producer ora passa gli stessi `messages` effettivamente trasmessi a un unico
`TokenizerAccountingGuard`. Per ogni risposta 122B con contabilità abilitata, il guard calcola
offline `len(tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True))`
e richiede l'uguaglianza esatta con `usage.prompt_tokens` (intero, non booleano, non negativo).
Prima di parsing, output valido, sonda o gate, il ledger persiste un evento create-once con
messaggi canonici e hash, revisione snapshot, conteggio locale/server, esito e hash del raw.
Un rifiuto persiste anche `stop:tokenizer_accounting`; bind, riserva, retry, resume, sonda e gate
falliscono quindi con `FATAL_ACCOUNTING_ERROR`, anche dopo restart. La rilettura ricalcola hash e
conteggio dal raw e dai messaggi persistiti.

## Test eseguiti

Eseguito offline, senza client provider né rete:

```text
python3 -m unittest studio2.fase03.harness.test_tokenizer_accounting -v
Ran 3 tests in 0.278s
OK
```

Copertura osservata: otto risposte valide distinte e legate alle rispettive richieste; caso
positivo; `usage` assente; `prompt_tokens` assente, `null`, booleano, stringa, negativo e diverso;
STOP durevole con blocco della richiesta successiva e dopo restart; alterazione di messaggi,
snapshot e raw persistito. I test usano esclusivamente tokenizer e risposte sintetici locali.

## Sola ispezione e verifiche bloccate

Ispezionati il contratto D9, il ledger, runner, CLI e percorsi di resume: la validazione è posta
dopo il salvataggio durabile del raw e prima dell'evaluazione/output; i percorsi che riservano o
riaprono uno stage interrogano il medesimo STOP durevole.

Non eseguiti, perché non autorizzati o non disponibili: chat completion, `/models`, `/version`,
`/tokenize`, sonda, gate, pilot, qualificazione del servizio, identità byte-identica del tokenizer
server, execution authorization e riconciliazione/applicazione dello storico S. L'uguaglianza
locale/server qualifica esclusivamente la singola richiesta operativa; non prova il tokenizer
server né autorizza il pilot.

La regressione harness più ampia è stata tentata, ma è bloccata dall'ambiente: `jsonschema`
carica `rpds` arm64 in un interprete x86_64 e fallisce all'importazione. Non viene conteggiata
come PASS né attribuita a questo delta.
