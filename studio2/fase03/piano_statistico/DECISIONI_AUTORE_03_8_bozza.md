# Bozza di decisione dell'autore — piano statistico 03.8 (base verificata: revisione 7, OK)

Stato: **BOZZA — approvazioni espresse in conversazione registrate, firma pendente**.
Preparata dal consulente il 2026-09-14 e aggiornata dopo il messaggio dell'autore che inizia
«Approvare senza modifiche: D2=8», comprese le successive risposte «Sì: ripetizione della
tripletta entro la stessa riserva» e «Approvo la regola proposta» per il gate.
La colonna finale registra le approvazioni esplicite, mantenendo distinte le condizioni esterne.
Le approvazioni sono registrate a nome **Luca**, comunicato dall'autore, con data
**14 settembre 2026**, scelta dal consulente su delega dell'autore. La firma materiale
resta vuota: registrare le approvazioni e il nome non equivale ad apporla per conto dell'autore.
Il recepimento nella revisione 8 e nel manifest richiederà un incarico successivo: questa
registrazione nella sola bozza non lo esegue né autorizza chiamate sperimentali.
L'intervallo Tango A2-bis resta facoltativo e non adottato. Le regole approvate per timeout,
sonda e prompt non valutabili sono specificate in B2-bis/B2-ter, da recepire e verificare prima del pilot.

### Base effettivamente confrontata

Le sigle seguenti indicano i file **nel worktree in sola lettura**
`/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/`, non eventuali
omonimi accanto a questa bozza:

- **PS**: [PIANO_STATISTICO.md](/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/PIANO_STATISTICO.md), rev. 7;
- **MF**: [PIANO_STATISTICO_FREEZE.json](/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/PIANO_STATISTICO_FREEZE.json), rev. 7, `open_author_decisions`;
- **V**: [VERIFICA_PIANO_STATISTICO.md](/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/VERIFICA_PIANO_STATISTICO.md), settimo verbale, **OK**;
- **RP**: [REPORT_PIANO_STATISTICO.md](/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/REPORT_PIANO_STATISTICO.md);
- **DR**: [DESIGN_RESOLUTION.json](/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/DESIGN_RESOLUTION.json) e [tabelle Markdown](/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/DESIGN_RESOLUTION.md).

**PG** indica il [piano generale](/Users/luker/fot-tep/docs/paper/FoT_TEP_Review_Piano_Sperimentale.md);
**PF** il [preflight 03.0](/Users/luker/fot-tep/studio2/fase03/PREFLIGHT_03_0.md), sezioni
«Script e guardie», «Stima preventiva» e «Perimetro dell'eventuale GO», con
[configurazione del pilot](/Users/luker/fot-tep/studio2/fase03/config/pilot_preflight.json), `call_budget`.

Controllo del 2026-09-14: branch `codex/studio2-piano-statistico-fix`, HEAD
`dd82cd1753b31c10235de18052f24683306f8751`, **otto file modificati non committati**:
PS, MF, V, RP, i due DR, `design_resolution.py`, `test_design_resolution.py`.
Il candidato verificato è questo stato effettivo, **non il solo HEAD**.
Su 14 voci improntate da MF (8 file + 6 input), **13 coincidono per SHA-256 e dimensione**.
L'unica eccezione è V: MF conserva il sesto verbale
`78dc30e6f9471a0a4afa559303388e486ac130346ac60456ff2c4a6b8e9f97fe` (11.297 byte),
mentre il settimo verbale OK è
`06c2a45bb13e70d92a6a7fbb1f6df1549ccaf5911e72f9f56066751d2f99abbe` (8.471 byte).
È la sostituzione documentata da V §6, non un ulteriore difetto degli artefatti sostanziali.
Anche `independent_review_verdict`/ruolo del verbale in MF e lo stato narrativo di RP sono
anteriori all'OK: andranno allineati nel futuro recepimento, non interpretati come un nuovo NON OK.
`base_commit` e `worktree_head_at_proposal` conservano la provenienza della proposta originaria;
`revision_base_commit` identifica correttamente `dd82cd1`. Tutte le 11 decisioni in MF sono
`open`, stato generale `proposed_pending_author_decisions`, `freeze_tag: null`.

Impronte di riferimento: PS `3326e992995114f92b20117cd4b4575f6c2e7ba1758fee4463461448f010fba6`;
DR JSON `8bf79dc958e045598cf7538b72752caa902d2f8b134f642e54daaf0274fddbde`;
MF `c4ad3ca8436bd1c2e74608d3044a9d46e974a83fc4d044f84b4b499bb7d767d8`.
Nessuno di questi file è modificato in questo incarico.

### Decisioni dell'autore — approvazioni in conversazione, firma pendente

La colonna «Parere» conserva la motivazione della proposta; la colonna finale registra le
approvazioni del messaggio dell'autore. Le approvazioni provengono da quel messaggio, non dall'OK
tecnico della revisione 7. MF resta invariato con le sue decisioni `open`: il documento distingue
questa registrazione dal futuro recepimento e dalla riverifica del delta. Le domande già risolte
negli allegati sono sostituite dall'esito; non si richiede una seconda approvazione delle stesse scelte.

| Decisione | Raccomandazione del piano | Parere del consulente | Decisione dell'autore |
| --- | --- | --- | :---: |
| D2 run per fault | 8 (64 cluster fault), PS §7 | **Accettare.** +18 run primari da generare; stima ~3.555 chiamate con retry entro il tetto proposto 3.700, alle condizioni di budget sotto. H3: potenza Tango simulata 0,7650 → 0,8600 passando da 48 a 64 cluster, con Δ₃=0, m=0,125, d=0,10, α=0,05 (DR; non potenza congiunta della gerarchia) | **APPROVATA** — firma pendente |
| Margine m e α di H3 | m=0,125; α unilaterale 0,05; test score di Tango; alternativa α=0,025 (PS §4–5) | **Proporre m=0,125**, con approvazione dell'autore sulla perdita media e giudizio esplicito del consulente (A1). Raccomandare **α primario 0,05** e **0,025 come sola sensibilità H3**, senza possibilità di sostituire l'esito primario; questa sensibilità aggiuntiva è approvata in A2 | **APPROVATI** m, α e sensibilità — giudizio A1/A2 |
| Reporting per agente/fault — dettaglio aggiuntivo | PS §12–13: analisi stratificate descrittive; soglia individuale non prescritta | **Proporre** conteggi guadagnati/persi/saldo per agente e fault e segnalazione del saldo ≤−2 su 8; è una soglia descrittiva approvata, non un gate individuale (A3) | **APPROVATA** — firma pendente |
| Gerarchia (decisione 5) | sequenza fissa H1 → H2 → H3, ciascuna a 0,05 (PS §4.2) | **Accettare.** Si procede solo se il precedente rifiuta; altrimenti le ipotesi successive restano descrittive. Garanzia finita conservativa di livello per H1/H2 sotto le ipotesi sotto; per H3 e dunque per la sequenza completa il controllo è **approssimato**, non esatto | **APPROVATA** — firma pendente |
| Test di H1/H2 | Hoeffding sulla media delle medie di cluster indipendenti, limitate in [−1,1]; α=0,05; soglia 0,3533018 (48) / 0,3059684 (64); MDE Hoeffding approssimato 0,3341–0,4620 sull'intera griglia fattibile (PS §4.1, §7.1; DR) | **Accettare, con consapevolezza.** La garanzia riguarda il livello sotto la nulla debole Δ≤0, non la potenza: dipendenza intra-cluster arbitraria, indipendenza fra cluster necessaria. Per effetti veri 0,1–0,3 la potenza è sotto l'80% negli scenari esaminati; un singolo campione può comunque superare la soglia. Non si deduce la potenza della sequenza dalle potenze marginali. Bootstrap solo intervalli; sign-flip supplementare sotto scambiabilità congiunta | **APPROVATA** — firma pendente |
| OOD (decisione 3) | PS §8.1: variabile perturbata diversa e, se flusso/apparato è condiviso, anche meccanismo diverso rispetto a ciascun fault del catalogo; F6+F4; sostituti F6→F5→F12 e F4→F11→F5 | **Accettare condizionatamente.** La scelta F6 resta condizionata alla verifica e registrazione del numero di rilevabilità dalla fonte primaria (Yin 2012 / PHM 2023, tabella primaria; finestra Letteratura_LLM). In assenza di un numero verificabile si applicano i sostituti pre-specificati; restano validi gli impedimenti tecnici di PS §8.2. Evidenze bibliografiche incompatibili con la motivazione di F6 richiedono decisione esplicita prima del freeze, senza ridefinire H: il [registro dei criteri](/Users/luker/fot-tep/docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md) §3 fissa H={F3,F9,F15} nominalmente ed esclude una soglia FDR universale. Sonda descrittiva: 6 cluster e 144 chiamate a R=1, non caratterizzazione open-set | **APPROVATA CONDIZIONATAMENTE** — rilevabilità e requisiti PS §8 |
| D11 coppie confondibili | {F1, F2} e {F14, F15}; run 1–3 del lotto sigillato (PS §9) | **Accettare**: l'alternativa {F1,F2}+{F8,F10} concentra tutto sul flusso 4. Ablation descrittiva, 8n+4×3×7=148 chiamate con n=8, già comprese nel budget | **APPROVATA** — firma pendente |
| Politica R (decisione 11) | nessun R=3 per sola assenza di controlli; divergenza della coppia parsata (`abstain`, `predicted_label`) **o della validità**; nessun cambio di R a studio iniziato (PS §10) | **Accettare**, includendo audit 10% a R=3, prima ripetizione nell'analisi primaria, sensibilità con maggioranza; 10 canary/giorno e sensibilità sui giorni marcati. Due giorni marcati o cambio ID modello sospendono fino a decisione dell'autore. Zero divergenze non dimostra determinismo. Un gate ≥1/40 implica R=3 e un nuovo controllo di budget/finestra, non autorizza a superare 3.700 | **APPROVATA** — firma pendente |
| Soglie GO/NO-GO (PS §11) | T3 ≥114/120 valide al primo tentativo **e** almeno un'astensione parsata correttamente per condizione (anche prova dedicata); T4 zero troncamenti su 120; T6 0/40→R=1 sui prompt valutabili, ≥1/40→R=3; un prompt con tre risposte non valide impedisce il GO tecnico (B2-ter); T11 almeno un'astensione di A sui local-unseen del gate, altrimenti OOD comunque eseguita ma esplorativa con validità non stabilita; T5 latenza×totale entro la finestra con margine 20% | **Accettare.** T11 non è un blocco del GO; T6 richiede il ricalcolo se attiva R=3. T5 non estende automaticamente la finestra di calendario. Il GO resta subordinato a tutti gli altri bloccanti del piano generale e alle dipendenze tecniche | **APPROVATA** — firma pendente |
| T9 / T3 semantica fail-closed | 16/16 insight validi nelle 8 chiamate di conformità: (a) un errore=NO-GO, oppure (b) remediation separata pre-specificata e pilot ricongelato (PS §11; MF) | **Proporre (b)**, B1: solo prompt del producer, prima di budget e gate, tutti gli otto casi ripetuti una sola volta; qualunque insight non valido nella ripetizione è NO-GO. L'uso limitato della riserva è approvato come specificato in B2 e B2-ter; firma pendente. L'esito negativo sul Qwen-27B va sottoposto alla decisione D9; non sceglie automaticamente fra Terra-only e rinvio | **APPROVATA VIA (b)** — regole B2-bis/B2-ter definite |
| Seed del bootstrap | 20260913, 10.000 repliche, namespace studio2-fase03-piano-statistico-v1 | **Accettare** | **APPROVATA** — firma pendente |
| Run di scorta | uno per fault D1 e per Normal, sostituzione solo tecnica e pre-chiamata (PS §7.4; MF) | **Proporre anche uno per ciascuno dei due fault OOD selezionati**: 11 scorte anziché 9, approvate espressamente. Uno dei tre run OOD perso ridurrebbe di un terzo il campione di quel fault. Le scorte sostituiscono run, non aggiungono osservazioni; i sostituti OOD cambiano invece il fault | **APPROVATA** — firma pendente |
| Tetto approvato e refusi da correggere in futuro | 3.700 è il tetto di pianificazione di PG §8.8, coerente con ~3.555 a R=1; 3.500 nelle vecchie righe è disallineato (PS §7.2; RP §1) | **3.700 approvato**; il conteggio era già determinato, l'accettazione del tetto è ora registrata. Futuri allineamenti anche a §11 T5, oltre a D2/O2, e del vecchio +590 a +702 (+24,6%) con retry / +638 prima del retry. Nessuna modifica al piano generale in questo incarico | **APPROVATA** — firma pendente |

**Origine di T9 e sostituzione della regola di divergenza.** PG §11 T9 richiede il logging di
conformità: la soglia 16/16 insight validi nelle 8 chiamate è una **scelta di progetto di PS §11**
associata a quella riga, non una soglia numerica già imposta da PG. La definizione proposta in
PS §10.3 (coppia parsata o validità) **sostituisce** quella provvisoria in
`pilot_preflight.json`, `determinism_policy.divergence_event`, che include anche differenze di
JSON parsato, finish reason e byte grezzi. Tali differenze restano nel log e nel reporting;
quelle che non modificano coppia parsata o validità non attivano R=3 secondo PS. Il recepimento
operativo richiederà questa sostituzione esplicita, non un semplice allineamento di nomi.

### Conseguenze numeriche già ricavabili (non decisioni ulteriori)

**Conteggi, condizionati alla scelta D2.** PS §2, §7.2, §8.3 e §9.2; PG §8.8:

| Quantità | D2=6 | D2=8 |
| --- | ---: | ---: |
| Cluster fault, per H1/H2 e H3 | 48 | 64 |
| Righe local-unseen / local-seen, per condizione | 336 / 48 | 448 / 64 |
| Run primari fault + Normal | 48+6=54 | 64+8=72 |
| Run OOD, separati dalle ipotesi primarie | 6 | 6 |
| Scorte proposte: 8 D1 + 1 Normal + 2 OOD | 11 | 11 |
| Lotto da generare, incluse OOD e tutte le scorte proposte | 71 | 89 |
| Nucleo chiamate a R=1, tre condizioni incluse | 1.296 | 1.728 |
| OOD / ablation B-senza-LF, chiamate a R=1 | 144 / 132 | 144 / 148 |
| Totale stimato prima del retry / con retry | ~2.594 / ~2.853 | ~3.232 / ~3.555 |
| Tetto proposto | 3.000 | 3.700 |

I 72 run di D2=8 **comprendono già gli 8 Normal**: la formula «72 fault + 8 Normal»
nell'handoff, blocco 4a, è un refuso; non si propaga. Le 64 unità delle ipotesi sono i
run fault; 448 righe local-unseen non sono 448 cluster indipendenti. Scorte non impiegate:
zero chiamate, nessun aumento di N. Con le sole 9 scorte della proposta PS il totale sarebbe
69/87; le due scorte OOD sono l'aggiunta approvata dall'autore.

Le stime assumono **R=1**, audit del nucleo, accantonamento prudenziale E5 e riuso di FULL.
Senza riuso di FULL, PG §8.8 riporta ~2.906/~3.626 con retry, ancora entro i tetti; E5 resta
parametrico. A D2=8, R=3 porterebbe il **solo nucleo** a 5.184: il tetto 3.700 non basta.
Il pilot ha già una voce di ~200 nel totale: la remediation entro quel limite non si somma
una seconda volta alla stima dello studio. Scorte e run di test richiedono stream disgiunti
e identificativi sigillati in 03.11; **20260913 è il seed del bootstrap, non il seed dei run**.
Le 10.000 repliche proposte per l'analisi finale sono distinte dalle 400 repliche Monte Carlo
×2.000 bootstrap già presenti in DR; nessuna è stata eseguita in questo incarico.

**MDE H1/H2.** A α=0,05, il campo DR `analytic[].hoeffding_mde_80`, filtrato con
`hoeffding_mde_80_feasible=true`, dà:

| N | Minimo (d=0,5, ρ=0) | Massimo (d=0,8, ρ=1) |
| ---: | ---: | ---: |
| 48 | 0,385768 | 0,461955 |
| 64 | 0,334085 | 0,400064 |

Quindi l'intervallo complessivo è **0,334–0,462**; 0,36–0,46 riguardava soltanto d∈{0,5;0,8},
ρ≥0,5. Sono MDE del test di Hoeffding **approssimati con una normale**,
`t_alpha + z_0.80 × SE`, usando Var(δ)=d; non il campo `mde_80` del test normale di riferimento
e non una garanzia esatta di potenza. Per d=0,3 tutti questi MDE superano d e sono non fattibili
nell'approssimazione. Le potenze simulate di DR sono marginali: la probabilità di passare
l'intera gerarchia non è disponibile (PS §7.1; RP §1).

### Condizioni esterne ancora aperte

- **OOD**: fonte primaria numerica per F6 e riverifica F4, da registrare nella finestra
  Letteratura; H={F3,F9,F15} resta nominale come nel registro dei criteri §3. Per i sostituti
  valgono gli stessi requisiti di ammissibilità e rilevabilità di PS §8. Nel pacchetto di
  selezione non è documentato un numero riverificato per F5/F11/F12, come per F6
  (`PROPOSTA_OOD_D11.md` §2). La regola condizionata resta pre-specificabile e valida, ma
  nessun sostituto è utilizzabile prima della propria verifica. Verificarli nella stessa
  finestra Letteratura può evitare una riapertura; non è indispensabile se F6/F4 risultano
  ammissibili. La generabilità e i
  possibili trip sono controlli tecnici futuri di 03.11. I due OOD devono restare distinti:
  se entrambe le catene arrivassero a F5 non si può contarlo due volte; una combinazione non
  risolta dalle catene richiede decisione esplicita prima delle chiamate.
- **Pilot**: schema/validatore 03.12 congelati e compatibili, input e capienza di 03.10,
  configurazione effettiva e ordine congelati; nessun GO è ancora acquisito. Una prova dedicata
  di astensione eventualmente aggiuntiva deve essere contabilizzata prima, non finanziata
  automaticamente con la riserva proposta per remediation/trasporto.
- **Fattibilità**: latenza misurata, finestra di calendario, eventuale R=3, costo E5 definitivo
  e riuso FULL restano condizioni del budget; il seed dei run e la specifica delle scorte
  verranno fissati in 03.11, dopo il freeze statistico.
- **Chiusura 03.8**: inserimento bibliografico e verifica delle fonti previsti altrove,
  recepimento delle sole decisioni confermate, riverifica del delta e allineamento degli
  stati/impronte. La firma non surroga queste condizioni.

Sequenza proposta per un **incarico successivo**, dopo l'approvazione delle decisioni necessarie
(non eseguita qui; il tag è l'ultimo passo):

1. finestra 03.8: recepisce le decisioni confermate e gli allegati A/B in §5, §11 e §13 come
   **revisione 8** (base verificata: rev. 7); manifest con le **decisioni confermate registrate,
   OOD ancora condizionata fino al punto 3**, stato `proposed_pending_author_decisions` →
   `decisions_recorded_pending_reverification`; commit del
   verbale rev. 7 (impronta 06c2a45b…) e del recepimento. Registrare anche il verdetto OK storico
   della rev. 7 senza confonderlo con la riverifica ancora da svolgere sulla rev. 8; se alcune
   scelte restano aperte, conservarne esplicitamente lo stato senza dichiarare completate le decisioni;
2. allineamenti meccanici, commit separati: `APERTURA_SOTTOFASI_FASE03.md` riga 03.13 (ordine
   conformità → eventuale remediation → budget → gate); piano: tetti 3.700 in D2 e §11 T5/O2,
   più i refusi sui totali e sul +590 nelle sezioni richiamate, usando PG §8.8 e PS §7.2;
3. finestra Letteratura_LLM: numero di rilevabilità di IDV(6) (e IDV(4)) dalla tabella primaria nel
   registro dei criteri → chiusura o sostituzione OOD secondo la regola; ingresso nel corpus di
   Tango, Maurer–Hothorn–Lehmacher, Westfall–Krishen, Clopper–Pearson, Kish, ICH E9, Hoeffding,
   Bahadur–Savage. Sono gli **otto** riferimenti metodologici esterni di PS §17;
   McMahan è il riferimento aggiuntivo indicato dall'handoff per la finestra Letteratura/FedAvg,
   non un nono riferimento metodologico esterno elencato in PS §17;
4. riverifica ristretta al delta rev. 7 → 8 (modello diverso), che include coerenza con il
   manifest, ordine del pilot (Allegato B) e budget;
5. aggiornamento finale delle impronte nel manifest (verbale della riverifica compreso) e commit;
6. dopo verifica e raggiungibilità del commit in `origin/main` secondo MF e MAINTENANCE §8,
   freeze e tag `studio2-fase03-piano-statistico-frozen-001` — prima di qualunque run di test
   (03.11) e prima del pilot per §10–§11; solo dopo, 03.10 sostituisce la regola di divergenza
   provvisoria con quella congelata.

Firma dell'autore: ____________________  data: __________

Autore delle approvazioni: **Luca**. Data di registrazione: **14 settembre 2026**.
Nome fornito dall'autore; data scelta su sua delega. Le approvazioni in conversazione sono
registrate separatamente dalla sottoscrizione materiale di questo documento.

---

## Allegato A — motivazione del margine m = 0,125 e giudizio del consulente (per PS §5)

**Che cosa il margine è.** Il margine m = 0,125 riguarda la **differenza media di accuratezza sui
local-seen** fra B-LF e A, con uguale peso agli otto fault (cluster run×fault, unità del disegno).
La scelta approvata lo definisce come **massima degradazione media netta accettabile in questo studio**,
pari a **12,5 punti percentuali di accuratezza**: un metodo che perde in media più di un ottavo
non soddisferebbe questo criterio, qualunque cosa guadagni sugli unseen. **L'approvazione è
registrata in A1; il giudizio metodologico del consulente è esplicitato sotto e non deriva
dai calcoli di potenza.**
Non è una soglia validata di adottabilità industriale. H3 misura il saldo
fra diagnosi guadagnate e perse rispetto ad A, non soltanto le diagnosi già corrette che vengono
compromesse.

**Che cosa il margine non è.** H3 **non garantisce la non inferiorità di ciascun agente** e può
nascondere peggioramenti concentrati su singoli fault: un agente potrebbe perdere due casi su otto
e gli altri nessuno, con una perdita aggregata di 2/64 = 3,1 %. Per questo l'analisi descrittiva
approvata come pre-specificata (da aggiungere a PS §13 nel futuro recepimento) riporterà la
differenza B-LF − A **per agente e per fault** con i conteggi grezzi (casi persi, casi guadagnati,
saldo), e segnalerà ogni agente con **saldo = guadagnati − persi
≤ −2 casi su 8**, senza
attribuire a questa segnalazione valore confermativo. La soglia −2 non è ricavata da PS o DR:
è una proposta aggiuntiva del consulente approvata dall'autore in A3. Con un fault posseduto da ciascun agente,
le righe local-seen per agente e per fault descrivono gli stessi otto gruppi, non evidenze
indipendenti aggiuntive. L'esempio e la soglia su otto casi presuppongono D2=8; con D2=6
occorre confermare la regola su sei casi, senza trasferirla tacitamente. Se il requisito operativo dell'autore fosse
«nessun agente perde più di un caso», il criterio scientifico andrebbe cambiato (test per agente
o regola di gate per agente), non rimotivato: **qui si propone il criterio aggregato**, e la
tabella per agente ne sarebbe il complemento descrittivo, non una garanzia individuale.

**Conseguenze della scelta, non sue giustificazioni.** Con D2 = 8 il bordo del margine coincide
con un conteggio osservabile (8 casi su 64; 6 su 48 con D2 = 6), il che rende leggibile l'esito al
bordo ma **non** è ciò che rende m ammissibile: anche 0,10 lo sarebbe, perché il parametro di
popolazione non è vincolato alla griglia campionaria. La risoluzione del disegno è la verifica
di sanità che il piano richiede, non l'origine della soglia. Il bordo 8/64 è un saldo netto
osservabile, **non una regola di superamento di H3**: la decisione resta il test score di Tango
contro Δ₃≤−m, subordinato a H1 e H2.
Non si traduce m=0,125 in «quattro perdite nette ammesse»: il test dipende dai conteggi
b (guadagnate) e c (perse), non dal solo saldo. La scelta sostanziale riguarda la perdita
media nella popolazione, non un numero fisso di errori consentiti nel campione.

La tabella seguente usa **N=64 cluster, Δ₃ vero=0, α=0,05 unilaterale** in tutte le righe.
Fonte: DR JSON, `analytic` (campi `power_at_null_or_effect`, `mde_80`) e `simulated`
(`hypothesis=H3`, `scenario=power_at_zero_delta`, campo `rejection_rate_tango`), con i filtri
N, d e m della riga; replica leggibile in DR Markdown. Le simulazioni già archiviate usano
400 repliche per scenario, seed globale 20260913 con contatore degli scenari; non sono state rigenerate.

| m | Discordanza d | Potenza analitica normale | Potenza Tango simulata | m minimo normale all'80% |
| ---: | ---: | ---: | ---: | ---: |
| 0,100 | 0,10 | 0,8119 | 0,7250 | 0,0983 |
| 0,125 | 0,10 | 0,9354 | 0,8600 | 0,0983 |
| 0,150 | 0,10 | 0,9842 | 0,9525 | 0,0983 |
| 0,125 | 0,20 | 0,7228 | 0,6975 | 0,1390 |

Con **m=0,10 e d=0,10**, dunque, è la potenza **Tango simulata** a essere sotto l'80%
(0,7250); il riferimento **normale analitico** è sopra (0,8119). I vecchi «0,81/0,73»
non rappresentavano due alpha. Analogamente «0,98/0,95» a m=0,15 indicava normale/Tango,
sempre a α=0,05. Con m=0,125, Tango supera l'80% a d=0,10 ma **non** a d=0,20.
Gli MDE della tabella sono approssimazioni normali con Var(δ)=d, non MDE simulati di Tango
né garanzie di raggiungere l'80%. Le potenze sono marginali per H3, non della sequenza completa.
Con 400 repliche il MCSE è al massimo 0,025 (PS §7.1; RP §1): le cifre servono a rintracciare
le righe, non attestano precisione al quarto decimale.

**Sensibilità α=0,025, distinta dalla griglia canonica a 0,05.** PS §4.1 riporta per
N=64, d=0,10, m=0,125, Δ₃=0 una potenza **analitica normale** 0,9354 a α=0,05 e 0,8854
a α=0,025. RP §6 riporta separatamente un controllo **Tango simulato** dello stesso scenario:
0,8675 a α=0,05 e 0,8075 a α=0,025 (seed proprio 20260913, 400×2.000).
Quel controllo ha uno stream diverso dalla griglia completa e **non sostituisce** il suo
0,8600 a α=0,05. Non è disponibile qui una griglia completa archiviata a α=0,025;
non se ne deducono altri valori. Non è stata eseguita alcuna nuova analisi Monte Carlo.

Le potenze sotto piccole perdite vere discusse nel secondo parere sono **scenari analitici
normali aggiuntivi**, non righe di DR né potenze simulate di Tango. Non vengono aggiunte alla
tabella verificata. A parità di d, una differenza vera negativa avvicina l'alternativa al bordo
−m e riduce la potenza nell'approssimazione normale: è un limite della lettura dei soli scenari
Δ₃=0, non una previsione sul collo di bottiglia della gerarchia. Anche le frequenze illustrative
della segnalazione per agente dipendono dal modello sintetico e, per la probabilità su tutti
gli agenti, dall'indipendenza fra gruppi; non giustificano la soglia −2 né entrano come garanzie.

La scelta di m cambia il claim e il bordo del test e ne cambia quindi la potenza, pur mantenendo
la famiglia di analisi. Il riferimento a ICH E9 resta quello proposto da PS §17, da verificare
e inserire nel corpus nella finestra Letteratura; non costituisce una validazione del valore
0,125 per questo contesto.

**Che cosa questa motivazione non usa.** Risultati precedenti citati come attese dal piano,
potenza osservata a posteriori o presunte preferenze di un ingegnere. Non sono una calibrazione
del margine; i calcoli sopra sono scenari sintetici di progetto, non risultati dello studio.

**Approvazioni registrate e giudizio metodologico esplicito del consulente.**

- **A1 — approvata in conversazione, firma pendente.** m=0,125 come massima perdita media
  netta sui local-seen, senza traduzione in numero di casi ammessi. **Giudizio del consulente:**
  ritengo difendibile chiamare questo risultato «conservazione entro un margine medio di 12,5
  punti percentuali» nel perimetro dello studio, rendendo esplicito il margine nel claim.
  Non lo equiparo ad assenza di danno o a conservazione di ciascun agente. È una scelta
  sostanziale di tolleranza dello studio, non un valore ottimizzato sulla potenza né una soglia
  di adozione industriale validata. Un requisito individuale sarebbe un'altra specifica.
- **A2 — approvata in conversazione, firma pendente.** α=0,05 primario, con H3 anche a
  α=0,025 come test di sensibilità pre-specificato; H1/H2 e gerarchia primaria restano a 0,05.
  **Giudizio del consulente:** la scelta mantiene il livello primario del piano e rende
  visibile la robustezza al livello più severo senza scegliere a posteriori il risultato da
  privilegiare. La sensibilità non sostituisce la decisione primaria; il controllo della
  sequenza completa resta approssimato perché Tango è asintotico.
- **A2-bis — facoltativa, non adottata.** L'eventuale limite inferiore unilaterale al 97,5%
  per inversione dello score di Tango resta un oggetto distinto, da specificare, approvare
  e verificare separatamente. Non è necessario aggiungerlo per attuare A2.
- **A3 — approvata in conversazione, firma pendente.** Tabella per agente/fault e segnalazione
  saldo≤−2 su 8, descrittiva e legata a D2=8. **Giudizio del consulente:** è una segnalazione
  leggibile dei peggioramenti concentrati; su otto casi, una perdita netta è al bordo del
  margine e due lo superano in valore assoluto. Questo legame aritmetico non estende H3 a un
  test per agente e non calibra il tasso di falsi allarmi. La segnalazione non è un gate e
  non determina il successo dello studio; i conteggi completi restano necessari.

## Allegato B — remediation T9, definizione operativa (per PIANO_STATISTICO §11 e 03.13)

**Stato.** L'autore ha approvato in conversazione **la via (b)**: una sola remediation al
prompt, prima della sonda e del gate, con i vincoli qui descritti. Ha inoltre escluso dalla
remediation i timeout senza prova di zero token e approvato le regole della sonda e dei prompt
del gate non valutabili in B2-ter. Le regole devono essere recepite e verificate prima del pilot.
PS, MF e PF non sono modificati: la loro registrazione storica resta aperta e PF conserva
`retry_reserve_authorized=false`. Nessuna chiamata o modifica operativa è eseguita qui.

**Ambito.** Le 8 chiamate di conformità del producer Qwen (2 insight per agente → 16 insight),
validate con il validatore 03.12 congelato al primo tentativo, senza retry automatici (PREFLIGHT).

**Ordine vincolante del pilot (03.13).** Conformità del producer → eventuale remediation → sonda
di budget → gate 40×3. L'ordine è obbligatorio, non «di norma»: se il gate fosse già stato eseguito,
la remediation **non è ammissibile** (due gate da 120 richiederebbero già 240 chiamate) e un
insight non valido è NO-GO. `APERTURA_SOTTOFASI_FASE03.md` riga 03.13 va corretta di conseguenza
in un incarico successivo, e `frozen_gate_config` deve registrare l'ordine. Il template risultante
dalla conformità/remediation entra negli input della sonda; la sonda completa e congela la
configurazione di budget usata dall'unico gate successivo. Non si presume che il freeze finale
del budget esista già prima della sonda.

**Evento.** Almeno un insight su 16 non valido al primo tentativo: T9 richiede 16/16 validi,
prodotti in 8 chiamate; non si confondono i due denominatori. La risposta grezza, l'hash, il prompt,
il fingerprint e l'errore tipizzato del validatore vengono conservati prima di qualunque altra
azione; l'insight non viene corretto a mano né riformattato.

**Classificazione proposta dell'errore.** Le classi 1–4 si basano sugli errori del validatore
e sui metadati di troncamento; la classe 5 sui log di trasporto/server, non su un codice di
validazione dello schema. Ogni errore va registrato nella classe pertinente; se una risposta
presenta più errori si conservano tutti, senza sceglierne uno per eludere T9:

1. *strutturale* — campo mancante/extra, tipo errato, cardinalità, JSON non parsabile;
2. *identificatori* — parafrasi o forma non letterale di XMEAS/XMV, ID fuori range;
3. *cap* — caratteri o token oltre il limite, troncamento;
4. *leakage* — parola o pattern vietato nella narrativa (falsi positivi dichiarati inclusi);
5. *trasporto* — errore d'infrastruttura **verificabile**: stato HTTP di errore o connessione
   caduta **e** log del server vLLM che attesti zero token generati per quella request id. Un
   timeout senza questa evidenza non dimostra che il modello non abbia generato testo e si
   distingue da un difetto diagnosticato dell'output. **Regola approvata B2-bis:** si registra
   come guasto tecnico non risolto; non è materia di remediation del prompt. Non lo si
   riclassifica come difetto strutturale per consentire un diff «plausibile», né lo si usa
   come prova di incapacità del modello.

**Che cosa è ammesso correggere, per classe.** Per difetti diagnosticati delle classi 1–4:
soltanto il **prompt del producer**
(istruzioni, esempio di formato, elenco esplicito dei vincoli), mai lo schema, mai il validatore,
mai le regole di leakage, mai i campi fissi serializzati; se l'analisi mostra che l'errore nasce
dallo schema o dallo scanner (per esempio un falso positivo non dichiarato), la correzione passa da
una **revisione di 03.12 con riverifica indipendente**, non da questa remediation. Classe 5: nessuna
correzione; non conta per T9; la chiamata si ripete dalla riserva finché **tutte e otto** le
chiamate sono valutabili, entro la **riserva residua e il limite cumulativo** sotto, e ogni
ripetizione è registrata. Senza riserva sufficiente non si dichiara PASS e non si avanza al gate;
l'impedimento tecnico resta documentato. La revisione di 03.12 è fuori da questa remediation
e non consente di proseguire sotto un vecchio freeze.

**Procedura.** (a) Artefatto `REMEDIATION_T9_001.md` in 03.13 con evento, classe, evidenza, diff
del prompt del producer prima/dopo, motivazione; (b) autorizzazione scritta dell'autore; (c)
la remediation avviene **esclusivamente prima** della sonda di budget e del gate; aggiorna il
template del producer e le relative impronte negli input che confluiranno in `frozen_gate_config`, nessun altro parametro
cambiato; sonda e gate vengono eseguiti successivamente sulla configurazione risultante; (d) le 8 chiamate si ripetono **tutte** — non solo quella fallita — sugli **stessi otto casi/input**
con il **nuovo template congelato** (non gli stessi prompt byte per byte: il diff del template è
registrato e le nuove impronte entrano in `frozen_gate_config`), attingendo alla riserva di 15
chiamate: 8 per la remediation, **al massimo 7 complessive** per ripetizioni di classe 5,
incluse quelle già spese prima della remediation; tetto
cumulativo del pilot 200 invariato e hard stop; (e) i 16 insight
della prima esecuzione, o quelli effettivamente ottenuti se incompleta, sono scartati e conservati
come evidenza: non entrano in alcuna libreria. Il nuovo template va congelato prima della
ripetizione completa e le nuove impronte dei prompt vanno conservate.

**Contabilità della riserva, derivata da PF e `call_budget`.** Senza remediation:
8 conformità Qwen + 3–9 sonda + 120 gate = **131–137** chiamate; includendo le 8 del producer
alternativo, tuttora differite, **139–145**. Con 8 chiamate di remediation:
**139–145** senza producer alternativo, **147–153** includendolo. Consumando anche tutte le
7 chiamate residue per trasporto si arriva al massimo a **152 / 160**, rispettivamente.
Senza remediation, la proposta ammette fino a 15 ripetizioni di sola classe 5 nella conformità.
Se la remediation diventa necessaria, deve restare spazio per **tutte e otto** le chiamate:
più di 7 chiamate di trasporto già consumate la rendono non finanziabile con questa riserva.

La riserva è **unica**: `8 × remediation + trasporto ≤ 15`, con remediation∈{0,1};
non si ricostituisce cambiando template, directory, esecuzione o producer. Ogni richiesta
effettivamente inviata conta anche se fallisce per trasporto e anche se T9 non la considera
valutabile. Il contatore del pilot include tutte le sue richieste: conformità, sonda, gate,
remediation, trasporto e producer alternativo se successivamente autorizzato. Le 8 chiamate
differite del producer alternativo restano accantonate e non finanziano ripetizioni ulteriori.
**200 è un hard stop cumulativo, non un'autorizzazione a spendere le 40 chiamate fra 160 e 200**
né a iniziare un altro pilot per azzerare il contatore. Nessun retry automatico è introdotto.
**Estensione esplicitamente approvata B2-ter:** la ripetizione dell'intera tripletta della
sonda per trasporto documentato consuma tutte le richieste ripetute dalla stessa riserva.
La quota di 8 resta destinata esclusivamente alla remediation e non viene riutilizzata per
la sonda se la remediation non è avvenuta. Le ripetizioni della sonda possono quindi usare
solo quanto resta delle altre 7 chiamate dopo i consumi di trasporto già registrati: al massimo
due triplette complete se tutte e 7 sono ancora disponibili. Una riserva insufficiente non
autorizza una tripletta parziale né un superamento del tetto. Nessuna ripetizione per trasporto
è ammessa nel gate. I massimi 152/160 e l'hard stop cumulativo 200 restano invariati.
L'esito R=3 richiede ricalcolo e decisione dell'autore senza aumento automatico
del tetto né NO-GO scientifico automatico.

**Limiti.** Una sola remediation per pilot: **qualunque** insight non valido al primo tentativo nella
ripetizione completa è **NO-GO**, anche se il difetto è diverso dal primo; non è ammessa una
seconda correzione. D9 resta una decisione dell'autore: sul Qwen-27B, l'opzione 3 è fermare
l'espansione e scegliere fra Terra-only e conferenza successiva, non avviare automaticamente
un altro modello. La remediation non si applica a T3
(≥ 95 % su 120: ha già la sua tolleranza), a T4 né a T6. Per T4: passare al candidato di budget
successivo vale **solo durante la sonda di budget**; un troncamento nel gate da 120, a configurazione
congelata, resta un fallimento T4. Il paper riporta se
la remediation è avvenuta, con classe e diff del prompt.

**Motivazione della raccomandazione.** Una correzione limitata al prompt, seguita da una sola
ripetizione completa documentata, verifica se la configurazione corretta soddisfa lo schema.
Non dimostra la causa del primo errore né rende la conformità immune da variabilità: l'esito
resta condizionato a una procedura adattiva pre-specificata, da descrivere nel paper insieme
al primo fallimento. Il limite a un intervento, lo schema invariato e l'esclusione degli insight
precedenti contengono la ricerca dell'esito; non la trasformano in una prova di affidabilità generale.
Le probabilità calcolate ipotizzando 16 insight indipendenti e una regola del tre con n=16
non sono una stima di affidabilità del pilot: l'indipendenza fra i due insight della stessa
chiamata non è stabilita. Eventuali esempi con quell'ipotesi restano illustrativi e non
dimostrano che il NO-GO immediato sia troppo fragile nel protocollo effettivo.

**Approvazioni registrate e regole da recepire prima del pilot.**

- **B1 — approvata in conversazione, firma pendente.** Via (b), una sola remediation prima
  di sonda e gate, soltanto per difetti diagnosticati dell'output e senza cambiare lo schema.
  Restano l'artefatto di remediation e l'autorizzazione scritta sul diff concreto previsti
  dalla procedura: l'approvazione del disegno non esegue l'intervento futuro.
- **B2 — perimetro della via (b).** Riserva unica di 15, con 8 chiamate per la remediation
  e al massimo 7 residue complessive dopo tale intervento; i trasporti precedenti consumano
  la stessa riserva. L'estensione alla sonda è approvata separatamente in B2-ter; le
  ripetizioni per trasporto nel gate sono escluse.
- **B2-bis — regola approvata in conversazione.** Timeout senza prova di zero token = guasto
  tecnico non risolto, non materia di remediation. La disponibilità dei log necessari alla
  classe 5 va verificata prima del pilot. Non è autorizzato aggirare un timeout tramite una
  correzione del prompt priva di diagnosi.
- **B2-ter, sonda — autorizzata esplicitamente in conversazione.** L'intera tripletta può
  essere ripetuta soltanto per trasporto documentato con prova di zero token. Tutte le
  richieste ripetute consumano la stessa riserva di 15, preservando la quota di 8 per
  l'eventuale remediation secondo la contabilità sopra e il limite cumulativo 200.
- **B2-ter, gate — regola approvata esplicitamente in conversazione.** Nessuna ripetizione
  per trasporto. Le risposte non valide sono conteggiate in T3.
  Con PS §10.3, una ripetizione non valida e una valida differiscono e attivano R=3;
  non è prevista un'esenzione del trasporto documentato da T6. Se un prompt ha tutte e tre
  le risposte non valide, T6 è non valutabile per quel prompt e non si concede GO tecnico.
  Le tre invalidità non sono chiamate «divergenza» per il solo flag di validità e il prompt
  non è promosso a stabile. La regola è fissata prima del pilot, non scelta in base agli esiti.

**Decisione organizzativa fuori tabella, da fissare prima del pilot.** Se il gate attiva R=3,
si ricalcolano budget e finestra e si rimette l'esito all'autore. Il solo nucleo a D2=8 costa
5.184 chiamate, oltre il tetto approvato 3.700: nessun aumento automatico del tetto e nessun
NO-GO scientifico automatico. Il messaggio dell'autore lascia esplicitamente da decidere
la gestione operativa di questo ramo prima del pilot.

---

### Correzioni documentali di questa consegna e fonti

| Punto corretto | Correzione rispetto alla bozza precedente | Fonte |
| --- | --- | --- |
| Base verificata | Identificati branch, HEAD più otto modifiche, 13/14 impronte allineate e sola impronta storica del verbale; distinti metadati pre-review dall'OK | Stato Git, MF, V §1/6, impronte lette |
| D2 e tetti | Separati 64 fault/8 Normal/6 OOD, 11 scorte proposte, 89 run totali; +702 con retry, +638 senza; 3.700 condizionato a R=1/E5/FULL | PS §2, §7–9; RP §1; PG §8.8; refuso handoff blocco 4a |
| MDE H1/H2 | 0,334–0,462 sull'intera griglia fattibile; intervalli per N; MDE approssimato distinto da garanzia di livello | DR `analytic`, MF `design_resolution.hoeffding_mde_80`, PS §7.1 |
| Allegato A, potenza | Ogni numero porta scenario, metodo e α; 0,8119 è normale e 0,7250 Tango a m=0,10, entrambi α=0,05; controllo α=0,025 separato dalla griglia | DR; PS §4.1/§7.1; RP §6 |
| Margine e gerarchia | Rimossa l'attribuzione all'autore di un giudizio già formato; 12,5 punti medi, nessuna garanzia per agente; FWER completo approssimato, potenze marginali | PS §4–5, V §3/5; soglia per agente proposta nella bozza, non in rev. 7 |
| OOD, D11, R e pilot | Condizioni bibliografiche/tecniche aperte; 148 chiamate D11; validità inclusa nella divergenza; T3/T11 esplicitati, audit/canary e costo R=3 richiamati | PS §8–11, registro criteri §2–3, PG §8.7/§11 |
| Allegato B | Ordine obbligatorio, un solo intervento, 16 insight/8 chiamate, schema invariato, riserva condivisa anche con trasporto precedente, totali 152/160 e hard stop 200; esito D9 non automatico | PS §11, PF, configurazione `call_budget`, PG D9; dettagli restano proposta B1/B2 |
| Chiusura e riferimenti | Recepimento rinviato; allineamento futuro anche T5/+590; otto riferimenti esterni di PS distinti da McMahan nell'handoff | PS §16–17; RP §4; MF; PG sezioni richiamate |
| Riesame del secondo parere | Esplicitati origine della soglia T9, sostituzione della divergenza provvisoria e verifica condizionata dei sostituti OOD; esclusa la regola delle quattro perdite; separati intervallo Tango, timeout e uso della riserva oltre la conformità | PG §11 T9; PS §4/§10.3/§11; `pilot_preflight.json` `determinism_policy`; `PROPOSTA_OOD_D11.md` §2; posizione riveduta comunicata in questa conversazione |
| Approvazioni dell'autore | Registrate le decisioni esplicite nella colonna finale e negli allegati; OOD condizionata; giudizio metodologico del consulente su A1–A3; autorizzata la sonda dalla stessa riserva e fissata la regola sui prompt del gate non valutabili; firma vuota, A2-bis non adottata | Messaggio «Approvare senza modifiche: D2=8» e successive risposte esplicite su sonda/gate in questa conversazione |

**Consegna limitata alla bozza.** Registrate soltanto le approvazioni espresse in conversazione,
con condizioni esterne e ramo organizzativo R=3 distinti. Nessuna firma apposta o modifica alla revisione 7,
al piano generale, ai registri, al codice o al walkthrough. Nessuna ricerca
bibliografica, chiamata sperimentale, simulazione, commit, push, merge o tag eseguiti.
