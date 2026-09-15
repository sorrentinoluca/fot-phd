# Prompt minimo — review chiusura 03.10

Verifica in sola lettura il delta esatto
`8fbbfa01820d00562188594123182982939187b2..dcc742282124784c3fd9004dc642962a9b1e9868`, nel worktree
`/Users/luker/fot-tep-harness-d9-correzioni`.

Controlla soltanto: identita Git e diff; coerenza del contratto di
riconciliazione S; atomicita/idempotenza/addebito S=4; assenza di autorizzazioni
a chiamate o ledger reali; corretto confine 03.10 offline / 03.13 servizi e
pilot. Esegui solo `test_history_reconciliation.py` con Python 3.11 arm64; non
ripetere guardian o suite gia registrate, ma verifica le impronte dei log.

Produci un solo file `VERIFICA_CHIUSURA_03_10.md`, con prima riga `OK` o
`NON OK`, rilievi bloccanti, commit/tree e limiti. Non modificare il candidato,
non creare altri artefatti, non effettuare chiamate esterne.
