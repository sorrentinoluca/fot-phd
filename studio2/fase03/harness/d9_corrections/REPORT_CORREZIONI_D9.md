# Correzioni R-D9-01 e R-D9-02 — candidato offline

15 settembre 2026. Preparatore: Codex in questa finestra; non è il revisore
indipendente. Il mandato corrente autorizza acquisizione della review, correzione
e prove rosso/verde, poi consegna alla stessa finestra revisore. Non autorizza
servizi, inferenze scientifiche, nuove decisioni D9, ledger operativi o pubblicazione.

## Problema e comportamento risultante

R-D9-01: `" PENDING "` veniva accettato come revisione documentata. `_text` ora
confronta i sentinel dopo `strip().upper()`, lasciando intatti i byte del documento.
Il rifiuto resta prima di client, riserva e invio. Sono rifiutati anche tab/newline,
NBSP e maiuscole/minuscole dei sentinel già previsti; valori reali restano ammessi.

R-D9-02: una perdita dei file tokenizer dopo la preparazione poteva lasciare
ammissibile una nuova riserva diretta e il trasporto. Il controllo comune
`validate_binding` ora richiama `verify_tokenizer` per R4 e per la chat del ruolo,
alle decisioni di binding/riserva/riuso nelle transazioni già esistenti. I runner
producer e consumer conservano nel binding il percorso assoluto della chat,
`tokenizer_snapshot`, distinto dal `r4_snapshot` canonico. Il controllo comprende
revisione, tokenizer.json, tokenizer_config.json e template effettivo, secondo
il validatore condiviso: il fallback al template inline già pinnato resta valido.

Non è una copia durevole alternativa: si sceglie la riconferma dei file recuperabili
prima della decisione. Un vecchio binding D9 senza il nuovo riferimento viene
rifiutato, senza migrazione/backfill o azzeramento. Il ledger generico offline senza
execution_config conserva il perimetro storico. Il difetto diretto esisteva già
prima di D9, come documentato dal revisore: non è rinominato regressione D04.

## Acquisizione e conservazione

Respinto tecnico: `6a8031b25aa1208047d79cc7f030bf9cf7841e67`, tree
`bb3872d8fc1cbddebb4b055a8edad372e5aad430`. Base documentale del lavoro:
`08670fb4793ecec99754a73c6a91a51c1c372960`.

[Verbale originale NON OK](non_ok_6a8031b/VERIFICA_D9.md), 18.659 byte,
SHA-256 `9e1de541cdebef75eac560aa9eb6261db3da5e3f04484e9fee006dd748e65b45`.
[Manifest originale](non_ok_6a8031b/MANIFEST.json), SHA-256
`269bfc69e1d1028b4466768d801d21bbf6e31b96266434ce53f16f9e03d0b435`.
Provenienza, percorsi e limiti: [acquisizione](ACQUISIZIONE_NON_OK.json).

Acquisiti e verificati byte-identici tutti i 591 membri del manifest, oltre ai
file originali MANIFEST/CONSEGNA. Il verbale, gli script finali/intermedi, log,
fixture e database di prova sono conservati. Le fixture rimangono intenzionalmente
fittizie o corrotte, esterne agli input scientifici. Non si eseguono i programmi
di raccolta/finalizzazione della review, che potrebbero riscrivere le prove.

L'archivio candidato di 244.633.206 byte è conservato byte-identico nella copia
locale acquisita e nella sede originale, escluso esplicitamente da Git per la
dimensione; percorso e hash sono nell'acquisizione. Tutti gli altri membri sono
committati. Il candidato è anche recuperabile dal commit Git esatto. Questo non
è pubblicazione dei dati: la recuperabilità finale remota richiederà il passo
seriale autorizzato di conservazione; nessun upload viene dichiarato qui.

Le impronte dimostrano integrità locale rispetto ai byte ricevuti, non una firma
crittografica del revisore o una certificazione dei servizi. Il NON OK originale
resta riferito al tecnico respinto; nessun OK D04 è trasferito ai nuovi byte.

## Catena delle prove

Il contratto è in [CONTRATTO_CORREZIONI_D9.md](CONTRATTO_CORREZIONI_D9.md).
`test_d9_corrections.py` è stato introdotto prima del runtime. La prima versione
provava impropriamente la perdita di chat_template.jinja senza tener conto del
fallback inline: errore della fixture, registrato in corrections_red.log e nella
storia Git. La versione successiva separa il positivo inline dalla corruzione.
Il primo verde aveva quattro sole divergenze della regex diagnostica
(`chat template` rispetto a `chat_template.jinja`): codice di rifiuto già corretto.
La regex finale ammette entrambe le diagnostiche del validatore, non un errore
arbitrario. Tutti gli stessi test finali sono stati rieseguiti su respinto e corretto.
I log intermedi sono conservati e non sostituiscono gli esiti finali.

Il rosso usa il worktree originale al successore documentale 08670fb, verificato
pulito e senza differenze Python rispetto al tecnico 6a8031b: i cinque file aggiunti
sono solo consegna/prompt/report/controlli documentali. Il controllo dei byte è
ripetuto nella consegna; questo limite d'identificazione è esplicito.

Gli originali U01–U08 del revisore sono rieseguiti **senza modificarli**, selezionando
il target con FOT_D9_TARGET e nuove destinazioni assolute per le fixture tramite
PROBE_OUTPUT; nessun output della review originale è sovrascritto.
`transport_boundary_regression.py` è una prova nuova, dichiarata come adattamento
concettuale del probe di trasporto originale: usa `_tracked_call → execute_request
→ Provider` reali con SDK fittizio, positivo intatto e perdita distinta di R4/chat.
Il suo codice finale è identico sui due runtime; non si presenta come esecuzione
letterale dello script originale senza assertion preventive.

| Prova finale | Metodi | Assertion fallite | Errori | Esito |
| --- | ---: | ---: | ---: | --- |
| Correzioni sul respinto | 11 | 32 | 0 | Rosso discriminante; subtest non sommati ai metodi |
| Stessi test sul corretto | 11 | 0 | 0 | Verde |
| U01–U08 originali sul respinto | 8 | 3 | 0 | Rosso sui rilievi originali |
| Stesse U01–U08 sul corretto | 8 | 0 | 0 | Verde |
| Adattatore reale / SDK fittizio sul respinto | 3 | 2 | 0 | Rosso sui due snapshot distinti |
| Stesso test di trasporto sul corretto | 3 | 0 | 0 | Verde |
| Suite mirata completa | 156 | 0 | 0 | OK, zero skip |
| Discovery completa | 191 | 0 | 0 | OK, zero skip |
| Guardiano prima/dopo | 35 | 14 | 0 | NON PASS storico; 1 skip, stessi identificativi/subtest |

Risultati e tempi misurati in [SUMMARY.json](results/SUMMARY.json), hash dei test
nei record rosso/verde sotto `results/`. I 425 Python tracciati inventariati
all'avvio coincidono con i byte finali: è un inventario di integrità, non la
rivendicazione che tutti siano stati eseguiti. L'ambiente effettivo è in
[TESTED_BYTES.json](results/TESTED_BYTES.json).
Le suite mirata e discovery sono complete e sovrapposte: non sommare i metodi.
La compilazione in memoria è un controllo aggiuntivo, non esecuzione scientifica.
I contatori e gli SDK sono fixture; i test dei runner vietano socket. Le dipendenze
legacy dei test restano quelle dichiarate dalla precedente consegna e non vengono
riscritte. Nessuna assertion storica è modificata.

## Rischi e residui

La riconferma riguarda i byte letti al confine della decisione. Non introduce lock
sul filesystem esterno né prova l'impossibilità di modifiche dopo quel controllo.
Il riuso non si basa su una cache di validazione. Il maggior costo di lettura/hash
locale non è una misura di latenza del servizio né una valutazione T5.

Rimangono invariati e pendenti metadati reali, qualifiche, ordine label 1a,
collocazione dell'alternativo, riconciliazione S 4/3, autorizzazione delle configurazioni
e chiamate. P=C=122B, P_alt=27B completo 16, consumer fisso nello swap, Terra storico
interno; temperature 122B omessa. Nessuna modifica a schema, quote, casi, A/B, FAR,
U3, piano statistico, configurazioni pending canoniche, paper o walkthrough.

Il candidato deve ricevere nuova review dalla finestra
`01a0a579-3fd7-7461-8c26-5449bd3d2b7a` — «Review indipendente D9 — candidato 6a8031b».
Questa consegna documenta le prove del preparatore; non emette l'OK indipendente,
GO, freeze o chiusura 03.10.


## Controlli di consegna

Manifest del candidato con byte/SHA-256; originali della review ricontrollati
contro sorgente e copia. Worktree originali D9, D04 e metadati puliti e invariati.
Main remoto effettivo ancora `a00605862f627710347bd63c49f79a6d0a00135f`.
`git diff --cached --check` sul delta intero segnala spazi nei log grezzi e nelle
fixture deliberatamente corrotte, conservati senza normalizzarli. Il controllo
limitato a sorgenti Python e documenti Markdown passa senza rilievi. Dettagli in
[diff_checks.json](results/diff_checks.json). Non si descrive il controllo integrale
come PASS. Nessun controllo documentale è una qualifica sperimentale.
