# Verifica indipendente D02 — candidato tecnico esatto

Incarico di **review in altra finestra**, preferibilmente altro modello. Sola lettura:
nessuna correzione, commit, tag, push, merge, freeze o GO. Non ereditare il giudizio della
preparazione. Scrivi un nuovo verbale autonomo con modello/finestra osservati e limiti.

## Oggetto e identità

- Source: `/Users/luker/fot-tep-harness-0310-d02`.
- Branch: `codex/studio2-harness-0310-d02`.
- **Candidato tecnico: `a219bd469bbd280f56b7fa9cb56cda115b0975ed`.**
- **Tree: `3fb8e50c189b85b447503b8a1ac99c1741904a5b`.**
- Base documentale: `7afbf41632aa8117c85274b5f471abca0a655462`.
- Acquisizione separata: `5b45cdcabe40aa64b0aecd1b5fe9d09c92ce5bb4`.
- Manifest: 17729 byte, 70 membri; SHA-256 `fb8474c6e71d63fbb54b83d46e63ae4238a7fb4b20d6c988866e27085d8db9a9`.
- Report: [REPORT_CORREZIONE_D02.md](REPORT_CORREZIONE_D02.md).

Il source potrà avere un HEAD documentale successivo: controllane parent e diff, poi crea
un clone/worktree di review detached sul tecnico esatto. Acquisisci i quattro file di
consegna via git show dal successore, senza sostituire il candidato tecnico. Non eseguire
prove in source, principale, review precedenti o directory evidence già popolate.
Prima delle scritture registra repository, HEAD/tree, branch, status, worktree e remoto
GitHub effettivo. Main osservato dalla preparazione: a00605862f627710347bd63c49f79a6d0a00135f.

## Fonti e provenienza

Leggi MAINTENANCE e prompt pertinenti; il report è oggetto della verifica, non prova.
Acquisisci [VERIFICA_D01.md](non_ok_edb37f3_20260915/files/VERIFICA_D01.md) integralmente:
SHA-256 `2806ce5c15d51c917e3e19cc77a935c37ffe09134b485fa257401f6b85ad2fd6`.
Manifest originale SHA-256 `dceb4ae6bd4c177002c0bbc1c942333590f114218d1499ebab0ae6475459dffd`.
Verifica inventari e membri su disco, non solo la presenza degli hash: 1.822 file acquisiti,
100 copie e 1.722 esterni. Verifica manifest tecnico e riproduzioni incluse/esterne.
Fixture SQL alterate rigorosamente separate da input scientifici; D01 legacy resta
costruito dal vecchio codice 0c8157f in subprocess, senza SQL che fabbrichi la precedenza.

## Requisito centrale D02

La review precedente chiude D01 originario ma rileva che `_successful` accetta predecessori
PASS/COMPLETED con raw corrotti o copertura incompleta. Controlla la correzione nel codice
e nei percorsi ordinari, senza limitarti ai helper invocati dalle prove.

1. Verifica Z01/Z02: dopo un positivo, corrompi separatamente raw primario/alternativo/sonda
o rimuovi una richiesta. Binding identico, successo gate, replay outcome e freeze devono
rifiutare la catena con HarnessError, mantenendo database logico e raw/storia disponibili.
2. Riproduci Z03 sul runner ordinario con alternativo completo, sonda/gate chiusi, poi raw
alternativo corrotto: --resume deve rifiutare prima di invii e output, conservando 139 intenti.
3. Verifica il validatore condiviso: copertura/order, identità, catene complete di retry,
raw/record/digest dell’artefatto e dell’evento, sonda e freeze persistiti. Prova anche perdita
di response/record, riduzione 9→6, record alterato con solo hash locale ricalcolato, producer
attivo in remediation e riconferma del proprio binding già chiuso.
4. Verifica Z04 e regressione D02 del lock con processi realmente concorrenti durante i
record dei predecessori. Una connessione e una transazione per tutta la conferma; nessun
controllo con stato già obsoleto, scrittura parziale o cache riutilizzata dopo nuovi fault.
5. Conserva i positivi: catene legacy valide con/ senza alternativo; sonda rimaterializzata
dopo gate; summary mancante rigenerato identico; retry producer nove intenti/otto coppie;
remediation valida; gate C02 con INVALID e replay FAIL Z05 senza promozione a PASS.
6. Controlla gli ingressi nuovi e CLI budget/stability --resume, zero chiamate stub/server
e byte invariati in caso di rifiuto. Lettura forense non equivale a conferma normativa.
7. Approfondisci altri guasti pertinenti; non rivendicare resistenza contro un attore che
riscrive coerentemente l’intero database e tutte le impronte. Distingui guasto iniettato,
perdita spontanea, reinvio e GO: non inferire gli ultimi tre dalle prove attuali.

## Suite e conteggi da verificare

Usa Python compatibile `/opt/anaconda3/bin/python3`, `PYTHONDONTWRITEBYTECODE=1`.
Comandi completi in [d02_evidence/COMANDI.md](d02_evidence/COMANDI.md).

- Mirati dichiarati **111/111**; discovery **146/146**, inclusi gli otto D02 e sette D01.
- Applicabili **14/14**, 12 letterali e due precedenti adattamenti fixture/argomento.
- **Z01–Z05 5/5**, script byte-identico; respinto tre failure/zero errori.
- **Y01–Y07 7/7** senza adattamenti.
- X: **23 letterali + X23 già adattato**. Preserva e spiega la sola failure X23 letterale
obsoleta; nessun nuovo adattamento di assertion. Per X23 copia anche extended_probes.py.
- Guardiano: **NON PASS**, 35 test, stessi 14 identificativi falliti e 1 skip, zero errori.
- Mantieni una matrice esplicita dei **50 metodi**, con corrispondenze e motivazioni degli
accorpamenti, equivalenza N48 al requisito C02 e assenza di 50/50 letterali impliciti.

Gli script esterni possono terminare exit 0 con assertion fallite: leggi JSON e log.
Il preliminare d02.log contiene 29 metodi (otto nuovi + 21 fixture importate): l’import è
corretto nelle suite finali. L’errore iniziale X23 è di setup, conservato e poi risolto con
copia byte-identica del modulo mancante. Non contarli come difetti o prove aggiuntive.
Suite sovrapposte e sottocasi non si sommano.

## Confini e consegna

Verifica diff e metriche qualificate intatte. D9 approvata: 122B principale/consumer, 27B
alternativo completo, Terra storico interno. Nessuna nuova decisione sui ruoli. Esecuzione
D9, ordine label reale, servizi/tokenizer/identità/capienza/T5 e pilot restano separati.
Storico preflight bloccato; nessuna chiamata API/inferenza/simulazione scientifica.
Preserva principale, source e precedenti review; nessun walkthrough/piano/APERTURA/freeze.

Produci verbale autonomo OK o NON OK **sul tecnico esatto**, prove/log e SHA256SUMS senza
autoreferenza, matrice dei 50 metodi e stato Git finale. Dichiara modello/finestra/effort
osservati; preparatore gpt-6-astra/xhigh, revisore precedente stessa famiglia/high in altra
finestra. Se il modello coincide, esplicita il limite. Nessun freeze o GO.
