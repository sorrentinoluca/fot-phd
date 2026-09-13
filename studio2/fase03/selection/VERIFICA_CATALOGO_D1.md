OK

# Verifica indipendente — D1 e catalogo degli otto fault

Data: **2026-09-13**. Verificatore: **Codex**; modello richiesto per il sottoagente dal tool:
**gpt-5.6-sol**; autoidentificazione disponibile nel contesto: **GPT-5**. Agente/finestra separata
`/root/verifica_criteri`.

Oggetto limitato a D1 e alla sua catena di attestazione. Non sono stati aperti risultati per-fault,
sonde o predizioni. La ricostruzione indipendente è stata scritta soltanto in
`/tmp/fot-tep-d1-independent-replay.json`. `PROPOSTA_OOD_D11.md` è stata letta esclusivamente per
verificare che non entrasse nel filtro o nell'esito D1; OOD e D11 non sono valutate né decise qui.

## 1. Riscontri positivi

| Esito | Riscontro |
| :---: | --- |
| ✅ | Il tag annotato `studio2-fase03-criteri-selezione-frozen-001` esiste localmente e sul remoto come oggetto tag `e2a7c49…`, risolve al commit `9faecaf7337e5864b7a3ad44cadb8971853dd260`, e quel commit coincide con `origin/main`. Il messaggio del tag limita correttamente il freeze ai criteri e dichiara D1 non eseguita. |
| ✅ | `CRITERIA_FREEZE.json` revisione 1 è byte-identico alla copia nel tag: **2.284 byte**, SHA-256 `ecae57172d6a83d8b0943f5a9f47b49a3966b96e2fb47f807a9ff61449755c9b`. I quattro snapshot normativi elencati nella rev. 1 restano invariati. |
| ✅ | Una implementazione indipendente, senza importare o invocare `draw_d1.py`, ricostruisce **330** quadruple candidate e **12** ammissibili nello stesso ordine. Le composizioni sono cinque 3/2/1/2 e sette 2/3/1/2; F14/F15 sono forzati e compare esattamente uno fra F3/F9. |
| ✅ | Il replay indipendente dei byte ASCII/UTF-8 `studio2-fase03-D1-v1|20260913|0` produce SHA-256 `0116bf108b82d515210233f433caa65f0b91d9fe46a18fc9d25a1294b8a644f0`. Con N=12, `2^256 mod 12 = 4`, il primo digest è accettato, `x mod 12 = 0`, e seleziona i nuovi fault **F2/F3/F14/F15**; catalogo **F1/F2/F3/F8/F10/F13/F14/F15**. Nessun contatore è rifiutato. |
| ✅ | Lista, digest, indice, catalogo, conteggi di meccanismo 3/2/1/2 e H={F3,F15} in `D1_DRAW_LOG.json` coincidono con la ricostruzione indipendente. `CATALOG_FREEZE.json` trascrive correttamente gli otto record e tutte le impronte elencate coincidono con i file correnti. |
| ✅ | `PROPOSTA_OOD_D11.md` è successiva logicamente al catalogo, dichiara stato non vincolante e non compare fra input, vincoli, file o hash del sorteggio. Non emerge alcuna influenza della proposta su D1; essa usa il catalogo come input, non viceversa. |
| ✅ | La nuova sezione 6 di `studio2/PROVENIENZA.md` identifica registro, freeze rev. 1, fattibilità, fonti esterne tramite il registro e piano; marca la procedura pre-specificata e distingue la proposta OOD/D11 dal freeze del catalogo. |

## 2. Problemi bloccanti del primo riesame

| Esito | Problema e correzione richiesta |
| :---: | --- |
| ❌ | **Ordine di sicurezza nello script.** `draw_d1.py` esegue `enumerate_admissible()` e `draw_index()` prima di verificare l'hash del registro congelato. Con un registro alterato calcolerebbe ed esporrebbe comunque il digest/indice/catalogo, fermandosi solo dopo. Il preflight su tag, commit, manifest rev. 1 e hash normativi deve precedere enumerazione e qualunque SHA del sorteggio. |
| ❌ | **Replay non byte-stabile dopo il commit.** Il campo `worktree_head_at_draw` deriva da `git rev-parse HEAD`; manca il parametro esplicito descritto dalla docstring. Dopo il commit D1 un replay produrrebbe byte diversi dall'originale pur con lo stesso sorteggio. Occorre conservare lo script eseguito come snapshot, e rendere il replay corretto esplicito e vincolato al commit originale `9faecaf`, senza attribuirgli retroattivamente l'esecuzione originaria. |
| ❌ | **Stato della revisione 2 non separato dalla revisione 1.** `CRITERIA_FREEZE_rev002.json` eredita `effective_when`, `freeze_tag`, `independent_review` e `source_commit` della rev. 1. Quelle condizioni sono già soddisfatte, mentre la rev. 2 e il nuovo stato `d1_draw_executed=true` non sono contenuti nel vecchio tag e non hanno ancora questa verifica o il tag D1. La rev. 2 deve distinguere l'origine immutabile dei criteri dal proprio stato pending, dalla propria verifica, dal commit di consegna e dal nuovo tag del catalogo. |

## 3. Coerenza degli stati al primo riesame

| Esito | Riscontro |
| :---: | --- |
| ✅ | `D1_DRAW_LOG.json` descrive un sorteggio eseguito; `CATALOG_FREEZE.json` dichiara `draft_pending_independent_review`, `d1_draw_executed=true`, `catalog_frozen=false`; il catalogo non è quindi ancora presentato come efficace. |
| ⚠️ | La coerenza è rotta nella sola `CRITERIA_FREEZE_rev002.json`: il nuovo stato D1 è reale, ma i metadati di efficacia ereditati dalla rev. 1 possono far apparire la revisione già verificata e pubblicata. È il terzo blocco sopra. |
| ✅ | `scientific_protocol_frozen=false`, `model_execution_authorized=false`, `per_fault_results_opened=false` e `model_calls=0` delimitano correttamente l'ambito dei record. L'assenza assoluta di attività esterne non registrate non è provabile dal repository, ma nessun elemento del calcolo dipende da risultati sperimentali. |

## 4. Verdetto del primo riesame

**NON OK — risultato numerico e catalogo sono corretti, ma la catena eseguibile e le attestazioni
non sono ancora congelabili.** Prima del commit/tag occorre correggere i tre problemi di §2,
preservando separatamente lo script realmente eseguito e il log originale. Dopo le correzioni serve
un riesame mirato di script snapshot/replay, manifest del catalogo e revisione 2; le fonti normative
e la bibliografia già verificate non vanno riaperte.

## 5. Riesame mirato dopo le correzioni

Il riesame è stato eseguito sugli artefatti stabilizzati dopo il NON OK di §4, senza riaprire le
fonti normative già verificate e senza accedere a risultati per-fault, sonde o predizioni. Non è
stato eseguito un nuovo sorteggio: il solo replay è stato scritto in
`/tmp/fot-tep-d1-corrected-replay-review2.json`.

| Esito | Riscontro |
| :---: | --- |
| ✅ | **Provenienza dell'esecuzione preservata.** `execution_snapshot/draw_d1.py` coincide con i byte osservati prima della correzione: **9.846 byte**, SHA-256 `b9fba113ade9729b0f59469b31e412ebb0c4ed0d2bc53ce580b65bd3e536f06b`. Il log originario resta **4.926 byte**, SHA-256 `fa571e89054a004021b08e93cd857ad4b8d41794b8c070260a49d4fb03a08b95`. Il report e il manifest attribuiscono l'esecuzione a questo snapshot e presentano lo script corrente soltanto come replay corretto. |
| ✅ | **Preflight prima di catalogo e digest.** Nel flusso corrente `validate_frozen_context()` precede `enumerate_admissible()` e `draw_index()`. Controlla contesto/data registrati, natura annotata e target del tag dei criteri, ascendenza del commit, hash e blob del manifest rev. 1, i quattro snapshot al suo `source_commit` e l'hash del registro normativo. Una prova ulteriore con manifest alterato in un clone temporaneo è terminata prima di chiamare enumerazione o digest. |
| ✅ | **Replay stabile e log protetto.** `--draw-context-commit` accetta soltanto `9faecaf7337e5864b7a3ad44cadb8971853dd260`; il record usa questo contesto storico anche quando HEAD avanza. Il replay corretto (12.483 byte, SHA-256 `60fa97d48ef6899b4e4fe17f12907361461d73ff4d9f14769e1da9e93a6ced6c`) ha prodotto un file byte-identico a `D1_DRAW_LOG.json`. La destinazione canonica del log viene rifiutata. |
| ✅ | **Test mirati.** Passano tutti i quattro test di `test_draw_d1.py`: replay identico dopo avanzamento di HEAD, registro alterato respinto prima di enumerazione/digest, contesto non registrato respinto prima del digest, log originario non sovrascrivibile. |
| ✅ | **Manifest del catalogo.** Le sette coppie SHA-256/dimensione di `CATALOG_FREEZE.json` coincidono con i file correnti. `integrity_basis=content_addressed_review_package_pending_commit` descrive correttamente che log e snapshot appartengono all'esecuzione originaria, mentre replay e test sono stati aggiunti durante il riesame; richiede il confronto dei byte elencati col futuro tag del catalogo e non li attribuisce a `worktree_head_at_draw`. Catalogo, digest, origine dei fault e stati restano coerenti con la ricostruzione indipendente. |
| ✅ | **Revisione 2 separata dalla revisione 1.** `CRITERIA_FREEZE_rev002.json` colloca sotto `criteria_origin` il freeze storico dei criteri e assegna al proprio stato D1 verifica, condizione di efficacia e tag dedicati. `supersedes` identifica la rev. 1 rimasta byte-identica al tag dei criteri. Gli hash diretti di rev. 1, log, snapshot eseguito, catalog manifest e replay coincidono; coincidono anche i quattro snapshot storici al `criteria_origin.source_commit`. La lista `changed_fields`, includendo per convenzione il campo autoriferito, è esattamente la differenza delle chiavi di primo livello rispetto alla rev. 1. Nessun criterio normativo è cambiato. |
| ✅ | **Proposta OOD/D11 ancora fuori dal freeze.** Le correzioni e il nuovo §6 del report non introducono la proposta negli input o nella procedura D1 e non decidono OOD o D11. |

## 6. Verdetto corrente e limiti

**OK — i tre problemi bloccanti del primo riesame sono risolti.** Il risultato D1, il catalogo,
la provenienza dell'esecuzione originale, il replay e la separazione amministrativa fra rev. 1 e
rev. 2 formano ora un pacchetto coerente e verificabile, pronto per il successivo passaggio
documentale e di pubblicazione autorizzato.

Al momento del controllo `CATALOG_FREEZE.json` e `CRITERIA_FREEZE_rev002.json` dichiarano ancora
`draft_pending_independent_review`, `catalog_frozen=false`; nella rev. 2 il verdetto incorporato è
`null`. È coerente con un pacchetto ancora non committato mentre questa verifica viene scritta e non
attesta una pubblicazione già avvenuta. L'efficacia richiede ancora che i byte finali siano
committati in una revisione raggiungibile da `origin/main` e inclusi nel tag annotato D1 proposto.
Qualunque aggiornamento successivo dei manifest per registrare questo OK cambia le loro impronte e
richiede un controllo finale mirato di parità con commit e tag; non richiede di ripetere il sorteggio
o la verifica bibliografica. Le dichiarazioni `model_calls=0`, `per_fault_results_opened=false` e
l'assenza di rilanci sono coerenti con i record ispezionati, ma l'assenza assoluta di attività non
registrate non è dimostrabile dai soli file.
