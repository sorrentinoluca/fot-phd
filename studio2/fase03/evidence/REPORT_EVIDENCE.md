# Sotto-fase 03.6 — report evidence 697-D

**Completata, in attesa di verifica indipendente.** Data: 2026-09-13. Nessuna
simulazione e nessuna chiamata a modelli linguistici.

## 1. Riassunto e risultati

L'autore ha autorizzato U3, estensione condizionata di U1/R2: N1–N5 è la sola baseline
di normalizzazione del verbalizzatore e resta accoppiata alle quattro soglie V2 congelate.
Il recheck R2 della 03.5 è `PASS`, coincide col commit `d09e7ed` e ha SHA-256
`7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8`.

La guardia ha verificato i quattro sorgenti congelati prima dell'import. L'estrattore ha
verificato i 40 CSV e i 40 manifest per-run, poi ha prodotto 320 unità, ciascuna con 41
righe di feature, JSON strutturato, testo neutrale e firma 697-D. L'indice con fault,
batch e stream è evaluator-side e separato.

| Controllo | Esito |
| --- | ---: |
| Run / finestre | 40 / 320 |
| Artefatti unitari verificati | 1.280 |
| File totali / byte totali | 1.283 / 61.208.618 |
| Dimensione firme e range | 697; tutte in `[0,1]` |
| Leakage su JSON e testi | PASS |
| SHA-256 `EVIDENCE_MANIFEST.csv` | `5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020` |
| SHA-256 `EVALUATOR_INDEX.csv` | `b966cdd3d579efaf595fd48c4b9baa70747ba584522926520840a1e914dbf69c` |
| SHA-256 `EXTRACTION_SUMMARY.json` | `fba6f90bcfe28a4d2423432e0d61272fb1888d9d56e8ed21109276a0a1cc614e` |

La fixture sintetica è stata eseguita due volte con output byte-identico. Test finali:
`Ran 4 tests — OK`; coprono end-to-end, dimensione, determinismo, guardia alterata,
recheck R2 non canonico e leakage intenzionale.

## 2. File toccati

- `studio2/fase03/evidence/DIPENDENZE_EVIDENCE.md` — dipendenze, default e decisione U3.
- `studio2/fase03/evidence/__init__.py` — package del nuovo harness.
- `studio2/fase03/evidence/extract_evidence.py` — guardie, estrazione e manifest.
- `studio2/fase03/evidence/leakage.py` — scanner D1 fail-closed.
- `studio2/fase03/evidence/test_evidence.py` — test sintetici e negativi.
- `studio2/fase03/evidence/verify_output.py` — verifica completa indipendente dalla scrittura.
- `studio2/fase03/evidence/OUTPUT_CHECK.json` — esito machine-readable del lotto.
- `studio2/fase03/evidence/.gitignore` — esclude la copia locale recuperabile di `output/`.
- `studio2/fase03/evidence/MANIFEST_CONSERVAZIONE.csv` — 1.283 percorsi, byte e hash.
- `studio2/fase03/evidence/ARTIFACT_STORAGE.json` — release e verifica per riscaricamento.
- `studio2/fase03/evidence/REPORT_EVIDENCE.md` — questo report.
- `studio2/PROVENIENZA.md` — §9, import function-level, U3, limiti e conservazione.

Non sono stati modificati file congelati, script/schema preesistenti di Fase 03, piano o
walkthrough.

## 3. Modello e profilo

OpenAI Codex (GPT-5), profilo **implementativo**, ragionamento medio, test eseguiti.
Runtime: `/opt/anaconda3/bin/python3`, NumPy 2.3.5, pandas 2.3.3, openpyxl 3.1.5.

## 4. Cosa è rimasto fuori

- separabilità, accuracy, rilevabilità e intensità del segnale: escluse per disegno;
- verifica indipendente della sotto-fase e documentazione nel walkthrough: finestre successive;
- integrazione del branch in `main`: decisione dell'autore.

Gli output voluminosi non sono in Git: la copia locale è ignorata e resta recuperabile
dalla release pubblica.

## 5. Decisioni ancora necessarie

Nessuna per l'estrazione corrente. Se R2 decade o la 03.5 passa a `baseline_fit_new`, la
regola già congelata impone di invalidare e rigenerare tutte le evidence; non autorizza
una sostituzione automatica della baseline.

## 6. Verifiche e conservazione

`docs/test_explanation.py` prima e dopo: `Ran 35 tests` — **FAILED (failures=14,
skipped=1)**, conteggio invariato e preesistente.

L'output da 61 MiB e 1.283 file è pubblicato in `fot-tep-data`, release
`studio2-fase03-evidence-v1`. Archivio: 64.817.152 byte, SHA-256
`3e1eb87f38ff3fc6dd3346476785d06c2b98944b209f7f58706b3c71c1676999`.
È stato riscaricato in `/tmp/fot-tep-evidence-redownload-verify-001`: hash archivio
coincidente, 1.283/1.283 file e 61.208.618 byte verificati, zero mismatch e zero extra.

## 7. Commit

Già creati:

- `cf1f70f` — dipendenze e fixture;
- `daf5dc5` — provenienza iniziale degli import.

Chiusura separata in due cambiamenti:

- `d54fa4a` — estrazione reale e verifica del lotto;
- il commit che contiene questo report — provenienza U3, manifest e conservazione.

## Fonti lette e costo

Letti i prompt operativi, MAINTENANCE §1/§2/§8, decisione/verifiche 03.4,
PROVENIENZA e qualificazione R1/R2, specifica/report/manifest dei run, i quattro
sorgenti congelati, configurazione V2, prima esposizione della pipeline e catalogo D1.
Costo approssimativo: 30–40 mila token di testo/codice; estrazione 16 secondi, audit
locale circa 5 secondi, più pubblicazione e verifica remota.
