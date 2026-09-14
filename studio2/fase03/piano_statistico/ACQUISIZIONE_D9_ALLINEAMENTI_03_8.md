# Acquisizione locale del record D9 nel ramo 03.8

Data: 2026-09-15T00:35:29.997714+02:00.
Sorgente: `/Users/luker/fot-tep-proposta-d9`, branch `codex/studio2-proposta-d9`.
Commit esatto: `aaba893dff8c62f9f9281eec7423eee020235e03`. Nessun merge o importazione del branch.
Destinazione: `/Users/luker/fot-tep-allineamenti-038-r1-r4`, branch `codex/studio2-allineamenti-038-r1-r4`.
Base dell'acquisizione: `5b784219b08de1249636536ac98e9a546b4d4577`
(acquisizione separata dell'OK R1–R4).

## Tre artefatti, stessi percorsi relativi e stessi byte

| File in studio2/fase03 | Byte | SHA-256 |
| --- | ---: | --- |
| `DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md` | 9083 | `fcb113636de80cc87709905324436555e0ba103bd46de3ac079ce0ef7f60f1b8` |
| `CONSEGNA_RECEPIMENTO_D9_2026-09-14.md` | 13282 | `3ea739065f1011ed2fd17bface11231f8857dc3f5256d26eff7abcc1d1ef2c77` |
| `IMPRONTE_DECISIONE_D9_2026-09-14.json` | 11169 | `3b95d17ab3b467bebe5d0bda5fa84d8ab63f3ee13f87397e02caf396654af77b` |

Tutti e tre confrontati byte per byte sia con i blob del commit sorgente sia con
le copie vive, identiche al riscontro. Nessuno era già presente nel target.
Le due voci `artifacts` del JSON coincidono con byte e SHA-256 dichiarati; il
JSON non impronta se stesso: la sua identità è attestata qui e dal blob Git.
Non sono importate le 17 fonti del JSON o i candidati delle altre finestre:
le voci `sources` restano l'inventario storico della registrazione D9.

Decisione approvata: P=C=122B, P_alt=27B con libreria intera di 16 insight;
consumer 122B fisso nello swap; Terra soltanto storico descrittivo interno,
separato dalle nuove stime, senza nuove chiamate. Il 27B non è consumer fallback.
Non occorre chiedere nuovamente l'approvazione dei ruoli.

## Provenienza e riferimenti ereditati

Le tre copie sono record immutabili dell'attività della finestra D9; i loro
stati “recepimento pendente” descrivono il momento della registrazione. Questo
commit acquisisce i record in 03.8; il recepimento documentale segue in un
commit distinto e non viene retrodatato negli originali.

Il link relativo `PROPOSTA_D9_RUOLI_MODELLI_2026-09-14.md` presente nel record
rimanda alla proposta storica, che non è inclusa nelle tre acquisizioni e non è
presente in questo checkout. Risoluzione autorevole e recuperabile:
`git show 95ff8571af02bab79094ed1a6be3f6a7b410c711:studio2/fase03/PROPOSTA_D9_RUOLI_MODELLI_2026-09-14.md`.
Sono verificati 36.141 byte e SHA-256
`a47f42dda7ee9702c292e34ada6b116ac3c85e42ec3a50e68af97c159f0d0f9d`;
la copia resta anche in `/Users/luker/fot-tep-proposta-d9/studio2/fase03/`.
Il rinvio è storico: la proposta non torna efficace e non è importata per
riparare un link alterando il perimetro. L'altro link assoluto alla proposta
harness descrive un documento storico nel worktree indicato e al pin 288dc19,
non il candidato harness in correzione. Nessuna sua scrittura o importazione.
Gli altri rinvii fra i tre artefatti acquisiti si risolvono localmente.

Scelta, acquisizione, recepimento documentale, recepimento eseguibile e qualifica
sono cinque stati distinti. Ordine label 1a, firma materiale 03.8, identità e
configurazioni effettive, qualifiche, fattibilità e autorizzazioni restano
separati. Nessuna configurazione, budget, calendario, collocazione delle chiamate
alternative o nuovo metadato viene deciso per deduzione.

Nessuna modifica al candidato statistico rev.10 o ai verbali/manifest storici.
L'OK su 9a56d12 non certifica il successivo delta. 03.8 e Fase 03 aperte;
nessun push, merge su main, tag, freeze, firma, API, inferenza o simulazione.
