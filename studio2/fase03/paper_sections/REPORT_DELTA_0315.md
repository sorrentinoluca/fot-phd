# Delta 03.15 — normal_dev reale, chiusura 03.5 e decisioni rev. 10

**Preparato per verifica indipendente; nessun OK attribuito al nuovo delta.**
Data: 2026-09-14, Europe/Rome. La sotto-fase 03.15 e la Fase 03 restano aperte.

## 1. Oggetto esatto e separazione dalla verifica storica

| Riferimento | Commit completo |
| --- | --- |
| Candidato scientifico storico riverificato OK | `cf79e81f917c7969dfd375e38db54315c28d4c07` |
| Acquisizione byte-identica del verbale | `50f07a998afb87b832aab6653c9241c69ac3b020` |
| Base di ingresso del nuovo lavoro, acquisizione report | `1d480fd62ff72c4bc5e60df6ffb46ee36f58151a` |
| Correzione documentale distinta | `bcb462da3f3c329af5b80d9cb028bb8893a8d09d` |
| **Candidato scientifico del nuovo delta** | **`91a880b136dee5d805b54040f5e32345be361eb2`** |

La genealogia è lineare: cf79e81 → 50f07a9 → 1d480fd → bcb462d → 91a880b.
`50f07a9` è figlio diretto di `cf79e81`. Il commit documentale corregge soltanto
«parent diretto» in «figlio diretto» nel report di acquisizione.
Il delta scientifico da valutare è **bcb462d..91a880b**; il perimetro complessivo
nuovo è **1d480fd..91a880b**, includendo il refuso separato.

Questo report, il prompt e `CONTROLLI_DELTA_0315.json` sono consegnati in un commit
successivo di soli documenti, identificato nella consegna operativa. Non cambiano
il candidato scientifico e non costituiscono un verbale indipendente.
Il revisore deve valutare il nuovo delta e la coerenza delle sezioni risultanti,
senza ripetere la vecchia review o trasferire automaticamente il suo OK al delta.

Il verbale storico [VERIFICA_PAPER_SECTIONS.md](VERIFICA_PAPER_SECTIONS.md) resta
byte-identico: **13.949 byte**, SHA-256
`8faca80c87071d87bf66d97848c290a5724f6569be6f6040cfb6568bad022cb1`.
Conservati il NON OK storico, il successivo OK, il record di acquisizione e
`REPORT_PAPER_SECTIONS.md`, comprese le loro descrizioni temporali superate.

## 2. Preflight, branch e concorrenza

Worktree usato: `/Users/luker/fot-tep-paper-sections`;
branch **`codex/studio2-paper-sections`**. Prima della prima scrittura:
HEAD esatto `1d480fd`, nessuna modifica tracciata o non tracciata; presente soltanto
la cache ignorata `paper_sections/__pycache__/`. Stato ricontrollato e nessun
processo Git di scrittura concorrente rilevato. Il worktree proprietario era libero;
non è stato necessario crearne un altro né riallineare la storia con un merge/rebase.

`origin/main` locale e `refs/heads/main` remoto coincidevano su
`c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`, confermato anche dopo il commit scientifico.
Sono stati controllati worktree, branch, HEAD, remote e storia. La copia iniziale
`/Users/luker/fot-tep` era su `codex/studio2-soglie-normal`, HEAD `819b12e`, con
molti file non tracciati: letta soltanto per handoff e prompt locale, non usata come main.
Nessuna scrittura nei worktree del raccordo seriale evidence→schema→letteratura,
nel piano statistico, nell'harness o nella chiusura 03.5/03.9.

## 3. Fonti, precedenze e impronte

[FONTI_DELTA_0315.json](FONTI_DELTA_0315.json) registra **54 fonti**, ciascuna con
percorso, commit completo quando esiste, byte e SHA-256. Le sigle nelle bozze sono
localizzatori editoriali verso questo record, non riferimenti a HEAD mobili.

| Sigla | Snapshot usato e funzione |
| --- | --- |
| S05 / S09 | main `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`: fonti e consegne correnti 03.5/03.9 |
| S08 | candidato rev. 10 `6aaa5b3eebfed4ba502c25c0443caabd0051af21`: piano, manifest, atto non firmato, addendum/approvazione e budget |
| S08-consegna | `51782e8c40069c0a2310afafc36907a61d517ff6`: consegna e verbale rev. 10 acquisito |
| S06 | `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb`: evidence-v2, dipendenze, codice di estrazione/leakage e provenienza U3 |
| S12 | `3c64390bc4dd58c48cc4e1e388a38989b32b3143`: contratto R4, schema e manifest; nessuna nuova qualifica di tokenizer/modello |
| L | `40911d0e3e7b75960e6973f3fd8f609e65ab6e05`: corpus e verifica bibliografica acquisita; candidato esterno al branch 03.15 |
| BASE | `1d480fd62ff72c4bc5e60df6ffb46ee36f58151a`: regole, prompt, piano generale e record storici |
| MAIN-provenienza | `c486eee`: §11 e §11.1, origine e destinazione U3 nella 03.9 già registrate |
| H | handoff rev02 locale non tracciato; versione identificata da percorso, byte e SHA-256, §§4.9 e 5 per il 122B |

I riferimenti generali ereditati «piano» restano il piano generale alla base;
le regole aggiornate della 03.8 vengono dal pin S08, con la consegna successiva
che distingue review, firma e freeze. Le fonti scientifiche non cambiano se
un'altra finestra integra nuovi commit. I pending dei manifest storici non sono
stati riscritti: per la pubblicazione 03.9 prevalgono consegna/rev. 3; per l'OK
statistico prevale la consegna successiva, senza trasformarlo in freeze.

H e il prompt storico 03.15 non hanno un commit: questo limite è esplicito, non
sostituito con un hash Git inventato. L'inventario server è una comunicazione
dell'autore riportata dall'handoff, non una misura o interrogazione del servizio.
Il revisore deve verificare l'impronta del file disponibile o dichiararne l'assenza.

## 4. Matrice fonte → modifica

| Fonti primarie identificate nel record | Destinazione | Modifica e limite |
| --- | --- | --- |
| S09 specifica Normal, piano CSV, audit, accettazione, consegna e freeze rev. 3 | `protocol.md`, `verbalizer.md` | normal_dev reale: 40 run preassegnati, cinque/agente, stream 60000–60039, 320 finestre/40 cluster; sviluppo esclusivo. Divieti su normalizzazione, soglie, FAR, selezione del protocollo e test. Provenienza verificata senza cancellare deviazioni accettate o attribuire il checkout al lancio |
| S09 prototipi, manifest, specifica baseline e controllo vettori | `verbalizer.md` | 9 globali +16 locali, 697-D, media aritmetica, L1 media, pareggi entro 1e-12 → astensione, nessuna soglia di distanza o ripiego globale. Scarto zero è un controllo già prodotto, non una nuova stima di performance |
| S09 handoff e specifica Normal; S06 dipendenze/U3; MAIN-provenienza §11 | `verbalizer.md`, appendice `PROVENIENZA.md` | evidence riuscite in normal_dev_002, otto esempi run locale 1/finestra [25,30); N1–N5/V2 indivisibili, rigenerazione fail-closed se R2 decade; seed/data legacy mancanti |
| S05 freeze, FAR JSON/MD, decisione autore, verbale correttivo e integrazione | `verbalizer.md`, `protocol.md` | 03.5 chiusa, soglia 13.623626738268857, rango 334/350 e S>threshold; FAR primario 11/150 e secondario 108/1500 con i rispettivi intervalli. Distinzione freeze/apertura analitica, accessibilità precedente e limite probatorio già accettato |
| S08 piano §§2–6, 12–16 e atto rev. 10; S08-consegna | `protocol.md`, `threats.md`, `PIANO_SEZIONI.md` | D2=8, 64 fault+8 Normal; Hoeffding, Tango, m=0,125, α=0,05, sensibilità H3 0,025, sequenza e guadagnati/persi/saldo approvati. Firma e freeze ancora distinti; garanzia finita H1/H2 condizionata e gerarchia approssimata per H3 |
| S08 §§7.2, 10–11 e budget rev. 10 | `protocol.md` | R su coppia parsata/validità, tripletta invalida, audit/canary, conto completo parametrico e margine temporale 20%; hard stop 200 distinto da riserva e massimi 152/160; nessun tetto vigente 3.700 o GO automatico |
| S08 §§7.4, 8–9, 16; L addendum PHM | `protocol.md` | D11 e run 1–3; F6/F4 condizionati con entrambe le catene; controlli OOD dopo freeze prima delle chiamate; scorte e sostituzione fault distinti, sospensione se le regole non risolvono il caso |
| H §§4.9, 5; piano D9; S08-consegna | blocchi VARIANTE di `protocol.md`, `method.md`, `threats.md`, `PIANO_SEZIONI.md` | D9 esplicitamente aperta, 122B dichiarato operativo ma non qualificato; nessun ruolo assegnato; opzioni storiche condizionali, producer-swap e alternativo D9.1 preservati; storico Terra non promosso a braccio controllato |
| S12 decisione/schema R4 | `method.md`, rinvio in `verbalizer.md` | solo pin del contratto e raccordo Normal senza insight; sei campi, otto label fault opache, Normal letterale e Unknown astensione preservati |
| L corpus §§14.1–14.2, Tango/Hoeffding/Clopper–Pearson/McMahan | `protocol.md`, `verbalizer.md`, `threats.md`, sola annotazione in `related_work.md` | riferimenti ora disponibili nel candidato bibliografico identificato, con limiti. Non riscritto il corpus; non dichiarato integrato nel branch. Per Tango l'indipendenza non risolve da sola l'eterogeneità in strati fissi |
| MAINTENANCE §8.2 e provenienze S06/S09 | `verbalizer.md`, `PIANO_SEZIONI.md`, raccordo in `threats.md`, appendice interna | eliminata dalla bozza la narrazione motivazionale dei risultati storici; origine/riuso documentati internamente. Nessun risultato storico cancellato dai report o dalla storia Git |

## 5. File e perimetro dei commit

Commit documentale **bcb462d**:

- `studio2/fase03/paper_sections/REPORT_ACQUISIZIONE_VERIFICA_PAPER_SECTIONS.md`: sola correzione figlio/parent.

Commit scientifico **91a880b**, otto file:

- `studio2/fase03/paper_sections/protocol.md`: allineamento dati, statistica, risorse, OOD e D9.
- `studio2/fase03/paper_sections/verbalizer.md`: evidence reali, baseline, soglia/FAR e provenienza.
- `studio2/fase03/paper_sections/method.md`: solo raccordo D9 e pin schema R4.
- `studio2/fase03/paper_sections/threats.md`: approvazioni, limiti inferenziali e raccordo D9; rimossa la comparazione narrativa con lo studio esplorativo.
- `studio2/fase03/paper_sections/related_work.md`: solo annotazione del riferimento FedAvg ora disponibile; nessun claim nuovo.
- `studio2/fase03/paper_sections/PIANO_SEZIONI.md`: mappa e segnaposto coerenti con le bozze aggiornate.
- `studio2/fase03/paper_sections/FONTI_DELTA_0315.json`: pin e impronte delle fonti.
- `studio2/PROVENIENZA.md`: sola nuova sezione in coda, riuso redazionale e raccordo U3 già autorizzato; nessuna riscrittura delle sezioni precedenti.

Il raccordo fuori da protocol/verbalizer evita stati contraddittori nelle sezioni
consegnate insieme: proposte statistiche ancora da approvare, pilot sul solo modello
disponibile e bibliografia FedAvg dichiarata da acquisire. Non cambia il metodo,
lo spazio delle label, i bracci o la letteratura; non promuove il pacchetto in `docs/paper/`.
Nessuna coppia MD/HTML modificata. Walkthrough invariato fino all'eventuale OK indipendente.

Commit successivo di consegna: questo report, `PROMPT_VERIFICA_DELTA_0315.md` e
`CONTROLLI_DELTA_0315.json`, senza modifiche scientifiche.

## 6. Controlli del preparatore, non certificazione

[CONTROLLI_DELTA_0315.json](CONTROLLI_DELTA_0315.json) conserva comandi, ambiente,
impronte, valori controllati, preambolo completo del guardiano e identificativi
con parametri dei subtest. Log completi e script di riscontro locale sono in
`/tmp/fot-tep-0315-delta-20260914`; non sono necessari per ricostruire i pin Git,
e la loro disponibilità temporanea non è presentata come conservazione permanente.

| Controllo | Prima | Dopo |
| --- | --- | --- |
| Lint delle cinque sezioni, corpus locale | 5 file, 0 segnalazioni, exit 0 | 5 file, 0 segnalazioni, exit 0 |
| `python3 docs/test_explanation.py` | 35 test, 14 fallimenti, 1 skip, 0 errori, exit 1 | stessi conteggi e stessi identificativi/parametri dei subtest, exit 1 |
| Preambolo completo test/subtest del guardiano | acquisito | byte-identico dopo estrazione, SHA nel JSON |
| `git diff --check` del delta | — | nessuna segnalazione |
| Fonti commit/path/byte/SHA | snapshot identificati | 54/54 coincidenti |
| Numeri su artefatti | — | soglia/rango/n; FAR e intervalli; 40/320; 9+16 vettori di 697 componenti; firme Normal 320 globali/40 locali; pareggi; scarto registrato zero; freeze inefficaci |
| Riferimenti | — | percorsi Git nel manifest risolti; link Markdown relativi controllati; localizzatori statistici/bibliografici letti sulle fonti identificate |
| Verbale indipendente storico e record protetti | acquisiti alla base | byte-identici |

Il guardiano controlla documentazione storica, non convalida queste bozze. Il lint
resta minimale e invariato: non prova sostegno scientifico, assenza di leakage semantico
o correttezza di ogni riferimento. La lettura manuale e i riscontri meccanici del
preparatore sono evidenza per il revisore, non un OK indipendente.
Non eseguiti test statistici che rigenerano simulazioni/Monte Carlo, bootstrap, batch,
inferenze, API sperimentali, estrazione o ricalcolo dei prototipi. I confronti numerici
sono letture di artefatti già prodotti e aritmetica delle cardinalità/contabilità.

## 7. Residui e decisioni dell'autore

- **D9:** formalizzare producer principale, consumer, producer alternativo e configurazione
  sulla disponibilità aggiornata 27B/122B/Terra. Fonte H §5: disponibilità e intenzione
  di confronto non assegnano ruoli. Conseguenza: senza decisione non si attiva un ramo,
  non si definisce un confronto controllato e non si qualifica il servizio per lo studio.
  L'alternativo D9.1 resta da identificare; producer-swap resta previsto.
- **03.8:** firma materiale e freeze/tag statistico restano pendenti; allineamenti,
  integrazione e documentazione competono alle finestre proprietarie. A/B, FAR e le
  altre decisioni approvate non richiedono una seconda approvazione.
- **Fattibilità e OOD:** misure T5, ledger/configurazione/calendario, implementazione
  03.10 e qualificazione sono ancora operative. In 03.11, dopo il freeze, controlli
  OOD e sostituti secondo B; eventuale collisione su F5 richiede sospensione e una
  decisione concreta allora, non una nuova selezione preventiva in questa finestra.
- **03.9:** lo snapshot S09 registra raccordo metriche, sorgenti 03.6 e tag baseline
  pendenti. Integrazioni concorrenti successive devono essere valutate per i loro
  commit esatti, senza aggiornare retroattivamente queste fonti.
- **Limiti già registrati:** indipendenza effettiva dei cluster e applicabilità Tango;
  tracciabilità FAR e normal_dev; seed/data mancanti N1–N5; H non tracciato; limiti del lint.
  L'OK storico non viene riesaminato su questi punti. Gli arretrati bibliografici e
  redazionali invariati del suo verbale, incluse O6/O7/O9, restano identificabili lì.
- **Consegna:** review indipendente del nuovo delta; soltanto dopo eventuale OK,
  documentazione e integrazione se autorizzate. Risultati diagnostici, abstract,
  conclusioni e promozione in `docs/paper/` restano fuori da questo incarico.

## 8. Esecutore e letture

Esecutore: **OpenAI `gpt-6-astra`, reasoning `high`**; task/sessione
**`01a0a0bb-1683-7dd0-b29b-edfffb83de56`**, agente `/root`, Codex desktop.
Identità letta nei metadati locali `session_meta` (provider OpenAI, ID) e
`turn_context` (modello, effort), non dedotta dallo stile. Profilo redazionale
con riscontri tecnici locali. Nessun revisore indipendente è stato avviato qui.

Letture mirate: handoff rev02; MAINTENANCE e cinque prompt operativi; prompt storico
03.15; acquisizione/verbale e sei file di sezione/mappa; fonti primarie della matrice,
consegne e allegati statistici pertinenti; provenienze S06/main; contratto schema R4;
corpus e verbale bibliografico per i soli raccordi descritti. I JSON grandi sono stati
ispezionati per campi pertinenti e improntati integralmente, non trascritti nelle bozze.
Ordine di grandezza del materiale consultato: decine di migliaia di token, senza
nuova ricerca bibliografica, simulazione o inferenza sperimentale. Commit solo locali;
nessun merge in main, push, tag o aggiornamento del walkthrough.
