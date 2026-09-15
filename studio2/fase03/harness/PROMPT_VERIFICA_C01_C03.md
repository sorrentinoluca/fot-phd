# Verifica indipendente delle correzioni C01–C03 — harness 03.10

Eseguire in una **finestra distinta dalla preparatrice**, preferibilmente con altro modello.
Questo è un incarico di review in sola lettura, non di correzione. Leggere
`docs/MAINTENANCE.md` e i prompt pertinenti. Nessun commit/tag/push/merge/freeze/GO,
provider/API/inferenza/simulazione. Sono previste esclusivamente prove offline con stub.

## Identità da verificare prima di eseguire

- Sorgente consegna locale: `/Users/luker/fot-tep-harness-0310-c01-c03`.
- **Candidato tecnico `9e18bcbd06fa2c54202c8eeda079c112dbfcefcd`**.
- **Tree `5d1fd7924c4e1e46346f367590e6aa1977a6ba75`**.
- Base documentale `6268437b8b64288b50ad5f7c924e1fcab85b27d3`; acquisizione `b882c27103dbd9d0e0462df20731123f5ed5a0c1`.
- Branch `codex/studio2-harness-0310-c01-c03`; main remoto effettivo
  `https://github.com/sorrentinoluca/fot-phd.git` osservato a `a00605862f627710347bd63c49f79a6d0a00135f`.
- Manifest tecnico `studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json`:
  SHA-256 `e0b6fc2ba4752b485829b397867b5ae5ee1a7ec5356ea4d11f24e09f39b2f228`, 14155 byte, 54 file.

L'HEAD della sorgente sarà un successore **documentale** con questo prompt/report/consegna/audit:
non eseguirlo al posto del candidato tecnico. Verificare la differenza e usare un clone/worktree
isolato, detached al candidato tecnico, con output in una directory sibling `evidence/`.
Preservare sorgente, copia principale, entrambe le review precedenti e lavori paralleli.
Verificare il remoto GitHub effettivo, non dedurre main dall'origin di un clone locale.

Leggere integralmente il report corrente `REPORT_CORREZIONI_C01_C03.md` e il secondo NON OK
acquisito `non_ok_0c8157f_20260915/evidence/VERIFICA_CORREZIONI_HARNESS_03_10.md`.
SHA-256 verbale `1785fb3cfb832b5a299fe885ac740a4f557ad83431e002451d447afab64f4efc`;
SHA-256 manifest originale `e5cb1589a9f8006303c9ea91a3ea37be742990c2ac6c86fb8ffc7e59fcbf7f80`.
Verificare inventari, copie ed esterni prima dell'uso. Gli script acquisiti e le fixture
forensi non si eseguono in-place; costruire nuove copie sacrificabili. Le fixture false
non sono sorgenti scientifiche né autorizzazioni reali.

## Verifiche centrali, da fonti e ingressi reali

1. **C01 / R04:** conformità alternativa definita, INTENT, FAILED, ZERO_TOKEN_PROVEN,
   completata senza outcome o chiusa FAIL deve bloccare la sonda prima di ogni invio;
   verificare CLI, restart, binding sonda antecedente e gara tra processi. PASS alternativo
   deve consentire il percorso. Controllare anche riserva/esito gate, non solo bind_stage.
2. **C02 / R07 / N48:** il piano rev.10 (fonte acquisita, righe 831/871–875) richiede
   invalidità di trasporto nel denominatore. Un timeout gate deve produrre INVALID durevole
   senza raw/fingerprint/token inventati, continuare fino a 120 primi tentativi e dare
   119/120 + R3 con gli altri 119 validi. Tre invalidi sullo stesso prompt devono impedire
   T6 valutabile; sette distribuiti devono fallire T3. Nessun retry gate.
3. Verificare l'atomicità FAILED+evento, crash prima/dopo commit e dopo raw; secondo processo
   deve continuare senza reinviare tentativi registrati. INTENT senza osservazione resta
   bloccato fino a prova zero-token esplicita/approvata; poi entra come INVALID senza retry.
   La prova successiva a un INVALID non lo cancella. Un raw con identità errata sospende;
   la nuova eccezione per assenza di risposta non deve mascherarlo. Provare manipolazioni.
4. **C03 / R07:** dopo timeout e retry producer, confrontare stub, ledger, summary e outcome:
   9 richieste provider, 8 coppie valutabili T9, 16 insight. Ripetere per alternativo e dopo
   restart/file summary assente. Non confondere consumo cumulativo dello stadio con invii
   del singolo processo o con prova di ricezione remota in caso di crash incerto.
5. Controllare R01–R10 con la matrice corrente e i 50 metodi nominativi acquisiti. Gli
   adattamenti pregressi restano documentati. N48 precedente era non equivalente; valutarne
   ora il collegamento effettivo all'evaluatore, senza fermarsi al contatore FAILED.

## Prove da riprodurre e conteggi dichiarati

Usare `/opt/anaconda3/bin/python3` (3.13.9/SQLite 3.51.0), o runtime compatibile verificato;
`PYTHONDONTWRITEBYTECODE=1`, cwd candidato per suite e subprocess. Comandi in
`c01_c03_evidence/COMANDI.md`; reference 03.6 locale:
`/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference`.

- Suite mirata: 96/96; discovery: 131/131; nuove regressioni: 14; metriche qualificate: 9
  già incluse, tre file byte-identici.
- Originali applicabili: 14/14 (12 invariati, 2 con i precedenti adattamenti di fixture).
- X01–X18 letterali: 18/18; X19–22/X24: 5/5. X23 letterale conserva **una failure** perché
  si aspettava l'interruzione difettosa del gate. Nuovo X23: 1/1 con 120 INVALID, T3/T6 e
  nessun reinvio. Leggere `x23_adapted/ADATTAMENTO.md`, confrontare byte originali/adattati;
  non accettare l'adattamento per fiducia nel report.
- Consolidamento: 24 metodi distinti, 23 letterali + 1 adattato dalla preparatrice;
  non 24/24 del file originale immutato. Sul candidato respinto: 4 failure/24, tre difetti.
- Primo discovery parziale conservato per un errore di import dei nuovi test; il finale
  completo con import assoluti è 131/131. Non contarlo come failure del servizio o fonte.
- Guardiano documentale: 35, **14 ID storici falliti invariati**, 1 skip; non PASS.

Verificare manifest 54 file, SHA256SUMS nuove prove e inventari: copie vs esterni
recuperabili, dimensioni/hash, metadati di provenienza. Confrontare perimetro Git completo
con la base documentale, acquisizione separata e 59 file del commit tecnico. Report e
prompt correnti non sono inclusi nel manifest tecnico per evitare autoreferenza.

D9 già approvata (122B principale producer/consumer, 27B alternativo completo, Terra
storico). Il suo recepimento eseguibile, l'ordine label reale e le qualifiche servizio/T5
restano separati. Nessuna riapertura delle scelte D9 né promozione del preflight storico.
Non modificare piano/statistica, APERTURA, walkthrough, raccordo metriche o freeze 03.7/03.9/03.12.

## Consegna della review

Scrivere un verbale con esito **OK oppure NON OK limitato al candidato offline esatto**,
rilievi motivati e riproduzioni, matrice dei metodi/adattamenti, manifest SHA-256 e stato
Git finale. Distinguere errore di dipendenza, errore del test e difetto candidato. Indicare
modello e finestra osservati, distinguendoli dal modello richiesto; l'acquisizione precedente
attesta stesso modello gpt-6-astra con effort high/xhigh in finestre diverse. Non assumere
indipendenza di modello da quella delle finestre. Nessuna correzione in questa review.
