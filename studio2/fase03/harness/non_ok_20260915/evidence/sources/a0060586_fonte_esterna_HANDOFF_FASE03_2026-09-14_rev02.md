# Handoff Fase 03 — studio 2 FoT-TEP — revisione 02

**Data: 14 settembre 2026, Europe/Rome. Fase 03 ancora aperta.**

Documento di trasferimento alla nuova finestra di coordinamento, richiesto da Luca.
Aggiorna e sostituisce **come stato operativo** `HANDOFF_FASE03_2026-09-14.md`, che resta
conservato come storico. Non è un report scientifico, un verbale indipendente, una firma
dell'autore o un'autorizzazione al pilot. Preparato nella task «Fase 03 orchestrator»,
ID `01a09ef6-3bc4-7e12-90db-fa01bbe0de19`.

Fonti: file e riferimenti Git letti dai worktree indicati, consegne delle sottofasi e
aggiornamenti dell'autore in conversazione. I parametri del nuovo server sono **comunicati
dall'autore**, non verificati da questa finestra. Nessuna credenziale è contenuta qui.

## 0. Ripartenza: le informazioni che cambiano il percorso

1. **03.5 è chiusa, integrata e pubblicata.** Non rifare FAR, bootstrap, decisione dell'autore
   o verifica. Il tag finale esiste; soglia e sigillo storico sono invariati.
2. **03.9 ha già generato e verificato `normal_dev`, costruito i prototipi, pubblicato e
   riscaricato i dati e integrato il pacchetto in main.** Non rilanciare il batch.
   Resta aperta: mancano il raccordo dei nomi delle metriche nella 03.10, la raggiungibilità
   in main dei sorgenti riusati della 03.6 e il successivo tag di freeze della baseline.
3. **03.8 è alla revisione 10, verificata OK. A/B sono già approvate da Luca.** Non chiedere
   di nuovo quelle approvazioni e non applicare il vecchio tetto rigido di 3.700 come regola
   corrente. La firma materiale è ancora assente; allineamenti e congelamento sono pendenti.
4. **03.12 revisione 4 e R4-V sono OK**, con test del tokenizer sul server 26/26 senza skip.
   Il target esatto del tag è `3c64390`, non `43b31af` né un futuro merge.
5. **Evidence-v2 e verifica bibliografica sono già completate.** Mancano le rispettive
   integrazioni; non ripartire dal repackaging o dalla ricerca bibliografica iniziale.
6. **Il nuovo server 122B è stato dichiarato operativo.** API ID `qwen3.5-122b`, contesto
   131.072, output massimo 16.384, temperatura da omettere nella richiesta. Il 27B resta
   sull'altro server. Ruoli sperimentali, identità completa e qualificazione non sono
   automaticamente decisi dalla disponibilità del servizio.

Ultimo main pubblicato e verificato durante la conversazione:
`c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`.
Prima di scrivere, ricontrollare stato, ref remoto e attività concorrenti: questo è uno snapshot.

## 1. Regole di lavoro e fonti autorevoli

- Leggere [MAINTENANCE.md](/Users/luker/fot-tep/docs/MAINTENANCE.md), soprattutto §§1, 8.2–8.6,
  e i prompt in [docs/prompts](/Users/luker/fot-tep/docs/prompts): `Prompt_LLM.md`,
  `Fase_LLM.md`, `Verifica_LLM.md`, `Documentazione_LLM.md`, `Commit_LLM.md`.
- Ciclo per sottofase: esecuzione → verifica indipendente in altra finestra e con identità
  del modello documentata → correzioni e riverifica del delta → documentazione → commit,
  integrazione e pubblicazione richieste → tag solo quando i requisiti sono soddisfatti.
  Il verificatore non corregge il candidato mentre lo certifica; conserva i NON OK storici.
- La documentazione segue l'OK scientifico. Le coppie Markdown/HTML vanno aggiornate insieme.
  L'integrazione di più sottofasi deve preservare contenuti, sezioni, link e numeri di entrambe.
- Gli OK valgono per commit/impronte/perimetro indicati, non per qualsiasi futuro HEAD.
  Uno stato `pending` in un manifest storico non va cancellato per uniformarlo a un esito
  successivo: usare il record di consegna/pubblicazione o una nuova revisione prevista.
- Perimetro concordato: Fase 03 = §6.1–§6.12 più capability pilot §7.1 fino al GO/NO-GO.
  Produzione insight definitiva, protocollo finale, studio e analisi sono fasi successive.
  `REPORT_FASE03.md` e `VERIFICA_FASE03.md` si producono alla chiusura dell'intera fase.
- Primo studio e artefatti congelati intoccabili. Riuso solo nei limiti di MAINTENANCE,
  con commit, impronte, destinazione, ruolo e distinzione pre-specificato/post-hoc.
- Nessuna nuova simulazione o inferenza sperimentale è autorizzata dal presente handoff.
  I batch Simulink vengono lanciati dall'autore; le chiamate del pilot richiedono protocollo,
  configurazione, contabilità e autorizzazioni pertinenti. Non inviare messaggi all'amministratore
  del server senza richiesta dell'autore.
- Il mandato precedente «Nel frattempo chiudiamo 3.5 e 3.9» ha già portato alle pubblicazioni
  descritte sotto. Conservare le autorizzazioni già espresse nel loro perimetro; non
  trasformare questo documento in approvazione generale di altri merge, modelli o esperimenti.
- Non riaprire decisioni approvate senza un problema concreto. Se occorre una nuova decisione,
  presentare la formulazione e spiegare quale requisito resta irrisolto.
- Le indicazioni di profilo/modello nei vecchi prompt sono storiche. La scelta dell'esecutore
  va distinta dalla scelta dei modelli Qwen/Terra **oggetto dell'esperimento**.

## 2. Repository, worktree e riferimenti

Repository codice: `origin` = `https://github.com/sorrentinoluca/fot-phd.git`.
Repository dati: `https://github.com/sorrentinoluca/fot-tep-data`.

Nelle sezioni successive, `I/`, `S08/`, ecc. significano **il percorso assoluto della radice
in questa tabella seguito dal percorso indicato**; non sono directory da creare.

| Sigla | Radice assoluta | Branch / HEAD rilevato |
|---|---|---|
| R | `/Users/luker/fot-tep` | `codex/studio2-soglie-normal` / `819b12e`; molti file non tracciati |
| I | `/Users/luker/fot-tep-chiusura-035-039` | `codex/studio2-chiusura-035-039` / `c486eee`; pulito, allineato a origin/main |
| S05 | `/Users/luker/fot-tep-correzione-soglie-normal` | `codex/studio2-soglie-normal-correzioni` / `b64ff38`; integrato |
| S06 | `/Users/luker/fot-tep-evidence` | `codex/studio2-evidence` / `c66bd8d`; pulito |
| S08 | `/Users/luker/fot-tep-piano-statistico-fix` | `codex/studio2-piano-statistico-fix` / `51782e8`; pulito |
| S09 | `/Users/luker/fot-tep/.worktrees/studio2-baseline-numerica` | `codex/studio2-baseline-numerica` / `459947a`; candidato integrato, dati ignorati presenti |
| S10 | `/Users/luker/fot-tep/.worktrees/studio2-harness` | `codex/studio2-harness` / `5116087` |
| S12 | `/Users/luker/fot-tep-schema-insight` | `codex/studio2-schema-insight` / `43b31af`; prompt non tracciato conservato |
| S14 | `/Users/luker/fot-tep/.worktrees/studio2-fedavg` | `codex/studio2-fedavg` / `bfbde77`; pulito |
| S15 | `/Users/luker/fot-tep-paper-sections` | `codex/studio2-paper-sections` / `cf79e81`; pulito |
| L | `/Users/luker/fot-tep-letteratura-fase03` | `codex/studio2-letteratura-fase03` / `a572d1c`; candidato bibliografico NON committato |
| VL | `/Users/luker/fot-tep-verifica-letteratura-fase03` | snapshot di verifica, **senza `.git`** |
| V15 | `/Users/luker/fot-tep/.worktrees/verifica-paper-sections-esterna` | detached `cf79e81`; verbale finale esterno |

**Non usare R come se fosse main aggiornato.** Per i contenuti già integrati leggere I o
il riferimento Git aggiornato. Prima di nuove integrazioni coordinare un solo writer sul
worktree scelto; non effettuare checkout nella copia principale con collisioni non tracciate.

## 3. Stato di tutte le sottofasi

| ID e nome | Stato aggiornato e residuo immediato |
|---|---|
| 03.1 — Criteri di selezione | **Chiusa**, integrata e congelata con tag. |
| 03.2 — Catalogo D1 | **Chiusa**, integrata e congelata con tag. |
| 03.3 — Run fault di sviluppo | **Chiusa**, 40 run verificati; release fault-dev-v1/v2 conservate. |
| 03.4 — Perimetro codice Q8 | **Chiusa**, decisione verificata e attuata in main. |
| 03.5 — Score e soglie Normal | **Chiusa e pubblicata**, merge `98d958d`, tag finale, consegna aggiornata in `c486eee`. |
| 03.6 — Evidence 697-D e verbalizzazioni | **Completata localmente**, verifica OK, release v2 pubblicata/riscaricata, documentazione pronta. Integrare il branch. |
| 03.7 — Pseudolabel, agenti e derangement | **Chiusa**, integrata e tag pubblicato. L'ordine di presentazione nei prompt resta competenza 03.10. |
| 03.8 — Piano statistico | **Rev. 10 verificata OK**, A/B approvate. Firma, allineamenti, bibliografia, documentazione/integrazione e tag pendenti. |
| 03.9 — normal_dev e baseline numerica | **Integrata e dati pubblicati**, ma aperta; raccordo 03.10, sorgenti 03.6 in main e tag di freeze pendenti. Manifest corrente rev. 3, effective=false. |
| 03.10 — Harness API e input pilot | **Aperta**, codice offline disponibile; allineamenti, input reali, pin 03.12, metriche 03.9 e qualificazione/configurazione server da completare. |
| 03.11 — Run finali e controlli OOD | **Non avviata**; parte dopo freeze statistico 03.8, secondo la regola B approvata. |
| 03.12 — Schema degli insight | **R4-V OK**, tokenizer server 26/26, log e verbale acquisiti. Documentazione finale, integrazione e tag pendenti. |
| 03.13 — Capability pilot e GO/NO-GO | **Non avviata**; server 122B disponibile secondo l'autore, non ancora qualificato; ruoli D9 da fissare. |
| 03.14 — FedAvg, pavimento locale e soffitto centralizzato | **Pacchetto verificato OK**, verbale acquisito. Smoke reale, prove/valutazioni previste e freeze ancora pendenti. |
| 03.15 — Sezioni del paper | **Delta fino a cf79e81 riverificato OK**; acquisire verbale finale e aggiornare le dipendenze maturate prima dell'integrazione. |
| Supporto — Letteratura Fase 03 | **Verifica indipendente OK**. Candidato non committato; verbale, PNG e integrazione da acquisire/conservare. |

03.0 è il preflight/codice preliminare, non una ulteriore sottofase scientifica chiusa.
I suoi file vanno allineati nella 03.10; non costituiscono un pilot già eseguito.

## 4. Dettaglio e fonti per proseguire

### 4.1 Sottofasi chiuse 03.1–03.4 e 03.7

Fonti integrate in `I/studio2/fase03/selection/`, `fault_runs/`, `perimetro_q8/`,
`pseudolabel/`, con walkthrough corrente in `I/docs/fot_walkthrough_conversazione_studio2.md`
e `.html`.

| Tag esistente | Commit destinatario |
|---|---|
| `studio2-fase03-criteri-selezione-frozen-001` | `9faecaf7337e5864b7a3ad44cadb8971853dd260` |
| `studio2-fase03-catalogo-D1-frozen-001` | `ab43f0b20f45cdb475c0caf52c6f7afcbae50891` |
| `studio2-fase03-pseudolabel-frozen-001` | `c16b533016db4617deb1ba96853253f117e8e32b` |

Catalogo D1: F1/F2/F3/F8/F10/F13/F14/F15. Per 03.7: otto label fault opache,
`Normal` letterale, `Unknown` solo astensione. Correlazione d'ordine lessicografico/catalogo
ρ=−0,833 accettata e documentata senza nuovo sorteggio; non ridisegnare le label per questo.

### 4.2 03.5 — chiusa: riferimento per gli altri cantieri

Fonte corrente: [INTEGRAZIONE_03_5.md](/Users/luker/fot-tep-chiusura-035-039/studio2/fase03/soglie_normal/INTEGRAZIONE_03_5.md).
Cartella: `I/studio2/fase03/soglie_normal/`.

- Candidato `b64ff387b8abad063a08885ac77e8a8f9621c3a8`; merge main
  `98d958d870a10ada0d095893af9edb05a68ebc67`.
- Tag pubblicato `studio2-fase03-soglie-normal-frozen-001` sul merge sopra;
  oggetto annotato `199c71b5f49537f2d77e5e4473446ab4a5509ecd`.
- Freeze scientifico storico della soglia: commit `950714389f92e559eac922a09404742a71c74346`.
  Il tag finale è consegna del pacchetto verificato: **non retrodata quel freeze**.
- Soglia `13.623626738268857`, rango 334 su 350, regola stretta `S > threshold`.
  FAR primario 11/150; secondario 108/1500. Nessuna ricalibrazione da fare.
- Limite di tracciabilità dei file FAR già disponibili prima del freeze **accettato dall'autore**
  in `DECISIONE_AUTORE_FAR.md`. Le prove attestano identità e sequenza registrata, non
  escludono in assoluto consultazioni non registrate. Non chiamare automaticamente
  «non conforme» la sola generazione anticipata: l'handoff vincolava l'apertura analitica.
- C4 e nota N1 completati. 95,38705407% e 96,89204510% sono masse nella distribuzione
  bootstrap empirica condizionata ai 350 score, **non garanzie di copertura della popolazione**.
  Beta(17,334) ha significato teorico condizionato alle ipotesi; 17/351 non è il FAR osservato.
- Verifica correttiva e appendici OK conservate, insieme al primo NON OK e alle evidenze.
  Esecutore C4 attestato `gpt-6-astra`, high; verifica mirata `gpt-5.6-sol`, high.
- Nel merge il report cambia soltanto due rinvii alla provenienza, da §9/9.1 a §10/10.1;
  report originale verificato SHA `d6d1a533ecb4fe7c25096f05971b7ae73f47dd053a09a4f592e2265c17011756`
  recuperabile dal candidato; report integrato SHA
  `4746cf975d4b0a3ff5823a4b859b5a1611c263678b5f729b42ccbffa5e86f516`.
- Test: 8/8 PASS; guardiano 35 test, stessi 14 fallimenti, 1 skip.
  `requirements-c4.txt` e `REPRODUCIBILITY_C4.md` documentano la riproduzione senza venv esterno.

### 4.3 03.6 — integrare il pacchetto evidence già verificato

Radice S06; cartella `studio2/fase03/evidence/`; HEAD
`c66bd8dddf8e2af9dd0665ee30afd36c248b93fb`.
Commit recenti: `54bbd0c` acquisizione verbale, `bb6d9e7` release v2, `c66bd8d` walkthrough.
Leggere `REPORT_EVIDENCE.md`, `VERIFICA_EVIDENCE.md`, `DIPENDENZE_EVIDENCE.md`,
`ARTIFACT_STORAGE.json`, `PACKAGING_V2_CHECK.json`, `extract_evidence.py`, `leakage.py`.

40 run fault, 320 finestre, 1.280 file unitari più 3 controlli. Evidence-v2 conserva gli stessi
1.283 file scientifici di v1, con packaging senza AppleDouble/PAX; 1.283/1.283 riscaricati,
zero differenze. Test evidence 4/4. **Non rigenerare la release v2.**

Residuo: integrare storia, verbale e documentazione preservando gli hash del codice letto
dalla 03.9. Nel walkthrough del branch evidence la sezione è §4.5, ma nel main aggiornato
§4.5 è della 03.5: rinumerare coerentemente la evidence a **§4.6**, verificando i rinvii.
Assegnare alla provenienza il primo numero libero effettivo, oggi §12 se questa è la prossima
integrazione. Non ripristinare l'intero walkthrough vecchio sopra quello corrente.

U3 riusa N1–N5/soglie V2 per normalizzazione e flag; non li trasforma in nuovi dati di sviluppo.
Se R2 decade o cambia la baseline autorizzata, l'efficacia delle evidence va riesaminata e
gli artefatti dipendenti rigenerati secondo il contratto, non mantenuti per comodità.

Prompt storico: `R/studio2/fase03/evidence/sottofase_3_6.md`; parti su release/documentazione
sono già eseguite. Il prossimo incarico è l'integrazione del candidato attuale.

### 4.4 03.8 — revisione 10 approvata, firma e chiusura pendenti

Fonte di ingresso: [CONSEGNA_REV10.md](/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/CONSEGNA_REV10.md).
Cartella `S08/studio2/fase03/piano_statistico/`, HEAD
`51782e8c40069c0a2310afafc36907a61d517ff6`.

Commit: `f37e7e0` approvazione A/B; `6aaa5b3eebfed4ba502c25c0443caabd0051af21`
candidato rev. 10; `51782e8` acquisizione verbale e consegna.
Verifica `gpt-5.6-sol`, sessione separata su copia isolata: **OK**, 26/26 test statistici.
La rev. 10 conserva il proprio snapshot pending: il successivo verbale attesta l'OK.

File operativi più recenti:

- `PIANO_STATISTICO.md`, `PIANO_STATISTICO_FREEZE.json`, `REPORT_PIANO_STATISTICO.md`.
- `APPROVAZIONE_ADDENDUM_03_8.md`, `ADDENDUM_DECISIONI_RESIDUE_03_8.md`.
- **`DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md`**: atto da firmare; non usare la vecchia
  bozza come se fosse la firma corrente. Verificare il legame con il piano prima di sottoscrivere.
- `BUDGET_RISORSE_REV10.md`, `CONTROLLI_REV10.json`, `VERIFICA_PIANO_STATISTICO_REV10.md`.
- `COORDINAMENTO_CHIUSURA_03_8.md`, `DELTA_HARNESS_03_10.md`,
  `ACQUISIZIONE_LETTERATURA_03_8.json`: delta concreti di coordinamento.
- `PROMPT_VERIFICA_REV10.md`: verifica già eseguita; adattare solo per un futuro nuovo delta.

**Decisioni già approvate da Luca il 14 settembre 2026:** D2=8, D11 {F1,F2}+{F14,F15},
m=0,125 medio aggregato, α=0,05 unilaterale con sensibilità 0,025, gerarchia H1→H2→H3,
regole di R/invalidità/remediation, OOD condizionati F6/F4 e le due nuove decisioni:

- **A:** sostituire il tetto rigido 3.700 con conteggio completo per blocco/modello e verifica
  temporale misurata con margine 20%. Nucleo R=1: 1.728 chiamate; R=3: 5.184, **non il totale**.
  Usare la formula parametrica dell'allegato rev. 10 per il totale. Se non fattibile:
  sospensione organizzativa e decisione autore, senza ridurre automaticamente il disegno,
  aumentare automaticamente la finestra o dichiarare NO-GO scientifico. Hard stop pilot 200 invariato.
- **B:** congelare candidati OOD, criteri e catene prima della generazione; controlli tecnici
  in 03.11 **dopo il freeze statistico e prima delle chiamate sui test**. Non reintrodurre
  la dipendenza circolare «03.11 necessaria prima del tag 03.8».

Regole pratiche da non perdere: sonda ripetibile solo per trasporto documentato/zero token,
per tripletta completa e preservando la quota remediation; nessun retry del gate;
validità mista nella tripletta è divergenza; tre invalidi rendono T6 non valutabile e bloccano
il GO tecnico. Timeout senza prova di zero token = guasto tecnico irrisolto, non remediation
del prompt. Una remediation sul solo prompt producer richiede il diff autorizzato e ripete
gli otto casi, senza riusare gli output sostituiti.

**Residui:** firma materiale; bibliografia/PNG acquisiti; allineamento piano generale,
APERTURA, preflight e harness; verifica del delta integrato; documentazione MD/HTML;
pubblicazione in main e tag `studio2-fase03-piano-statistico-frozen-001`.
Fattibilità reale, D9 e qualificazione del servizio restano operativi. Le formule
«se A/B approvate» nei documenti preparatori sono ormai soddisfatte: prevale la rev. 10.

### 4.5 03.9 — pacchetto integrato; completare solo i residui

Fonte corrente: [CONSEGNA_INTEGRAZIONE_03_9.md](/Users/luker/fot-tep-chiusura-035-039/studio2/fase03/baseline_numerica/CONSEGNA_INTEGRAZIONE_03_9.md).
**Usare I per manifest/stato correnti**, S09 per gli artefatti grandi locali ignorati.

- Candidato `459947af892e33ed23a8bdf998db49aabf923c68`; OK indipendente sul contenuto
  `ba1a206e1fe31c062d5491b4fb821ff925149982` (identità dichiarata nel verbale: Codex GPT-5,
  sessione `/root/verifica_039`; non inventare un'identificazione più precisa).
- Merge `5bd1648c54a0673ebd66df3655cf8258dfa48d3b`; pubblicazione/metadati correnti `c486eee`.
- `BASELINE_FREEZE_rev003.json`: `effective=false`, nessun tag; preserva rev. 2 e storico.
  SHA corrente `0312f416dfdbaf8984b2063df2c2e9d00e1737321b9a65dd7e32b0295a937ec8`.
- Lotto `runs/normal_dev_001`: 40 run validi, stream 60000–60039, 320 finestre.
  Evidence nella **destinazione riuscita `evidence/normal_dev_002`**: 320 unità da 697 componenti.
- Prototipi: 9 globali, 16 locali. Ricalcolo indipendente dei 25 vettori con differenza zero.
  Media aritmetica, L1 media, pareggio assoluto 1e-12 → astensione, nessuna soglia di distanza
  e nessun ripiego globale per classi assenti nel modello locale.
- Otto esempi Normal deterministici: primo run locale, prima finestra [25,30), uno per agente.
  `NORMAL_DEV_HANDOFF.json` è già accettato dal parser 03.10, ma non basta a completare il pilot.
- Deviazioni del pathname e della tracciabilità comando/MATLABPATH già accettate dall'autore,
  senza convertirle in conformità. Lo stato di origin/main al lancio non è attestato da quell'OK.
  Warning del buffer accettabile per il lotto/configurazione normal ispezionati; non è una
  garanzia scientifica generale né un'estensione a ERT/GRT/embedded.
- 10/10 test PASS. Release normal-dev-v1 già pubblicata e riscaricata, 1.336/1.336 file.

File chiave in `I/studio2/fase03/baseline_numerica/`: `REPORT_BASELINE_NUMERICA.md`,
`VERIFICA_BASELINE_NUMERICA.md`, `SPECIFICA_NORMAL_DEV.md`, `SPECIFICA_BASELINE_NUMERICA.md`,
`AUDIT_NORMAL_DEV.json/.md`, `DECISIONE_ACCETTAZIONE_NORMAL_DEV.md`,
`SIMULATOR_WARNING_CHECK.json`, `PROTOTYPES.json`, `PROTOTYPES_MANIFEST.json`,
`BASELINE_CHECK.json`, `NORMAL_DEV_HANDOFF.json`, `INTERFACE_CHECK.json`,
`ARTIFACT_STORAGE.json`, `VERIFICA_RISCARICAMENTO_NORMAL_DEV.json`, manifest rev. 3.

**Tre residui di chiusura:**

1. 03.10 adotta e testa `accuracy`→`accuracy_all`, `n`→`total`,
   `abstentions`→`abstained`; gestisce esplicitamente `non_abstained` e `invalid`.
   Il solo confronto in `INTERFACE_CHECK.json` non è adozione del raccordo.
2. Integrare i sorgenti 03.6 e le dipendenze necessarie alla riproduzione, come MAINTENANCE §8.5.
   La release evidence-v2 conserva i dati, non sostituisce i sorgenti in main.
3. Dopo controlli/verifiche pertinenti e raggiungibilità del candidato finale, pubblicare il
   tag della baseline e registrarne l'efficacia in una revisione successiva. Non confondere
   il tag della **release dati** con il tag di **freeze della baseline**.

Non serve attendere l'intera esecuzione del pilot per risolvere il raccordo di interfaccia;
va però implementato e verificato nella finestra proprietaria 03.10, senza anticipare
un GO del pilot. Non spostare un tag esistente e non inventare oggi il target del futuro tag.

### 4.6 03.10 — harness: lavoro residuo concreto

Radice S10, HEAD `51160872906feaa63c1fda5e9cf6e0fe8538fb16`.
Leggere `studio2/fase03/harness/REPORT_HARNESS.md`, `SPECIFICA_HARNESS.md`,
`INTEGRATION_STATUS.json`, `HARNESS_FREEZE.json`, oltre al delta 03.8 citato sopra.
Prompt storico `R/studio2/fase03/harness/sottofase_3_10.md`: non eseguirlo senza aggiornare
dipendenze, modello e regole alla situazione corrente.

- Aggiornare i pin dell'adapter al contratto 03.12 R4 e alle sue fonti esatte.
- Recepire il raccordo delle metriche 03.9, con test di semantica e conteggi.
- Collegare gli otto esempi Normal reali e gli input di sviluppo verificati.
- Distinguere input della conformità producer dalla libreria validata che la conformità
  produce: non creare il ciclo «servono insight già conformi per fare la conformità».
- Completare i manifest reali di sonda/gate, ordine di presentazione delle label e capienza
  sul tokenizer/configurazione **del modello effettivamente scelto**, senza ereditare il vecchio GO.
- Applicare `S08/studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md` e rev. 10 a `run_pilot.py`, preflight/config,
  test e ledger. Il documento cita ancora il precedente alias del server nuovo: §5 di questo
  handoff aggiorna il solo inventario disponibile; D9 resta una decisione distinta.
- Contare persistentemente ogni invio attraverso stadi, riavvii, directory e producer.
  Riserva unica: `8r+t≤15`, remediation r∈{0,1}; quota alternativa distinta. Sonda: quota
  trasporti massima 7 anche senza remediation, per triplette; gate mai ripetuto.
  Massimi pianificati 152/160 secondo presenza dell'alternativo; hard stop 200 separato.
- Divergenza: validità e coppia `(abstain, predicted_label)`; byte/spiegazioni/finish reason
  restano forensi, con troncamento valutato separatamente. T3≥114/120 più coperture richieste,
  T4=0 troncamenti; T6 non valutabile con una tripletta tutta invalida; R3 non dà GO automatico.

Le proposte 1a/1c del vecchio harness non vanno approvate entrambe per analogia:
l'ordine conformità→remediation→sonda→gate è ormai recepito in 03.8; la decisione specifica
sull'ordine delle label va cercata e, se non registrata, sottoposta all'autore.
Verifica offline sul delta finale; integrazione coordinata dei file condivisi in commit separato.

### 4.7 03.11 — run finali e OOD

Non avviata; prompt operativo ancora da scrivere sul piano statistico congelato.
D2=8: **64 fault + 8 Normal = 72 primari; +6 OOD +11 scorte =89 run** per il lotto
con due OOD selezionati. Le scorte sostituiscono, non aggiungono osservazioni.

Secondo B: congelare prima criteri/candidati/catene; dopo il tag 03.8 verificare generabilità,
assenza di trip e ammissibilità tecnica prima delle chiamate sui test. F6/F4 non sono
tecnicamente qualificati dalla sola verifica PHM. Catene: **F6→F5→F12; F4→F11→F5**.
Ogni sostituto va verificato autonomamente; i due OOD devono essere distinti. Se entrambe
le catene portano a F5, sospendere e chiedere una decisione, non contarlo due volte.

Stream/seed da rendere disgiunti dai lotti esistenti: 1000–1009, 2000–2099,
10000–10349, 20000–20149, 30000–30039, 40000–40349, 49900–49901,
50000–50149, 60000–60039; verificare inventario corrente, non usare l'elenco come allocatore.
Generazione dall'autore, audit solo tecnico, sigilli, conservazione e verifica del lotto.
Tag previsto del lotto: `studio2-fase03-test-v1`. Nessuna selezione su prestazioni.

### 4.8 03.12 — pronta per documentazione, integrazione e tag esatto

Radice S12, HEAD `43b31afc1ff271594cb4bd21a39fa4469a8c83bc`.
**Usare il prompt già aggiornato:**
[integrazione_tag_3_12_prompt.md](/Users/luker/fot-tep-schema-insight/studio2/fase03/schema_insight/integrazione_tag_3_12_prompt.md).

- Implementazione/target tag: `3c64390bc4dd58c48cc4e1e388a38989b32b3143`.
- `SCHEMA_FREEZE.json`: contratto rev. 4, manifest rev. 5, 18/18 voci verificate;
  SHA `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`.
- `TEST_RESULTS_qwen_rev004.txt`: 7.459 byte, SHA
  `a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972`.
  È **trascrizione del terminale fornita dall'autore**, acquisita byte-identica dall'allegato,
  non il file originale riscaricato dal server. Evidenza supplementare esterna al manifest.
- `VERIFICA_SCHEMA_INSIGHT_rev004.md`: 21.288 byte, SHA
  `d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e`.
  R4-V OK, precedente rilievo sull'indipendenza chiuso, NON OK precedente preservato.
- Esecutore R4 attestato dal prompt: `gpt-5.6-sol`, medium, task
  `01a09f1b-a581-7c41-a1ec-87912c8896ef`; revisore Claude `claude-fable-5-1`,
  sessione `session_01Y11UC227qhEvrbQxjzRpzK`, con limiti d'identificazione nel verbale.
- Test locali 25 PASS +1 SKIP; prova server 26/26 senza skip, circa 5 secondi.
  Questa è qualifica dei test/tokenizer, non capienza del futuro pilot né prova sul nuovo 122B.
- `context_check`: otto owner opache e assegnazione esatta, `normal_label == "Normal"`;
  niente owner Normal, varianti di maiuscole/spazi o sentinel opaco. Nessun insight per Normal.

Non creare rev. 6 solo per acquisire il log. Conservare R4 e manifest rev. 5 byte-identici;
documentare successivamente integrazione e pubblicazione. Tag proposto
`studio2-fase03-schema-insight-frozen-001` **esclusivamente su 3c64390** dopo che storia,
evidenze e documentazione sono raggiungibili da origin/main. Target `e058cb0` superato.
Per 03.10, nuovo hash `validator.py`:
`cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508`.

### 4.9 03.13 — pilot non avviato

Le specifiche vecchie puntano al 27B locale; il nuovo 122B non sostituisce automaticamente
quel candidato nel protocollo. Individuare decisione D9, identità/configurazione, tokenizer,
capienza, input e contabilità prima degli invii.

Ordine corrente: input di sviluppo e schema congelati → conformità producer (8 richieste,
16 insight) → eventuale unica remediation autorizzata → prompt definitivi/capienza →
sonda 3/6/9 → freeze configurazione → unico gate 40×3 → validità, troncamento, divergenza,
latenza → fattibilità T5 e altri requisiti → GO/NO-GO. Producer alternativo solo dopo D9.

La generazione dei test 03.11 non è input del pilot di sviluppo. Il pilot non autorizza
automaticamente le chiamate dello studio finale. Le vecchie stime di durata 3–9 ore
non valgono per il nuovo server: vanno misurate sulla configurazione scelta.

### 4.10 03.14 — verifica acquisita, lavoro sui dati reali ancora da fare

Radice S14, commit acquisizione `bfbde772bf14c496ff0b255008904d3deb424e54`, parent e
oggetto dell'OK `d56354934d2b5f88dace3f9b312fcf64ce3cf42b`.
`studio2/fase03/fedavg/VERIFICA_FEDAVG.md`: 33.761 byte, SHA
`57784bf2ff7e8d7d8143bdf7efa29256f44384939a56139b5999f21b0281f11b`.
Leggere anche `REPORT_FEDAVG.md`, `SPECIFICA_FEDAVG.md`, `FEDAVG_FREEZE.json`.

R1/R2 del revisore chiusi; 11/11 test, loader fault 320×697/40 cluster, smoke su fixture
byte-identico. **Non è uno smoke TEP reale né un freeze efficace.**
Il report dice ancora che normal_dev non è pubblicato: ora quel motivo è superato.
Prima dello smoke reale verificare interfacce e disponibilità dei due bundle; trattare
lo sbilanciamento 320 Normal contro 40 finestre per fault nella ricetta autorizzata.
Non cambiarla per ottenere prestazioni migliori. Valutazioni finali dopo 03.11 e condizioni
statistiche; documentazione, integrazione e freeze secondo perimetro verificato.

Prompt storici: `R/studio2/fase03/fedavg/sottofase_3_14.md`, `verifica_3_14_prompt.md`.
L'acquisizione del verbale è già eseguita, non va ripetuta.

### 4.11 03.15 — riverifica già OK, da acquisire e allineare

Radice S15, HEAD `cf79e81f917c7969dfd375e38db54315c28d4c07`.
Cartella `studio2/fase03/paper_sections/`: `REPORT_PAPER_SECTIONS.md`, `PIANO_SEZIONI.md`,
`related_work.md`, `method.md`, `verbalizer.md`, `protocol.md`, `threats.md`, lint.

Verbale **finale esterno**:
[VERIFICA_PAPER_SECTIONS.md](/Users/luker/fot-tep/.worktrees/verifica-paper-sections-esterna/studio2/fase03/paper_sections/VERIFICA_PAPER_SECTIONS.md),
13.949 byte, SHA `8faca80c87071d87bf66d97848c290a5724f6569be6f6040cfb6568bad022cb1`.
Conferma cf79e81; il report del branch contiene ancora la richiesta storica di riverifica.
Non confonderla con una riverifica ancora da fare sullo stesso delta.

Correzioni: otto label fault opache + Normal letterale; Unknown solo astensione; D9.1
conserva producer-swap con identità alternativa `[DECISIONE]`; pilot previsto, non eseguito;
27B non chiamato «nuovo». Lint 5 file senza rilievi; guardiano invariato.

Residui: acquisire verbale byte-identico e registrare lo stato; aggiornare protocollo e
verbalizzatore con normal_dev reale e le decisioni statistiche effettivamente maturate.
Il vecchio residuo «verificare 03.5» è superato. D9/ruoli e risultati non vanno inventati;
ogni nuovo delta scientifico richiede propria verifica. Documentazione e integrazione,
senza anticipare risultati, abstract o conclusioni. Prompt storico `R/studio2/fase03/paper_sections/sottofase_3_15.md`.

### 4.12 Letteratura — candidato e verifica pronti, ma non committati

Sorgente L; report `docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md`.
Verbale indipendente:
[VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md](/Users/luker/fot-tep-verifica-letteratura-fase03/docs/lit_review/VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md),
`gpt-5.6-sol`, **OK**, 30.107 byte, SHA
`551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`.

- PHM: F6 FDR 100/99/100% per DAE/T²/SPE; F4 100/18/100%. Risultati circoscritti ai metodi.
- F9–SPE nella fonte è **5,6%**, registro storico congelato **6,6%**: discrepanza nell'addendum,
  non correggere retroattivamente il registro congelato.
- Nove riferimenti controllati entro i limiti documentati. Yin: metadati/abstract verificati,
  numeri non verificati nel testo integrale. Corpus 128 voci e 40 schede; sette coppie PDF/MD.
- H e D1 preservati. L'OK bibliografico non approva OOD, fattibilità tecnica o statistica.

Inventario `S08/studio2/fase03/piano_statistico/ACQUISIZIONE_LETTERATURA_03_8.json`:
**23 file, 6.407.129 byte**, 21 non ignorati (4 modificati +17 nuovi) e **2 PNG ignorati**.
Ricontrollare le 23 impronte prima del commit; la base Git a572d1c da sola NON identifica
il candidato non committato. Acquisire il verbale in commit separato, preservandone i byte.
Conservare i PNG in sede recuperabile verificata, non limitarsi a registrarne gli hash.

PNG da preservare in `L/papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/`:

| File | Byte | SHA-256 |
|---|---:|---|
| `page-6.png` | 286.075 | `0d4174ce35e88e941540b722ff1d632b5a0ed6527f66aeed7d2089eb6d4f2bf8` |
| `page-7.png` | 557.127 | `020f08386172d87c5ca45fecabc30a402904498bbb60754a745a4520104bed91` |

Integrare gli hunk di `docs/letteratura.md/.html`, blueprint e `papers/README.md` sul main
corrente. Non importare interamente lo snapshot VL e non sovrascrivere aggiornamenti successivi.

## 5. Server e modelli: inventario, non decisione D9

### Vecchio server — accesso root disponibile all'autore

L'autore ha fornito l'ispezione di due processi, PID storici 554919 e 690460:

- modello dichiarato dal comando: `Qwen/Qwen3.8-27B-FP8`;
- `--revision 017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`;
- `--served-model-name fot-exp2-consumer`.

I PID sono uno snapshot, non identificatori persistenti. Configurazione locale del pilot
precedentemente documentata: `http://127.0.0.1:8001/v1`, max-model-len 16.384;
verificare processo e fingerprint correnti prima dell'uso. Per i test R4 l'autore si è
collegato da **Windows con PuTTY/OpenSSH**, non da questo Mac. Non presumere SSH già
configurato sul Mac; evitare istruzioni che suppongono file presenti su entrambi i computer.

### Nuovo server — solo API

Ultima comunicazione dell'autore: **«Up and running»**. Modello annunciato in avvio
`Qwen3.5-122B-A10B-FP8`; alias esposto e limiti comunicati:

| Parametro | Valore comunicato |
|---|---|
| Base URL | `http://cygnusx1.portici.enea.it:8000/v1` |
| Model ID API | `qwen3.5-122b` |
| Context Window | 131.072 token |
| Max Output | 16.384 token |
| Temperature | **Omettere il parametro**: default server dichiarato 0,6; non inviare stringa vuota o null per rappresentare l'omissione |
| Immagini | Supportate secondo il gestore; l'esperimento non diventa multimodale per questo |
| Browser use | Non supportato |
| Prompt cache | Non disponibile secondo il gestore; non presumere riuso del prefisso o relativo risparmio |
| Quota d'uso | Gestore: «non hai limiti di utilizzo in token»; non elimina limiti per richiesta, tempi, concorrenza o contabilità sperimentale |

**API key deliberatamente omessa.** Era stata condivisa una credenziale in conversazione;
non copiarla in file, prompt, commit o output. Usare la gestione dei segreti del progetto.
Nessuna connessione o inferenza è stata eseguita da questa finestra sul nuovo endpoint.

Da acquisire come metadati: repository esatto dei pesi, revisione, quantizzazione effettiva,
tokenizer/template, versione e configurazione del serving, budget effettivo input+output,
comportamento thinking/output, errori/troncamenti e stabilità del servizio. L'alias da solo
non certifica FP8 o revisione; l'accesso API non equivale ad accesso ai pesi o alla macchina.

**Superato:** il nuovo server non va più descritto come qwen3.8-27b con 262144/32768.
Il modello 2.4T `Qwen/Qwen3.8-2.4T-A95B` è stato dichiarato non ospitabile dalla macchina;
non mantenerlo come risorsa disponibile o prerequisito che sta per arrivare.

L'autore vuole comprendere il confronto tra risultati storici Terra, 27B e nuovo modello.
Non risulta ancora formalizzata qui la scelta finale di producer principale, alternativo,
consumer, ruolo dei dati storici e condizioni comparabili. Non assumere che due server
significhino tre modelli distinti o che 122B sia scientificamente migliore per dimensione.
Decidere e registrare D9 prima di modificare configurazione canonica e lanciare le prove.

## 6. Piano di prosecuzione in cinque blocchi

È un piano di dipendenze, non una barriera che impone di attendere tutto il blocco per
avviare un ramo indipendente. I task possono preparare/verificare file in worktree distinti;
**merge, PROVENIENZA e walkthrough condivisi devono essere seriali**.

### Blocco 1 — consegne mature e decisioni ancora necessarie

- **Integrazione 03.6:** candidato c66bd8d, con rinumerazione documentale e sorgenti in main.
- **Documentazione/integrazione/tag 03.12:** prompt R4 già pronto; tag su 3c64390.
  Preparazione verificabile in parallelo alla 03.6, integrazioni sullo stesso main in sequenza.
- **In parallelo:** firma materiale 03.8; acquisizione/commit del candidato Letteratura e
  conservazione PNG; inventario verificabile del nuovo endpoint e decisione D9 da sottoporre
  all'autore. Le approvazioni A/B e FAR non sono domande da rifare.
- **In parallelo:** acquisizione della riverifica 03.15 già esistente, senza nuovo giro sullo
  stesso commit; preparazione degli allineamenti che hanno fonti ormai disponibili.

### Blocco 2 — raccordo minimo 03.10 e chiusura effettiva 03.9

- Nel worktree 03.10, implementare/testare il raccordo delle metriche; preservare semantica
  dell'astensione e denominatori. Non presentare questo delta come chiusura dell'intero harness.
- Con i sorgenti 03.6 in main, raccordo verificato e riferimenti stabili, completare il
  record di freeze 03.9 e pubblicare il relativo tag secondo le verifiche richieste.
- In parallelo: aggiornare i pin 03.12 e gli input reali 03.10; preparare smoke reale 03.14
  sui bundle verificati e allineamenti paper 03.15. Qualunque esecuzione rispetta i propri
  prerequisiti; lo smoke non è una valutazione sui run finali.

### Blocco 3 — piano statistico e harness coerenti

- Bibliografia acquisita + firma rev. 10 → allineamenti piano generale/APERTURA e regole
  preflight/harness → verifica indipendente del nuovo delta → documentazione → integrazione
  e pubblicazione → tag del piano statistico. Non riproporre una rev. 8 o rev. 9 come finale.
- Il lavoro implementativo 03.10 può procedere in parallelo nel suo worktree, ma le revisioni
  devono essere rese coerenti prima delle prove del pilot; nessuna modifica simultanea dei
  file condivisi da parte di due finestre.
- Definire configurazione del modello effettivo, identità, tokenizer/capienza, ledger,
  input e condizioni D9. Il servizio disponibile non sostituisce queste verifiche.

### Blocco 4 — due rami operativi distinti

- **03.11:** dopo tag statistico, specifica/stream del lotto finale → batch dell'autore →
  controlli tecnici OOD/scorte → audit, sigilli e conservazione. Nessuna analisi prestazionale.
- **03.13:** dopo input/schema/configurazione e harness conformi, catena del pilot e
  GO/NO-GO secondo §4.9. I dati test 03.11 non sono input del pilot di sviluppo.
- I rami possono avanzare in parallelo se le risorse lo consentono; nessun trasferimento
  di risultati test nel pilot e nessuna scelta di disegno successiva a una chiamata sui test.

### Blocco 5 — completamento dei cantieri e chiusura Fase 03

- Completare 03.14 e 03.15 nei rispettivi perimetri e dopo i relativi prerequisiti;
  distinguere risultati ancora futuri da specifiche/bozze già verificabili.
- Consolidare tutte le condizioni e il GO/NO-GO; scrivere report di fase come indice delle
  consegne, poi verifica indipendente di coerenza fra sottofasi senza rifare calcoli già validati.
- Documentazione di fase, report e verifica in origin/main, dati conservati e verificati.
  Solo allora la Fase 03 è chiusa; le fasi successive non partono dal solo elenco di stato.

**Cammini aggiornati:** per chiudere 03.9, integrazione 03.6 + raccordo 03.10 → tag 03.9.
Per il pilot, 03.6/03.7/03.12 + regole 03.8 recepite + scelta/configurazione modello → 03.10 → 03.13.
Per i test finali, firma/bibliografia/allineamenti 03.8 → tag 03.8 → 03.11.
La precedente catena «03.12 R4 → lancio normal_dev» è già stata eseguita e non va ripercorsa.

## 7. Decisioni dell'autore: cosa chiedere e cosa è già deciso

| Tema | Stato / comportamento della nuova finestra |
|---|---|
| Accettazione FAR 03.5 | Già approvata e pubblicata. Non riaprire. |
| Deviazioni normal_dev 03.9 | Già accettate nel perimetro registrato. Non estenderle a prove mancanti o altra modalità simulativa. |
| A/B, D2, margine, alpha, gerarchia, D11, politica R | Approvate e recepite rev. 10. Non chiedere nuova approvazione delle stesse formulazioni. |
| Firma materiale 03.8 | Ancora necessaria. Usare atto rev. 10 e hash corretto del piano; non firmare per Luca. |
| D9: ruoli 27B/122B/Terra e confronto storico | Da formalizzare sulla disponibilità aggiornata. Il confronto con il vecchio esperimento non è automaticamente un braccio controllato del nuovo. |
| Ordine delle label nei prompt, proposta 1a | Cercare un'approvazione specifica; se manca, porre la decisione concreta. Non rifare il sorteggio 03.7. |
| Fattibilità R=3/calendario | Regola approvata; esito operativo da misurare. Se non fattibile, sospensione e decisione organizzativa dell'autore. |
| OOD F6/F4 | Candidati e catene fissati condizionatamente; esiti tecnici demandati a 03.11. Eventi fuori regola richiedono decisione, non sostituzioni arbitrarie. |
| Nuovi invii API/simulazioni | Nessuno autorizzato dal solo handoff. Applicare mandato, stadi e contabilità del protocollo. |

## 8. Integrazione, file esclusi e conservazione

### Numerazione attuale e merge

In I/main: `PROVENIENZA.md` §9 = 03.7, §10 = 03.5, §11 = 03.9. Le integrazioni successive
usano il primo numero libero, **non i numeri previsti dall'handoff originale**.
Walkthrough: §4.1 criteri, §4.2 D1, §4.3 fault, §4.4 Q8, **§4.5 soglie**, §4.7 pseudolabel,
§4.9 baseline. Riservare coerentemente §4.6 alla evidence e §4.8 al piano, verificando sempre
il target reale. La documentazione già chiusa non va persa nei conflitti di appendice.

Non modificare report/manifest verificati per correggere lo stato storico salvo delta necessario
e tracciato; conservare lo snapshot di origine e chiarire quali hash si riferiscono a quale commit.
Per 03.12 il prompt richiede esplicitamente byte invariati del pacchetto e record successivo.

### File da non committare o eliminare incidentalmente

- In R: numerosi `sottofase_*.md`, `*_prompt.md`, bozze e copie di report sotto le cartelle
  delle sottofasi, oltre a vecchio handoff/APERTURA non tracciati. Non fare `git add .`.
- `R/studio2/fase03/soglie_normal/runs/normal_001/`: 500 workbook; esclusioni aggiunte nel
  nuovo main, ma R è ancora sul vecchio branch e può mostrarli come non tracciati.
- Runtime del batch, dati grandi, evidence e conservazione 03.9: ignorati; preservarli
  e recuperarli dalle release quando necessario. La presenza locale non basta alla consegna.
- `studio2/fase02/simulator/matlab/MultiLoop_mode1.mdl.autosave`: non committare.
- `S12/studio2/fase03/schema_insight/sottofase_3_12_verifica.md`: prompt non tracciato preesistente da preservare.
- PNG Letteratura: due file specifici da conservare, non cancellare con pulizie di directory.
- Worktree di verifica esterni/detached e `/sessions/...` locked/prunable: non rimuoverli
  per fare ordine prima di aver acquisito tutte le prove necessarie.

Non effettuare checkout di main nella copia principale per risolvere collisioni eliminando
i file. Usare I, se libero e aggiornato, o un nuovo worktree. Non eliminare lock finché
non è provato che siano orfani e nessuna operazione Git sia in corso.

Rimozioni worktree/branch: soltanto dopo integrazione, conservazione degli ignorati e controllo
di non utilizzo da altre task. Nessuna rimozione è stata fatta nella chiusura 03.5/03.9.

### Release da preservare

| Lotto / release | Archivio / prova |
|---|---|
| [fault-dev-v1](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-fault-dev-v1) e [fault-dev-v2](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-fault-dev-v2) | Già pubblicati; fonti in `I/studio2/fase03/fault_runs/ARTIFACT_STORAGE.json`. Non rigenerare per pulizia storica. |
| [normal-v1](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-normal-v1) | 943.793.152 byte; SHA `bbcfd0c43a5fbda624deba62fea746150dda4a6d649e6372b8e118270277ac1d`; 515/515 payload verificati nella verifica acquisita. La chiusura 03.5 non ha ripetuto il download. |
| [evidence-v2](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-evidence-v2) | 62.185.472 byte; SHA `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf`; 1.283/1.283 file, 61.208.618 byte, zero differenze/PAX/AppleDouble. V1 preservata. |
| [normal-dev-v1](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-normal-dev-v1) | 151.500.800 byte; SHA `eef69b42d8506c993ac45d77208df982d138b4354d7d4134bd67ba421dc91a03`; 1.336/1.336 file, 150.575.225 byte, zero differenze/PAX/AppleDouble. Archivio e checksum separato, prova di riscaricamento in main. |

Asset già pubblicati immutabili. Nuove revisioni di packaging non riscrivono le vecchie.
Le directory `/tmp` dei download/verifiche e il venv `/tmp/fase03-035039-venv` sono temporanei,
non dipendenze permanenti della riproduzione; usare requisiti e prove committate.

## 9. Verifiche e rischi ancora aperti

- Guardiano `docs/test_explanation.py`: **35 test, 14 fallimenti preesistenti, 1 skip**,
  stessi identificativi prima/dopo le ultime integrazioni. Non chiamare tutto PASS né
  attribuire quei 14 fallimenti al nuovo delta senza confronto. Per la prossima modifica
  confrontare anche gli identificativi/subtest, non il solo conteggio.
- Ultimi test qualificanti: 03.5 8/8; 03.9 10/10; 03.8 26/26; schema R4 server 26/26;
  FedAvg 11/11; evidence 4/4. Sono risultati dei perimetri dichiarati, non test della Fase 03 completa.
- Ultima integrazione: controllati byte dei file scientifici e verbali, 9 impronte sorgente
  del manifest 03.9, 2 evidenze supplementari, parità numerica MD/HTML, sezioni/anchor e link nuovi.
  Il controllo dell'integratore non è una nuova review scientifica indipendente.
- Python di sistema e ambienti possono avere pacchetti assenti o conflitti arm64/x86_64
  (`rpds` già osservato). Distinguere fallimento d'ambiente da fallimento del prodotto;
  registrare interprete e dipendenze, evitare falsi PASS o SKIP che cancellano il problema.
- Codice 03.6 ancora fuori main è un limite concreto di riproducibilità 03.9, anche con dati
  già pubblicati. La rev. 3 lo registra; non eliminarlo perché il lotto è integro.
- 03.8: la disponibilità API senza quota non prova latenza, riproducibilità, finestra operativa,
  capienza, stabilità della revisione o fattibilità R3. I massimi per richiesta restano limitati.
- Il vecchio schema di pilot, i riferimenti a Qwen-2.4T e i vecchi conteggi nei documenti
  generali sono da allineare; non correggere indiscriminatamente le sezioni storiche.
- Le date del 17 settembre per D9/GO e del 30 settembre citate nei documenti precedenti
  sono riferimenti di calendario storici da confermare rispetto al piano operativo corrente;
  non inventare proroghe o nuove durate.
- F6/F4: evidenza bibliografica non dimostra generabilità; fallback autonomi e distinti.
  Con 6 OOD si tratta di una sonda, non di una caratterizzazione generale delle prestazioni.
- Dipendenza U3 e sbilanciamento di sviluppo restano limiti metodologici da dichiarare.
  Nessuna riqualificazione di N1–N5 come nuovi esempi Normal.
- Nel branch evidence esiste un rinvio storico a `../tep_heldout_phase_summary.md` segnalato
  mancante; in main 03.5 il collegamento F6 è stato corretto in `b64ff38`. Preservare la
  correzione corrente e controllare i link del merge, senza copiare il vecchio errore.
- Non confondere «completata localmente», «OK indipendente», «integrata», «pubblicata» e
  «freeze efficace». È la distinzione essenziale rimasta per 03.6/03.8/03.9/03.12/03.14.

## 10. Messaggio per aprire la nuova finestra

```text
Stiamo proseguendo lo studio 2 FoT-TEP, Fase 03.
Leggi /Users/luker/fot-tep/studio2/fase03/HANDOFF_FASE03_2026-09-14_rev02.md.
È l'handoff aggiornato: sostituisce lo stato del precedente documento, non le fonti scientifiche.
Leggi le regole e le consegne pertinenti; verifica branch, worktree e origin/main prima di scrivere.
Non rilanciare attività già completate e non riaprire approvazioni A/B o FAR già registrate.
03.5 è chiusa; 03.9 è integrata e pubblicata nei dati ma ha ancora i residui indicati.
Il nuovo server API 122B è dichiarato operativo, ma D9 e la qualificazione non sono risolti.
Inizia indicando soltanto le prime operazioni eseguibili e quali possono procedere in parallelo.
Se serve una decisione nuova dell'autore, formula una domanda concreta e spiegane il motivo.
Non avviare simulazioni o chiamate sperimentali sulla sola base di questo messaggio.
```

Questo file è una consegna locale per la conversazione. La sua creazione non comporta
nuovi commit, merge, tag o modifiche ai pacchetti sperimentali.
