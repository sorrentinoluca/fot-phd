# Comandi della verifica indipendente D04

Radice: `/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec`.
Cwd delle prove: `candidate/`; output nel fratello `evidence/`. Python `/opt/anaconda3/bin/python3`.
Non rilanciare sulle directory già popolate: creare una nuova radice e adeguare soltanto i percorsi di output/import del revisore. Nessuna prova nel source o nelle acquisizioni tracciate.

```bash
export PYTHONDONTWRITEBYTECODE=1
export FOT_HARNESS_TEST_EVIDENCE=/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output
```

## Identità prima delle scritture

Letture principale, sette source e sei candidati precedenti: `git status --short --branch`, `git rev-parse HEAD HEAD^{tree}`, `git worktree list --porcelain`, remote -v. Controllati tecnico/tree, parent del successore e suo diff esatto di quattro file. Snapshot iniziale conservato in initial_git_state.json e worktrees_initial.txt.

```bash
git -C /Users/luker/fot-tep-harness-0310-d04 ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main
git clone --shared --no-checkout /Users/luker/fot-tep-harness-0310-d04 /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate
git -C /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate checkout --detach aae29a908356e4a4842a214fdc3db9bff26ec3ca
```

Acquisizione quattro documenti mediante `git show feaf1d3c56ff142e1d1b4bc4dd243348c20bcb98:studio2/fase03/harness/FILE`: PROMPT_VERIFICA_D04.md, REPORT_CORREZIONE_D04.md, CONSEGNA_D04.json, DELIVERY_AUDIT_D04.json. Candidato rimasto sul tecnico.

## Audit, cwd radice review

```bash
/opt/anaconda3/bin/python3 evidence/audit.py
```

9.209 controlli con hash/dimensione sui file reali, copie ed esterni; manifest, fonti Git esatte, tag remoti, reference, moduli, 177 file protetti, 94 sorgenti live, cronologia e hash test-first/finali. Crea solo dopo i controlli sei contenitori nuovi v_original/w_original/z_original/y_original/literal/x23_adapted. Script e dipendenze copiati byte-identici dalla review 23859a2. Non rieseguibile in-place: mkdir intenzionalmente rifiuta contenitori già presenti. Entrambi i verbali Codex/Claude sono stati letti integralmente; il loro perimetro resta distinto dalle esecuzioni correnti.

## Suite, cwd candidate

```bash
/opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions studio2.fase03.harness.test_c01_c03 studio2.fase03.harness.test_d01_replay studio2.fase03.harness.test_d02_predecessors studio2.fase03.harness.test_d03_contract studio2.fase03.harness.test_d04_open_quota
/opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
/opt/anaconda3/bin/python3 docs/test_explanation.py
FOT_HARNESS_TARGET=/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate FOT_D04_OBSERVATIONS=/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/red_contract.json /opt/anaconda3/bin/python3 studio2/fase03/harness/test_d04_open_quota.py
FOT_HARNESS_TARGET=/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate FOT_D04_OBSERVATIONS=/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/green_contract.json /opt/anaconda3/bin/python3 studio2/fase03/harness/test_d04_open_quota.py
```

Output: targeted.log 128/128, discovery.log 163/163, documentation.log 35/14 failure/1 skip/zero errori (NON PASS). red_contract 8 metodi/240 assertion fallite in sei metodi/0 errori; green_contract 8/8. Il test è lo stesso file finale e test-first, fuori dal vecchio clone; FOT_HARNESS_TARGET seleziona il codice importato. Nessun test scritto nel candidato respinto. Le prove dirette D04 usano temporanei nuovi e conservano log/JSON; nessuna riesecuzione delle fixture tracciate.

```bash
/opt/anaconda3/bin/python3 studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py --candidate /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate --original /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.py --reference /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference --sandbox /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/applicable
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/w_original/evidence/retry_proof_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/y_original/evidence/edge_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/z_original/evidence/chain_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/literal/evidence/extended_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/literal/evidence/additional_edges.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/x23_adapted/evidence/additional_edges.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/v_original/evidence/independent_d03_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/decision_edge_probes.py
```

Log e JSON nei relativi contenitori, console separate nella radice evidence. Leggere i risultati: gli script storici possono terminare exit 0 con assertion fallite. V6/W4/Y7/Z5 passano byte-identici. X23 letterale resta una failure obsoleta, adattato passa, senza nuove modifiche alle assertion. V05/V06: SQL su un solo quota_kind, otto intenti/sette retry reali, zero nuovi invii e rifiuto preventivo. V01 usa os._exit reale nei punti di crash; V03 un writer SQLite in un processo separato. Le nuove U sono cinque metodi indipendenti: sei ingressi sotto lock, rollback a metà tripletta, due processi al limite 15, fault di altro stadio prima/dopo restart e richiesta diretta senza rebind. Non sono chiamate reali né dati scientifici.

## Matrici e consegna, cwd radice review

```bash
/opt/anaconda3/bin/python3 evidence/generate_decision_matrix.py --harness-dir /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate/studio2/fase03/harness --checks-dir /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence --output-dir /Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/generated_decisions
/opt/anaconda3/bin/python3 evidence/build_matrices.py
/opt/anaconda3/bin/python3 evidence/package_review.py
```

Il generatore è byte-identico al candidato e legge il contratto candidato, senza scrivere nella directory harness. Output JSON/MD coincidono con la matrice candidata usando osservazioni di questa review, confronto in decision_matrix_comparison.json. build_matrices verifica una prova nominata corrente passata per ognuno dei 50 metodi e distingue X/Y/Z/W/V/U.

Il comparatore documentale confronta gli stessi 14 identificativi ordinati con la review precedente. Le suite complete sono state eseguite una volta, anche con concorrenza fra processi di suite indipendenti; non si sommano suite sovrapposte o sottocasi. Fixture e output sono separati per esecuzione.

package_review ricontrolla Git e impronte, risultati strutturati, copie byte-identiche e link; produce RESULTS.json, stato Git finale, EVIDENCE_INVENTORY.json e SHA256SUMS senza autoreferenza e senza seguire symlink. Stampa hash del verbale e manifest fuori dai file inventariati. Le altre operazioni sono letture mirate con rg/cat/sed/nl, git show/diff e JSON. Nessun commit/tag/push/integrazione.

Il controllo finale richiede identità e status invariati per tutti i quattordici repository osservati e candidato corrente detached pulito. Il verbale Claude untracked nel source D03 è preesistente e conservato anche per hash/dimensione; nessuna modifica, cancellazione o integrazione. GitHub main viene interrogato direttamente una seconda volta. Il pacchetto non incorpora modifiche parallele.
