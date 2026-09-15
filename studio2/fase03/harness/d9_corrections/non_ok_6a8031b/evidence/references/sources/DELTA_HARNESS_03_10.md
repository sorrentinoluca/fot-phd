# Delta da consegnare alla finestra proprietaria 03.10

Preparato il 2026-09-14; **specifica, non implementazione né approvazione del pilot**.
Destinazione: `/Users/luker/fot-tep/.worktrees/studio2-harness`, branch
`codex/studio2-harness`, HEAD letto
`51160872906feaa63c1fda5e9cf6e0fe8538fb16`, worktree pulito.
Prima di applicare, riverificare HEAD/stato e concordare l'esclusività della finestra.
Nessuna scrittura a questo worktree durante la preparazione 03.8.

Fonte normativa: piano statistico §§10–11 e decisioni storiche Allegato B;
le sole variazioni A/B sono condizionate alla registrazione di approvazione e
alla nuova revisione verificata. Non scegliere D9, non lanciare il pilot.

## Modifiche per file e punto di ingresso

| File relativo al worktree proprietario | Stato osservato | Delta necessario |
| --- | --- | --- |
| `studio2/fase03/PREFLIGHT_03_0.md`, politica retry e budget | riserva solo contabile; cronologia precedente | riportare ordine conformità→remediation eventuale→sonda→gate, riserva unica e massimi sotto; separare record storico da configurazione nuova |
| `studio2/fase03/config/pilot_preflight.json`, `determinism_policy.divergence_event` | include JSON, finish reason e byte | solo coppia parsata e validità; il resto forense |
| stesso JSON, `call_budget` | `retry_reserve_authorized=false` | rappresentare autorizzazione **limitata** B2/B2-ter, non un generico true spendibile; quota remediation 8, shared reserve 15, gate retries 0, hard stop 200 |
| stesso JSON, `candidate`/freeze | vecchio server locale 16384 e fingerprint precedente | conservare record storico; candidato API nuovo dichiarato qwen3.8-27b, 262144/32768, dati ancora da verificare; non ereditare revision/FP8, tokenizer, PID o fingerprint vecchi |
| `studio2/fase03/run_pilot.py:510`, `divergence_signature` | firma di sei campi | firma semantica `(validità, abstain, predicted_label)`; invalidità senza coppia valida con sentinella unica, dettagli grezzi conservati separatamente |
| stesso file, `run_stability_stage` da r. 523 | ogni invalidità forza NO_GO; assenza invalidità può dare PASS | valutare T3 ≥114/120, T4=0/120, copertura astensione per condizione; gruppi tutti invalidi rendono T6 non valutabile e bloccano GO |
| stesso file, `print_plan` e orchestrazione stadi | durata vecchio server e riserva flag semplice | prospetto per blocco/modello, nessuna estrapolazione di prestazioni API; macchina a stati e ledger persistente condiviso descritti sotto |
| `studio2/fase03/harness/test_harness.py` e test offline di `run_pilot` nel modulo pertinente | da aggiornare insieme al codice | casi comportamentali sotto; test solo sintetici/offline, provider simulato |

Non basta correggere `if invalid`: T3, T4, T6, T9 e prerequisiti restano gate
separati. Con ≥1 divergenza e altri controlli conformi l'esito indica
**R3_REQUIRED_PENDING_FEASIBILITY**, non GO finale né NO-GO scientifico.
T11: astensione A su local-unseen del gate; se assente, OOD comunque eseguita
come esplorativa con validità non stabilita, non blocco tecnico automatico.

## Macchina a stati e contabilità

1. Conformità: 8 richieste, 16 insight distinti; conservare ogni output e errore.
2. Unico ramo remediation prima di sonda/gate: difetto diagnosticato strutturale,
   identificatori, cap o leakage. Solo prompt producer; schema/validatore/campi
   fissi immutati. Acquisire autorizzazione scritta sul diff e congelare template.
   Rieseguire tutti gli otto casi; escludere i primi output dalle librerie.
3. Sonda 3/6/9, triplette A/B-LF/E-LF complete; congela configurazione gate.
4. Unico gate 40×3 con prompt/config/template improntati; nessun retry gate.

Contatore persistente di **ogni richiesta inviata**, condiviso fra stadi, producer,
directory e riavvii; verificare consumo storico prima di ulteriori invii. Ledger
con identificativo richiesta univoco, modello, stadio, esito, token quando esposti,
latenza e imputazione a quota; scrittura atomica prima dell'invio, crash/resume
senza azzerare o duplicare. Il nuovo alias non azzera il consumo del pilot.
Rispettare `8r+t≤15`, r∈{0,1}, senza usare gli 8 dell'alternativo per retry.
Con remediation restano 7 trasporti cumulativi; senza, 15, ma oltre il settimo
non si può più finanziare una remediation intera. Le 15 senza remediation sono
usabili nella sola conformità. La sonda non usa mai la quota 8, anche se la
remediation non è avvenuta: richiedere `trasporto_già_consumato+3≤7` prima di
ogni tripletta ripetuta, al massimo due triplette in assenza di altri consumi.
Trasporto della sonda solo
con prova zero token e tripletta completa; gate mai ripetuto. Timeout senza
prova zero token è guasto irrisolto, non difetto correggibile col prompt.
Massimi 152 senza alternativo /160 con alternativo, hard stop 200 separato.
Il ledger conserva consumo e stato anche se si sospende per esaurimento riserva.

Non creare la dipendenza «insight già conformi prima di eseguire la conformità»:
gli input di sviluppo e lo schema vengono prima; la libreria validata risultante
alimenta la costruzione dei prompt definitivi di sonda/gate. Gli eventuali fixture
autorizzati restano distinguibili e non diventano la libreria scientifica per nome.

## Test di accettazione offline da implementare nella 03.10

- byte, spiegazione, JSON accessorio o finish reason diversi con stessa coppia
  valida: nessuna divergenza; T4 resta fallibile separatamente per `length`;
- coppia diversa oppure validità diversa: divergenza; tre invalidi, anche diversi
  fra loro: T6 non valutabile, nessun GO, tre invalidità in T3;
- 114 validi passano la sola soglia numerica T3; 113 no; manca astensione in una
  condizione: T3 non completo; zero troncamenti richiesto anche con 120 validi;
- assenza astensione A local-unseen: T11 esplorativo; non altera T3/T6;
- remediation dopo gate rifiutata; seconda remediation rifiutata; template nuovo
  richiede diff autorizzato e ripetizione degli stessi otto casi;
- nessun retry automatico/gate; timeout senza prova zero token bloccato;
  sonda ripetuta solo per triplette complete entro la quota 7, anche senza
  remediation: due triplette ammesse con quota integra, la terza rifiutata;
- 8r+t=15 ammesso nei soli stadi consentiti, 16 rifiutato; nessuna appropriazione
  quota alternativa; verifica limiti 152/160 e hard stop cumulativo 200;
- riavvio, cambio directory/producer o doppio processo non aggirano ledger o budget;
- output pre-remediation mai riusato; schema/cap/leakage non modificabili;
- risultato gate R3 non autorizza esecuzione senza T5 e gli altri prerequisiti;
- fingerprint/ID cambiato sospende, capacità dichiarate senza identità verificata
  non ereditano il GO del vecchio servizio.

Le regole e soglie appartengono alla 03.8; implementazione, verifica offline,
congelamento configurazione e report del delta appartengono alla 03.10. La loro
implementazione è requisito **prima del pilot**, non un risultato prodotto da
questa finestra. A/B non eliminano 03.6, 03.7, 03.12, tokenizer/capienza,
provenienza degli input e controllo dell'identità effettiva.
