# D03 — comandi e provenienza delle verifiche offline

Cwd: `/Users/luker/fot-tep-harness-0310-d03`.
Output: `/Users/luker/fot-tep-harness-0310-d03-checks`.
Python `/opt/anaconda3/bin/python3`; `PYTHONDONTWRITEBYTECODE=1`.
Usare nuove directory sacrificabili per riprodurre: non sovrascrivere le evidence.

## Ordine prima del runtime

1. Verificati principale, source, dieci source/candidati precedenti complessivi, worktree,
   branch, HEAD/tree/status e main sul remoto GitHub effettivo. Snapshot nell’acquisizione.
2. Verificati 70 membri del manifest tecnico precedente e 1.868 membri del manifest review,
   più il suo SHA256SUMS: 1.869 file, 116 copie byte-identiche e 1.753 esterni recuperabili.
3. Commit acquisizione `efa9f6f94194985104047d831c0b087dc460532d`.
4. Inventario e contratto scritti prima del codice; matrice di test eseguita sul respinto.
   Prima versione sette metodi/sei failure; aggiunti gli involucri e la prova legacy reale:
   nove metodi/otto failure/zero errori, runtime ancora identico al blob a219bd4.
5. Commit contratto/test-first `567881abf06572812c00ccc0ed817d169b68fee6`.
   TEST_FIRST.json e i due red_contract originali tracciati rimangono immutati.
6. Correzione del runtime. Prima prova verde nove/nove. Rafforzata poi la sola guardia
   dell’inventario sui nuovi campi nominati annidati in evidence/approval. Versione finale
   rieseguita rossa sul respinto e verde sul nuovo codice; suite complete rilanciate.
   Le esecuzioni precedenti restano in pre_inventory_guard, non sostituiscono quelle finali.

## Matrice simmetrica e test D03

Eseguire il file del nuovo worktree usando esplicitamente il candidato da importare.
Il candidato respinto rimane detached e pulito. Non copiare test dentro la sua directory.

```bash
PYTHONDONTWRITEBYTECODE=1 FOT_HARNESS_TARGET=/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/candidate FOT_D03_OBSERVATIONS=NUOVO_PERCORSO_RED.json /opt/anaconda3/bin/python3 studio2/fase03/harness/test_d03_contract.py
PYTHONDONTWRITEBYTECODE=1 FOT_HARNESS_TARGET=/Users/luker/fot-tep-harness-0310-d03 FOT_D03_OBSERVATIONS=NUOVO_PERCORSO_GREEN.json /opt/anaconda3/bin/python3 studio2/fase03/harness/test_d03_contract.py
```

Versione finale: **9 test/8 failure/0 errori** sul respinto; **9/9** sul corretto.
JSON completi red_contract.json e green_contract.json; log omonimi.
37 varianti su 11 campi × tre percorsi; 33 colonne SQL N/F; 12 campi degli involucri;
14 alterazioni plausibili di contenuti/impronte. I nove metodi non sono la somma dei
sottocasi. La guardia confronta gli undici controlli effettivamente superati nei tre percorsi.

La prima invocazione diretta verde ometteva il percorso di import e terminava prima dei
test con ModuleNotFoundError: log green_contract_setup_error.log. Corretto il comando con
FOT_HARNESS_TARGET; nessuna modifica del requisito. FINAL_TEST_PROVENANCE.json distingue
la revisione iniziale dalla sola estensione finale della guardia di inventario.

## Suite complete

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions studio2.fase03.harness.test_c01_c03 studio2.fase03.harness.test_d01_replay studio2.fase03.harness.test_d02_predecessors studio2.fase03.harness.test_d03_contract
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 docs/test_explanation.py
```

Log finali targeted.log e discovery.log. Comprendono tutti i sette D01 e otto D02,
oltre ai nove D03. Guardiano documentale prima/dopo e confronto con la review:
35 test, stessi 14 identificativi falliti, 1 skip, zero errori, **NON PASS non bloccante**.

## W, Y, Z, X e originali applicabili

W01–W04: copie byte-identiche di retry_proof_probes.py in before/evidence e after/evidence,
con sibling candidate symlink rispettivamente al clone respinto e al nuovo worktree.
Comando `python COPIA/evidence/retry_proof_probes.py`, cwd rispettivo candidato.
Before: quattro metodi/due failure/zero errori; after: quattro/quattro.

run_extensions.py crea nuovi contenitori per Y, Z, X letterali e X23 già adattato, copia
script e dipendenze byte-identici e salva extension_commands.json con comandi ed exit code.
Il contenitore X23 include sin dall’inizio anche il sibling extended_probes.py.
Y01–Y07 e Z01–Z05 rimangono letterali. Per gli X resta la distinzione 23 letterali più il
solo X23 già adattato: la failure letterale obsoleta X23 è conservata, nessuna nuova assertion
modificata. Gli script possono uscire 0 anche con failure: leggere sempre JSON/log.

Gli originali applicabili usano il RUN_APPLICABLE_ORIGINAL.py storico con candidato corrente,
negative_probes.py e reference della prima review, nuovo sandbox sotto checks/applicable.
Comando esatto in extension_commands.json. 14 metodi: 12 letterali e due soli adattamenti
fixture/argomento precedenti. Tutti i 50 metodi restano nominativi nella matrice acquisita;
non si dichiara 50/50 letterali. Nessuna esclusione implicita di D01/D02/W o N48.

## Storico e contatori

Le vecchie catene senza prove riconciliate restano riprendibili. Una nuova prova genera
con il vecchio 0c8157f una catena valida con retry e 132 intenti: il codice corrente la
rifiuta per assenza del nuovo legame, senza backfill o riscritture. Questo è il cambiamento
di requisito approvato dall’autore. Non si adattano le vecchie prove positive se non ne
dipendono. Le prove W create ora via API ottengono il nuovo legame e restano positive,
compreso il multi-hop a dieci intenti/otto coppie.

Runner/CLI budget e stability con prova alterata: zero query stub, zero nuovi invii,
132 intenti e output/database logico invariati. Gate INVALID resta separato dalla risposta;
un FAILED già registrato INVALID non viene riscritto da una riconciliazione successiva.

## Controlli finali

scope_audit.py confronta 176 file protetti con la base documentale e compila in memoria
93 Python live. Metriche qualificate, runtime C02/C03 esterni al ledger, D01/D02 e documenti
protetti byte-identici. runtime.json contiene il turn_context selezionato della preparazione.
La matrice dei campi è generata da DURABLE_FIELD_CONTRACT.json e dalle osservazioni rosso/verde;
distingue 56 voci esercitate dalle nuove mutazioni e 13 collegate ai contratti storici,
senza rivendicare nuove mutazioni individuali di questi ultimi o esaustività combinatoria.

Manifest e inventari distinguono copie, coordinate esterne, hash, dimensioni e motivi.
Tutti gli originali restano recuperabili. Nessun provider reale, inferenza, simulazione,
push, merge, tag, freeze o GO. D9 eseguibile, ordine label, qualificazioni, T5 e pilot separati.
