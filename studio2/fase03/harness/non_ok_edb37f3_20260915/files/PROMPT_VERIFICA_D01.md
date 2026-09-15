# Verifica indipendente D01 / C01 / R04 — harness offline 03.10

Review in una finestra distinta dalla preparatrice, preferibilmente con altro modello.
Leggere `docs/MAINTENANCE.md` e prompt pertinenti. **Sola lettura del candidato**: nessuna
correzione, commit, tag, push, merge, freeze o GO. Test esclusivamente offline con stub;
nessuna API provider, inferenza o simulazione scientifica.

## Candidato da eseguire, distinto dalla consegna documentale

- Sorgente: `/Users/luker/fot-tep-harness-0310-d01`, branch `codex/studio2-harness-0310-d01`.
- **Candidato tecnico `edb37f359f29c461c5a507c1027c4bf411654130`**.
- **Tree `56d98666e1d18c7958ac8d3631ae6d5b8ec04bf9`**.
- Base documentale `52e13e1ed540e1ad076474398bf850445c9a4a00`; acquisizione separata `89b016a728bdbf5d2d8b438416e6133b050683da`.
- Respinto `9e18bcbd06fa2c54202c8eeda079c112dbfcefcd`, tree `5d1fd7924c4e1e46346f367590e6aa1977a6ba75`.
- Manifest `studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json`: **62 file**, 15815 byte,
  SHA-256 `c823cb669fb408080b46311e6c753be4b5243764d76e88ed67273f3c213c4fd8`.
- Remoto effettivo `https://github.com/sorrentinoluca/fot-phd.git`, main osservato
  `a00605862f627710347bd63c49f79a6d0a00135f`; ricontrollarlo, non usare l'origin locale come prova.

L'HEAD della sorgente comprende quattro file documentali successivi: report, prompt,
consegna e audit. Non eseguirlo in luogo del tecnico. Verificare diff, branch, HEAD/tree,
worktree, indice e modifiche prima di scrivere; creare un clone/worktree isolato detached
sul tecnico, output sibling `evidence/`. Preservare principale, sorgenti e review precedenti.

## Fonti

Leggere integralmente REPORT_CORREZIONE_D01.md e il verbale acquisito
`non_ok_9e18bcb_20260915/evidence/VERIFICA_C01_C03.md`.
SHA-256 verbale `35e047834ec957a8008db7b82c375d3022cbcfeb7a8d2fb80143f44e9cabfe42`;
manifest originale `29385ea6589286e7a551c13ee61c8588b7b5792dabba7fa5d3ebebcd090a34ea`.
Verificare copie/esterni e inventari prima dell'uso. Script acquisiti e prove già eseguite
non vanno lanciati in-place. Le fixture false/alterate non diventano input scientifici.

## Rilievo da verificare senza fermarsi alle nuove riserve

D01 residuo C01/R04: un vecchio ledger v2 con sonda e gate PASS ma alternativo FAILED o
INTENT era riconfermato dopo restart. Y01 usa il runner ordinario, Y02 le API di conferma.
Il delta corrente modifica solo ledger.py fra i runtime.

1. Generare nuove fixture con il codice **0c8157f esatto e pulito**, in subprocess, come
   edge_probes.py: otto producer validi, alternativo irrisolto, tre sonda e 120 gate chiusi
   dal vecchio codice. Poi riaprire col nuovo candidato. Nessuna modifica SQL per costruire
   tale difetto. Atteso rifiuto esplicito, nessun nuovo invio, contatori/raw/eventi preservati.
2. Eseguire entrambe le Y01/Y02 **senza adattare lo script**, poi gli ingressi: binding
   identico, verify_stage_success, replay dello stesso hash/outcome, authenticate_frozen,
   runner e CLI budget/stability con --resume. Provare sei stati alternativi non PASS.
3. Verificare che i prerequisiti siano ricontrollati anche sulla catena dei predecessori,
   e che conferma/autenticazione vedano una transazione coerente sotto scrittore concorrente.
   Non basta verificare solo `_ready` o ottenere una qualunque eccezione di setup.
4. Controlli positivi obbligatori: vecchio gate valido con alternativo assente o PASS;
   sonda rimaterializzata dopo gate già concluso; summary gate mancante; remediation
   valida e invalidità C02. Nessun nuovo invio, evento o azzeramento per la sola ripresa.
5. Distinguere lettura forense di event/binding/record da conferma normativa. Le prove
   negative devono respingere la conferma senza cancellare gli eventi storici irregolari.
6. Non riaprire C02/C03 per assunzione: verificare che il delta mantenga 120 primi tentativi,
   INVALID nel denominatore, R3 con 119 validi, zero retry gate e contatore producer 9
   distinto da 8 coppie T9. Y03–Y07 e le suite forniscono controlli aggiuntivi.

## Riproduzioni e conteggi dichiarati

Runtime `/opt/anaconda3/bin/python3`, Python 3.13.9 e SQLite 3.51.0, oppure ambiente compatibile
verificato. `PYTHONDONTWRITEBYTECODE=1`, cwd candidato anche per subprocess. Comandi in
`d01_evidence/COMANDI.md`. La reference è
`/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference`.
FOT_HARNESS_LEGACY_CANDIDATE può indicare un altro checkout esatto/pulito 0c8157f per le
nuove regressioni; edge_probes.py originale mantiene il suo percorso OLD da verificare.

- 103/103 mirati, 138/138 discovery (sette D01 già inclusi); sette nuove regressioni 7/7.
- Y01–Y07: sul respinto 5 PASS e 2 failure; sul nuovo 7/7, nessun adattamento degli assert.
- 14/14 applicabili: 12 letterali, due con i vecchi adattamenti fixture/argomento.
- X: 23 letterali + X23 adattato, già verificato nel terzo verbale. Il file X23 letterale
  conserva una failure perché attende l'interruzione difettosa di C02; non chiamarlo 24/24
  del file immutato. Nessun adattamento nuovo in questa consegna.
- Nove test del raccordo qualificato inclusi; i tre file metriche invariati.
- Guardiano documentale **NON PASS**, 35 test, stessi 14 identificativi falliti, 1 skip.
- 91 sorgenti live compilabili; 174 file protetti confrontati senza variazioni.

Matrice R01–R10 corrente in MATRICE_R01_R10_D01.md; matrice esplicita dei 50 metodi acquisita
in non_ok_9e18bcb_20260915/evidence/MATRICE_50_METODI.md e JSON. Verificare corrispondenze e
limiti senza confondere 14 applicabili con l'intera copertura, né contare le sovrapposizioni.
Il difetto D01 è uno, riprodotto con due Y e ulteriori controlli del delta.

Verificare manifest 62/62, SHA256SUMS nuove prove, 1.789 file acquisizione e 1.893 file delle
riproduzioni con i rispettivi inventari e coordinate esterne recuperabili. Diff tecnico:
49 file dopo acquisizione separata di 175; solo ledger.py fra i runtime. Successore
quattro documenti distinto. Non modificare C02/C03, metriche, piano, APERTURA, walkthrough,
D9, 03.7/03.9/03.12, A/B, FAR o U3 per risolvere problemi del setup di review.

## Limiti e consegna della review

D9 già approvata: 122B principale producer/consumer; 27B alternativo per libreria completa;
Terra storico interno. Recepimento eseguibile D9, ordine label e qualificazioni rimangono
separati; non chiedere nuovamente i ruoli né abilitare il preflight storico.

La preparatrice è il task 01a0a204-abda-7a00-8466-f52f5bc84812, runtime osservato
gpt-6-astra/xhigh (estratto nel DELIVERY_AUDIT_D01 documentale). La review acquisita usa
un'altra finestra ma lo stesso modello gpt-6-astra/high. Registrare modello/effort realmente
osservati e finestra propria; non equiparare indipendenza di finestre e di modello.

Scrivere un verbale con **OK o NON OK limitato al candidato offline esatto**, motivazioni,
matrice dei metodi/adattamenti, log e manifest SHA-256. Distinguere difetti del candidato,
errori di setup/dipendenze e limiti non verificati. Preservare stato del candidato detached
pulito e di tutte le sorgenti; niente correzioni in questa review, nessun freeze o GO.
