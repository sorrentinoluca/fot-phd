# Esecuzione producer Qwen D9 — 03.13

Esito: **STOP** durante `producer_conformity`, alla prima richiesta 122B. Nessun
retry è stato eseguito; il tunnel 27B non è stato aperto e
`alternate_conformity` non è iniziato.

## Autorizzazione e avvio

L'ACCEPT è stato acquisito nel commit documentale `b795e79fee99f07d1c8bf267ed05203a5e54915b`.
Prima del trasporto, `validate_config` e `require_execution` erano PASS, i guard
tokenizer/service/provider e le quote erano PASS e i dry-plan non avevano modificato
il ledger. La configurazione autorizzata ha SHA-256 byte
`3c29f8ff414d27c36dcad3cf49e03ed02d8c944ed651c944e89f8df09eb30131`;
lo SHA canonico senza authorization resta
`1305c158a98c40cb57e45b43e8d872d3d66e4d6d050d1d167c91b23e0a2fccc8`.

La rotta privata 122B risultava raggiungibile. L'entrypoint versionato è stato
avviato con 8 casi prespecificati, `max_tokens=2560`, senza temperatura, seed,
thinking budget o retry automatici.

## Richiesta certa e causa dello STOP

È stata addebitata una sola nuova chiamata:

- logical ID `agent_1`;
- request ID `0fc7a507bda5da6dd7a29c8e39d67acf48747e6efdf1f73f1e7bdd528ed7f684`;
- response ID `chatcmpl-a0e2cd74648ea3ef`;
- intent `2026-09-16T01:28:24.343169+00:00`, risposta ricevuta
  `2026-09-16T01:28:45.236063+00:00`, completamento durevole
  `2026-09-16T01:28:45.283270+00:00`.

L'alias restituito coincide con `qwen3.5-122b`, ma il contratto autorizzato
richiedeva fingerprint esplicitamente `null`, mentre la risposta ha esposto
`vllm-0.27.1-934a3247`. Il guard ha quindi registrato `identity_valid=false` e
sospeso il pilot. La stessa risposta ha `finish_reason=length`, nessun JSON testuale
valido e zero coppie insight conformi.

L'accounting esatto è invece PASS: prompt locale/server 1395, completion 2560,
totale 3955. Il raw e il record sono preservati nel ledger privato con SHA-256
rispettivamente `e6489e73…` e `0136fe47…`; non sono committati.

## Conteggi e stato durevole

122B: 1 chiamata tentata, 1 risposta ricevuta, 1 record durevole, 0 output schema-validi,
0 coppie insight conformi. 27B: 0 chiamate e 0 risposte. Nuove chiamate addebitabili:
1; con S=4 storico contato una volta, cumulativo 5.

Il ledger passa `integrity_check`, ha WAL vuoto ed è passato da SHA-256
`02ce8df4…` a `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`.
Stato finale: external history 4, richieste native 1, stage 1, receipt 1, response 1,
eventi 4; nessun accounting STOP. Il journal privato ha SHA-256
`6c64e4412ab7c4ea8bea85ff40284869ee6bc703ec2a2b106034fd3399370d4b`.

Non sono stati eseguiti retry, remediation, alternate, consumer budget probe,
stability gate, final-test, OOD o scorte. Nessun URL o segreto è incluso negli
artefatti versionati.
