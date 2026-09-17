OK

# Verifica indipendente della sotto-fase 03.13 — capability pilot Qwen su `pilot-03`

Data della verifica: 2026-09-17, Europe/Rome.  Finestra: `b567` (“Verifica integrazione finale
D9 Qwen”). Modello: `gpt-6-astra`, reasoning `high`. La verifica segue
`docs/prompts/Verifica_LLM.md`, `docs/MAINTENANCE.md` §8.6 e i criteri di controllo indipendente
del ledger durevole. Non sono state effettuate chiamate a provider, aperture di tunnel, esecuzioni
scientifiche, retry, resume, merge su `main`, commit, push o tag.

## Oggetto verificato

| Voce | Valore verificato |
| --- | --- |
| Worktree candidata | `/Users/luker/fot-tep/.worktrees/rem6-riconciliazione` |
| Branch | `codex/studio2-riconciliazione-stop-contabile` |
| Commit | `9937ce3e5801ff455b60b45f7f532373daaa941c` |
| Tree | `be4520da313607c8052462b465d6124448a0ceb2` |
| Parent / codice di riferimento | `d3f8f844e5be4244477fc294ca754528e6938b15` |
| Subject | `studio2(fase03): registra esecuzione finale pilot-03 e report di sotto-fase` |
| `origin/main` usato per la prova di merge | `c633dcef618afa1226ed09366a9ed1680213fc72` |
| Ledger finale | SHA-256 `93ff83a5a4132800c2973fe6687c8e0ffcdb07d33f293a8517ca715ff8dc4089` |
| Archivio locale | 9.021.440 byte; SHA-256 `30cdd5ca5715695bae4cc61c3b3919d3949f471c768d008d87395430d9c2c3b8` |
| Verbale d'esito copiato | SHA-256 `1ce0a466586a65993d1269476f9de8a4812b9f64a20eae71cd9aec7e8bee4b70`, byte-identico all'originale in `b567` |

## Esito delle verifiche 1–7

| N. | Verifica | Esito | Evidenza indipendente |
| ---: | --- | --- | --- |
| 1 | Identità e perimetro del commit | **PASS** | Commit, tree e parent coincidono. Il delta dal parent contiene 26 file: 25 artefatti censiti dal manifest più il manifest stesso. Sono presenti soltanto evidenza, log, report, walkthrough e manifest; nessun file di codice o configurazione runtime è nel delta. I blob del codice sono quindi byte-identici al parent. `git diff --check` è pulito e il subject è conforme. |
| 2 | Ledger, quote, gate e T5 | **PASS** | Dopo `lsof` vuoto, il ledger reale è stato interrogato esclusivamente con URI SQLite `mode=ro&immutable=1`. Sono stati ricalcolati 156 tentativi nativi e 5 di lineage, cioè 161 cumulativi su 167 pianificati e hard stop 200. Per stage: 1 tecnica, 8 producer, 10 remediation, 14 alternate, 3 sonda, 120 gate. Il gate contiene 119 `COMPLETED` e 1 `FAILED`, zero troncamenti e la sola divergenza di validità `S2-P03-002`. Le 8 leaf finali 27B sono valide; la sonda è 3/3 e il digest congelato è `de1f59ceb28e50cd8b9027874f5d2d22cb1337ceab2e4dda8c2adda4b2dda6f2`. Media/p95: 26,208619/36,660866 s per il gate e 34,042580/37,167291 s per le leaf 27B. Sul conteggio conservativo di 7.174 richieste, `1,20×T` è 62,694435 h alla media e 87,669701 h al p95, entrambe entro W=168 h. |
| 3 | Coerenza fra evidenza, report, §4.13 e nota metodi | **PASS** | Numeri, identità, fingerprint, deviazioni e cronologia coincidono. Sono dichiarati thinking disattivato sui producer, remediation, riconciliazioni di STOP e sospensione, revisione della config, quota `requalification`, W/T5 e passaggio del GO R=3 da subordinato a definitivo il 2026-09-17. Il confronto 122B/27B è esplicitamente descrittivo e fra pipeline configurate; non è formulato alcun claim di effetto. Il risultato del primo studio è rimosso come fonte citabile. I parametri operativi S/U/d/X/Q da congelare restano correttamente indicati come lavoro successivo; il margine T5 verificato corrisponde a 12.053 retry alla media o 6.573 al p95. |
| 4 | Log, hash, segreti e redazione | **PASS** | Sono presenti i 15 log dei run richiesti, più `CHIUSURA_03_13_verification.log` e `REDACTION_INDEX.json`. I 25 hash degli artefatti repository dichiarati nel manifest sono stati ricalcolati senza mismatch. I 14 run log non redatti sono byte-identici alle sorgenti. Nel log della sonda la sola differenza è l'oggetto `prompt_sample`: 40 record con testo e `true_pseudolabel` sono sostituiti da conteggio e digest canonico `602e93270f33d2394b275167256cab61d8a41862bf1b5324748d345b3c31df7b`; tutto il resto è identico. Nessun valore compatibile con credenziale, `Authorization: Bearer`, password o API key è stato rilevato. Il log redatto conserva però il `base_url` HTTP del 122B e path locali, come dichiarato sotto. |
| 5 | Conservazione e archivio | **PASS** | Dopo `lsof` vuoto, tutti i 77 file del runtime risultano presenti, con dimensione e SHA-256 identici a `MANIFEST_CONSERVAZIONE.csv` (0 mancanti, 0 mismatch). L'archivio contiene esattamente gli stessi 77 file, senza extra, e tutti i digest coincidono. Il ledger ha lo stesso SHA prima e dopo la lettura, non ha sidecar WAL/SHM e `lsof` finale è vuoto. L'archivio non è pubblicato; i contenuti da valutare prima della pubblicazione sono elencati sotto. |
| 6 | Walkthrough e guardian | **PASS** | §4.13 ha struttura conforme (`Riassunto`, `Dettaglio`, letteratura, critiche, artefatti, lavoro residuo), anchor unico `pilot-qwen-0313` e parità semantica MD/HTML (1.174 token normalizzati, identici). La sintesi divulgativa rinvia all'anchor. La sezione dichiara verifica ancora in attesa, runtime/release fuori Git, freeze/tag non eseguiti, mancata integrazione in `main` e Fase 03 non chiusa. Il guardian resta separato e **NON PASS**, ma è invariato: 35 test, 14 failure, 1 skip e identico insieme di failure prima/dopo. |
| 7 | Prova di merge | **PASS** | In una worktree temporanea creata da `origin/main` `c633dce`, il merge `--no-commit --no-ff` ha prodotto esattamente tre conflitti: i tre walkthrough. La risoluzione con le versioni del branch elimina tutti i conflitti e i blob coincidono con `9937ce3`; `git diff --check --cached` è pulito. La discovery completa del harness nell'ambiente arm64 coerente ha superato **232/232** test. Un primo avvio con Python x86_64 aveva prodotto soli errori ambientali per una wheel `rpds` arm64 incompatibile; nessun errore è rimasto nell'ambiente coerente. Le worktree temporanee sono state rimosse. |

## Ricalcolo del ledger

Il conteggio distingue tentativi provider, risposte durevoli e output logici: il ledger contiene
156 richieste native, 148 risposte, 148 receipt, 5 record di lineage e 309 eventi. La scomposizione
dell'alternate è 14 tentativi provider: 5 `ZERO_TOKEN_PROVEN`, una risposta completata ma sospesa e
troncata, una requalification valida e 7 ulteriori leaf valide. Le leaf finali sono quindi 8; non si
confondono i 14 tentativi con gli 8 output logici.

La formula verificata per la proiezione completa è:

`6.732 + 192 + 64 + 70 + 8 + 8 + 100 + 0 = 7.174`, di cui 7.166 richieste sul 122B e 8 sul 27B.
Applicando le latenze ricalcolate si ottengono `T=52,245362 h`, `1,20×T=62,694435 h` alla media e
`T=73,058084 h`, `1,20×T=87,669701 h` al p95. Il solo nucleo 5.184×R3 equivale a 45,29 h con il
margine del 20 %. Il PASS T5 vale per l'inviluppo dichiarato nel report; il freeze operativo
successivo deve mantenere S/U/d/X/Q entro tale inviluppo e il relativo margine.

## Contenuti dell'archivio da valutare prima della pubblicazione

Il prefisso comune degli elenchi seguenti è `studio2-fase03-d9-pilot-03/`.

### Endpoint o `base_url` — 12 file

- `ledger.sqlite3`
- `execution/pilot_d9_successor_candidate_03_13.private.json`
- `execution/pilot_d9_successor_candidate_03_13.private.json.pre_authorization`
- `execution/pilot_d9_successor_candidate_03_13.private.json.pre_rev2`
- `execution/producer_122b_successor_03_13.private.json`
- `execution/producer_27b_successor_03_13.private.json`
- `execution/producer_27b_successor_03_13.rev2.private.json`
- `execution/service_122b_successor_03_13.private.json`
- `execution/service_27b_successor_03_13.private.json`
- `execution/service_27b_successor_03_13.rev2.private.json`
- `results/budget_20260917T163729.log`
- `results/frozen_gate_config.json`

I valori presenti sono l'endpoint HTTP del 122B `http://cygnusx1.portici.enea.it:8000/v1`, quello
locale del tunnel 27B `http://127.0.0.1:18001/v1` e `/v1/chat/completions`. Non sono certificati TLS
o fingerprint SSH: i fingerprint registrati sono identità applicative restituite da vLLM.

### Path locali assoluti — 26 file

- `ledger.sqlite3`
- `MATERIALIZATION_SUMMARY.private.json`
- `execution/PRE_GATE_ACCEPTANCE_03_13.private.json`
- `execution/pilot_d9_successor_candidate_03_13.private.json`
- `execution/pilot_d9_successor_candidate_03_13.private.json.pre_authorization`
- `execution/pilot_d9_successor_candidate_03_13.private.json.pre_rev2`
- `execution/service_122b_successor_03_13.private.json`
- `execution/service_27b_successor_03_13.private.json`
- `execution/service_27b_successor_03_13.rev2.private.json`
- `lineage/SUCCESSOR_LINEAGE_S5_122B_QWEN_D9_03_13.approval.private.json`
- `lineage/SUCCESSOR_LINEAGE_S5_122B_QWEN_D9_03_13.private.json`
- `prepared/pre_gate_hashes.json`
- `prepared/pre_gate_plan.json`
- `results/alternate_20260917T125137.log`
- `results/alternate_20260917T125401.log`
- `results/alternate_20260917T125847.log`
- `results/alternate_20260917T130137.log`
- `results/alternate_20260917T130331.log`
- `results/alternate_20260917T131707.log`
- `results/alternate_20260917T131826.log`
- `results/budget_20260917T163729.log`
- `results/frozen_gate_config.json`
- `results/remediation_20260917T123528.log`
- `results/remediation_20260917T123723.log`
- `results/remediation_20260917T123804.log`
- `results/remediation_20260917T124316.log`

I path identificano principalmente `/Users/luker/fot-tep-runtime`, la worktree `dd86` e la
worktree `rem6-riconciliazione`; alcuni rimandano anche al ledger di `pilot-001` come fonte di
lineage/qualifica. In questa verifica `pilot-001` e `pilot-002` non sono stati aperti né hashati.

### Approvazioni contenenti il nome letterale `Luca` — 18 file

- `ledger.sqlite3`
- `execution/PRE_GATE_ACCEPTANCE_03_13.private.json`
- `execution/accounting_stop_reconciliation_03_13.private.json`
- `execution/alternate_accounting_approval.private.json`
- `execution/config_revision_01_03_13.private.json`
- `execution/presentation_approval.private.json`
- `execution/producer_failure_diagnosis_03_13.private.json`
- `execution/remediation_approval_03_13.private.json`
- `execution/suspension_reconciliation_03_13.private.json`
- `execution/technical_execution_authorization_03_13.private.json`
- `execution/technical_execution_authorization_03_13.rev2.private.json`
- `execution/zero_token_approval_20938b223df536de1a0d60db604de36cf548f9848316ad3d690bb8b3710726ac.private.json`
- `execution/zero_token_approval_39bc1b4c0e8688634fe922078088845629cb8a0588005cd438de68fa7839b5f8.private.json`
- `execution/zero_token_approval_446216bce69e747d78de900d1f0496e82d21ecc455e7b937d54c9a1863526eed.private.json`
- `execution/zero_token_approval_7bbd56ff476ce612db13f6e43f8e90492fe99d71378c053355f027cf14da426e.private.json`
- `execution/zero_token_approval_8e7d1e72f4a2751aa5d062e0e12e0899b6892f02fc60e3b4e942ada91f9ca14c.private.json`
- `execution/zero_token_approval_9bc178d9999313704cd963e9b2c92a1ecdf42dd21330f50ff57e35b2a103ab9d.private.json`
- `execution/zero_token_approval_dde658fd333ed614ab33a295f72af3a3be7073aef4e7baeeec749abab07f1f71.private.json`

### Prompt, pseudolabel o risposte grezze

Oltre alle categorie richieste, la pubblicabilità deve considerare `ledger.sqlite3`, i tre snapshot
`execution/pilot_d9_successor_candidate_03_13.private.json*`, `prepared/pilot_prompts.jsonl`,
`results/budget_20260917T163729.log`, `results/budget_probe_journal.jsonl`,
`results/frozen_gate_config.json`, i tre journal producer e `results/stability_journal.jsonl`.
Questi artefatti contengono, secondo il file, prompt completi, `true_pseudolabel`, risposte grezze o
record equivalenti. L'assenza di credenziali rilevate non equivale quindi a una decisione di
pubblicabilità.

## Osservazioni non bloccanti

1. Il guardian storico resta intenzionalmente NON PASS (35/14/1); non è una regressione del commit.
2. I `ResourceWarning` su connessioni SQLite non chiuse compaiono sotto Python 3.13 durante la
   discovery, ma i 232 test terminano OK. Non modificano il risultato e non appartengono al delta
   documentale verificato.
3. Il caricamento dell'archivio richiede una decisione esplicita dell'autore sui dati elencati sopra.
   `ARTIFACT_STORAGE.json` resta correttamente `prepared_not_published`.

## Verdetto

Il commit `9937ce3e5801ff455b60b45f7f532373daaa941c` supera le verifiche richieste. Può essere integrato
in `main` e taggato `studio2-fase03-pilot-v1` da Luca. Il presente verdetto non autorizza né esegue
merge, tag o pubblicazione; il caricamento dell'archivio resta una decisione separata di Luca dopo
la valutazione dei contenuti indicati al punto 5.
