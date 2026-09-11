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
| **Letteratura — paper** | `papers/` | — | Solo paper. Un paper in una copia sola: `.pdf` + `.md` + `_images/`. |
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

| Documento | Stato | Note |
| --- | --- | --- |
| `fot_walkthrough_conversazione.md` / `.html` | **canonico** | Ciò che oggi vale |
| `fot_walkthrough.html` | **canonico** | |
| `fot_walkthrough_conversazione_v2.md` / `.html` | **bozza** | Sostituirà il canonico quando l'autore lo deciderà |
| `fot_walkthrough_v2.html` | **bozza** | idem |

Conseguenze operative, da rispettare:

- **Il lavoro nuovo va nelle bozze `_v2`**, non nei canonici, salvo richiesta esplicita.
- **Non promuovere, rinominare o cancellare** una generazione: la promozione la decide
  l'autore, non un aggiornamento di routine.
- **Non allineare le due generazioni fra loro.** Divergono per costruzione: la v2 ha una
  sezione «14 · Letteratura» che la v1 non ha, e ha abbandonato l'impaginazione a `Step N / M`
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

## 6. Manutenzione di questo file

Si aggiorna quando cambiano le **categorie** o le **coppie in sync**, non quando si aggiunge
un file. Se serve modificarlo a ogni commit, è scritto male.
