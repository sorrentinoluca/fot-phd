# Prompt breve — review indipendente mapping S=4 e ledger pilot 03.13

Esegui una review indipendente, in sola lettura, del commit `HEAD` che contiene questo
file; il parent atteso è `7db7e54a4b67a54eac0642757063a34c46e47f74`.
Non modificare repository o ledger e non creare `IMPORT_AUTHORIZED`.

Verifica il package:

- path: `studio2/fase03/harness/MAPPING_REVIEWED_STORICO_S4_PILOT_03_13.json`
- SHA-256 atteso: `98608abe9831707254208ed29e493f92d29c06313a219d238ceec933f064d53c`
- ledger: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/ledger.sqlite3`
- `pilot_id`: `studio2-fase03-d9-pilot-001`

Controlla sui byte reali, non sul solo accordo fra hash: schema del package; derivazione
deterministica e unicità delle quattro identità; binding ordinato S1→attempts:1 e
S2–S4→records:1–3; tipi e campi consumati; response ID, usage, timestamp, fingerprint,
finish reason e raw/output delle tre risposte complete. Conferma che S1 resti
`HISTORICAL_OUTCOME_UNCERTAIN`, senza zero-token proof, retry o token inventati, e che
S=4 sia un unico addebito cumulativo senza modificare quote native/remediation/transport.

Ricalcola almeno questi hash fonte:

- summary `c9adf2a8f07d9058257cc2c51a00064662874611875a715c716a1f1ea4828368`;
- attempts `cc3a21d8a045598b844372b04af4a68a4ac6702c05c5428a457eed098f03c382`;
- records/raw `825b649e409e462b953da263fd01d11b9d92563fd930747da17e36f93d94b158`;
- ricognizione `f9e1ed2f72a16b00dd8c39b0a012813e9b6fc09d1c6675a7d6c4fb8f2ddad5f7`;
- inventario `c49b499d56251f3b72335ed3a6cb21f82388984079322d0163a1f7d0c3a4feb2`;
- proposta `55a3e8a7dd37966abf8d6f679e4ef7bffdc6077480d51bae56a7d917555ccd5a`;
- review ricognizione `cbf363316646f5f75a4123adcb30f312fce0dfce6cb0548bf953deb2718d7e31`.

Apri il ledger in sola lettura e conferma: schema v2, `pilot_id` esatto, zero richieste
native, zero stage/eventi/risposte/ricevute, nessuna tabella o riga `external_history`.
Valuta esplicitamente la distinzione fra il valore di schema `MAPPING_REVIEWED`, la review
precedente limitata a ricognizione/proposta e la review ancora necessaria del mapping
esatto. Segnala come blocker qualsiasi rappresentazione che anticipi `IMPORT_AUTHORIZED`.

Emetti `ACCEPT` o `REJECT` con commit/tree, hash ricalcolati e limiti. Non applicare il
mapping, non mutare il ledger e non chiamare provider, endpoint, sonda, gate o pilot.
