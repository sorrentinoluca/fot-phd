# Report della sotto-fase 03.15 — sezioni comuni del paper

Data: 2026-09-14. Profilo: decisionale/redazionale, ragionamento esteso. Branch dedicato
`codex/studio2-paper-sections`, base `origin/main` al commit `46c0b62`. Nessuna chiamata a modelli
linguistici, nessuna simulazione e nessun risultato del nuovo studio prodotto o anticipato.

## 1. Riassunto e risultati

È stata costruita una mappa editoriale e sono state redatte cinque sezioni per lo scenario Q8 —
otto agenti e otto fault — riusabili nei rami di modello previsti da D9: related work, metodo,
verbalizzatore/evidence, protocollo e threats. Le differenze di modello sono confinate in blocchi
`VARIANTE`; scelte ed esiti non disponibili sono marcati `[DECISIONE: …]` e `[RISULTATO: …]`.

| Sezione | Stato | Aperture residue |
| --- | --- | --- |
| Related work | scritta | conversione futura alle citazioni IEEE; nessun risultato |
| Metodo | scritta | gate D9, identità/configurazione del modello e producer alternativo solo nel ramo D9.2 |
| Verbalizzatore/evidence | scritta sulla base disponibile | soglia numerica e FAR omessi; risultati di conformità assenti; integrazione `normal_dev` dopo 03.9 |
| Protocollo | scritto nella parte congelata alla base | D2, statistica, OOD, D11, politica R, modello, endpoint osservati e ruoli di `normal_dev` dopo 03.9 |
| Threats | scritta | impatto empirico del modello, audit e canary come segnaposto |

Le bozze non rivendicano l'invenzione di FoT, della verbalizzazione o degli artefatti strutturati;
non sostengono privacy, efficienza, generalità cross-model, scalabilità di rete o superiorità alle
baseline numeriche. I due soli numeri di esito storico compaiono come motivazione con la formula
prescritta «dichiarato descrittivo».

## 2. File toccati

- `studio2/fase03/paper_sections/PIANO_SEZIONI.md` — mappa, fonti, stato, segnaposto e varianti.
- `studio2/fase03/paper_sections/related_work.md` — related work per filoni e claim esclusi.
- `studio2/fase03/paper_sections/method.md` — FoT, agenti, condizioni, local-first, pseudolabel e schema.
- `studio2/fase03/paper_sections/verbalizer.md` — pipeline evidence, firma 697-D, neutralità e provenienza.
- `studio2/fase03/paper_sections/protocol.md` — dati, separazione dei ruoli, endpoint, ipotesi e controlli.
- `studio2/fase03/paper_sections/threats.md` — threats statistiche, strutturali, esterne e di modello.
- `studio2/fase03/paper_sections/lint_paper_sections.py` — lint minimale delle cinque bozze.
- `studio2/fase03/paper_sections/REPORT_PAPER_SECTIONS.md` — report di chiusura della sotto-fase.
- `studio2/PROVENIENZA.md` — unica sezione nuova in coda per la sotto-fase 03.15.

Non sono stati toccati piano, walkthrough, `docs/letteratura.md`, `docs/paper/`, `phase_b/`, `code/`,
`protocol.py`, `run_pilot.py`, `prepare_gate.py` o gli schema esistenti.

## 3. Modello e profilo

La sotto-fase è stata eseguita con `gpt-5.6-sol`, finestra
`01a09cd4-51f2-7240-bbab-20e92e8bb993`, come accertato dal verbale preliminare tramite i metadati
della sessione. È un'attività decisionale/redazionale con ragionamento esteso. Il lint e i controlli
Git sono attività implementative locali; non sono stati delegati a modelli esterni.

La verifica preliminare è stata svolta in una finestra distinta ma ancora con `gpt-5.6-sol` e ha
emesso `NON OK`. Le correzioni richieste sono state applicate, ma una conclusione indipendente
richiede una nuova verifica del commit corretto con un modello diverso da `gpt-5.6-sol`.
[Fonte: `VERIFICA_PAPER_SECTIONS.md`, verifica preliminare del commit `c63864b`]

## 4. Fuori perimetro

Restano fuori risultati, abstract, conclusioni, figure e impaginazione finale. Le bozze non sono
state spostate in `docs/paper/`: quella cartella è «Materiale del paper» e la collocazione richiede
una decisione dell'autore dopo la verifica indipendente.

Non è stata modificata la letteratura. I seguenti riferimenti restano una lista per
`Letteratura_LLM`, senza essere citati come fonti già verificate del corpus in queste bozze:

- Tango (1998), test di equivalenza/non inferiorità per proporzioni appaiate;
- Maurer, Hothorn e Lehmacher (1995), ipotesi ordinate a priori;
- Westfall e Krishen (2001), fixed-sequence e gatekeeping;
- Clopper e Pearson (1934), intervalli binomiali esatti;
- Kish (1965), effetto di disegno da correlazione intra-cluster;
- ICH E9 (1998), convenzione sul livello unilaterale di non inferiorità;
- McMahan et al. (2017), riferimento canonico per FedAvg richiesto dal protocollo.

Hoeffding (1963) e Bahadur–Savage (1956), aggiunti nella revisione successiva del piano statistico,
sono anch'essi esterni secondo la sua §17 e vanno verificati prima che il test proposto entri nella
bibliografia finale; non erano compresi nella lista originaria dei sei riportata dal report 03.8.

### Apertura residua dovuta alla base precedente alla revisione 7

Il branch 03.15 è nato da `origin/main` a `46c0b62`, prima della revisione 7 del piano al commit
`a572d1c`. Di conseguenza, `protocol.md` descrive la separazione fra sviluppo, calibrazione e test
senza includere il lotto Normal di sviluppo `normal_dev`; `verbalizer.md` non dichiara ancora che
anche le evidence Normal di sviluppo attraversano la trasformazione congelata N1–N5/soglie V2
sotto U3. È un residuo temporale registrato, non un difetto delle bozze rispetto alla loro base.

L'integrazione va eseguita quando il lotto esiste, usando come fonti il piano revisione 7 §6.2 e
`SPECIFICA_NORMAL_DEV.md` della sotto-fase 03.9. In quel momento andranno aggiunti: ruolo esclusivo
di sviluppo per prototipi, esempi locali e baseline; divieto di fit, calibrazione, verifica FAR e
test; assegnazione pre-generazione; distinzione fra finestre e repliche indipendenti; dipendenza U3
dalla coppia N1–N5/V2. Fino ad allora non si anticipano in `protocol.md` o `verbalizer.md` dettagli
che la specifica 03.9 deve attestare.

## 5. Decisioni ancora necessarie

1. Conservare Q8 come nome dello scenario e chiudere il gate D9: Qwen-2.4T se disponibile e promosso
   dal pilot; altrimenti Qwen-27B dopo pilot positivo con Terra alternativo solo nel producer-swap;
   se anche Qwen-27B fallisce, scegliere fra Terra-only e una submission successiva.
2. Confermare o modificare le proposte 03.8: D2, margine *m*, α, gerarchia, test locali, OOD, D11,
   politica R, seed e soglie GO/NO-GO.
3. Completare la verifica indipendente di 03.5 prima di inserire valore della soglia e FAR.
4. Pubblicare il tag dello schema 03.12 se non è già stato pubblicato al momento dell'integrazione.
5. Eseguire risultati, baseline, producer-swap, sonda OOD, conformità e ablazioni prima di sostituire
   i segnaposto `[RISULTATO]`.
6. Decidere se e quando promuovere le bozze in `docs/paper/`.
7. Avviare `Letteratura_LLM` per i riferimenti elencati in §4.
8. Dopo la produzione del lotto 03.9, integrare `normal_dev` in `protocol.md` e `verbalizer.md` dalle
   fonti indicate nell'apertura residua, quindi rieseguire il lint.

## 6. Verifiche

Baseline prima delle modifiche: `python3 docs/test_explanation.py` → 35 test, 14 fallimenti e un
test skipped. Dopo le modifiche: stesso esito, 35 test, 14 fallimenti e un test skipped; tutti i
fallimenti sono preesistenti e il test non copre queste bozze.

`python3 studio2/fase03/paper_sections/lint_paper_sections.py --corpus docs/letteratura.md` → cinque
file controllati, zero segnalazioni. Il lint controlla paragrafi numerici senza fonte, marcatori
bibliografici senza `docs/letteratura.md` e sigla §14.x, un insieme esplicito di citazioni contro il
corpus, F-number vicino a `pseudolabel` e parole di primato non autorizzate.

Il verbale preliminare ha rilevato quattro righe vuote finali nel controllo
`git diff --check 46c0b62..c63864b`; sono state rimosse. Sul pacchetto corretto il controllo è stato
rieseguito esplicitamente contro la base `46c0b62` ed è pulito. I nuovi file non introducono link Markdown
interni da risolvere e non creano coppie `.md`/`.html`; la coppia letteratura è rimasta intatta.

## 7. Commit

Il commit sottoposto alla verifica preliminare era `c63864b`, preceduto dalla seguente sequenza:

1. `2baf2e3` — `studio2(paper): pianifica le sezioni comuni del manoscritto`;
2. `1590581` — `studio2(paper): redige le sezioni comuni senza risultati`;
3. `283532f` — `studio2(paper): aggiunge lint e report delle sezioni comuni`;
4. `c63864b` — `studio2(paper): registra il residuo normal_dev`.

Le correzioni conseguenti al verbale preliminare — varianti D9, FedDTPT, audit del report e righe
vuote finali — formano un nuovo commit, il cui hash va registrato dopo la creazione.

## Fonti lette e costo

Letti: prompt 03.15; `Prompt_LLM.md`; `Fase_LLM.md`; MAINTENANCE §1, §2 e §8; piano §0.1, §2,
§5, §8.1–§8.12, §9, §12.5–§12.9 e §13; blueprint §C, §E, §I, §K e bibliografia; letteratura
§14.1–§14.6; walkthrough del primo studio soltanto nelle sezioni operative richieste e nei due
riscontri motivazionali autorizzati; catalogo D1, run fault, 03.5, 03.6, 03.7, 03.8 e 03.12 ai
commit/tag indicati. Costo approssimativo: 55–70 mila token documentali; zero chiamate modello e
zero simulazioni.
