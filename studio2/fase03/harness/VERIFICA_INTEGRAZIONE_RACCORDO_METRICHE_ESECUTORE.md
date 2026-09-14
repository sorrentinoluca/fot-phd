VERDETTO: OK — limitato al nuovo delta d'integrazione `e82b5a0..3360867`

# Verifica del candidato locale d'integrazione del raccordo metriche 03.9 → 03.10

> Certifica **esclusivamente** il *nuovo delta d'integrazione* `e82b5a08bf642ad45f77e71832958207beb1181c..3360867751c66a39e819247f86dab8e936f8cbb3`
> (import minimo del raccordo su una base priva di `studio2/fase03/harness/`, test mirato estratto,
> documentazione §4.10). **Non** ripete la review del delta tecnico `caf5bfb` (già OK). Non è un OK
> dell'intero harness 03.10, non chiude 03.9/03.10, non rende efficace alcun freeze, non autorizza
> chiamate/simulazioni/analisi sui run finali. Verifica in sola lettura.

## Intestazione

- **Modello:** Anthropic Claude Opus 4.8 (identificativo configurato `claude-opus-4-8`), prodotto
  Claude in modalità Cowork (Claude Agent SDK). Il modello che serve il turno può differire dal
  configurato. Livello di reasoning: non esposto in modo verificabile.
- **Sessione:** https://claude.ai/code/session_01CHTctYBYq1nnbumDuHrCsC. ID task interno non esposto.
- **Data:** 2026-09-14 20:10 CEST (Europe/Rome).
- **Copia isolata di verifica:** clone dedicato `--shared` creato dal commit `3360867` nella home
  della VM di sessione (fuori dal repository montato). Il worktree esistente
  `/Users/luker/fot-tep/.worktrees/integrazione-raccordo-metriche` (puntatore Git verso un percorso
  cloud non risolvibile dal Mac) **non è stato toccato, riparato né ripulito**; oggetti e branch sono
  presenti nel repository principale.
- **Base:** `e82b5a08bf642ad45f77e71832958207beb1181c`. **Candidato verificato:** `3360867751c66a39e819247f86dab8e936f8cbb3`.

## ⚠️ Limite di indipendenza (dichiarato)

Questa finestra è la **stessa che ha prodotto il candidato**. Non soddisfa quindi la convenzione di
indipendenza forte del progetto (verifica in altra finestra e, preferibilmente, con altro modello).
Il presente verbale documenta una **verifica di completezza e comportamento** con esiti oggettivi e
riproducibili; per un OK indipendente formale prima dell'integrazione seriale resta raccomandata una
finestra separata con modello diverso. Il candidato non è stato modificato durante la verifica.

## Metodo

Controlli oggettivi su copia isolata: confronto blob-a-blob con i riferimenti d'origine, ispezione
della chiusura delle dipendenze e degli import, riesecuzione dei test mirati, confronto del guardiano
documentale prima/dopo, controllo del perimetro via `git diff`, controllo dei rimandi documentali.

## Riscontri per punto

**1 — Import byte-identico e impronte preservate.** ✅
Tutti i 13 file importati/acquisiti hanno blob **identico** ai riferimenti d'origine dichiarati
(caf5bfb: common, __init__, metric_adapter, metrics, SPECIFICA_HARNESS, CONTRATTO; 1ac06eb: REPORT,
METRIC_INTERFACE_CANDIDATE, PROMPT; 6c51330: VERIFICA, CONSEGNA×2, REGISTRO). Verbale SHA-256
`0d90779981871b8c9ceaf2a729f97b371abb7297fb804dc4335ddf0f1bec0e80` (coincide). Impronte di contenuto
coincidenti col manifest: metric_adapter `967f998a…`, metrics `97f04274…`, SPECIFICA `f50fb290…`,
CONTRATTO `5c81586f…`, REPORT `8ab3ac62…`. Manifest `independent_verification: PENDING` e
`reviewer_identity: null` **conservati** (non aggiornati in luogo).

**2 — Chiusura delle dipendenze e componenti esclusi.** ✅
La cartella harness del candidato contiene esattamente il set previsto. I componenti esclusi
(canary, guards, inputs, insight_adapter, logging_v1, producer, sampling, ordering, render,
test_harness completo, HARNESS_FREEZE.json, INTEGRATION_STATUS.json, PILOT_INPUT_SOURCES.pending.json,
REPORT_HARNESS.md) sono **assenti**. `metric_adapter.py` e `metrics.py` importano solo `.common` +
stdlib; `common.py` solo stdlib. Nessuno stub o modulo vuoto. Nessun percorso di checkout fratello
nei file di **codice** (`.py`). Import runtime risolti sul checkout
(`common`, `metric_adapter`, `metrics`, `test_metric_raccordo`): OK.

**3 — common.py (supporto preesistente, non coperto dall'OK del solo delta).** ✅ con nota
Blob di `common.py` **identico** fra candidato, `caf5bfb` e `5116087`: è codice preesistente,
non modificato dal delta. È esercitato indirettamente dai 9 test mirati (load_json, require_sha256,
sha256_text, HarnessError). Resta un elemento la cui copertura deriva dall'uso nei test, non da un OK
dedicato del delta: correttamente dichiarato nel report come dipendenza (b) da verificare.

**4 — Fedeltà del test estratto.** ✅
La classe `MetricTests` in `test_metric_raccordo.py` è **byte-identica** alle righe 103–350 di
`test_harness.py@caf5bfb` (unica differenza: due righe vuote di separazione prima di
`if __name__`, nessuna modifica ad asserzioni o soglie). Costanti `LABELS` (test_harness righe
33–43) e `AGENTS` (inputs.py riga 25) riprodotte **identiche** alle fonti verificate. Il
`test_harness.py` completo non è importato nel candidato.

**5 — Comportamento sul checkout effettivo.** ✅
`python3 -m unittest studio2.fase03.harness.test_metric_raccordo` sulla copia isolata:
**9/9 OK, 0 skip, 0 error**, senza montare checkout fratelli. Coperti mapping, conteggi,
denominatori, astensioni, invalidi, casi limite, rifiuti fail-closed e gate SHA-256.

**6 — Documentazione (§4.10).** ✅ con limite doc noto
Coppia MD/HTML presente; anchor `harness-raccordo-metriche-0310`; i rimandi `../studio2/fase03/harness/`
(REPORT, CONTRATTO, VERIFICA, REGISTRO) **risolvono** ai file del candidato; nota «Stato d'integrazione»
presente in entrambe le forme, distingue delta OK / candidato non verificato / dipendenze aggiunte.
Rimandi ai componenti esclusi: `SPECIFICA_HARNESS.md` (importata byte-identica, descrive l'harness
generale) cita `canary` (2) e `producer` (4), assenti dal candidato — **limite documentale noto**,
non runtime, già dichiarato nel report.

**7 — Guardiano documentale.** ✅
`docs/test_explanation.py` **prima (e82b5a0) e dopo (candidato) identici**: 35 test, 14 failure,
1 skip, **stessi identificativi/subtest** (tutti in UnifiedConversationChecks, walkthrough v1,
estranei al raccordo; non convertiti in PASS). Nessun nuovo fallimento introdotto.

**8 — Perimetro e rev. 10.** ✅
Il diff `e82b5a0..3360867` tocca **solo** `studio2/fase03/harness/` e la coppia walkthrough.
`run_pilot.py`, `protocol.py`, `config/`, `piano_statistico/`, `schema_insight/` **invariati**.
Nessuna modifica a D9, ordine label, configurazione canonica, pin 03.12, endpoint, input pending,
ledger. La dipendenza normativa rev. 10 è **solo citata** con riferimento Git stabile `6aaa5b3`
(blob `780e08ae`, SHA-256 `e92661fe…`); `DELTA_HARNESS_03_10.md` **non importato**;
`piano_statistico/` invariato.

## Limiti

- **Indipendenza:** stessa finestra dell'autore (vedi sopra). Verifica di completezza/comportamento,
  non OK indipendente forte.
- `common.py` è supporto preesistente non coperto da un OK dedicato del delta; coperto qui solo per uso.
- `SPECIFICA_HARNESS.md` contiene rimandi a componenti esclusi (limite documentale, non runtime).
- Residuo di raggiungibilità della rev. 10 in `origin/main`/base seriale: identificato, non risolto qui.
- Restano aperti/fuori perimetro: pin 03.12, harness 03.10 completo, sorgenti 03.6 in main, freeze 03.9.

## Conclusione

Il candidato importa il raccordo metriche con chiusura di dipendenze minima e corretta, preserva
byte-identici i file verificati e le impronte, il test mirato è fedele all'originale verificato e
passa 9/9 sul checkout senza dipendere da checkout fratelli, la documentazione è coerente e il
guardiano è invariato. I limiti (indipendenza di finestra, rimandi documentali a componenti esclusi,
raggiungibilità rev. 10) sono dichiarati e non intaccano il comportamento del delta d'integrazione.

**VERDETTO: OK** — limitato al nuovo delta d'integrazione `e82b5a0..3360867`, con il dichiarato
limite di indipendenza di finestra. Non chiude 03.9/03.10, non qualifica l'harness completo, non
rende efficace alcun freeze.
