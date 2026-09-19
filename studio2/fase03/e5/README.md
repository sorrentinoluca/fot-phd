# E5 — ablazione testuale dei descrittori: materiale di preparazione

Cartella nuova. **Nessun file esistente del repository è stato modificato**, nessuna chiamata
al modello è stata fatta, nessun artefatto congelato è stato toccato, nessuna scrittura git.

Esecuzione del piano `studio2/fase03/PIANO_E5_ABLAZIONE_rev2_2026-09-19.md`, data 2026-09-19.

## Stato dei gate

| Gate | Contenuto | Stato |
| --- | --- | --- |
| **G0** | mappa colonne/famiglie/derivate; misura E5-C2 su dev | **parziale** — `|Δtoken|` misurato; il 5 % va verificato sui prompt completi (`VERIFICA_E5_C2.md` §3) |
| **G1** | decisioni autore A–G | **in attesa dell'autore** — `DECISIONI_AUTORE_E5.md` |
| **G2** | codice corruzione, renderer OMIT, assegnazioni, test | **fatto** — 35 test verdi |
| **freeze** | `exp5-protocol-frozen-001` | bloccato da G1 e dalla misura finale di E5-C2 |
| **G3** | prompt PERM/OMIT sul lotto test | dopo il freeze |
| **G4** | export FULL, sei identità, canary E5 | dopo la chiusura del batch — `VERIFICA_FULL_BLF.md` |

Due cose aprono e chiudono tutto il resto:

* **68 token** — il massimo `|Δtoken|` fra FULL e PERM su 13.500 coppie di sviluppo. È una
  misura, ed è piccola.
* **La verifica del 5 % sui prompt completi** non è ancora fatta: richiede i prompt B-LF
  resi, che stanno in `fot-tep-runtime`. Comando, senza chiamate: `VERIFICA_E5_C2.md` §3.
  Non è sostituibile con una soglia sulla «parte costante» calcolata per sottrazione — con un
  tokenizer BPE i conteggi non sono additivi ai confini.

## File

| File | Ruolo |
| --- | --- |
| `PROTOCOLLO_E5.md` / `.json` | protocollo candidato, con gli hash dei riferimenti |
| `DECISIONI_AUTORE_E5.md` | le sette decisioni A–G, con proposta, motivazione e costo |
| `family_map.json` | colonne → famiglia, grandezze derivate, mappa famiglia–meccanismo proposta, S_F |
| `e5_corruption.py` | scambio della colonna della famiglia, a monte del verbalizzatore |
| `protocol_omit.py` | renderer OMIT per sottrazione letterale dal testo congelato |
| `e5_derangement.py` | derangement disgiunto per classe, campionato uniformemente; frazione ammissibile esatta |
| `build_e5_assignments.py` | → `DERANGEMENTS_E5.json`, `RICEVENTI_E5.json` (solo identificativi) |
| `build_e5_prompts.py` | compone offline PERM/OMIT nei portanti B-LF e prova S18: solo il case block cambia |
| `run_e5.py` | valida e pianifica l'inventario E5; non espone `--execute` |
| `build_dev_units.py` | ricostruisce le tabelle di feature dei 40 run di sviluppo (cache fuori dal repo) |
| `verifica_e5_c2.py`, `riepiloga_e5_c2.py` | misura di `|Δtoken|` sul testo, offline, e riepilogo |
| `verifica_e5_c2_prompt.py` | verifica del 5 % su prompt completi composti e contati interi: `--dev-units` per la fattibilità pre-freeze, `--case-texts` per la misura reale a G3; portante peggiore scelto dopo composizione |
| `export_full_blf.py` | export **in sola lettura** dal ledger del target (gate G4) |
| `test_e5.py` | fixture e regressioni: diff, determinismo, S18, pianificazione senza esecuzione |
| `VERIFICA_E5_C2*.json`, `raw_e5_c2_*.jsonl.gz`, `DEV_UNITS_INDEX.json` | evidenza della misura |
| `VERIFICA_E5_C2_PROMPT_SINTETICO.json` | residuo di confine BPE: 0 su 3.600 osservazioni, con portanti sintetici |

## Riproduzione della misura E5-C2

```bash
python3 studio2/fase03/e5/build_dev_units.py --output ~/e5_work/dev_units
for b in 20260919 20260969 20261019; do
  python3 studio2/fase03/e5/verifica_e5_c2.py --dev-units ~/e5_work/dev_units \
    --seeds 50 --base-seed $b --raw-out ~/e5_work/raw.jsonl --out ~/e5_work/part_$b.json
done
python3 studio2/fase03/e5/riepiloga_e5_c2.py --raw ~/e5_work/raw.jsonl --out ~/e5_work/riepilogo.json
E5_DEV_UNITS=~/e5_work/dev_units python3 studio2/fase03/e5/test_e5.py
```

Dipendenze: `pandas`, `numpy`, `openpyxl` e uno fra `tokenizers` e `transformers`. Senza di
esse i test non partono — l'esito dichiarato qui è quello ottenuto sulla macchina con quelle
librerie, non una garanzia su ogni ambiente.

Il primo passo legge i CSV dei run di sviluppo e ne verifica l'hash contro
`MANIFEST_FAULT_DEV.csv`; il resto non tocca il disco fuori da `--output`/`--out`.

## Che cosa NON c'è, e perché

* Gli adattatori `build_e5_prompts.py` e `run_e5.py` sono testati solo su fixture: il primo
  usa i portanti B-LF e si blocca se S18 trova differenze fuori dal blocco caso; il secondo non
  ha `--execute`. L'integrazione con ledger, canary e target nuovo resta un delta da applicare
  su `main` dopo il freeze.
* **`AGENT_ASSIGNMENT.json`** non è in questo checkout: `build_e5_assignments.py` lo prende da
  `--assignment`. Gli artefatti qui presenti sono stati generati dalla copia su `main`
  (`git show main:studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json`) e sono riproducibili.
* **Il ledger e le librerie di insight** non sono stati aperti: stanno in `fot-tep-runtime`,
  fuori perimetro per questa sessione.
