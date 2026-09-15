# D03 — candidato locale corretto, nuova verifica indipendente richiesta

15 settembre 2026. Implementazione autorizzata dall’autore dopo la review di processo.
Questo report non chiude il NON OK e non autorizza freeze o GO.

## Risultato

Acquisizione, riconferma dell’antenato retry e gate riconciliato condividono ora gli stessi
**11 controlli di contenuto** per prova zero-token e approvazione. Le nuove prove conservano
hash dei file, digest ricalcolabili dei contenuti e un legame durevole separato. La ripresa
con prove alterate viene rifiutata **prima di interrogare lo stub/server**. Le prove legacy
senza digest/legame sono rifiutate senza backfill, come richiesto dall’autore.

Il presidio è stato introdotto nell’ordine richiesto: inventario, contratto e test rossi
prima del runtime. I test finali producono **9 metodi, 8 failure e zero errori su a219bd4**;
**9/9 sul nuovo codice**. Le suite complete finali passano **120/120 mirati e 155/155 discovery**.
Tutti i D01/D02 e W01–W04 sono rieseguiti. Nessuna chiusura autonoma di D03.

## Identità e separazione dei commit

| Oggetto | Identificatore |
| --- | --- |
| Worktree | `/Users/luker/fot-tep-harness-0310-d03` |
| Branch | `codex/studio2-harness-0310-d03` |
| Base documentale | `e9b60c5db77edfd3c06a29857e6ba5f61ebe139a` |
| Respinto tecnico | `a219bd469bbd280f56b7fa9cb56cda115b0975ed` |
| Tree respinto | `3fb8e50c189b85b447503b8a1ac99c1741904a5b` |
| Acquisizione separata | `efa9f6f94194985104047d831c0b087dc460532d` |
| Contratto e test-first | `567881abf06572812c00ccc0ed817d169b68fee6` |
| **Nuovo candidato tecnico** | **`23859a29225ccd9cd6f47e4a0b6e36258831dbab`** |
| **Tree tecnico** | **`fe66025f4925e27676b0be16428475e3fcaee060`** |
| Manifest | 83 file diretti, 20826 byte |
| SHA-256 manifest | `483c7db5ad4a763a8f41d084538c7a2cce6b2a7d799a5ba11d57da852cee3828` |
| Main remoto effettivo letto | `a00605862f627710347bd63c49f79a6d0a00135f` |

Il tecnico era pulito prima della scrittura della consegna. Il successore documentale
aggiunge soltanto REPORT_CORREZIONE_D03.md, PROMPT_VERIFICA_D03.md, CONSEGNA_D03.json e
DELIVERY_AUDIT_D03.json; il suo HEAD resta distinto dal candidato. Nessun hash autoreferenziale.

## Acquisizione verificata

Il [verbale NON OK originale](non_ok_a219bd4_20260915/files/VERIFICA_D02.md) e il suo
[SHA256SUMS](non_ok_a219bd4_20260915/files/SHA256SUMS) provengono da
`/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence`.

- Verbale SHA-256 `b88f046592ac9d1b0f784c1d127f83ea3cc609c93bd547bbc91c7541cfd0223f`.
- Manifest SHA-256 `4ed360ee40d521e989e38fa2a2a68d5a5c461a5a6397c94dd34a598300141776`.
- **1.868 membri + il manifest**, tutti riletti: **116 copie byte-identiche**, **1.753 esterni**
  recuperabili con percorso, hash, dimensione e motivo. Fixture W pertinenti incluse;
  fixture N/X/Y/Z ripetute conservate esternamente. Symlink inventariati separatamente.
- [Inventario](non_ok_a219bd4_20260915/ACQUISITION_INVENTORY.json),
  [provenienza](non_ok_a219bd4_20260915/PROVENIENZA.md) e stati Git prima delle scritture.
- Analisi Fable fornita dall’autore acquisita byte-identica come contesto di processo,
  non come nuovo OK tecnico o prova della diversità del modello.

Originali e copie sono stati verificati prima dell’esecuzione e nuovamente prima della
consegna. I guasti SQL sono soltanto su nuove fixture sacrificabili, mai dati scientifici,
candidati precedenti o prove conservate. Source e clone detached sono distinti; il source
e9b60c5 differisce dal precedente tecnico a219bd4 solo nei quattro documenti della sua consegna.

## Contratto prima del codice e matrice

[Contratto iniziale D03](CONTRATTO_D03_PRIMA_DEL_CODICE.md) e
[inventario macchina](DURABLE_FIELD_CONTRACT.json) sono committati prima del runtime.
[TEST_FIRST.json](d03_evidence/TEST_FIRST.json) conserva hash del runtime allora invariato,
fonti e prove rosse. Gli hash delle fonti in TEST_FIRST si verificano sui blob del commit
`567881abf06572812c00ccc0ed817d169b68fee6`, non confondendoli con la successiva estensione della guardia.

Inventario: **69 voci** (33 colonne SQLite, 11 campi prova/approvazione, 25 voci dei payload).
N è normativo; F è forense. Raw, record e contenitori improntati sono atomici: i discendenti
sono N per integrità dei byte, inclusi i timestamp incorporati. Le colonne di cattura e le
note esterne a tali artefatti sono F. I duplicati di bookkeeping nelle requests non sostituiscono
il consumo normativo nel record o i tre contatori zero nell’evidence. Nessuna nuova quantità
viene dedotta dalla modifica di un duplicato forense.

La [matrice generata dei campi](MATRICE_D03_CAMPI.md) e il [JSON](MATRICE_D03_CAMPI.json)
derivano dall’inventario e dalle osservazioni rosso/verde: **37 varianti × 3 percorsi**,
**33 colonne SQL**, **12 campi degli involucri**, **14 alterazioni plausibili di contenuti/impronte**.
Sono 56 voci con nuove mutazioni generate e 13 con corrispondenze ai contratti storici:
non si rivendicano nuove mutazioni individuali di queste ultime o esaustività combinatoria.
I campi strutturali nuovi, incluse le chiavi nominate annidate in evidence/approval, sono
DA_COPRIRE; la guardia deve segnalarli. I payload opachi restano protetti come contenitori.
Il generatore riproducibile è in d03_evidence/runs/generate_field_matrix.py, con argomenti
--harness-dir e --checks-dir.

La prima versione a sette metodi era rossa; completata prima del runtime a nove metodi,
era ancora rossa (otto failure, zero errori). Dopo il primo verde è stata rafforzata solo
la guardia per le nuove chiavi annidate; nessuna aspettativa è stata indebolita. La versione
finale è stata rieseguita sul respinto e sul corretto, e le suite complete rilanciate.
Le prove iniziali rimangono immutate; quelle intermedie sono conservate in runs/pre_inventory_guard.
[Provenienza finale dei test](d03_evidence/runs/FINAL_TEST_PROVENANCE.json) distingue le versioni.

## Delta del runtime

Il solo runtime modificato è `ledger.py`:

1. `_validate_zero_token_evidence` verifica identità, disposition, ricevuta/evidenza provider,
   tre int zero (esclusi bool), autore, decisione e approvazione del file esatto. I tre
   percorsi invocano l’intero contratto; i chiamanti mantengono le proprie precondizioni di stato.
2. Acquisizione legge una sola volta i byte di prova/approvazione. Conserva gli hash dei file
   e aggiunge evidence_content_sha256/approval_content_sha256; formula esplicita richiesta:
   `digest(canonical_json(value))`, distinta dall’hash dei byte originali. Poiché digest
   canonizza già l’argomento, la formula viene applicata letteralmente anche nella verifica.
3. `reconciled_integrity:<request_id>` lega identità della richiesta, hash dei file, digest
   dei contenuti e stato precedente. Evento, prova e cambio di stato sono atomici; il legame
   viene ricalcolato nella riconferma. Non basta l’uguaglianza fra vecchie stringhe hash.
4. `_validated_reconciliation` è usato dagli antenati retry, dall’assegnazione di un nuovo
   retry e dal gate ZERO_TOKEN_PROVEN. Anche il binding di uno stadio aperto ripreso verifica
   le prove prima del server. L’ingresso pubblico gate_transport_record ha un’unica transazione.
5. Un FAILED già rappresentato da INVALID conserva il suo record immutabile anche dopo una
   riconciliazione; il riuso verifica la prova successiva. Nessuna risposta viene inventata.
6. La matrice SQL ha evidenziato quota_kind non ricontrollato: ora deve coincidere con il
   ruolo base/remediation/transport. Le quote e i massimi non cambiano.

Il formato SQLite resta v2. Nessuna cache fra transazioni, migrazione automatica, backfill,
nuovo invio implicito, riscrittura di storia, azzeramento o cambiamento di metriche.

## Requisito storico approvato

Una prova senza nuovi digest/legame non viene riconfermata, anche se era accettata dal vecchio
codice. Lo sblocco richiede una riconciliazione revisionata separata già prevista per il legacy;
non viene aggiunta qui un’API che autentichi a posteriori dati ignoti.

Una nuova regressione genera con il vecchio 0c8157f, verificato esatto e pulito, una catena
allora valida con retry: il nuovo codice la rifiuta e conserva **132 intenti** e database logico.
Le vecchie positive D01 senza tali prove rimangono valide: tutti i loro sette metodi sono
invariati e passano. Non è stato necessario adattarli. I positivi creati con il codice corrente
ottengono il nuovo legame e mantengono retry a nove intenti, multi-hop a dieci e gate INVALID.

## Risultati finali

| Prova | Esito |
| --- | --- |
| Mirati | **120/120**, zero failure/errori |
| Discovery | **155/155**, zero failure/errori |
| Test D03 finali sul respinto | **9 metodi, 8 failure, zero errori** |
| Test D03 finali sul corretto | **9/9** |
| D01 e D02 storici | **7/7 e 8/8**, inclusi nelle suite, file invariati |
| W01–W04 letterali | **4/4**, contro due failure sul respinto |
| Y01–Y07 e Z01–Z05 letterali | **7/7 e 5/5** |
| Originali applicabili | **14/14**, 12 letterali e due precedenti adattamenti fixture/argomento |
| X01–X18 | **18/18** letterali |
| X19–X24 | Cinque PASS e sola failure letterale obsoleta X23 |
| X23 già adattato | **1/1**, nessun nuovo adattamento |
| Guardiano documentale | **NON PASS**, 35 test, stessi 14 identificativi falliti, 1 skip, zero errori |
| Sintassi | **93** Python live, zero errori |
| File protetti | **176** confronti byte-identici con la base |

Runner e CLI budget/stability con prova alterata rifiutano tutti e quattro gli ingressi:
**zero query stub, zero nuovi invii, 132 intenti e stessi output/database logico**. W02 conferma
anche il percorso ordinario. W03/W04 preservano multi-hop e verifica dopo un nuovo fault nella
stessa istanza. La guardia simmetrica osserva gli stessi 11 controlli nei tre percorsi;
le mutazioni con hash locali riallineati continuano a richiedere contenuti semanticamente validi.

Le [50 corrispondenze nominative](non_ok_a219bd4_20260915/files/MATRICE_50_METODI.md) sono
acquisite byte-identiche, compresa N48 equivalente a C02. Nessun 50/50 letterali implicito.
[Matrice R01–R10 corrente](MATRICE_R01_R10_D03.md). Suite e sottocasi non si sommano;
il consolidamento X è 23 letterali + X23 già adattato, non 24/24 sul file immutato.

[RESULTS.json](d03_evidence/RESULTS.json), [comandi](d03_evidence/runs/COMANDI.md),
[inventario](d03_evidence/REPRODUCTION_INVENTORY.json) e [SHA256SUMS](d03_evidence/SHA256SUMS):
**61 copie byte-identiche delle riproduzioni e 1848 fixture esterne**
recuperabili. I tre file della prova test-first restano separati e immutati.
Un iniziale errore di percorso d’import nella sola invocazione diretta verde è conservato
in green_contract_setup_error.log: risolto passando FOT_HARNESS_TARGET; non è un difetto runtime
né un PASS. Le whitespace degli originali acquisiti/log non sono state normalizzate.

## Perimetro, modello e limiti

Task preparatore `01a0a204-abda-7a00-8466-f52f5bc84812`, **gpt-6-astra/xhigh**, da turn_context
selezionato in [runtime.json](d03_evidence/runs/runtime.json). Il precedente revisore usa altra
finestra e stesso modello/high; diversità di modello assente. La causa dimostrata era la
validazione divergente; il nesso con la famiglia del modello resta ipotesi. La guardia di
contratto e la matrice sono presidi indipendenti dal modello. Nessuna delega o nuova review
indipendente viene rivendicata dalla preparazione.

Letti mandato aggiornato e analisi Fable, MAINTENANCE e prompt pertinenti già acquisiti,
verbale D03 integrale, codice/contratti/prove interessati; ordine di grandezza alcune centinaia
di kB pertinenti, oltre ai confronti meccanici. Nessun nuovo audit scientifico o di letteratura.

Undici repository/source/candidati precedenti vengono confrontati con gli stati iniziali;
main remoto reale ricontrollato. Tre metriche qualificate, C02/C03 esterni al ledger, D01/D02,
piano rev.10, APERTURA, D9, walkthrough, A/B, FAR, U3 e freeze preservati. Nessuna modifica
parallela importata. Nessun push/merge/tag, provider reale, inferenza o simulazione scientifica.

D9 approvata: 122B producer principale e consumer, 27B alternativo completo 16 insight,
Terra storico interno. Recepimento eseguibile D9, ordine label reale, qualificazioni,
T5 e pilot restano separati; preflight storico bloccato. Nessun freeze o GO.

Limiti: test finiti e classificazione dei contenitori non dimostrano assenza di ogni futuro
difetto. Non si rivendica resistenza a una riscrittura arbitraria coerente dell’intera catena
e delle impronte. Le prove legacy prive di nuovo legame rimangono bloccate. Serve una nuova
verifica indipendente del candidato e tree esatti.

## File e commit

Il commit test-first contiene sei file (contratto iniziale, inventario, test, due prove rosse
e TEST_FIRST.json). Il commit runtime/consegna tecnica contiene 71 percorsi;
il delta complessivo successivo all’acquisizione contiene 76 percorsi.
Elenco del commit tecnico finale:

- `studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md`
- `studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json`
- `studio2/fase03/harness/MATRICE_D03_CAMPI.json`
- `studio2/fase03/harness/MATRICE_D03_CAMPI.md`
- `studio2/fase03/harness/MATRICE_R01_R10_D03.md`
- `studio2/fase03/harness/d03_evidence/REPRODUCTION_INVENTORY.json`
- `studio2/fase03/harness/d03_evidence/RESULTS.json`
- `studio2/fase03/harness/d03_evidence/SHA256SUMS`
- `studio2/fase03/harness/d03_evidence/runs/COMANDI.md`
- `studio2/fase03/harness/d03_evidence/runs/FINAL_TEST_PROVENANCE.json`
- `studio2/fase03/harness/d03_evidence/runs/after/console.log`
- `studio2/fase03/harness/d03_evidence/runs/after/evidence/retry_proof_probes.json`
- `studio2/fase03/harness/d03_evidence/runs/after/evidence/retry_proof_probes.log`
- `studio2/fase03/harness/d03_evidence/runs/after/evidence/retry_proof_probes.py`
- `studio2/fase03/harness/d03_evidence/runs/applicable.console.log`
- `studio2/fase03/harness/d03_evidence/runs/applicable/applicable.json`
- `studio2/fase03/harness/d03_evidence/runs/applicable/applicable.log`
- `studio2/fase03/harness/d03_evidence/runs/applicable/evidence/negative_probes.py`
- `studio2/fase03/harness/d03_evidence/runs/before/console.log`
- `studio2/fase03/harness/d03_evidence/runs/before/evidence/retry_proof_probes.json`
- `studio2/fase03/harness/d03_evidence/runs/before/evidence/retry_proof_probes.log`
- `studio2/fase03/harness/d03_evidence/runs/before/evidence/retry_proof_probes.py`
- `studio2/fase03/harness/d03_evidence/runs/compile.json`
- `studio2/fase03/harness/d03_evidence/runs/discovery.log`
- `studio2/fase03/harness/d03_evidence/runs/documentation_after.log`
- `studio2/fase03/harness/d03_evidence/runs/documentation_before.log`
- `studio2/fase03/harness/d03_evidence/runs/documentation_comparison.json`
- `studio2/fase03/harness/d03_evidence/runs/extension_commands.json`
- `studio2/fase03/harness/d03_evidence/runs/generate_field_matrix.py`
- `studio2/fase03/harness/d03_evidence/runs/green_contract.json`
- `studio2/fase03/harness/d03_evidence/runs/green_contract.log`
- `studio2/fase03/harness/d03_evidence/runs/green_contract_setup_error.log`
- `studio2/fase03/harness/d03_evidence/runs/literal/additional_edges.py.console.log`
- `studio2/fase03/harness/d03_evidence/runs/literal/evidence/additional_edges.py`
- `studio2/fase03/harness/d03_evidence/runs/literal/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d03_evidence/runs/literal/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d03_evidence/runs/literal/evidence/extended.json`
- `studio2/fase03/harness/d03_evidence/runs/literal/evidence/extended.log`
- `studio2/fase03/harness/d03_evidence/runs/literal/evidence/extended_probes.py`
- `studio2/fase03/harness/d03_evidence/runs/literal/extended_probes.py.console.log`
- `studio2/fase03/harness/d03_evidence/runs/pre_inventory_guard/discovery.log`
- `studio2/fase03/harness/d03_evidence/runs/pre_inventory_guard/green_contract.json`
- `studio2/fase03/harness/d03_evidence/runs/pre_inventory_guard/green_contract.log`
- `studio2/fase03/harness/d03_evidence/runs/pre_inventory_guard/red_contract.json`
- `studio2/fase03/harness/d03_evidence/runs/pre_inventory_guard/red_contract.log`
- `studio2/fase03/harness/d03_evidence/runs/pre_inventory_guard/targeted.log`
- `studio2/fase03/harness/d03_evidence/runs/red_contract.json`
- `studio2/fase03/harness/d03_evidence/runs/red_contract.log`
- `studio2/fase03/harness/d03_evidence/runs/red_contract_initial.json`
- `studio2/fase03/harness/d03_evidence/runs/red_contract_initial.log`
- `studio2/fase03/harness/d03_evidence/runs/run_extensions.py`
- `studio2/fase03/harness/d03_evidence/runs/runtime.json`
- `studio2/fase03/harness/d03_evidence/runs/scope.json`
- `studio2/fase03/harness/d03_evidence/runs/scope_audit.py`
- `studio2/fase03/harness/d03_evidence/runs/setup_notes.json`
- `studio2/fase03/harness/d03_evidence/runs/targeted.log`
- `studio2/fase03/harness/d03_evidence/runs/x23_adapted/additional_edges.py.console.log`
- `studio2/fase03/harness/d03_evidence/runs/x23_adapted/evidence/additional_edges.py`
- `studio2/fase03/harness/d03_evidence/runs/x23_adapted/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d03_evidence/runs/x23_adapted/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d03_evidence/runs/x23_adapted/evidence/extended_probes.py`
- `studio2/fase03/harness/d03_evidence/runs/y_original/edge_probes.py.console.log`
- `studio2/fase03/harness/d03_evidence/runs/y_original/evidence/edge_probes.json`
- `studio2/fase03/harness/d03_evidence/runs/y_original/evidence/edge_probes.log`
- `studio2/fase03/harness/d03_evidence/runs/y_original/evidence/edge_probes.py`
- `studio2/fase03/harness/d03_evidence/runs/z_original/chain_probes.py.console.log`
- `studio2/fase03/harness/d03_evidence/runs/z_original/evidence/chain_probes.json`
- `studio2/fase03/harness/d03_evidence/runs/z_original/evidence/chain_probes.log`
- `studio2/fase03/harness/d03_evidence/runs/z_original/evidence/chain_probes.py`
- `studio2/fase03/harness/ledger.py`
- `studio2/fase03/harness/test_d03_contract.py`
