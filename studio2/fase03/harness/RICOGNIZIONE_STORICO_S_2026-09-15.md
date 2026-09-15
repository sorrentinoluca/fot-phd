# Ricognizione delle identità durevoli dello storico S

**Stato: ricognizione documentale locale; nessuna riconciliazione eseguita, nessun GO.**

Data effettiva della ricognizione: 15 settembre 2026, Europe/Rome. Mandato:
`PROMPT_PROSECUZIONE_03_10_RICOGNIZIONE_STORICO_S_2026-09-15.md` nella copia
principale. Worktree esaminato: `/Users/luker/fot-tep-harness-d9-correzioni`, branch
`codex/studio2-harness-d9-correzioni`, base
`a5ffc5e555df998431c615a97a2d9ff2ed087d7f`, tree
`5200def66e5084a22ca719544d4c108cdde12701`.

La ricognizione è stata svolta da Codex, agente basato su GPT-5. Il livello di
reasoning effettivo non è esposto alla sessione e non viene inventato; il modello
suggerito dal mandato, Sol con reasoning high, non è assunto come identità effettiva.

## Esito

Le fonti disponibili identificano quattro tentativi provider: un HTTP 400 registrato
come rifiutato prima dell'inferenza e tre risposte completate. Per le tre risposte
sono disponibili timestamp, response ID, modello restituito, fingerprint, usage,
finish reason, prompt hash e hash dell'output. Questi campi sono internamente coerenti
nei byte esaminati.

Non sono disponibili nelle fonti esaminate il percorso e il `pilot_id` di un ledger
autorizzato, quattro `request_id`, quattro `request_identity_sha256` o un binding
revisionato fra righe del ledger e fonti raw/record. Per S1 non è disponibile una
prova durevole conforme al contratto D03 che stabilisca zero token: il solo HTTP 400
e il campo storico `inference_completed=false` non la sostituiscono.

Ne segue che lo storico non può essere registrato come `RECONCILED` con i dati
attuali. Rimane valido l'addebito prudenziale approvato **S=4 una sola volta**:
le tre inferenze completate sono comprese nei quattro tentativi e non producono
tre addebiti aggiuntivi.

## Fonti lette e impronte

I sei file minimi sono stati letti e validati come JSON o JSONL. Le impronte dei
tre file primari coincidono sia con i collegamenti nel summary/inventario sia con
i blob dei commit di origine.

| Fonte | Byte | SHA-256 | Provenienza Git |
| --- | ---: | --- | --- |
| `results/provisional_cap_stress/provisional_stress_probe_summary.json` | 4375 | `c9adf2a8f07d9058257cc2c51a00064662874611875a715c716a1f1ea4828368` | introdotto da `6a029270a7c29122bd7c56ee2b34ac236f359839` |
| `results/provisional_cap_stress/provisional_stress_probe_attempts.jsonl` | 275 | `cc3a21d8a045598b844372b04af4a68a4ac6702c05c5428a457eed098f03c382` | introdotto da `4691acbbf486fcbf205fec374ae614eed5fa5605` |
| `results/provisional_cap_stress/provisional_stress_probe_records.jsonl` | 20221 | `825b649e409e462b953da263fd01d11b9d92563fd930747da17e36f93d94b158` | introdotto da `6a029270a7c29122bd7c56ee2b34ac236f359839` |
| `harness/HISTORICAL_S_SOURCE_INVENTORY_2026-09-15.json` | 3595 | `ae8b89f23fc38344aa777037edf71f9dcf5e504c1e35e85482089d57c6a7682f` | `3180aeaacbec25a5907d556e8ca2aa7060a04865` |
| `harness/REGISTRO_DECISIONI_AUTORIALI_D9_2026-09-15.md` | 2611 | `feea9dcbaf2e9810e6a4c6a72d0336c236313a98f595ff0cf876141987cef0c0` | `af50d54f1efea2c489b04f54e16cd99778f20c31` |
| `config/pilot_d9_decisions_received.json` | 2456 | `9d3870b659f28f24ee2b275acc76ca90e67191a59d481643f429e87851a46367` | `3180aeaacbec25a5907d556e8ca2aa7060a04865` |

Consultati inoltre, solo per contratto e provenienza, `PROVISIONAL_STRESS_PROBE.md`,
`harness/d9.py`, `harness/ledger.py`, il contratto D9 e le occorrenze Git mirate
dei tre response ID, del timestamp S1 e dell'hash del summary. Le fixture di test
contenenti ledger non sono state trattate come ledger storico autorizzato.

## Matrice S1–S4

“Trovato e verificato” significa presenza, formato, hash e coerenza interna nei
byte locali; non significa nuova verifica del servizio o autenticazione esterna.
“Dichiarato ma non verificato” conserva una dichiarazione della fonte senza
promuoverla a prova semantica. “Non disponibile nelle fonti esaminate” non significa
che il dato non sia mai esistito.

| Campo | S1 | S2 | S3 | S4 |
| --- | --- | --- | --- | --- |
| Ordinale/tipo | trovato e verificato: tentativo 1 | trovato e verificato: risposta 1 dei records | trovato e verificato: risposta 2 | trovato e verificato: risposta 3 |
| Esito | dichiarato ma non verificato dal servizio: `REJECTED_BEFORE_INFERENCE`, HTTP 400 `uniqueItems` | trovato e verificato nei record: `COMPLETED`, parsing valido | trovato e verificato nei record: `COMPLETED`, parsing valido | trovato e verificato nei record: `COMPLETED`, parsing valido |
| Timestamp | `2026-09-13T00:39:31+00:00` | `2026-09-13T00:40:14.133715+00:00` | `2026-09-13T00:40:46.960150+00:00` | `2026-09-13T00:43:19.495953+00:00` |
| Condizione/prompt | non disponibile | A / `S2-P03-031` | B-LF / `S2-P03-004` | E-LF / `S2-P03-005` |
| Prompt SHA-256 | non disponibile | `bf5bc383472092fdd262ee08becc8b20d6e2656aa21678fe05851a1c704f1df5` | `073fda4269027701f83550ec1513f6fc0d21ceff53dd3ae69f432bf7b0bdb6cd` | `85d063eb2b4f57400f3bd5f422fc67c2ca9fa51533347e22fcd847c2b00712ae` |
| Provider response ID | non disponibile | `chatcmpl-a2c8b987009e9048` | `chatcmpl-b0321b315d5b2d64` | `chatcmpl-8e6fdbca7d5ac3c4` |
| Usage prompt/completion/total | non disponibile | 6579 / 409 / 6988 | 9875 / 2174 / 12049 | 9875 / 835 / 10710 |
| Finish reason | non disponibile | `stop` | `stop` | `stop` |
| Raw output SHA-256 | non disponibile | `61666e0305bd7c9cb6d476b0dcd9e3627b90a7fbe1f8e865a861e2cf7eb58aa4` | `b573b0ebf52c4a9a74e0d5b0d7e1557f6e8db4baeea239ae8f1f6639c23825bf` | `5049a49b668ac5740d37868c58f312432fbc34b471a7d2da99d2dc293fe937b5` |
| Returned model/fingerprint | non disponibile | `fot-exp2-consumer` / `vllm-0.28.0-5fc21ed4` | uguale a S2 | uguale a S2 |
| Ledger path / `pilot_id` | non disponibile | non disponibile | non disponibile | non disponibile |
| Ledger `request_id` | non disponibile | non disponibile | non disponibile | non disponibile |
| `request_identity_sha256` | non disponibile | non disponibile | non disponibile | non disponibile |
| Binding ledger↔raw/record revisionato | non disponibile | non disponibile | non disponibile | non disponibile |
| Prova D03 zero-token | **non stabilita** | non applicabile alla risposta completata | non applicabile | non applicabile |

Per S2–S4 sono state ricalcolate le tre impronte di `raw_output`; ciascuna coincide
con il record. `response_raw.id`, modello, fingerprint, contenuto, finish reason e
usage coincidono con i campi di primo livello. Le tre righe coincidono con il
summary per condizione, prompt, token e hash. Questa coerenza non crea i quattro
`request_id` o il binding col ledger mancanti.

La storia Git mirata ritrova S1 in `4691acb` e S2–S4 in `6a02927`; le occorrenze
successive sono copie/recepimenti documentali. Non è emerso un ledger autorizzato
contenente quei response ID. I database presenti nel candidato sono fixture di
test e non possono essere promossi a fonte dello storico reale.

## Stato rispetto al contratto corrente

Il runtime D9 richiede un documento di riconciliazione con `status=RECONCILED`,
revisore, fonte esatta, stesso `pilot_ledger` della configurazione e una mappa di
quattro `request_id` a quattro hash dell'`identity_json`. `validate_history`
ricontrolla questa mappa contro le righe del ledger nella transazione della
decisione. Questi prerequisiti non sono soddisfatti.

Il prospetto `pilot_d9_decisions_received.json` resta quindi correttamente sospeso:
`history_reconciliation=null`, servizi e configurazioni null, qualifica non svolta
e `pilot_go=false`. L'approvazione S=4 stabilisce la contabilità prudenziale, non
fornisce identità o autorizzazione esecutiva.

La [proposta separata](PROPOSTA_RICONCILIAZIONE_STORICO_S_ESTERNO_2026-09-15.md)
descrive un possibile contratto futuro. Richiede review indipendente e approvazione
esplicita prima di qualsiasi implementazione.

## Controlli e limiti

- JSON e JSONL validati: un tentativo e tre record; summary 4 richieste/3 inferenze.
- Impronte dei file ricalcolate; blob Git originari uguali ai byte correnti.
- Collegamenti summary→attempts/records verificati.
- Coerenza raw/response/usage verificata per 3/3 record.
- Ricerca Git limitata a percorsi e identificatori pertinenti.
- Nessuna suite harness rieseguita; nessun test scientifico richiesto da questa ricognizione.
- Nessun runtime, ledger, loader, configurazione eseguibile, raw output o record storico modificato.
- Nessuna API, SSH, inferenza, replay, retry, sonda o pilot.

Rimangono bloccanti: identità ledger durevoli oppure un contratto approvato per
storico esterno, metadati/qualificazioni dei servizi e autorizzazione esecutiva.
