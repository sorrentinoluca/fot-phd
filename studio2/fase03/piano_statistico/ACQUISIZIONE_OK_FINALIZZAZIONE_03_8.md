# Acquisizione dell'OK indipendente — finalizzazione 03.8

Data acquisizione: 2026-09-15T18:06:34+02:00.

Il verbale indipendente già presente nella sede preparatrice è acquisito senza
copiarlo, normalizzarlo o modificarlo. Questo record ne documenta provenienza,
identità e portata; non estende il verdetto.

## Artefatto acquisito

- Percorso:
  `studio2/fase03/piano_statistico/VERIFICA_FINALIZZAZIONE_03_8.md`.
- Dimensione osservata prima della scrittura del presente record: **11.988
  byte**.
- SHA-256 calcolato prima della scrittura del presente record:
  `03cb06132ce10c80ff866d9cf18d5a812237a63da5b84cee9734d22e52a7a763`.
- Stato iniziale: unico file non tracciato nel worktree preparatore a HEAD
  `03a7d7609faad06f2e6f2a6d39fd007268a99cde`.
- Sede sorgente e destinazione: coincidono; non è stata creata una copia
  duplicata.

Il verbale rinvia a una nota di consegna della sessione per dimensione e
impronta, ma né il suo corpo né il mandato di acquisizione forniscono il valore
di una precedente impronta attestata. Di conseguenza il digest sopra è
**calcolato ora dalla finestra acquisitrice**, non presentato come certificato
pregresso del revisore. Dimensione e SHA-256 vengono ricontrollati dopo staging
e commit; l'identità byte per byte è provata dall'invarianza dei byte nella
stessa sede, non da un confronto con una seconda copia.

## Provenienza e identità della review

Il verbale dichiara:

- natura: review read-only e indipendente;
- data: 2026-09-15;
- base: `6490af4889fd679d491f63b9debdf2314eaf7aca`;
- candidato: `4c9e7a1f1d8bd07b7d6be8df724f743986717da8`;
- tree: `03b215980ae170db2e1284dd7bd5eb07b830fb28`;
- perimetro: gli otto file del delta `6490af4..4c9e7a1`;
- esito: **OK**, senza rilievi bloccanti;
- metodo dichiarato: lettura degli oggetti Git e guardiano su archivi completi
  dei due commit in directory isolate.

Il verbale non identifica nome o sessione del revisore, modello, provider,
backend o livello di reasoning. Questi dati sono pertanto **non attestati** e
non vengono inferiti dalla finestra acquisitrice.

Il commit candidato è presente, ha il tree e il solo genitore dichiarati e il
diff contiene esattamente i sei file modificati e due aggiunti elencati nel
verbale. Il successore `03a7d7609faad06f2e6f2a6d39fd007268a99cde`, che aggiunge
`CONSEGNA_FINALIZZAZIONE_03_8.md` e
`PROMPT_VERIFICA_FINALIZZAZIONE_03_8.md`, è esplicitamente escluso dall'OK.

## Portata del verdetto

L'OK certifica soltanto i byte del commit `4c9e7a1`, tree `03b2159`, contro
`6490af4`. Non certifica:

- il successore documentale `03a7d76`;
- il verbale stesso o il presente record di acquisizione;
- futuri delta di integrazione o manifest;
- una futura pubblicazione, un tag o il relativo peeled;
- harness D9 eseguibile, servizi, configurazioni, ordine label 1a, T5, pilot,
  inferenze, simulazioni o run finali.

03.8 resta in finalizzazione locale e la Fase 03 resta aperta.

## Significato operativo delle due osservazioni non bloccanti

1. **Regola A già vigente.** `APPROVAZIONE_ADDENDUM_03_8.md` registra A
   approvata senza modifiche. Vale il conteggio completo per blocco/modello e la
   fattibilità temporale misurata `1,20 × T ≤ W`; 3.700 è soltanto un tetto
   storico. La formulazione condizionale in
   `COORDINAMENTO_CHIUSURA_03_8.md` resta una guida storica a due rami e non
   riapre A.
2. **Bibliografia già acquisita e pubblicata.** L'handoff rev.03 e i registri
   correnti dichiarano concluse acquisizione, integrazione e pubblicazione
   bibliografica. Il passo “futuro” descritto nel §1 del coordinamento è storico
   e non autorizza nuove ricerche, copie, download o acquisizioni.

Il verbale non viene corretto. Le due osservazioni non rendono indispensabile
un nuovo delta normativo prima della pubblicazione: il candidato già riporta lo
stato vigente nei documenti correnti e il revisore le classifica non bloccanti.

## Controlli di acquisizione

- repository e branch: `/Users/luker/fot-tep-finalizzazione-038`,
  `codex/studio2-finalizzazione-038`;
- HEAD iniziale: `03a7d7609faad06f2e6f2a6d39fd007268a99cde`, tree
  `a55017e3f3c1d0a5d14675a8dc8eb9b8649fff17`;
- remoto effettivo: `https://github.com/sorrentinoluca/fot-phd.git`;
- `refs/heads/main` remoto osservato:
  `a00605862f627710347bd63c49f79a6d0a00135f`;
- piano rev.10: 81.490 byte, SHA-256
  `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`;
- manifest storico: 25.894 byte, SHA-256
  `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`;
- manifest candidato: 12.382 byte, SHA-256
  `bcc9ef183190e2fd0997b2e600fc53498e4a6194993e997820255a4b6d124dc6`,
  con `freeze_effective=false`;
- guardiano prima dell'acquisizione: **NON PASS**, 35 test, 14 fallimenti
  storici, 1 skip; non classificato PASS;
- nessun file sottoscritto, push, merge, tag, pubblicazione o esecuzione.

Il commit che contiene verbale e presente record è un successore documentale e
non può essere incluso nel proprio testo senza auto-riferimento. Sarà indicato
nella consegna di pubblicazione successiva.
