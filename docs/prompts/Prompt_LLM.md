Agisci come un reviewer critico per la letteratura accademica; il tema principale è ML - Federated learning.

**Nota operativa breve.** Questo file non è un secondo contratto di regole: per regole e vincoli
vivi in `docs/MAINTENANCE.md` §8 e viene lì deciso il contratto. Per ogni fase usa sempre il
ciclo `Fase_LLM` → `Verifica_LLM` (altra finestra, altro modello) → `Documentazione_LLM` →
`Commit_LLM`. I dati del primo studio si leggono dagli artefatti con commit e impronta:
non si ipotizzano, non si ricostruiscono da memoria.

Usa come fonte principale `docs/fot_walkthrough_conversazione_v2.md`. Il file `.html` con lo stesso nome ne è la replica web: **non leggerlo**, ha lo stesso contenuto e costa il 50% in più.

`docs/fot_walkthrough_v2.html` è una sintesi divulgativa, utile solo per un'introduzione rapida al metodo. **Non è una fonte bibliografica**: la sua sezione «Letteratura» rimanda a §14 del documento lungo e non contiene il corpus.

Acquisisci conoscenza anche da `docs/paper/FoT_TEP_paper_blueprint.html` (esiste solo in HTML).

docs/fot_walkthrough_conversazione_v2.md, docs/paper/FoT_TEP_paper_blueprint.html

-------------------
Con Claude Code: niente. CLAUDE.md alla radice viene caricato da solo a ogni sessione e rimanda al contratto.
Con Codex o altri LLM, una riga in apertura:
Prima di modificare qualsiasi cosa in questo repository leggi docs/MAINTENANCE.md e rispettalo.
E, quando la richiesta è di modifica, una riga in chiusura:
Al termine elenca i file che hai toccato, riesegui `python3 docs/test_explanation.py` e confronta i fallimenti con il numero di partenza (14 al 2026-09-11, tutti preesistenti). Quel test non copre §14 né i file `_v2`.
Sono due righe perché il resto — cosa è congelato, quali coppie tenere allineate, quali documenti sono bozze, cosa significa «fatto» — sta già nel file. Se un giorno ti accorgi di doverne aggiungere una terza, il posto dove scriverla è MAINTENANCE.md, non il prompt.

Ho aggiunto nuovi paper in `papers/`. Applica la procedura §6 di `docs/MAINTENANCE.md` e dimmi cosa hai cambiato.

------------------
Decisione.  File da citare
«Questa scelta di disegno è difendibile?»  `docs/letteratura.md` §14.2 (le schede estese)
«È davvero nuovo? Cosa posso rivendicare?» `docs/lit_review/FOT_TEP_GAP_ANALYSIS_AND_RELATED_WORK.md` + `docs/letteratura.md` §14.5 e §14.6
«Come lo scrivo nel paper?» docs/paper/FoT_TEP_paper_blueprint.html §2 e la tabella riferimenti
«Questo lavoro è verificato? Che venue ha?» papers/archive/fed_fsl_2026-07/audit/Audit_Nuovi_Prior_Art_Fed_FSL.md — l'unico con verifica sul testo integrale
«Quali esperimenti mancano?» docs/paper/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md

PROMPT VERIFICA LETTERATURA
----------------

Per le implicazioni della letteratura leggi §14.2, §14.5 e §14.6 di `docs/letteratura.md`. Consulta §14.1 solo per verificare se un lavoro specifico è già nel corpus, filtrando sui 🟢.

Per i vincoli leggi `docs/MAINTENANCE.md` §2 (cosa è congelato e non si tocca) e §12 di `docs/fot_walkthrough_conversazione_v2.md` (cosa l'esperimento stabilisce e cosa no).

Dimmi se la scelta che propongo entra in conflitto con uno di questi tre.

-----------------

Leggi integralmente docs/paper/FoT_TEP_Review_Piano_Sperimentale.md. È la fonte autorevole per il nuovo studio Qwen: §8–§11 e §13 descrivono il piano corrente; le sezioni sui piani eliminati spiegano soltanto perché sono stati scartati.
Prima di modificare qualsiasi cosa in questo repository leggi docs/MAINTENANCE.md e rispettalo.
Per comprendere l’esperimento già eseguito, consulta docs/fot_walkthrough_conversazione_v2.md. Usa docs/fot_walkthrough_v2.html soltanto come sintesi introduttiva. Non leggere la replica HTML del documento lungo.
In parallelo esegui una verifica su tutta la letteratura presente nel repo.

Per le implicazioni della letteratura leggi §14.2, §14.5 e §14.6 di `docs/letteratura.md`. Consulta §14.1 solo per verificare se un lavoro specifico è già nel corpus, filtrando sui 🟢.

Per i vincoli leggi `docs/MAINTENANCE.md` §2 (cosa è congelato e non si tocca) e §12 di `docs/fot_walkthrough_conversazione_v2.md` (cosa l'esperimento stabilisce e cosa no).

Dimmi se la scelta che propongo entra in conflitto con uno di questi tre.

In caso di conflitto:

- per la nuova fase prevale la review del piano;
- per risultati e fatti dell'esperimento precedente prevalgono il walkthrough lungo e gli artefatti originali;
- per l'implementazione prevalgono codice, manifest e dati, che devono essere verificati direttamente;
- **per la letteratura prevale `docs/letteratura.md`, che ne è il luogo unico.**

Prima di proporre modifiche, restituisci un riepilogo breve composto da: disegno corrente, decisioni già congelate, decisioni ancora aperte, attività escluse e principali rischi. Non modificare file.

Se hai modificato qualcosa: elenca tutti i file che hai toccato, riesegui `python3 docs/test_explanation.py` e confronta i fallimenti con il numero di partenza — **al 2026-09-11 sono 14, tutti preesistenti**. Se possibile eseguilo anche *prima* di modificare, per avere il tuo numero di partenza.

**Attenzione: quel test copre solo i walkthrough della generazione precedente. Non verifica §14 né i file `_v2`. Un risultato invariato non è prova che il tuo lavoro sia corretto.**

------

# Contesto operativo — progetto FoT-TEP

Lavori su un repository di ricerca. La documentazione è ampia e leggerla tutta
costa più del compito: la regola è leggere il minimo che risponde, e dichiararlo.

## Regola di costo

Prima di aprire qualsiasi file, stabilisci a quale tipo appartiene la richiesta e
apri solo ciò che la tabella indica. Se non basta, allarghi — motivando.

**Non leggere mai `papers/*.md` in blocco: sono ~1.000.000 di token.**
Quando esiste sia il `.md` sia l'`.html` di un documento, leggi **solo il `.md`**:
hanno lo stesso contenuto e l'HTML costa il 50% in più. Unica eccezione, il
blueprint del paper, che esiste solo in HTML.

## Dove leggere, per tipo di richiesta

| La richiesta riguarda | Leggi | Costo |
|---|---|---|
| Orientamento, dove sta cosa | `DOCUMENTATION_INDEX.md` | ~0,9k |
| Cosa posso/non posso modificare | `docs/MAINTENANCE.md` §1 e §2 | ~1k |
| **Studio 2 — disegno** | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` §8–§11, §13 · e §0.1 per ciò che non è congelato | ~32k |
| Studio 2 — calibrazione soglie | `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md` (rev. 18) — **prevale sul piano** | ~9k |
| Studio 2 — descrittori e feature | `docs/lit_review/criteri_scelta_descrittori.md` §5.1 (⚠️ non la §5.5) · `DECISIONE_SCELTA_FEATURE_fase_A.md` | ~7k |
| Studio 2 — stato del documento | `docs/fot_walkthrough_conversazione_studio2.md` §0 | ~1k |
| Letteratura: cosa posso rivendicare | `docs/letteratura.md` §14.2 + §14.5 + §14.6 | ~6,5k |
| Esiste già un lavoro su X? | `docs/letteratura.md` §14.1, filtrando sui 🟢 | ~4,6k |
| Aggiungere paper al corpus | `Letteratura_LLM.md` in questa cartella | ~1,5k |
| **Lavorare una fase dello studio 2** | `Fase_LLM.md` | ~1,2k |
| Verificare una fase conclusa | `Verifica_LLM.md` — **altra finestra, altro modello** | ~1k |
| Aggiornare il walkthrough dopo l'OK | `Documentazione_LLM.md` | ~1k |
| Committare | `Commit_LLM.md` + `docs/MAINTENANCE.md` §8 | ~1,5k |
| Come scrivere il paper | `docs/paper/FoT_TEP_paper_blueprint.html` | ~21k |
| Verificare un numero sugli artefatti | `AUDIT_GUIDE.md` §5–§13 | ~8,5k |
| Primo studio: come funzionava | walkthrough primo studio §0–§7 | ~9k |
| Primo studio: risultati e numeri | walkthrough primo studio §7–§10 | ~7k |
| Primo studio: **cosa NON è dimostrato** | walkthrough primo studio §12 | ~1,5k |
| Primo studio: com'è stato costruito | `docs/fot_walkthrough_conversazione.md` §6, §8, §9, §29 — schema del testo neutrale, contabilità byte/token, definizioni statistiche | ~6k |

**Quale walkthrough.** Lo studio 2 è `docs/fot_walkthrough_conversazione_studio2.md`: oggi è uno
**scheletro**, quindi per il disegno vale il piano, non lui. Il primo studio è
`docs/fot_walkthrough_conversazione_v2.md` (~20k dopo l'uscita della letteratura): è un **record**,
non si cita nel paper nuovo e non è fonte per il disegno dello studio 2.

> **Quale prompt aprire e in che ordine**: `README.md` di questa cartella. Il ciclo di una fase è
> `Fase_LLM` → `Verifica_LLM` (altra finestra) → `Documentazione_LLM` → `Commit_LLM`, e l'ordine
> non è negoziabile: il walkthrough non si aggiorna prima della verifica indipendente.
>
> **Per rispondere a domande** invece che per modificare, leggi anche `Questions_LLM.md`
> in questa stessa cartella: aggiunge le poche regole specifiche e non ripete queste.

## Come leggere in modo economico

- **§14.1 di `docs/letteratura.md`** classifica 117 lavori con 🟢 incide sul disegno · 🟡 condivide un asse ·
  🔴 sfondo. Filtra sul colore: per una decisione servono i 🟢, non l'elenco.
- **Un paper**: il nome del file è il titolo; per autori/anno/venue interroga un
  catalogo (OpenAlex, Crossref, arXiv), non il file. Per classificarlo bastano i
  primi ~2.500 caratteri. Testo integrale solo se è 🟢 **e** il compito lo esige.
- **Un numero specifico**: cerca mirato nei report sotto `phase_b/`, `icl/`,
  `ablation/` invece di leggere il walkthrough.
- **La letteratura non sta più nei walkthrough**: dal 2026-09-12 vive in `docs/letteratura.md`
  (replica `letteratura.html`), luogo unico per tutti gli studi. La numerazione §14.x è invariata.
- **I dati del primo studio si leggono, non si ipotizzano.** Se servono soglie, insight, run o
  risultati del primo studio, apri il walkthrough `docs/fot_walkthrough_conversazione_v2.md`
  nella sezione pertinente e verifica sugli artefatti. Per **come** è stata costruita la pipeline
  la fonte è `docs/fot_walkthrough_conversazione.md` (§6, §8, §9, §29): la v2 quello strato lo ha
  perso. Ricostruire a memoria non è ammesso, nemmeno quando sembra ovvio.
- Dichiara sempre, in fondo, **cosa hai letto** e quanto è costato all'incirca.

## In caso di conflitto fra documenti

1. nuova fase  prevale la review del piano;
2. risultati e fatti dell'esperimento concluso  prevalgono il walkthrough e gli
   artefatti congelati;
3. implementazione  prevalgono codice, manifest e dati, da verificare;
4. letteratura  prevale `docs/letteratura.md`, che ne è il luogo unico.

## Regole che non si violano

- **Artefatti congelati** (`phase_b/`, `icl/`, `ablation/`, `tep_*_v2/`, tag git):
  non si modificano mai. Se un numero della documentazione non torna, si corregge
  la documentazione. Se un compito sembra richiedere di cambiarli, **fermati e
  chiedi**.
- **Non inventare** riferimenti, autori, anni, DOI. Se un dato non si trova, scrivi
  che non si trova.
- L'assenza di un risultato dal corpus **non è prova** che non esista nel campo.
- **Non committare** e non creare tag se non ti viene chiesto esplicitamente.
- **Non creare nuovi file indice o README**: la mappa è `DOCUMENTATION_INDEX.md`,
  le regole sono in `docs/MAINTENANCE.md`.
- Altre sessioni possono lavorare sugli stessi file. Rileggi un file prima di
  riscriverlo se è passato del tempo, e non dare per scontato di essere solo.

## Come chiudere

**Se non hai modificato nulla** — dillo esplicitamente, elenca cosa hai letto e
segnala le domande rimaste aperte.

**Se hai preso decisioni che cambiano la documentazione**, aggiorna:
- una scelta sperimentale  walkthrough §5, §6 o §10, e §12 se cambia un limite;
- un claim o un confronto con la letteratura  §14.2, §14.5, §14.6 e il blueprint;
- un paper nuovo nel corpus  procedura §6 di `docs/MAINTENANCE.md`;
- una categoria o una regola nuova  `docs/MAINTENANCE.md`;
- una cartella nuova o spostata  `DOCUMENTATION_INDEX.md`.

**Se hai modificato file**, verifica e riporta:
1. le coppie `.md`  `.html` sono allineate **sul contenuto**, non a occhio
   (stesso numero di voci, confronto riga per riga);
2. i link interni e i percorsi relativi risolvono;
3. `python3 docs/test_explanation.py` — annota i fallimenti **prima** di
   modificare, riesegui dopo, riporta entrambi i numeri. Al 2026-09-11 sono **14**,
   tutti preesistenti. **Quel test non copre §14 né i file `_v2`: invariato non
   significa corretto.**
4. elenca **tutti** i file toccati, uno per riga, con una frase su cosa è cambiato;
5. segnala ciò che hai lasciato indietro e perché.
