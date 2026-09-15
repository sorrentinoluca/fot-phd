# D04 — matrice R01–R10 per il nuovo candidato

Le due review di 23859a2 confermano D03 nel perimetro eseguito. La review Codex apre D04
su R05; il delta corrente richiede una nuova verifica indipendente. Nessun freeze o GO.

| Requisito | Modifica o conservazione | Prove del delta e non-regressione |
| --- | --- | --- |
| R01 | Binding prima del client/server ora valida tutti i tentativi che consumano quote; configurazione storica sempre bloccata | D04 runner/CLI, V04/V06; R01, Y05, X17 |
| R02 | Piano e identità verificati anche prima delle riserve; pin/input/R4 e digest D03 invariati | D04 role_dependencies; D02/D03, R02, X12/X14/X17 |
| R03 | Nessuna modifica label_space/presentazione | R03, X17, applicabili; ordine reale separato |
| R04 | `_validate_attempts` riusato sugli stadi aperti senza richiedere outcome o copertura completa; chiusura invariata | D04 matrice e lock; D01/D02/D03, V01/V03, Y/Z |
| **R05 / D04** | `_validated_attempt_inventory` controlla piano/ruolo/catena di tutti gli stadi prima di binding e `_insert_intent`, nella transazione chiamante | **216 mutazioni quota + 14 dipendenze**, V05/V06, ottavo retry, rinuncia, triplette, altro stadio aperto, scrittore reale |
| R06 | Remediation usa la stessa riserva cumulativa validata; regole/diagnosi/diff/template/otto casi invariati | D04 matrice remediation, R06, D01/D02 remediation, X10/X20/X24 |
| R07 | Restart rifiuta quota incoerente prima della nuova riga e del trasporto; prove D03/no-backfill invariati | D04 runner/CLI e stessa istanza, V04–V06; W01–W04, D03 completo |
| R08 | Sonda/freeze continuano a riconfermare predecessori e prove; nessuna nuova decisione scientifica | D01/D02, Z01/Z02/Z04, X18, R08 |
| R09 | Raw/risposte, identità provider e sospensione conservati | R09, X13/X22, Y03/Y05; D04 conserva output e DB |
| R10 | Triplette atomiche validate prima della prima riserva; gate senza retry e criteri invariati | D04 triplette, R05, GateRevisions, C02, X11, X23 adattato, Z05 |

## Distinzioni necessarie

- Quote 8r+t≤15, sette trasporti senza rinuncia, massimo 15 con rinuncia, sonda mai oltre
  sette, massimo pianificato 152/160 e hard stop 200 restano distinti e invariati.
- Lo snapshot è diagnostico su dati persistiti: non certifica la validità di un DB
  deliberatamente alterato. Binding/riserva ne rifiutano la discordanza senza ripararla.
- L’[inventario dei campi](DURABLE_FIELD_CONTRACT.json) e i nove test D03 restano identici.
  La [matrice nuova](MATRICE_D04_DECISIONI.md) aggiunge stadio/ruolo/stato/ingresso.
  Non è una dimostrazione esaustiva di ogni combinazione futura.
- I sette D01, otto D02, nove D03, W 4, V 6, Y 7 e Z 5 vengono rieseguiti integralmente.
  Gli script indipendenti sono byte-identici. X: 23 letterali + X23 già adattato;
  la failure letterale obsoleta rimane visibile. Applicabili: 14, con i due soli precedenti
  adattamenti di fixture/argomento.
- [50 metodi espliciti](non_ok_23859a2_20260915/files/MATRICE_50_METODI.md), compresa N48≡C02:
  matrice acquisita byte-identica, nessuna pretesa di 50/50 letterali.
- Risultati eseguiti e conteggi finali: [RESULTS.json](d04_evidence/RESULTS.json).
  Suite, metodi e sottocasi sovrapposti non si sommano.

Il guardiano documentale NON PASS resta non bloccante. D9 eseguibile, ordine label,
qualificazioni, T5 e pilot sono perimetri separati; nessun freeze o GO.
