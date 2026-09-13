# Fase 03 — report della sotto-fase D1: estrazione del catalogo degli otto fault

Data: **2026-09-13**. Autore: **Claude (Cowork, modello configurato `claude-fable-5-1`)**, finestra
di lavoro principale. Profilo: **decisionale** per la ricostruzione dello spazio ammissibile e il
congelamento; **implementativo** per lo script e le verifiche. Branch di lavoro:
`codex/studio2-criteri-freeze-rev002`, creato da `main` = `origin/main` = `9faecaf`.
Stato aggiornato dopo la prima verifica: correzioni e replay verificato descritti in §6. Le sezioni A–D registrano la consegna originaria di Claude.
Perimetro: esecuzione della decisione D1 secondo la procedura prespecificata nel registro
congelato; nessun commit, push o tag in questa finestra. Non è la chiusura della macro-Fase 03.

## 1. Risultati nell'ordine delle sotto-attività

### A · Attestazione del congelamento dei criteri

- Il tag annotato `studio2-fase03-criteri-selezione-frozen-001` (oggetto `e2a7c49`) punta al
  commit `9faecaf7337e5864b7a3ad44cadb8971853dd260`, che coincide con `origin/main` e con l'HEAD
  da cui è stato creato il branch di lavoro. Worktree pulito prima dell'inizio.
- `CRITERIA_FREEZE.json` (rev. 1, SHA-256 `ecae5717…5575c9b`) riportava `d1_draw_executed=false`
  e `catalog_frozen=false`.
- I quattro file elencati nel manifest coincidono per SHA-256 e dimensione sia col worktree sia
  col blob al `source_commit` `9d0e191`: registro `d58a7606…231c7` (11.339 byte), piano
  `7f9462c2…1767a` (159.979), `FEASIBILITY.json` `ca830d05…d9810` (504), `SOURCE_CHECK.json`
  `82c654d1…65372` (747).
- `python3 docs/test_explanation.py` prima delle modifiche: **35 test, 14 fallimenti, 1 skipped**.

### B · Spazio ammissibile ricostruito dal registro (§2–§4)

Universo IDV(1)–IDV(15); continuità F1/F8/F10/F13; undici candidati per quattro posti nuovi,
C(11,4) = **330** quadruple. Vincoli congiunti: almeno 2 step, 2 random variation, 2 sticking
valve, 1 slow drift; nessuna coppia con la stessa chiave di identità ({3,9}, {4,11}, {5,12});
almeno due membri di H = {F3, F9, F15}.

Derivazione dei posti forzati, verificata dall'enumerazione: l'universo contiene esattamente due
sticking valve (F14, F15) e la continuità nessuna, quindi la quota sticking = 2 forza **F14 e
F15**. Con F15 ∈ H già dentro, H ≥ 2 richiede almeno uno fra F3 e F9; il divieto {3,9} ne
ammette **uno solo**. Il quarto posto è libero fra {2, 4, 5, 6, 7, 11, 12}, ma con F9 (random) la
quota step ≥ 2 esclude F11 e F12, perché la continuità porta un solo step (F1). Ne risultano
7 + 5 = **12** cataloghi, in accordo con `FEASIBILITY.json` e con la verifica indipendente:

| Indice | Nuovi | Catalogo | Composizione step/random/drift/sticking | H |
| ---: | --- | --- | --- | --- |
| 0 | 2, 3, 14, 15 | 1, 2, 3, 8, 10, 13, 14, 15 | 3/2/1/2 | 3, 15 |
| 1 | 2, 9, 14, 15 | 1, 2, 8, 9, 10, 13, 14, 15 | 2/3/1/2 | 9, 15 |
| 2 | 3, 4, 14, 15 | 1, 3, 4, 8, 10, 13, 14, 15 | 3/2/1/2 | 3, 15 |
| 3 | 3, 5, 14, 15 | 1, 3, 5, 8, 10, 13, 14, 15 | 3/2/1/2 | 3, 15 |
| 4 | 3, 6, 14, 15 | 1, 3, 6, 8, 10, 13, 14, 15 | 3/2/1/2 | 3, 15 |
| 5 | 3, 7, 14, 15 | 1, 3, 7, 8, 10, 13, 14, 15 | 3/2/1/2 | 3, 15 |
| 6 | 3, 11, 14, 15 | 1, 3, 8, 10, 11, 13, 14, 15 | 2/3/1/2 | 3, 15 |
| 7 | 3, 12, 14, 15 | 1, 3, 8, 10, 12, 13, 14, 15 | 2/3/1/2 | 3, 15 |
| 8 | 4, 9, 14, 15 | 1, 4, 8, 9, 10, 13, 14, 15 | 2/3/1/2 | 9, 15 |
| 9 | 5, 9, 14, 15 | 1, 5, 8, 9, 10, 13, 14, 15 | 2/3/1/2 | 9, 15 |
| 10 | 6, 9, 14, 15 | 1, 6, 8, 9, 10, 13, 14, 15 | 2/3/1/2 | 9, 15 |
| 11 | 7, 9, 14, 15 | 1, 7, 8, 9, 10, 13, 14, 15 | 2/3/1/2 | 9, 15 |

Cinque cataloghi con composizione 3/2/1/2 e sette con 2/3/1/2. L'ordinamento è quello
lessicografico delle quadruple di nuovi ID come tuple di interi (§5.2); per questi dodici casi
coincide con l'ordinamento lessicografico degli otto ID completi, quindi non c'è ambiguità
residua nella lettura del registro.

### C · Esecuzione della procedura §5

Script originariamente eseguito, ora conservato byte per byte in
`studio2/fase03/selection/execution_snapshot/draw_d1.py` (nessuna dipendenza esterna, solo
`hashlib`/`itertools`; niente `hash()` del linguaggio, niente RNG di sistema). Il record è
`studio2/fase03/selection/D1_DRAW_LOG.json`.

| Elemento | Valore |
| --- | --- |
| N ammissibili | 12 |
| Namespace / seed | `studio2-fase03-D1-v1` / `20260913` |
| L = 2²⁵⁶ − (2²⁵⁶ mod 12) | 2²⁵⁶ mod 12 = 4; probabilità di rifiuto ≈ 3,5·10⁻⁷⁷ |
| Contatore accettato | **c = 0**, messaggio `studio2-fase03-D1-v1|20260913|0` |
| Estrazioni rifiutate | **nessuna** |
| SHA-256 accettato | `0116bf108b82d515210233f433caa65f0b91d9fe46a18fc9d25a1294b8a644f0` |
| x mod 12 = indice | **0** |
| Quadrupla estratta | **F2, F3, F14, F15** |

Il digest è stato replicato indipendentemente con soli primitivi (`hashlib`, senza importare lo
script) con lo stesso esito; un secondo run dello script produce un record identico byte per
byte. Un solo sorteggio, nessun rilancio, nessun secondo seed.

L'indice estratto è il primo della lista ordinata. È l'esito del digest prespecificato, non una
scelta: chiunque può ricalcolarlo con `sha256("studio2-fase03-D1-v1|20260913|0")` e prenderne il
resto modulo 12. Resta il limite già registrato dal verificatore dei criteri: un seed pubblico è
calcolabile da chiunque prima del passo formale, e il commit prova la precedenza dei criteri
rispetto ai risultati futuri, non lo stato cognitivo delle persone.

### D · Catalogo risultante e congelamento

| IDV | Variabile (tabella 8) | Meccanismo | Chiave | Strato | Origine |
| ---: | --- | --- | --- | :---: | --- |
| 1 | rapporto A/C, B costante, flusso 4 | step | ratio_ac_s4 | O | continuità |
| 2 | composizione B, A/C costante, flusso 4 | step | composition_b_s4 | O | **nuovo D1** |
| 3 | temperatura alimentazione D, flusso 2 | step | temperature_d_s2 | **H** | **nuovo D1** |
| 8 | composizione A/B/C, flusso 4 | random variation | composition_abc_s4 | O | continuità |
| 10 | temperatura alimentazione C, flusso 4 | random variation | temperature_c_s4 | O | continuità |
| 13 | cinetica di reazione | slow drift | reaction_kinetics | O | continuità |
| 14 | valvola acqua reattore | sticking valve | valve_cw_reactor | O | **nuovo D1** (forzato) |
| 15 | valvola acqua condensatore | sticking valve | valve_cw_condenser | **H** | **nuovo D1** (forzato) |

Composizione 3 step / 2 random / 1 drift / 2 sticking; H = {F3, F15}; nessuna chiave duplicata.
Tutti e quattro i meccanismi della tabella 8 sono rappresentati.

File prodotti:

- `CATALOG_FREEZE.json` — otto fault con variabile, meccanismo, chiave, strato, origine; parametri
  e digest del sorteggio; hash di registro, manifest rev. 1, script, record e `FEASIBILITY.json`;
  `d1_draw_executed=true`, `catalog_frozen=false` con condizione di efficacia (verifica indipendente
  OK, commit raggiungibile da `origin/main`, tag annotato proposto
  `studio2-fase03-catalogo-D1-frozen-001`).
- `CRITERIA_FREEZE_rev002.json` — nuova revisione tracciata del manifest dei criteri
  (MAINTENANCE §8.4): copia integrale dei campi della rev. 1, `supersedes` con hash e byte della
  rev. 1, `reason_for_revision`, `changed_fields`, `d1_draw_executed=true`, puntatori a record e
  manifest del catalogo. **`CRITERIA_FREEZE.json` è rimasto byte-identico** (`ecae5717…5575c9b`).
- `studio2/PROVENIENZA.md` — nuova sezione 6 con le fonti usate da D1 e la marca pre-specificata.

## 2. Cosa non è stato fatto e perché

- **Nessun risultato per-fault dei nostri esperimenti è stato aperto**: né
  `studio2/fase03/results/`, né `phase_b/`, né i walkthrough del primo studio nelle sezioni con
  accuratezze, né i file della sonda. Le uniche letture sono state i documenti di procedura,
  il pacchetto §6.1 congelato, le sezioni D1/§6.1/§0.1/§8.3/§8.6/§12.1–12.4/D11 del piano e
  il walkthrough studio 2 §0, §0.1, §4.1.
- **I criteri non sono stati riaperti né interpretati oltre il testo.** L'unica libertà
  potenziale — se «quadruple» in §5.2 si riferisca ai quattro nuovi ID o agli otto — è risultata
  irrilevante perché i due ordinamenti coincidono sui 12 casi.
- **La tabella 8 di Downs & Vogel non è stata riscaricata**: le proprietà usate (meccanismo,
  variabile, chiave) sono quelle trascritte nel registro §2 e già riverificate sul PDF primario
  dal verificatore dei criteri (`SOURCE_CHECK.json`, `VERIFICA_CRITERI_6_1.md` §2). Questa
  sotto-fase non aggiunge proprietà oltre quelle.
- Nessuna chiamata al modello, nessuna simulazione, nessun push, nessun tag.
- Non è stato scritto `REPORT_FASE03.md`: la Fase 03 non si chiude con D1.

## 3. Ciò che resta aperto dopo D1

| Voce | Stato | Nota |
| --- | --- | --- |
| D2 — 6 o 8 run per fault | aperta, indipendente da D1 | piano §8.8 |
| D11 — coppie confondibili | **ora lavorabile**; proposta non vincolante in `PROPOSTA_OOD_D11.md` | richiede decisione dell'autore |
| OOD — due fault fuori catalogo (§8.6, S13) | **ora lavorabile**; proposta non vincolante in `PROPOSTA_OOD_D11.md` | «meccanicamente distinto» non è definito formalmente dal piano: decisione dell'autore |
| Producer alternativo | aperto | nessuna configurazione |
| Specifica di generazione | aperta | deve esplicitare il rapporto con la nota Downs & Vogel su IDV(14)–IDV(15) (perturbazione congiunta, 24–48 h) **prima** dei nuovi run; F14/F15 sono in catalogo per vincolo |
| Gate reale 03.0, nuovi run, evidence | aperti | invariati |
| Congelamento del catalogo | in attesa | verifica indipendente → documentazione → commit → tag su richiesta esplicita |

## 4. Verifiche e decisione di commit

- Replay dello script: record identico byte per byte.
- `python3 docs/test_explanation.py` dopo le modifiche: **35 test, 14 fallimenti, 1 skipped**,
  identico alla baseline; il test non copre questa sotto-fase. `git diff --check` pulito.
- Tutti gli hash dichiarati in `CATALOG_FREEZE.json` e `CRITERIA_FREEZE_rev002.json` sono stati
  ricontrollati contro il worktree dopo la scrittura di tutti i file: nessuna discrepanza.
- Artefatti congelati non toccati; `CRITERIA_FREEZE.json` invariato; nessun file del pilot mutato.

Decisione proposta: **committare dopo l'OK della verifica indipendente**, sul branch
`codex/studio2-criteri-freeze-rev002`, con messaggio
`studio2(fase03): esegue D1 ed estrae il catalogo degli otto fault`. Il tag
`studio2-fase03-catalogo-D1-frozen-001` e l'integrazione in `origin/main` seguono il ciclo
Verifica_LLM → Documentazione_LLM → Commit_LLM, su richiesta esplicita dell'autore.

## 5. Fonti lette e costo

Prompt del ciclo, MAINTENANCE §1/§2/§8, walkthrough studio 2 §0/§0.1/§4.1, il pacchetto §6.1
completo, piano D1/§0.1/§6.1/§8.3/§8.6/§12.1–12.4/D11, `PROVENIENZA.md` (struttura e coda).
Nessuna lettura in blocco del corpus, del piano o dei dati. Ordine di grandezza: ~40k token di
contesto documentale; zero inferenze scientifiche, zero batch.


## 6. Riesame del 2026-09-13 — correzioni di tracciabilità

Responsabile delle correzioni: **Codex, GPT-6**, profilo implementativo; verifica indipendente
in contesto separato con modello richiesto `gpt-5.6-sol`. La prima verifica ha dato NON OK
per tre problemi di tracciabilità, pur confermando catalogo, digest, ordinamento e impronte.
Il suo esito e il successivo riesame sono in `VERIFICA_CATALOGO_D1.md`.

1. **Guardia prima dell'esito.** La revisione corrente `draw_d1.py` verifica tag annotato,
   commit, manifest rev1, snapshot delle quattro fonti e hash del registro prima di enumerare
   cataloghi o calcolare il digest D1. La precedente esecuzione aveva criteri validi, attestati
   separatamente prima del run; la correzione chiude il percorso errato su input alterati.
2. **Replay dopo un nuovo commit.** Il parametro `--draw-context-commit` è vincolato al contesto
   storico `9faecaf7337e5864b7a3ad44cadb8971853dd260` e alla data 2026-09-13. Il record conserva
   `worktree_head_at_draw` storico; non lo sostituisce con HEAD del replay. Un test in clone
   locale temporanea, con HEAD avanzato, riproduce esattamente i byte originali. Il comando è:

   ```bash
   python3 studio2/fase03/selection/draw_d1.py \
     --draw-context-commit 9faecaf7337e5864b7a3ad44cadb8971853dd260 \
     --out /tmp/D1_DRAW_LOG_replay.json
   ```

   Il comando rifiuta la destinazione del log originale. L'originale `D1_DRAW_LOG.json` resta
   immutato (SHA-256 `fa571e89054a004021b08e93cd857ad4b8d41794b8c070260a49d4fb03a08b95`).
3. **Revisione amministrativa distinta.** `CRITERIA_FREEZE_rev002.json` mantiene i metadati
   storici dei criteri sotto `criteria_origin`; il proprio stato D1 richiede invece
   `VERIFICA_CATALOGO_D1.md`, commit e il nuovo tag del catalogo. Il vecchio tag non attesta
   l'esecuzione D1 e non rende automaticamente efficace la rev002. Il campo `changed_fields`
   registra le differenze rispetto alla rev1, che resta intatta. L'aggiornamento non modifica
   alcun criterio normativo.

**Conservazione dell'esecuzione originale.** `execution_snapshot/draw_d1.py` ha gli stessi
9.846 byte e SHA-256 `b9fba113ade9729b0f59469b31e412ebb0c4ed0d2bc53ce580b65bd3e536f06b`
dello script eseguito da Claude. È una copia forense, non il comando corrente di replay.
Il manifest del catalogo distingue lo snapshot eseguito dalla revisione corretta di replay;
non attribuisce retroattivamente l'esecuzione originaria al codice corretto. Il log originale
rimane identico. I due replay di audit non sono nuovi sorteggi o nuovi seed: `reruns=0`
conta i rilanci per cambiare esito, non le riproduzioni di verifica.

File ulteriori: `test_draw_d1.py` copre quattro regressioni (criteri alterati prima del
sorteggio, contesto non registrato, protezione del log, identità del replay dopo avanzamento
HEAD); `D1_REVIEW_CHECK.json` registra esiti e impronte. I quattro test passano. Il controllo
documentale resta a 35 test, 14 fallimenti preesistenti e 1 skipped.

OOD e D11 restano proposte non approvate. La presente correzione non sceglie fault OOD o
coppie, non esegue simulazioni e non modifica i risultati del pilot. Dopo l'OK indipendente si
aggiorna la documentazione; commit, tag e integrazione del catalogo richiedono la conferma di
pubblicazione di questa consegna D1. Fino alla pubblicazione il catalogo resta un candidato
verificato al congelamento, con `catalog_frozen=false`.


## 7. Documentazione dopo l'OK indipendente

Aggiornati il piano autorevole (stato di D1 in §0.1, §6.1 e D1) e la coppia walkthrough Studio 2
(§4.1 resa esplicitamente storica, nuova §4.2 e dipendenze). La documentazione distingue
estrazione verificata e congelamento ancora da pubblicare. I manifest riportano
`reviewed_pending_commit_and_publication`, verifica D1 OK e `catalog_frozen=false`.
`D1_DELIVERY_CHECK.json` registra i controlli finali della coppia e dei link. La sintesi divulgativa
resta invariata: è preparazione del protocollo, senza un nuovo risultato scientifico.
La proposta OOD/D11 rimane visibile come proposta non vincolante e non entra nelle impronte del
catalogo. Nessun commit, push o tag è stato eseguito durante il riesame e la documentazione.
