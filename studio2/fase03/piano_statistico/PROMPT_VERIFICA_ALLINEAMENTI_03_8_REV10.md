# Prompt per la verifica indipendente del candidato di allineamento 03.8 rev.10

## Configurazione raccomandata

- Modello: **`gpt-6-astra`**.
- Reasoning: **`max`**.
- Esecuzione: nuova task, nuovo contesto e copia Git isolata; nessun agente o
  sessione che abbia preparato il candidato può svolgere la review.

## Incarico

Svolgi una verifica indipendente, in sola lettura, del candidato di allineamento
normativo per la sottofase 03.8 dello Studio 2 FoT-TEP.

Oggetto esatto:

- repository sorgente `/Users/luker/fot-tep-piano-statistico-fix` o una sua
  copia/worktree isolata (il candidato è già disponibile nel worktree
  `/Users/luker/fot-tep-piano-statistico-chiusura`);
- candidato `4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8`;
- tree `1eb1d7df58e55a546931711f0a1cf9d800e02e3e`;
- baseline immediata del delta `70c84e3a573951171813add26a46167cbc6c7203`;
- base `origin/main` osservata alla preparazione:
  `a00605862f627710347bd63c49f79a6d0a00135f`;
- candidato statistico rev.10 originario:
  `6aaa5b3eebfed4ba502c25c0443caabd0051af21`;
- consegna/verifica rev.10 originaria:
  `51782e8c40069c0a2310afafc36907a61d517ff6`.

Prima di leggere il merito, verifica branch/HEAD, pulizia della copia, oggetti Git
e tree. Non correggere alcun file. Non firmare, non creare commit o tag, non
eseguire push, simulazioni, pilot, chiamate API o run finali.

## File da leggere

1. `docs/MAINTENANCE.md` e i prompt `Verifica_LLM.md`, `Fase_LLM.md`,
   `Documentazione_LLM.md`, `Commit_LLM.md`;
2. `studio2/fase03/piano_statistico/CONSEGNA_REV10.md`;
3. piano, manifest, verbale rev.10, atto non firmato,
   `BUDGET_RISORSE_REV10.md`, `COORDINAMENTO_CHIUSURA_03_8.md` e
   `DELTA_HARNESS_03_10.md`;
4. `MANIFEST_ALLINEAMENTI_03_8_REV10.json`,
   `MATRICE_RESIDUI_CHIUSURA_03_8_REV10.md`,
   `ISTRUZIONI_FIRMA_MATERIALE_REV10.md`,
   `CONSEGNA_TECNICA_03_10_DA_REV10.md` e
   `REPORT_ALLINEAMENTI_03_8_REV10.md`;
5. il diff completo
   `70c84e3a573951171813add26a46167cbc6c7203..4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8`;
6. le pubblicazioni correnti 03.9 e 03.12 e la consegna bibliografica già in
   `main`.

## Verifiche obbligatorie

### A. Perimetro e preservazione

- Il delta candidato modifica esattamente due file esistenti e aggiunge cinque
  documenti/manifest di coordinamento; nessun preflight, harness, codice, test,
  dato o coppia walkthrough MD/HTML.
- Piano rev.10, manifest rev.10, report rev.10, verbale rev.10, atto non firmato,
  budget e delta 03.10 coincidono byte per byte con i blob della consegna
  `51782e8` e con le impronte dichiarate.
- Tutte le 19 voci `files` e le 6 `inputs_read` del manifest rev.10 risolvono e
  coincidono. Verifica anche i nove prerequisiti storici acquisiti in `70c84e3`.
- Il manifest del presente delta è JSON valido, non autoreferenziale e le sue
  6/6 voci coincidono per byte e SHA-256.

### B. Stato pubblicato e residui reali

- Conferma con la storia Git e, se disponibile, `git ls-remote` in sola lettura:
  `origin/main` alla base, tag/peeled di 03.9 e 03.12 e raggiungibilità delle
  pubblicazioni.
- Ricalcola 23/23 impronte dell'inventario bibliografico; verifica il verbale
  `551f7da9…ddaf` e l'addendum `f2c29416…0b8e`. La bibliografia non deve restare
  classificata pending.
- Conferma che 03.5, 03.9 e 03.12 siano distinte da 03.8 e che 03.8/Fase 03 non
  siano dichiarate chiuse.

### C. Merito degli allineamenti

- Nel piano generale e in APERTURA risultano correnti: D2=8; 64 fault +8 Normal
  primari; 6 OOD; 11 scorte; F6/F4 condizionati; D11; m=0,125; alpha e gerarchia;
  politica R approvata; nessuna riapertura di FAR, U3 o A/B.
- Ricalcola 1.728/5.184, 224/672, 148/444, 144/432 e 2.244/6.732.
  Verifica la formula completa, +702/+24,6% e +638 storici, e che 3.700 sia
  soltanto storico. Nessun totale esemplificativo deve diventare budget vigente.
- Verifica la catena: conformità → eventuale remediation autorizzata → sonda
  3/6/9 → gate 40×3; T3, T4, T6, T9, T11; riserva `8r+t≤15`, massimi
  152/160 e hard stop 200.
- Conferma che producer, consumer e alternativo restino ruoli non assegnati e
  che tutti i punti dipendenti da D9 siano separati da quelli completabili ora.
- Conferma l'assenza di ciclo: il freeze 03.8 fissa candidati/criteri/catene;
  03.11 esegue dopo il freeze i controlli tecnici OOD e prima delle chiamate sui
  test. Il completamento di 03.11 non è richiesto prima del tag 03.8.
- L'atto non firmato deve legare correttamente il piano a
  `675dbbcc…032a`; le istruzioni devono richiedere luogo/data/firma reali e una
  copia separata, senza trasformare approvazioni precedenti in firma.
- La matrice deve distinguere i veri bloccanti del tag dalle condizioni future
  di esecuzione. D9/T5/03.10/03.11 non vanno eliminati, ma non vanno usati per
  reintrodurre una dipendenza circolare nel freeze statistico.

### D. Controlli documentali

- `git diff --check` sul delta candidato;
- risoluzione dei link locali nei file modificati/nuovi;
- guardiano `python3 docs/test_explanation.py`: registra conteggio, skip,
  identificativi e subtest; confronta con la baseline 35 test / 14 fallimenti /
  1 skip, con ripartizione 1/1/9/3 dichiarata nel report;
- verifica che nessuna coppia MD/HTML sia stata modificata. Non richiedere la
  parità del walkthrough prima della review: è deliberatamente il passo
  documentale successivo all'OK.

## Verdetto e uscita

Prima riga del verbale: `OK` oppure `NON OK`.

Scrivi soltanto
`studio2/fase03/piano_statistico/VERIFICA_ALLINEAMENTI_03_8_REV10.md` nella
copia isolata, lasciandolo non tracciato. Registra modello, reasoning, data,
task/sessione, worktree, commit/tree, comandi e risultati. Un `OK` qualifica
esclusivamente il candidato `4503cb6`; non costituisce firma, pubblicazione,
freeze, chiusura o autorizzazione sperimentale. Se trovi un difetto, indica file,
righe, prova primaria e correzione minima; ogni correzione richiederà un nuovo
candidato e una nuova review.
