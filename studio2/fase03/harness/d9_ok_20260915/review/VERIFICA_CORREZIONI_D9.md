OK limitato offline — correzioni R-D9-01 / R-D9-02 sul tecnico `16c98f39c044d812458705234b1a3f8ee4940b34`.

# Riverifica indipendente delle correzioni D9

15 settembre 2026. Revisore: Codex, agente basato su GPT-6, task `01a0a579-3fd7-7461-8c26-5449bd3d2b7a`, «Review indipendente D9 — candidato 6a8031b». È la stessa finestra che ha emesso il precedente NON OK, distinta dalla finestra del preparatore. Nessun sottoagente. Non posso attestare autonomamente variante, revisione dei pesi o backend effettivamente servito; non rivendico diversità di famiglia del modello rispetto al preparatore.

## Esito e perimetro

R-D9-01 e R-D9-02 sono chiusi nei casi offline verificati. Le prove finali richieste sono state rieseguite autonomamente, con gli stessi byte dei test sui due runtime: i fallimenti attesi ricompaiono sul tecnico respinto e scompaiono sul corretto. Le suite complete mirata e discovery passano. Nessun nuovo rilievo bloccante emerso nel delta esaminato.

L'OK riguarda esclusivamente i byte identificati e il contratto locale delle due correzioni. Non chiude la sottofase 03.10 o la fase 03, non qualifica servizi, non autorizza chiamate, capienza, T5, GO o congelamento. Il precedente NON OK resta intatto e valido per `6a8031b`; gli OK D04 conservano il proprio riferimento e i propri limiti.

Ho letto prima `docs/MAINTENANCE.md`, poi mandato, contratto delle correzioni, report/consegna, contratto D9 originario e skill `fot-tep-harness-lessons` con il relativo riferimento. La verifica della lista task e dei processi non mostrava un'altra riverifica attiva; ho continuato questa revisione senza crearne una seconda.

## Identità e integrità

| Oggetto | Pin verificato |
| --- | --- |
| Worktree sorgente | `/Users/luker/fot-tep-harness-d9-correzioni` |
| Branch | `codex/studio2-harness-d9-correzioni` |
| Tecnico corretto | `16c98f39c044d812458705234b1a3f8ee4940b34` |
| Tree tecnico | `1dd8f84d991190d9d8316e6c56899bc115232716` |
| HEAD documentale | `cf763333b7951b4cf711e1286657f6afc6a9df87` |
| Tecnico respinto | `6a8031b25aa1208047d79cc7f030bf9cf7841e67` |
| Tree respinto | `bb3872d8fc1cbddebb4b055a8edad372e5aad430` |
| Manifest candidato | 282.272 byte, 1.062 membri; SHA-256 `a2fbabcaa997831446c4c2775d62fa6fc2078229a4c71187337be30a9ae7e4e1` |
| Remoto configurato fetch/push | `https://github.com/sorrentinoluca/fot-phd.git` |

Il remoto è la configurazione Git effettivamente letta, senza interrogazione della rete: non è attestazione dello stato attuale di main remoto. Il successore documentale aggiunge soltanto consegna e mandato. I cinque file fra `6a8031b` e `08670fb` sono documentali; in questa review il rosso usa direttamente l'archivio del tecnico `6a8031b`, non il suo successore.

Le suite girano nella copia isolata `work/corrections-candidate`, estratta con `git archive` dal tecnico esatto. Gli archivi corretto e respinto sono stati confrontati con un nuovo stream locale `git archive` dei rispettivi commit; la copia respinta è stata confrontata membro per membro con il suo archivio. Tutti i 1.062 membri del manifest candidato e i 425 Python inventariati dal preparatore coincidono con la copia corretta. L'inventario Python descrive byte, non l'esecuzione di ogni modulo.

Worktree puliti e byte tracciati di candidato, D9 originale e D04 verificati prima/dopo. Campionamento processi e `lsof` conservato; nessun descriptor aperto rilevato nel candidato al campionamento. Ciò non costituisce un lock contro writer esterni. Anche la dipendenza locale legacy dei test, 1.283 file in `fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output`, è stata improntata e ricontrollata invariata. È una dipendenza recuperabile localmente, non una certificazione della sua pubblicazione remota.

## R-D9-01: sentinel nei metadati

`harness/d9.py:_text` applica ora `strip().upper()` al confronto con PENDING, UNKNOWN e UNDECIDED. Il confronto non riscrive i documenti acquisiti. Il validatore comune è usato dalla configurazione, quindi dai runner e dalla riconferma dei binding.

Il test finale prova `" PENDING "`, tab/newline con `unknown` e NBSP con `UnDeCiDeD`, per entrambi i servizi. Le fixture aggiornano coerentemente documento, hash e autorizzazione sintetica: il rifiuto dipende dalla semantica del metadato, non da un'impronta lasciata incoerente. Verifica diagnostica specifica, assenza di chiamata al server fittizio e invariabilità di database logico, artefatti e contatori degli invii. Il controllo positivo usa una revisione sintetica non sentinel, anche circondata da spazi, completa otto richieste fittizie e riusa gli output senza nuovi invii. Non sono metadati reali qualificati.

U03 originale continua a discriminare il difetto. Le altre prove originali e le suite preservano il blocco dei prerequisiti pendenti.

## R-D9-02: recuperabilità dei tokenizer al confine

La precedente review aveva già osservato il difetto diretto sul tecnico antecedente D04: non lo rietichetto come nuova regressione D04. Questa riverifica non riapre quella campagna storica.

`validate_binding` riconferma con il medesimo `verify_tokenizer` usato all'ingresso:

- snapshot canonico R4 da `execution_config.d9.r4_snapshot`, con pin R4;
- snapshot chat assoluto da `binding.tokenizer_snapshot`, con pin del servizio selezionato da `model_for_stage(stage)`.

`producer_probe.run` persiste il percorso effettivamente risolto; budget e stability lo derivano dal piano autenticato. Sono tre file runtime modificati; il quarto Python del delta esterno alla cartella delle prove è il nuovo test. Nessuna modifica al ledger, alle quote o allo schema SQLite.

La lettura `_binding` verifica prima l'hash del binding e poi richiama questo controllo. `bind_stage` lo esegue prima di inserimento o riuso, anche chiuso. La riserva base, remediation, retry e tripletta passano dal controllo comune nelle transazioni esistenti; l'inventario D04 riconferma i contributori. `execute_request` riacquisisce il binding prima di riuso, riserva e trasporto; anche l'esportazione del journal lo riacquisisce. Questi collegamenti sono stati letti nel codice; non presento ogni combinazione possibile di operazione/stadio come nuova prova tokenizer eseguita. Le regressioni D01–D04 sono comprese nelle suite complete.

I test finali esercitano directory R4/chat distinte, perdita o alterazione di tokenizer.json e tokenizer_config.json, alterazione del template, riserva diretta e restart, successo seguito da nuovo guasto, rebind, riuso chiuso e mancato campo. Confrontano stato logico SQLite, file di output/preparazione e invii rispetto alla baseline dopo l'iniezione del guasto. L'assenza del file `.jinja` con template inline già pinnato resta un positivo legittimo.

La regressione di trasporto percorre `_tracked_call → execute_request → Provider` reali con SDK fittizio: il positivo registra un invio e nove intenti cumulativi; la perdita distinta di R4 o chat blocca prima di SDK, nuovo intento e journal. È il nuovo test del preparatore, non lo script osservazionale originale rinominato. I suoi byte sono identici sui due runtime.

Ho aggiunto due verifiche indipendenti sul corretto:

1. Tre snapshot con revisioni/contenuti/pin differenti: R4, chat122B, chat27B. Principale e alternativo completano otto richieste fittizie ciascuno; entrambi i binding chiusi si riusano senza effetti. Sostituire i byte27B con quelli122B provoca rifiuto di lettura, rebind e restart; ripristinare i byte corretti recupera il positivo.
2. Un binding budget valido viene trasformato in una fixture legacy priva di `tokenizer_snapshot`, aggiornando coerentemente l'hash persistito. Lettura, restart e nuova riserva lo rifiutano senza effetti e senza backfill. Il ledger generico senza `execution_config` mantiene il perimetro storico, verificato dalle suite.

La prima esecuzione aggiuntiva ha avuto un errore dell'assertion sul percorso macOS `/var` contro il suo equivalente risolto `/private/var`. Ho conservato v1, log e fixture, e corretto soltanto l'aspettativa con `Path.resolve()`. La versione finale passa 2/2. Questi due controlli aggiuntivi sono verdi sul corretto; non sono inclusi nei conteggi rosso/verde richiesti. I ResourceWarning delle connessioni SQLite di prova sono conservati nei log, senza trasformarli in errori comportamentali o normalizzarli.

## Esecuzioni indipendenti

| Prova | Metodi | Fallimenti | Errori | Skip | Esito |
| --- | ---: | ---: | ---: | ---: | --- |
| Mirata completa — corretto | 156 | 0 | 0 | 0 | PASS |
| Discovery completa — corretto | 191 | 0 | 0 | 0 | PASS |
| Correzioni finali — respinto | 11 | 32 | 0 | 0 | Rosso discriminante |
| Stesse correzioni — corretto | 11 | 0 | 0 | 0 | PASS |
| U01–U08 originali — respinto | 8 | 3 | 0 | 0 | Rosso discriminante |
| Stesse U01–U08 — corretto | 8 | 0 | 0 | 0 | PASS |
| Trasporto reale / SDK fittizio — respinto | 3 | 2 | 0 | 0 | Rosso discriminante |
| Stesso test trasporto — corretto | 3 | 0 | 0 | 0 | PASS |
| Guardiano — respinto | 35 | 14 | 0 | 1 | NON PASS storico |
| Guardiano — corretto | 35 | 14 | 0 | 1 | NON PASS storico |
| Controlli indipendenti aggiuntivi — corretto | 2 | 0 | 0 | 0 | PASS |

Metodi, subtest e assertion non sono sommati. Mirata/discovery si sovrappongono; 156+191 non è un totale di test distinti. I 32 fallimenti del rosso correzioni sono assertion/subtest negli 11 metodi, senza errori. Esiti ricavati dai log e confrontati con gli exit code, non dal solo completamento del launcher.

Ambiente: Python Anaconda 3.13.9, SQLite 3.51.0, macOS 26.6.2 ARM64. Le suite hanno `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` separati e cwd nella copia isolata. Il launcher completo è [run_review_tests.py](evidence/run_review_tests.py); ogni esecuzione ha un `*_command.json` con argomenti, cwd, override, exit code e durata. Non è stato eseguito il launcher del preparatore che avrebbe scritto nelle sue destinazioni.

Comandi principali:

```text
/opt/anaconda3/bin/python3 -m unittest -v
  studio2.fase03.harness.test_c01_c03
  studio2.fase03.harness.test_d01_replay
  studio2.fase03.harness.test_d02_predecessors
  studio2.fase03.harness.test_d03_contract
  studio2.fase03.harness.test_d04_open_quota
  studio2.fase03.harness.test_d9
  studio2.fase03.harness.test_d9_corrections
  studio2.fase03.harness.test_harness_offline
  studio2.fase03.harness.test_metric_raccordo
  studio2.fase03.harness.test_revisions
  studio2.fase03.tests.test_execution_guard
  studio2.fase03.tests.test_protocol
/opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
/opt/anaconda3/bin/python3 docs/test_explanation.py
```

La prima invocazione è mostrata su più righe per leggibilità; l'array eseguibile esatto è in `targeted_command.json`. I tre script finali correzioni/U/trasporto sono eseguiti per percorso con `FOT_D9_TARGET` impostato al rispettivo runtime. `PROBE_OUTPUT` e `TRANSPORT_RESULTS` puntano a nuove destinazioni assolute in questo pacchetto. Lo script U è una copia byte-identica dell'originale: nessun suo output precedente è stato sovrascritto.

## Guardiano, conservazione e limiti

Il guardiano resta **NON PASS: 35 test, 14 fallimenti storici, 1 skip, 0 errori**. Gli identificativi completi dei fallimenti/subtest sono confrontati, non soltanto il numero: nessun peggioramento fra respinto e corretto. Il confronto è conservato in [guardian_comparison.json](evidence/guardian_comparison.json). Questo esito documentale distinto non viene etichettato PASS.

`git diff --check` su Python/Markdown del delta passa. Il controllo integrale restituisce 2 per whitespace nei log grezzi e nelle fixture deliberate: le prove sono conservate senza correzioni cosmetiche. Il dettaglio grezzo è in [source_audit.json](evidence/source_audit.json).

Il verbale precedente rimane 18.659 byte, SHA-256 `9e1de541cdebef75eac560aa9eb6261db3da5e3f04484e9fee006dd748e65b45`; il suo manifest resta SHA-256 `269bfc69e1d1028b4466768d801d21bbf6e31b96266434ce53f16f9e03d0b435`. Tutti i 591 membri, oltre a manifest e consegna, sono verificati sia nella sede originale sia nella copia acquisita dal preparatore. Anche l'archivio originale da 244.633.206 byte rimane recuperabile localmente e invariato. Il certificato finale registra il controllo prima/dopo; nessun file candidato o precedente verbale è modificato.

Il nuovo [archivio tecnico](candidate_16c98f3.tar.gz) conserva il candidato; script, log, nuove fixture ed inventari sono in `evidence/`. [MANIFEST.json](MANIFEST.json) enumera i membri del nuovo pacchetto con byte e SHA-256; [CONSEGNA.json](CONSEGNA.json) impronta verbale e manifest. Gli hash provano integrità rispetto ai byte locali verificati, non una firma crittografica o la provenienza dei pesi. Nessuna pubblicazione o recuperabilità remota è dichiarata: non sono stati usati servizi o rete per questa review.

La riconferma vale per i byte letti al confine della decisione; non crea un lock globale sul filesystem e non garantisce immutabilità contro un writer successivo al controllo. I contatori e gli SDK sono fittizi, i socket nelle fixture dei runner sono vietati. Non sono state eseguite inferenze, simulazioni TEP, sonde o pilot scientifici, né modificati ledger operativi. Nessun SSH, push, merge o tag.

Restano invariati P=C=122B, alternativo27B completo16, consumer fisso nello swap, Terra storico interno, temperature122B omessa. Metadati/qualifiche reali, ordine1a, collocazione operativa dell'alternativo, riconciliazione S4/3 e autorizzazioni esecutive rimangono pendenti. Nessuna nuova approvazione dei ruoli è stata richiesta o inferita dalle fixture.
