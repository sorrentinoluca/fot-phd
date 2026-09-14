# Report di sotto-fase 03.8 — revisione 10, recepimento A/B

Data: **2026-09-14**. Preparatore: **Codex GPT-6**, sessione corrente.
Profilo: decisionale/documentale, controlli offline.
Stato: **A/B approvate e recepite; nuova verifica indipendente pending**.
Firma materiale **pending**; piano non congelato; sotto-fase 03.8 e Fase 03 aperte.

## 1. Approvazione e perimetro

Luca ha approvato senza modifiche A e B dell'addendum al commit
`526561feabeb6b4083170b1817b8abdac1a2a4c7`. Il messaggio esplicito è registrato
con data effettiva **14 settembre 2026**, Europe/Rome, in
[APPROVAZIONE_ADDENDUM_03_8.md](APPROVAZIONE_ADDENDUM_03_8.md), commit
`f37e7e00cbdd959ef6fdb7cc96ce42ed521075d6`.
L'addendum approvato è rimasto byte-identico, SHA-256
`6035967ceb390de69e63cac9f828b17386ab8a76bb1999db524597770fc782f8`, 3.768 byte.
La registrazione dell'approvazione non costituisce firma materiale.

Sono recepite soltanto le due modifiche del protocollo approvate:

- **A:** il tetto rigido 3.700 è sostituito da conteggio completo per blocco/modello
  e fattibilità temporale misurata nel pilot, con margine 20%; trigger R invariato,
  sospensione organizzativa e decisione autore se il ramo non è fattibile;
- **B:** candidati/criteri/catene OOD e disegno si congelano prima dei run;
  generabilità/trip/ammissibilità sono verificati in 03.11 dopo freeze e prima
  delle chiamate. Non si scelgono fault usando prestazioni o separabilità;
  sostituti con verifiche proprie, OOD distinti, sospensione dei casi non risolti.

L'OK rev. 9 resta storico, non approva il delta. Nessuna nuova scelta D9 o E5;
nessuna modifica a ipotesi, margine m, alpha, gerarchia, reporting, algoritmi e
risultati DESIGN_RESOLUTION, campioni, scorte, criteri OOD, validità, remediation,
riserva e gate, salvo la regola organizzativa A effettivamente approvata.

## 2. Base preservata e catena delle impronte

Worktree iniziale pulito sul commit approvato `526561f`, branch
`codex/studio2-piano-statistico-fix`. Gli undici artefatti della preparazione e la
bozza storica restano invariati: i pending in quei documenti sono lo stato di quel
checkpoint, superato dal record di approvazione e dalla presente revisione.
Il controllo `check_preparazione_chiusura.py` si riferisce allo snapshot `526561f`:
è stato superato prima delle modifiche; non va eseguito contro il piano rev. 10
aspettandosi le vecchie impronte. La verifica corrente usa il nuovo manifest.

| Record storico | Identità preservata |
| --- | --- |
| Rev. 7, checkpoint | `7f760b7146cb858f5ef01ab3a1c61aef3a7577b3` |
| Rev. 8, candidato | `75bd14898e43f03f849c5d248d6c2481da55e245` |
| Rev. 8, verbale NON OK | commit `f700326a096c7a79efd2feceb93939580f5057dc`; hash `e7b0846e36b9b2328bb073f486921aacbf29e66337bcb53efe8ab1cdec7cdd11` |
| Rev. 9, candidato verificato | `6015f8fdb1b28e0adad50219466bf13cd988c137`; manifest di allora `586a26239862ed981bed35614486b9596b8f3931d638107ea214c7cb1d40121c` |
| Rev. 9, verbale OK | preservato in `29249a9305c44a44b96e6f49f94e978956ed0ac2`; hash `289a74433d70e2bf911bdea893711ff7a294c75cf74d5e6fa0addbf3ede72a58` |
| Rev. 9, registrazione dell'OK | `0f1a9bae8b522f614720fa5efe7bd9d2577609ae`; manifest `2b6ad396307be634428d9355d4aa65144b4956d675ccb9e4b47536e4bdaf8d76` |
| Preparazione delle proposte | `526561feabeb6b4083170b1817b8abdac1a2a4c7`; manifest `a570c0c91f3a45d4435d318e628cdad37ef7be0dceda17fcb62cf50350dead93` |

Il manifest storico rev. 9 è anche conservato byte per byte in
[PIANO_STATISTICO_FREEZE_REV9.json](PIANO_STATISTICO_FREEZE_REV9.json): le sue
voci di piano/report vanno risolte al commit storico `0f1a9ba`, non ai file correnti.
I verbali rev. 7/8/9 non sono stati modificati. Il report precedente resta
recuperabile con `git show 526561f:studio2/fase03/piano_statistico/REPORT_PIANO_STATISTICO.md`.

Il manifest corrente `PIANO_STATISTICO_FREEZE.json` porta **revision=10**,
`freeze_effective=false`, `freeze_tag=null`, `independent_review.revision_10=pending`.
Impronta piano, report, approvazione, allegato contabile, atto non firmato, controlli,
prompt di verifica e input storici. Non contiene il proprio SHA né un commit che
si auto-referenzia; commit candidato e impronta del manifest si registrano nella
consegna e nel successivo verbale indipendente.

## 3. Delta esatto del piano

| Punto | Modifica |
| --- | --- |
| Intestazione e nota rev. 10 | data effettiva, fonte A/B, review nuova pending; note storiche riconoscibili |
| §0 e §1 | regola organizzativa approvata; vincolo verso 03.11 con ordine B |
| §7.2 | 3.700 storico, conteggio completo e T5 misurato; allegato per blocco/modello/R |
| §8.2 | ordine candidati/criteri/catene→run→controlli→chiamate; divieto di selezione diagnostica e sospensione esplicita |
| §10.2 | il richiamo al vecchio tetto rinvia alla fattibilità della regola A; trigger di R intatto |
| §11 T5 e ultimo paragrafo §11.1 | regola A recepita, altri gate/riserva e autorizzazione futura remediation invariati |
| §15 | A/B approvate, residui operativi distinti dalle nuove decisioni |
| §16 | condizioni freeze separate da prima-pilot/prima-chiamate-test; ciclo 03.8→03.11→03.8 eliminato da B |

Il congelamento statistico richiede ancora firma, nuova verifica, integrazione
bibliografica, allineamenti delle regole, documentazione e pubblicazione secondo
MAINTENANCE. L'implementazione 03.10, input di sviluppo, schema, mapping, capienza
ed identità della configurazione rimangono obbligatori **prima del pilot**.
I controlli OOD non sono eliminati: restano obbligatori **prima delle chiamate sui
test**, dopo la generazione e il congelamento del disegno. T5 usa le misure del
pilot per autorizzare lo studio; la regola non dichiara misure già disponibili.

## 4. Contabilità e bibliografia

[BUDGET_RISORSE_REV10.md](BUDGET_RISORSE_REV10.md) è l'allegato contabile corrente.
Il nucleo costa 1.728/5.184 a R=1/3; nucleo+swap misura+ablation+OOD 2.244/6.732.
Il totale aggiunge audit (2k soltanto a R=1), E5 a R=1, eventuale FULL non riusabile,
canary 10/giorno, produzione ulteriore, pilot, tecnica e retry ammessi. Nessun
conteggio doppio fra librerie/conformità o audit/ripetizioni già incluse.
Scenario S=12, d=10, riusi completi, P_tot=160, X=100, Q=0: **3.142/7.284**,
prima di retry fuori pilot; è uno scenario, non budget definitivo o nuova autorizzazione.
Le vecchie differenze arrotondate +638 e +702 (+24,6%) restano storiche.
La sonda può ripetere solo triplette entro la quota 7 anche senza remediation;
conformità e riserva restano `8r+t≤15`, massimi 152/160, hard stop 200 separato.

Il candidato bibliografico resta esterno: la preparazione ne ha verificato 23/23
impronte nella sorgente e nello snapshot. Verbale OK SHA-256
`551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`.
F6 soddisfatta entro PHM non equivale a prova tecnica. Registro, H, D1 e addendum
F9–SPE restano intatti; nessuna integrazione o conservazione esterna dei PNG
viene dichiarata eseguita dalla rev. 10.

## 5. Allineamenti e file

Il delta predisposto in `COORDINAMENTO_CHIUSURA_03_8.md` resta utilizzabile:
si applica ora il ramo **A approvata** per i punti correnti §8.8/D2/T5/O2/§13 e
il ramo **B approvata** per OOD/APERTURA; 3.700 resta solo nei richiami storici.
Le condizioni «se A/B» di quel checkpoint non sono nuove richieste all'autore.
`DELTA_HARNESS_03_10.md` resta la consegna tecnica al proprietario; questa finestra
non modifica il suo branch. Le modifiche al piano generale/APERTURA, l'integrazione
bibliografica e il walkthrough saranno eseguiti serialmente con le altre finestre,
riverificando ogni delta ulteriore prima di dichiarare il candidato finale verificato.

File del recepimento, nella cartella 03.8:

- `APPROVAZIONE_ADDENDUM_03_8.md`: nuova decisione in commit separato;
- `PIANO_STATISTICO.md`: recepimento normativo A/B;
- `REPORT_PIANO_STATISTICO.md`: questo report, sostituisce il report corrente rev. 9;
- `PIANO_STATISTICO_FREEZE.json`: manifest corrente rev. 10, review/firma/freeze pending;
- `PIANO_STATISTICO_FREEZE_REV9.json`: copia storica integra;
- `BUDGET_RISORSE_REV10.md`: allegato contabile con A approvata e parametri pending;
- `DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md`: atto corrente con approvazioni A/B e firma vuota;
- `CONTROLLI_REV10.json`: esiti offline e confronto degli invarianti;
- `PROMPT_VERIFICA_REV10.md`: incarico della nuova verifica su commit esatto.

Nessuna coppia MD/HTML toccata, nessuna nuova struttura da indicizzare; la sintesi
divulgativa non è pertinente a questo passaggio interno. Il walkthrough non viene
aggiornato prima del nuovo OK. Gli artefatti preparatori restano come traccia del
lavoro antecedente all'approvazione, non fonti correnti dello stato.

## 6. Controlli del preparatore

- 26/26 test statistici OK, `/Users/luker/fot-env/bin/python`, Python 3.13.9;
  soltanto i calcoli temporanei previsti dalla suite, nessuna nuova griglia.
- `python3 docs/test_explanation.py`: 35 test, 14 fallimenti, 1 skip sia prima sia
  dopo; identici tutti i 14 identificatori/subtest, registrati in CONTROLLI_REV10.json.
- 28 blocchi di testo statistico confrontati byte per byte con la base;
  15 input/file immutati del vecchio manifest ricalcolati; DESIGN_RESOLUTION,
  generatore, test, bozza e verbali storici integri.
- Impronte correnti, JSON, link, conti, stati e `git diff --check` verificati prima
  del commit. I controlli locali non sono una verifica indipendente.

## 7. Requisiti di chiusura

| Requisito | Prova | Stato |
| --- | --- | --- |
| Approvazioni storiche | bozza intatta e manifest | completato |
| Nuove decisioni A/B | messaggio Luca, data effettiva, commit f37e7e0 | completato |
| Recepimento nella revisione 10 | piano e manifest correnti, delta §3 | completato, da riverificare |
| Firma materiale | atto rev. 10 predisposto, nessuna firma acquisita | pending |
| Budget completo e regola organizzativa | allegato e §7.2; parametri/misure effettive mancanti | regola completata; T5 pending |
| Ordine OOD non circolare | §8.2/§16 con B approvata | regola completata; controlli 03.11 pending |
| Integrazione bibliografica e PNG | inventario/procedura preparati | pending seriale |
| Piano generale/APERTURA | delta predisposto, rami A/B ora approvati | applicazione pending seriale |
| Implementazione 03.10/prerequisiti pilot | delta per worktree proprietario | pending prima del pilot |
| Nuova verifica indipendente | prompt rev. 10 pronto, verbale non ancora acquisito | pending |
| Walkthrough e commit finali | dopo OK del candidato effettivo | pending |
| origin/main e tag previsto | nessuna operazione esterna eseguita | pending |

Messaggio candidato: `studio2(piano-statistico): recepisce addendum A e B nella revisione 10`.
Nessun push, merge o tag; nessuna scelta D9, inferenza, simulazione TEP o modifica
03.5. La revisione si consegna a un revisore distinto; non si certifica il proprio
lavoro. Il tag `studio2-fase03-piano-statistico-frozen-001` resta non creato.

Letture: contratto/prompt di ciclo, file del candidato approvato, piano/manifest/
report correnti e sezioni pertinenti già lette, delta predisposti; ordine di
qualche decina di migliaia di parole di documentazione. Nessun nuovo paper o
risultato sperimentale letto in questo recepimento.
