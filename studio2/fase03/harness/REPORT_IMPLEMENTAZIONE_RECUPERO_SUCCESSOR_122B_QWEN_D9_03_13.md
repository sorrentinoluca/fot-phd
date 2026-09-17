# Implementazione recupero successor 122B — Qwen D9 03.13

## Esito

**READY_FOR_INDEPENDENT_REVIEW.** Il recupero approvato è stato implementato e materializzato
offline. Non è stata creata alcuna execution authorization; la configurazione privata del
successore rifiuta quindi sia l'entrypoint diretto sia la CLI prima della costruzione del ledger,
del client o del trasporto.

Base di lavoro: commit `6e15fe59fe7b2f69c3e74e0bbf344985fa696c36`, tree
`7f5ba92c81bda1eaa0e13b42bc9da807d472d2c5`, parent
`0523c9279a3e760bd001daf399267c642deda02d`. Il manifest di consegna è
`IMPLEMENTAZIONE_RECUPERO_SUCCESSOR_122B_QWEN_D9_03_13.manifest.json`, SHA-256
`18dba5fc5f5241c50982ca2de4b176b7cceaeaf5d69f2ef26db23550e80eb691`.

## Decisione ed evidenza

La scelta autoriale acquisita è l'antecedente di qualificazione/configurazione. Il record redatto
lega la disposizione a S=5, lineage exactly-once, no-thinking solo producer, una qualifica tecnica
separata, T9 invariata, remediation non consumata, massimo 166/200 e review indipendente. Il
contratto controlla anche il significato di questi campi e il digest UTF-8 del testo, non soltanto
l'hash del file.

Il verbale indipendente è stato copiato byte-identico in `reviews/`; sorgente e copia hanno
SHA-256 `849e5979fa6459b4eaf505bc298c44a7dbd0e40ef9e11e26c521c23fe70bce41`.

## Lineage e quote

Il nuovo pilot è `studio2-fase03-d9-pilot-002`. Il suo ledger è stato creato da zero: non è una
copia del predecessore. Una tabella durevole distinta dallo storico S=4 contiene esattamente le
quattro richieste storiche e la richiesta nativa 122B completata/invalida, con identità,
disposizioni, binding, raw/record hash, package, approval e SHA-256 del predecessore.

L'import è transazionale, exactly-once e non transitivo. Import parziale, duplicato, selettivo,
tampered, provenienza incoerente, predecessore non sospeso e riuso dell'ID del predecessore come
richiesta o retry sono rifiutati prima dell'inserimento. I cinque addebiti sono sempre inclusi
nella quota e non possono essere azzerati da restart o cambio directory.

Il budget materializzato è:

- S predecessore: 5;
- qualifica tecnica pianificata: 1;
- massimo futuro con riserva: 161;
- massimo cumulativo: 166;
- hard stop: 200;
- margine non spendibile: 34;
- remediation consumata/autorizzata: 0/false.

## Qualifica tecnica e no-thinking

Lo stage `technical_qualification_122b` precede la conformità producer, ha quota separata esatta
di una chiamata, nessun retry e nessun uso scientifico/T9. Prompt, schema, risposta attesa,
`max_tokens=32` e criteri sono prespecificati. PASS richiede simultaneamente alias/fingerprint,
content esatto, reasoning assente/null/vuoto, `finish_reason=stop` e accounting locale/server
esatto. Ogni mismatch produce uno STOP durevole e mantiene la chiamata addebitata.

Per il solo producer 122B è ammessa la forma esatta
`extra_body.chat_template_kwargs.enable_thinking=false`; chiavi aggiuntive e pass-through sono
rifiutati. Gli stessi kwargs entrano nel rendering locale, nello stage binding, nell'evidence e
nel commitment. Consumer, sonda e gate continuano a usare i candidati prespecificati di thinking
budget. Producer prompt, schema, validatore, otto casi, ordine e `max_tokens=2560` non sono stati
modificati. Provider e service 27B del successore sono byte-identici ai precedenti.

Il supplemento registra `vllm-0.27.1-934a3247` esclusivamente come valore opaco esatto; vieta
inferenze su versione vLLM, pesi, quantizzazione, parser o capability server. Un valore futuro
diverso causa un nuovo STOP fail-closed addebitato.

## Test-first e verifiche

Rosso iniziale sul candidato precedente: 10 test, 10 errori attesi per le interfacce lineage,
qualifica tecnica e kwargs mancanti. Dopo l'assestamento del contratto di test, i byte finali della
suite sono stati rieseguiti sul commit precedente: 9 test, 9 errori per gli stessi motivi
discriminanti. Sul candidato corrente: 9/9 PASS.

La regressione finale pertinente ha eseguito 140 test D9/accounting/ledger/lifecycle: 140 PASS,
0 failure, 0 error. Sono comparsi i ResourceWarning SQLite già osservati nelle suite storiche,
senza variazione dell'esito. Il guardian documentale è stato eseguito separatamente e resta
correttamente **NON PASS storico**: 35 test, 14 failure, 1 skip; non è stato riclassificato.

## Artefatti privati

Directory: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-002`, mode `0700`; tutti i file
sono `0600`.

- ledger: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-002/ledger.sqlite3`, SHA-256
  `9c9101826d2cb39498c1e8d0b167921680c38f045aa156220a3a4ba077ed304b`;
- config: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-002/execution/pilot_d9_successor_candidate_03_13.private.json`,
  SHA-256 `f21b33a5e9a625ca8fa9f08711a09d456ee613b23b1f7f447faf6b26bd114067`;
- package lineage: SHA-256 `64b37439761d482d285baf5717fc50947dd4ca42afd745eb9a2224842fbee2a5`;
- approval lineage: SHA-256 `192a648f0acabc90406a8af6e45506cb635925bafb37a78437287a3c72faf03d`.

Il predecessore `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/ledger.sqlite3` è rimasto
byte-identico prima e dopo, SHA-256
`4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`.

Attività esterna: **zero chiamate provider, zero token, zero tunnel**. Nessuna sonda, gate, batch,
pilot, push, merge o tag. Nessuna authorization eseguibile.
