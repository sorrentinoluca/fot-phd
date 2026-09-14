from pathlib import Path
import json
W=Path('/Users/luker/fot-tep-verifica-consolidamento-04dee86');O=Path(__file__).parent
I=json.loads((O/'integrity.json').read_text());T=json.loads((O/'checks.json').read_text());S=json.loads((O/'supplement.json').read_text());F=json.loads((O/'preflight.json').read_text())
rows='\n'.join('| `'+x['destination']+'` | '+str(x['bytes'])+' | `'+x['sha256']+'` |' for x in I['acquisitions'])
fails='\n'.join('- `'+x+'`' for x in S['guardian_candidate']['failure_ids'])
archive=T['archive_root']
report='''VERDETTO: OK

# Verifica circoscritta — consolidamento 03.15 e raccordo metriche

**Candidato tecnico verificato:** `04dee86140b3ff18882f9d164beef5ab7bf33e00`.
**ID operativo:** Studio 2 FoT-TEP, Fase 03 — consolidamento locale 03.15 + raccordo minimo 03.9→03.10.
**Data:** 2026-09-14, Europe/Rome; controlli eseguiti dal turno iniziato alle 19:32:50 UTC.

L'OK riguarda soltanto genealogia, conservazione, raccordo documentale, acquisizioni e isolamento
del test mirato del candidato esatto. Non ripete né amplia gli OK scientifici di e82b5a0,
cf79e81, 91a880b, d35b684 o del delta tecnico metriche già verificato. Non autorizza integrazione,
pubblicazione o congelamento e non chiude 03.9, 03.10, 03.15 o Fase 03.
Non sono emersi difetti bloccanti del candidato nel perimetro richiesto. Le osservazioni non
bloccanti e i controlli con esito non-zero sono esplicitati sotto.

## 1. Identità effettiva, indipendenza e copia di verifica

| Voce | Riscontro |
| --- | --- |
| Provider/prodotto del revisore | `openai`, Codex Desktop |
| Modello esposto | `gpt-6-astra` |
| Reasoning esposto | `effort=high` |
| ID sessione | `01a0a0e2-5a0b-7bc3-a111-b41f24734216` |
| Cwd iniziale del runtime | `/Users/luker/fot-tep` |
| Sede effettiva di verifica | `/Users/luker/fot-tep-verifica-consolidamento-04dee86` |
| Branch/HEAD verifica | nessun branch, detached a `04dee86140b3ff18882f9d164beef5ab7bf33e00` |
| Worktree dell'esecutore, solo letto | `/Users/luker/fot-tep-consolidamento-0315-metriche` |
| Branch dell'esecutore | `codex/studio2-consolidamento-0315-metriche` |
| HEAD sorgente osservato | `380d162390048e8a7e9e9884b4e932867e63a821` |

La prova del revisore è il log locale
`/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T19-06-23-01a0a0e2-5a0b-7bc3-a111-b41f24734216.jsonl`,
`session_meta` riga 1 e `turn_context` riga 418. Sono conservati soltanto estratti pertinenti,
non l'intera conversazione. Non si deduce un'identità più precisa di quella esposta.

L'esecutore del consolidamento è collegato direttamente alle chiamate/output che creano il merge
4ba2ad6 e il commit finale 04dee86: sessione `01a0a0b9-fc72-79b1-81b4-a4d5daa38f94`,
`openai`, `gpt-5.6-sol`, `effort=high`. Nel relativo rollout locale
`rollout-2026-09-14T18-22-18-01a0a0b9-fc72-79b1-81b4-a4d5daa38f94.jsonl`, contesto riga 466,
chiamata/output merge righe 569/572, chiamata/output finale righe 873/876. Sono quindi diversi
modello e sessione rispetto al revisore. Il revisore aveva redatto i verbali storici A e B qui
acquisiti: questo incarico ne controlla la conservazione, non costituisce una seconda review
indipendente del loro merito. Non sono stati usati sottoagenti o chiamate a modelli.

**Preflight.** Prima di creare il worktree sono stati letti HEAD, branch, stato, worktree e main
remoto. Il sorgente era pulito. `380d162` ha un unico genitore, esattamente 04dee86, e aggiunge
soltanto consegna e prompt di preparazione: tali due file sono conservati nelle prove come indice
operativo esterno al candidato qualificato. Non si usa il branch principale come base implicita.
Nessun checkout altrui è stato spostato; nessun lock o worktree preesistente è stato riparato.

`origin` è `https://github.com/sorrentinoluca/fot-phd.git`; tracking main e main remoto sono a
`c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`. La lettura remota finale, alle
19:42:12 UTC, conferma main e non restituisce né il branch remoto del consolidamento né il tag
`studio2-fase03-schema-insight-frozen-001`. È un riscontro delle ref interrogate, non una
ricostruzione di ogni operazione remota possibile. Nessuna ref remota è stata modificata.

## 2. Grafo, perimetro e conservazione — ✅

Sono antenati di 04dee86 tutti i riferimenti richiesti:

- base `e82b5a08bf642ad45f77e71832958207beb1181c`;
- 03.15 corretto `10582798eb5a4b52672bfbcb1cc028adcb73e9f1`;
- pacchetto scientifico `d35b684acbfd1f357bc34f3a21cebb18e8a6bea0`;
- metriche minime `3360867751c66a39e819247f86dab8e936f8cbb3`;
- merge `4ba2ad6e4a298411b4f0f7572ad3ef8e55948015`.

Il merge ha esattamente due genitori, nell'ordine **10582798, 3360867**. Dopo il merge la catena
è lineare: 1e4afa8 (63 acquisizioni: cinque verbali e 58 file delle due directory di prova),
8a99df0 (tre consegne successive), d3bc506 (report metriche), 73dc4e5 (record runtime),
04dee86 (tipografia HTML). Hash completi, genitori e percorsi per commit sono in `integrity.json`
e `supplement.json`; il diff dalla base contiene 103 percorsi, tutti riconducibili al perimetro.

| Oggetto | Verifica diretta | Esito |
| --- | --- | --- |
| 17 file paper presenti a d35b684 | stessi blob e stessi byte nel candidato e nel worktree isolato | 17/17 |
| 14 file harness presenti a 3360867 | stessi blob e stessi byte nel candidato e nel worktree isolato | 14/14 |
| `studio2/fase03/evidence` | stesso oggetto tree Git di e82b5a0 | identico |
| `studio2/PROVENIENZA.md` | confronto integrale con 10582798 | byte-identico, §§1–14 conservate |

I 17 file scientifici paper sono distinti dalle consegne e dalle prove successive. Le acquisizioni
in `paper_sections/` includono il NON OK storico, il correttivo C e il suo bundle di prove: i file
Python contenuti in quest'ultimo sono script storici di audit, non nuovi moduli dell'harness.
In `harness/` le sole quattro aggiunte rispetto ai 14 file sono la consegna di acquisizione OK,
il report d'integrazione e i due verbali D/E. Nessun file scientifico viene sostituito.

Il codice Python del package harness resta limitato a `__init__.py`, `common.py`,
`metric_adapter.py`, `metrics.py` e `test_metric_raccordo.py`. Gli import sono stdlib, `.common`
e i tre moduli esplicitamente importati dal test. Nessun vecchio harness completo, pilot,
configurazione, endpoint, input pending, ledger o pin 03.12 è importato. `SPECIFICA_HARNESS.md`
conserva riferimenti al sistema generale escluso (per esempio producer e canary): è un limite
documentale dichiarato, non una dipendenza runtime del package minimo.

## 3. R4, fonti 03.6/03.9 e ripartizione 03.15 — ✅

`SCHEMA_FREEZE.json` è byte-identico al target esclusivo
`3c64390bc4dd58c48cc4e1e388a38989b32b3143`. Verificate **18/18 voci**, dimensione e SHA-256:
10 file del contratto in R4 e nel candidato, più otto fonti ai rispettivi riferimenti storici.
Per sei fonti è stato usato `base_commit=d815ce96d928254de79209f02e11a561445764cd`;
per le due fonti pseudolabel il `source_ref=a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155`.
Il confronto storico non sostituisce la letteratura corrente con quella del manifest.
Il futuro tag resta destinato **soltanto a 3c64390**, mai a 04dee86, al merge o al record successivo.
Nessun test scientifico R4 o tokenizer è stato rieseguito e nessun tag è stato creato.

Le quattro SHA-256 fissate da `CONTRATTO_RACCORDO_METRICHE.md` coincidono con i blob in c486eee
e con il candidato: `baseline.py`, `SPECIFICA_BASELINE_NUMERICA.md`, `INTERFACE_CHECK.json`,
`BASELINE_FREEZE_rev003.json`. Le due impronte 03.6 in `normal_evidence` di quest'ultimo
coincidono con `evidence/extract_evidence.py` e `evidence/leakage.py`: **6/6 riscontri**, senza
estrazioni o valutazioni di risultati. Impronte complete e riferimenti in `integrity.json`.

Le **54 fonti** del registro 03.15 conservano le rispettive impronte, 52 oggetti Git più due
file locali, con questa ripartizione sia a 10582798 sia a 04dee86:

| Categoria | Voci |
| --- | ---: |
| commit antenati | 44 |
| commit locali presenti ma non antenati | 8 |
| fonti locali senza commit nel registro | 2 |

Le otto fonti S08/S08-consegna restano ai pin 6aaa5b3 e 51782e8, esterni all'ascendenza.
H e PROMPT-0315 mantengono `commit: null`: l'acquisizione di copie storiche nelle evidenze non
trasforma retroattivamente quelle voci in fonti committate al loro percorso originario.
Non è richiesta né eseguita l'integrazione della rev. 10.

## 4. R1/R2, walkthrough e stati — ✅ con precisazione tipografica

§4.10 MD coincide con 3360867; §4.15 MD e HTML coincidono con 10582798. La §4.10 HTML prima
di 04dee86 coincide con 3360867. Il nuovo commit cambia soltanto la spaziatura delle tre frecce
del mapping, senza cambiare parole, numeri, link o codice.

**Precisazione sulla consegna/prompt esterni al candidato:** «tre spazi tipografici» è una
descrizione abbreviata inesatta se intesa come conteggio di caratteri. Sono **tre siti di
intervento e sei caratteri U+0020 aggiunti**, uno prima e uno dopo ciascuna freccia. Il confronto
esatto della sottostringa §4.10 e `typography.patch` lo dimostrano. Non è un difetto semantico
o una modifica ulteriore del candidato; in un eventuale nuovo record usare questa formulazione.
Non si richiede di togliere gli spazi necessari alla parità.

Parità normalizzata per blocchi visibili (intestazioni, paragrafi, liste/celle; whitespace
collassato, link letteratura MD/HTML equivalenti): **16/16 blocchi per §4.10**, **15/15 per §4.15**.
Nessun nuovo blocco MD senza corrispondenza HTML rispetto alla sorgente 10582798.
Ordine esplicito: 4.9 → 4.10 → 4.12 → 4.15, coerente con gli anchor e l'indice HTML.
**20 ID HTML univoci; 475/475 link locali** della coppia e di PROVENIENZA risolti per percorso
Git e frammento; zero marker di conflitto. Non sono stati visitati link di rete.

Sono identiche le dieci sezioni precedentemente ancorate di 10582798 (incluse 4.6, 4.9, 4.12,
4.15). Sottraendo dal candidato soltanto la nuova §4.10, il suo rinvio nella sintesi iniziale e
la sua voce d'indice HTML, i due file tornano **esattamente** a 10582798. Ciò copre anche la
conservazione delle altre sezioni, della tabella riassuntiva e della voce §6.12.
`PROVENIENZA` conserva integralmente §§1–14; nessuna rinumerazione o perdita.

R1 distingue correttamente 44/8/2; R2 distingue i 17 file del pacchetto dalle due consegne del
raccordo 03.15 storico. Le successive acquisizioni di prove sono inventariate separatamente,
non presentate come nuovi file scientifici. Restano distinti l'OK storico cf79e81, il nuovo
OK scientifico 91a880b, la sua acquisizione d35b684, il delta R1/R2 e il consolidamento qui verificato.

I testi storici `PENDING` o «non ancora verificato» sono conservati nei record e nelle sezioni
provenienti dai candidati precedenti; i successivi verbali sono acquisiti senza riscriverli.
Non ne viene dedotta una qualificazione dell'harness completo. Il nuovo OK riguarda il raccordo
esatto in prima riga; non anticipa pubblicazione, promozione in `docs/paper`, firma/freeze 03.8,
D9, pin 03.12 o chiusura di sottofase/Fase 03.

## 5. Acquisizioni byte-identiche — ✅

Confrontati **sorgente originale, copia nel worktree dell'esecutore, copia isolata e blob Git**.
Le nove acquisizioni principali coincidono; anche i 58 file delle due directory di evidenza
coincidono, per un totale di **67 percorsi** confrontati con la copia di lavoro dell'esecutore.
Le fonti assolute e le impronte individuali sono in `integrity.json`.

| Destinazione nel candidato | Byte | SHA-256 |
| --- | ---: | --- |
'''+rows+'''

D proviene da `/Users/luker/fot-tep/Claude outputs/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE.md`;
E da `/Users/luker/fot-tep/.worktrees/integrazione-raccordo-metriche/_delivery/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE.md`.
«Byte-identici» significa ciascuno rispetto alla propria sorgente: D ed E sono documenti diversi,
con dimensioni e hash diversi, conservati con nomi di destinazione distinti. D mantiene il limite
esplicito di non indipendenza; E non espone sessione/task, modello preciso o effort verificabili.

| Snapshot/versione | Byte | SHA-256 |
| --- | ---: | --- |
| B comune storico | 17597 | `46185e3d15867253e98f5c9f08df5ab8ed8a6a6643a15d5011079341045514e6` |
| B 03.15 storico | 11046 | `b7398a24f57f18b59be4cd77e40785a286805e619f76eb65d8642f0d941ba607` |
| Consegna viva 03.15 successiva | 11801 | `8f2c1082606eea5554f0213d66a0f8dac5d66adc5ade4d35bca0a832bb4bdb71` |

Il B 03.15 storico non è stato sostituito dalla versione viva. La consegna comune viva coincide
con il suo snapshot da 17.597 byte; la coincidenza non fonde i ruoli dei documenti.

Manifest A: **30/30 voci**; manifest B: **28/28 voci**, dimensioni e SHA-256 corrispondenti al
candidato. Ogni manifest esclude sé stesso. Le directory hanno rispettivamente 30 e 28 file,
incluso il manifest; ciascun inventario include invece il verbale esterno alla directory.
Il manifest B contiene percorsi assoluti della sede storica: la verifica ha applicato una
mappatura esplicita della radice storica al medesimo percorso relativo nel candidato, senza
modificare un byte del manifest. Sono stati controllati anche gli originali, non solo i target
rimappati. È conservato il limite di portabilità del documento storico.

## 6. Identità runtime acquisite — ✅ con limiti preservati

`ACQUISIZIONE_IDENTITA_RUNTIME_CONSOLIDAMENTO_2026-09-14.md` è coerente con le fonti mirate.
Le identità del raccordo comune coincidono con i due JSON storici acquisiti. Per R1/R2 è stato
controllato il rollout locale della sessione `01a0a0e3-c3bd-7523-90ca-b5f28a40461f`:

- session meta riga 1: provider `openai` e ID;
- contesto righe 8 e 421: `gpt-5.6-sol`, `effort=medium`;
- chiamata riga 460, 18:07:33.657Z: creazione del commit nel worktree 03.15;
- output riga 463, 18:07:34.932Z: hash completo 10582798 e genitore 9b6bd64;
- stesso `call_id=call_815jnitmdSVTznzjm8e1EcbA` per chiamata e output.

Il collegamento non è dedotto dal committer o dallo stile. C dichiara sessione Claude
`session_013BLwcitiaqnqjNBLvV2mhH`, modello configurato `claude-opus-4-8`, effort non esposto;
si conserva questo livello di prova dichiarativa. Il solo indice Claude citato dal record
collega D, `session_01CHTctYBYq1nnbumDuHrCsC`, a `/Users/luker/fot-tep`; non dimostra indipendenza.
Per E non è emersa in queste fonti una prova affidabile di ID/effort: il limite è mantenuto,
non colmato con ipotesi e non usato per riscrivere E. L'OK presente non certifica l'identità E.

## 7. Test, isolamento e controlli documentali

Sono state ottenute due copie indipendenti degli oggetti Git tramite `git archive --format=tar`,
senza `.git` e senza symlink. Nessun worktree fratello è stato montato o importato. Percorsi:

- candidato: `'''+archive+'''/candidate`;
- base: `'''+archive+'''/base`.

Python effettivo: `/usr/local/bin/python3`, **3.11.5**. `PYTHONPATH` e `PYTHONHOME` rimossi
nell'ambiente dei processi; `PYTHONDONTWRITEBYTECODE=1`. Gli import e le stringhe del runtime sono
stati ispezionati: niente rete, subprocess, manipolazioni di sys.path o percorsi assoluti di
checkout. I due literal `/` rilevati dall'AST fanno parte di messaggi f-string diagnostici
(`condition/population`, `label/case_id`), non sono accessi al filesystem. Il test scrive soltanto
una fixture temporanea tramite `TemporaryDirectory` e la elimina automaticamente.

| Comando, da ciascuna copia indicata | Risultato | Exit |
| --- | --- | ---: |
| candidato: `python3 -m unittest studio2.fase03.harness.test_metric_raccordo -v` | 9 test, 9 OK, 0 failure, 0 error, 0 skip | 0 |
| candidato: `python3 studio2/fase03/paper_sections/lint_paper_sections.py --corpus docs/letteratura.md` | 5 file, 0 segnalazioni | 0 |
| base e82b5a0: `python3 docs/test_explanation.py` | 35 test, 14 failure, 0 error, 1 skip | 1 |
| candidato: `python3 docs/test_explanation.py` | 35 test, 14 failure, 0 error, 1 skip | 1 |
| `git diff --check 4ba2ad6 04dee86 -- docs/fot_walkthrough_conversazione_studio2.md docs/fot_walkthrough_conversazione_studio2.html` | nessuna segnalazione | 0 |

Il test unitario richiesto include `test_cluster_bootstrap_and_tests`, con **200 iterazioni su
fixture sintetica** e assert tecnici già presenti. È stato eseguito integralmente come richiesto
(9 test); non sono stati avviati bootstrap scientifici sui dati, rianalisi sperimentali o run finali.
Nessuna estrazione, simulazione TEP, inferenza, ricerca bibliografica o chiamata API.
Il lint e i test non qualificano scientificamente i pacchetti o l'harness completo.

**Il guardiano resta FAILED, non PASS.** Sono identici tutti i 14 identificativi di failure,
compresi i subtest, e il singolo skip. Nessun errore di ambiente o nuovo fallimento del candidato.
Gli identificativi conservati in entrambi i log sono:

'''+fails+'''

Skip comune: `TutorialChecks.setUpClass`, motivo `legacy part-1 walkthrough is not present in this checkout`.
Questi esiti storici non sono stati convertiti in PASS né trattati come copertura scientifica.

**Controllo aggiuntivo non-zero.** `git diff --check 4ba2ad6 04dee86 --
studio2/fase03/ACQUISIZIONE_IDENTITA_RUNTIME_CONSOLIDAMENTO_2026-09-14.md` restituisce **exit 2**:
trailing whitespace alle righe 3 e 5. Sono due spazi terminali Markdown che producono ritorni
di riga nell'intestazione. Il controllo non è PASS; la segnalazione è valutata non bloccante
per il raccordo, con testo e metadati invariati, e non giustifica una riscrittura del record.
Nessuna correzione richiesta al candidato per questo punto.

Due tentativi dello script documentale del verificatore si sono fermati su assert della
spaziatura: prima sull'interpretazione letterale «tre spazi», poi su un selettore esteso a tutto
l'HTML. È stato circoscritto il selettore alla §4.10 e verificata la sostituzione esatta in tre
posizioni. Sono problemi del controllo preparato in questa verifica, non test del prodotto
falliti o skip promossi a PASS. Esito completo e script finale conservati.

## 8. Stato finale, prove e residui

Il candidato 04dee86 è conservato: nessun file tracciato corretto, nessun commit, merge, push,
tag o freeze eseguito. Il worktree sorgente resta pulito a 380d162. I worktree sorgente, metriche,
harness e delle precedenti verifiche sono stati soltanto letti. Nella copia isolata sono nuovi e
**non tracciati** esclusivamente questo verbale e `evidenze_verifica_consolidamento_04dee86/`;
nessuna modifica staged o tracciata. La prova finale è `final_preservation.json`.

Le prove conservate comprendono prompt/consegna operativi successivi al candidato, preflight,
script di verifica, inventari blob/SHA-256, mappatura dei manifest, estratti runtime mirati,
diff MD/HTML, risultati documentali, log dei quattro comandi Python e dei diff-check.
`MANIFEST_EVIDENZE.json` registra byte e SHA-256 del verbale e di tutte le prove, escludendo
sé stesso per evitare auto-riferimento. Le directory e i tar temporanei ottenuti da `git archive`
restano nel percorso sopra: hash e dimensioni in `checks.json`; non sono necessari per alterare
o ricostruire il candidato, che resta un oggetto Git esatto.

**Residui fuori perimetro, non sanati dall'OK:** firma/freeze 03.8, D9, qualificazione 122B,
harness completo, pin 03.12, OOD, T5/ledger/calendario, sorgenti rev. 10 esterne all'ascendenza,
raggiungibilità dalla futura base seriale/remota, identità precisa E e fallimenti/skip storici.
A/B, FAR e U3 non sono stati riaperti. Nessuna nuova decisione scientifica dell'autore è richiesta
da questa verifica. Per eventuali integrazione, pubblicazione e congelamento serve un incarico
separato: questo verbale non li autorizza.

**Prossimo passo:** acquisire questo OK come verbale separato del solo 04dee86 e rimettere
all'autore la decisione sulle operazioni successive. Qualunque nuovo delta tecnico/documentale
va identificato separatamente; non estendere automaticamente il presente OK.

Letture: prompt e consegna di consolidamento; MAINTENANCE e instradamento Verifica/Prompt;
record runtime e sole fonti mirate; verbali A/B come baseline conservate, C/D/E per raccordo e
limiti; contratto metriche, manifest R4/03.9/fonti 03.15, cinque file Python per dipendenze,
diff e coppia walkthrough. I pacchetti e le fonti sono stati letti come byte per le impronte,
non riesaminati scientificamente. Costo indicativo di lettura: alcune decine di migliaia di
token; nessuna misura affidabile del consumo fatturato disponibile.
'''
p=W/'studio2/fase03/VERIFICA_CONSOLIDAMENTO_0315_METRICHE.md';p.write_text(report)
print(p, len(p.read_bytes()))
