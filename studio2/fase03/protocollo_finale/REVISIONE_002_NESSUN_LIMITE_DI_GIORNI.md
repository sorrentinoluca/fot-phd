# Revisione 002 del protocollo finale — nessun limite di giorni

**Decisione dell'autore (Luca), 2026-09-18**, presa prima di qualunque chiamata del batch finale
e prima della materializzazione del target. Revisione rispetto al tag
`studio2-fase03-protocollo-finale-frozen-001` (`396353778887f3748be331727187035d4fe1e779`);
tag previsto: `studio2-fase03-protocollo-finale-frozen-002`.

`PROTOCOLLO_FINALE_CANDIDATE.md` (`5d130dd4…`) e `.json` (`cdf64c94…`) **non sono modificati**:
questa revisione si legge sopra di essi e prevale solo sui punti elencati sotto.

## Decisione

La campagna non ha un numero massimo di giorni civili. Si esegue un canary (dieci prompt di §6)
per ogni giorno civile Europe/Rome in cui si inviano chiamate scientifiche, prima del primo lotto,
per tutti i giorni che servono.

## Motivazione

Il tetto di sette giorni civili non ha funzione scientifica. `W` = 7 giorni (168 h) era un
controllo di **fattibilità pre-avvio** (T5), già superato: 62,9 h alla media e 88,0 h al p95 con
margine del 20 %. Non è una scadenza di campagna. La stabilità del modello lungo la campagna è
garantita dal canary giornaliero e dal controllo d'identità su ogni chiamata, non dalla durata.
La decisione è presa prima di qualunque dato del batch finale e non dipende da alcun risultato.

## Diff dei numeri

| Voce | frozen-001 | Revisione 002 |
| --- | ---: | ---: |
| Giorni civili massimi di campagna (§6.1) | 7 | nessun massimo |
| Quota dello stage `final_canary` (§7.1) | 70 | **300** |
| Massimo totale di chiamate (§5.1) | 7.202 | **7.432** = 6.732 + 300 + 400 |
| Scientifiche, `technical_verification`, retry `Q` | 6.732 / 0 / 400 | invariati |

La quota 300 (30 giorni × 10) è una **guardia contabile senza significato scientifico**: esiste
perché il ledger vuole un involucro di quota finito e dichiarato alla creazione. Il massimo 7.432
non è un obiettivo: le chiamate canary effettive sono dieci per giorno di campagna. Raggiungere
300 è uno STOP contabile che si risolve con una nuova revisione dichiarata, non localmente.

Punti del candidato sostituiti: §6 regola 1 («massimo sette giorni civili… Oltre sette giorni o
W: STOP») → un canary per giorno, senza massimo; §6 regola 3 («slot dei 70») → slot della quota
canary; §5.1 e §7.1 dove citano 70 e 7.202 → 300 e 7.432. §5.2 (T5) resta com'è, come controllo
pre-avvio superato; le sue durate sono calcolate con 70 canary e ogni giorno aggiuntivo costa
dieci chiamate (~4–6 minuti).

## Invariato

Barriera canary per giorno civile (nessun lotto scientifico senza canary PASS dello stesso
giorno); primo giorno PASS obbligatorio; STOP immediato su cambio di `returned_model` o
`system_fingerprint`; STOP al secondo giorno MARKED; maschere primaria/forense/unione; retry D3
(`Q` = 400, solo zero-token provati, STOP a 5 fallimenti tecnici consecutivi); D1, D2, D4, H1–H3,
`X` = 0. Pin invariati: inventario `227e5e9c…`, schedule `1acfc404…`, assegnazione finestre
`c809e79d…`, manifest di input `67e7584a…`, mappa dei prompt `b8192003…`. Inventario e schedule
non dipendono dalle costanti canary (`harness/final_inventory.py` non le importa).

## Codice

- `harness/ledger.py`: `FINAL_CANARY_QUOTA = 300` nel profilo `final_batch`;
  `CANARY_MAX_DAYS = FINAL_CANARY_QUOTA // CANARY_DAILY_CALLS` (era 7): guardia derivata dalla
  quota, non limite di calendario.
- `run_final_canary.py`: `MAX_DAYS` importa la stessa guardia; il binding dello stage copre tutti
  gli slot della quota (300) invece di 70. Nessun target esiste ancora, quindi nessun binding
  esistente cambia.
- `materialize_final_target.py`: `PROTOCOL_TAG` → `…-frozen-002`, perché l'approvazione
  dell'autore copra la revisione in vigore.
- `harness/test_final_batch.py`: 7.202 → 7.432; default del profilo ridotto 70 → 300.
- `RUNBOOK_7_4_BATCH_FINALE.md`: nota di aggiornamento e numeri.

## Secondo contenuto della revisione: modo `d9.final_target`

Rilevato in 7.4-MAT prima di qualunque esecuzione: la guardia D9 era specifica del pilot. Con
`successor_lineage`, `validate_config` autentica il pacchetto di lineage contro il ledger
dichiarato dalla configurazione, e quel pacchetto appartiene al ledger di `pilot-03`; senza
lineage pretende la riconciliazione delle quattro richieste storiche. `require_pilot_ledger`
esegue `validate_history` anche nel piano senza chiamate. Nessuna configurazione derivata dal
pilot poteva quindi aprire il ledger fresco del target finale. La suite non lo vedeva perché
`test_final_batch.py` toglie `execution_config` dai binding.

Decisione dell'autore (2026-09-18): terzo modo esplicito, solo in `harness/d9.py`:

- `d9.final_target = {artifact_version: FINAL_TARGET_1, target_id, predecessor_consumption:
  NONE_FRESH_TARGET}`, con `target_id` uguale al `pilot_id` del ledger della configurazione;
- esclusivo con `successor_lineage`, `successor_lineage_approval`, `history_reconciliation`,
  `history_approval`;
- ammesso **solo** su un ledger di profilo `final_batch`, e un ledger `final_batch` ammette solo
  questo modo; il ledger non deve portare righe di lineage, storico esterno o eventi relativi;
- il binding d'identità 122B (`identity_binding` → proposta rivista `77d72204…`, supplemento di
  qualifica `dd9c53f0…`, identità `d1800613…`) resta obbligatorio e autenticato come nel successor;
- tutto il resto di `validate_config` (ruoli, servizi documentati, tokenizer, presentazione,
  allowlist producer, approvazione d'esecuzione sulla configurazione esatta) è invariato. Nessuna
  modifica a ledger, quote o contabilità.

Test nuovo `harness/test_final_target_d9.py`: binding **reali** con configurazione D9 valida su
ledger `final_batch` (canary del giorno, passata, piano senza chiamate, guardie), più i rifiuti:
combinazione con i modi del pilot, dichiarazione che nomina un altro ledger, binding d'identità
assente, modo e profilo non corrispondenti.

## Controllo

Per decisione dell'autore nessuna review separata, per entrambi i contenuti: sono fissati prima
di qualunque dato. Il controllo è il diff visibile del codice, la suite completa rieseguita da
Luca sul Mac, il dry-run di materializzazione e il piano canary senza chiamate sul target reale;
se OK, merge in `main` e tag `studio2-fase03-protocollo-finale-frozen-002`.

Da dichiarare nel paper (metodi): canary giornaliero senza limite di giorni; la finestra di
sette giorni era solo il criterio di fattibilità pre-avvio.
