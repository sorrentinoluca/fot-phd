# Comandi della verifica indipendente D03

Radice: `/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec`.
Cwd delle prove: `candidate/`; output nel fratello `evidence/`. Python `/opt/anaconda3/bin/python3`.
Non rilanciare sulle directory già popolate: creare una nuova radice e adeguare soltanto i percorsi di output/import del revisore. Nessuna prova nel source o nelle acquisizioni tracciate.

```bash
export PYTHONDONTWRITEBYTECODE=1
export FOT_HARNESS_TEST_EVIDENCE=/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output
```

## Identità prima delle scritture

Letture principale, sei source e cinque candidati precedenti: `git status --short --branch`, `git rev-parse HEAD HEAD^{tree}`, `git worktree list --porcelain`, remote -v. Controllati tecnico/tree, parent del successore e suo diff esatto di quattro file. Snapshot iniziale conservato in initial_git_state.json e worktrees_initial.txt.

```bash
git -C /Users/luker/fot-tep-harness-0310-d03 ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main
git clone --shared --no-checkout /Users/luker/fot-tep-harness-0310-d03 /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate
git -C /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate checkout --detach 23859a29225ccd9cd6f47e4a0b6e36258831dbab
```

Acquisizione quattro documenti mediante `git show 97868f9d6ef281c2dd4ab1c6ffb67e2477ee5715:studio2/fase03/harness/FILE`: PROMPT_VERIFICA_D03.md, REPORT_CORREZIONE_D03.md, CONSEGNA_D03.json, DELIVERY_AUDIT_D03.json. Candidato rimasto sul tecnico.

## Audit, cwd radice review

```bash
/opt/anaconda3/bin/python3 evidence/audit.py
```

7.098 controlli con hash/dimensione sui file reali, copie ed esterni; manifest, fonti Git esatte, tag remoti, reference, moduli, 176 file protetti, 93 sorgenti live, cronologia e hash test-first/finali. Crea solo dopo i controlli cinque contenitori nuovi w_original/z_original/y_original/literal/x23_adapted. Script e dipendenze copiati byte-identici dalla review a219bd4. Non rieseguibile in-place: mkdir intenzionalmente rifiuta contenitori già presenti.

## Suite, cwd candidate

```bash
/opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions studio2.fase03.harness.test_c01_c03 studio2.fase03.harness.test_d01_replay studio2.fase03.harness.test_d02_predecessors studio2.fase03.harness.test_d03_contract
/opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
/opt/anaconda3/bin/python3 docs/test_explanation.py
FOT_HARNESS_TARGET=/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate FOT_D03_OBSERVATIONS=/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/red_contract.json /opt/anaconda3/bin/python3 studio2/fase03/harness/test_d03_contract.py
FOT_HARNESS_TARGET=/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate FOT_D03_OBSERVATIONS=/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/green_contract.json /opt/anaconda3/bin/python3 studio2/fase03/harness/test_d03_contract.py
```

Output: targeted.log 120/120, discovery.log 155/155, documentation.log 35/14 failure/1 skip/zero errori (NON PASS). red_contract 9 metodi/8 failure/0 errori; green_contract 9/9. Il test è lo stesso file finale, fuori dal vecchio clone; FOT_HARNESS_TARGET seleziona il codice importato. Nessun test scritto nel candidato respinto. Le prove dirette D03 usano temporanei nuovi e conservano log/JSON; nessuna riesecuzione delle fixture tracciate.

```bash
/opt/anaconda3/bin/python3 studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py --candidate /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate --original /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.py --reference /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference --sandbox /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/applicable
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/w_original/evidence/retry_proof_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/y_original/evidence/edge_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/z_original/evidence/chain_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/literal/evidence/extended_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/literal/evidence/additional_edges.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/x23_adapted/evidence/additional_edges.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/independent_d03_probes.py
```

Log e JSON nei relativi contenitori, console separate nella radice evidence. Leggere i risultati: gli script storici e quello V possono terminare exit 0 con assertion fallite. W4/Y7/Z5 passano byte-identici. X23 letterale resta una failure obsoleta, adattato passa, senza nuove modifiche alle assertion. V: sei metodi, quattro PASS e due failure D04; SQL su un solo quota_kind, otto retry contro sette contati e un invio allo stub. V01 usa os._exit reale nei punti di crash; V03 un writer SQLite in un processo separato. Non sono chiamate reali né dati scientifici.

## Matrici e consegna, cwd radice review

```bash
/opt/anaconda3/bin/python3 evidence/generate_field_matrix.py --harness-dir /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence/generated_fields --checks-dir /Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence
/opt/anaconda3/bin/python3 evidence/build_matrices.py
/opt/anaconda3/bin/python3 evidence/package_review.py
```

Per il generatore è stata copiata soltanto DURABLE_FIELD_CONTRACT.json nella nuova generated_fields; il generatore è byte-identico al candidato. Output JSON/MD coincidono con la matrice candidata usando osservazioni di questa review, confronto in field_matrix_comparison.json. build_matrices verifica una prova nominata corrente passata per ognuno dei 50 metodi e distingue X/Y/Z/W/V.

Il comparatore documentale iniziale usava l'ordine dei 14 identificativi, diverso dalla precedente lista: l'assertion locale è stata corretta confrontando gli stessi identificativi ordinati. Nessun test candidato o requisito modificato. Due letture di log inizialmente usavano cwd candidate invece della radice: errore di percorso di lettura, nessuna esecuzione persa. Le suite complete sono state eseguite una volta; non si sommano suite sovrapposte o sottocasi.

package_review ricontrolla Git e impronte, risultati strutturati, copie byte-identiche e link; produce RESULTS.json, stato Git finale, EVIDENCE_INVENTORY.json e SHA256SUMS senza autoreferenza e senza seguire symlink. Stampa hash del verbale e manifest fuori dai file inventariati. Le altre operazioni sono letture mirate con rg/cat/sed/nl, git show/diff e JSON. Nessun commit/tag/push/integrazione.

Il primo controllo Git finale ha rilevato un nuovo VERIFICA_D03.md non tracciato nel source, apparso durante la review. La differenza è stata registrata con hash/dimensione in external_git_changes.json: nessuna cancellazione o modifica, nessun verdetto importato. Il controllo finale richiede identità invariate per tutti i dodici repository e status invariato per gli altri undici; non dichiara il source finale pulito.
