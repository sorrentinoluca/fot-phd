# Comandi della verifica D02 — solo offline

Candidato: `/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate`.
Output sibling: `/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence`.
Il cwd dei test è il candidato, anche nei subprocess. Le impostazioni seguenti sono state passate ai processi:

```bash
export PYTHONDONTWRITEBYTECODE=1
export FOT_HARNESS_TEST_EVIDENCE=/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output
```

## Prima della scrittura

Letture su sorgente, principale e review precedenti: `git status --short --branch`, `git rev-parse HEAD HEAD^{tree}`, `git worktree list --porcelain`, `git remote -v`; controllo commit/tree/parent e diff del successore. Il risultato iniziale è in initial_git_state.json e worktrees_initial.txt.

```bash
git -C /Users/luker/fot-tep-harness-0310-d02 ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main
git clone --shared --no-checkout /Users/luker/fot-tep-harness-0310-d02 /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate
git -C /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate checkout --detach a219bd469bbd280f56b7fa9cb56cda115b0975ed
```

Quattro file del successore acquisiti con `git show e9b60c5db77edfd3c06a29857e6ba5f61ebe139a:studio2/fase03/harness/FILE`: PROMPT_VERIFICA_D02.md, REPORT_CORREZIONE_D02.md, CONSEGNA_D02.json, DELIVERY_AUDIT_D02.json. Nessun checkout documentale. Si usa il remoto GitHub effettivo, non origin del clone locale.

## Audit prima delle prove

Dal fratello superiore della cartella candidate:

```bash
/opt/anaconda3/bin/python3 evidence/audit.py
```

Risultati in audit.log, integrity.json, runtime.json e technical.diff. Verifica i 70 membri tecnici, tutte le copie/coordinate esterne di acquisizione e riproduzione, fonti Git esatte, tag remoti, moduli recuperati, reference precedente, metriche, perimetri protetti e 92 sorgenti live. Soltanto dopo i confronti crea i quattro nuovi contenitori z_original/y_original/literal/x23_adapted con copie byte-identiche degli script e symlink candidate al checkout tecnico. Non rieseguire lo script sulle directory già popolate: ricreare una nuova radice per una nuova review.

## Suite, cwd candidato

```bash
/opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions studio2.fase03.harness.test_c01_c03 studio2.fase03.harness.test_d01_replay studio2.fase03.harness.test_d02_predecessors
/opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
/opt/anaconda3/bin/python3 docs/test_explanation.py
```

Output integrale in targeted.log (111 OK), discovery.log (146 OK), documentation.log (35, 14 failure storiche e 1 skip, NON PASS). I sette D01 e gli otto D02 sono già inclusi, non una suite aggiuntiva da sommare. Il confronto degli identificativi con la review precedente è in documentation_comparison.json.

```bash
/opt/anaconda3/bin/python3 studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py --candidate /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate --original /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.py --reference /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference --sandbox /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/applicable
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/y_original/evidence/edge_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/literal/evidence/extended_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/literal/evidence/additional_edges.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/x23_adapted/evidence/additional_edges.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/z_original/evidence/chain_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence/retry_proof_probes.py
```

Log/JSON nei relativi contenitori e console log separati nella radice evidence. Gli script indipendenti stampano conteggi ma non restituiscono necessariamente exit nonzero per assertion fallite: leggere sempre tests/failures/errors. Y=7/7; X=23 letterali PASS più un X23 letterale FAIL conservato e X23 adattato PASS; Z=5/5; W=4 test, due failure pertinenti D03 e due PASS, zero errori. Gli X/Y/Z restano byte-identici alle copie precedenti, incluso l'adattamento X23 già verificato; nessuna assertion modificata qui.

Y01/Y02 generano nuove fixture con cwd/PYTHONPATH al checkout esatto e pulito 0c8157f `/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate`. Tale vecchio codice è solo generatore di fixture; il candidato a219bd4 esegue la riconferma. Nessuna modifica SQL in questa riproduzione D01. Le regressioni consegnate verificano HEAD/tree/status del generatore; FOT_HARNESS_LEGACY_CANDIDATE è un'alternativa per quelle regressioni, non modifica il percorso OLD della Y letterale.

chain_probes.py usa solo nuove copie sacrificabili. Z01/Z03 cambiano un raw conservando l'hash originario; Z02 rimuove una riga richiesta; Z04 tenta un vero BEGIN IMMEDIATE in un altro processo durante e dopo la verifica; Z05 controlla un gate già FAIL dopo 120 INVALID. I fault SQL sono dichiarati, distinti dalla generazione naturale del difetto D01 e non applicati al candidato. Il confronto logical database usa iterdump prima/dopo, non la sola lista di eventi. Le fixture del runner sono catturate prima del cleanup, con percorsi temporanei originali preservati nei documenti.

## Matrici e consegna, cwd radice della review

```bash
/opt/anaconda3/bin/python3 evidence/build_matrices.py
/opt/anaconda3/bin/python3 evidence/package_review.py
```

Il primo verifica che ogni riga dei 50 metodi abbia una prova corrente passata e produce le matrici. Il secondo ricontrolla Git/fonti finali, legge gli esiti dai log, verifica i link e produce EVIDENCE_INVENTORY.json e SHA256SUMS senza seguire symlink. Gli inventari distinguono file copiati da riferimenti esterni. Nessun commit/tag/push o integrazione.

Le altre operazioni sono letture con rg/cat/sed/nl e JSON, non prove scientifiche. Per riprodurre usare una nuova radice, adattando soltanto i percorsi di output degli script del revisore; non eseguire le copie tracciate o sovrascrivere le evidence conservate.

retry_proof_probes.py aggiunge quattro metodi W: sette alterazioni indipendenti del solo detail_json di una prova zero-token inizialmente valida; replay nel runner dopo restart con token positivi iniettati; catena valida con due retry seguita da perdita della prova intermedia; riconferma valida seguita da corruzione raw nella stessa istanza. Hash, outcome e altri dati non sono riscritti. W01/W02 falliscono con assertion pertinenti D03, W03/W04 passano. Nessun invio reale; le interrogazioni server sono mock. I sottocasi e le suite sovrapposte non si sommano.
