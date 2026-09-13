# Report della sotto-fase 03.7 — pseudolabel opache, assegnazione degli agenti e derangement di E

Data: **2026-09-13**. Piano §6.5, D10, §8.1, §8.2, §8.4. Branch `codex/studio2-pseudolabel`, base
`d815ce9` (attuazione 03.4); worktree dedicato. Profilo dichiarato in apertura: implementativo
combinatorio con congelamento. Stato: **sotto-fase eseguita, congelamento in attesa di verifica
indipendente** (`VERIFICA_PSEUDOLABEL.md`, altra finestra, altro modello). La Fase 03 **non** è
chiusa.

## 1. Riassunto e risultati

**Specifica prima dell'esecuzione** (`SPECIFICA_PSEUDOLABEL.md`, commit `221bf58`). Congelati:
namespace `studio2-fase03-pseudolabel-v1`; seed `20260913` (entra solo nei derangement); label
= `S2-CLS-` + primi 5 caratteri base32 di SHA-256(`namespace|label|<identifier>|<counter>`), con
`identifier` = campo `label` del catalogo (`F1`…`F15`); rifiuto e incremento del contatore per
collisione o se il suffisso contiene le cifre dell'idv del proprio fault; `Normal` letterale in
ultima posizione; `label_space` = otto label in ordine lessicografico + `Normal`; assegnazione
= fault ordinati per SHA-256(`namespace|assignment|<identifier>`), il k-esimo è locale ad
`agent_k`; derangement = per agente un indice uniforme fra i 1854 derangement dei 7 peer
(ordine lessicografico delle permutazioni), rejection sampling su parole a 32 bit da
SHA-256(`namespace|seed|derangement|<agent_id>|<i>`), peer ordinati come in `label_space`.
Guardia sul catalogo D1: SHA-256 `68b8461a…`, lista `[1,2,3,8,10,13,14,15]`, tag
`studio2-fase03-catalogo-D1-frozen-001` (commit `ab43f0b2…`).

**Esecuzione** (commit `8c90ece`): dichiarata singola dall’autore originale, nessun rilancio dichiarato, contatori di collisione tutti a 0,
zero parole rifiutate nel rejection sampling. Zero chiamate a modelli, zero simulazioni.

**Le nove label** (questa tabella di mapping è evaluator-side, mai in un prompt; le sole label operative possono comparire nei prompt):

| Identificatore | idv | Pseudolabel |
| --- | ---: | --- |
| F1 | 1 | `S2-CLS-TYFPG` |
| F2 | 2 | `S2-CLS-GSX3L` |
| F3 | 3 | `S2-CLS-QRCCB` |
| F8 | 8 | `S2-CLS-HEW25` |
| F10 | 10 | `S2-CLS-MHMU4` |
| F13 | 13 | `S2-CLS-FD3GZ` |
| F14 | 14 | `S2-CLS-4AMS4` |
| F15 | 15 | `S2-CLS-3ZGWQ` |
| Normal | — | `Normal` |

`label_space` = `3ZGWQ, 4AMS4, FD3GZ, GSX3L, HEW25, MHMU4, QRCCB, TYFPG` (con prefisso), poi
`Normal`. `Unknown` non esiste come label: è l'astensione (D10).

**Assegnazione agente → fault locale** (evaluator-side):

| Agente | Fault locale | Pseudolabel |
| --- | --- | --- |
| agent_1 | F10 | `S2-CLS-MHMU4` |
| agent_2 | F3 | `S2-CLS-QRCCB` |
| agent_3 | F2 | `S2-CLS-GSX3L` |
| agent_4 | F8 | `S2-CLS-HEW25` |
| agent_5 | F13 | `S2-CLS-FD3GZ` |
| agent_6 | F15 | `S2-CLS-3ZGWQ` |
| agent_7 | F14 | `S2-CLS-4AMS4` |
| agent_8 | F1 | `S2-CLS-TYFPG` |

**Derangement di E** (vista per identificatore; la forma operativa `pseudolabel → pseudolabel` è
in `CONDITION_E_DERANGEMENTS.json`; indici scelti 1619, 1422, 1716, 1201, 919, 620, 1203, 1196):

| Agente | Mappa sui 7 peer (sorgente → destinazione) |
| --- | --- |
| agent_1 | F15→F1, F14→F13, F13→F14, F2→F3, F8→F2, F3→F8, F1→F15 |
| agent_2 | F15→F10, F14→F8, F13→F15, F2→F13, F8→F2, F10→F1, F1→F14 |
| agent_3 | F15→F1, F14→F8, F13→F3, F8→F13, F10→F15, F3→F14, F1→F10 |
| agent_4 | F15→F10, F14→F1, F13→F2, F2→F15, F10→F13, F3→F14, F1→F3 |
| agent_5 | F15→F8, F14→F1, F2→F3, F8→F2, F10→F14, F3→F15, F1→F10 |
| agent_6 | F14→F8, F13→F14, F2→F13, F8→F10, F10→F2, F3→F1, F1→F3 |
| agent_7 | F15→F10, F13→F1, F2→F8, F8→F15, F10→F3, F3→F2, F1→F13 |
| agent_8 | F15→F8, F14→F3, F13→F14, F2→F10, F8→F13, F10→F15, F3→F2 |

Nessun agente ha ricevuto la rotazione di un passo; nessun punto fisso; ogni mappa è una biiezione
dei suoi 7 peer e non tocca la label locale.

**Test** (`test_pseudolabel.py`, `python3 -m unittest studio2.fase03.pseudolabel.test_pseudolabel`):
**21/21 OK** nell’esecuzione originale. Coprono: 9 label uniche, con uguale lunghezza delle sole 8 label opache (`Normal` è letterale); regex di `protocol.PSEUDOLABEL` e
`protocol._validate_label_space`; `Normal` letterale e ultimo, `Unknown` assente; identificatori
uguali al catalogo congelato; opacità — test dichiarato: nessun suffisso contiene le cifre
dell'idv del proprio fault, né `F<idv>`, né `F` seguito da cifra; ordine lessicografico delle
label diverso dall'ordine del catalogo e dal suo inverso, con Spearman riportato; biiezione
agenti↔fault e coerenza con l'ordine del digest; forma `agents` del manifest; enumerazione dei
derangement = 1854 in ordine lessicografico; zero punti fissi e dominio = 7 peer per tutti gli 8
agenti; `protocol._validate_derangements` accetta gli artefatti; parole del log che riproducono
gli indici; vista per identificatore coerente; generazione deterministica e replay byte-identico
sui file su disco; seed diverso cambia i derangement e non le label, namespace diverso cambia
le label; fallimento (`CatalogMismatch`) se il catalogo differisce per byte o per lista. I 16 test
preesistenti di `studio2/fase03/tests/` restano OK.

**Osservazione e limite del controllo.** La correlazione di Spearman fra ordine del
catalogo e ordine lessicografico delle otto label di fault (esclusa `Normal`) è **−0,833**
(esattamente −5/6): F15, F14 e F13 hanno le tre label lessicograficamente più basse.
Il test implementato (`|ρ| < 1`, ordine ≠ catalogo e ≠ inverso) passa, ma esclude soltanto
una relazione monotona perfetta: non dimostra «nessuna correlazione», come richiesto
letteralmente dal prompt iniziale. Il nome del test è quindi più forte del controllo effettivo.
La specifica fissa la derivazione prima dell’esecuzione; non si sceglie un altro risultato
in funzione della correlazione osservata.

L’autore ha accettato esplicitamente la conservazione del sorteggio unico **dopo aver
osservato questo risultato**, registrando la differenza dal requisito iniziale e senza
introdurre una nuova soglia statistica post-hoc: si veda
[`DECISIONE_ACCETTAZIONE_V1.md`](DECISIONE_ACCETTAZIONE_V1.md).
Nessuna stringa contiene un identificatore esplicito del proprio fault secondo le guardie
implementate; ciò non prova indipendenza statistica o segretezza. Conoscendo namespace,
algoritmo e identificatori il mapping è ricostruibile: questi ingredienti e il mapping
restano evaluator-side, fuori dai prompt sperimentali.
Non si cambia ora l’ordine per compensare −0,833. Un’eventuale regola generale di
presentazione appartiene a 03.10/03.12, deve essere riproducibile e comune alle condizioni
confrontate, e va fissata prima del pilot senza modificare mapping e derangement v1.

**Congelamento** (`PSEUDOLABEL_FREEZE.json`): stato `frozen_pending_independent_verification`,
`source_commit` = `8c90ecec421980211258e9323d4266a32ba70ccd`, `catalog_tag`
`studio2-fase03-catalogo-D1-frozen-001`. Impronte SHA-256:

| File | SHA-256 |
| --- | --- |
| `PSEUDOLABEL_MAP.json` | `b0ce81d53f11038ddf51c9ec964a1e838a7045e2e57b8ac3368f05e9a215bbc6` |
| `AGENT_ASSIGNMENT.json` | `df7434230dcd1d5460cd19e0d27e909efd40289f64d89a4b3fee2a0e55b79fcf` |
| `CONDITION_E_DERANGEMENTS.json` | `34350c7e49b11d29b885da128d4b34ce3df31cd41df7c521cb66421aa1b9d001` |
| `DRAW_LOG.json` | `469da8eac9f84ee007183d10c0c024f4c5bfb293136867cba4ab59e4d974fd03` |
| `pseudolabel_draw.py` | `c4e886695ff0d58e8ea7674f5b29f1075c86a8c065c1a4dd7af142c3b689d410` |
| `test_pseudolabel.py` | `284b366b06ff350a09ebd7d73d43e5431d4660f5f837434b7f9135d7397e80fb` |
| `SPECIFICA_PSEUDOLABEL.md` | `ee7109cd425da639caa0bc6c450b759aea5885cc7daebd6d7dabd619c1f60cef` |

Nessun tag creato. Tag proposto `studio2-fase03-pseudolabel-frozen-001`, alle condizioni
MAINTENANCE §8.4 elencate nel freeze: verifica indipendente OK, commit raggiungibile da
`origin/main`, `--check` superato al commit taggato.

**Interfaccia con 03.12.** Solo il formato della pseudolabel (regex in `protocol.py`) è condiviso.
Se 03.12 lo cambia, la rigenerazione è deterministica e si rifà con namespace
`studio2-fase03-pseudolabel-v2` in nuovi file, senza sovrascrivere v1.

## 2. File toccati

| File | Cosa è cambiato |
| --- | --- |
| `studio2/fase03/pseudolabel/SPECIFICA_PSEUDOLABEL.md` | nuovo: specifica pre-esecuzione (commit 1) |
| `studio2/fase03/pseudolabel/__init__.py` | nuovo: pacchetto |
| `studio2/fase03/pseudolabel/pseudolabel_draw.py` | nuovo: generatore, replay `--check`, `--freeze` |
| `studio2/fase03/pseudolabel/test_pseudolabel.py` | nuovo: 21 test unittest |
| `studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json` | nuovo: mapping evaluator-side e `label_space` |
| `studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json` | nuovo: assegnazione e blocco `agents` |
| `studio2/fase03/pseudolabel/CONDITION_E_DERANGEMENTS.json` | nuovo: derangement per agente |
| `studio2/fase03/pseudolabel/DRAW_LOG.json` | nuovo: log completo del sorteggio |
| `studio2/fase03/pseudolabel/PSEUDOLABEL_FREEZE.json` | nuovo: impronte, commit sorgente, catalog_tag, stato |
| `studio2/fase03/pseudolabel/REPORT_PSEUDOLABEL.md` | nuovo: questo report |
| `studio2/PROVENIENZA.md` | nuova sezione §9 in coda: pattern `derive_opaque_pseudolabel` e forma dell'artefatto E, pre-specificati |

Non toccati, come richiesto: `studio2/fase03/protocol.py`, `run_pilot.py`, `prepare_gate.py`,
`schemas/`, piano, walkthrough, `MAINTENANCE.md`, `phase_b/`, `code/`.

**Collegamento proposto, non attuato** (spetta a 03.10): il manifest del pilot può leggere
`label_space` da `PSEUDOLABEL_MAP.json`, `agents` da `AGENT_ASSIGNMENT.json` e `derangements` da
`CONDITION_E_DERANGEMENTS.json`, dopo aver verificato le impronte contro `PSEUDOLABEL_FREEZE.json`;
`protocol.py` li accetta già così come sono (test `test_protocol_validator_accepts_artifacts`).

## 3. Modello e profilo

Sotto-fase eseguita da un modello capace con ragionamento medio (Claude, finestra Cowork),
profilo implementativo combinatorio con congelamento, come dichiarato in apertura. La sola scelta
mini-decisionale (namespace, seed, regole) è stata fissata nella specifica prima dell'esecuzione.

## 4. Cosa è rimasto fuori

- Lo schema e il contenuto degli insight (03.12), gli esempi locali, i casi di sviluppo e di
  trasferimento (03.6, 03.10): non fissati qui, per specifica §8.
- Il collegamento al manifest del pilot: proposto, non attuato (03.10).
- La sezione del walkthrough studio2: si scrive solo dopo la verifica indipendente.
- Tag, push, merge: non eseguiti.

## 5. Decisioni ancora necessarie (autore)

1. Verifica indipendente (`Verifica_LLM.md`, altra finestra e modello) → `VERIFICA_PSEUDOLABEL.md`.
2. Se OK: integrazione del branch e tag `studio2-fase03-pseudolabel-frozen-001`.
3. **Deciso dall’autore il 2026-09-13:** conservare v1 e il sorteggio unico, registrare il limite
   del test e non cambiare l’ordine ad hoc; eventuale regola generale in 03.10/03.12 prima del pilot
   (`DECISIONE_ACCETTAZIONE_V1.md`).
4. Rimozione del worktree `.worktrees/pseudolabel` dopo l'integrazione.

## 6. `python3 docs/test_explanation.py`

Prima: **14** fallimenti, 1 skipped (35 test). Dopo: **14** fallimenti, 1 skipped. Invariati, tutti
preesistenti; il test non copre `studio2/`.

## 7. Commit

Tre commit sul branch `codex/studio2-pseudolabel`, base `d815ce9`, nel formato di MAINTENANCE §8.3:

1. `221bf58` `studio2(fase03): specifica pre-esecuzione della sotto-fase 03.7 (pseudolabel, assegnazione agenti, derangement di E)`
2. `8c90ece` `studio2(fase03): genera le nove pseudolabel, l'assegnazione fault↔agente e i derangement di E (sotto-fase 03.7)` — codice, test e i quattro artefatti (i test leggono i file su disco: vanno insieme)
3. (questo) `studio2(fase03): congela gli artefatti della sotto-fase 03.7 in attesa di verifica e registra la provenienza del pattern` — freeze, PROVENIENZA §9, report

Nessun push, merge o tag.

## 8. Rettifica documentale del 2026-09-13

Dopo il parere e l’autorizzazione dell’autore, il report precisa il limite del test
di correlazione, la distinzione fra label operative e mapping evaluator-side,
l’eccezione di lunghezza per `Normal` e la natura riproducibile, non segreta, della
derivazione. I risultati dei test in §1 e §6 sono quelli dichiarati dall’autore
originale; i riscontri indipendenti sono nel verbale di verifica. Specifica, codice,
test e tutti gli artefatti elencati nel freeze v1 restano byte-identici.

**Precedenza di 03.12.** `APERTURA_SOTTOFASI_FASE03.md` §5 indica 03.12 → 03.7,
come ordine proposto non ancora approvato, mentre la tabella operativa consente di lavorare da 03.4 e D1. Il lavoro eseguito
è quindi un anticipo limitato alla derivazione combinatoria nel formato v1 già
accettato da `protocol.py`: non chiude l’interfaccia con 03.12. Il formato resta
provvisorio rispetto alla decisione di 03.12; prima del pilot va verificata la
compatibilità finale. Se cambia, si applica la revisione con nuovo namespace e
nuovi file prevista dalla specifica, senza sovrascrivere v1. Questa sotto-fase
non autorizza avvio del pilot o produzione degli insight.

**Limiti della prova di processo.** La storia Git contiene la specifica prima del
commit di generazione e un unico insieme di artefatti. Replay e log deterministici
non possono dimostrare che non siano esistite esecuzioni private non registrate:
«singola esecuzione» resta una dichiarazione dell’autore originale coerente con
la storia disponibile. Il rejection sampling elimina il bias dell’operazione
modulo assumendo parole uniformi; l’impiego di SHA-256 è pseudocasuale e
deterministico, non una prova empirica di randomizzazione uniforme.
