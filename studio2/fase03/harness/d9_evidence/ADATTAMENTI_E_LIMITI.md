# Adattamenti dichiarati D9 e limiti

Le sorgenti e le assertion storiche restano recuperabili byte-identiche nella base
`5886c6f`; tutti i verbali/acquisizioni e pending certificati rimangono nel worktree.

- `test_revisions.RunnerRevisions`: fixture esplicite D9 (metadati di due servizi,
  hash provider per ruolo, scelta deferred), modello stub ricavato dall'alias richiesto.
  Solo nel supporto test `d9_offline_fixtures` si sostituiscono i pin tokenizer reali
  e la fonte di consumo storico con file sintetici e una storia vuota fittizia.
  La produzione richiede sempre il riferimento S con 4 richieste/3 inferenze.
  Non è una nuova approvazione o qualifica; i controlli e le assertion dei runner
  rimangono operanti. Il provider alternativo della fixture è ora distinto.
- C01 runner alternativo: scelta `pilot` esplicita prima del primo binding. Il test
  conserva errore del primo tentativo, rifiuto sonda, riconciliazione e retry autorizzato.
  Il vecchio ingresso implicito con provider principale non rappresenta più D9.
- D01 legacy runner/CLI: configurazioni generate col codice esatto 0c8157f sono prive
  di D9; nuovo rifiuto preventivo D9 prima della vecchia diagnostica sull'alternativo.
  Il precedente positivo di rematerializzazione scientifica richiede ora la nuova
  autorizzazione: è trasformato in rifiuto con contatori/DB intatti e file non ricreato.
  Le prove di replay sul ledger v2 generico rimangono invariate e mantengono il loro
  positivo. Nessun backfill sui ledger legacy. Questa variazione è una barriera
  del nuovo contratto, non un rilievo che riapre D01.
- D02 runner: scelta `pilot` esplicita prima del binding, per raggiungere la
  corruzione del predecessore alternativo già prevista. Assertion D02 invariate.
  Sorgenti D03/D04 non modificate. Usano la fixture runner D9
  quando serve raggiungere le stesse barriere storiche; i loro test generici sono
  invariati. Non si dichiara l'intera suite come esecuzione letterale delle fixture D04.

Le prove iniziali (`test_first_red.log`) distinguono un fallimento comportamentale
(config APPROVED senza D9 accettato dall'antecedente) da tre API assenti. Il file
finale aggiunge altre prove; viene rieseguito per intero sullo stesso tecnico
`aae29a9`, non sul successore documentale. Le nuove API mancanti sono errori di
assenza funzionalità nell'antecedente, non regressioni D04 o assertion rosse autonome.

Il primo tentativo con Python di sistema incontra un'ABI x86_64/arm64 incompatibile
in rpds/jsonschema: log conservato. Le prove finali usano Python Anaconda 3.13.9.
La prima suite intermedia è stata interrotta dopo il rilievo della fixture C01
implicita; il suo output parziale non entra nei totali finali. Gli altri log
intermedi preservano anche un NameError corretto nel nuovo percorso Provider.

`server_contract` nel percorso D9 restituisce soltanto provenienza documentata,
marcata DOCUMENTED_NOT_LIVE_VERIFIED. Non interroga /version, /openapi o PID locali
per presumere il contratto del servizio remoto API-only. Il digest documentale
non è chiamato fingerprint del processo. Identità della risposta e raw restano
controllati/persistiti per ogni futura richiesta; una corrispondenza API non prova
crittograficamente i pesi. La compatibilità reale di schema, parser, thinking e
limiti richiede la futura qualificazione nei soli stadi autorizzati.

La collocazione alternativa resta PENDING nel config consegnato. Il codice testa
entrambi i valori futuri espliciti: pilot richiede il PASS alternativo prima della
sonda; deferred non consente alternate_conformity nel pilot. Non implementa un
nuovo stadio post-gate o una spesa in G_A: quel percorso resta da specificare dopo
la decisione. La helper swap conserva i casi forniti e autentica due librerie
complete; non seleziona P1 né avvia lo studio definitivo.

La prima suite mirata completa ha eseguito 145 test con un errore nella
fixture D02: la conformità alternativa richiedeva la scelta pilot esplicita.
Il log `intermediate_targeted_145.log` conserva questo esito; il successivo
run finale include la correzione della sola predisposizione della fixture.
