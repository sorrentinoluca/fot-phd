# Consegna del raccordo metriche 03.9 → 03.10

## Identità, data ed esito

- **Sottofase:** 03.10 — harness API e input pilot; delta circoscritto al raccordo delle
  metriche prodotte dalla baseline numerica 03.9.
- **Data:** 14 settembre 2026, Europe/Rome.
- **Attività:** implementazione e verifica offline del mapping dei nomi, dei conteggi e dei
  denominatori; ricognizione dei punti effettivi di produzione, lettura e consumo; aggiunta di
  test per casi ordinari, astensioni, invalidi e denominatori nulli.
- **Esito:** candidato implementato e committato localmente; verifica indipendente ancora
  **PENDING**. L'esito non chiude 03.9 o 03.10 e non costituisce autorizzazione al pilot.

## Identità Git e worktree

- **Worktree proprietario:**
  `/Users/luker/fot-tep/.worktrees/studio2-harness`
- **Branch:** `codex/studio2-harness`
- **HEAD iniziale del delta:**
  `51160872906feaa63c1fda5e9cf6e0fe8538fb16`
- **Commit implementativo:**
  `caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae`
- **Commit di consegna/manifest:**
  `1ac06ebdc92f73d3b630ccca9bf75f413bea170b`
- **HEAD corrente:**
  `1ac06ebdc92f73d3b630ccca9bf75f413bea170b`
- **`origin/main` verificato:**
  `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`
- **Relazione corrente:** branch 8 commit avanti e 31 indietro rispetto a `origin/main`;
  nessun merge del candidato in main.

## Contratto implementato

Il raccordo applica `accuracy` → `accuracy_all`, `n` → `total` e `abstentions` →
`abstained`. `non_abstained` viene preservato solo dopo la verifica
`non_abstained = total - abstained`. I tre rapporti vengono copiati dalla sorgente dopo averne
verificato l'aritmetica, senza ricalcolo o arrotondamento nell'output.

La baseline 03.9 produce esclusivamente righe `valid=true` e arresta l'esecuzione sugli input
invalidi; l'adapter può quindi esporre `invalid=0` solo dopo aver verificato il formato valid-only
03.9. Nel calcolo generale 03.10 un invalido non è corretto e non è un'astensione: resta incluso
in `non_abstained` e nel denominatore di `accuracy_non_abstained`. Un campo `invalid` inatteso
nella sorgente 03.9, un hash errato o conteggi/rapporti incoerenti causano un arresto fail-closed.

## File creati o modificati e documenti pertinenti

Tutti i file del delta committato sono sotto
`/Users/luker/fot-tep/.worktrees/studio2-harness/studio2/fase03/harness/`:

- `metric_adapter.py` — creato; lettore hash-pinned e adapter del documento 03.9 completo;
- `metrics.py` — modificato; aggiunge `non_abstained` all'output nativo 03.10;
- `test_harness.py` — modificato; test del raccordo e delle semantiche limite;
- `SPECIFICA_HARNESS.md` — modificato; mapping, denominatori e invalidità espliciti;
- `CONTRATTO_RACCORDO_METRICHE.md` — creato; contratto autonomo e inventario dei consumer;
- `METRIC_INTERFACE_CANDIDATE.json` — creato; manifest del candidato e impronte;
- `REPORT_RACCORDO_METRICHE.md` — creato; report implementativo;
- `PROMPT_VERIFICA_RACCORDO_METRICHE.md` — creato; incarico per l'altra finestra.

Report e verbali pertinenti:

- report del delta, già committato e preservato perché la sua impronta SHA-256
  `8ab3ac62b9fc066259fb00afb1b8d96a6954d8355a4af1e40559d56b7d201c2e` è registrata nel
  manifest:
  `/Users/luker/fot-tep/.worktrees/studio2-harness/studio2/fase03/harness/REPORT_RACCORDO_METRICHE.md`;
- report storico dell'harness:
  `/Users/luker/fot-tep/.worktrees/studio2-harness/studio2/fase03/harness/REPORT_HARNESS.md`;
- report 03.9 sul main corrente:
  `/Users/luker/fot-tep-chiusura-035-039/studio2/fase03/baseline_numerica/REPORT_BASELINE_NUMERICA.md`;
- verbale indipendente storico 03.9:
  `/Users/luker/fot-tep-chiusura-035-039/studio2/fase03/baseline_numerica/VERIFICA_BASELINE_NUMERICA.md`;
- verbale indipendente del presente delta: non ancora esistente; percorso richiesto
  `studio2/fase03/harness/VERIFICA_RACCORDO_METRICHE.md` nella copia isolata del revisore;
- prompt pronto per tale verifica:
  `/Users/luker/fot-tep/.worktrees/studio2-harness/studio2/fase03/harness/PROMPT_VERIFICA_RACCORDO_METRICHE.md`.

Il presente file è una consegna separata perché il report implementativo è già vincolato dalla
propria impronta nel manifest. Non ne modifica byte o significato.

## Controlli già eseguiti

- `MetricTests`: 9/9 PASS.
- Suite baseline 03.9 sul main `c486eee`: 10/10 PASS.
- Confronto esaustivo fra `baseline.py::metric`, adapter e `three_numbers`: 12.341/12.341
  configurazioni PASS per `total=0..40`, con identità dei valori numerici copiati.
- Verifica delle impronte elencate in `METRIC_INTERFACE_CANDIDATE.json`: 7/7 PASS.
- `python3 -m py_compile` sui moduli interessati: PASS.
- `git diff --check` sul range del candidato: PASS.
- Suite protocollo/guardie/harness dopo il delta: 34 eseguiti, 33 PASS e 1 errore preesistente
  nel test del vecchio pin 03.12.
- `python3 docs/test_explanation.py`: 35 test, gli stessi 14 failure preesistenti e 1 skip prima
  e dopo il delta.

Non sono state rieseguite prove per questa sola richiesta di consegna. I log temporanei della
sessione implementativa erano sotto `/tmp` e non sono dipendenze né artefatti committati.

## Limiti dei controlli

- Non esiste ancora una verifica indipendente del commit `caf5bfb`; l'esecutore non lo
  autocertifica.
- L'unico errore della suite completa dipende dal fatto che il checkout esterno 03.12 corrente
  non coincide con il vecchio hash pinnato dal candidato storico 03.10. I pin 03.12 erano esclusi
  dal mandato e non sono stati cambiati.
- Non sono stati aperti dati o risultati dei run finali e non è stata misurata alcuna performance.
- Non sono state eseguite chiamate API, simulazioni, inferenze sperimentali o prove endpoint.
- L'adapter è disponibile e testato, ma il suo collegamento ai futuri artefatti finali resta
  subordinato a manifest e impronte congelati nel flusso completo 03.10.

## Stato Git finale di questa consegna

Stato osservato subito prima della creazione di questo file: branch pulito a `1ac06eb`, con gli
otto file elencati sopra già committati nei commit `caf5bfb` e `1ac06eb`.

Stato dopo la creazione del presente documento:

- **committati:** gli otto file del delta e della prima consegna elencati sopra;
- **modificati ma non committati:** nessuno;
- **non tracciati:** soltanto
  `/Users/luker/fot-tep/.worktrees/studio2-harness/studio2/fase03/harness/CONSEGNA_RACCORDO_METRICHE_03_10.md`, cioè questo report;
- **staged:** nessuno.

Per esplicita richiesta, questa consegna non viene aggiunta all'indice e non viene committata.

## Integrazione, pubblicazione e congelamento effettivi

- **Delta metriche 03.10:** committato solo sul branch locale; non integrato in `main`, non
  pubblicato e non congelato.
- **Harness 03.10 complessivo:** ancora aperto; `HARNESS_FREEZE.json` resta lo snapshot pending
  del candidato storico `5116087` e non rappresenta il nuovo delta.
- **Baseline 03.9:** pacchetto e dati già integrati/pubblicati secondo la consegna 03.9, ma
  `BASELINE_FREEZE_rev003.json` ha `effective=false`; la sottofase non è dichiarata chiusa.
- **Freeze/tag:** nessun tag creato o spostato in questo lavoro.
- **Walkthrough:** non aggiornato, come richiesto fino all'OK indipendente.

## Residui, dipendenze e prossimo passo

1. Aprire una finestra realmente indipendente sul commit tecnico esatto `caf5bfb`, usando
   `PROMPT_VERIFICA_RACCORDO_METRICHE.md`; il revisore deve registrare modello, provider,
   reasoning se esposto, ID task/sessione, data, worktree e commit.
2. Acquisire il verbale e la sua impronta senza riscrivere il report già sigillato. In caso di
   NON OK, correggere soltanto i rilievi e richiedere una riverifica del nuovo delta.
3. Solo dopo l'OK, aggiornare i record di stato pertinenti e valutare un commit selettivo della
   consegna/verbale; il walkthrough resta successivo all'OK.
4. La finestra orchestratrice potrà poi pianificare l'integrazione del delta nel main aggiornato,
   senza merge implicito del vecchio branch divergente.
5. Per l'efficacia del freeze 03.9 resta inoltre la dipendenza dalla raggiungibilità in main dei
   sorgenti 03.6 e dai controlli/tag successivi previsti dal manifest rev. 3.

Il mapping delle metriche non richiede una nuova decisione dell'autore: è già fissato dalle
specifiche. Restano fuori da questo incarico e ancora da coordinare per l'harness complessivo D9,
configurazione/qualificazione endpoint e modelli, ordine di presentazione delle label, pin 03.12,
input completi, piano statistico e autorizzazioni del pilot.
