# Report di sotto-fase 03.4 — Perimetro del codice Q8

Sotto-fase **03.4** della Fase 03 dello studio 2 (`APERTURA_SOTTOFASI_FASE03.md` §2: blocco a monte,
non un cantiere del piano). Profilo dichiarato in apertura: **decisionale**. Report secondo
`docs/prompts/Fase_LLM.md`, «Chiusura della finestra», punti 1–7, e `docs/MAINTENANCE.md` §8.6.
Solo Markdown, senza coppia `.html`.

**Esito in una riga:** la sotto-fase produce una **proposta** (`PROPOSTA_PERIMETRO_Q8.md`), non una
decisione; nessun artefatto è congelato, nessun tag creato, nessun file fuori da
`studio2/fase03/perimetro_q8/` modificato. La verifica indipendente (`Verifica_LLM.md`, altra
finestra, altro modello) e la conferma dell'autore precedono qualunque modifica a
`docs/MAINTENANCE.md`, al walkthrough e a `studio2/PROVENIENZA.md`.

## 1. Riassunto e risultati

Una sola sotto-fase eseguita, in quest'ordine interno.

**Lettura del contratto e dello stato.** `MAINTENANCE.md` §1, §2, §8.1–8.6; walkthrough studio2 §0 e
§0.1 (punto 2 testualmente); `Fase_LLM.md`; PROVENIENZA §5; `IMPLEMENTATION_STATUS.md`;
`APERTURA_SOTTOFASI_FASE03.md` §2–§3; piano §6.4, §6.5, §6.7, §6.8, §8.5, §8.9, D10; prima
esposizione, sezioni feature → flag → JSON → testo neutrale e caratterizzazione del payload.
Impronte in `PROPOSTA_PERIMETRO_Q8.md` §0.

**Inventario** (proposta §2): 44 file classificati con commit, SHA-256, copertura da manifest/tag/test
di pinning, assunzioni del primo studio e sotto-fasi che li richiedono. Criterio scritto prima
dell'applicazione (proposta §1): harness riutilizzabile / harness con costanti di protocollo /
artefatto. Verifiche eseguite: 56/56 impronte del manifest `PHASE_B_PROTOCOL_HASHES.json` coincidono
con HEAD; le undici occorrenze di `label_space[:-1]` sono esattamente quelle che D10 elenca; nessun
modulo di `studio2/` importa da `phase_b/`; quattro file di `code/` sono nel manifest, pinnati da
`phase_b/tests/test_phase_a_hashes.py` e identici sotto cinque tag; la firma 697-D è
`code/evaluate_verbalizer_v2.py::signature_vector` (41 × 17); `studio2/fase02/analysis/tep_features.py`
è copia byte-identica di `code/tep_features.py` senza riga in PROVENIENZA.

**Stato del punto 2 di §0.1** (proposta §3): operativamente chiuso da §8.2 e dal precedente di
PROVENIENZA §5 — l'estensione a 8 agenti, le 9 pseudolabel con astensione e il controllo E a campo
singolo sono già in `studio2/fase03/protocol.py` senza scrivere in `phase_b/`; testualmente aperto
per una premessa errata («richiedono di scrivere dentro `phase_b/`») e per tre residui: stato di
`code/` in §1, regola copia/import per il codice, riga PROVENIENZA mancante per la copia di Fase 02.

**Opzioni** (proposta §4): (a) nessuna modifica a §1; (b) separazione harness/artefatto in §1 con
elenco — giudicata inerte o pericolosa, perché ogni modulo harness è nel manifest e §1 vieta gli
elenchi; (c) `phase_b/q8/` — da escludere per §1/§8.1 — o `studio2/harness/` — organizzazione
interna, non perimetro. Motivata sul testo la lettura di `code/`: nucleo congelato per impronta anche
se §1 non lo nomina.

**Raccomandazione** (proposta §5): opzione **(a′)** = (a) più tre precisazioni testuali, con il
testo esatto per §1, §8.2, la chiusura in §0.1 e una riga PROVENIENZA; effetti su 03.6, 03.7, 03.9,
03.10 in §5.5.

## 2. File toccati

| File | Cosa è cambiato |
| --- | --- |
| `studio2/fase03/perimetro_q8/PROPOSTA_PERIMETRO_Q8.md` | **nuovo**: proposta di decisione con inventario, analisi del punto 2, opzioni, raccomandazione e testi proposti |
| `studio2/fase03/perimetro_q8/REPORT_PERIMETRO_Q8.md` | **nuovo**: questo report |

Nessun altro file. In particolare **non** toccati: `docs/MAINTENANCE.md`,
`docs/fot_walkthrough_conversazione_studio2.md` (e `.html`), `studio2/PROVENIENZA.md`, `phase_b/`,
`code/`, `docs/paper/`, alcun artefatto congelato o tag. `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`
era già presente come file **non tracciato** nella copia di lavoro: letto, non modificato, non
committato.

Operazione accessoria: il repository conteneva un `.git/index.lock` stantio (creato 15:43 UTC,
nessun processo git attivo) che impediva di creare il branch; è stato rimosso con permesso esplicito
dell'autore. Non è una modifica al contenuto tracciato.

## 3. Modello e profilo

| Sotto-fase | Profilo dichiarato | Modello | Ragionamento |
| --- | --- | --- | --- |
| 03.4 | decisionale (breve) | Claude Fable 5.1 (`claude-fable-5-1`) | esteso |

Nessuna chiamata a modelli linguistici, nessuna simulazione, nessuna esecuzione di test di
`phase_b/` o `studio2/` (non richiesti: la sotto-fase legge, non implementa). Comandi eseguiti:
`git` (checkout del branch, log, rev-parse, tag), `sha256sum`/`hashlib`, `grep`, `sed -n`,
`python3 docs/test_explanation.py`.

## 4. Cosa è rimasto fuori e perché

- **L'attuazione della decisione** (modifica a §1, §8.2, §0.1, PROVENIENZA): per mandato, in
  un'altra finestra dopo la conferma dell'autore.
- **La scelta copia/import** per il codice congelato: è una scelta dell'autore (proposta §6.2); qui
  è solo raccomandata.
- **Test di `studio2/fase03/`** non eseguiti (`pytest` non installato nell'ambiente locale; non
  richiesti dalla sotto-fase).
- **Ogni decisione delle sotto-fasi successive**: schema insight (03.12), seed/namespace delle
  pseudolabel (03.7), soglie del verbalizzatore (03.5/03.6), forma della terza metrica e del
  bootstrap (03.8). Dove la proposta le nomina, dichiara la dipendenza e si ferma.
- **`APERTURA_SOTTOFASI_FASE03.md`** resta non tracciato: non era fra i file autorizzati al commit.

## 5. Decisioni ancora necessarie

1. Confermare l'opzione (a′), o scegliere (a)/(b)/(c). La colonna «Decisione da chiudere in» del
   punto 2 indicava §1 «separato tra harness riutilizzabile e artefatto»: la proposta se ne discosta e
   spiega perché (§4 b).
2. Regola copia/import per `code/tep_features.py`, `tep_verbalize_v2.py`, `verbalizer_config_v2.json`,
   `evaluate_verbalizer_v2.py` (vincola 03.6 e 03.9).
3. Sanare o no il precedente di Fase 02 con la riga PROVENIENZA di §5.4.
4. Se e quando committare `APERTURA_SOTTOFASI_FASE03.md`.

## 6. `python3 docs/test_explanation.py`

| Momento | Risultato |
| --- | --- |
| Prima (HEAD `b7f359f`, prima di creare il branch) | `Ran 35 tests` — **FAILED (failures=14, skipped=1)** |
| Dopo (con i due file nuovi) | `Ran 35 tests` — **FAILED (failures=14, skipped=1)** |

Numero di partenza dichiarato in `MAINTENANCE.md` §5: 14 al 2026-09-11, preesistenti e relativi ai
walkthrough v1 (`test_step27_qwen_*`, `test_condition_c_*`, `test_one_flow_*`). Invariato. Il test
non copre `studio2/`, quindi l'invarianza non è prova di correttezza della proposta.

## 7. Commit

**Sì**, un solo commit sul branch `codex/studio2-perimetro-q8`, con i soli due file di §2:

```
studio2(fase03): propone il perimetro del codice Q8 (sotto-fase 03.4) con inventario di phase_b/ e code/
```

Non è un congelamento (§8.4): nessun tag. L'integrazione in `main` è ammessa su richiesta
dell'autore (§8.6), ma la sotto-fase si considera chiusa solo dopo `VERIFICA_PERIMETRO_Q8.md`
(verdetto in prima riga, modello e finestra dichiarati) e la conferma dell'autore sulla decisione.
