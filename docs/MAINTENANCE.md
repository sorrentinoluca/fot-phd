# Contratto di manutenzione del repository

> **Bozza da correggere.** Le categorie qui sotto sono state dedotte dalla struttura esistente,
> non decise. Correggile: è questo file a comandare, non la struttura attuale.

Da citare nel prompt quando si chiede a un LLM di aggiornare qualcosa in questo repository:

> «Prima di modificare qualsiasi cosa leggi `docs/MAINTENANCE.md` e rispettalo.»

Questo file dice **dove sta cosa**, **chi è la fonte di verità** e **che cosa va tenuto
allineato**. Non elenca i file: gli elenchi marciscono, le regole no. L'unica enumerazione
ammessa è quella delle coppie in sync (§3), che cambia quasi mai.

---

## 1. Categorie

| Categoria | Dove | Fonte di verità | Regola |
| --- | --- | --- | --- |
| **Artefatti congelati** | `phase_b/`, `icl/`, `ablation/`, `tep_*_v2/`, `reproducibility/`, tag git | sé stessi | **Non si modificano mai.** Se un numero nella documentazione non torna, si corregge la documentazione. |
| **Documentazione narrativa** | `docs/fot_walkthrough*` | gli artefatti congelati | Ogni numero deve essere ricavabile da un artefatto. Coppie `.md`/`.html` da aggiornare insieme (§3). |
| **Materiale del paper** | `docs/paper/` | — | Blueprint e piano sperimentale del paper futuro. Non è documentazione del processo. |
| **Letteratura — analisi** | `docs/lit_review/` | — | Solo rassegne, gap analysis, analisi comparative. Niente piani, niente paper. |
| **Letteratura — paper** | `papers/` | — | Solo paper. Un paper in una copia sola: `.pdf` + `.md` + `_images/`. Le due eccezioni — manca il `.md`, manca il `.pdf` — sono ammesse ma vanno **dichiarate** nella riga di `papers/README.md` (§6). |
| **Letteratura — archivi importati** | `papers/archive/<nome>_<AAAA-MM>/` | sé stessi | Istantanee di lavori precedenti, **non** il corpus corrente. Si lasciano intatte, con README di provenienza. I loro audit restano con il loro corpus. |
| **Audit di processo** | `docs/audits/` | — | Audit prodotti *durante* il processo FoT-TEP. Non ci vanno audit di lavori importati. |
| **Indici** | `README.md`, `DOCUMENTATION_INDEX.md`, `AUDIT_GUIDE.md`, README locali | — | Vedi §4. |
| **Codice e verifica** | `code/`, `docs/test_explanation.py`, `papers/tools/` | — | `test_explanation.py` è il guardiano della documentazione: vedi §5. |
| **Fuori perimetro** | `docs/figures/`, `docs/prompts/`, `docs/archive/`, `_to_delete/` | — | Non toccare se non richiesto esplicitamente. |

## 2. Che cosa non si tocca mai

- Predizioni congelate, freeze manifest, hash, tag git, contenuto di `papers/archive/`.
- I numeri primari. Se un aggiornamento sembra richiedere di cambiarli, **fermarsi e chiedere**.

## 3. Coppie e valori da tenere in sync

**Coppie di file** — vanno modificate nella stessa sessione, mai una sola:

- `docs/fot_walkthrough_conversazione.md` ↔ `docs/fot_walkthrough_conversazione.html`
- `docs/fot_walkthrough_conversazione_v2.md` ↔ `docs/fot_walkthrough_conversazione_v2.html`

### 3.1 Documenti in transizione — leggere prima di toccare i walkthrough

> Sezione **temporanea**: §3.1 e §3.2 si cancellano a promozione avvenuta.

I walkthrough esistono in **due generazioni contemporanee**. La regola per distinguerle è
meccanica: **tracciato da git = canonico, non tracciato = bozza.**

| Documento | Ruolo | git |
| --- | --- | --- |
| `fot_walkthrough_conversazione_v2.md` / `.html` | **riferimento di lavoro** — ogni aggiornamento va qui | non tracciato |
| `fot_walkthrough_v2.html` | **riferimento di lavoro**, versione divulgativa | non tracciato |
| `fot_walkthrough_conversazione.md` / `.html` | generazione precedente, **da non aggiornare e da non usare come fonte** | tracciato |
| `fot_walkthrough.html` | generazione precedente, idem | tracciato |

Le `_v2` sono **il default per il contenuto**: si trattano come se le precedenti non
esistessero. Restano non tracciate da git finché non avviene la promozione (§3.2), quindi
la regola «tracciato = canonico» descrive lo stato del repository, non quale documento
consultare.

Conseguenze operative, da rispettare:

- **Il lavoro nuovo va nelle `_v2`**, sempre.
- **Non promuovere, rinominare o cancellare** una generazione: la promozione la decide
  l'autore, non un aggiornamento di routine.
- **Non allineare le due generazioni fra loro.** Divergono per costruzione: la v2 ha una
  sezione «14 · Letteratura» — unico luogo della letteratura — che la v1 non ha, e ha abbandonato l'impaginazione a `Step N / M`
  per le sezioni §0–§15. Non è un disallineamento da correggere.
- **Non usare la v1 come fonte** per verificare un fatto: la fonte sono gli artefatti
  congelati (§3), mai l'altra generazione.

### 3.2 Checklist di promozione v2 → canonico

Da eseguire quando l'autore decide che la v2 è pronta, **non prima**:

1. ripristinare nella v2 i contenuti che la v1 aveva e la v2 ha perso — verificati al
   2026-09-11: la stringa `C1–C4: 4/4 PASS` (presente in v1, assente in v2);
2. decidere, una per una, le asserzioni che `docs/test_explanation.py` pretende e che
   nessuna delle due generazioni soddisfa: il caveat `non un risultato empiricamente
   misurato` sulla Condizione C, la cifra `0.944444`, l'hash di provenienza `d9bb95c`.
   Per ciascuna: ripristinare nel documento **oppure** togliere l'asserzione, con motivo;
3. promuovere rinominando, così che i percorsi canonici non cambino e nulla vada aggiornato
   altrove;
4. solo dopo, riportare `docs/test_explanation.py` sull'architettura a sezioni: eliminare i
   test che verificano l'impaginazione a step (morta) e conservare quelli che verificano la
   verità rispetto agli artefatti;
5. rieseguire il test e annotare il nuovo numero di partenza al punto 4 di §5;
6. **cancellare §3.1 e §3.2 di questo file**: esaurita la transizione, sono peso morto.

**Contenuti che vivono in più documenti.** Non sono coppie, sono *insiemi*: una modifica
di contenuto va propagata a tutti i membri, che hanno forma diversa e non sono
allineabili meccanicamente.

| Contenuto | Dove vive |
| --- | --- |
| **Letteratura — luogo unico** | `fot_walkthrough_conversazione_v2.md` §14 ↔ `fot_walkthrough_conversazione_v2.html` §14 (coppia, da allineare) |

> Nessun altro file contiene letteratura. `fot_walkthrough_v2.html` **rimanda** alla §14
> e non va riempito di nuovo; `docs/lit_review/` conserva le analisi di supporto che
> alimentano la §14, non un corpus parallelo; `docs/archive/lit_review_2026-09/` è
> un'istantanea chiusa. Se un lavoro nuovo va aggiunto, si aggiunge in §14 e basta.

**Le categorie di §14.1 sono definite nel walkthrough, non qui.** Aprirne una nuova non cambia
le categorie di §1 né le coppie in sync: cambia il contenuto di un documento che è già in sync.
Quello che questo file impone è che le due forme portino **lo stesso insieme di categorie, nello
stesso ordine, con gli stessi conteggi**, verificato sul contenuto e non a occhio (§5). L'elenco
aggiornato sta in §14.1, non qui: duplicarlo significherebbe farlo marcire. Ultima apertura:
2026-09-11, due categorie — «Diagnosi e monitoraggio di processo centralizzati su TEP» e
«Rilevamento di anomalie e soglie statistiche» — per i lavori che condividono il banco di prova
senza toccare nessuno dei quattro assi.

**Valori che compaiono in più documenti** — se ne cambia uno, si cercano tutte le occorrenze
prima di chiudere. Fonte di verità: l'artefatto congelato, mai un altro documento.

| Valore | Riferimento |
| --- | --- |
| Exp1 locally-unseen: A 0/36 · B 31/36 (86,11 %) · E 3/36 | `phase_b/final_evaluation/` |
| Exp2 Qwen: A 0/36 · B 34/36 (94,44 %) · E 1/36 | `phase_b/exp2/qwen/` |
| Exp3_V2: A 0/72 · B 68/72 (94,44 %) · E 4/72 | tag `exp3-v2-results-frozen-001` |
| Baseline numerica same-task: 36/36 unseen (100 %) | `phase_b/baselines/c02b_shared_numeric_prototypes/` |

## 4. Regole per gli indici

- Un README contiene **solo ciò che `ls` non dice**: DOI, venue, disambiguazioni fra omonimi,
  provenienza, trappole note. Elenchi di nomi di file: da cancellare, non da aggiornare.
- `DOCUMENTATION_INDEX.md` mappa **cartelle**, non file.
- Un avvertimento che serve a chi apre una cartella sta **in quella cartella**, non in un indice.

## 5. Definizione di «fatto»

Un aggiornamento è concluso solo quando:

1. la coppia `.md`/`.html` è allineata (§3), verificata sul contenuto, non a occhio;
2. i link interni risolvono (anchor esistenti, percorsi esistenti);
3. se un file è stato spostato o rinominato: cercati **tutti** i riferimenti, inclusi quelli
   dentro `.py`, e aggiornati;
4. `python3 docs/test_explanation.py` non ha **più** fallimenti di prima (annotare il numero
   di partenza: al 2026-09-11 sono 14, preesistenti e relativi ai walkthrough v1);
5. l'indice pertinente è aggiornato solo se è cambiata la **struttura**, non a ogni file.

## 6. Procedura: nuovi paper in `papers/`

Da eseguire ogni volta che entrano lavori nuovi nel corpus. I passi 1 e 3 non
sono opzionali: senza il primo un paper entra con metadati plausibili e nessuno
se ne accorge; senza il terzo la letteratura si sdoppia.

0. **Quanto leggere — regola di costo.** I `.md` dei paper pesano fra 36 e 208 KB:
   leggerne uno per intero costa quanto tutto il resto della procedura. Scala di
   lettura, dal più economico:

   | Ti serve | Leggi |
   | --- | --- |
   | Il titolo | il **nome del file**, che è la chiave di ricerca. **Non la prima intestazione del `.md`**: su una quarantina di conversioni una dozzina apre con il nome della rivista o un'etichetta del convertitore — «Journal of Process Control», «ISA Transactions», «Highlights», «Article», «processes» — e non col titolo. `head -5 file.md` serve al più a leggere rivista e anno, non a identificare il lavoro |
   | Autori, anno, venue, DOI | **il catalogo**, non il file |
   | L'abstract, per classificare | il catalogo; se non lo restituisce, `head -c 2500 file.md` |
   | Contenuto, metodo, risultati | il `.md` **per intero — solo se il lavoro è 🟢** e deve avere una scheda in §14.2 |
   | Le figure | il PDF, solo se davvero necessarie |

   Il PDF non si apre per catalogare: serve solo se la conversione `.md` è
   illeggibile o se devi guardare una figura. Il `.md` è sempre la prima scelta.

1. **Metadati, prima di tutto.** Verifica autori, anno, venue e DOI sui cataloghi
   (OpenAlex, Crossref, arXiv), usando il nome del file come chiave di ricerca.
   **Non dedurre, non completare a memoria.** Se un dato non si trova, scrivilo
   come `—`. Il nome del file è un buon punto di partenza, non una fonte: è quel
   2% di scarto che il catalogo serve a intercettare. Segnala sempre i titoli che
   non corrispondono a quelli dei cataloghi — capita più spesso di quanto sembri.
2. **`papers/README.md`** — una riga per paper, solo con ciò che `ls` non dice:
   titolo esteso, autori, venue, DOI, disambiguazioni fra omonimi.
3. **§14.1 del walkthrough**, in `.md` e `.html` — aggiungi alla categoria giusta
   con autori, anno e colore di vicinanza (🟢 incide sul disegno o delimita un
   claim · 🟡 condivide un asse · 🔴 sfondo). Motiva ogni colore in una riga,
   mantieni i due formati allineati e l'ordinamento per vicinanza dentro la
   categoria.
4. **Se è 🟢** — scheda estesa in §14.2 nel formato delle altre: descrizione, poi
   *Somiglianza / Differenza / Implicazione*. Poi verifica se tocca §14.4
   (perimetro), §14.5 (lavori più vicini), §14.6 (tenuta della novità) o §14.7
   (priorità bibliografica).
5. **Se delimita un claim** — aggiorna `docs/paper/FoT_TEP_paper_blueprint.html`:
   corrente E del §2 e tabella dei riferimenti, con lo stato di verifica.
6. **Chiusura** — §5 di questo file: parità MD/HTML verificata sul contenuto,
   link risolti, `docs/test_explanation.py` non peggiorato.

**Conversioni `.md` senza PDF.** Sono ammesse, ma vanno dichiarate: i riferimenti
alle immagini restano rotti e il lavoro non è rileggibile in originale. Annotalo
nella riga di `papers/README.md`, come già fatto per `papers/archive/`.

**PDF senza conversione `.md`.** È il caso simmetrico e va dichiarato allo stesso modo:
il testo non è ricercabile con `grep`, il lavoro non si legge fuori dal PDF e l'unico modo
di catalogarlo è il catalogo. Controllalo esplicitamente a ogni ingresso — un `.pdf` senza
`.md` non si nota scorrendo l'elenco dei `.md`.

**Prompt minimo da usare:** «Ho aggiunto nuovi paper in `papers/`. Applica la
procedura §6 di `docs/MAINTENANCE.md` e dimmi cosa hai cambiato.»

Se i paper nuovi sono molti, la verifica dei metadati si delega bene a un
sottoagente: sono interrogazioni indipendenti, e torna indietro solo la tabella.

## 7. Manutenzione di questo file

Si aggiorna quando cambiano le **categorie** o le **coppie in sync**, non quando si aggiunge
un file. Se serve modificarlo a ogni commit, è scritto male.
