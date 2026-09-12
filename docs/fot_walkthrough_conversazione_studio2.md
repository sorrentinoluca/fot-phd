# Studio 2 — walkthrough

> **Documento vivo, a scheletro.** Si aggiorna **fase per fase**: si lavora su una fase, si
> documenta qui, si passa alla successiva. Stato al **2026-09-12**: nessuna fase ancora
> documentata. Finché una sezione resta vuota, **la fonte autorevole è il piano**, non questo file.

| Ruolo | File |
| --- | --- |
| Documento lungo (questo) | `fot_walkthrough_conversazione_studio2.md` |
| Replica web, da tenere allineata | `fot_walkthrough_conversazione_studio2.html` |
| Sintesi divulgativa | `fot_walkthrough_studio2.html` — rimanda, non duplica |
| Letteratura | [`letteratura.md`](letteratura.md) — luogo unico, non si copia qui |
| Primo studio | `fot_walkthrough_conversazione_v2.md` — **record**, non fonte per questo disegno |

**Perché la numerazione salta da 1 a 13.** Le sezioni §2–§12 sono riservate alle fasi, che si
aggiungeranno man mano. §13 e §14 stanno dove stavano nel primo studio, così i riferimenti
«§13» e «§14» conservano lo stesso significato in entrambi gli studi.

---

## 0 · Fonti autorevoli e precedenze

Da rispettare finché questo documento non descrive una fase di persona.

| Ambito | Fonte | Nota |
| --- | --- | --- |
| Disegno generale | `paper/FoT_TEP_Review_Piano_Sperimentale.md` §§8–11, §13 | la revisione corrente è la 6 |
| Decisioni non ancora congelate | idem, §0.1 | prima cosa da guardare |
| Calibrazione delle soglie | `lit_review/DECISIONE_calibrazione_soglie_fase_B.md` (rev. 18) | **prevale sul piano**: il piano dichiara di non riformularne la decisione. Sette requisiti residui, tre bloccanti |
| Scelta dei descrittori | `lit_review/criteri_scelta_descrittori.md` §5.1 | ⚠️ **non** la §5.5, superata dal piano |
| Feature e pre-impegno su E5 | `lit_review/DECISIONE_SCELTA_FEATURE_fase_A.md` | registro di decisione; il disegno resta autorevole nel piano |
| Ablazione dei descrittori | `../analysis/feature_ablation/FEATURE_ABLATION.md` | |
| Vincoli su cosa è congelato | `MAINTENANCE.md` §1 e §2 | |
| Letteratura | [`letteratura.md`](letteratura.md) | |

**Il ciclo di lavoro di una fase.** `Fase_LLM` → `Verifica_LLM` (altra finestra, altro modello) →
`Documentazione_LLM` → `Commit_LLM`, tutti in [`prompts/`](prompts), con il `README.md` della
cartella che dice quale aprire quando. L'ordine non è negoziabile: **questa sezione del walkthrough
non si scrive prima della verifica indipendente.** Le regole di perimetro, commit e congelamento
sono in [`MAINTENANCE.md`](MAINTENANCE.md) §8.

**I dati del primo studio si leggono, non si ipotizzano.** Sono patrimonio disponibile, non una
storia da raccontare: nel paper si descrivono per quello che sono — configurazione, seed, data di
generazione — senza narrare un esperimento precedente. Ciò che non è sostenibile è farli passare
per generati *per* questo studio. La provenienza resta interna, in `studio2/PROVENIENZA.md`, con la
marca **pre-specificato / post-hoc** di ogni analisi che li usa ([`MAINTENANCE.md`](MAINTENANCE.md) §8.2).

**Da non usare come fonte:** `paper/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md` — è il piano
originale che la review critica, non lo stato corrente; i risultati e la narrazione del primo
studio; `archive/lit_review_2026-09/`.

## 0.1 · Punti aperti — da risolvere, non da aggirare

Nessuno dei tre si risolve dentro una singola sessione di lavoro: richiedono una decisione
dell'autore. Restano qui finché non sono chiusi, con la data in cui sono stati registrati.

| # | Punto aperto | Perché blocca | Chi decide | Registrato | Decisione da chiudere in |
| :---: | --- | --- | --- | --- | --- |
| 1 | **Sigle `C06`, `C07`, `C18`** citate dal piano sperimentale | Vengono dal registro critiche `C01–C18`, che esiste **solo** in `fot_walkthrough_conversazione.md` §33 — la prima esposizione del primo studio, che non è fonte. Finché restano così sono riferimenti appesi a un documento che nessuno deve usare | riportarle per esteso nel piano **oppure** rinumerarle | 2026-09-12 | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` §0.1 — **non** il piano BIGDATA2026, che §0 esclude dalle fonti autorevoli |
| 2 | **Quali dati del primo studio lo studio 2 riusa davvero** | Se sono solo i run Normal per la calibrazione è una cosa; se sono anche gli insight o le soglie congelate è un'altra, e cambia quanto dello **strato operativo** va recuperato dalla prima esposizione (schema del testo neutrale §9, contabilità byte/token §29, definizioni statistiche §6 e §8) | autore | 2026-09-12 | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` §0.1, più un registro in `docs/lit_review/` se la selezione del riuso richiede motivazione per singolo dato |
| 3 | **Perimetro del codice della Q8** | La terza metrica di §8.5, il cap sulla lunghezza dello schema, l'estensione a 8 agenti e il derangement a 7 pseudolabel richiedono tutti di scrivere dentro `phase_b/`, che [`MAINTENANCE.md`](MAINTENANCE.md) §1 dichiara **congelato**. Nessuna sessione può decidere da sola di scriverci | aprire un perimetro nuovo (`phase_b/q8/`) **oppure** dichiarare quale parte di `phase_b/` è harness riutilizzabile e quale è artefatto — in entrambi i casi è una modifica a §1 | 2026-09-12 | `docs/MAINTENANCE.md` §1 (separato tra harness riutilizzabile e artefatto) |

*Registrati il 2026-09-12. Quando uno si chiude, va tolto da qui e la decisione va scritta dove
compete: nel piano, in un registro di `lit_review/`, o in `MAINTENANCE.md` §1.*

---

## 1 · Introduzione

*Scheletro. Ogni voce dice dove sta oggi la fonte; il testo si scrive quando la fase relativa
è conclusa.*

- **Le fasi dello studio 2** — l'elenco completo è in [§2–12](#2–12--fasi) qui sotto; questa voce ne dà
  la lettura in una riga e segnala che l'ordine dentro §6 è vincolato: preparazione
  indipendente dal modello, capability pilot come gate, produzione insight, congelamento, esecuzione, analisi.
- **Obiettivo e domanda scientifica dello studio 2** — piano §8
- **Che cosa cambia rispetto al primo studio** — e che cosa viene riusato: da decidere e
  scrivere qui, è la voce che manca a tutti gli altri documenti
- **Banco di prova: agenti, guasti, pseudolabel** — piano §8; ⚠️ le pseudolabel sono **nove**,
  non dieci: `Unknown` è il nome dell'astensione, non una classe
- **Condizioni e bracci** — piano §8, incluso il braccio *producer-swap*
- **Popolazione, endpoint e contrasti** — piano §8.5
- **Protocollo di valutazione e criteri di successo** — piano §8.5, §11 (GO/NO-GO)
- **Baseline** — piano §9
- **Che cosa non è ancora congelato** — piano §0.1, più i sette requisiti residui di
  `lit_review/DECISIONE_calibrazione_soglie_fase_B.md`
- **Limiti dichiarati in partenza** — piano §5 (tabella delle critiche) e §12

---

## 2–12 · Fasi

Le fasi non sono un'invenzione di questo documento: vengono da **§6** (attività che si possono
iniziare subito, indipendenti dal modello) e **§7** (esecuzione, tutta subordinata alla
disponibilità di Qwen) del piano sperimentale. Qui sono raggruppate nelle sezioni che
occuperanno, così che ogni sessione di lavoro sappia dove scrivere.

### Sintesi per sezione

| § | Fase | Che cos'è | Fonte | Stato |
| :---: | --- | --- | --- | --- |
| 2 | **Preparazione indipendente dal modello** | Raggruppamento operativo dei 12 cantieri in §6 (ordine da rispettare) | piano §6.1–6.12 | da fare |
| 3 | **Capability pilot** | Il *gatekeeper*: il modello risponde, il JSON passa il parser, il budget di ragionamento tiene, la stabilità regge | piano §7.1 | bloccata dall'API |
| 4 | **Produzione degli insight** | Gli 8×2 insight dai dati di sviluppo, più la libreria completa del producer alternativo per il braccio *producer-swap* | piano §7.2 | dopo il pilot |
| 5 | **Congelamento del protocollo** | Solo dopo il pilot, mai prima | piano §7.3 | dopo il pilot |
| 6 | **Esecuzione dello studio finale** | Tutte le inferenze A, B-LF, E-LF, più swap, OOD, ablation e canary — circa 2.450 chiamate | piano §7.4 | dopo il congelamento |
| 7 | **Analisi e redazione** | Solo a esecuzione completata | piano §7.5 | ultima |
| 8–12 | *riservate* | Spazio per fasi non previste, o per separare l'analisi dalla redazione | — | — |

Dettaglio degli ambiti indicati in §2–6:

1. **§6.1** — Definire i criteri di selezione degli 8 fault
2. **§6.2** — Generare nuovi run di sviluppo
3. **§6.3** — Calibrare soglie sui Normal di sviluppo
4. **§6.4** — Produrre dati strutturati e verbalizzazioni di sviluppo
5. **§6.5** — Definire pseudolabel e permutazioni di E
6. **§6.6** — Scrivere il piano statistico completo
7. **§6.7** — Preparare la baseline numerica
8. **§6.8** — Preparare l'harness API
9. **§6.9** — Generare e congelare i run finali di test
10. **§6.10** — Congelare lo schema degli insight
11. **§6.11** — Implementare la baseline FedAvg
12. **§6.12** — Scrivere le sezioni del paper indipendenti dal modello
13. **§7.1** — Capability pilot su Qwen-2.4T
14. **§7.2** — Produzione insight con Qwen-2.4T
15. **§7.3** — Congelamento protocollo finale
16. **§7.4** — Esecuzione studio finale
17. **§7.5** — Analisi e redazione

⚠️ **Ordine vincolato, non suggerito.** Dentro §6 le dipendenze non sono libere: i criteri di
§6.1 devono congelarsi **prima** che si estraggano gli 8 fault, e le decisioni «meccanicamente
distinto dal catalogo» e «coppia confondibile» sono definite *rispetto a quegli otto*, quindi non
sono lavorabili oggi. Il piano §7 lo dice esplicitamente: il rischio più urgente non è
scientifico, è **temporale**, e si concentra su una sola data — la decisione GO/NO-GO sul modello.

*Una sezione si scrive quando la fase è conclusa, non mentre è in corso: finché è aperta, la
fonte resta il piano.*

---

## 13 · Conferenza

*Work in progress.* Sede, scadenze, formato e vincoli editoriali. Finché è vuota, il
riferimento è il piano e `paper/FoT_TEP_paper_blueprint.html`.

---

## 14 · Letteratura

Il corpus bibliografico **non vive qui**: sta in [`letteratura.md`](letteratura.md)
(replica web [`letteratura.html`](letteratura.html)), che è il **luogo unico** stabilito da
[`MAINTENANCE.md`](MAINTENANCE.md) §3. Vale per entrambi gli studi, e per questo non appartiene
a nessuno dei due walkthrough.

La numerazione interna è invariata: `§14.1` corpus completo (117 lavori), `§14.2` schede estese,
`§14.3` riferimenti metodologici, `§14.4` perimetro consultato, `§14.5` i lavori più vicini,
`§14.6` tenuta della novità, `§14.7` priorità bibliografica.

Quando lo studio 2 avrà implicazioni bibliografiche proprie, si aggiornano **§14.5 e §14.6 in
`letteratura.md`**, non questa sezione.
