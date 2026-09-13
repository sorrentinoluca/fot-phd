# Sotto-fase 03.6 — report evidence 697-D

**Stato: sospesa prima dell'estrazione reale per decisione di provenienza.** Data:
2026-09-13. La parte implementativa e la fixture sintetica sono complete; non sono stati
letti né trasformati i CSV dei 40 run fault.

## 1. Riassunto e risultati

È stata dichiarata prima dell'estrazione la catena function-level richiesta da
`docs/MAINTENANCE.md` §8.2. L'harness verifica SHA-256 di quattro sorgenti congelate prima
di importarli, rende espliciti `start_h=25.0`, `end_h=65.0`, `window_h=5.0`, otto finestre
per run e il percorso della configurazione V2, quindi produce per ogni finestra:

- 41 righe di feature numeriche;
- JSON strutturato e testo neutrale consumer-facing;
- firma di 697 componenti in ordine fisso;
- manifest con percorso, byte e SHA-256 di ogni artefatto;
- indice evaluator-side separato con run, fault, batch e stream.

Lo scanner fail-closed copre gli otto identificatori D1, `IDV(n)`, le descrizioni e le
chiavi dei meccanismi, e le marche «continuità/nuovo». La fixture sintetica end-to-end ha
prodotto 8/8 unità; due estrazioni hanno avuto tree digest byte-identico; tutte le otto
firme hanno dimensione 697. Il test della guardia con `tep_features.py` alterato e il test
di leakage intenzionale hanno entrambi rilevato l'errore atteso.

Esito test:

```text
Ran 3 tests
OK
```

Runtime usato per i test: `/opt/anaconda3/bin/python3`, NumPy 2.3.5, pandas 2.3.3,
openpyxl 3.1.5, pytest 8.4.2. Nessuna chiamata a modelli linguistici e nessuna
simulazione.

## 2. File toccati

- `studio2/fase03/evidence/DIPENDENZE_EVIDENCE.md` — import, dipendenze transitive,
  impronte, default, blocco di provenienza ed esclusioni scientifiche.
- `studio2/fase03/evidence/__init__.py` — rende importabile il nuovo harness nei test.
- `studio2/fase03/evidence/extract_evidence.py` — guardia, estrazione deterministica,
  separazione consumer/evaluator, manifest e scrittura atomica.
- `studio2/fase03/evidence/leakage.py` — scanner anti-leakage D1 riscritto.
- `studio2/fase03/evidence/test_evidence.py` — fixture end-to-end, dimensione,
  determinismo, guardia negativa e leakage intenzionale.
- `studio2/fase03/evidence/REPORT_EVIDENCE.md` — questo verbale della finestra sospesa.
- `studio2/PROVENIENZA.md` — nuova §9 con una riga per funzione importata e senza
  promuovere la baseline non autorizzata.

Non sono stati modificati `code/`, `phase_b/`, gli script e gli schemi già presenti in
`studio2/fase03/`, il walkthrough o il piano. La nuova §9 di `studio2/PROVENIENZA.md`
registra il solo codice importato e marca la baseline reale come non autorizzata.

## 3. Modello e profilo

Sotto-fase 03.6 eseguita da **OpenAI Codex (GPT-5)**, profilo **implementativo**,
ragionamento medio, con test eseguiti. Nessun profilo esecutivo-batch è stato avviato.

## 4. Cosa è rimasto fuori

- Estrazione dei 40 run × 8 finestre = 320 unità reali: sospesa prima della lettura dei
  CSV per il punto bloccante della sezione 5.
- `evidence/output/`, `EVIDENCE_MANIFEST.csv`, `EVALUATOR_INDEX.csv` e relative
  impronte reali: non esistono ancora.
- Riga di **riuso effettivo della baseline** in `studio2/PROVENIENZA.md`: subordinata
  all'autorizzazione e all'uso reale; la §9 attuale registra soltanto gli import.
- Conservazione su Git o `fot-tep-data`: la scelta dipende dai byte effettivi, che non
  possono essere misurati prima dell'estrazione autorizzata.
- Valutazioni di separabilità, accuracy o intensità del segnale: escluse per disegno,
  non rinviate.

## 5. Decisione ancora necessaria

U1/R2 autorizza N1–N5 esclusivamente come `baseline_fit` dello score A e nomina come
destinazione i parametri di Fase 02. Il verbalizzatore richiede invece le statistiche
N1–N5 per normalizzare le feature e applicare i propri flag congelati. Occorre scegliere:

1. estendere U1/R2 alla normalizzazione e ai flag del verbalizzatore 03.6, con marca
   esplicita e nuova riga autonoma in `studio2/PROVENIENZA.md`; oppure
2. attendere e usare una baseline dei nuovi Normal della 03.5, con regola e artefatto
   verificati.

Domanda precisa all'autore: **autorizzi l'opzione 1, oppure prescrivi l'opzione 2?**

## 6. `docs/test_explanation.py`

Prima delle modifiche: `Ran 35 tests` — **FAILED (failures=14, skipped=1)**. Dopo le
modifiche: `Ran 35 tests` — **FAILED (failures=14, skipped=1)**. Il conteggio è
invariato; i 14 fallimenti sono quelli preesistenti dichiarati dal contratto di
manutenzione.

## 7. Commit

La parte autorizzata è pronta per due commit autonomi:

```text
studio2(fase03): dichiara dipendenze e valida la fixture evidence 697-D
studio2(fase03): registra la provenienza degli import evidence 697-D
```

Non vanno creati i commit successivi di estrazione reale, riuso della baseline e
conservazione finché la decisione della sezione 5 non è registrata e applicata.

## Fonti lette e costo

Letti integralmente o nelle sezioni richieste: `Prompt_LLM.md`, `Fase_LLM.md`,
`MAINTENANCE.md` §1/§2/§8, decisione e verifiche 03.4, `PROVENIENZA.md` §1–§5,
`QUALIFICAZIONE_RIUSO.md`, specifica/report/manifest dei run fault, i quattro sorgenti
congelati, configurazione e manifest delle impronte; mirate le sezioni operative della
prima esposizione e i documenti D1 per il lessico anti-leakage. Costo approssimativo di
lettura: 25–35 mila token di testo e codice, oltre ai controlli meccanici.
