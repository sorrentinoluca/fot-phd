# Acquisizione NON OK + ACCEPT — accounting 122B 03.13

Data di acquisizione: 2026-09-16.

## Oggetto e genealogia

Si acquisisce il verdetto indipendente **ACCEPT** sul candidato tecnico
`38db018ad6fac1dd598cc9cde82efa06b27ec06b`, tree
`006317bd775acf3c081fbb08dee0f8cdb295cb7c`. Il suo parent è il candidato respinto
`6431612c632b4c46f87f3edec9d662c572a4996a`, tree
`dfa85151b291b69f800ab90c9c81902460463385`.

La genealogia documentata è quindi:

```text
6431612c632b4c46f87f3edec9d662c572a4996a  NON OK
└─ 38db018ad6fac1dd598cc9cde82efa06b27ec06b  ACCEPT
```

Il commit che introduce questo record è un successore esclusivamente documentale,
identificabile con:

```text
git log --diff-filter=A -- studio2/fase03/harness/ACQUISIZIONE_ACCEPT_ACCOUNTING_122B_03_13.md
```

Non trasferisce l'ACCEPT a byte tecnici futuri e non modifica il candidato accettato.

## Verbali acquisiti byte-identici

| Ruolo | Copia conservata | Byte | SHA-256 |
| --- | --- | ---: | --- |
| NON OK | [VERIFICA_CONFIG_122B_ACCOUNTING_03_13.md](reviews/VERIFICA_CONFIG_122B_ACCOUNTING_03_13.md) | 4.761 | `c7209a3f8c93380422841c648741795a9e03d6851e4e2d9a3597e794bce17052` |
| ACCEPT | [VERBALE_RIVERIFICA_CONFIG_122B_ACCOUNTING_03_13.md](reviews/VERBALE_RIVERIFICA_CONFIG_122B_ACCOUNTING_03_13.md) | 13.891 | `007652fcc26ba2e1ad0cac9ccc303dcfb93a93ddc12279cc488b54fce7813a40` |
| Sidecar ACCEPT | [VERBALE_RIVERIFICA_CONFIG_122B_ACCOUNTING_03_13.md.sha256](reviews/VERBALE_RIVERIFICA_CONFIG_122B_ACCOUNTING_03_13.md.sha256) | 117 | `ce7de698ddcb813d7b222725dd3da4e53ec8a9f9ce0960c64e5c2002cda712f7` |

Gli hash degli originali sono stati verificati contro il mandato prima della copia e
ricalcolati sulle copie. Il sidecar contiene l'hash atteso dell'ACCEPT e la sua verifica
locale restituisce `OK`. I verbali sono conservati senza riscritture, incluse le
formulazioni e le limitazioni dei rispettivi ambienti.

## Chiusura dei quattro blocker

L'ACCEPT limita la chiusura ai quattro rilievi del NON OK e ai byte esatti del candidato:

1. per il modello richiesto esattamente `qwen3.5-122b`, il guard e gli stessi messaggi
   trasmessi sono obbligatori nel punto comune prima di intent, riserva e trasporto, sia
   per producer sia per consumer budget/gate, runner, CLI e chiamata diretta; i modelli
   diversi dal 122B restano compatibili senza guard;
2. raw senza record e record completati vengono riconvalidati prima del riuso su resume,
   retry e restart, senza un nuovo trasporto;
3. l'evidenza lega in modo semanticamente ricalcolabile identità della richiesta,
   messaggi, snapshot, raw e campi consumati dal record, respingendo alterazioni coerenti
   dei soli hash interni;
4. ogni eccezione ordinaria del tokenizer/template produce uno STOP durevole, mentre un
   PASS create-once valido privo del record finale viene rivalidato e completato
   idempotentemente senza collisione né reinvio.

La prova indipendente ha confermato anche che la validazione precede parsing e decisioni,
che `bool` non è accettato come intero dei token e che un errore successivo al trasporto
non viene presentato come prevenzione della chiamata.

## Risultati acquisiti e limiti ambientali

Sul Mac dell'autore, prima del commit tecnico, erano già state eseguite integralmente
con interprete arm64 le regressioni pertinenti: **127/127 PASS** per D01–D04, D9,
D9-corrections, harness offline, riconciliazione storico e revisions; **14/14 PASS**
per C01–C03. Questi risultati appartengono all'ambiente autore e non vengono attribuiti
alla VM della riverifica.

La riverifica VM ha riprodotto sui byte finali i **9/9 PASS** della contabilità sul
successore e il rosso discriminante sul parent (**4 failure e 3 error**, sette prove
discriminanti). Ha inoltre ottenuto **20/20 PASS** per harness offline e **10/10 PASS**
per la riconciliazione dello storico.

Le restanti regressioni nella VM non sono dichiarate PASS: dipendevano da fixture esterne
su percorsi assoluti del Mac, in particolare il manifesto 03.6 non versionato e worktree
legacy assenti. I relativi errori, e la failure a valle della stessa assenza, restano
registrati come limiti ambientali; non sono stati riclassificati, ricostruiti o sommati ai
risultati verdi. Anche il guardian documentale resta **NON PASS**: 35 test, 14 failure
storiche e 1 skip, identici sul successore e sul parent secondo il verbale.

Questa acquisizione non riesegue le suite e non estende le conclusioni oltre quanto
riportato nei due verbali.

## Portata dell'ACCEPT

L'ACCEPT certifica soltanto la chiusura offline dei quattro blocker sui byte del commit
tecnico indicato. Non qualifica il servizio, il tokenizer/template server, l'identità
byte-identica server/client, l'endpoint, il modello effettivamente servito o la capacità.
Non autorizza chat completion, `/models`, `/version`, `/tokenize`, sonda, pilot, gate,
batch, riconciliazione/applicazione dello storico S, freeze o GO operativo.

Per questa acquisizione non sono stati modificati runtime, test, configurazioni, storico S
o rapporti già verificati. Non sono stati usati provider, endpoint o ledger reali e non
sono stati effettuati merge, rebase, push, tag o pubblicazioni.
