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

- `docs/letteratura.md` ↔ `docs/letteratura.html`
- `docs/fot_walkthrough_conversazione_studio2.md` ↔ `docs/fot_walkthrough_conversazione_studio2.html`
- `docs/fot_walkthrough_conversazione_v2.md` ↔ `docs/fot_walkthrough_conversazione_v2.html` *(primo studio: record, si tocca solo per correzioni)*
- `docs/fot_walkthrough_conversazione.md` ↔ `docs/fot_walkthrough_conversazione.html` *(prima generazione del primo studio, chiusa)*

### 3.1 Mappa dei documenti e loro ruolo

> Sostituisce, dal **2026-09-12**, le vecchie §3.1 e §3.2 sulla «transizione fra generazioni».
> Quella transizione non avverrà: il primo studio **non verrà citato nel paper**, quindi la v2
> non va promossa a canonico. Resta come record.

| Documento | Ruolo | Si aggiorna? |
| --- | --- | --- |
| `fot_walkthrough_conversazione_studio2.md` / `.html` | **Studio 2 — documento di lavoro.** Si aggiorna fase per fase | **sì**, è qui che si scrive |
| `fot_walkthrough_studio2.html` | Sintesi divulgativa dello studio 2 | sì, quando c'è qualcosa da sintetizzare |
| `letteratura.md` / `.html` | **Corpus bibliografico, luogo unico.** Non appartiene a nessuno studio | **sì**, procedura §6 |
| `fot_walkthrough_conversazione_v2.md` / `.html` | **Primo studio: record.** Base consultabile per lo studio 2, non fonte del suo disegno | solo correzioni |
| `fot_walkthrough_v2.html` | Sintesi divulgativa del primo studio | solo correzioni |
| `fot_walkthrough_conversazione.md` / `.html`, `fot_walkthrough.html` | Prima esposizione del primo studio. Conserva lo **strato operativo** che la v2 ha perso: nomi di campo del testo neutrale (§9), contabilità byte/token (§29), definizioni statistiche (§6, §8) | no |

**Il primo studio è consultabile, non citabile.** Le due esposizioni — `conversazione` e
`conversazione_v2` — descrivono lo **stesso** esperimento: la prima segue la costruzione passo
passo in 36 sezioni, la seconda la riorganizza in 16 per un lettore. La v2 **non è un
sovrainsieme**: mancano gli identificatori di caso (`PBH-*`, `EXP3V2-*`, `CLS-*`, `LKP-*`), il
registro critiche `C01–C18` e lo strato operativo elencato sopra. Chi cerca *come è stato fatto*
guarda la prima; chi cerca *che cosa è risultato* guarda la seconda; chi progetta lo studio 2 non
guarda né l'una né l'altra, ma il piano e i registri di decisione.

⚠️ **Tre sigle in sospeso.** Il piano cita `C06`, `C07` e `C18`, che vengono dal registro
`C01–C18` presente solo in `fot_walkthrough_conversazione.md` §33. Vanno riportate per esteso nel
piano o rinumerate, altrimenti restano riferimenti appesi.


**Contenuti che vivono in più documenti.** Non sono coppie, sono *insiemi*: una modifica
di contenuto va propagata a tutti i membri, che hanno forma diversa e non sono
allineabili meccanicamente.

| Contenuto | Dove vive |
| --- | --- |
| **Letteratura — luogo unico** | `docs/letteratura.md` ↔ `docs/letteratura.html` (coppia, da allineare) |

> **Spostata il 2026-09-12.** Il corpus stava nella §14 di `fot_walkthrough_conversazione_v2`;
> ora vive in `docs/letteratura.md` e nella sua replica. La numerazione interna è rimasta
> **14.1–14.7** apposta: decine di riferimenti nel repository citano «§14.1», «§14.2», «§14.5».
>
> Nessun altro file contiene letteratura. I tre walkthrough — primo studio, studio 2 e le
> sintesi divulgative — **rimandano** e non vanno riempiti di nuovo; `docs/lit_review/`
> conserva le analisi di supporto che alimentano il corpus, non un corpus parallelo;
> `docs/archive/lit_review_2026-09/` è un'istantanea chiusa. Se un lavoro nuovo va aggiunto,
> si aggiunge in `letteratura.md` e basta — procedura in §6, prompt pronto in
> `docs/prompts/Letteratura_LLM.md`.
>
> **La letteratura non appartiene a nessuno studio.** Vale per il primo, per lo studio 2 e per
> quelli successivi: è la ragione per cui non sta più dentro un walkthrough.

**Le categorie di §14.1 sono definite in `letteratura.md`, non qui.** Aprirne una nuova non cambia
le categorie di §1 né le coppie in sync: cambia il contenuto di un documento che è già in sync.
Quello che questo file impone è che le due forme portino **lo stesso insieme di categorie, nello
stesso ordine, con gli stessi conteggi**, verificato sul contenuto e non a occhio (§5). L'elenco
aggiornato sta in §14.1 di `letteratura.md`, non qui: duplicarlo significherebbe farlo marcire. Ultima apertura:
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
3. **§14.1 di `docs/letteratura.md`**, e la stessa riga nella replica `.html` — aggiungi alla categoria giusta
   con autori, anno e colore di vicinanza (🟢 incide sul disegno o delimita un
   claim · 🟡 condivide un asse · 🔴 sfondo). Motiva ogni colore in una riga,
   mantieni i due formati allineati e l'ordinamento per vicinanza dentro la
   categoria.
4. **Se è 🟢** — scheda estesa in §14.2 di `letteratura.md` nel formato delle altre: descrizione, poi
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

**Prompt pronto:** `docs/prompts/Letteratura_LLM.md`, che contiene anche i controlli che questa
procedura non copre (riconciliazione `papers/` ↔ §14.1, criteri di colore, formato scheda).
In alternativa, il minimo indispensabile: «Ho aggiunto nuovi paper in `papers/`. Applica la
procedura §6 di `docs/MAINTENANCE.md` e dimmi cosa hai cambiato.»

Se i paper nuovi sono molti, la verifica dei metadati si delega bene a un
sottoagente: sono interrogazioni indipendenti, e torna indietro solo la tabella.

## 7. Manutenzione di questo file

Si aggiorna quando cambiano le **categorie** o le **coppie in sync**, non quando si aggiunge
un file. Se serve modificarlo a ogni commit, è scritto male.
