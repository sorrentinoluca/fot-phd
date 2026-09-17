VERDETTO: OK

# Verifica minima indipendente — smoke reale 03.14

## Identità, indipendenza e ambiente

- Candidato verificato: `f66f30d99b6d9f89d13e9644cb38e7ee0a52f70a`
- Tree: `9d24d5312fc8a978a8c7a24381d4717b0cf25ccf`
- Parent/base: `bfbde772bf14c496ff0b255008904d3deb424e54`
- Branch contenente il candidato: `codex/studio2-fedavg`.
- Copia di sola lettura: worktree detached `/tmp/fot-tep-review-f66f30d`, creato direttamente all'hash del candidato. Il worktree dell'esecutore `/Users/luker/fot-tep/.worktrees/studio2-fedavg` non è stato modificato; al controllo finale conteneva soltanto il prompt non tracciato preesistente `studio2/fase03/PROMPT_VERIFICA_MINIMA_03_14.md`.
- Revisore: Codex, modello/sessione esposti come GPT-5, sessione locale `/root`.
- Finestra di verifica: 2026-09-15, fino alle 23:01:22 CEST (+0200).
- Ambiente esecutivo: macOS arm64; `/tmp/fedavg-review-NKu7lF/venv/bin/python`, Python 3.13.9, NumPy 2.3.5. Output, download, estrazioni, raccordo e replay sono rimasti in `/tmp/fedavg-minverify-Tb7359`.

Sono stati letti prima `docs/MAINTENANCE.md` e `docs/prompts/Verifica_LLM.md`. È stata applicata la lezione pertinente del harness: verificare le prove persistite sui byte effettivamente letti e distinguere identità del candidato, output osservati e limiti del verdetto. Non sono stati avviati guardian, test/held-out/03.11, modelli LLM, tuning, freeze, merge, rebase, tag o commit.

## Esiti

| Requisito | Prova primaria e comandi rilevanti | Esito |
| --- | --- | :---: |
| Grafo, tree, parent e perimetro | `git worktree add --detach /tmp/fot-tep-review-f66f30d f66f30d...`; `git rev-parse HEAD^{tree} HEAD^`; `git diff --name-status bfbde772... f66f30d...`; `git diff --check ...` | ✅ |
| Cinque artefatti candidati | Il diff contiene soltanto `REPORT_FEDAVG.md`, `INPUT_PREFLIGHT.json`, `SMOKE_SUMMARY.json`, `cluster_metrics.csv`, `weight_hashes.json`; le cinque SHA-256 sono rispettivamente `3677c6ab...43ed8`, `8b1e8125...daad5`, `53f9d165...22f04`, `8ed7d807...9079b`, `82bc7d01...835f`. | ✅ |
| Fatti ereditati invariati | `git diff --quiet base HEAD --` su specifica, loader, training, test, freeze, fixture e precedente `VERIFICA_FEDAVG.md`; tutte le 8 impronte di `FEDAVG_FREEZE.json` ricalcolate e coincidenti. | ✅ |
| Asset pubblicati e sicurezza archivi | Riscaricati solo `studio2-fase03-evidence-v2` e `studio2-fase03-normal-dev-v1`: fault 62.185.472 byte / `6d724a...37cf`, Normal 151.500.800 byte / `eef69b...91a03`. Ispezione `tarfile` pre-estrazione: nessun path assoluto o `..`, symlink o membro speciale; solo file regolari e, nel fault, due directory necessarie. | ✅ |
| Raccordo Normal | Indice sorgente `4f340a...5329`, 320 righe, `class_identifier=Normal`, `agent_run_index` 1–5. Vista temporanea preserva righe, ordine, colonne e contenuti, aggiungendo in coda `label=class_identifier` e `batch=agent_run_index`, UTF-8/LF: `27a534...31ae`. | ✅ |
| Refusal sull'indice originale | `load_evidence_bundle` sul Normal originale, con manifest e indice verificati, ha rifiutato prima di ogni training: `ValueError: NDEV-EVD-0001: unknown label ''`. | ✅ |
| Loader sui dati adattati | Il loader del candidato verifica manifest/indici fault `5111d0...0020`/`b966cd...69c`, Normal `cc8d96...fdc1`/`27a534...31ae`; legge 320 firme finite ×697 per classe, join uno-a-uno, 40 run fault e 40 Normal, otto client e cinque batch. Combinato 640×697/80 run; training 512/64; validation batch 5 128/16; intersezioni fault/Normal e training/validation entrambe 0. | ✅ |
| Coerenza output | JSON validi. Ricalcolo diretto dal CSV: 160 righe (128 local, 16 fedavg, 16 centralized), 8 tentativi per riga, zero astensioni e `accuracy_non_abstained=accuracy`; local 500/1024 = 0.48828125, FedAvg 111/128 = 0.8671875, centralizzato 56/128 = 0.4375. Le SHA del CSV e dei pesi coincidono con `SMOKE_SUMMARY.json`; `weight_hashes.json` contiene otto digest locali più FedAvg e centralizzato, NumPy 2.3.5. | ✅ |
| Replay massimo consentito | Un solo comando `smoke_fedavg.py` sulla ricetta congelata, con le radici temporanee fault e Normal adattata, ha prodotto in `/tmp/fedavg-minverify-Tb7359/replay` tre output byte-identici al candidato: CSV `8ed7d807...9079b`, pesi `82bc7d01...835f`, summary `53f9d165...22f04`. | ✅ |
| Limiti dichiarati | `REPORT_FEDAVG.md` e `SMOKE_SUMMARY.json` qualificano l'esito come smoke LOBO tecnico di sviluppo, non stima finale; escludono tuning e confronto LLM, non attribuiscono al `PASS` una soglia di prestazione e mantengono aperte 03.14/Fase 03 e il freeze non efficace. Il raccordo è esplicitamente temporaneo, non un adapter durevole. | ✅ |

## Comandi eseguiti

1. Lettura dei due documenti di istruzioni e del contratto di manutenzione; creazione del worktree detached all'hash esatto.
2. `git rev-parse`, `git diff --name-status`, `git diff --check`, `git diff --quiet` e SHA-256 dei cinque nuovi file e degli otto file congelati.
3. `curl -fL --retry 2` delle sole due release indicate, `wc -c`, `shasum -a 256`, scansione dei header TAR e sola estrazione temporanea degli evidence bundle.
4. Script temporaneo con `csv.DictReader`/`DictWriter` per il raccordo nominale, poi `load_evidence_bundle`, `concatenate` e `split_leave_one_batch_out` del codice candidato.
5. Script temporaneo di audit del CSV/JSON e un solo replay CLI; confronti `cmp -s` byte-per-byte dei tre output.

## Limite del verdetto

Questo `OK` riguarda esclusivamente il preflight del loader, il raccordo **temporaneo** dell'indice Normal e l'unico smoke LOBO reale di sviluppo dei byte di `f66f30d99b6d9f89d13e9644cb38e7ee0a52f70a`. Non autorizza integrazione, pubblicazione, freeze efficace, tuning, accesso o procedura sui dati finali, né chiude 03.14 o Fase 03. Non esprime una stima di prestazione finale e non effettua confronto con il braccio LLM.
