# Rapporto breve — preparazione mapping S=4 e ledger pilot 03.13

Stato: **CANDIDATO ALLA REVIEW; NESSUNA IMPORTAZIONE E NESSUNA CHIAMATA**.

## Risultato

È stato inizializzato offline il ledger operativo prespecificato:

- `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/ledger.sqlite3`
- `pilot_id=studio2-fase03-d9-pilot-001`
- schema v2, richieste native 0, storico esterno 0, eventi scientifici 0, chiamate 0.

È stato preparato il package candidato
`MAPPING_REVIEWED_STORICO_S4_PILOT_03_13.json`, 4.427 byte, SHA-256
`98608abe9831707254208ed29e493f92d29c06313a219d238ceec933f064d53c`.
Contiene quattro identità nuove e deterministiche, marcate
`ASSIGNED_DURING_RECONCILIATION`: S1 è `HISTORICAL_OUTCOME_UNCERTAIN`; S2–S4 sono
`COMPLETED`. Il conteggio candidato è quattro contributori storici univoci alla quota
cumulativa, da addebitare una sola volta, zero richieste native e nessuna variazione
delle quote remediation/transport.

## Fonti pinnate

| Fonte | SHA-256 |
| --- | --- |
| `RICOGNIZIONE_STORICO_S_2026-09-15.md` | `f9e1ed2f72a16b00dd8c39b0a012813e9b6fc09d1c6675a7d6c4fb8f2ddad5f7` |
| `INVENTARIO_RICOGNIZIONE_STORICO_S_2026-09-15.json` | `c49b499d56251f3b72335ed3a6cb21f82388984079322d0163a1f7d0c3a4feb2` |
| `PROPOSTA_RICONCILIAZIONE_STORICO_S_ESTERNO_2026-09-15.md` | `55a3e8a7dd37966abf8d6f679e4ef7bffdc6077480d51bae56a7d917555ccd5a` |
| `/Users/luker/Downloads/VERIFICA_RICOGNIZIONE_STORICO_S_1.md` | `cbf363316646f5f75a4123adcb30f312fce0dfce6cb0548bf953deb2718d7e31` |
| summary | `c9adf2a8f07d9058257cc2c51a00064662874611875a715c716a1f1ea4828368` |
| attempts | `cc3a21d8a045598b844372b04af4a68a4ac6702c05c5428a457eed098f03c382` |
| records con raw incorporati | `825b649e409e462b953da263fd01d11b9d92563fd930747da17e36f93d94b158` |
| `HISTORICAL_S_SOURCE_INVENTORY_2026-09-15.json` | `ae8b89f23fc38344aa777037edf71f9dcf5e504c1e35e85482089d57c6a7682f` |
| `REGISTRO_DECISIONI_AUTORIALI_D9_2026-09-15.md` | `feea9dcbaf2e9810e6a4c6a72d0336c236313a98f595ff0cf876141987cef0c0` |
| `pilot_d9_decisions_received.json` | `9d3870b659f28f24ee2b275acc76ca90e67191a59d481643f429e87851a46367` |

Le fonti sono state lette senza modifica. Summary, attempts e records usati dal
package sono i file canonici sotto `/Users/luker/fot-tep/studio2/fase03/results/`;
i loro byte coincidono con quelli ricogniti. Non esistono raw separati: i tre envelope
`response_raw` e i relativi output sono incorporati nelle tre righe records.

## Controlli eseguiti

- HEAD/tree e worktree iniziale coincidenti con il mandato;
- hash e dimensioni delle fonti ricalcolati;
- JSON/JSONL parsati, cardinalità 1 attempt + 3 records;
- binding di riga, identità e request ID ricalcolati con JSON canonico;
- coerenza semantica dei tre record completi e dei rispettivi raw già verificata dalle
  fonti acquisite e riconfermata offline;
- schema e contenuto del ledger riletti in modalità read-only dopo l'inizializzazione;
- package JSON valido; nessuna approval o importazione usata.

Il controllo semantico mirato del package è `PASS`: quattro identità univoche e
ricalcolabili, binding S1–S4 ordinati, tre record completi validi e stato logico del
ledger invariato. L'apertura SQLite read-only ha materializzato i sidecar temporanei
WAL/SHM senza cambiare i byte del database; a connessione chiusa sono stati rimossi e
la directory operativa contiene di nuovo soltanto `ledger.sqlite3`, con la stessa
impronta iniziale.

Il guardian documentale è stato eseguito separatamente ed è **NON PASS** nel baseline
storico: 35 test, 14 failure e 1 skip. Non è riclassificato come verde e non riguarda
i quattro nuovi artefatti di preparazione.

Non è stato creato `IMPORT_AUTHORIZED`. Il valore `MAPPING_REVIEWED` è il formato
contrattuale del package candidato, non un'autorizzazione: l'hash esatto sopra deve
ancora ricevere review indipendente e successiva approvazione autoriale.

Non sono stati chiamati provider o endpoint e non sono stati eseguiti sonda, gate,
batch o pilot. Runtime, test, configurazioni, storico S e fonti sono rimasti invariati.
