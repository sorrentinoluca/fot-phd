# Esito della pubblicazione autorizzata — 03.8

Data e ora della verifica: 2026-09-15 18:25:40 +0200.

## Esito

La pubblicazione autorizzata è stata completata con aggiornamento non forzato
di `refs/heads/main` sul remoto effettivo
`https://github.com/sorrentinoluca/fot-phd.git`.

- `main` remoto prima dell'operazione:
  `a00605862f627710347bd63c49f79a6d0a00135f`;
- commit pubblicato e `main` remoto verificato dopo l'operazione:
  `8dbd2b49176c16f9e100e5f181c729b99d406a35`;
- tree del commit pubblicato:
  `d1d2a0bb3b5247190340a9d091452e55099d6a18`;
- refspec utilizzato:
  `8dbd2b49176c16f9e100e5f181c729b99d406a35:refs/heads/main`;
- esito Git: fast-forward `a006058..8dbd2b4`, senza opzioni di forza.

Il confronto eseguito immediatamente prima del push ha confermato che il
valore live di `refs/heads/main` coincideva ancora con la base autorizzata. Il
delta pubblicato comprende 23 commit, 79 file modificati (75 aggiunti e 4
modificati), 18.427 inserimenti e 181 rimozioni; `git diff --check` era pulito.

## Verifica remota

Dopo il push sono stati verificati separatamente il riferimento live con
`git ls-remote` e il tracking ref dopo un nuovo fetch. Entrambi coincidevano
con `8dbd2b49176c16f9e100e5f181c729b99d406a35`.

Sono raggiungibili dal nuovo `origin/main`:

- la base precedente `a00605862f627710347bd63c49f79a6d0a00135f`;
- la base di finalizzazione `6490af4889fd679d491f63b9debdf2314eaf7aca`;
- il candidato verificato `4c9e7a1f1d8bd07b7d6be8df724f743986717da8`;
- il successore documentale `03a7d7609faad06f2e6f2a6d39fd007268a99cde`;
- l'acquisizione pubblicata `8dbd2b49176c16f9e100e5f181c729b99d406a35`.

Il successore locale
`39a3e577e6e0eba32ad925347be9606d846b2c64`, che contiene la consegna
preparatoria, **non è raggiungibile** dal `main` remoto ed è quindi rimasto
escluso come richiesto. Anche il presente record è un successore locale e non
fa parte del commit pubblicato.

## Artefatti di provenienza inclusi

- `VERIFICA_FINALIZZAZIONE_03_8.md`: 11.988 byte, SHA-256 calcolato
  all'acquisizione
  `03cb06132ce10c80ff866d9cf18d5a812237a63da5b84cee9734d22e52a7a763`;
- `ACQUISIZIONE_OK_FINALIZZAZIONE_03_8.md`: 5.072 byte, SHA-256
  `6268c7bdec58e97bed460fa61f52016c603c7a61330794f103bddfce06f06935`;
- `MANIFEST_CANDIDATO_FREEZE_03_8.json`: 12.382 byte, SHA-256
  `bcc9ef183190e2fd0997b2e600fc53498e4a6194993e997820255a4b6d124dc6`,
  con `freeze_effective=false`.

## Stato successivo

Questa operazione ha pubblicato il solo commit autorizzato. Non sono stati
pubblicati altri commit e non sono stati creati o pubblicati tag. In
particolare, non è stato creato il tag pianificato
`studio2-fase03-piano-statistico-frozen-001`.

La sottofase 03.8 resta priva di freeze. Il passo successivo, soggetto a mandato
separato, è preparare il manifest finale pre-tag, sottoporlo alla review
pertinente, acquisirne l'esito e soltanto in seguito determinare e autorizzare
il target del tag annotato con verifica remota dell'oggetto e del peeled.
