VERDETTO: OK

Verifica indipendente del solo delta di chiusura residui baseline 03.9.

Data: 2026-09-14, Europe/Rome. Revisore: OpenAI Codex Desktop, modello esposto
`gpt-6-astra`, reasoning `high`, provider `openai`.
Sessione: `01a0a199-006e-74c0-841b-f166692301ea`; agente `/root`.
Commit completo verificato: `49bc53b6d4630e7675eb5cf59c6d483d694ab042`.
Base: `f1746e1e76c5657e5cb74ed765d2f22143f979ce`.
Branch: `codex/studio2-baseline-039-residui`.
Worktree letto: `/Users/luker/fot-tep-baseline-039-residui`.

La consegna Git è stata riscontrata nel messaggio finale della sessione produttrice
`01a0a18c-3719-7611-a52e-3b4b42ccd180` (rollout del 2026-09-14T22-11-56, riga 284):
riporta letteralmente candidato, base e worktree sopra. Il produttore espone
`gpt-5.6-sol`, reasoning `high`: modello e sessione distinti dal revisore.
Gli estratti selettivi di consegna e metadati sono in `runtime_e_consegna.json`.
Per il revisore la prova è il rollout
`/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T22-25-54-01a0a199-006e-74c0-841b-f166692301ea.jsonl`,
righe 1 e 8. Non si deduce l'identità dal committer Git.

Il candidato è stato letto senza modificarlo; HEAD e stato pulito ricontrollati alla fine.
Il presente verbale e le prove sono scritti fuori dal repository per l'acquisizione additiva
in una finestra successiva. Nessun commit, push, merge, release o tag è stato prodotto.

| Requisito | Prova primaria e controllo di questa sessione | Esito |
| --- | --- | --- |
| Perimetro esatto | `git diff --name-status f1746e1… 49bc53b…`: esattamente cinque aggiunte, nessuna modifica o cancellazione; 364 righe e 25.912 byte di contenuto aggiunto. `git diff --check` senza errori. Identità worktree/commit controllata per i cinque file. | ✅ |
| 1. Acquisizione byte-identica | Confrontati direttamente i byte di `DELTA_HARNESS_03_10.md` nel candidato, in `6aaa5b3eebfed4ba502c25c0443caabd0051af21` e nel commit introduttivo `526561feabeb6b4083170b1817b8abdac1a2a4c7`. Tutti coincidono: 7.108 byte, blob `780e08ae9e176a819a745ab2054a2e6ae79a8a9a`, SHA-256 `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`. I pin del record di acquisizione e della rev.4 corrispondono. | ✅ |
| 2. Limiti dell'acquisizione | Letti integralmente i cinque nuovi file. Si acquisisce la sola fonte normativa, con esplicita natura di specifica; nessun altro file del piano entra nel diff. Non risultano approvazione/congelamento del piano 03.8, decisione D9, qualifica 122B o autorizzazione/esecuzione del pilot. Le prescrizioni del documento storico restano condizionate e non sono un'approvazione operativa nuova. | ✅ |
| 3. Mapping adottato e testato | Ispezionati `harness/metric_adapter.py::adapt_baseline_metric`, `adapt_baseline_metrics_document`, `load_baseline_metrics`, `metrics.py::three_numbers`, `SPECIFICA_HARNESS.md` §8 e `test_metric_raccordo.py`. Il lettore verifica SHA-256, visita summary e cluster e applica `accuracy→accuracy_all`, `n→total`, `abstentions→abstained`; i valori numerici validati sono copiati. Codice e test sono byte-identici alla base pubblicata. La prova non dipende dal solo `INTERFACE_CHECK.json`. I 9 test e le verifiche indipendenti pregresse sono riusati, non rieseguiti. | ✅ |
| 3. `non_abstained` e `invalid` | L'adapter verifica `non_abstained=n-abstentions` e rifiuta campi estranei, invalidi dichiarati, conteggi e rapporti incoerenti; emette `invalid=0` nel contratto 03.9 valid-only. Nel produttore generale `three_numbers`, correttezza e astensione richiedono `valid is True`; una riga invalida resta nel totale e in `non_abstained`, anche con payload `abstain=true` o label coincidente. Test espliciti coprono questi casi, insieme vuoto e tutto astenuto. | ✅ |
| 4. Ancestry e sorgenti 03.6 | `git merge-base --is-ancestor` conferma `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb` e `7c99a8318cbe24bf864790566302f72614d963ed` nella base pubblicata. `extract_evidence.py` e `leakage.py` sono identici nei due commit, nella base e nel candidato; SHA-256 completi nella tabella sotto. | ✅ |
| 4. Pin effettivi dell'estrattore Normal | Letto `extract_normal_evidence.py::load_verified_extractor`: controlla esistenza e SHA-256 sia dell'estrattore sia del modulo adiacente `leakage.py` prima del caricamento, e solleva errore in caso di mismatch. Costanti ricavate anche staticamente tramite AST, coincidenti con rev.3/rev.4 e byte dei sorgenti. SHA-256 del consumer `8d50bf…c62c1d`. Tutte le nove voci `source_files` della rev.3 esistono e coincidono con i rispettivi pin nel tree pubblicato e nel candidato. | ✅ |
| 5. Metodo preservato | `baseline.py::arithmetic_mean` usa media componente per componente; `classify` usa somma assoluta divisa per 697 e astensione per più minimi entro tolleranza assoluta `1e-12`, senza cutoff sulla distanza. `evaluate` sceglie soltanto i prototipi locali quando richiesto, senza fallback globale, e produce righe valide; `metric` conserva i denominatori congelati. Codice, specifica e metodo della rev.3 sono invariati; la rev.4 li riporta coerentemente. Nessuna estrazione, classificazione su dati reali o costruzione prototipi eseguita. | ✅ |
| 6. Catena revisioni e pin rev.3 | Ricalcolati i tre SHA-256 storici, confrontati con `revision_chain` rev.4 e con `previous_manifest_sha256` nelle rev.2 e rev.3. Tutti i byte sono identici alla base. `METRIC_INTERFACE_CANDIDATE.json.source.baseline_freeze_rev003_sha256` e il contratto del raccordo continuano a identificare la rev.3 storica, senza ripuntamento alla rev.4. | ✅ |
| 7. Candidato, tag, efficacia | Rev.4: `effective=false`, verifica `PENDING`, `tag_name=null`, `tag_target_commit=null`, `tag_published=false`, nessun oggetto/peeled/record efficace inventato. Rapporto e requisiti separano OK, acquisizione del verbale, pubblicazione, decisione autoriale su nome/target, pubblicazione e controllo del tag, successiva revisione di efficacia. Il nome della release dati non è usato come nome del freeze baseline. | ✅ |
| 8. Dipendenza rev.10 | `REGISTRO_OK_RACCORDO_METRICHE.md`, verbali del raccordo e walkthrough §4.10 citano il file esatto come fonte normativa; `6aaa5b3…` non è antenato della base e il file mancava nel suo tree. MAINTENANCE §8.5 richiede provenienza recuperabile nella storia integrata: l'acquisizione chiude la lacuna nel candidato, da pubblicare. `APERTURA_SOTTOFASI_FASE03.md` riga 03.9 indica 03.4/03.6 come dipendenze; la rev.3 richiede mapping adottato/testato, sorgenti integrati e tag, non il freeze dell'intero piano. Confermata l'interpretazione circoscritta del rapporto. | ✅ |
| 9. Riuso e assenza di nuove analisi | Il rapporto separa controlli di preparazione e risultati riusati; questa review distingue ulteriormente i propri controlli nel paragrafo seguente. Verifica scientifica Normal/evidence/prototipi e tecnica del raccordo restano acquisite. Il diff contiene soltanto Markdown/JSON di specifica e tracciamento: niente dati test, nuove prestazioni o artefatti voluminosi. | ✅ |
| Assenza di regressione documentale | Guardiano eseguito ora sulla base esatta e sul candidato: entrambi 35 test, 14 failure, 1 skip, 0 errori, exit code 1. Log identici dopo la sola normalizzazione del percorso dei due checkout e della durata. Nessun nuovo fallimento. | ✅ |

Le prove sui ref remoti (`git ls-remote`, senza fetch/download di artefatti) confermano
`refs/heads/main=f1746e1e76c5657e5cb74ed765d2f22143f979ce`.
Anche `3360867751c66a39e819247f86dab8e936f8cbb3` e
`04dee86140b3ff18882f9d164beef5ab7bf33e00` sono antenati della base.
Il candidato non è ancora antenato del main pubblicato. Il tag schema 03.12 osservato è
`studio2-fase03-schema-insight-frozen-001`, oggetto
`4d15c4fb915ea9db9f7425225d231746778f0ba1`, peeled
`3c64390bc4dd58c48cc4e1e388a38989b32b3143`; nessuna nuova review 03.12 è stata effettuata.

Precisazioni di lettura, senza rilievi bloccanti: il pin della rev.3 è un pin di provenienza
nel manifest/contratto del raccordo; il lettore runtime verifica invece lo SHA-256 del
`metrics.json` passato. La fonte rev.10 sostiene l'autonomia di invalidità e astensione;
le formule esatte dei denominatori sono esplicite nel contratto/§8 e nel codice pubblicati.
Il richiamo a `4f98a297` nel campo descrittivo `independent_verification.scope` della rev.4
è un riferimento al precedente consolidamento: la base effettiva è quella completa
`f1746e1…` dichiarata nel medesimo JSON, nel rapporto, nel prompt e nella consegna Git.

Le impronte principali ricalcolate sono:

| File | SHA-256 |
| --- | --- |
| `BASELINE_FREEZE.json` | `8ac1f1e72b23484395c2955c7d14ac333e61f8743d662dd92b933e37f90547c9` |
| `BASELINE_FREEZE_rev002.json` | `b6f455f65640a5bc4353874627d4777fc596aee2b6ddb22757aaef3ab112589b` |
| `BASELINE_FREEZE_rev003.json` | `0312f416dfdbaf8984b2063df2c2e9d00e1737321b9a65dd7e32b0295a937ec8` |
| `BASELINE_FREEZE_rev004.json` | `4fa5f52bbb48ab94611a1e6a2208b96a8a15fc78b9a5c2fc7b7d7df2806a2b57` |
| `evidence/extract_evidence.py` | `46b451c2d6d8b1627993828ac9bac39532562f2fa1b27955b8a20f098ba24e97` |
| `evidence/leakage.py` | `c77ae5b11186c5b0df87b2f1df8800cb45fb25317e248fe8484d3e8283073887` |
| `baseline_numerica/extract_normal_evidence.py` | `8d50bf1466b7b87b303ff742b2e99a5d4eea8b147545ad4fa466b005d9c62c1d` |

Controlli eseguiti ora: lettura delle fonti, confronto Git/byte, SHA-256, ancestry,
ispezione statica dei punti di produzione/consumo e dei test, confronto dei pin,
interrogazione dei ref remoti, `git diff --check`, due esecuzioni del guardiano e confronto
integrale dei log normalizzati. Comando del guardiano in ciascun checkout:
`PYTHONDONTWRITEBYTECODE=1 python3 docs/test_explanation.py`.
I fallimenti sono gli stessi gruppi storici: condition C (1), ordine sezioni (1),
step27 risultati/limiti (9), step27 fatti di protocollo (3); skip legacy part-1 mancante.
Questo guardiano non certifica la correttezza scientifica né copre integralmente Studio 2.

Non rieseguiti i 19 test mirati: il prompt lo consente solo se necessario e il confronto
integrale del delta, più l'identità dei file interessati, dimostra che nessun sorgente o test
è stato alterato. I risultati 9/9 e 10/10 restano risultati storici riusati, non successi di
questa sessione. Sono riusati anche 12.341 casi valid-only e 10.626 con invalidi, review
`3360867`/`04dee86`, audit 40/40 e 320/320, evidence e 25 prototipi, conservazione di 1.336
membri. Il record `VERIFICA_RISCARICAMENTO_NORMAL_DEV.json` riporta 1.336 file, zero mismatch
e archivio `eef69b42d8506c993ac45d77208df982d138b4354d7d4134bd67ba421dc91a03`:
è stato letto, non rigenerato e non seguito da un nuovo download.
Nessuna simulazione, estrazione, costruzione prototipi, bootstrap, inferenza o run finale.
Il guardiano legge i propri risultati storici del primo studio; nessun nuovo dato test Studio 2
è stato aperto.

Il verdetto OK riguarda esclusivamente il delta `f1746e1…49bc53b…` di chiusura residui.
Non autocertifica il freeze e non chiude 03.9, 03.10, 03.8 o Fase 03.
Restano necessari nome e target autorevoli del tag baseline, acquisizione dell'OK,
pubblicazione e verifica di raggiungibilità, pubblicazione/controllo del solo tag autorizzato,
quindi un successivo record immutabile di efficacia. La rev.4 resta `effective=false`.

Fonti lette: MAINTENANCE e prompt Verifica/Prompt_LLM; cinque file del delta; freeze storici,
specifica/codice baseline e guardia estrattore; punti pertinenti di codice, test, specifica,
contratto, manifest e verbali del raccordo; registro OK, apertura sottofasi, walkthrough §4.10;
record di verifica Normal/conservazione e metadati selettivi delle due sessioni.
Costo indicativo di lettura: circa 30–40 mila token di output, con estratti ripetuti;
nessuna rassegna bibliografica o verifica scientifica ripetuta.

Prove esterne conservate accanto al verbale: `integrity.json`, `runtime_e_consegna.json`,
`ref_remoti.txt`, `guardiano_base.log`, `guardiano_candidato.log`, `guardiano_comparison.json`.
Le loro impronte sono in `SHA256_PROVE.txt`. La successiva finestra può acquisire il verbale
byte-identico; la sua impronta viene fornita separatamente, senza autoriferimento nel file.
