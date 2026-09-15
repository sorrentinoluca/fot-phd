# Delta D9 eseguibile — contratto prima del codice

15 settembre 2026. Base documentale `5886c6f9d078ee624deaec08763e04c14e96e4f0`;
tecnico antecedente `aae29a908356e4a4842a214fdc3db9bff26ec3ca`, tree
`4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`. Nuovo delta da verificare,
nessuna estensione dell'OK D04. Profilo implementativo locale/offline.

## Fonti e decisioni

Fonti esatte in [SOURCES.json](d9_evidence/SOURCES.json), copie da blob Git:
D9 `aaba893`, piano rev.10/budget/delta `6aaa5b3`, inventario/checklist/richiesta
`b65834d`. Ruoli D9 prevalgono sui nomi e sugli stati temporali superati delle
fonti rev.10. R4 resta `3c64390`; contratti D03/D04 e acquisizioni intatti.
P=C=122B, P_alt=27B completo (16 insight), C fisso nello swap, Terra storico
interno. Nessun fallback, fattoriale o gate consumer 27B.

## Mappa ingresso → decisione

| Valore/percorso | Acquisizione e persistenza | Rilettura e decisione |
| --- | --- | --- |
| Ruoli/backend | Nuova configurazione esplicita D9; documenti dei servizi con hash; autorizzazione sui byte della configurazione | require_execution; producer runner; Provider/server_contract; binding immutabile e riserva ledger |
| Libreria principale/alternativa | Otto richieste producer per stadio, raw SQLite, handoff R4 | _insights: libreria completa del ciclo selezionato, rimediation prevale sul principale; nessun mix |
| Tokenizzazione | Pin R4 canonico separato dal tokenizer/template del servizio | producer, prepare_gate, load_prepared: cap R4 e conteggio chat completo distinti |
| Generazione | Parametri espliciti coperti dalla configurazione; niente eredità dal preflight sospeso | Payload 122B senza temperature; seed/thinking omessi se non configurati; limiti completi prima dell'invio |
| Ordine label | Inventario canonico e approvazione distinta per ordine 1a | Preparazione/autenticazione prompt; 03.7 immutabile, fixture non sono approvazione |
| Quote/storia | Un ledger identificato, contatori durevoli; stato riconciliazione esterna coperto da autorizzazione | Nessun reset/migrazione/backfill. Riserva D04 in transazione, tutti i contributori; limiti invariati |
| Alternativo nel pilot | Scelta esplicita ancora mancante, distinta dai ruoli | Nessuna scelta implicita: pending blocca; valore futuro pilot richiede conformità completa prima sonda; deferred non abilita un nuovo stadio post-gate |
| CLI/preparazione | Selezione esplicita --config, nuova configurazione pending separata | Default storico resta bloccato; piano offline senza rete; nessun client prima delle barriere |
| Swap | Autenticazione separata della libreria alternativa e della principale | Sostituzione della sola libreria, conservando casi/label/consumer; nessun runner scientifico finale autorizzato |

## Contratto del delta

1. Gli ingressi scientifici esigono il blocco D9 oltre all'approvazione esatta già
   prevista. I vecchi config anche promossi nominalmente ad APPROVED non bastano.
   Nessun percorso alternativo automatico. Il ledger generico offline resta riusabile
   per le regressioni storiche; i binding dei runner D9 conservano l'intera configurazione
   approvata e il ruolo, ricontrollati in transazione nel riuso e nelle riserve.
2. I servizi 122B e 27B hanno alias/identità/pin/configurazioni espliciti e documentazione
   improntata. Metadati documentati non significano servizio qualificato. Campi mancanti,
   placeholder, ordine non approvato o riconciliazione pendente impediscono i futuri invii.
   Le prove zero-token mantengono il proprio contratto D03: nessun metadato generale le sostituisce.
3. Identità canonica nominale distinta dall'alias; P e C condividono lo stesso servizio 122B.
   Provider producer scelto per hash e stadio, non da una lista libera. Alternativo solo 27B.
4. Il campo temperature 122B è vietato nella configurazione di generazione e assente dai
   kwargs finali; 0.6 rimane dichiarazione del servizio, non valore da inviare.
5. R4 usa i pin canonici 27B senza special token; la chat usa i pin del servizio attivo.
   Verificare entrambi prima della produzione e del riuso; nessuna libreria prerequisito
   della conformità che deve crearla. Capienza controllata anche sul massimo output attestato.
6. Si può autenticare una libreria alternativa completa dopo il suo PASS, senza attivare
   consumer 27B. Lo swap conserva tutti i casi e sostituisce soltanto la libreria; i casi
   dello studio definitivo e le relative esecuzioni restano nei mandati successivi.
7. Collocazione alternativa PENDING impedisce l'esecuzione. La scelta futura pilot/deferred
   deve essere esplicita e coperta dall'autorizzazione; deferred vieta alternate_conformity
   nel pilot. Il nuovo percorso differito dopo pilot non viene inventato in questo delta.
8. Riconciliazione del consumo S (4 richieste riportate, 3 inferenze completate) resta esterna
   e bloccante. Nessuna riga di consumo viene creata o azzerata da questo delta. Si richiede
   un record revisionato che leghi pilot/ledger e inventario della storia precedente;
   dichiarazioni generiche o contatore iniziale zero non bastano.

## Test discriminanti e controlli positivi

Prima del runtime: nuove prove sul tecnico esatto aae29a9, registrando anche eventuali
API mancanti separatamente dai fallimenti comportamentali. Stessi byte finali sul delta.

- Config APPROVED priva di D9: rifiuto prima client/server; positivo completo su fixture.
- Ruoli scambiati, fallback, servizio consumer 27B, provider principale/alternativo
  invertito, metadati o riconciliazione mancanti: rifiuto senza nuovi intenti/invii.
- Temperature null/0/0.6/stringa: rifiuto 122B; positivo payload con campo assente.
- Conteggi R4/chat deliberatamente differenti: cap canonico non sostituibile dal servizio.
- Alt pending/deferred/pilot e necessità PASS nel pilot: controlli distinti;
  libreria alternativa completa autenticata, principali e casi preservati nello swap.
- Config persistita o fonte alterata dopo binding, prima/dopo restart: rifiuto prima
  riserva/trasporto; positivi resume senza nuovi invii.
- Contabilità per ruolo/modello: ogni intento una volta; P+C aggregati, P_alt separato,
  nessuna nuova quota, nessuna riscrittura della storia.

Eseguire regressioni interessate e suite mirata/discovery complete sul candidato finale.
Gli adattamenti necessari delle fixture storiche al nuovo prerequisito saranno dichiarati;
assertion di D01–D04 non indebolite. Guardiano prima/dopo con identificativi, sempre NON PASS
storico. Nessuna qualifica reale, OK indipendente, GO, pubblicazione o freeze.
