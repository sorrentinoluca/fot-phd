# Consegna per la futura pubblicazione autorizzata — 03.8

Data: 2026-09-15. Stato: **proposta locale, pubblicazione non eseguita**.
03.8 resta in finalizzazione locale e la Fase 03 resta aperta.

## Identità osservate

- Remoto effettivo: `https://github.com/sorrentinoluca/fot-phd.git`.
- `refs/heads/main` remoto osservato dopo l'acquisizione:
  `a00605862f627710347bd63c49f79a6d0a00135f`.
- Branch sorgente: `codex/studio2-finalizzazione-038`.
- Candidato normativo verificato:
  `4c9e7a1f1d8bd07b7d6be8df724f743986717da8`, tree
  `03b215980ae170db2e1284dd7bd5eb07b830fb28`.
- Successore con consegna e prompt, non coperto dall'OK:
  `03a7d7609faad06f2e6f2a6d39fd007268a99cde`.
- Acquisizione dell'OK e **punta locale proposta per la pubblicazione**:
  `8dbd2b49176c16f9e100e5f181c729b99d406a35`, tree
  `d1d2a0bb3b5247190340a9d091452e55099d6a18`.
- Genitore della punta proposta:
  `03a7d7609faad06f2e6f2a6d39fd007268a99cde`.

Il presente file è un successore documentale della punta proposta e **non** fa
parte del contenuto da pubblicare in questa operazione. Il suo commit non deve
essere usato in luogo di `8dbd2b4` senza una nuova ricognizione esplicita.

## Catena e contenuto destinati all'integrazione

La pubblicazione proposta è un fast-forward di `refs/heads/main` da `a006058`
a `8dbd2b4`. La catena è lineare, 23 commit avanti e 0 indietro:

1. 20 commit 03.8 da `945cb1f` a `6490af4`, enumerati con genitori completi in
   `MANIFEST_CANDIDATO_FREEZE_03_8.json`;
2. `4c9e7a1`: otto file del candidato di finalizzazione verificato;
3. `03a7d76`: consegna e prompt operativi, esplicitamente esclusi dall'OK;
4. `8dbd2b4`: verbale OK byte-identico e record di acquisizione.

Il diff effettivo `a006058..8dbd2b4` contiene **79 file**: 75 aggiunti e 4
modificati, per 18.427 inserimenti e 181 rimozioni. I quattro file preesistenti
modificati sono esclusivamente:

- `docs/fot_walkthrough_conversazione_studio2.md`;
- `docs/fot_walkthrough_conversazione_studio2.html`;
- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`;
- `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`.

I 75 file aggiunti sono i tre record sorgente D9 e il pacchetto tracciato
`studio2/fase03/piano_statistico/`: piano rev.10, decisioni, budget, manifest
storici e candidato, report, controlli, verbali OK/NON OK, acquisizioni,
consegne, prompt e codice/test di risoluzione statistica già compresi nella
catena verificata. Non sono inclusi runtime harness D9, configurazioni di
servizio, `paper_sections/`, risultati sperimentali o file sottoscritti.

## Prove acquisite

- Verbale `VERIFICA_FINALIZZAZIONE_03_8.md`: **11.988 byte**, SHA-256 calcolato
  all'acquisizione
  `03cb06132ce10c80ff866d9cf18d5a812237a63da5b84cee9734d22e52a7a763`.
  Non era disponibile nel mandato una precedente impronta attestata dal
  revisore; il record non la inventa.
- Record `ACQUISIZIONE_OK_FINALIZZAZIONE_03_8.md`: **5.072 byte**, SHA-256
  `6268c7bdec58e97bed460fa61f52016c603c7a61330794f103bddfce06f06935`.
- Manifest candidato: **12.382 byte**, SHA-256
  `bcc9ef183190e2fd0997b2e600fc53498e4a6194993e997820255a4b6d124dc6`;
  conserva `freeze_effective=false`.
- Manifest storico: **25.894 byte**, SHA-256
  `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`,
  byte-identico.

L'OK riguarda soltanto `6490af4..4c9e7a1` e gli otto file del candidato. Non si
estende a `03a7d76`, al verbale, all'acquisizione o a questa consegna. Questi
successori sono documenti operativi e di provenienza; non cambiano regole
scientifiche o contenuto del candidato. Non è quindi necessario un nuovo audit
normativo prima della pubblicazione proposta. Qualunque modifica ulteriore ai
documenti del candidato o risoluzione di conflitto produrrebbe invece nuovi byte
da sottoporre a review circoscritta.

## Procedura proposta, da eseguire solo dopo autorizzazione

La futura finestra di pubblicazione deve operare con un solo writer e senza
usare il `main` locale arretrato come fonte:

1. ricontrollare worktree, branch, stato e attività concorrenti;
2. eseguire `git fetch origin main` e verificare che
   `refs/remotes/origin/main` e `git ls-remote origin refs/heads/main`
   coincidano ancora con `a00605862f627710347bd63c49f79a6d0a00135f`;
3. verificare che `origin/main` sia antenato di `8dbd2b4`, che la divergenza sia
   23/0, che `git diff --check origin/main..8dbd2b4` sia pulito e che il tree
   proposto sia `d1d2a0bb3b5247190340a9d091452e55099d6a18`;
4. soltanto con autorizzazione esplicita, pubblicare il fast-forward con un
   refspec diretto equivalente a
   `git push origin 8dbd2b49176c16f9e100e5f181c729b99d406a35:refs/heads/main`;
5. verificare con `git ls-remote origin refs/heads/main` che il ref remoto sia
   esattamente `8dbd2b4` e che candidato, verbale e acquisizione siano
   raggiungibili dalla nuova `origin/main`.

Se il main remoto è avanzato, **non eseguire il push** e non riscrivere la
storia 03.8. Preparare un ramo di integrazione dalla nuova `origin/main`,
integrare la punta `8dbd2b4`, confrontare i file condivisi correnti e sottoporre
a review ogni conflitto risolto o nuovo delta risultante. Solo la nuova punta
verificata potrà diventare target di pubblicazione.

## Sequenza successiva per manifest e freeze

Dopo la pubblicazione verificata di `8dbd2b4`, o della futura punta sostitutiva
se il remoto sarà avanzato:

1. preparare un **nuovo manifest finale pre-tag** senza modificare
   `PIANO_STATISTICO_FREEZE.json` né
   `MANIFEST_CANDIDATO_FREEZE_03_8.json`; registrare il commit pubblicato e le
   prove acquisite, mantenendo lo stato non efficace prima del tag e senza
   includere l'hash del manifest in se stesso;
2. creare un commit candidato esatto per quel solo delta, con report e prompt,
   e farlo verificare indipendentemente;
3. acquisire il nuovo verbale in un successore documentale e pubblicare la
   catena autorizzata;
4. solo allora identificare come target del tag la punta pubblicata che contiene
   manifest, review e acquisizione; il target non è determinabile oggi e non è
   anticipato in questo record;
5. creare e pubblicare, con mandato separato, il tag annotato
   `studio2-fase03-piano-statistico-frozen-001`;
6. verificare sul remoto sia l'oggetto del tag sia
   `refs/tags/studio2-fase03-piano-statistico-frozen-001^{}` e controllare che
   il peeled coincida con il target allora stabilito;
7. produrre un record successore di efficacia che riporti commit pubblicato,
   oggetto tag e peeled reali. Se tale record o manifest dichiara
   `effective=true`, deve nascere **dopo** il tag e ricevere la verifica prevista
   prima di dichiarare conclusa 03.8.

Il prompt della review del manifest finale non viene creato ora: senza il nuovo
file, la sua base, il commit candidato e le impronte reali sarebbe un prompt con
identità inventate. Dovrà essere autonomo e limitato al delta esatto quando
questi oggetti esisteranno.

## Residui

- autorizzazione esplicita alla pubblicazione del fast-forward proposto;
- ricontrollo live del main remoto immediatamente prima del push;
- manifest finale pre-tag, sua review e acquisizione;
- pubblicazione di quella catena, tag annotato e verifica remota oggetto/peeled;
- record successore di efficacia e relativo controllo.

A resta approvata con conteggio completo e `1,20 × T ≤ W`; 3.700 è storico.
Bibliografia e relativa acquisizione/pubblicazione sono concluse e non vanno
ripetute. Firma materiale non richiesta. Harness D9 eseguibile, ordine label,
servizi, T5, 03.11, pilot e run restano filoni separati e non sono importati.

Nessun push, merge su `main`, tag, pubblicazione, firma, invio, chiamata,
inferenza, simulazione o pilot è stato eseguito da questa preparazione.
