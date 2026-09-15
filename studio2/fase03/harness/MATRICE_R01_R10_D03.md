# Matrice del delta D03 — R01–R10

Nuovo candidato locale successivo al NON OK a219bd4. D01/D02 originari e C02/C03 sono
chiusi dal precedente revisore nei percorsi descritti; D03 richiede nuova review indipendente.
Il contratto/test-first è distinto dal commit runtime. Nessun freeze o GO.

| Requisito | Modifica o conservazione | Prove correnti | Limite |
| --- | --- | --- | --- |
| R01 | Binding ripreso controlla anche le prove zero-token dello stadio prima di interrogare il server; blocchi storici conservati | D03 runner/CLI e legacy, W02; test_R01_*, Y05, X17 | Nessuna autorizzazione del preflight storico |
| R02 | Contenuto della prova e approvazione improntati separatamente dai file originali; pin/input/R4 invariati | Matrice D03 digest/involucri; test_R02_*, X12/X14/X17, Z01/Z03 | Non è una qualifica provider o input scientifico |
| R03 | Nessuna variazione a label_space e ordine di presentazione | test_R03_*, X17, applicabili | Ordine label reale separato |
| **R04 / D03** | `_validate_zero_token_evidence` unico nei tre percorsi; due eventi e cambio stato atomici nella stessa transazione | **37 varianti × acquisizione/retry/gate**, guardia degli 11 controlli; W01/W02; D01/D02 e Z04 | Precondizioni di stato distinte; zero reinvii e nessuna riscrittura nella sola conferma |
| R05 | Antenati e nuovo retry validano prova/approvazione/legame. quota_kind deve coincidere con il ruolo originale/remediation/retry | Matrice SQL N/F, W03 multi-hop, D03 legacy/new retry; test_R05_*, X06–09/X19/X21, Y06 | Quote 8r+t≤15, 152/160 e 200 distinte, invariate |
| R06 | Conformità del producer attivo e remediation conservata | test_R06_*, D01/D02 remediation, X10/X20/X24 | Nessuna modifica a diff/template/otto casi o librerie |
| **R07 / D03** | Prove prive di digest/legame rifiutate senza backfill; lettura dei file una sola volta per parsing/hash | D03 legacy reale 0c8157f, assenza digest; W01–W04 e runner/CLI | Sblocco legacy solo tramite riconciliazione revisionata separata; nessuna migrazione automatica |
| R07 / C02 | `_gate_transport_record` verifica la prova quando ZERO_TOKEN_PROVEN, anche dopo un INVALID già esistente; transazione unica pubblica | Terzo percorso della matrice simmetrica, C02, Z05, X23 adattato, Y03–Y06 | INVALID non diventa risposta e il record originario resta immutabile |
| R07 / C03 | Contabilità stadio/pilot e coppie valutabili invariata | test_C03_*, Y07, W02/W03, D02 retry | Nove intenti/otto coppie e dieci nel multi-hop; nessun azzeramento |
| R08 | Riconferma ricorsiva della sonda/freeze comprende le prove degli antenati | W01/W02, Z01/Z02/Z04, D01/D02; test_R08_*, X18 | Il digest frozen non sostituisce quello delle prove zero-token |
| R09 | Contenuto/identità della prova verificato nel validatore comune; raw e guardie risposta invariati | Matrice simmetrica identità, test_R09_*, X13/X22, Y03/Y05 | Nessuna identità remota inventata o qualificata |
| R10 | Criteri gate e triplette invariati; il terzo percorso autentica l’assenza di risposta riconciliata | GateRevisions, C02, X11, Z05, matrice D03 gate | 120 primi tentativi, zero retry gate, nessuna modifica a gate_rules/metriche |

## Inventario e copertura

[DURABLE_FIELD_CONTRACT.json](DURABLE_FIELD_CONTRACT.json) classifica 69 voci strutturali:
33 colonne SQLite, 11 campi di prova/approvazione e 25 voci dei payload degli eventi.
La [matrice generata](MATRICE_D03_CAMPI.md) e il [JSON](MATRICE_D03_CAMPI.json) distinguono
56 voci esercitate con nuove mutazioni e 13 collegate alle prove storiche, senza attribuire
loro mutazioni individuali non eseguite. I contenitori opachi improntati ereditano N per
tutti i discendenti. Il test-guardia scopre nuove colonne e nuovi campi nominati degli eventi,
comprese evidence/approval; default DA_COPRIRE. Classificazione completa dei contenitori
noti non significa esaustività di valori/combinazioni o prova formale dell’intera macchina.

Nove metodi D03, scritti prima del primo runtime e poi rafforzati soltanto nella guardia
sui campi annidati. Entrambe le versioni sono rosse sul respinto e verdi sul corretto;
la versione finale è quella usata nelle suite complete finali. 8 failure/zero errori sul
respinto, 9/9 sul corretto. Le failure non sono otto nuovi rilievi. Le mutazioni SQL hanno
portato anche al controllo quota_kind previsto dal contratto, senza cambiare la quota.

## Storico e requisito cambiato consapevolmente

Le sette regressioni D01 e otto D02 vengono rieseguite integralmente e rimangono invariate.
Le vecchie catene positive D01 non dipendono da una prova zero-token senza digest; nessun
adattamento di quei metodi è necessario. Il cambiamento è coperto da una nuova prova che
usa il vecchio 0c8157f per creare una catena allora valida con retry: ora è respinta e i
132 intenti restano intatti. Non si classifica questo rifiuto come regressione inattesa.

W01–W04, Y01–Y07 e Z01–Z05 sono rieseguiti da script byte-identici. X mantiene 23 letterali
più X23 già adattato; la sola failure letterale obsoleta X23 rimane nel log. Gli applicabili
sono 14, di cui 12 letterali e due precedenti adattamenti di fixture/argomento.
La [matrice nominativa dei 50 metodi](non_ok_a219bd4_20260915/files/MATRICE_50_METODI.md)
e il JSON acquisiti documentano tutte le corrispondenze, inclusa N48 equivalente a C02.
Non si dichiara 50/50 letterali, né si sommano suite e sottocasi sovrapposti.

Risultati e log: [d03_evidence/RESULTS.json](d03_evidence/RESULTS.json).
