# Report — documentazione delle sotto-fasi chiuse della Fase 03

**ESITO ESECUZIONE: OK** — documentazione completata, parità MD/HTML verificata,
`test_explanation` 14 → 14 (storiche). Non è un OK di verifica: il delta va sottoposto alla
verifica documentale indipendente prima del commit. Nessun rilievo bloccante; tre segnalazioni
non bloccanti in §7.

Data: 2026-09-17. Esecutore: Claude (Cowork), modello configurato `claude-opus-5`.
Worktree: `/Users/luker/fot-tep/.worktrees/studio2-doc-fase03`, branch
`codex/studio2-doc-fase03`, base `origin/main` `15e56a89b0f377e6d90eef28ed941d4d54b5b00c`.
Nessun commit, push, merge o tag. Nessuna rete, nessun file privato letto
(`api_key.json`, `server_enea.json`, ledger, config private). La Fase 03 **non è chiusa**.

## 1. Scostamento dal prompt: che cosa c'era già

Il prompt partiva dall'ipotesi che il walkthrough avesse solo §4.1–4.3. Quello era lo stato della
copia nell'orchestratore; su `origin/main` `15e56a8` esistevano già §4.4, 4.5, 4.6, 4.7, 4.8, 4.9,
4.10 (solo raccordo metriche), 4.12 e 4.15. Queste sezioni non sono state riscritte: sono state
corrette solo dove lo stato era superato. Il lavoro nuovo è §4.10 (chiusura 03.10), §4.11, §4.13
(una riga) e §4.14.

| Sotto-fase | Sezione | Intervento |
| --- | --- | --- |
| 03.4 perimetro Q8 | §4.4 | già presente, invariata |
| 03.5 soglie Normal | §4.5 | già presente, invariata |
| 03.6 evidence | §4.6 | già presente, invariata |
| 03.7 pseudolabel | §4.7 | già presente, invariata |
| 03.8 piano statistico | §4.8 | stato aggiornato: chiusura con OK acquisito e integrata in `main` |
| 03.9 baseline numerica | §4.9 | due frasi di stato (03.8/03.10 chiuse; sbilanciamento trattato in 03.14) |
| 03.10 harness | §4.10 | aggiunta la chiusura dell'harness offline; riquadro e «Lavoro che resta» aggiornati |
| 03.11 run finali/OOD | §4.11 | **nuova**, dichiarata non integrata in `main` |
| 03.12 schema insight | §4.12 | già presente, invariata |
| 03.13 pilot | §4.13 | **una riga**: aperta, non documentata |
| 03.14 FedAvg | §4.14 | **nuova**, dichiarata non integrata in `main` |
| 03.15 paper sections | §4.15 | stato aggiornato: NON OK storico su `9b6bd64`, OK sul delta correttivo, integrazione in `main` tramite consolidamento pubblicato |

Aggiornati anche intestazione, §0.1, tabella «Sintesi per sezione» ed elenco dei cantieri.

## 2. Fonti usate, per sotto-fase

**03.8** — `piano_statistico/VERIFICA_CHIUSURA_DOCUMENTALE_03_8.md` (OK sul delta
`2edd4550..b2184360`, SHA-256 `a80cb1f63c8ba8ccf8210c9315046184c28b6045d2d7c76e17da07d94578cba6`,
ricalcolato), acquisizione nel commit `f887b0aac9b0ef6cab1d3159de260183c1d837b7`; cherry-pick
`24999d60769b6af91cc53a63017df29396ddaf8a` con albero identico a `b2184360` (diff vuoto).

**03.10** — `harness/CHIUSURA_SOTTOFASE_03_10.md` (SHA-256 `450454b152f9c93421b587e02e48da8c3112d9d21f195ec9cee8fb456eb38c2f`),
`harness/VERIFICA_CHIUSURA_03_10.md` (OK sul delta `8fbbfa0..dcc7422`, 5.785 byte, SHA-256
`1d67c6425bd8e2e1c0904c3b7f08675e7774d4ace214c76abcffcd27c0afeeb7`, ricalcolato),
`ACQUISIZIONE_OK_CHIUSURA_03_10.md` (commit `e853d5f`), merge `15e56a8`;
cifre rosso/verde e regressioni da `history_reconciliation_evidence/RESULTS.json`.

**03.11** — branch locale `codex/studio2-esecuzione-0311`, HEAD
`349ead315de575cf43977fdf807d43b64070546c`, letto con `git show` dal repository comune (la worktree
`/Users/luker/fot-tep-wt-0311` non era montata). Verbali: `VERIFICA_ESECUZIONE_03_11.md` (OK sullo
stop `1cdf597`, SHA-256 `2fb7dc83…bae8`) e `VERIFICA_ESECUZIONE_03_11_v2.md` (OK finale su
`fd41fcf`, SHA-256 `09994cf7…f16f`), entrambi ricalcolati. Artefatti con impronta ricalcolata:
`SIGILLO_LOTTO_03_11.json`, `BATCH_AUDIT_03_11.json`, `SIGILLO_PREFLIGHT_03_11.json`,
`PREFLIGHT_AUDIT_03_11.json`, i tre piani CSV e `VERIFICA_RILEVABILITA_F5_03_11.md`. Conteggi
(89 righe, 8 per classe primaria, 3+3 OOD, 11 scorte, stream 71000–71088 e 72000–72088, 70000–70002)
ricalcolati dai piani.

**03.14** — branch locale `codex/studio2-fedavg`, HEAD `e1b46faf5aee27b2a1f98d4c568c3e276bf33ae4`,
letto con `git show`. Verbali: `VERIFICA_FEDAVG.md` (OK su `d563549`, NON OK storico su `b39b723`
in appendice), `VERIFICA_MINIMA_03_14_f66f30d.md` (VERDETTO OK), `VERBALE_VERIFICA_ESECUZIONE_FINALE_FEDAVG_03_14.md`
(OK su `8cb9a8b`, SHA-256 `a43db064…e58e`, identico alla copia nell'orchestratore) e
`VERBALE_REPLAY_INDIPENDENTE_FEDAVG_03_14.md` (OK, SHA-256 `dff09562…4ac4`). Metriche primarie
(897/4608, 434/576, 443/576) e somme delle attribuzioni OOD ricalcolate da
`final/primary_cluster_metrics.csv` e `final/ood_forced_attributions.csv`; impronte della tabella
ricalcolate; ricetta e pesi di classe da `SPECIFICA_FEDAVG.md`; smoke da `smoke_real/SMOKE_SUMMARY.json`.

**03.15** — `paper_sections/VERIFICA_RACCORDO_DOCUMENTALE_0315.md` (NON OK su `9b6bd64`),
`paper_sections/VERIFICA_DELTA_RACCORDO_0315.md` (OK su `9b6bd64..1058279`),
`VERIFICA_CONSOLIDAMENTO_0315_METRICHE.md` (OK su `04dee86`),
`REGISTRO_PUBBLICAZIONE_CONSOLIDAMENTO_0315_METRICHE_2026-09-14.md`; ascendenza di `04dee86`,
`07a64e9`, `1058279`, `4f98a29` rispetto a `15e56a8` verificata con `git merge-base`.

Letteratura: `docs/letteratura.md` §14.1/§14.2 per Xiao, Kordon e Sen 2023 e McMahan et al. 2017
(entrambi 🟢). Stato di coordinamento: `APERTURA_SOTTOFASI_FASE03.md` e
`HANDOFF_FASE03_2026-09-16_rev06.md` §1, §3, §4, §8, §9 (untracked nell'orchestratore).

## 3. Cifre non ritrovate o non ricalcolate

- Nessuna cifra del report è stata scartata perché assente dagli artefatti.
- **Non ricalcolate qui**: le impronte e le dimensioni degli archivi 03.11
  (`test_batch_f5_001.tar.gz`, `chain_f5_001.tar.gz`, `ood_preflight_001.tar`), dei manifest runtime
  e delle firme 03.14 su disco: stanno fuori dalla cartella montata o fuori da Git. Sono riportate
  dal sigillo e dai verbali, e la §4.11 lo dichiara.
- I numeri FDR/FAR di F5 (p. 6 di Xiao et al.) vengono dal record di rilevabilità e dal verbale v2,
  che li ha controllati sul PDF; il PDF non è stato riaperto qui.
- Le regressioni 03.10 (17/11/8/37) sono registrate in `RESULTS.json` ma non rieseguite dal
  verificatore; la §4.10 lo dice.

## 4. Sintesi divulgativa

`docs/fot_walkthrough_studio2.html` aggiornato con quattro voci brevi (03.8, 03.11, 03.14, 03.15),
ciascuna con link alla sezione lunga e soli numeri già presenti nelle rispettive sezioni del documento lungo (§4.11, §4.14 e §4.15). Le altre sotto-fasi non
sono sintetizzate perché tecniche; la pagina lo dichiara. L'avviso «scheletro al 2026-09-12»
**era già assente** su `origin/main`: nulla da rimuovere.

## 5. §0.1

Nessuno dei punti aperti 1 e 3 è chiuso da queste sotto-fasi, e il paragrafo ora lo dice. Il
punto 4 era marcato «Chiuso» ma ancora in tabella: è stato tolto, come prescrive la nota della
sezione stessa.

## 6. Controlli

- Parità MD ↔ HTML sul contenuto: confronto token per token delle sezioni §0.1, intestazione,
  §4.8–§4.15, sintesi ed elenco cantieri. Differenze solo di forma (numerazione dell'elenco resa
  da `<ol>`, un trattino in §4.12 preesistente).
- HTML: 23 `<section>` aperte e 23 chiuse; indice laterale aggiornato con §4.11, §4.13, §4.14.
- Link: tutti gli anchor interni risolvono. Restano non risolvibili su questo branch, per
  costruzione, i 10 link ai file di 03.11 e 03.14 che esistono solo sui branch locali; le due
  sezioni lo dichiarano.
- `python3 docs/test_explanation.py`: **prima** 35 test, 14 failure, 1 skip; **dopo** 35 test,
  14 failure, 1 skip. Le failure sono le storiche: `test_step27_qwen_frozen_results_and_limitations`
  (9), `test_step27_qwen_protocol_stable_facts` (3), `test_condition_c_contract_and_caveats` (1),
  `test_one_flow_and_ordered_step_headings` (1). Il test non copre questo walkthrough.

## 7. Da segnalare

- **Link a branch non integrati.** Se 03.11 e 03.14 non entrano in `main` prima di questo commit,
  i 10 link restano rotti su `main` finché non vengono integrate. È una scelta consapevole: i path
  diventano validi con l'integrazione.
- **Consegna dati 03.11.** Gli archivi del lotto non sono su `fot-tep-data`: secondo
  `Commit_LLM.md` §7 il lotto non è consegnato.
- **Nome del modello nell'elenco cantieri.** §7.1/§7.2 parlano ancora di «Qwen-2.4T», mentre il
  record D9 fissa 122B e 27B. Non corretto qui (è la dicitura del piano); da allineare a parte.
- **Worktree.** Creata dalla VM Cowork: `git worktree add` ha lasciato tre lock vuoti
  (`refs/heads/codex/studio2-doc-fase03.lock`, `worktrees/studio2-doc-fase03/HEAD.lock`,
  `locked`), rimossi con permesso dell'autore. Il file `.git` della worktree usa il percorso
  relativo `../../.git/worktrees/studio2-doc-fase03`, e `gitdir` punta al path macOS, così la
  worktree funziona sia sul Mac sia nella VM.

## 8. File toccati

- `docs/fot_walkthrough_conversazione_studio2.md` — §4.11, §4.13, §4.14 nuove; chiusura 03.10 in
  §4.10; stato di §4.8, §4.9, §4.15, intestazione, §0.1, sintesi e cantieri.
- `docs/fot_walkthrough_conversazione_studio2.html` — stesse modifiche, più l'indice laterale.
- `docs/fot_walkthrough_studio2.html` — quattro voci di sintesi e nota sulle sotto-fasi tecniche.
- `studio2/fase03/REPORT_DOCUMENTAZIONE_SOTTOFASI_CHIUSE.md` — questo report.

## 9. Commit proposto (non eseguito)

Tutti e quattro i file in un solo commit (la coppia MD/HTML deve stare insieme), dopo la verifica
documentale:

```
studio2(fase03): documenta sotto-fasi chiuse 03.4–03.15 nel walkthrough

Aggiunge al walkthrough dello studio 2 le sezioni 4.11 (run finali e
controlli OOD) e 4.14 (baseline FedAvg), entrambe verificate ma non
ancora integrate in main, e la chiusura dell'harness offline 03.10 in
4.10. Aggiorna lo stato di 4.8, 4.9 e 4.15, l'intestazione, §0.1 e la
sintesi per sezione; 4.13 dichiara il pilot ancora aperto. Aggiunge alla
sintesi divulgativa le voci 03.8, 03.11, 03.14 e 03.15. La Fase 03 resta
aperta. test_explanation invariato: 14 failure storiche.
```

## 10. Rettifica post-verifica (2026-09-17)

Verifica `VERIFICA_DOCUMENTAZIONE_SOTTOFASI_CHIUSE.md` (SHA-256 `d8347224…`): NON OK per il solo rilievo sulla frase di §4, corretta come proposto dal verificatore. Walkthrough invariati.
