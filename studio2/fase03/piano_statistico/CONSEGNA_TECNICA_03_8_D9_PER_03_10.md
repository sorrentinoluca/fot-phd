# Consegna successiva 03.8 → 03.10: stato documentale D9

Data: 2026-09-15. Documento della sottofase **03.8**, non un file dell'harness.
Successore limitato allo stato D9 della
[consegna rev.10](CONSEGNA_TECNICA_03_10_DA_REV10.md), preservata byte-identica.
Regole e requisiti rev.10 restano nella fonte immutata
[DELTA_HARNESS_03_10.md](DELTA_HARNESS_03_10.md); nessuna modifica R01–R10
è prescritta o importata da questa sessione. La finestra proprietaria valuterà
il recepimento eseguibile sul proprio candidato aggiornato.

Fonte: [decisione dell'autore](../DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md),
commit sorgente `aaba893dff8c62f9f9281eec7423eee020235e03`, SHA-256
`fcb113636de80cc87709905324436555e0ba103bd46de3ac079ce0ef7f60f1b8`.
Record, consegna e impronte sono acquisiti byte-identici localmente in 03.8.
Il nuovo recepimento documentale è candidato per review; quello eseguibile
nell'harness è **ancora pendente e non verificato qui**.

| Oggetto | Decisione già approvata | Residuo distinto |
| --- | --- | --- |
| Producer principale P | 122B | identità e configurazione effettive, input/libreria e conformità da documentare/verificare |
| Consumer C | 122B | resta fisso nello swap; nessun consumer fallback 27B |
| Producer alternativo P_alt | 27B, libreria completa di 16 insight secondo R4 | stesse regole strutturali, nessuna libreria mista o limitata ai fault misurati; collocazione delle chiamate e riusi non scelti qui |
| Terra | solo riferimento storico descrittivo interno, separato dalle nuove stime | nessuna nuova chiamata, produzione o accesso Terra, nessun pooling storico/nuovo |

Queste assegnazioni superano il residuo “ruoli non scelti” nelle consegne
precedenti. Non richiedono una seconda approvazione; i nomi nominali non provano
pesi, revisione, quantizzazione, endpoint, tokenizer/template o serving effettivi.
I dati tecnici e le misure devono essere documentati sui servizi pertinenti;
non trasferire una qualifica dal vecchio endpoint o dedurla da un alias.
Il contatore canonico e i cap R4 restano quelli del contratto congelato;
la scelta del consumer non sostituisce automaticamente il contatore. Capienza
reale e tokenizer/template del servizio sono verifiche distinte.

Restano intatti ledger, conteggio completo per modello, R, riserve, hard stop,
ordine degli stadi e gate rev.10. P=C comporta aggregare richieste distinte sul
122B, non contarle due volte o azzerare contatori. Non si fissano `a=1`, X/Q,
riusi, retry, calendario, capienza o fattibilità con la sola decisione dei ruoli.
Non si sceglie il quartetto della misura swap: vale il rintraccio richiesto dalla
consegna D9, senza dedurlo da D11.

**Ordine label 1a ancora non approvato**, firma materiale 03.8, qualificazione dei
servizi e autorizzazione al pilot restano separati. Nessuna chiave/configurazione
eseguibile è creata qui, nessun GO o prova sul servizio. Il recepimento e i test
harness restano nel cantiere parallelo. Il suo completamento non è un nuovo
prerequisito circolare del freeze statistico, né lo sono gli OOD 03.11, da
verificare dopo freeze e prima delle chiamate. 03.8 e Fase 03 restano aperte.
