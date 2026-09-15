# Candidato locale C01–C03 — nuova verifica indipendente richiesta

15 settembre 2026. **Implementazione, non review.** Corrette le tre riproduzioni del
secondo NON OK. I controlli locali riportati sotto passano; il verdetto indipendente
su `0c8157f` resta NON OK e non viene chiuso da questa finestra. Nessun freeze o GO.

## Identità e catena della consegna

| Ruolo | Identità esatta |
| --- | --- |
| Remoto effettivo | `https://github.com/sorrentinoluca/fot-phd.git` |
| main remoto osservato prima del lavoro | `a00605862f627710347bd63c49f79a6d0a00135f` |
| Candidato respinto | `0c8157f23bee49a3a5a2df648525c34706da29d7` |
| Tree respinto | `a1573b49615a875f24ee97f9f1cd4bab399be93d` |
| Base documentale del nuovo worktree | `6268437b8b64288b50ad5f7c924e1fcab85b27d3` |
| Branch locale | `codex/studio2-harness-0310-c01-c03` |
| Commit separato di acquisizione NON OK | `b882c27103dbd9d0e0462df20731123f5ed5a0c1` |
| **Nuovo candidato tecnico esatto** | **`9e18bcbd06fa2c54202c8eeda079c112dbfcefcd`** |
| **Tree del candidato tecnico** | **`5d1fd7924c4e1e46346f367590e6aa1977a6ba75`** |
| Worktree | `/Users/luker/fot-tep-harness-0310-c01-c03` |
| Manifest tecnico v3 | `HARNESS_OFFLINE_CANDIDATE.json`, 54 file, 14155 byte |
| SHA-256 manifest tecnico | `e0b6fc2ba4752b485829b397867b5ae5ee1a7ec5356ea4d11f24e09f39b2f228` |

Questo report, il prompt nuovo, la consegna JSON e l'audit finale appartengono a un
**successore documentale**. Il loro HEAD non è il candidato tecnico da eseguire. I dati
del successore sono nel commit e non in un campo autoreferenziale dello stesso report.
Prima dei documenti il worktree tecnico risultava pulito; verificare nuovamente HEAD,
tree e stato come indicato nel prompt. L'audit allegato confronta le copie preservate.

## Acquisizione e riproduzione del NON OK

Fonte: `/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/evidence`.
Verbale e prove acquisite in
[non_ok_0c8157f_20260915/PROVENIENZA.md](non_ok_0c8157f_20260915/PROVENIENZA.md).
SHA-256 verbale `1785fb3cfb832b5a299fe885ac740a4f557ad83431e002451d447afab64f4efc`;
SHA-256 manifest originale `e5cb1589a9f8006303c9ea91a3ea37be742990c2ac6c86fb8ffc7e59fcbf7f80`.

Verificati **3.025 membri più il manifest** prima dell'uso e nuovamente prima del commit
tecnico. Copiati **324 file byte-identici**, inclusi report, matrici, script, log e nuove
fixture X01–X24; **2.702 file** di fixture replicate restano esterni, con collocazione
esatta, hash, dimensioni e motivo nell'inventario. Il commit acquisisce 328 file contando
anche inventario, provenienza, stato iniziale e script di acquisizione. Symlink dichiarati
separatamente. Nessuna normalizzazione di newline, path o spazi nei log.

Nel sandbox `before/`, con candidato esatto 0c8157f e script del revisore byte-identici:
18 prove estese → **4 failure** (X01/X02/X03/X15), **0 errori**; ulteriori 6 → **6/6**.
Confermata quindi la riproduzione dei tre difetti, senza usare l'errore iniziale di cwd
della precedente review: lo script acquisito già correggeva soltanto quei cwd.

Le nuove prove sono conservate in [c01_c03_evidence/](c01_c03_evidence/).
Sono copiati **44 file** di script/log/osservazioni; **1.891 file** di fixture rimangono
nel sandbox recuperabile `/Users/luker/fot-tep-harness-0310-c01-c03-checks`, tutti
verificati per hash e dimensioni e inventariati. Il manifest delle copie, il loro
inventario e il riepilogo aggiungono altri tre file tracciati. Gli alberi di fixture
sono deliberatamente falsi/alterati; non diventano input scientifici.

## Correzioni

### C01 / R04 — precedenza dell'alternativo

Il binding dell'alternativo avvia lo stadio opzionale. Da quel momento la sonda e il gate
richiedono la sua chiusura PASS, verificata dentro `BEGIN IMMEDIATE` sia al binding sia
alla riserva sia all'esito. INTENT, FAILED, ZERO_TOKEN_PROVEN, completamento privo di
outcome e FAIL non soddisfano il prerequisito. Non viene introdotto un abbandono implicito.

X01/X02 ora rifiutano la transizione; la CLI sonda registra **zero invii consumer** dopo
il timeout alternativo. Le regressioni verificano anche un alternativo inserito dopo
il binding della sonda ma prima del suo primo invio, e una gara reale tra due processi.
Dopo prova zero-token e retry esplicito, l'alternativo chiude 8 coppie valutabili su 9
richieste: soltanto allora la sonda procede. D9 reale non viene recepita in questo delta.

### C02 / R07 — N48 nel denominatore T3/T6

La precedente interruzione del gate era una regressione rispetto al piano rev.10 §§11–11.1,
righe 831 e 871–875 della fonte acquisita. La sostituzione precedente di N48 era **non
equivalente**. Contratto, mappa e intestazioni dei vecchi documenti lo dichiarano.

Un'eccezione osservata dal trasporto nel gate salva atomicamente FAILED e un evento
`transport_invalidity:<request_id>`. L'evento contiene un record INVALID con identità
della richiesta/campione congelato, tipo/messaggio e latenza; **raw assente**, identità
restituita e consumo token null, nessuna risposta finta. Tutti i restanti primi tentativi
proseguono; zero retry gate. Il ledger autentica l'evento, il valutatore controlla forma,
campione e triplette, quindi applica le soglie esistenti.

| Caso stub | Risultato osservato |
| --- | --- |
| Un timeout, altre 119 risposte valide | T3 119/120; una tripletta divergente; `R3_REQUIRED_PENDING_FEASIBILITY` |
| Tre timeout sullo stesso prompt | 117 valide, T3 passa ma T6 non valutabile; NO_GO tecnico |
| Sette timeout distribuiti | 113 valide, T3 fallisce; NO_GO tecnico |
| Timeout su tutti i 120 originali, via CLI | 120 INVALID, 40 triplette non valutabili; NO_GO tecnico |
| Timeout seguito da risposta con modello errato | Il raw della risposta errata è conservato e il pilot si sospende |
| Morte reale del processo dopo commit FAILED | Secondo processo riusa raw/INVALID, invia solo 118 originali restanti; totale 131 intenti |

Un crash senza osservazione durevole lascia INTENT: --resume si blocca, senza nuovo invio.
Una prova zero-token completa e approvata consente di includerlo come INVALID e di eseguire
i soli originali non ancora tentati. La prova successiva a un timeout già contabilizzato
aggiunge un evento forense separato e non cambia il record invalido né il riepilogo.
Le failure preventive delle barriere non vengono convertite in invalidità del modello.

Il formato SQLite v2 resta invariato. Non si migra né si riscrive automaticamente un
outcome del candidato precedente. FAILED v2 privo di evento nuovo richiede riconciliazione
esplicita per diventare INVALID; gli stati storici già chiusi violando C01 restano rifiutati.

### C03 / R07 — due denominatori nel producer

Il riepilogo v4 ricava `provider_requests` dal contatore durevole dello **stadio**, inclusi
errori e retry. `evaluable_calls` separa le otto coppie T9. X15 e la regressione corrente
osservano **9 invii stub = 9 intenti ledger = 9 richieste nel summary**, con 8 coppie
valutabili, 8 valide e 16 insight. Il riepilogo entra così nell'outcome e viene rigenerato
identico dopo restart/cancellazione del file, senza invio.

Gli intenti sono il denominatore contabile prudenziale: dopo un crash prima dell'invio
non dimostrano da soli che il provider abbia ricevuto una richiesta. Non vengono azzerati.

## Prove e risultati

| Controllo | Esito |
| --- | --- |
| Suite mirata | **96/96** = 82 preesistenti + 14 regressioni C01–C03 |
| Discovery completa finale | **131/131** = 117 preesistenti + 14 nuove |
| Prove originarie applicabili | **14/14**, 12 metodi invariati e 2 con gli adattamenti fixture già verificati |
| Estensioni X01–X18 sul nuovo codice | **18/18**, script letterale |
| X19–X22 e X24 | **5/5**, script letterale |
| X23 letterale | **1 failure conservata**: si aspettava l'interruzione che costituiva C02 |
| X23 riallineato al requisito del piano | **1/1**, adattamento esplicito e isolato, senza ripetere gli altri 5 |
| Compilazione sorgenti live fase03 | **90 file**, nessun errore sintattico; escluse acquisizioni/prove forensi |
| Guardiano documentale | **35 test, stessi 14 ID falliti, 1 skip — NON PASS** |
| Integrità | 54/54 file manifest; 3.026 file acquisizione e 1.935 file delle nuove prove verificati |
| Perimetro | **169 file protetti** confrontati byte per byte con la base documentale; invariati |

Il consolidamento X è **24 metodi distinti: 23 letterali + 1 adattato**, eseguiti localmente
dalla preparatrice. Non si dichiara 24/24 sullo script originario immutato. X23 originario
rimane nel log con la sua failure; il nuovo X23 mantiene il timeout su ogni invio e verifica
120 INVALID, T3/T6, prova successiva e zero reinvii. La matrice rende esplicita la
corrispondenza con N48 e con i 50 metodi originari:
[MATRICE_R01_R10_C01_C03.md](MATRICE_R01_R10_C01_C03.md).

Un primo discovery è stato fermato dopo errori di import nel nuovo modulo di test:
`harness.*` e `studio2.fase03.harness.*` duplicavano l'identità delle eccezioni. Gli import
sono stati allineati a quelli assoluti della suite; nessun assert modificato. Il log
iniziale parziale è conservato, la discovery finale 131/131 usa il test corretto. La suite
mirata aveva già caricato il namespace completo. I log intermedi 37/37 e 13/13 restano
separati dalle cifre finali. Comandi e dettagli in
[c01_c03_evidence/COMANDI.md](c01_c03_evidence/COMANDI.md) e
[c01_c03_evidence/RESULTS.json](c01_c03_evidence/RESULTS.json).

## Perimetro del diff e tracciabilità

Commit tecnico: **59 file** dopo l'acquisizione separata. Sono 6 file Python (5 modificati,
1 nuovo test), 6 documenti/manifest e 47 file di prove e inventari. Il delta coordina la
macchina a stati, il ciclo durevole, l'evaluatore e il summary; le prove e il contratto
entrano nello stesso candidato verificabile. L'acquisizione rimane nel commit precedente.

- `harness/ledger.py`: precedenza alternativa, eventi INVALID atomici/autenticati,
  raccolta record, riconciliazione gate e verifica outcome secondo T3/T6.
- `harness/runtime.py`: persistenza timeout gate e ripresa da INVALID; journal separato.
- `harness/gate_rules.py`: validazione esplicita delle invalidità senza risposta.
- `run_pilot.py`: rimosso il parametro privato inattivo return_error_record; la semantica
  del gate è obbligatoria nel runtime condiviso.
- `producer_probe.py`: conteggio tentativi dello stadio e coppie valutabili separati.
- `harness/test_c01_c03.py`: 14 regressioni, CLI, concorrenza, arresto reale e restart.
- Documenti/manifest: contratto corretto, due mappe, manifest v3 e marca storica sui due
  documenti del candidato respinto. Nessun aggiornamento anticipato del walkthrough.

I tre file del raccordo qualificato (`metric_adapter.py`, `metrics.py`,
`test_metric_raccordo.py`) sono invariati. Piano generale/statistico, APERTURA, D9,
walkthrough, 03.7/03.9/03.12, A/B, FAR e U3 non ricevono modifiche. Copia principale,
worktree precedenti e candidati del revisore sono preservati. Nessuna modifica parallela
importata. Nessun push, merge, tag, freeze, GO, chiamata API, inferenza o simulazione.

## Finestra, limiti e seguito

Preparazione implementativa: **Codex**, task `01a0a204-abda-7a00-8466-f52f5bc84812`, stessa
finestra preparatrice. Il verbale acquisito attesta `gpt-6-astra/xhigh` nella preparazione
precedente e `gpt-6-astra/high` nella finestra revisore distinta. Il modello/effort di questo
turno non sono riesposti dall'ambiente: non vengono riattestati sulla sola continuità del
task. La distinzione delle finestre non prova una diversità di modello. Runtime Python e
identità del task sono registrati in `c01_c03_evidence/runtime.json`.

D9 è già approvata: 122B producer principale e consumer; 27B libreria alternativa completa;
Terra storico interno. Il recepimento **eseguibile D9**, l'ordine reale delle label e le
qualifiche di provider, tokenizer, capienza/tempi/T5 rimangono delta separati. Il preflight
storico resta bloccato. Gli output fixture non attestano comportamento di modelli reali.

Passo richiesto: nuova verifica indipendente sul candidato tecnico esatto, usando il
[PROMPT_VERIFICA_C01_C03.md](PROMPT_VERIFICA_C01_C03.md). Nessuna nuova approvazione dei
ruoli viene richiesta e nessuna review viene eseguita o inviata a un'altra finestra qui.

## Elenco esatto dei file del commit tecnico

- `studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md`
- `studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json`
- `studio2/fase03/harness/MAPPA_RIPRODUZIONI_R01_R10.md`
- `studio2/fase03/harness/MATRICE_R01_R10_C01_C03.md`
- `studio2/fase03/harness/PROMPT_VERIFICA_CORREZIONI_HARNESS_03_10.md`
- `studio2/fase03/harness/REPORT_CORREZIONI_HARNESS_03_10.md`
- `studio2/fase03/harness/c01_c03_evidence/COMANDI.md`
- `studio2/fase03/harness/c01_c03_evidence/REPRODUCTION_INVENTORY.json`
- `studio2/fase03/harness/c01_c03_evidence/RESULTS.json`
- `studio2/fase03/harness/c01_c03_evidence/SHA256SUMS`
- `studio2/fase03/harness/c01_c03_evidence/acquire.py`
- `studio2/fase03/harness/c01_c03_evidence/add_crash_test.py`
- `studio2/fase03/harness/c01_c03_evidence/after/additional_console.log`
- `studio2/fase03/harness/c01_c03_evidence/after/console.log`
- `studio2/fase03/harness/c01_c03_evidence/after/evidence/additional_edges.py`
- `studio2/fase03/harness/c01_c03_evidence/after/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/c01_c03_evidence/after/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/c01_c03_evidence/after/evidence/extended.json`
- `studio2/fase03/harness/c01_c03_evidence/after/evidence/extended.log`
- `studio2/fase03/harness/c01_c03_evidence/after/evidence/extended_probes.py`
- `studio2/fase03/harness/c01_c03_evidence/applicable/applicable.json`
- `studio2/fase03/harness/c01_c03_evidence/applicable/applicable.log`
- `studio2/fase03/harness/c01_c03_evidence/applicable/evidence/negative_probes.py`
- `studio2/fase03/harness/c01_c03_evidence/applicable_console.log`
- `studio2/fase03/harness/c01_c03_evidence/before/additional_console.log`
- `studio2/fase03/harness/c01_c03_evidence/before/console.log`
- `studio2/fase03/harness/c01_c03_evidence/before/evidence/additional_edges.py`
- `studio2/fase03/harness/c01_c03_evidence/before/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/c01_c03_evidence/before/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/c01_c03_evidence/before/evidence/extended.json`
- `studio2/fase03/harness/c01_c03_evidence/before/evidence/extended.log`
- `studio2/fase03/harness/c01_c03_evidence/before/evidence/extended_probes.py`
- `studio2/fase03/harness/c01_c03_evidence/compile.json`
- `studio2/fase03/harness/c01_c03_evidence/discovery.log`
- `studio2/fase03/harness/c01_c03_evidence/discovery_initial.log`
- `studio2/fase03/harness/c01_c03_evidence/documentation_after.log`
- `studio2/fase03/harness/c01_c03_evidence/documentation_before.log`
- `studio2/fase03/harness/c01_c03_evidence/documentation_comparison.json`
- `studio2/fase03/harness/c01_c03_evidence/edit.py`
- `studio2/fase03/harness/c01_c03_evidence/first_regressions.log`
- `studio2/fase03/harness/c01_c03_evidence/initial_git_state.json`
- `studio2/fase03/harness/c01_c03_evidence/new_regressions_initial.log`
- `studio2/fase03/harness/c01_c03_evidence/package_evidence.py`
- `studio2/fase03/harness/c01_c03_evidence/protected_scope.json`
- `studio2/fase03/harness/c01_c03_evidence/runtime.json`
- `studio2/fase03/harness/c01_c03_evidence/targeted.log`
- `studio2/fase03/harness/c01_c03_evidence/update_manifest.py`
- `studio2/fase03/harness/c01_c03_evidence/x23_adapted/ADATTAMENTO.md`
- `studio2/fase03/harness/c01_c03_evidence/x23_adapted/console.log`
- `studio2/fase03/harness/c01_c03_evidence/x23_adapted/evidence/additional_edges.py`
- `studio2/fase03/harness/c01_c03_evidence/x23_adapted/evidence/additional_edges/additional.json`
- `studio2/fase03/harness/c01_c03_evidence/x23_adapted/evidence/additional_edges/additional.log`
- `studio2/fase03/harness/c01_c03_evidence/x23_adapted/evidence/extended_probes.py`
- `studio2/fase03/harness/gate_rules.py`
- `studio2/fase03/harness/ledger.py`
- `studio2/fase03/harness/runtime.py`
- `studio2/fase03/harness/test_c01_c03.py`
- `studio2/fase03/producer_probe.py`
- `studio2/fase03/run_pilot.py`
