"""One explicit reviewed row per original method; no silent exclusions."""
from pathlib import Path
import ast,json,re
E=Path(__file__).resolve().parent;C=E.parent/'candidate'
original=json.loads((E/'original_methods.json').read_text())
old=json.loads((C/'studio2/fase03/harness/non_ok_20260915/evidence/negative_probes.json').read_text())
raw=json.loads((E/'original_all_unadapted/evidence/negative_probes.json').read_text())
defs={}
for p in [C/'studio2/fase03/harness/test_harness_offline.py',C/'studio2/fase03/harness/test_revisions.py',E/'extended_probes.py',E/'additional_edges.py']:
    for cls in ast.parse(p.read_text()).body:
        if isinstance(cls,ast.ClassDef):
            for n in cls.body:
                if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'):defs[n.name]=(p,n.lineno)
T={
1:('test_R07_real_crashes_intent_raw_and_completed_restart','Piano immutabile prima della riserva e tabella v2; stesso os._exit e verifica su processo nuovo. Esteso a raw/completed e runner reali.'),
2:('test_X06_real_concurrent_base_reservation_12_writers','Nuovo piano; 12 processi sul medesimo originale: un solo vincitore, undici rifiuti, contatore 1. X06 valido nel rerun con cwd corretto.'),
3:('test_R05_changed_alias_run_pilot_id_and_duplicate_original','stage_run è digest del binding, non spazio di quota. Accorpati cambio alias, pilot-id e duplicato; distinta prova directory R01 e stato dopo restart X04.'),
4:('test_R04_failed_and_zero_token_cannot_pass','Registrati sette successi con raw e un FAILED nel piano completo. PASS rifiutato; fixture nuova necessaria per raggiungere il controllo.'),
5:('test_R04_failed_and_zero_token_cannot_pass','Stesso caso di N04 poi riconciliazione concreta a ZERO_TOKEN_PROVEN senza retry riuscito: PASS ancora rifiutato. Accorpamento conserva i due assert.'),
6:('test_X04_late_retry_is_rejected_before_and_after_restart','Catena lecita riconciliata e completata, stadio chiuso; rifiuto anticipato della riserva tardiva. Non si pretende di creare un intento ora vietato.'),
7:('test_X04_late_retry_is_rejected_before_and_after_restart','Nuova istanza ledger dopo chiusura e rifiuto tardivo; sonda soltanto senza intenti primari pendenti. X05 copre primario incompleto; X01/X02 scoprono il residuo alternativo C01.'),
8:('test_R04_public_normative_event_forbidden','Rifiuto anticipato di outcome:budget_probe, remediation_authorized e frozen_gate nella API record_event; eventi vuoti. Non occorre arrivare al gate dopo una falsificazione rifiutata.'),
9:('test_R06_same_case_cannot_replace_eight_and_non_template_contracts_immutable','Diff e autorizzazione di fixture concreti; il secondo originale dello stesso caso è rifiutato. X20 controlla anche il primo binding remediation, evitando un test vacuo sul binding già congelato.'),
10:('test_R06_timeout_and_missing_concrete_approval_cannot_remediate','Otto originali, uno FAILED: una diagnosi structure dichiarata non converte il timeout in difetto R4. Approvazione/template solo hash sono respinti.'),
11:('test_R05_two_processes_reserve_one_original_once','Prova zero-token concreta prima del retry; due processi sull’identico originale, un solo figlio. Nessun riuso dell’originale aperto.'),
12:('test_R05_triplet_cannot_reuse_original_or_mix_budget','Piano budget e prove concrete; rifiutati tre riferimenti al medesimo originale e tre originali di gruppi diversi. Quota resta zero.'),
13:('test_probe_triplet_retry_is_atomic_and_capped','Seconda tripletta riferita alle foglie riconciliate della prima; terza rifiutata a quota 6. X08 prova anche rollback dopo prima possibile inserzione (quota globale 6→7→8).'),
14:('test_reserve_15_waiver_and_maxima_152_160','Catena di foglie, waiver e rifiuto oltre 15; X19 prova esplicitamente che gli originali dell’alternativo non finanzino il sedicesimo trasporto.'),
15:('test_gate_is_not_repeatable_and_has_no_retry','Predecessori con raw/record e sonda congelata; gate non ripetibile, nessun ritorno sonda. X16 ammette soltanto ricostruzione file a consumo invariato.'),
16:('test_reserve_15_waiver_and_maxima_152_160','Remediation 8 + retry 7 + budget 9 (primi due gruppi troncati) + gate 120; 152 senza e 160 con alternativo. Non si usa un PASS fittizio sui primi budget.'),
17:('test_hard_200_on_explicit_imported_fixture','Prepopolazione SQLite sacrificabile nel formato v2 per separare hard stop 200 dai massimi ordinari. Non è una migrazione o permesso di consumare 200.'),
18:('test_X07_outcome_transaction_excludes_writer_while_closing','Hook immediatamente prima dell’evento nel vero BEGIN IMMEDIATE: writer distinto bloccato fino al commit e vede outcome completo. Estende il test consegnato, il cui retry tardivo sarebbe comunque illecito.'),
22:('test_R10_repetition_condition_hash_uniqueness_and_distribution','Campione e identità inizialmente validi; duplicata solo repetition. L’assenza di expected_prompts nel vecchio test darebbe un falso verde.'),
23:('test_R10_repetition_condition_hash_uniqueness_and_distribution','Campione valido, alterata la condizione di una sola risposta. Stessa invalidità mirata; non si conta il rifiuto per campione mancante.'),
24:('test_R10_repetition_condition_hash_uniqueness_and_distribution','Campione e record modificati insieme da 8/16/16 a 7/17/16: rifiuto della distribuzione, non mero mismatch di una risposta. X11 aggiunge ruoli/agenti/testo/ripetizione bool.'),
35:('test_R03_real_pipeline_labels_preserved_and_pending_rejected','Handoff ora prodotto da otto coppie stub validate/persistite; builder autentico conserva label_space canonico e ordine diverso in presentation. Vecchio handoff autocertificato non è più fixture positiva lecita.'),
39:('test_R03_real_pipeline_labels_preserved_and_pending_rejected','Dopo pipeline autentica si rimette pending nell’inventario. Sia prepare sia load_prepared rifiutano; API protocol ordinaria pure. Fixture completa necessaria per isolare la barriera label.'),
40:('test_R06_real_runner_remediation_approved_bytes_and_old_handoff','Otto risposte, una malformata, sette valide: nessuna libreria parziale; poi otto richieste remediation autorizzate. X24 replica con JSON valido ma envelope errato.'),
41:('test_R02_inventory_tamper_r4_and_tokenizer_zero_sends','Preflight di fixture autorizzato per raggiungere R4; alterati i quattro file, nessun intento/invio. Test dependency pretransport e X12 estendono dipendenza e mutazione durante il ciclo.'),
42:('test_R09_producer_identity_mismatch_preserves_raw_and_suspends','Attesa identità dichiarata nella fixture; modello errato alla prima risposta, raw durevole e sospensione. X13 verifica fingerprint e conservazione token=5.'),
43:('test_R07_producer_timeout_resume_no_resend_and_explicit_reconciliation','Timeout alla seconda richiesta: prima raw/record e secondo FAILED conservati; resume incerto non invia. Estensione processi reali nella suite, senza pretendere di recuperare raw mai arrivati su disco.'),
44:('test_R07_producer_timeout_resume_no_resend_and_explicit_reconciliation','Dopo prova zero-token riferita all’esatto tentativo, --resume e retry selezionato saltano la prima risposta e completano con consumo 9. X15 rileva separatamente il riepilogo errato C03.'),
45:('test_R06_real_runner_remediation_approved_bytes_and_old_handoff','Diff, template e approvazione concreti sostituiscono hash arbitrari. Template diverso respinto senza invii; il template approvato completa stessi otto. X20 isola ogni invariante prima del binding.'),
47:('test_R02_source_manifest_and_prompt_rehash_cannot_bypass','Fixture prepared autentica; alterazione source e ricalcolo dei riferimenti/sidecar non superano rigenerazione da sorgenti canoniche. X17 verifica anche approvazione esatta.'),
48:('test_X03_gate_transport_invalidity_remains_in_T3_T6','NON EQUIVALENTE: i sostituti dichiarati provano FAILED contabile e assenza retry, non il record invalido né l’ingresso in T3/T6. X03 fallisce e X23 conferma gate definitivamente incompleto. C02; nessuna esclusione scientifica approvata.'),
49:('test_R02_inventory_tamper_r4_and_tokenizer_zero_sends','Testo inventory alterato in fixture altrimenti ammessa: rifiuto prima di trasporto. Handoff modificato e ri-hashato provato separatamente da test_R02_handoff_cannot_self_certify_or_change_library.'),
50:('test_R07_consumer_budget_crash_and_resume_preserve_raw','Budget autentico; crash seconda richiesta, prima raw durevole e due intenti contati; resume non reinvia. os._exit nei processi reali e test raw-before-record/closed artifact completano il lifecycle.'),
51:('test_R07_gate_crash_retains_raw_and_blocks_uncertain_resume','Gate dopo sonda autentica; seconda chiamata interrompe senza perdita della prima raw. Test processo reale e X16 coprono ripresa da raw e dopo outcome/file cancellato senza nuovi invii.'),
52:('test_R08_frozen_budget_tamper_first_gate_zero_additional_calls','Freeze deriva da sonda e ledger reali con stub; max_tokens alterato prima del primo gate: zero invii aggiuntivi. X18 altera soltanto serializzazione; rifiuto byte esatti.'),
53:('test_R09_consumer_identity_change_during_gate_suspends','Modello errato in una risposta gate: sospensione con raw, quota e identità. X22 prova medesimo controllo nella sonda.'),
}
unchanged={30,31,32,33,34,36,37,38,46,60,61,62}
for n in unchanged:T[n]=(None,'Metodo originale invariato eseguito dal wrapper; prerequisiti e assertion originali conservati. Il risultato non qualifica dati reali o servizi.')
for n in (20,21):T[n]=(None,'Metodo/assertion originali invariati; rows aggiunge campione autentico di fixture, request_id e identity_valid; evaluate riceve expected_prompts. Nessuna soglia o firma semantica modificata.')
assert set(T)=={r['number'] for r in original}
rows=[]
def has(ids,name):return any(name in x for x in ids)
for r in sorted(original,key=lambda r:r['number']):
    n=r['number'];method,note=T[n]
    if method:
        assert method in defs,method
        p,line=defs[method];proof=f'[{method}]({p}:{line})'
    else:proof=f'[N{n:02d} originale]({E}/applicable/evidence/negative_probes.py:{r["line"]})'
    mode='invariato' if n in unchanged else 'sola fixture/argomento' if n in (20,21) else 'adattato / accorpato esplicito'
    status='NON EQUIVALENTE / NON OK' if n==48 else 'requisito originario riscontrato; vedere limiti R04/R07'
    item=dict(number=n,original=r['name'],original_line=r['line'],old_failed=has(old['failed_methods'],r['name']),unadapted_failed=has(raw['failed_methods'],r['name']),mode=mode,proof_method=method,proof_link=proof,rationale=note,result=status)
    rows.append(item)
(E/'MATRICE_50_METODI.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
intro='''# Corrispondenza indipendente dei 50 metodi originali

Il mandato non consente di sostituire 50 metodi con il totale 14/14. Questo registro ha esattamente una riga per ciascun metodo originale: nessun requisito è escluso implicitamente.

Lo script originale è conservato byte-identico (SHA-256 69d53547ab0e799b6110534b1016914780554a434e5f88fd0b6d97fc66c3907c). La prova letterale sul nuovo candidato dà 50 eseguiti, 2 failure e 32 errori, 16 metodi verdi. È una **prova di incompatibilità delle vecchie fixture/API**, non il conteggio dei difetti nuovi. I quattro verdi N22/N23/N24/N41 fuori dai 12 riutilizzati non sono accettati come prova: rifiuto per campione mancante o preflight non autorizzato può renderli vacui.

Il wrapper dichiarato è stato rieseguito: 12 metodi invariati + N20/N21 con fixture/argomento nuovi = 14/14. Per gli altri 36 sono stati letti e rieseguiti i metodi adattati della suite; i controlli indipendenti X01–X24 ampliano le lacune. Le prove si sovrappongono: non sono 50 nuovi test identici né un 50/50. N48 non conserva la semantica richiesta e produce C02. R04/R07 hanno inoltre i residui documentati nel verbale.

X06/X07 sono attestati da concurrency_rerun/concurrency.json, dopo correzione del solo cwd dei subprocess del revisore; gli altri X01–X18 da extended.json, X19–X24 da additional_edges/additional.json. I file candidati linkati sono letti dal checkout esatto e non modificati.

| Originale | Modalità | Codice di prova eseguito | Motivazione e limite |
| --- | --- | --- | --- |
'''
body='\n'.join(f'| N{r["number"]:02d} `{r["original"]}` | {r["mode"]} | {r["proof_link"]} | {r["rationale"]} |' for r in rows)
(E/'MATRICE_50_METODI.md').write_text(intro+body+'\n')
print('50 rows; 12 unchanged, 2 fixture/argument, 36 explicitly mapped; N48 non-equivalent')
