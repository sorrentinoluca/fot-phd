OK — candidato offline aae29a908356e4a4842a214fdc3db9bff26ec3ca, tree 4e1f7f043725d64fb16b7d1c921c619bce8d1bb3. D04 chiuso nelle riproduzioni e nelle ulteriori prove eseguite. Nessun freeze o GO.

# Verbale autonomo D04 — 15 settembre 2026

## Identità, isolamento e indipendenza

| Oggetto | Identità verificata |
| --- | --- |
| Tecnico eseguito | `aae29a908356e4a4842a214fdc3db9bff26ec3ca` |
| Tree tecnico | `4e1f7f043725d64fb16b7d1c921c619bce8d1bb3` |
| Parent contratto/test-first | `bf7774f2d153ecc50f27ba095f77b612933b4d26` |
| Acquisizione separata | `f0dca4d2d46a290d2ffeb1840abd46eb7664f0ae` |
| Base documentale | `97868f9d6ef281c2dd4ab1c6ffb67e2477ee5715` |
| Successore documentale escluso dall'esecuzione | `feaf1d3c56ff142e1d1b4bc4dd243348c20bcb98` |
| Tree documentale | `0fa64bfaa7b462c01adf75a5c1c45e11e1745201` |
| Respinto usato nel differenziale | `23859a29225ccd9cd6f47e4a0b6e36258831dbab`, tree `fe66025f4925e27676b0be16428475e3fcaee060` |
| Main GitHub effettivo prima/dopo | `a00605862f627710347bd63c49f79a6d0a00135f` |

✅ Prima delle scritture controllati repository, branch, HEAD/tree/parent, status, worktree e `git ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main`. Source `/Users/luker/fot-tep-harness-0310-d04`, branch `codex/studio2-harness-0310-d04`, pulito sul successore. Quest'ultimo aggiunge soltanto quattro documenti di consegna, acquisiti via git show; non è stato eseguito al posto del tecnico.

Review in `/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate`, clone detached con worktree, indice e riferimenti separati; oggetti Git locali condivisi in lettura. Output esclusivamente nel fratello `/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence`. Le prove usano nuove fixture e temporanei sacrificabili: nessuna modifica al candidato, alla principale, ai source o alle prove precedenti, nessun commit/tag/push/integrazione.

| Esecutore | Runtime osservato |
| --- | --- |
| Revisore, questa finestra | sessione `01a0a1ec-35a4-7870-9c39-9bf922d36c85`; `gpt-6-astra`; effort `high` |
| Preparatrice | sessione distinta `01a0a204-abda-7a00-8466-f52f5bc84812`; `gpt-6-astra`; effort `xhigh` |
| Test | `/opt/anaconda3/bin/python3`, Python 3.13.9, arm64, SQLite 3.51.0 |

Fonte: session_meta/turn_context dei rollout locali riletti in [runtime.json](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/runtime.json). L'effort è il valore registrato, non una misura del calcolo consumato. **Finestra distinta, stesso modello**: diversità di modello assente e non rivendicata. Nessuna delega, nessuna attribuzione causale dei difetti alla famiglia del modello, nessuna promessa che cambiarla elimini difetti.

MAINTENANCE principale e candidato, già letti integralmente e applicati nei precedenti cicli, sono stati nuovamente improntati: SHA-256 `4a75b0677c5eb09d36274cb36be37a1ec73afb2ca86b274cc36193812465647b` e `77b4768c2b6ae1bc27d2e1aaaa56f9c38626add20b2f5e74f6a426eef7a66ec0`, invariati. Applicate le regole pertinenti Prompt_LLM/Verifica_LLM. Letti mandato/report D04, entrambi i verbali acquisiti integralmente, contratto iniziale, delta del contratto corrente rispetto al D03 già letto, codice runtime, test, inventari e generatore. Nessun AGENTS.md nel nuovo perimetro. Fonti a commit esatto, senza incorporare lavori paralleli. Letture pertinenti dell'ordine di alcune centinaia di kB, oltre ai confronti meccanici; nessun nuovo audit scientifico o bibliografico.

## Provenienza e perimetro

✅ [integrity.json](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/integrity.json): **9.209 confronti**, zero mismatch. Sono confronti anche ripetuti, non metodi di test aggiuntivi.

| Oggetto | Verifica autonoma |
| --- | --- |
| Manifest tecnico | 98 membri, 24.151 byte, SHA-256 `9fbad8c036075605a9bbdfdac84078259428b679fc33341ed98f21050a07efd6`; file reali e blob HEAD confrontati |
| Acquisizione Codex | 1.930 file, 133 copie byte-identiche e 1.797 esterni; hash/dimensioni riletti per ogni membro |
| Acquisizione Claude separata | Originale untracked e copia: 13.529 byte, SHA-256 `bc3ee96afb2bd890d0b326ca4965d03c46d241f288a30c5ee1455a0c8ec9a47f` |
| Riproduzioni D04 | 3.850 file: 98 copie byte-identiche e 3.752 esterni, verificati anche tutti i membri del relativo SHA256SUMS |
| Evidence originaria | Riletti 2.754 file, inclusi 1.283 membri della reference evidence-v2 già scaricata e verificata nel primo ciclo |
| R4/baseline/input/piano | 18 membri R4, 17 pin baseline, quattro input e tre fonti piano su blob esatti; tre tag ricontrollati sul remoto effettivo |
| Moduli recuperati | Nove moduli confrontati con fonte `1ac06ebdc92f73d3b630ccca9bf75f413bea170b`; sette adattamenti dichiarati, solo logging_v1.py e sampling.py identici alla fonte |
| Perimetro protetto | 177 file byte-identici alla base documentale; tre metriche qualificate anche identiche alla base pubblicata |
| Sintassi/import | 94 Python live compilati in memoria, zero errori; nessun import diretto phase_b, alberi forensi esclusi |

Verbale Codex acquisito SHA-256 `21e457af023a9a8fae3560f663784c55788408942f8c9e902b3d468764aceef9`, manifest `9334c9c57b159cf14f047d28646544615c99aaf751298753e573f893dbbb86a1`. Non è stata verificata la sola presenza di hash: riletti originali, copie e coordinate esterne prima delle prove e al termine. Il verbale Claude originale nel source D03 è rimasto untracked e intatto. I suoi log scratch non sono disponibili qui: le sue esecuzioni sono dichiarazioni del verbale, non nuovi risultati osservati da questa finestra.

Claude dà OK sul nucleo del vecchio D03 con suite parzialmente bloccate nell'ambiente Linux; Codex conferma quel nucleo e rileva D04 dopo esecuzione completa su macOS. I due perimetri non si sommano; i metodi env-bloccati non diventano PASS. Le prove del nuovo candidato sono state eseguite qui, senza quei blocchi di riferimenti esterni. L'identità del backend Claude non viene dedotta dalla sua configurazione dichiarata.

R4 rimane al target `3c64390bc4dd58c48cc4e1e388a38989b32b3143`, manifest `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`; piano rev.10 `6aaa5b3eebfed4ba502c25c0443caabd0051af21`. Pin baseline rev005, Normal e 03.7 conservati. Nessuna provenienza ipotizzata o fonte sostituita con il lavoro corrente di altre finestre.

✅ Test-first verificato sui blob `bf7774f…`: contratto, inventario, test e rosso precedono il runtime nella storia Git; ledger allora identico al respinto, SHA-256 `2dd95090eafd1e1d0395c45205ff66c5dcaf6f563d11de4862711bf229bf4add`. Il test finale **è identico** al test-first, SHA-256 `fbf9bc637f3922425b718620c9f60c2a1c6f4114f8115bf9c7348d538cba725e`. Stesso file usato su entrambi i codici, senza copiarlo nel respinto. test_first_final.diff è vuoto.

✅ Acquisizione: 139 percorsi; test-first: sei; commit tecnico: 107, delta dopo acquisizione: 113. **Solo ledger.py è runtime modificato, +18/−3**. Tre metriche, producer/consumer, gate_rules, test D01/D02/D03, docs/walkthrough, phase_b, code, icl/ablation, piano, pseudolabel, schema, baseline, soglie Normal, APERTURA, preflight e inventario pending preservati. Nessuna rigenerazione di input o risultati scientifici. Le tre failure intermedie della preparatrice sulla precedenza diagnostica sono conservate; nei byte finali hard stop e prerequisiti vengono rifiutati prima dell'inventario, che rimane obbligatorio prima di ogni nuova autorizzazione.

## Risultati autonomi

| Prova | Esito osservato | Evidenza |
| --- | --- | --- |
| Mirati completi | ✅ 128/128, zero failure/errori | [targeted.log](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/targeted.log) |
| Discovery completa | ✅ 163/163, zero failure/errori | [discovery.log](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/discovery.log) |
| Stesso D04 sul respinto | Otto metodi, 240 assertion fallite in sei metodi, zero errori | red_contract.json/log |
| Stesso D04 sul corretto | ✅ 8/8 | green_contract.json/log |
| V01–V06 byte-identici | ✅ 6/6, inclusi i precedenti V05/V06 | v_original/evidence/independent_d03_probes.json/log |
| W/Y/Z byte-identici | ✅ 4/4, 7/7, 5/5 | w_original, y_original, z_original/evidence |
| Originali applicabili | ✅ 14/14, dodici letterali e N20/N21 sola fixture/argomento | applicable/applicable.json/log |
| X01–X18 letterali | ✅ 18/18 | literal/evidence/extended.json/log |
| X19–X24 letterali | Cinque PASS, sola failure X23 obsoleta, zero errori | literal/evidence/additional_edges |
| X23 già adattato | ✅ 1/1 | x23_adapted/evidence/additional_edges |
| Nuove U01–U05 indipendenti | ✅ 5/5, zero failure/errori | [decision_edge_probes.json](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/decision_edge_probes.json) e log omonimo |
| Guardiano documentale | **NON PASS**: 35 test, stessi 14 identificativi falliti, un skip, zero errori; non bloccante | documentation.log e documentation_comparison.json |

Sette D01, otto D02, nove D03 e otto D04 sono già inclusi nelle suite complete. Non si sommano suite sovrapposte, sottocasi, coordinate o processi. Le 240 assertion rosse non sono 240 difetti. Gli script storici possono terminare exit zero con assertion fallite: sono stati letti JSON e log. Nessun errore di setup nelle nuove esecuzioni.

X23 letterale resta visibile come failure perché pretende l'interruzione C02 difettosa del vecchio codice. L'adattamento già verificato conserva TimeoutError e richiede 120 INVALID, T3/T6 falliti, 40 triplette non valutabili, dati ignoti null, riconciliazione immutabile e nessun reinvio. **23 letterali più X23 già adattato**, non 24/24 del file immutato. Nessuna nuova assertion adattata.

[MATRICE_50_METODI.md](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/MATRICE_50_METODI.md), JSON omonimo: 50 nomi, fonti/riga, corrispondenze correnti, log di prove passate e motivazioni di adattamenti/accorpamenti. Dodici letterali, due sola fixture/argomento, 35 adattati/accorpati e N48 equivalente a C02 nella nuova API. Nessuna esclusione implicita o 50/50 letterali. I falsi verdi storici N22–24/N41 non sono usati; le nuove fixture raggiungono il controllo con prerequisiti completi. [MATRICE_ESTENSIONI.md](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/MATRICE_ESTENSIONI.md) distingue X/Y/Z/W/V/U.

## D04: codice, prove negative e chiusura

✅ [ledger.py:98](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:98) rilegge tutte le righe, raggruppa ogni stadio contribuente e riusa **l'intero `_validate_attempts`**, confrontando binding, identità, ruolo, catena e prove. Non introduce una seconda lista parziale, non pretende outcome/PASS o completezza negli stadi aperti. Gli altri stadi sono inclusi: il controllo non riguarda soltanto la foglia scelta.

✅ [Binding:152](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:152), nuovo e ripreso, e [riserva:290](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate/studio2/fase03/harness/ledger.py:290) verificano l'inventario nella transazione della decisione. Base, remediation, retry e triplette convergono su questa riserva prima della nuova riga. Il binding del runner precede client/server. I rifiuti preliminari hard stop/prerequisiti restano legittimi e non autorizzano alcun lavoro.

✅ **V05/V06 originali:** un solo quota_kind di un retry da transport a base, prove/digest intatti. Binding, ottavo retry e producer dopo restart ora restituiscono `persisted attempt quota differs from its role`, prima dell'invio. **Otto intenti, sette archi retry_of, zero nuovi invii, nessun waiver, database logico invariato dopo il fault.** Il confronto rosso resta nel verbale acquisito, senza riscriverlo.

Lo snapshot mostra ancora **sei transport_calls** perché legge il campo SQL deliberatamente alterato. È una lettura diagnostica, non una certificazione o una riparazione del database. Non viene usato per autorizzare il retry: la discordanza è rifiutata. U05 sostituisce snapshot con un errore se invocato nel percorso di autorizzazione verificato; il rifiuto preventivo resta corretto.

✅ **Runner/CLI:** due ingressi D04 con client non costruito, `server_mock.assert_not_called()`, zero invii, output e database invariati. U05 chiama execute_request su una nuova richiesta **senza rebind preventivo**, con contributore di altro stadio corrotto: rifiuto nella riserva prima di trasporto/journal. Non si confonde il timeout successivo a un invio con il rifiuto preventivo richiesto.

✅ **Matrice D04:** 216 coordinate = nove combinazioni stadio/ruolo × quattro stati × due ingressi × tre valori quota errati; 72 positivi precedenti e 14 dipendenze del ruolo. Tutte le coordinate candidate sono riprodotte. La [matrice rigenerata](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/generated_decisions/MATRICE_D04_DECISIONI.json) usa i miei JSON rosso/verde: coincide byte per byte in JSON e Markdown con quella consegnata, confronto in decision_matrix_comparison.json. Il file di test è immutato rispetto al test-first.

✅ **Lock e guasti successivi:** prova D04 con scrittore reale, nuovo fault nella stessa istanza e dopo restart. U01 estende il controllo a sei ingressi: binding nuovo/ripreso, base, retry, remediation e tripletta; validatore chiamato in transazione, writer di altro processo bloccato durante e libero dopo. U04 verifica anche stadio ignoto, parent mancante e prova mancante in un **altro stadio aperto**, dopo un precedente successo, prima/dopo restart: tutti rifiutati, database invariato.

✅ **Concorrenza al limite:** U03 parte da 14 trasporti leciti con rinuncia, distribuiti fra primario e alternativo. Due processi sincronizzati competono per l'ultimo posto: un solo retry autorizzato, l'altro rifiutato, **15 trasporti e 17 intenti complessivi**, nessun sedicesimo trasporto. Il test D04 conserva la rinuncia lecita fino a 15 e rifiuta il sedicesimo; la sonda non supera sette neppure con rinuncia.

✅ **Atomicità:** test D04 rifiuta la tripletta con quota corrotta, preserva il retry lecito e rifiuta la successiva tripletta oltre quota senza consumo parziale. U02 inietta un HarnessError **dopo la seconda inserzione**, verifica rollback integrale anche dopo riapertura del ledger e successiva tripletta lecita: tre trasporti, 14 intenti. Nessuna prova modifica il candidato o i dati scientifici.

Nessun rilievo D04 residuo riprodotto. Non viene attribuita autenticità a un dump SQL manomesso, né richiesta resistenza a chi riscriva coerentemente l'intera catena e tutte le impronte. I fault iniettati non dimostrano guasti spontanei; gli invii osservati sono soltanto quelli degli stub. La verifica riguarda questi byte e questi ingressi, non una futura implementazione.

## Regressioni e matrice requisito → codice → prova

| Requisito | Codice pertinente | Prova e riscontro |
| --- | --- | --- |
| R01 | guards.py:93, ledger.py:257 | ✅ R01, X17, Y05: preflight storico UNDECIDED/SUSPENDED rifiutato, nessun default eseguibile |
| R02 | inputs.py:155, preparation.py:11 | ✅ N30–33/36–38/41/47/49, R02, X12/X14/X17, Z: pin/input/handoff/libreria e raw producer autenticati |
| R03 | inputs.py:230, protocol.py | ✅ N34/35/39, R03, X17: label evaluator-side separata dall'ordine presentato; ordine reale ancora non approvato |
| R04 / D01 / D02 | ledger.py:225, 643 | ✅ Y/Z e suite D01/D02: prerequisiti storici, copertura/order, raw/record, outcome/freeze; rifiuti senza scritture o invii |
| R05 / D04 | ledger.py:98, 290, 610 | ✅ V05/V06, D04 8/8, U01–U05, N11–17/R05/X06–09/X19/X21: quote prima delle decisioni, tutti i contributori, rollback e concorrenza |
| R06 | ledger.py:719, producer_probe.py | ✅ R06, X10/X20/X24, remediation D01/D02: diagnosi/diff/template concreti e libreria completa, nessuna seconda remediation |
| R07 / C02 / C03 / D03 | runtime.py:41, producer_probe.py:181, ledger.py:509 | ✅ W 4/4, V01–V04, D03 9/9, C02/C03: prove zero-token, crash/ripresa, denominatori e contatori preservati |
| R08 | ledger.py:712 | ✅ R08, X18, Z01/Z02/Z04, D02: freeze/sonda/predecessori autenticati nella stessa transazione |
| R09 | guards.py:107, ledger.py:494 | ✅ R09, X13/X22, Y03/Y05: raw/consumo conservati, identità errata sospende, INVALID non maschera risposte |
| R10 | gate_rules.py:51 | ✅ N20–24, GateRevisions, X11, C02, Z05: 40×3, 120 ID, ripetizioni/ruoli/agenti/condizioni corretti, nessun retry gate |

Le corrispondenze nominative, i percorsi completi e i log sono nelle matrici estese. I rilievi R01–R10 e i successivi C01–C03/D01–D04 sono chiusi **nel perimetro dei casi verificati sul candidato corrente**, senza retrodatare OK ai candidati respinti.

✅ D03 resta invariato: validatore condiviso nei tre percorsi e undici controlli effettivi, digest ricalcolabili distinti dagli hash dei file, legame durevole, lettura singola dei byte, niente backfill. Le nove prove D03 e W sono rieseguite. V01 conserva atomicità dei due eventi e del cambio stato con morte reale prima/dopo commit; V02 verifica i byte letti una volta; V03 mantiene l'INVALID del FAILED poi riconciliato, senza inventare una risposta; V04 rifiuta una prova alterata nel producer aperto prima del client.

✅ D01/D02: catene legacy generate dal codice esatto/pulito 0c8157f in subprocess, senza SQL che fabbrichi la precedenza. Catene senza prove legacy prive di digest restano positive; quelle con tali prove sono rifiutate secondo il requisito storico autorizzato, 132 intenti invariati e nessun backfill. Alternativo irrisolto o raw/copertura dei predecessori corrotti bloccano riconferma/runner/CLI prima del server e delle proiezioni; 139 intenti conservati nei relativi casi. Sonda rematerializzata dopo gate e summary mancante rigenerato identico non riaprono richieste.

✅ C02/C03 e metriche: 120 primi tentativi includono INVALID, non risposte inventate. Un timeout produce 119/120 e tripletta divergente; invalidità concentrate/distribuite mantengono i criteri T3/T6 del piano; tutte invalide conservano FAIL, nessuna promozione a PASS. Nessun retry gate. Nove richieste provider/ledger/summary distinte da otto coppie T9/16 insight; multi-hop dieci intenti/otto coppie e alternativo 17 cumulativi preservati. Tre metriche qualificate intatte e nove test di raccordo passati. Non sono insight o risultati scientifici reali.

## Limiti e consegna

La matrice è finita: non prova ogni valore, guasto combinato, interleaving o futura API. Il guardiano D04 confronta STAGES, ruoli e i quattro stati censiti; le dipendenze sono verificate contro l'inventario N/F. La guardia D03 segnala nuove colonne/chiavi nominate, mentre i payload opachi improntati ereditano N. Le 69 voci D03 restano 56 con mutazioni e 13 con collegamenti storici; non sono 69 nuove mutazioni individuali in questo ciclo. La classificazione non sostituisce prove specifiche per nuovi stati o percorsi futuri. Questi limiti non vengono trasformati in garanzie di esaustività.

Le fixture dipendono da riferimenti locali macOS: sono tutti raggiunti e verificati qui, ma non si dichiara portabilità automatica a VM prive di quei percorsi. I log scratch Claude non sono stati acquisiti; non sono necessari come sostituti delle esecuzioni correnti. Guardiano documentale ancora NON PASS, stesso perimetro storico e stessi 14 identificativi, non bloccante per il delta offline.

**OK limitato al candidato tecnico esatto.** Nessun difetto residuo riscontrato nelle prove e nel codice esaminati. [Stato Git finale](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/final_git_state.json): candidato detached pulito; quattordici repository osservati preservati. Principale con HEAD `819b12e97fb94d501032655ec2f226139e6c5ca5`, branch codex/studio2-soglie-normal e untracked preesistenti; verbale Claude untracked nel source D03 conservato per hash. Nessun commit/tag/push/merge/integrazione, modifica al walkthrough, provider API, inferenza o simulazione scientifica. Rete usata soltanto per le letture Git richieste.

D9 è già approvata: **122B producer principale e consumer, 27B alternativo per una libreria completa di 16 insight, Terra storico descrittivo interno**. La vecchia proposta Terra è superata, nessuna nuova decisione sui ruoli richiesta. Restano distinti recepimento eseguibile D9, ordine label 1a ancora non approvato, insight reali, qualificazioni servizi/tokenizer/identità/capienza, T5 e autorizzazione pilot. Preflight storico bloccato. Nessun trasferimento dell'OK ai futuri byte D9, nessun freeze o GO; 03.10 e Fase 03 non sono chiuse da questo verbale.

[COMANDI.md](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/COMANDI.md), [inventario](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/EVIDENCE_INVENTORY.json), [SHA256SUMS](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/SHA256SUMS). File regolari e symlink distinti, nessun attraversamento dei symlink o autoreferenza. Hash del verbale e manifest comunicati esternamente. Fixture catturate con riferimenti ai temporanei originari preservati; per riprodurre creare nuove directory, mai sovrascrivere prove conservate.
