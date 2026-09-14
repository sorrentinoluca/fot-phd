# REPORT — soglie Normal, sotto-fase 03.5

**Revisione correttiva del 2026-09-14**, su richiesta dell’autore dopo il verbale NON OK sul
candidato `819b12e97fb94d501032655ec2f226139e6c5ca5`. Il report e l’addendum originali restano
recuperabili a quel commit. Questa revisione corregge D1–D4 e completa C4; non costituisce
una nuova verifica indipendente. La Fase 03 non è chiusa.

## Perimetro, fonti e responsabilità

Fonte autorevole: `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md`, **rev. 19**,
requisiti iniziali, P0, C0–C4 e controllo dei pareggi; prevale sul piano §6.3.
La specifica è `SPECIFICA_SOGLIE_NORMAL.md`; la base effettiva della 03.5 è
`53a3e9299ff7548fde30c54014a340d7113bf882`, che contiene la precedente **03.4, perimetro Q8**.
`b7f359f`, citato come base nella specifica, è il precedente contesto bibliografico; il suo
confronto col candidato include anche la 03.4 e non va descritto come delta della sola 03.5.

| Passo | Modello / esecutore | Finestra e profilo |
|---|---|---|
| Specifica e scelta operativa | `gpt-5.6-luna` | `01a09b8c-822a-70a3-a5e0-246d9c8bf840`; decisionale |
| Piani, launcher, smoke, correzione impronta R2 | `gpt-5.6-luna` | stessa finestra; implementativo |
| Batch 350+150 | script MATLAB/Simulink R2025b ARM; comando fornito all’autore per esecuzione locale | esecutivo-batch; nessuna inferenza LLM nei run |
| Audit, score, freeze, FAR, conservazione e addendum originale | `gpt-5.6-luna` | stessa finestra; analisi/implementazione |
| Verifica del candidato 819b12e | `gpt-6-astra` | `01a09f81-e508-77e0-b510-872bdeba46e3`; verifica in finestra distinta, esito NON OK |
| Presente correzione e completamento C4 | `gpt-6-astra` | stessa finestra del verificatore NON OK, reasoning `high`, ora incaricata dall’autore della correzione; implementazione/analisi, non verifica indipendente di sé stessa |

Identità ricostruite dai `turn_context` e dalle esecuzioni registrate, non dalla sola etichetta
“Codex”. Il rollout esecutore archiviato ha SHA-256
`3f21bd048089023c500f2393acaa237e328a59c6adc78987e5d582dadcf16e47`.
I metadati pertinenti della finestra di correzione sono conservati, senza copiare il rollout,
in [`evidence/EXECUTOR_IDENTITY.json`](evidence/EXECUTOR_IDENTITY.json): otto `turn_context`
registrano `gpt-6-astra`, effort `high`; il rollout originale ha SHA-256
`45c71aca14e2f40818f394c29e7a52f160493c0c8c56759c62976075960f3aad`.
Il verbale originale rimane acquisito byte per byte in
[`evidence/VERIFICA_SOGLIE_NORMAL_NON_OK_819b12e.md`](evidence/VERIFICA_SOGLIE_NORMAL_NON_OK_819b12e.md);
metadati e prove sono nel supporto `/Users/luker/verifica-soglie-normal-support-WE8Qqc`.
Non si attribuisce al terminale umano una registrazione più forte di quella disponibile.

## Risultati, nell’ordine di produzione

1. **Specificazione, 8ec3c38.** Baseline U1/R2 N1–N5 come sola `baseline_fit`; score A e
   riferimenti congelati in Fase 02; burn-in 20 h. 350 `cal_thr`, una finestra per run in
   posizione J uniforme fra 1 e 10, generazione economica fino a `20+5J` e uso dell’ultima
   finestra; 150 `far_ver` di 70 h con dieci finestre e posizione primaria preassegnata.
   Trip-stop e fallback R2 predefiniti. Specifica iniziale prima degli smoke e dei nuovi run.
2. **Piani e smoke, 6c128c4 / 4fb1620.** Stream cal 40000–40349, FAR 50000–50149,
   smoke 49900–49901, disgiunti dai lotti pertinenti. Quattro piani riprodotti byte per byte
   nella verifica. Smoke definitivo: 1 finestra cal e 10 FAR, senza trip; 42,79 s reali,
   runtime nei manifest circa 10,00 e 10,25 s. Gli smoke non entrano nei lotti scientifici.
3. **Correzione pre-batch, d09e7ed.** Riparata l’impronta troncata `tep_features_sha256`
   mediante nuovo script `recheck_r2_guard.py` e test, non mediante correzione manuale del
   digest. Valore completo `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c`.
   La scansione allora eseguita non trovò altri valori troncati negli artefatti controllati.
   **Solo in quella finestra di correzione** batch, soglia e FAR erano ancora fuori perimetro:
   furono prodotti successivamente, come riportato sotto.
4. **Batch e guardia.** 350+150 run completi, 500 workbook; audit con zero trip/errori
   tecnici e zero file estranei al lotto. Guardia R2 `pass=true`; confermata nella verifica
   dai dieci pilot qualificati con scarto massimo `5,44e-15`. Per S: scarto mediana
   0,3898894833 MAD e rapporto MAD 0,9562001603. Ramo attivo 350+150, fallback non attivato.
   Totale `ΣJ=2022`: **17.110 h cal + 10.500 h FAR = 27.610 h**. Il log contiene warning
   di espansione buffer Variable Time Delay, non arresti del batch.
5. **Calibrazione e freeze, 0127ef4 / 9507143.** CSV con 350 score; rango
   `ceil((350+1)(1−0,05))=334`, soglia **13.623626738268857**, regola stretta **S > threshold**.
   Freeze alle **2026-09-13 18:28:19 UTC**, prima dell’analisi FAR registrata; contiene
   le 150 impronte del sigillo. SHA-256 del freeze:
   `ff5c27002a2548003e4bc5f54805cda3754fb19b9cb2559222996b9c7f7e14a9`.
   Non è stato modificato successivamente, inclusa questa correzione.
6. **FAR, 0b2aac5.** Primario **11/150 = 7,333333%**, CP95%
   **[3,717461%;12,742416%]**. Secondario **108/1500 = 7,2%**, SE bootstrap
   **0,751251 punti percentuali**, IC percentile95% **[5,733333%;8,733333%]**.
   Ricampionamento per run: seed 20260913, 10.000 repliche; le dieci finestre del run
   restano insieme. Diagnostica, posizioni 1–10: **14,10,12,6,14,8,11,13,10,10**.
   I 35 score cal e le 150 finestre di 15 run FAR ricalcolati nella verifica hanno errori
   massimi rispettivamente `3,55e-15` e `5,33e-15`, entro `1e-8`.
7. **Conservazione, 264a20e / 0802c31.** Release `studio2-fase03-normal-v1`, archivio di
   **943.793.152 byte**, SHA-256
   `bbcfd0c43a5fbda624deba62fea746150dda4a6d649e6372b8e118270277ac1d`.
   Riscaricamento verificato: 515/515 file attesi per percorso, dimensione e hash;
   150/150 sigilli FAR coincidenti. Distinzioni sul contenuto dell’archivio sotto.
8. **Chiusura originaria / addendum / correzione.** Report a `582e575`, addendum a
   `819b12e` (solo report, 24 righe aggiunte). La presente revisione corregge le formulazioni
   contestate e aggiunge il completamento C4 dai soli score già congelati.

**Errata della specifica storica.** In “Contabilità e prestazione attesa”, «35.000 h piene
per cal_thr» va letto **24.500 h per i 350 cal_thr pieni**; 35.000 h è il totale per 500 run
pieni. La proiezione economica di 27.610 h è corretta. Si registra qui l’errata senza
riscrivere la specifica pre-esecuzione o il suo snapshot nella release.

## Completamento C4: pareggi e incertezza della soglia

Fonti nuove: [protocollo operativo](THRESHOLD_UNCERTAINTY_PROTOCOL.json),
[script riproducibile](complete_threshold_uncertainty.py) e
[risultato numerico](THRESHOLD_UNCERTAINTY.json).

**Temporizzazione dichiarata:** l’obbligo C4 e lo score/rango precedono la calibrazione.
Seed **20260914**, **10.000** repliche e convenzione percentile95% sono stati definiti
**ora, dopo l’osservazione dei risultati e prima di questo bootstrap supplementare**.
La scelta tecnica è post-hoc rispetto ai dati; non viene presentata come preregistrazione
cieca. Protocollo registrato prima del calcolo, impronte degli input controllate prima e
dopo; nessuna scelta modificata in base all’esito.

Sono ricampionati con rimpiazzo **350 run di calibrazione**, ciascuno rappresentato dal suo
unico score già prescritto. Ogni replica usa il **334° valore ordinato**, non un quantile
interpolato. Fit e riferimenti di Fase 02 restano fissi. Questo bootstrap non include
l’incertezza di stima della baseline e non produce una soglia operativa sostitutiva.

| Quantità | Risultato | Interpretazione |
|---|---|---|
| Score cal distinti | **350/350**, zero gruppi duplicati | diagnostica sull’intero campione |
| Molteplicità alla soglia | **1** | un’osservazione, nessun pareggio |
| Beta(17,334), media | **4,843304843%** | media del FAR condizionale su ripetute calibrazioni, sotto le ipotesi |
| Beta, SD | **1,144245586 punti percentuali** | dispersione teorica fra calibrazioni |
| Beta, intervallo centrale90% | **[3,118163613%;6,860631796%]** | distribuzione teorica del FAR, non IC empirico della soglia realizzata |
| Bootstrap della soglia, SE | **0,5821769414** | unità dello score, non percentuale |
| Bootstrap della soglia, percentile95% | **[12,2632210962;14,2087372188]** | approssimazione da 10.000 ricampionamenti |

La Beta è riportata **solo sotto continuità di S**, IID dei run pertinenti e funzione di
score fissata indipendentemente da calibrazione/verifica. L’assenza di pareggi è diagnostica,
non dimostrazione di continuità o IID. Il nuovo script controlla tutti i pareggi e omette la
rendicontazione Beta se ne osserva, anziché trattarla come “approssimata”. I duplicati
introdotti dal ricampionamento bootstrap non sono pareggi del campione originario.

**Controllo della variabilità Monte Carlo.** La distribuzione empirica esatta del bootstrap
è verificabile senza simulazioni TEP: per ogni score x,
`P(T* ≤ x) = P(Binom(350, F_emp(x)) ≥ 334)`. Dà SD **0,5831861336** e intervallo centrale
con inversa generalizzata95% **[12,2632210962;14,4086543351]**. La CDF campionata dista al
massimo **0,00371907** da quella esatta; lo scarto della media è −0,294 errori standard
Monte Carlo. La distribuzione è discreta e l’estremo superiore percentile può saltare
fra score adiacenti: il risultato delle 10.000 repliche non viene sostituito scegliendo
un altro seed. Il confronto esatto è un controllo del ricampionamento empirico, **non**
un intervallo di confidenza esatto per il quantile della popolazione.

**Precisazione N1, successiva alla riverifica e concordata con l’autore.** Si mantengono
entrambi gli intervalli. Nella distribuzione bootstrap empirica, condizionata ai 350 score
osservati, le probabilità degli intervalli chiusi (estremi inclusi) sono:

| Intervallo della soglia | P(T* nell’intervallo) | P(T* oltre l’estremo superiore) |
|---|---:|---:|
| Monte Carlo: [12,2632210962;14,2087372188] | **95,38705407%** | **2,51853266%** |
| Inversa generalizzata esatta: [12,2632210962;14,4086543351] | **96,89204510%** | **1,01354163%** |

Le probabilità sono calcolate sui valori non arrotondati. La coda inferiore stretta comune
vale **2,09441327%**. La CDF esatta in 14,2087372188 vale **0,9748146734**, appena sotto
0,975; il quantile esatto al 97,5% è 14,4086543351. È la stima Monte Carlo dell’estremo
a variare fra ricampionamenti, mentre l’inversa generalizzata della CDF empirica è definita.
Queste sono **masse di probabilità nella distribuzione bootstrap empirica**, non coperture
frequentiste garantite del quantile della popolazione. Nessuna soglia o risultato numerico
congelato viene sostituito.

Fonte numerica della precisazione: controllo autonomo della riverifica, acquisito in
[`evidence/mc_vs_exact_container.json`](evidence/mc_vs_exact_container.json);
verbale e suo perimetro sono identificati nella sezione di consegna sotto.

## Confronto FAR teorico e osservato — correzione dell’addendum

Si distinguono **α nominale=5%**, **17/351≈4,8433%** come media teorica fra calibrazioni,
**q(T)** come FAR ignoto della soglia effettivamente ottenuta per la miscela uniforme delle
dieci posizioni, e le stime **11/150** e **108/1500** di q(T).

Per `X~Binomiale(150,p)`, la probabilità di **3–12 superamenti inclusi** è:

| p assunto per la diagnostica | Probabilità |
|---|---:|
| 17/351 | **0,9470465066** |
| 0,0484, arrotondamento del registro | **0,9471050102** |
| 0,05 | **0,9433302578** |

L’addendum a 819b12e associava impropriamente 0,947 al 5%; quel riferimento è qui corretto.
Il registro usa lo scenario con FAR vero circa 4,84%. Lo scenario binomiale a p fissato
non dimostra che q(T) sia proprio quel valore: q(T) varia con la calibrazione.

Il conteggio primario 11 è compreso fra 3 e 12 e il CP95% include sia 4,8433% sia 5%.
La compatibilità non dimostra uguaglianza del FAR, continuità, IID o una verifica stretta
della Beta. Con 150 run si controlla l’ordine di grandezza con la precisione limitata
indicata dal registro; non si verifica strettamente la legge Beta fra calibrazioni.

Il secondario 7,2% ha IC95% **che esclude 4,8433% e anche 5%**. Stima il FAR della
**miscela uniforme delle dieci posizioni**, la stessa quantità coperta dalla garanzia
sotto le ipotesi applicabili. I FAR delle singole posizioni possono invece differire.
La dipendenza intra-run riguarda il calcolo dell’incertezza: per questo si ricampionano
interi run. Non sono giustificati 1500 trial binomiali indipendenti. Primario e secondario
stimano q(T) con procedimenti diversi; l’esclusione della media teorica dal secondo
intervallo non è una contraddizione con la variabilità della soglia realizzata.

La posizione 1 ha 14 superamenti come la 5: non emerge un massimo esclusivo in posizione 1.
Questo non prova burn-in sufficiente e non autorizza interpretazioni causali immediate.
Nessuna modifica di burn-in, finestra, inclusione dei run o soglia deriva da questi dati.

## Sequenza di processo e limiti probatori

I manifest datati UTC registrano `cal_thr` il 13 settembre **16:38:19–17:19:15** e
`far_ver` **17:19:17–17:42:24**, dunque prima del freeze alle **18:28:19**.
L’[handoff](HANDOFF_BATCH.md) prevedeva esplicitamente entrambi i piani in un processo
MATLAB e prescriveva il freeze **prima di aprire le finestre far_ver**. Il registro chiede
il freeze dopo calibrazione e prima della verifica; non contiene un divieto esplicito di
simulare e conservare far_ver prima del freeze. L’attribuzione all’handoff di tale divieto,
nell’addendum precedente, era quindi errata.

Le tracce accessibili sostengono la sequenza: generazione e conservazione; lettura dei
byte FAR per hash e dei metadati di manifest; score cal; freeze; apertura analitica FAR.
L’audit esaminato decodifica i workbook solo nel ramo cal_thr. La prima invocazione
registrata dello script FAR è successiva al freeze; gli score degli smoke erano già
stati calcolati sui run separati 49900–49901. Una versione intermedia del conteggio
secondario fu corretta prima di 0b2aac5; la soglia non cambiò.

**Il sigillo prova identità, non mancata lettura.** I log e l’assenza di derivati Git non
escludono letture umane o da processi non registrati, né file poi rimossi. I file FAR
erano accessibili prima del freeze: è un limite di segregazione operativa da dichiarare.
La generazione anticipata non assolve né invalida automaticamente il FAR. Il 2026-09-14
l’autore ha approvato la decisione registrata in
[`DECISIONE_AUTORE_FAR.md`](DECISIONE_AUTORE_FAR.md): accetta l’uso dei risultati FAR e
mantiene invariata la soglia, dichiarando che l’assenza assoluta di consultazioni non
registrate non è dimostrabile. Questa accettazione resta distinta dalle prove tecniche.

## Conservazione, snapshot e provenienza

Il [manifest](MANIFEST_CONSERVAZIONE.csv) e [ARTIFACT_STORAGE.json](ARTIFACT_STORAGE.json)
continuano a descrivere l’asset pubblicato, senza modifiche. Contabilità del riscaricamento:
**515 file attesi coincidenti, 0 mancanti, 0 mismatch**, più il manifest stesso come
**unico file ordinario extra**, byte-identico a Git: totale **516 file ordinari**.
Sono separati **514 membri AppleDouble** e **514 membri con metadati PAX associati**;
non sono run aggiuntivi.

Il report archiviato, SHA-256 `b22acf0f098482344f00c1fbabea4ba946fc382ab7dd982c26979bd8a40a01b0`,
è lo snapshot pre-chiusura presente da d09e7ed a 0802c31. Non include 582e575, 819b12e
o questa correzione. La release è integra e immutata; la storia del report resta in Git,
mentre i nuovi piccoli artefatti C4 appartengono alla presente revisione ancora non committata.
Non si dichiarano già pubblicati né inclusi nel vecchio manifest.

U1/R2 resta soltanto `baseline_fit`, pre-specificato nello studio ma su dati già osservati;
nessuna promozione a cal_thr, FAR o test. Provenienza in `studio2/PROVENIENZA.md` §§4,10.
Il commit storico 309b944f… non è disponibile localmente: è verificata l’impronta della
sorgente Normal, non il suo legame a quell’oggetto Git. Il completamento C4 usa soltanto
il CSV congelato; dettagli post-hoc e impronte sono registrati nella nuova §10.1.

## Verifiche della presente correzione e stato di consegna

Comando C4 originariamente eseguito dal worktree
`/Users/luker/fot-tep-correzione-soglie-normal`:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/luker/verifica-soglie-normal-support-WE8Qqc/venv/bin/python studio2/fase03/soglie_normal/complete_threshold_uncertainty.py --output studio2/fase03/soglie_normal/THRESHOLD_UNCERTAINTY.json
```

Ambiente registrato nell’output: Python 3.11.5, NumPy 2.4.6, SciPy 1.17.1, macOS26.6.2
x86_64. Il risultato include hash del codice, del protocollo e degli input. Il comando
rifiuta di sovrascrivere un output esistente. Non importa FAR né i workbook e non richiama
il simulatore o lo score fitting. Tempo e costo: un solo script locale, 3,5 milioni di
indici di ricampionamento; nessun tool per replica.

La riproduzione non dipende più da quel venv esterno: ambiente e dipendenze sono fissati in
[`requirements-c4.txt`](requirements-c4.txt) e i comandi che producono un output temporaneo,
senza sovrascrivere quello registrato, sono in
[`REPRODUCIBILITY_C4.md`](REPRODUCIBILITY_C4.md).

Test della sotto-fase: **8 PASS** (4 preesistenti, 4 nuovi). I nuovi test confrontano la
legge esatta con enumerazione esaustiva di un piccolo campione con pareggi, verificano
la statistica d’ordine, rifiutano input non validi e impronte alterate. Script stdlib PASS.
`python3 docs/test_explanation.py`, prima/dopo: **35 test, 14 failure e 1 skip**, con
identità dei fallimenti e parametri dei subtest invariati; nessuna regressione.
Quel test copre documenti storici, non convalida C4. Nessuna coppia MD/HTML toccata.

Log, controlli di integrità e diff sono conservati in
`/Users/luker/correzione-soglie-normal-support-XKCNMN`.
Il verbale NON OK su 819b12e resta intatto ed è acquisito byte per byte in
[`evidence/VERIFICA_SOGLIE_NORMAL_NON_OK_819b12e.md`](evidence/VERIFICA_SOGLIE_NORMAL_NON_OK_819b12e.md),
SHA-256 `ccaec80994522ba5167fdf9ef6f3500d220c19f86977de53afdb2dee7be548bd`.
La riverifica indipendente ha dato **OK tecnico**
ai sei file candidati, incluso il report con SHA-256
`5323438f8f2426f859537e12dee24139c3b8daa0b858b01934b4f7fc23308e32`.
Il verbale è acquisito byte per byte in
[`evidence/VERIFICA_CORREZIONI_SOGLIE_NORMAL_OK.md`](evidence/VERIFICA_CORREZIONI_SOGLIE_NORMAL_OK.md),
SHA-256 `d98a2856647493b0e96fc1198ac32c457510fc10399538511373655e1b6f1c9e`,
verificatore dichiarato `claude-fable-5-1`, finestra `session_01NfcCmkTeXtdvJZcykoHddT`.
L’OK riguarda quello snapshot: la presente precisazione N1 e questo aggiornamento di stato
sono successivi e non vengono attribuiti alla verifica già conclusa. Il report precedente
resta acquisito in
[`evidence/REPORT_SOGLIE_NORMAL_SNAPSHOT_OK.md`](evidence/REPORT_SOGLIE_NORMAL_SNAPSHOT_OK.md)
con la stessa impronta. L’autore ha concordato la presentazione N1 e ha poi approvato la
distinta decisione sul limite di tracciabilità FAR. Nessuna chiusura della Fase 03 è implicita.

La verifica mirata successiva ha conservato il proprio primo verdetto **NON OK** in
[`VERIFICA_DELTA_N1_IDENTITA.md`](VERIFICA_DELTA_N1_IDENTITA.md): rilevava un aggiornamento
non necessario di `PROVENIENZA.md`. Quel file è stato ripristinato byte-identico allo snapshot
approvato. Le appendici separate
[`01`](VERIFICA_DELTA_N1_IDENTITA_APPENDICE_01.md) e
[`02`](VERIFICA_DELTA_N1_IDENTITA_APPENDICE_02.md), svolte da `gpt-5.6-sol`, reasoning `high`,
sessione `01a0a03d-6daf-7540-947c-6f94ab12b2f5`, hanno dato **OK** rispettivamente sulle
impronte e sul supporto locale di riproducibilità. L’aggiornamento coordinato del walkthrough
è stato aperto soltanto dopo questi OK.

Fuori perimetro: nuove simulazioni, nuova calibrazione operativa, modifica dei dati/score,
freeze o soglia, pubblicazione della release, interventi sulle sotto-fasi 03.8/03.9 e chiusura
Fase03. Copia principale e worktree del verbale preservati.

**Commit al momento della redazione:** non ancora eseguito; nessun push/tag/merge. Le modifiche sono pronte da rivedere nel branch
`codex/studio2-soglie-normal-correzioni`; dopo riverifica, messaggio proposto:
`studio2(fase03): completa C4 e corregge il report soglie Normal`.

## File della presente revisione

- `studio2/fase03/soglie_normal/REPORT_SOGLIE_NORMAL.md`: report riconciliato, quantità FAR, processo, snapshot, modelli e risultati C4.
- `studio2/PROVENIENZA.md`: precisazione del limite probatorio e nuova provenienza del completamento C4.
- `studio2/fase03/soglie_normal/THRESHOLD_UNCERTAINTY_PROTOCOL.json`: scelte tecniche datate prima del nuovo bootstrap, con marca temporale onesta e input immutabili.
- `studio2/fase03/soglie_normal/complete_threshold_uncertainty.py`: calcolo C4, controllo di tutti i pareggi, verifica hash e controllo esatto del bootstrap empirico.
- `studio2/fase03/soglie_normal/THRESHOLD_UNCERTAINTY.json`: risultati supplementari C4 e impronte, senza sovrascrivere risultati congelati.
- `studio2/fase03/soglie_normal/tests/test_threshold_uncertainty.py`: quattro controlli numerici e di integrità della nuova procedura.
- `studio2/fase03/soglie_normal/DECISIONE_AUTORE_FAR.md`: accettazione esplicita del limite di tracciabilità, separata dalle prove tecniche.
- `studio2/fase03/soglie_normal/evidence/`: verbali precedenti e snapshot approvato acquisiti byte per byte, fonte numerica N1 e metadati minimi dell’identità dell’esecutore.
- `studio2/fase03/soglie_normal/requirements-c4.txt`: versioni Python fissate per ricostruire l’ambiente C4 senza il venv esterno.
- `studio2/fase03/soglie_normal/REPRODUCIBILITY_C4.md`: procedura locale di riproduzione e confronto, con output temporaneo.
- `studio2/fase03/soglie_normal/VERIFICA_DELTA_N1_IDENTITA.md` e appendici 01–02: verbale mirato preservato con il primo NON OK e i successivi OK separati.

Letture della correzione: contratto e prompt di processo, registro P0/C4/pareggi, specifica,
report, provenance e verbale precedente; circa 15 mila token, stima non di fatturazione.

## File del pacchetto originale, 53a3e92 → 819b12e

Elenco ricostruito da Git senza escludere percorsi; **questi non sono nuovi file modificati
dalla correzione**, salvo report e provenienza già indicati sopra.

- `studio2/PROVENIENZA.md`: registrazione del lotto Normal e del riuso U1/R2.

- `studio2/fase03/soglie_normal/ARTIFACT_STORAGE.json`: identificazione della release e verifica del riscaricamento.

- `studio2/fase03/soglie_normal/CAL_THR_SCORES.csv`: 350 score di calibrazione.

- `studio2/fase03/soglie_normal/FAR_VERIFICATION.json`: risultati e 1500 score FAR.

- `studio2/fase03/soglie_normal/FAR_VERIFICATION.md`: esposizione dei risultati FAR.

- `studio2/fase03/soglie_normal/HANDOFF_BATCH.md`: consegna del launcher e ordine freeze/apertura.

- `studio2/fase03/soglie_normal/LOT_AUDIT.json`: audit del lotto e impronte workbook.

- `studio2/fase03/soglie_normal/MANIFEST_CONSERVAZIONE.csv`: inventario dei 515 file conservati.

- `studio2/fase03/soglie_normal/R2_GUARD_RECHECK.json`: attestazione delle impronte e guardia R2.

- `studio2/fase03/soglie_normal/REPORT_SOGLIE_NORMAL.md`: report e addendum originali.

- `studio2/fase03/soglie_normal/SMOKE_CHECK.json`: risultati smoke.

- `studio2/fase03/soglie_normal/SPECIFICA_SOGLIE_NORMAL.md`: specifica pre-esecuzione e contabilità.

- `studio2/fase03/soglie_normal/THRESHOLD_FREEZE.json`: soglia e sigillo congelati.

- `studio2/fase03/soglie_normal/analyze_far_ver.py`: implementazione analyze far ver.

- `studio2/fase03/soglie_normal/audit_lot.py`: implementazione audit lot.

- `studio2/fase03/soglie_normal/build_generation_plan.py`: implementazione build generation plan.

- `studio2/fase03/soglie_normal/conserve_normal.py`: implementazione conserve normal.

- `studio2/fase03/soglie_normal/freeze_threshold.py`: implementazione freeze threshold.

- `studio2/fase03/soglie_normal/generate_normal_runs_soglie.m`: implementazione generate normal runs soglie.

- `studio2/fase03/soglie_normal/launch_normal_batch.sh`: implementazione launch normal batch.

- `studio2/fase03/soglie_normal/plans/cal_thr.csv`: piano immutabile con stream e posizioni.

- `studio2/fase03/soglie_normal/plans/far_ver.csv`: piano immutabile con stream e posizioni.

- `studio2/fase03/soglie_normal/plans/smoke_cal_thr.csv`: piano immutabile con stream e posizioni.

- `studio2/fase03/soglie_normal/plans/smoke_far_ver.csv`: piano immutabile con stream e posizioni.

- `studio2/fase03/soglie_normal/preflight.py`: implementazione preflight.

- `studio2/fase03/soglie_normal/recheck_r2_guard.py`: implementazione recheck r2 guard.

- `studio2/fase03/soglie_normal/runs/smoke_001/cal_thr/generation_manifest.csv`: manifest di esecuzione smoke.

- `studio2/fase03/soglie_normal/runs/smoke_001/far_ver/generation_manifest.csv`: manifest di esecuzione smoke.

- `studio2/fase03/soglie_normal/runs/smoke_002/cal_thr/generation_manifest.csv`: manifest di esecuzione smoke.

- `studio2/fase03/soglie_normal/runs/smoke_002/far_ver/generation_manifest.csv`: manifest di esecuzione smoke.

- `studio2/fase03/soglie_normal/runtime/smoke_foreground/matlab.log`: log MATLAB dello smoke.

- `studio2/fase03/soglie_normal/runtime/smoke_foreground/matlab_002.log`: log MATLAB dello smoke.

- `studio2/fase03/soglie_normal/score_cal_thr.py`: implementazione score cal thr.

- `studio2/fase03/soglie_normal/tests/test_generation_plan.py`: controllo di piano o impronte R2.

- `studio2/fase03/soglie_normal/tests/test_generation_plan_stdlib.py`: controllo di piano o impronte R2.

- `studio2/fase03/soglie_normal/tests/test_r2_guard_recheck.py`: controllo di piano o impronte R2.

- `studio2/fase03/soglie_normal/verify_smoke.py`: implementazione verify smoke.
