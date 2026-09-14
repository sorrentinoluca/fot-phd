# Prompt per verifica indipendente del raccordo metriche 03.9 → 03.10

```text
Svolgi una verifica indipendente, in sola lettura, del raccordo delle metriche fra baseline
numerica 03.9 e harness 03.10. Non correggere il candidato mentre lo certifichi e non usare la
stessa finestra che lo ha implementato.

Repository: /Users/luker/fot-tep
Worktree proprietario: /Users/luker/fot-tep/.worktrees/studio2-harness
Branch: codex/studio2-harness
Base del delta: 51160872906feaa63c1fda5e9cf6e0fe8538fb16
Candidato implementativo esatto: caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae
Main sorgente 03.9: c486eee95fe24c1e7bf4135ed7cebf01ac2962f1

Prima di verificare, leggi integralmente:
- docs/MAINTENANCE.md;
- docs/prompts/Prompt_LLM.md e docs/prompts/Verifica_LLM.md;
- studio2/fase03/harness/REPORT_RACCORDO_METRICHE.md;
- studio2/fase03/harness/CONTRATTO_RACCORDO_METRICHE.md;
- studio2/fase03/harness/SPECIFICA_HARNESS.md §8;
- dal main c486eee: `studio2/fase03/baseline_numerica/SPECIFICA_BASELINE_NUMERICA.md`,
  `baseline.py`, `INTERFACE_CHECK.json` e `BASELINE_FREEZE_rev003.json` nella stessa cartella;
- /Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/
  DELTA_HARNESS_03_10.md, soltanto per astensione, invalidità e denominatori.

Non fidarti del report. Ricostruisci il contratto dalle fonti e verifica il diff
5116087..caf5bfb. Controlla in particolare:

1. mapping esatto accuracy→accuracy_all, n→total, abstentions→abstained;
2. non_abstained preservato e uguale a total-abstained;
3. invalid=0 ammesso soltanto per la sorgente 03.9 valid-only, che fallisce prima di produrre
   righe invalide;
4. nell'harness generale gli invalidi non sono corretti né astensioni e restano nel denominatore
   di accuracy_non_abstained;
5. null soltanto con denominatore zero e rifiuto fail-closed di campi, conteggi, rapporti,
   strutture o SHA-256 incoerenti;
6. tutte le foglie summary e clusters vengono adattate, senza arrotondamento o sostituzione dei
   tre valori numerici sorgente;
7. nessun consumer effettivo delle metriche è stato omesso;
8. nessuna modifica fuori perimetro a D9, endpoint, modelli, ordine label, pin 03.12,
   run_pilot.py, walkthrough o run finali.

Riesegui almeno:

python3 -m unittest -v studio2.fase03.harness.test_harness.MetricTests

Nel checkout main c486eee riesegui:

python3 -m unittest -v \
  studio2.fase03.baseline_numerica.test_baseline \
  studio2.fase03.baseline_numerica.test_normal_dev_plan \
  studio2.fase03.baseline_numerica.test_extract_normal_evidence

Esegui anche la suite completa dichiarata nel report e il guardiano documentale. È noto prima
della review un errore estraneo nel test del vecchio pin 03.12 e sono noti 14 failure + 1 skip
nel guardiano: confronta identificativi e causa, non trasformarli in PASS e non correggerli in
questo perimetro. Verifica autonomamente l'equivalenza fra baseline.py::metric, adapter e
three_numbers su casi ordinari, astensioni, invalidi e limiti; non limitarti a rieseguire i test
dell'autore.

Non eseguire API, simulazioni, dati test o analisi sui run finali. Non aggiornare il walkthrough,
non creare tag, non fare merge o push e non dichiarare chiuse 03.9/03.10.

Scrivi il verbale in VERIFICA_RACCORDO_METRICHE.md nella tua copia isolata. Prima riga soltanto
"VERDETTO: OK" oppure "VERDETTO: NON OK". Prima dei riscontri registra obbligatoriamente:
- modello esatto e provider/prodotto;
- livello di reasoning, se esposto;
- ID task/sessione o, se non esposto, la dicitura esplicita "non esposto";
- data e timezone;
- percorso della copia isolata;
- commit verificato caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae.

Per ogni punto usa ✅, ⚠️ o ❌, cita file/funzione e prova primaria. Solo dopo i dettagli formula
il verdetto. Un OK vale esclusivamente per questo delta e non è un OK dell'intero harness o della
sottofase. Non committare il verbale: restituiscine percorso e SHA-256 alla finestra proprietaria,
che lo acquisirà separatamente senza presentare l'autore come revisore.
```
