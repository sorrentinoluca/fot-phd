OK

# Verifica indipendente esterna — sotto-fase 03.15, sezioni comuni del paper

| Campo | Valore |
| --- | --- |
| Commit verificato | `cf79e81f917c7969dfd375e38db54315c28d4c07` (`codex/studio2-paper-sections`), `studio2(paper): corregge label e producer-swap D9`; base `46c0b623f55154684f326a8523521fb28991fb09` |
| Commit precedente, già verificato | `e2f9aea948ac4bfc64089962c5357343f997621f` → verdetto **NON OK** (2026-09-14, primo passaggio di questa stessa sessione; esito riportato in §B sotto) |
| Verificatore | modello `claude-fable-5-1` (Claude Fable 5.1), sessione Cowork `session_01HR1jHUUpSs8pMD5WcyjTRH`; identità letta dai metadati di sessione, non dedotta dallo stile |
| Esecutore (noto) | `gpt-5.6-sol`, finestra `01a09cd4-51f2-7240-bbab-20e92e8bb993` (`REPORT_PAPER_SECTIONS.md` §3) |
| Verificatore preliminare (noto) | `gpt-5.6-sol`, altra finestra (`REPORT_PAPER_SECTIONS.md` §3) |
| Stato dell'indipendenza | **compatibile**: modello diverso da `gpt-5.6-sol`, finestra diversa, sola lettura |
| Worktree di verifica | detached a `cf79e81` in `/Users/luker/fot-tep/.worktrees/verifica-paper-sections-esterna` (il percorso `/Users/luker/fot-tep-verifica-paper-sections-esterna` non era raggiungibile dalla sessione; il worktree dell'esecutore non è stato toccato) |

**Qualificazione dell'OK.** Vale esclusivamente per le bozze nel perimetro attuale di 03.15 (mappa, cinque sezioni comuni, lint, report, sezione 03.15 di `PROVENIENZA.md`) alla base `46c0b62`. Non approva il manoscritto finale, le decisioni ancora aperte (gate D9, producer alternativo D9.1, proposte 03.8, promozione in `docs/paper/`), i risultati non disponibili, la soglia/FAR di 03.5, né l'integrazione di `normal_dev`.

---

## A. Verifica del delta `e2f9aea..cf79e81`

`git diff --stat e2f9aea..cf79e81`: 5 file, tutti in `studio2/fase03/paper_sections/` (`PIANO_SEZIONI.md`, `REPORT_PAPER_SECTIONS.md`, `method.md`, `protocol.md`, `threats.md`); `related_work.md`, `verbalizer.md`, `lint_paper_sections.py` e `PROVENIENZA.md` invariati. `git diff --name-status 46c0b62..cf79e81`: gli stessi 9 file del pacchetto precedente, nessun artefatto congelato, piano, corpus, walkthrough o codice scientifico toccato. Un solo commit lineare dopo `e2f9aea`, autore Luca Sorrentino, messaggio conforme a MAINTENANCE §8.3. ✅

| Rilievo del primo passaggio | Stato in `cf79e81` | Verifica |
| --- | :-: | --- |
| **R1** spazio delle label (`method.md`) | ✅ chiuso | r. 8–9: «otto etichette opache di fault, l'etichetta letterale `Normal` oppure astenersi con `Unknown` (`abstain=true`, `predicted_label=null`)»; r. 20–22: sedici record per le sole otto classi fault, «`Normal` non ha insight»; r. 37–38: `Unknown` «non come label o classe; la nona e ultima label dello spazio è `Normal`»; r. 49–52: opacità limitata alle otto label di fault, `Normal` letterale in nona posizione, derangement sulle «sole etichette fault dei peer». Conforme a 03.7 `SPECIFICA_PSEUDOLABEL.md` §3 e §5 e a D10 (`Unknown` non esiste come label). |
| **R2** producer-swap nel ramo D9.1 | ✅ chiuso | `method.md` r. 85–90, `protocol.md` r. 112–117, `threats.md` r. 109–114, `PIANO_SEZIONI.md` r. 84–89: «il braccio producer-swap resta nel disegno/protocollo/previsto; D9 non nomina il producer alternativo» + `[DECISIONE: … producer alternativo del ramo D9.1]`; fonte corretta a «piano §8.4, §8.10 punto 3 e D9 opzione 1». Coerente con §8.4 e §8.10 punto 3 del piano e con l'handoff §4 («aperta; Terra solo nell'opzione 2»). |
| **R3** pilot 03.13 «prova/documenta» | ✅ chiuso | in tutti i blocchi D9.2: «Il pilot 03.13, non ancora avviato, è previsto su Qwen-27B FP8 locale; Qwen-2.4T risulta non disponibile alla data dell'handoff»; fonte rinominata «handoff di fase 03.13». Coerente con `HANDOFF_FASE03_2026-09-14.md` (03.13 «non avviata», pilot sul solo modello disponibile). Il documento resta non tracciato: osservazione residua, non bloccante. |
| **O8** frase «il modello non è nuovo» (D9 opz. 2) | ✅ chiuso | presente nei blocchi D9.2 di `PIANO_SEZIONI.md`, `method.md`, `protocol.md`, `threats.md`. |
| **O1** hash `e2f9aea` nel report | ✅ chiuso | `REPORT` §7: sequenza a cinque commit con messaggio di `c63864b` per esteso; il commit correttivo è dichiarato «identificato nella consegna operativa», corretto (un commit non può citare il proprio hash). |
| **O2** verbale preliminare fuori dal tree | ⚠️ residuo dichiarato | `REPORT` §3 ora cita anche la verifica esterna di `e2f9aea` con il percorso del worktree di verifica; nessuno dei due verbali è nel tree di `cf79e81`. Da committare nella cartella della sotto-fase all'integrazione (MAINTENANCE §8.6). Non bloccante. |
| **O4** «piano revisione 7» con tree a rev. 6 | ⚠️ residuo parziale | corretto nei blocchi D9.1 e D9.2; resta in tutti i blocchi D9.3 (`PIANO_SEZIONI.md` r. 105, `method.md` r. 103, `protocol.md` r. 131, `threats.md` r. 127). Testo di D9 identico fra le due revisioni: non bloccante. |
| **O5** U3 «già registrata» in `PROVENIENZA.md` | ⚠️ invariato | U3 vive sul branch `codex/studio2-evidence` (`2f6dd8d`); da riconciliare al merge di 03.6. Non bloccante. |
| **O6** DP-FPL/FedDTPT «§14.1–§14.2» in `threats.md` r. 91 | ⚠️ invariato | senza scheda in §14.2; citare §14.1. Non bloccante. |
| **O7** «Q8 non un modello [Fonte: piano §8.1]» | ⚠️ invariato | §8.1 lega Q8 a Qwen-2.4T; la separazione scenario/modello è decisione dell'autore (report §5 punto 1). Non bloccante. |
| **O9** limiti del lint | ⚠️ invariato | parole di primato solo in inglese; `needles` senza Lee/Pappa/Zhou & Yu/Sun. Verifica manuale ripetuta sul delta: nessun claim nuovo introdotto. |
| **O10** «preregistered» in `letteratura.md` §14.6 | fuori perimetro | per `Letteratura_LLM`. |

Il delta non introduce numeri nuovi (grep: nessun valore di soglia, FAR, α o percentuale oltre 86,1 % e 94,4 %), nessun GO/NO-GO, nessun risultato, nessuna frase specifica del modello fuori dai blocchi VARIANTE, nessuna occorrenza di «preregistr», Terra solo in D9.2/D9.3. ✅

Controlli rieseguiti nel worktree a `cf79e81`:

- `python3 studio2/fase03/paper_sections/lint_paper_sections.py --corpus docs/letteratura.md` → «5 file, 0 segnalazioni», exit 0;
- `git diff --check 46c0b62..HEAD` → nessuna segnalazione, exit 0;
- `python3 docs/test_explanation.py` → `Ran 35 tests`, `FAILED (failures=14, skipped=1)`, invariato rispetto alla baseline del 2026-09-11 e a quanto dichiarato nel report §6.

## Esito per controllo su `cf79e81`

| # | Controllo | Esito |
| :-: | --- | :-: |
| 1 | Perimetro e storia Git | ✅ |
| 2 | Sostegno delle affermazioni | ✅ (⚠️ residue O4/O5 sulle sole citazioni, contenuto verificato) |
| 3 | Related work e claim | ✅ |
| 4 | Metodo e condizioni | ✅ |
| 5 | Evidence e provenienza | ✅ |
| 6 | Segnaposto e numeri | ✅ |
| 7 | `normal_dev` e varianti D9 | ✅ |
| 8 | Threats e controlli eseguibili | ✅ |

I controlli 1–8 non toccati dal delta (`related_work.md`, `verbalizer.md`, `lint`, `PROVENIENZA.md`, parti invariate di `protocol.md`/`threats.md`/`method.md`) restano verificati come in §B, sulle stesse fonti primarie.

## Rilievi bloccanti

Nessuno.

## Osservazioni non bloccanti (da chiudere in documentazione/integrazione, non prima dell'OK)

| ID | File : righe | Osservazione | Correzione suggerita |
| --- | --- | --- | --- |
| O2 | `REPORT_PAPER_SECTIONS.md` : 44–58 | I due verbali citati non sono nel tree. | Committarli in `studio2/fase03/paper_sections/` all'integrazione e aggiornare i rinvii. |
| O4 | `PIANO_SEZIONI.md` : 105; `method.md` : 103; `protocol.md` : 131; `threats.md` : 127 | «piano revisione 7» nei blocchi D9.3 con piano a rev. 6 nel tree. | «piano D9 opzione 3» (invariato fra rev. 6 e 7), o allineare dopo il rebase su `a572d1c`. |
| O5 | `studio2/PROVENIENZA.md` : sezione 03.15, ultima riga; `verbalizer.md` : 27 | U3 registrata solo su `codex/studio2-evidence`. | Nota «U3 in 03.6 a `2f6dd8d`, in attesa di integrazione». |
| O6 | `threats.md` : 91 | DP-FPL/FedDTPT senza scheda §14.2. | Citare solo §14.1. |
| O7 | `method.md` : 82–83; `protocol.md` : 108–110; `threats.md` : 105–107; `PIANO_SEZIONI.md` : 79–82 | Fonte §8.1 per «Q8 non un modello». | Citare la decisione dell'autore. |
| O9 | `lint_paper_sections.py` : 14, 83–107 | Copertura del lint. | Estendere prima della promozione in `docs/paper/`. |
| R3-bis | blocchi D9.2 | Fonte «handoff di fase 03.13» non tracciata. | Sostituire con `REPORT`/`APERTURA` di 03.13 quando esisteranno in un commit. |

## Aggiornamenti pianificati non bloccanti

- **`normal_dev`**: integrare `protocol.md` e `verbalizer.md` dopo il lotto 03.9 (piano rev. 7 §6.2, `SPECIFICA_NORMAL_DEV.md`), poi rieseguire il lint. Nessuna frase attuale è incompatibile con il ruolo prespecificato del lotto.
- **Decisioni dell'autore**: gate D9 e producer alternativo del ramo D9.1; D2, *m*, α, gerarchia, test locali, OOD, D11, politica R (03.8); promozione in `docs/paper/`.
- **Letteratura**: Tango, Maurer–Hothorn–Lehmacher, Westfall–Krishen, Clopper–Pearson, Kish, ICH E9, McMahan, Hoeffding, Bahadur–Savage; schede mancanti FICAL, DP-FPL, FedDTPT, T2SP; O10.
- **Risultati**: tutti i `[RISULTATO]` restano vuoti; soglia numerica e FAR di 03.5 dopo la verifica indipendente OK; tag 03.12 dopo la revisione 4 e la pubblicazione.

---

## B. Primo passaggio — commit `e2f9aea` (verdetto NON OK, 2026-09-14, stessa sessione)

Conservato come traccia. Metodo: analisi autonoma del tree `e2f9aea` sulle fonti primarie (piano a `46c0b62` e `a572d1c`, `docs/letteratura.md`, 03.5 a `9507143`, 03.6 a `2f6dd8d`, 03.7 in `main`, 03.8 a `dd82cd1`, 03.12 a `e058cb0`, `phase_b/final_evaluation/`, tag `exp3-v2-results-frozen-001`, `fault_runs/`, `selection/`); report trattato come oggetto della verifica; verbale preliminare non raggiungibile (cartella non connessa, file non committato), rilievi residui del mandato ricontrollati sulle fonti.

Esito per controllo su `e2f9aea`: 1 ✅ · 2 ⚠️ · 3 ✅ · 4 ❌ · 5 ✅ · 6 ✅ · 7 ❌ (D9.1) / ⚠️ (D9.2) / ✅ (D9.3, `normal_dev`) · 8 ✅.

Verifiche puntuali (valide anche per `cf79e81`, file invariati o parti invariate):

| Affermazione | Fonte letta | Esito |
| --- | --- | :-: |
| innesco 25 h, orizzonte 40 h, 8 finestre half-open da 5 h, `ode45`, uscita 1/60 h, un solo IDV, Philox4x32-10, stream 30000–30039, 5 × 8 = 40 run | `fault_runs/SPECIFICA_RUN_FAULT.md` §1–§3; `REPORT_RUN_FAULT.md` | ✅ |
| deviazione da Downs & Vogel per F14/F15 | `SPECIFICA_RUN_FAULT.md` §2; `letteratura.md` §14.3 | ✅ |
| catalogo 8 fault, 4 continuità + 4 nuovi, tag D1 → `ab43f0b2…`, `CATALOG_FREEZE.json` SHA-256 `68b8461a…` | `git rev-parse`, `shasum`, `REPORT_CATALOGO_D1.md` | ✅ |
| firma 41 × 17 = 697, catena feature→JSON→testo→firma, codice a `3fd960a1…`, 40 run / 320 unità, release `3e1eb87f…`, scanner fail-closed | `DIPENDENZE_EVIDENCE.md`, `REPORT_EVIDENCE.md` a `2f6dd8d` | ✅ |
| N1–N5 solo normalizzazione sotto U3, coppia indivisibile con le quattro soglie V2 | `DIPENDENZE_EVIDENCE.md` §3; `PROVENIENZA.md` a `2f6dd8d` | ✅ |
| 350 `cal_thr` / 150 `far_ver`, `S > soglia`; valore e FAR assenti dalle bozze | 03.5 a `9507143`; grep delle bozze | ✅ |
| pseudolabel SHA-256, biiezione, derangement dei 7 peer, `Normal` letterale nona | 03.7 `SPECIFICA_PSEUDOLABEL.md` §3–§7 | ✅ (in `cf79e81`) |
| schema 6 campi, `additionalProperties: false`, 2/16/14, E dopo filtro peer, diff byte-level, manifest `d6ef52de…`, tag non creato | 03.12 a `e058cb0` | ✅ |
| H1–H3, sequenza raccomandata e aperta, Hoeffding/Tango/bootstrap a cluster, 8 run/64 cluster, stato `proposed_pending_author_decisions`, §14, §17 | 03.8 a `dd82cd1` | ✅ |
| 86,1 % (B 31/36) e 94,4 % (B unseen 68/72) con «dichiarato descrittivo» | `phase_b/final_evaluation/primary_metrics.csv`; `exp3v2_confirmatory_results.json` al tag `exp3-v2-results-frozen-001`; walkthrough v2 §7.3/§8.3; piano §8.10 punto 1 | ✅ |
| attribuzione FoT a Yao, Rabbani, Zaheer, Li (2026); tutti i lavori citati in §14.1 con i titoli usati; FedDTPT e DP-FPL come delimitazione; FaultExplainer con le tre qualificazioni di §12.5; nessun claim di novità/privacy/efficienza/cross-model/scalabilità/superiorità; riferimenti esterni segnalati e non citati | `letteratura.md` §14.1–§14.7; piano §12.5–§12.9, §8.10 | ✅ |
| «pre-specificato», mai «preregistrato» | piano §0 riga 4, §5 C06; grep | ✅ |
| `normal_dev`: nessuna frase incompatibile con piano rev. 7 §6.2/§8.1 | `a572d1c` changelog 45–47 | ✅ |

Rilievi bloccanti allora emessi: **R1** (`method.md` r. 5–8, 36–37, 48–49: spazio delle label non conforme a 03.7 §3) e **R2** (`method.md` r. 84–85, `threats.md` r. 110–111: «producer alternativo non configurato» in D9.1 letto come assenza del braccio producer-swap). Entrambi chiusi in `cf79e81` (§A).

---

**Fonti lette e costo (complessivo, due passaggi).** MAINTENANCE.md, Prompt_LLM.md, Verifica_LLM.md, `sottofase_3_15.md`; bozze, report e lint a `e2f9aea` e delta a `cf79e81`; log e diff `46c0b62..cf79e81`; piano a `46c0b62` e `a572d1c`; `letteratura.md` §14.1–§14.7 (parti pertinenti); artefatti 03.5/03.6/03.7/03.8/03.12 ai commit indicati; `phase_b/final_evaluation/`; tag `exp3-v2-results-frozen-001`; walkthrough v2 §7.3/§8.3 e v1 §«Evaluator · signature vector»; `HANDOFF_FASE03_2026-09-14.md` (confronto, non fonte); `revisione4_normal_prompt.md`. Circa 75 mila token documentali. Zero chiamate a modelli, zero simulazioni, nessuna modifica a bozze, corpus o walkthrough; nessun commit, push, merge o tag. Con permesso dell'autore sono stati rimossi i soli lock git orfani creati da questa sessione (`.git/index.lock`, `.git/worktrees/verifica-paper-sections-esterna/{HEAD.lock,index.lock,locked}`).
