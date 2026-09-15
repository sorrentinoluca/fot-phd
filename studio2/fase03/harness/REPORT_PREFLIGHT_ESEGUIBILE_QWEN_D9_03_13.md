# Report preflight Qwen D9 03.13

Esito: **STOP**. La preparazione è rimasta interamente offline. Il candidato è
deliberatamente fail-closed e non può essere trasformato in configurazione eseguibile
aggiungendo soltanto una execution authorization.

## Base e acquisizione minima

La base è stata verificata a commit
`d38da38b96d252ba1a224b6f373cb08ca519a1ed`, tree
`02ad075223d42bf3db0d17927c9938a6274ecc75`.

La review indipendente dell'import S=4 è stata copiata byte-identica in
`studio2/fase03/harness/reviews/VERIFICA_IMPORT_STORICO_S4_LEDGER_PILOT_03_13.md`:
SHA-256 `a70a6170c75445ce670c095a462ebc8be97209face16e7cbcc7c187644c0d2ee`.
Il suo OK riguarda soltanto l'import storico e non autorizza esecuzione.

## Artefatti accertati

- La decisione D9 mantiene producer 122B, consumer 122B e alternate 27B nel pilot;
  l'ordine delle nove classi è approvato e legato al relativo record.
- L'accounting 122B corretto ha review indipendente `ACCEPT`; lo snapshot client
  122B alla revisione `a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9` è stato collocato
  nel runtime esterno con directory `0700` e file `0600`. I tre pin sono verificati
  dal guard reale. L'assenza di `/tokenize` server resta un limite dichiarato e non
  viene convertita in parità server/client.
- Il record storico 27B conserva pesi, revisione, processo vLLM e i tre pin
  tokenizer/template, ma lo snapshot recuperabile è presente soltanto nel percorso
  Linux remoto documentato, non sul Mac.
- Lo schema insight R4, l'inventario reale degli input producer, il piano statistico
  rev. 10 e il budget rev. 10 risultano integri ai pin registrati nel manifest.
- Il worktree 03.11 chiuso è a commit
  `349ead315de575cf43977fdf807d43b64070546c`, tree
  `38e546c0c1f253af5dc75fe65505b8039fc5e189`, con audit PASS di 89 run
  (64 fault primari, 8 Normal primari, 6 OOD, 11 scorte). Questi dati sono final-test,
  OOD o scorte e sono quindi **esclusi** dagli input del pilot. Il pilot usa soltanto
  evidenza di sviluppo congelata e Normal-dev tramite
  `PILOT_INPUT_SOURCES.pending.json`.

L'inventario producer reale deve restare `INCOMPLETE` con il solo requisito
«16 real schema-valid producer insights»: quegli insight sono l'output delle prime
otto chiamate, non un loro prerequisito. Per lo stesso motivo manifest consumer e
prompt preparati completi possono essere creati soltanto dopo un ciclo producer
durevole concluso con PASS. È una dipendenza di sequenza, non un blocker scientifico
per iniziare la conformità producer.

## Connessioni riservate

`/Users/luker/fot-tep/studio2/fase03/server_enea.json` esiste, è JSON valido e non è
tracciato da Git. Contiene record di connessione denominati `122B` e `27B`; nessun
valore, URL completo, credenziale o hash del file è riportato in questo rapporto o
negli artefatti versionati. L'etichetta del record `27B` è coerente con il ruolo, ma
non sostituisce la verifica scientifica dell'identità effettivamente esposta.

Il file originale ha permessi correnti `0600`, quindi restrittivi. Non ne è stato
modificato il contenuto. Il piano operativo non segreto è conservato fuori repository
in `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/runtime_connection_plan.json`,
modo `0600`, SHA-256
`8dbeb38f2e406a5860e451a6a5ff5f94e085e272a694098acb5e7fe2d0aeee32`.
Prescrive il caricamento runtime del record 122B e, per il secondo server, un tunnel
locale `127.0.0.1:18001` verso il loopback remoto `127.0.0.1:8001`, ricavando host e
utente soltanto al momento dell'uso dal record riservato. Il tunnel non è stato aperto.
L'operatore ha dichiarato disponibile la VPN ENEA, ma lo stato ENEA non è stato
identificato come attivo dai controlli locali; nessuna connessione o retry è stata
tentata.

## Blocker indispensabili

1. **Tecnico — identità 122B.** I byte disponibili documentano `/models`, limiti e
   tokenizer client, ma non stabiliscono la coppia `returned_model` / fingerprint
   richiesta dal guard di risposta né un service record completo.
   **Azione minima:** acquisire e conservare i raw metadata originali e il contratto
   esatto dell'identità di risposta (fingerprint `null` solo se esplicitamente
   indisponibile), quindi scrivere e improntare il service record 122B.

2. **Tecnico-scientifico — configurazioni producer.** Non esistono due producer config
   distinte e congelate. Temperatura, seed e thinking storici del 27B consumer non sono
   trasferibili al 122B né al producer alternate.
   **Azione minima:** congelare per decisione autoriale una configurazione producer per
   ruolo, con `max_tokens` e soltanto i controlli supportati e prespecificati, poi
   registrarne gli hash.

3. **Runtime — snapshot 27B/R4.** I byte tokenizer/template alla revisione
   `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a` non sono disponibili sul Mac.
   **Azione minima:** dopo accesso VPN, copiare o montare i tre file esatti in un path
   assoluto recuperabile e verificare i pin R4 prima di ricostruire il candidato.

4. **Runtime-tecnico — identità della connessione `27B`.** L'uso della rotta riservata
   e la sua etichetta non provano che il servizio sia il 27B prespecificato; processo e identità disponibili
   sono storici.
   **Azione minima:** con VPN attiva aprire il tunnel prescritto e conservare una verifica
   non generativa `/models`/processo che leghi il servizio al 27B approvato, senza retry
   se la VPN è assente.

Non c'è un blocker scientifico sugli input producer iniziali; i dati 03.11 non sono
acquisiti nel candidato perché vietati come input e non necessari all'esecuzione delle
otto chiamate di conformità.

## Configurazione e verifiche offline

Il candidato fail-closed è
`studio2/fase03/config/pilot_d9_execution_candidate_03_13.json`, SHA-256 dei byte
`5431ab2fe4bb4a09d065d1a5e5d5339bf860ddbfbc3029b8802f07606980d7ff`.
Il suo SHA-256 canonico, calcolato escludendo l'inesistente campo
`execution_authorization`, è
`233b83a6999a624463edc756ef4aaa5b1f20fd4c5d1e5140a98e0d3959c898e6`.
Questo hash identifica lo STOP corrente e **non è eleggibile per ACCEPT o execution
authorization**; la configurazione completa avrà necessariamente un hash diverso.

Esiti mirati:

- `validate_config`: rifiuto atteso `D9: prerequisites remain incomplete`;
- `require_execution`: rifiuto atteso prima del controllo dell'approval, perché lo stato
  tecnico non è eseguibile; quindi non è soddisfatta la prova «fallisce soltanto per
  authorization»;
- package storico e approval: validazione reale PASS, quattro mapping esatti;
- dry-plan producer e consumer: `PLAN_ONLY_NO_PROVIDER_CALLS`, nessun intent;
- ledger read-only: S=4, tre completed + uno uncertain, native=0, receipts=0, stages=0,
  hard-stop event=0.

Piano chiamate: il 122B ha 8 conformità producer + 3–9 budget + 120 gate =
**131–137** richieste future base; il 27B ha **8** richieste future base alternate.
Lo storico S=4 è attribuibile al vecchio servizio 27B e si conta una volta: totale
cumulativo base **143–149**. La riserva unica soddisfa
`8*remediation+transport<=15`; massimo futuro pianificato **160**, cumulativo **164**,
hard stop **200**, margine non spendibile **36**. Gli upper bound per modello dipendono
dall'attribuzione della riserva e non sono sommabili.

Nessun comando di primo pilot è emesso finché lo STOP non è chiuso. Non è stata creata
alcuna execution authorization.

Contabilità finale dell'attività: **zero chiamate provider, zero nuovi intent, zero
tunnel, ledger invariato**.
