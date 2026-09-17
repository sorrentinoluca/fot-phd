**NON OK** — due rilievi bloccanti (B1, B2); il resto del candidato è verificato e coerente.

# VERIFICA_PROTOCOLLO_FINALE — review indipendente 7.3-R (seconda esecuzione)

Data: 2026-09-17. Modello: `claude-fable-5-1` (Claude Cowork), **in sostituzione dichiarata** di
`gpt-6-astra`/finestra `b567` a cui il mandato era indirizzato; il verbale 7.2-R citato come «tuo»
non è di questo modello. Sola lettura: nessuna chiamata a provider, nessuna modifica a codice,
ledger, runtime o candidato; nessun push/merge/tag; `api_key.json` e `server_enea.json` non letti.
Il ledger è stato interrogato su una **copia** fuori dal runtime. Unica attività di rete: due
`git ls-remote --tags` (solo elenco ref, `fot-phd` e `fot-tep-data`).

Oggetto: commit `e0db132fc6ef477bc054d8c02b3fb62f8c39da06`,
`PROTOCOLLO_FINALE_CANDIDATE.md` SHA `d4f00224…e97fa`, `.json` SHA `d2f32d70…be25c5`
(byte della worktree = blob del commit).

Nella cartella esiste già `VERIFICA_PROTOCOLLO_FINALE.md` (SHA `d0fe9d31…5261c`, esito NON OK,
rilievo R1 «manca il runner finale»), letto **solo dopo** aver formato i rilievi qui sotto. Non è
stato sovrascritto. Il suo R1 è nel frattempo affrontato dal commit 7.4-PREP `9e0e086`; i rilievi
B1 e B2 qui sotto coincidono con i due punti bloccanti che quel lavoro ha incontrato.

## Riscontri per punto del mandato

1. **Riferimenti.** 32/32 SHA dei file repository coincidono, sia al commit candidato sia in
   `origin/main`; i tre file 7.2 coincidono ai commit `c284523`/`f0d0393`; librerie (file e SHA
   canonico di `library`), manifest input, `pilot_prompts.jsonl`, `stability_records.jsonl`,
   `frozen_gate_config.json`, template di remediation (`4306c5da…`), handoff e prompt esterni:
   tutti coincidono. Gli otto tag esistono, sono annotati e sono antenati di `main`. I tag delle
   release `evidence-v2`, `test-v1`, `pilot-v1` esistono su `fot-tep-data`. Eccezioni: C1, C2, C3.
   **Ordine di merge:** `c284523` e `f0d0393` stanno solo su
   `codex/studio2-riconciliazione-stop-contabile` (base `540df7b`, toccano solo `librerie/`); il
   candidato parte da `ea90761` e tocca solo `protocollo_finale/`: nessun conflitto. Ordine:
   ramo librerie **fino a `f0d0393`** in `main` → candidato corretto in `main` → tag sul commit in
   `main`. `9e0e086` (7.4-PREP) sta sopra `f0d0393` sullo stesso ramo: non va trascinato dentro
   prima della sua review.
2. **Conteggio da zero.** Catalogo 8 fault (`CATALOG_FREEZE.json`), proprietà 1:1
   (`AGENT_ASSIGNMENT.json`), sigillo 03.11: 64 primari + 8 Normal + 6 OOD + 11 scorte = 89.
   Prompt unici: nucleo `(64×8 + 8×8)×3 = 1.728`; swap `4×8×7 = 224`; ablation `64 + 84 = 148`;
   OOD `6×8×3 = 144`; totale 2.244. A R=3: 5.184 / 672 / 444 / 432 = 6.732; + canary 70 + X 100 =
   **6.902**. Coincide con REV10 (`N = 2244R + … `). Delta da 7.174: −256 −16 = −272, verificato
   sulla tabella del report pilot. Pilot storico: 156 richieste + 5 lineage nel ledger. Nessuna
   differenza.
3. **T5.** Dalle 120 righe del gate: media 26,2086 s, p95 (interpolazione lineare) 36,6609 s.
   `6902×26,209/3600 = 50,248 h → 60,298 h`; `6902×36,661/3600 = 70,287 h → 84,345 h`; < 168 h.
   Sulle sole 119 completate la media è 26,409 s (60,76 h): irrilevante.
4. **Piano statistico.** Popolazioni, cluster, endpoint, §3.3, H1→H2→H3, uso delle ripetizioni
   (§10.3–10.4) e canary (§10.5) sono un rinvio fedele. Regole **nuove** rispetto alle fonti:
   (a) schedule a tre passate con `PCG64(20260913)`; (b) `Q=0`; (c) STOP anche su
   `system_fingerprint` (il piano dice solo ID del modello; coerente con `runtime.py`);
   (d) marcatura «fra ultimo canary PASS e canary fallito» (il piano marca le chiamate **del
   giorno**) → C4; (e) tetto di sette giorni canary; (f) zero-token = invalidità senza nuovo
   invio → C6; (g) covariata di copertura nello swap (decisione autore). Manca una regola → C7.
5. **S18.** Rifatto con `protocol.peer_insights`, derangement congelati (identici a quelli del
   manifest) e librerie reali: `G_P` 112/112 solo `pseudolabel`, 0 altrove; idem `G_A`. Copertura
   bidirezionale ricalcolata: 6/16 e 0/16. PASS.
6. **Canary.** `select_canaries` su `pilot_prompts.jsonl` riproduce i dieci ID nello stesso
   ordine, 2/4/4, otto agenti; SHA dei prompt = SHA del testo; nel ledger ogni prompt ha tre
   `COMPLETED` con coppia attesa e **lo stesso** hash grezzo in tutte e tre. PASS. Regole: C4, C5.
7. **Regole di esecuzione.** Non vero che non servano meccanismi nuovi: B1, C8. Nessuna regola
   consente scelte dopo lettura del contenuto, salvo la lacuna C7.
8. **Checklist / §9.** Decisioni d'autore recepite fedelmente (R=3, W, thinking off, SWAP4,
   riuso a 0 chiamate, testo dell'asimmetria, covariata, E5 fuori). Nessun «template unico»;
   3.700 e E5 dichiarati. Evidenze non puntuali: S3 (C3), T2 (C2), S8 e O2 (B1, B2).
9. **Cosa manca a 7.4.** B1, B2, C5, C6, C8. §10 «domande aperte: nessuna» non è vero.

## Rilievi

**B1 — bloccante — il braccio B-senza-LF non è producibile dal renderer dichiarato vincolante.**
`protocol.py` (`791fa347…`) ha `CONDITIONS = ("A","B-LF","E-LF")` e aggiunge `DECISION POLICY`
a ogni condizione ≠ A; il contratto di logging ammette solo quelle condizioni. §4 dichiara
eseguibili 444 richieste «con il renderer di §3.1»: falso. Serve nel candidato: token di
condizione, definizione («prompt B-LF meno la sezione DECISION POLICY, nient'altro», piano §9.2),
e forma dell'adattamento come **file nuovo** con SHA proprio (MAINTENANCE §8.2), con test di diff
B-LF↔B-noLF. Il token entra nell'ID stabile e cambia lo SHA della schedule.

**B2 — bloccante — non è definito quale finestra di un run è «il caso», e l'input del lotto test
non esiste.** Il piano conta un caso per run; 03.6 produce 8 finestre per run (712 nel lotto
test) e copre solo i 40 run di sviluppo. La regola run→finestra non è scritta in nessuna fonte
(FedAvg usa 8 finestre/run; esempi locali e handoff baseline usano `window_ordinal=1`,
[25,30) h). È una decisione d'autore da prendere **prima** di aprire i dati di test, e va
scritta nel protocollo insieme a: estrazione evidence del lotto 03.11 come prerequisito di §7.1
(0 chiamate), e dichiarazione che esempi locali, label space e agenti sono quelli del manifest
`84176888…`.

**C1 — da correggere — due coppie tag↔file di §2 non reggono.** `CRITERIA_FREEZE_rev002.json`
non esiste al tag `criteri-selezione` (c'è `CRITERIA_FREEZE.json`; la rev002 è raggiungibile dal
tag `catalogo-D1`); `BASELINE_FREEZE_rev005.json` non esiste al tag `baseline-numerica` (entra
con `a006058`, dopo il tag). SHA corretti in `main`: citare il commit, non il tag.

**C2 — da correggere — `VERIFICA_PILOT_03_13.md` vive solo, non tracciato, in
`~/.codex/worktrees/b567/…`.** SHA ricalcolato e coincidente (`944db3d7…`), ma nessun ref Git lo
contiene: evidenza di T2 non raggiungibile da `main` (§8.5). Va committato prima del tag.

**C3 — da correggere — S3 cita la release `test-v1`, ma in `main`
`fault_runs/ARTIFACT_STORAGE.json` la dà `publication_pending_author` e
`ACQUISIZIONE_OK_ESECUZIONE_03_11.md` dice «non pubblicata».** Il tag remoto esiste; manca la
registrazione della verifica per riscaricamento (§8.5).

**C4 — da correggere — marcatura canary ambigua e diversa dal piano.** §6.5 marca l'intervallo
precedente il canary fallito; §10.5 marca le chiamate del giorno. Non è detto quale insieme esce
dall'analisi di sensibilità, né se le chiamate del giorno marcato dopo il canary fallito sono
marcate. Proposta: unione dei due insiemi, definita sui timestamp del ledger.

**C5 — da correggere — canary senza risposta valida non trattato.** `canary.compare_run` solleva
errore se `parsed_output` non è un oggetto; il candidato non dice se un canary invalido o fallito
per trasporto marca il giorno, conta nei 70, si ripete (con `Q=0` no).

**C6 — da correggere (una riga di decisione autore) — `Q=0` sugli zero-token.** Nel pilot 8
richieste su 156 (5,1 %) sono fallite prima della generazione (401, connection error; 1/120 nel
gate). Col candidato ognuna diventa «non valida = non corretta» nell'endpoint primario, e non c'è
STOP su fallimenti di trasporto consecutivi: una caduta di rete brucia slot in serie. Il rimedio
già implementato (`reserve_transport_retry` dopo prova zero-token) non legge alcun contenuto e T5
ha margine per >6.000 retry. Raccomando: `Q>0` limitato ai soli zero-token provati, con tetto, più
STOP dopo k fallimenti di trasporto consecutivi. In alternativa confermare `Q=0` sapendolo.

**C7 — da correggere — regola di maggioranza incompleta.** Né §10.4 né il candidato dicono cosa
fare con tre ripetizioni tutte diverse o con ripetizioni non valide. A R=3 il caso è raggiungibile
e oggi lascerebbe una scelta post-hoc. Una riga basta (es.: senza maggioranza resta la
ripetizione 1; l'invalida vota come «non corretta»).

**C8 — da correggere — schedule sotto-determinata.** Il testo non fissa: chiamata numpy
(`permutation(n)` vs `shuffle`) e versione, forma dell'ordinamento (tupla vs stringa), valori di
`library_role` per A ed E-LF, definizione degli stage per la «quota per stage». Ognuno cambia lo
SHA della schedule.

**N1 — nota.** Il JSON non contiene la tabella canary (20 SHA), mentre §2 lo dice «elenco
meccanico completo». **N2.** §7.2 rinvia a «handoff §6.2», file non tracciato: citare
`ledger.reconcile_zero_token` / `CONTRATTO_ESECUZIONE_E_RIPRESA.md`. **N3.** `X=100` richiede
verifiche «identificate prima dell'esecuzione»: l'elenco non esiste; o si scrive o `X` resta
inutilizzabile. **N4.** `d=7` giorni civili con ~50–70 h sequenziali richiede ≥7–10 h/giorno di
esecuzione: oltre il settimo giorno la quota canary ferma il batch.

## Tag

Il nome `studio2-fase03-protocollo-finale-frozen-001` è conforme alla serie esistente e resta
`001` (nessun candidato è mai stato taggato). **Non va creato su `e0db132`**: va creato,
annotato, sul commit della revisione corretta, dopo nuova review dei soli delta e quando quel
commit e `f0d0393` sono in `main`.
