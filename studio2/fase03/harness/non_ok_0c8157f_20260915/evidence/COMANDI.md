# Comandi e protocollo di riproduzione

Tutti gli esperimenti sono offline, con fixture sacrificabili. Nessuna API provider, inferenza o simulazione scientifica. Non eseguire alcun originale in-place nella precedente review o nell’acquisizione tracciata. Non riutilizzare un contenitore di fixture: gli script richiedono directory nuove, per preservare le evidenze già prodotte.

Directory candidato (cwd per le suite e per i subprocess):

```text
/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate
```

Runtime verificato: `/opt/anaconda3/bin/python3`, 3.13.9 arm64, SQLite 3.51.0. Ogni esecuzione usa `PYTHONDONTWRITEBYTECODE=1`. Le suite che usano RunnerRevisions impostano:

```text
FOT_HARNESS_TEST_EVIDENCE=/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output
```

## Identità prima della scrittura

Eseguiti sulla copia principale e sui worktree sorgenti:

```bash
git status --short --branch
git rev-parse HEAD 'HEAD^{tree}'
git worktree list --porcelain
git remote -v
git show --no-patch --format=fuller 0c8157f23bee49a3a5a2df648525c34706da29d7
git rev-parse '0c8157f23bee49a3a5a2df648525c34706da29d7^{tree}'
git ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main
```

Clone locale separato creato con `git clone --shared --no-checkout` dalla copia principale e `git checkout --detach 0c8157f23bee49a3a5a2df648525c34706da29d7`. Nessun branch nuovo, commit o tag. Estratti dal successore documentale con `git show 6268437b8b64288b50ad5f7c924e1fcab85b27d3:studio2/fase03/harness/<nome>` i tre file di consegna, scritti in evidence, fuori candidato.

## Suite richieste

```bash
PYTHONDONTWRITEBYTECODE=1 FOT_HARNESS_TEST_EVIDENCE=/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output /opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions
PYTHONDONTWRITEBYTECODE=1 FOT_HARNESS_TEST_EVIDENCE=/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output /opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 docs/test_explanation.py
```

Output acquisito rispettivamente in `targeted.log` (exit 0, 82/82), `discovery.log` (exit 0, 117/117), `documentation.log` (exit 1, 35 test/14 failure storiche/1 skip/0 errori).

## Riproduzioni originarie

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py --candidate /Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate --original /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.py --reference /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference --sandbox /Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/evidence/applicable
```

Exit 0, 14/14. Il sandbox contiene una copia byte-identica dello script e symlink al candidato e alla reference verificata. Per il replay letterale completo è stato creato allo stesso modo `original_all_unadapted/`, quindi eseguito:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/evidence/original_all_unadapted/evidence/negative_probes.py
```

Exit 1: 50 metodi, 2 failure e 32 errori dovuti a prerequisiti/API/fixture precedenti; non conteggiati come difetti del candidato. Il log e il JSON sono conservati nello stesso sandbox.

## Controlli indipendenti e audit

Eseguiti i seguenti script in `evidence/`, con lo stesso Python e cwd candidato:

| Script | Output | Risultato |
| --- | --- | --- |
| audit_integrity.py | integrity.json/log, original_methods.json, technical_delta.txt, technical_diff.patch, documentary_delta.txt | 5.655 registrazioni, nessun mismatch, 2.754 membri precedenti preservati |
| extended_probes_initial.py (in quel run denominato extended_probes.py) | extended.log/json, extended_console.log, extended_fixtures/ | 18 metodi; 4 assertion candidate + 2 fallimenti del solo setup subprocess del revisore; altri 12 conformi |
| rerun_concurrency.py, con extended_probes.py corretto solo nei due cwd | concurrency_rerun/, concurrency_console.log | X06/X07: 2/2 conformi |
| additional_edges.py | additional_edges/, additional_console.log | X19–X24: 6/6 conformi |
| scope_and_results.py | scope_and_results.json/log | perimetri invariati, 90 sorgenti compilabili, ID documentali invariati, riproduzione precedente corrispondente |
| build_mapping.py | MATRICE_50_METODI.md/json | 50 corrispondenze esplicite, N48 non equivalente |
| build_report.py | VERIFICA_CORREZIONI_HARNESS_03_10.md | verbale derivato dalle evidenze, NON OK |

Consolidamento X01–X24: **24 metodi distinti, 20 conformi, 4 failure di assertion del candidato, zero errori validi**, con quattro failure raggruppate in tre rilievi. Il rerun non ha rieseguito o sovrascritto gli altri casi. I file originali di fixture restano intatti; non si modificano script o candidato per trasformare i fallimenti reali in PASS.

Per un nuovo run copiare gli script in un nuovo `evidence/` fratello di un checkout identico; mantenere la reference in sola lettura. `extended_probes.py` ha ora il cwd subprocess corretto e ricrea da zero tutti i suoi 18 casi. `rerun_concurrency.py` documenta la ripetizione mirata di questa sessione. I percorsi temporanei archiviati nei raw/config/SQLite restano quelli realmente usati; non sono riscritti retroattivamente.

Lo script di audit consulta soltanto oggetti Git esatti, file locali e `git ls-remote` di main/tag. Nessuna fonte di altre finestre è incorporata nel candidato. `scope_and_results.log` contiene il messaggio Git atteso per `test_revisions.py` assente nel candidato vecchio; è gestito come file nuovo, non un errore di esecuzione.

## Stato finale e impronte

Ripetuti `git rev-parse`, `git status`, `git worktree list --porcelain` e `git ls-remote origin refs/heads/main`: dati in `final_git_state.json`. Il candidato è detached e pulito; sorgente, precedente review e principale conservano identità/stato iniziali. Non sono stati creati commit o tag.

SHA256SUMS elenca i file regolari della consegna, escluso se stesso. EVIDENCE_INVENTORY.json elenca file, dimensioni, hash e collegamenti simbolici; esclude se stesso e SHA256SUMS per evitare cicli di impronte. Il manifest SHA256SUMS comprende invece EVIDENCE_INVENTORY.json. Symlink e percorsi esterni sono dichiarati, non seguiti ricorsivamente né nascosti.
