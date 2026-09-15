# D04 — nuovo candidato locale, verifica indipendente richiesta

15 settembre 2026. Prosecuzione del mandato R05/R07 di correzione dell’harness offline.
Questo report non chiude autonomamente il NON OK. Nessun freeze o GO.

## Risultato e causa

Il candidato 23859a2 validava quota_kind contro il ruolo in `_validate_attempts` alla
chiusura/riconferma. Il binding dello stadio aperto ricontrollava soltanto le prove zero-token;
la nuova riserva contava quota_kind senza quella validazione. La precedente preparazione
aveva quindi verificato il campo nella fase sbagliata del suo utilizzo. Non era un difetto
del validatore di contenuto D03, ma della collocazione della barriera rispetto alla decisione.

Ora binding/ripresa e ogni nuova riserva validano l’intero inventario cumulativo dei tentativi,
inclusi gli altri stadi aperti, nella stessa transazione. `_validated_attempt_inventory` riusa
`_validate_attempts` contro il piano immutabile: identità, ruolo, catena, prove zero-token.
Non richiede completezza né outcome degli stadi aperti. L’unico runtime cambiato è ledger.py:
**18 righe aggiunte, tre rimosse**; la precedente lista parziale nel binding è sostituita.

V05/V06 originali ora rifiutano la quota incoerente prima della riserva/invio: otto intenti,
sette retry effettivi, zero nuovi invii, database logico invariato dopo il fault. Anche runner
e CLI nuovi rifiutano prima di costruire il client, con server_mock non chiamato e output intatti.

## Le due review ricevute

| Review | Esito e limite preservato |
| --- | --- |
| [Claude](non_ok_23859a2_20260915/VERIFICA_D03_CLAUDE.md) | OK limitato al nucleo D03; differenziale e sonde proprie. Parte delle suite non eseguibile nella VM Linux per riferimenti macOS mancanti. Non equivale a OK sull’intero harness. |
| [Codex](non_ok_23859a2_20260915/files/VERIFICA_D03.md) | D03 originario chiuso nelle prove; NON OK per distinto D04 P2. Tutte le suite dichiarate confermate, V05/V06 fallite. |

I due esiti non sono contraddittori sul nucleo D03. La review Claude dichiara famiglia
Claude e configurazione claude-opus-4-8, con modello servito non dimostrabile dall’interno;
questo report non trasforma tale dichiarazione in una verifica del backend. La review Codex
osserva gpt-6-astra/high in una finestra distinta dalla preparatrice gpt-6-astra/xhigh.
La divergenza fra controlli era dimostrata; il nesso causale con la famiglia di modello no.
La matrice utile dei campi non copriva la dimensione stadio aperto/decisione di riserva.

Hash verificati prima dell’uso:

- Claude, 13.529 byte: `bc3ee96afb2bd890d0b326ca4965d03c46d241f288a30c5ee1455a0c8ec9a47f`.
- Codex: `21e457af023a9a8fae3560f663784c55788408942f8c9e902b3d468764aceef9`.
- Manifest Codex: `9334c9c57b159cf14f047d28646544615c99aaf751298753e573f893dbbb86a1`.

Acquisiti 1.929 membri più il manifest: **1.930 file**, 133 copie byte-identiche e 1.797
esterni con posizione recuperabile, hash, dimensione e motivo. Claude acquisito separatamente
con provenienza, lasciando il file originale untracked nel source intatto. Fixture V con guasti
SQL deliberate e marcate come prove sacrificabili; non sono input scientifici. Symlink separati.
[Inventario](non_ok_23859a2_20260915/ACQUISITION_INVENTORY.json) e
[provenienza](non_ok_23859a2_20260915/PROVENIENZA.md). I log scratch di Claude non sono qui disponibili.

## Identità e cronologia test-first

| Oggetto | Identità |
| --- | --- |
| Worktree | `/Users/luker/fot-tep-harness-0310-d04` |
| Branch | `codex/studio2-harness-0310-d04` |
| Base documentale | `97868f9d6ef281c2dd4ab1c6ffb67e2477ee5715` |
| Tecnico respinto | `23859a29225ccd9cd6f47e4a0b6e36258831dbab` |
| Tree respinto | `fe66025f4925e27676b0be16428475e3fcaee060` |
| Acquisizione separata | `f0dca4d2d46a290d2ffeb1840abd46eb7664f0ae` |
| Contratto/test-first | `bf7774f2d153ecc50f27ba095f77b612933b4d26` |
| **Nuovo tecnico** | **`aae29a908356e4a4842a214fdc3db9bff26ec3ca`** |
| **Tree tecnico** | **`4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`** |
| Manifest | 98 file diretti, 24151 byte |
| SHA-256 manifest | `9fbad8c036075605a9bbdfdac84078259428b679fc33341ed98f21050a07efd6` |

Contratto, inventario delle decisioni e test sono committati **prima della prima modifica
runtime**. TEST_FIRST.json conserva hash delle fonti, dei log e del ledger ancora identico
al respinto. Il file test definitivo non è cambiato dopo il commit test-first.

Stessi otto metodi: **240 assertion fallite in sei metodi, zero errori su 23859a2; 8/8 sul
corretto**. Non sono 240 difetti: 216 sottocasi quota, 14 dipendenze e altre verifiche di
ingresso/ripresa. I due positivi/guardia restano verdi su entrambi. V01–V06 byte-identici:
6 metodi/due failure sul respinto, 6/6 dopo. Nessun errore di setup nelle nuove prove. Le prime suite complete rilevarono tre failure
di precedenza diagnostica (hard stop 200 e prerequisito alternate), pur con rifiuto:
corretta la precedenza nel runtime, mantenendo il nuovo controllo prima di ogni autorizzazione.
Test storici invariati; log intermedi conservati in pre_diagnostic_precedence, suite complete
e prove indipendenti rieseguite sui byte finali.

## Matrice e contratto

[Contratto iniziale](CONTRATTO_D04_PRIMA_DEL_CODICE.md),
[contratto corrente](CONTRATTO_ESECUZIONE_E_RIPRESA.md),
[inventario decisioni](D04_DECISION_CONTRACT.json),
[matrice generata](MATRICE_D04_DECISIONI.md) / [JSON](MATRICE_D04_DECISIONI.json).

- 9 combinazioni stadio/ruolo × 4 stati × 2 ingressi × 3 valori quota errati = **216**.
  **72 controlli positivi** precedono le mutazioni; copertura parziale resta lecita.
- **14** alterazioni dei campi da cui dipende il ruolo, confrontati con piano e catena.
- Ottavo retry senza rinuncia, stessa istanza dopo un precedente successo e restart;
  triplette atomiche, contributori di altro stadio aperto, lock con vero scrittore concorrente.
- Positivi: rinuncia esplicita fino a 15 trasporti, rifiuto del sedicesimo; sonda ferma a sette
  anche con rinuncia, rollback di tutta la tripletta. Quote, remediation e massimi invariati.
- Gli otto nuovi metodi sono sempre gli stessi nel confronto rosso/verde e nelle suite.

L’inventario D03 e i suoi nove test sono byte-identici. La matrice D03 dei 69 campi conserva
la verifica precedente (56 nuove mutazioni, 13 collegamenti storici); questo delta aggiunge
le coordinate delle decisioni negli stadi aperti. Nuovi stadi/ruoli nell’inventario sono
soggetti alla guardia; i campi nuovi restano DA_COPRIRE nella guardia D03. Sono prove finite,
non esaustività di ogni valore, stato futuro o riscrittura coerente dell’intera catena.

**Snapshot diagnostico:** non certifica il DB manomesso e non autorizza nuove richieste.
Nelle V05/V06 corrette rimangono sette archi retry_of, mentre la singola quota alterata
fa ancora leggere sei trasporti allo snapshot. La discordanza è preservata come guasto:
le operazioni normative la rifiutano, senza riparazione o riclassificazione automatica.
Nessuna nuova politica legacy: digest/legame assenti restano bloccati, nessun backfill.

## Risultati eseguiti

| Prova | Esito |
| --- | --- |
| Mirati completi | **128/128**, zero failure/errori |
| Discovery | **163/163**, zero failure/errori |
| D04 | **8/8**, contro 240 assertion fallite/zero errori sul respinto |
| D01 / D02 / D03 | **7/7, 8/8, 9/9**, tutti inclusi e file invariati |
| V01–V06 | **6/6**, byte-identici, contro V05/V06 fallite sul respinto |
| W01–W04 / Y / Z | **4/4, 7/7, 5/5**, byte-identici |
| Applicabili | **14/14**, 12 letterali e due soli precedenti adattamenti fixture/argomento |
| X | 23 letterali più X23 già adattato; sola failure letterale obsoleta X23 conservata |
| Guardiano documentale | **NON PASS**, 35 test, stessi 14 identificativi falliti, 1 skip, zero errori |
| Perimetro | **177** file protetti byte-identici alla base |
| Sintassi | **94** Python live compilati in memoria, zero errori |

Suite e sottocasi si sovrappongono e non si sommano. [Matrice R01–R10](MATRICE_R01_R10_D04.md)
e [50 nomi espliciti](non_ok_23859a2_20260915/files/MATRICE_50_METODI.md), N48≡C02:
nessuna pretesa di 50/50 letterali. Guardiano documentale non bloccante per questo delta.

[RESULTS](d04_evidence/RESULTS.json), [comandi](d04_evidence/runs/COMANDI.md),
[inventario prove](d04_evidence/REPRODUCTION_INVENTORY.json), [SHA256SUMS](d04_evidence/SHA256SUMS):
98 copie delle riproduzioni e 3752 fixture esterne recuperabili.
Originali, copie e coordinate esterne ricontrollati prima della consegna. Il generatore della
matrice è incluso; i log conservano le whitespace originali senza normalizzazione.

## Perimetro e limiti

Tredici repository confrontati con lo stato iniziale, incluso il source con verbale Claude
untracked già presente; principale e review precedenti preservate. Main effettivo su GitHub
ricontrollato (`a00605862f627710347bd63c49f79a6d0a00135f`). Nessun lavoro parallelo importato.
Tre metriche qualificate, runtime producer/consumer, gate_rules, D01/D02/D03, piano rev.10,
APERTURA, D9, walkthrough, A/B, FAR, U3 e freeze restano intatti.

Preparatrice: task `01a0a204-abda-7a00-8466-f52f5bc84812`, gpt-6-astra/xhigh osservato in
[runtime.json](d04_evidence/runs/runtime.json); Python 3.13.9, SQLite 3.51.0 su macOS.
Nessuna delega o nuova verifica indipendente rivendicata. L’OK Claude sul vecchio D03 non
si trasferisce a questi nuovi byte. I percorsi esterni delle fixture storiche restano un
limite di portabilità verso VM non dotate degli stessi riferimenti, già esplicitato da Claude.

Letti entrambi i verbali integrali e relativi hash, prove V, codice e contratti pertinenti,
MAINTENANCE principale, prompt operativi e fonti §0 del walkthrough candidato: alcune centinaia
di kB pertinenti, oltre ai confronti meccanici. Nessun nuovo audit scientifico o bibliografico.

D9 approvata: 122B principale/consumer, 27B alternativo completo 16 insight, Terra storico
interno. Recepimento eseguibile D9, ordine label reale, qualificazioni, T5 e pilot restano
separati; preflight storico bloccato. Nessun push/merge/tag, provider reale, inferenza,
simulazione scientifica, freeze o GO. Serve la review del tecnico e tree esatti.

## File e consegna

Acquisizione: 139 file. Test-first: sei file. Commit tecnico: 107 percorsi;
delta dopo acquisizione: 113 percorsi. Solo ledger.py è runtime live.
Il successore documentale aggiunge esclusivamente REPORT_CORREZIONE_D04.md,
PROMPT_VERIFICA_D04.md, CONSEGNA_D04.json e DELIVERY_AUDIT_D04.json: HEAD distinto dal tecnico.
Nessuna autoreferenza negli hash. Elenco del commit tecnico (codice/contratto/matrici e
relative prove, log, script e inventari):

- `studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md`
- `studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json`
- `studio2/fase03/harness/MATRICE_D04_DECISIONI.json`
- `studio2/fase03/harness/MATRICE_D04_DECISIONI.md`
- `studio2/fase03/harness/MATRICE_R01_R10_D04.md`
- `studio2/fase03/harness/d04_evidence/REPRODUCTION_INVENTORY.json`
- `studio2/fase03/harness/d04_evidence/RESULTS.json`
- `studio2/fase03/harness/d04_evidence/SHA256SUMS`
- `studio2/fase03/harness/d04_evidence/runs/COMANDI.md`
- `studio2/fase03/harness/d04_evidence/runs/after/console.log`
- `studio2/fase03/harness/d04_evidence/runs/after/evidence/independent_d03_probes.json`
- `studio2/fase03/harness/d04_evidence/runs/after/evidence/independent_d03_probes.log`
- `studio2/fase03/harness/d04_evidence/runs/after/evidence/independent_d03_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/applicable.console.log`
- `studio2/fase03/harness/d04_evidence/runs/applicable/applicable.json`
- `studio2/fase03/harness/d04_evidence/runs/applicable/applicable.log`
- `studio2/fase03/harness/d04_evidence/runs/applicable/evidence/negative_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/before/console.log`
- `studio2/fase03/harness/d04_evidence/runs/before/evidence/independent_d03_probes.json`
- `studio2/fase03/harness/d04_evidence/runs/before/evidence/independent_d03_probes.log`
- `studio2/fase03/harness/d04_evidence/runs/before/evidence/independent_d03_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/compile.json`
- `studio2/fase03/harness/d04_evidence/runs/diagnostic_precedence.log`
- `studio2/fase03/harness/d04_evidence/runs/discovery.log`
- `studio2/fase03/harness/d04_evidence/runs/documentation_after.log`
- `studio2/fase03/harness/d04_evidence/runs/documentation_before.log`
- `studio2/fase03/harness/d04_evidence/runs/documentation_comparison.json`
- `studio2/fase03/harness/d04_evidence/runs/extension_commands.json`
- `studio2/fase03/harness/d04_evidence/runs/extensions.console.log`
- `studio2/fase03/harness/d04_evidence/runs/generate_decision_matrix.py`
- `studio2/fase03/harness/d04_evidence/runs/green_contract.json`
- `studio2/fase03/harness/d04_evidence/runs/green_contract.log`
- `studio2/fase03/harness/d04_evidence/runs/literal/additional_edges.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/literal/evidence/additional_edges.py`
- `studio2/fase03/harness/d04_evidence/runs/literal/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d04_evidence/runs/literal/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d04_evidence/runs/literal/evidence/extended.json`
- `studio2/fase03/harness/d04_evidence/runs/literal/evidence/extended.log`
- `studio2/fase03/harness/d04_evidence/runs/literal/evidence/extended_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/literal/extended_probes.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/PROVENANCE.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/after/console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/after/evidence/independent_d03_probes.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/after/evidence/independent_d03_probes.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/after/evidence/independent_d03_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/applicable.console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/applicable/applicable.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/applicable/applicable.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/applicable/evidence/negative_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/discovery.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/extension_commands.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/extensions.console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/green_contract.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/green_contract.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/literal/additional_edges.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/literal/evidence/additional_edges.py`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/literal/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/literal/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/literal/evidence/extended.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/literal/evidence/extended.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/literal/evidence/extended_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/literal/extended_probes.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/runtime_delta.diff`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/targeted.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/w_original/evidence/retry_proof_probes.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/w_original/evidence/retry_proof_probes.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/w_original/evidence/retry_proof_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/w_original/retry_proof_probes.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/x23_adapted/additional_edges.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/x23_adapted/evidence/additional_edges.py`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/x23_adapted/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/x23_adapted/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/x23_adapted/evidence/extended_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/y_original/edge_probes.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/y_original/evidence/edge_probes.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/y_original/evidence/edge_probes.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/y_original/evidence/edge_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/z_original/chain_probes.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/z_original/evidence/chain_probes.json`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/z_original/evidence/chain_probes.log`
- `studio2/fase03/harness/d04_evidence/runs/pre_diagnostic_precedence/z_original/evidence/chain_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/red_contract.json`
- `studio2/fase03/harness/d04_evidence/runs/red_contract.log`
- `studio2/fase03/harness/d04_evidence/runs/run_extensions.py`
- `studio2/fase03/harness/d04_evidence/runs/runtime.json`
- `studio2/fase03/harness/d04_evidence/runs/scope.json`
- `studio2/fase03/harness/d04_evidence/runs/scope_audit.py`
- `studio2/fase03/harness/d04_evidence/runs/setup_notes.json`
- `studio2/fase03/harness/d04_evidence/runs/targeted.log`
- `studio2/fase03/harness/d04_evidence/runs/w_original/evidence/retry_proof_probes.json`
- `studio2/fase03/harness/d04_evidence/runs/w_original/evidence/retry_proof_probes.log`
- `studio2/fase03/harness/d04_evidence/runs/w_original/evidence/retry_proof_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/w_original/retry_proof_probes.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/x23_adapted/additional_edges.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/x23_adapted/evidence/additional_edges.py`
- `studio2/fase03/harness/d04_evidence/runs/x23_adapted/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/d04_evidence/runs/x23_adapted/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/d04_evidence/runs/x23_adapted/evidence/extended_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/y_original/edge_probes.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/y_original/evidence/edge_probes.json`
- `studio2/fase03/harness/d04_evidence/runs/y_original/evidence/edge_probes.log`
- `studio2/fase03/harness/d04_evidence/runs/y_original/evidence/edge_probes.py`
- `studio2/fase03/harness/d04_evidence/runs/z_original/chain_probes.py.console.log`
- `studio2/fase03/harness/d04_evidence/runs/z_original/evidence/chain_probes.json`
- `studio2/fase03/harness/d04_evidence/runs/z_original/evidence/chain_probes.log`
- `studio2/fase03/harness/d04_evidence/runs/z_original/evidence/chain_probes.py`
- `studio2/fase03/harness/ledger.py`
