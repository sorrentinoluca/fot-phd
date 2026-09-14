# Verifica indipendente delle correzioni R1–R4 — allineamenti 03.8 rev.10

Aprire una **nuova task indipendente dal preparatore**, preferibilmente con un
modello diverso. Sola lettura sul candidato: non correggere i file, non fare
commit, merge, push, tag, firma, API, inferenza, pilot o simulazione. È consentito
creare una copia isolata e scrivere soltanto il verbale finale nella sua cartella
di sottofase. Se individui un difetto, riportalo; non modificarlo.

Identifica effettivamente nel verbale **modello, provider, reasoning se esposto,
ID task/sessione e worktree**, branch o detached HEAD, commit/tree, stato locale.
Non copiare dal prompt un'identità o un effort atteso: se non esposti, dichiarali
non esposti e indica la fonte dei metadati disponibili. Dichiara l'indipendenza
rispetto alla task preparatrice e ogni suo limite reale.

## Oggetto esatto

- Base immediata (acquisizione NON OK): `1a21fd260ad2df6a3b04ffb6fa5e2d642a3f63b1`.
- **Nuovo candidato:** `9a56d12d0633a0c9790c48792182f26fc6eb424a`.
- **Tree candidato:** `e35e5ca661325657715dce6723e4e8ec09540101`.
- Main verificato dal preparatore: `a00605862f627710347bd63c49f79a6d0a00135f`.
- Candidato precedente NON OK: `4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8`.
- Sua consegna: `2520e7abc1cd68785f2789448b509dea5e55ee7d`.
- Candidato statistico storico OK: `6aaa5b3eebfed4ba502c25c0443caabd0051af21`;
  consegna/verifica: `51782e8c40069c0a2310afafc36907a61d517ff6`.
- Report candidato: `/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/REPORT_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`; SHA-256 `19d69fc5cb2d3deee514044ccb47e1e9b61eab2df996c0834e4594d03ac23dc4`.
- Manifest candidato: `/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/MANIFEST_CORREZIONI_ALLINEAMENTI_03_8_REV10.json`; SHA-256 `d422279aa15c94cbafe5afb0a1b61fb105967804709762d7942a9cef53b55303`.
- Worktree preparatore: `/Users/luker/fot-tep-allineamenti-038-r1-r4`,
  branch `codex/studio2-allineamenti-038-r1-r4`.

Il commit che consegna questo prompt è successivo, solo documentale: non è il
candidato normativo. Se la sessione monta soltanto `/Users/luker/fot-tep`, usare
gli oggetti Git per leggere `git show 9a56d12d0633a0c9790c48792182f26fc6eb424a:studio2/fase03/piano_statistico/REPORT_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`
e gli altri file, e creare da quel commit la propria copia detached. Non usare
il working tree principale, né sostituire il candidato con un HEAD mobile.

Prima di leggere il merito, controlla repository, worktree, branch, stato locale,
HEAD/tree e `origin/main`; confronta `git ls-remote origin refs/heads/main`.
Se main è avanzato, registra la differenza: valuta questo candidato sulla sua
base pinnata e segnala l'eventuale raccordo futuro senza importarlo o certificarlo.

## Letture e fonti

Leggi MAINTENANCE e prompt Prompt/Fase/Verifica/Documentazione/Commit pertinenti;
fonti/prevalenze del walkthrough, senza modificarlo. Leggi report, manifest e
controlli del nuovo delta, l'acquisizione NON OK e il verbale originario
`VERIFICA_ALLINEAMENTI_03_8_REV10.md`. Ricostruisci le fonti dai 27 pin del
manifest, non dal racconto del preparatore. Il verbale NON OK deve conservare
22.063 byte e SHA-256 `52944646527d0e73d6508ae53669f47f5e8661050ff777c75a448ca535ca9c13`.

Fonti di merito: piano statistico rev.10 §§1, 5, 7–11, 15–16; budget rev.10;
coordinamento §2; catalogo D1; pubblicazione/manifest schema R4; chiusura 03.5;
consegne e matrice storiche. I file rev.10 restano fotografie verificate: stati
storici pending/D9 non scelta non annullano il mandato successivo documentato.
L'approvazione dei ruoli deriva **dal mandato dell'autore trascritto nel report**:
122B principale/consumer; 27B alternativo, 16 insight, consumer 122B fisso nello
swap; Terra solo riferimento storico descrittivo interno. Il registro formale è
in acquisizione nella finestra proprietaria: non attendere né importare suoi
file non committati. Non pretendere una nuova approvazione dei ruoli e non
attribuire alla trascrizione una firma materiale o una qualificazione tecnica.

## Verifiche richieste

1. Genealogia: 4503cb6→2520e7a→acquisizione→nuovo candidato; verifica parent/tree.
   Acquisizione: due soli nuovi file, verbale byte-identico, nessuna correzione.
   Delta normativo: **2 M +5 A**. Report/manifest/controlli e log accompagnano
   soltanto piano generale e APERTURA. Nessuna modifica di harness, proposta o
   registro D9, paper_sections o walkthrough.
2. Preservazione: **38/38 file preesistenti** in piano_statistico identici a
   2520e7a; **19/19 files +6/6 inputs_read** del manifest rev.10 per dimensione,
   SHA-256 e byte con la consegna 51782e8. Verifica piano, manifest, verbale OK,
   atto non firmato, budget e delta harness. Vecchio report/manifest del candidato
   respinto e NON OK non sono cancellati o riscritti. Mantieni l'OK A/B nel suo
   perimetro: non ripetere la review statistica o i test che rigenerano griglie.
3. **R1:** §7/§8.7 e ogni altra prescrizione corrente: nucleo 1.728/5.184,
   totale distinto, niente giorni non misurati. Ledger e 1,20×T≤W, nessun tetto
   rigido 3.700, margine di calendario o percentuale del budget non documentati.
4. **R2:** otto run per fault e otto Normal, 64+8 primari; 148/444 per ablation;
   72+6+11=89, scorte sostitutive, mai nuove osservazioni, regole prima delle
   chiamate. Controlla anche §§5, 6.9, 8.1/8.3/8.5/8.8/8.12, D2/D3, §13 e
   confronto SWaT. Sei run/48 cluster ammessi soltanto come confronto storico.
5. **R3:** OOD F6/F4 condizionati, catene F6→F5→F12 e F4→F11→F5; sostituti
   verificati individualmente, distinti; collisione F5 o caso irrisolto→autore.
   D11={F1,F2}/{F14,F15}, indici 1–3; D12 R4 pubblicata e congelata, adapter
   e conformità futuri distinti. Freeze statistico→03.11 tecnica→chiamate dopo
   gli altri GO, anche nei raccordi E5: nessuna generazione anticipata o ciclo.
   T11 non diventa un nuovo blocco automatico, 03.5/FAR/U3 non si riaprono.
6. **R4:** ricerca estesa nel piano: niente assegnazione corrente Qwen-2.4T,
   surrogato consumer 27B o fallback Terra. Ruoli e aggiornamento del mandato
   coerenti, libreria alternativa completa e consumer fisso; storia preservata
   e localmente marcata, Terra fuori dalle nuove stime. Decisione dell'autore,
   acquisizione documentale e qualifica tecnica distinti; niente firma 03.8,
   ordine label approvato o servizi qualificati per implicazione.
7. Coerenza risultante: leggi tutte le prescrizioni correnti per queste quattro
   classi, non soltanto gli hunk o le righe del vecchio NON OK. Conferma che
   APERTURA resti coerente e che il perimetro aggiuntivo sia motivato. Nessun
   risultato nuovo, nuova analisi o nuova scelta scientifica introdotti.
8. Impronte nuovo manifest: **6/6 altri file**, nessun autoriferimento;
   27 fonti ai commit esatti. Il mandato è una fonte di conversazione dichiarata,
   senza inventare commit/hash esterni. `freeze_effective=false`, tag null e
   review pending corretti. Verifica anche report e stato dei residui.
9. Controlli: `git diff --check 1a21fd260ad2df6a3b04ffb6fa5e2d642a3f63b1..9a56d12d0633a0c9790c48792182f26fc6eb424a` e link/riferimenti pertinenti.
   Riesegui `python3 docs/test_explanation.py`: attesi **35 test, 14 fallimenti
   storici, 1 skip, 0 errori, exit 1**; confronta gli identificativi completi e i
   parametri dei subtest coi controlli JSON, non soltanto il conteggio. **Non PASS**.
   I log committati hanno solo tre spazi finali rimossi (righe 34/41/52); hash e
   dimensioni grezzi sono registrati nel JSON e ricostruibili aggiungendo uno
   spazio a ciascuna delle tre righe. Non confrontare hash grezzi fra diverse
   esecuzioni come se fossero deterministici: il tempo di esecuzione varia.

Questa è una **nuova review del delta correttivo e della coerenza risultante**;
non è una ripetizione della vecchia review, né una revoca o estensione automatica
dell'OK statistico. Non usare il guardiano come prova della correttezza normativa.

## Uscita

Scrivi nella tua copia isolata
`studio2/fase03/piano_statistico/VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`:
verdetto **OK oppure NON OK in prima riga**, identità effettiva del revisore,
base/candidato/tree/main osservato, metodo e comandi, per ogni punto esito
✅/⚠️/❌ con fonte, eventuali rilievi precisi, controlli e limiti. Comunica percorso
assoluto, dimensione e SHA-256, lasciando il file non tracciato per acquisizione.
Un OK non chiude 03.8/Fase 03, non firma, non pubblica, non congela, non approva
l'ordine label e non autorizza pilot o servizi. Nessun'altra scrittura sul candidato.
