NON OK

# Verifica indipendente del candidato di allineamento 03.8 rev.10

## Identità, mandato e indipendenza

Verifica del 14 settembre 2026, Europe/Rome. Revisore **gpt-6-astra**, reasoning effettivo
**high**, task/sessione `01a0a1d9-8ccd-7893-b504-4fde93380ea0`, agente `/root`.
Modello ed effort sono stati letti dal record `turn_context` della sessione locale;
non si dichiara `max`: era la configurazione raccomandata dal prompt, diversa da quella
utilizzata. Questa è una nuova task con contesto indipendente dal preparatore; nessun
agente preparatore è stato coinvolto e nessun sottoagente è stato utilizzato.

Prompt eseguito dalla copia di consegna:
`/Users/luker/fot-tep-piano-statistico-chiusura/studio2/fase03/piano_statistico/PROMPT_VERIFICA_ALLINEAMENTI_03_8_REV10.md`.
SHA-256 verificato prima della lettura del merito:
`04401004d2bcc0196725faca22d8c4ff2cc97e2903e833399628bffb0d7a33e5`.

| Oggetto | Identità verificata |
| --- | --- |
| Worktree di review | `/Users/luker/fot-tep-verifica-allineamenti-03-8-rev10` |
| Branch | detached HEAD, copia inizialmente pulita |
| Candidato | `4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8` |
| Tree | `1eb1d7df58e55a546931711f0a1cf9d800e02e3e` |
| Baseline immediata | `70c84e3a573951171813add26a46167cbc6c7203` |
| Base locale e remota main | `a00605862f627710347bd63c49f79a6d0a00135f` |
| Candidato statistico originario | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` |
| Consegna/verifica originaria | `51782e8c40069c0a2310afafc36907a61d517ff6` |

Il worktree sorgente di consegna era pulito sul branch
`codex/studio2-piano-statistico-chiusura-rev10`, HEAD
`2520e7abc1cd68785f2789448b509dea5e55ee7d`, tree
`37f246174c9fecb6e623873c5487de04ec65b400`. Non è stato recensito quel successore:
è stata creata una copia detached dell'esatto candidato richiesto. Gli oggetti commit
indicati esistono; HEAD/tree e pulizia sono stati controllati prima del merito.

## Rilievi che impediscono l'OK del delta

I controlli di integrità passano. L'allineamento del **piano generale** è però incompleto:
nuovi riepiloghi corretti convivono con prescrizioni operative ancora formulate come
correnti. La nota di prevalenza alle righe 10–18 aiuta a scegliere la fonte, ma non
completa il mandato di allineamento: §8 si presenta ancora come «versione definitiva»
(riga 390), mentre le righe sotto non sono contrassegnate localmente come storia.
I rilievi seguenti riguardano omissioni nel perimetro richiesto, anche quando la singola
riga era già presente nella baseline. Non richiedono modifiche agli artefatti rev.10.

### R1 — Costo del nucleo e durata ancora errati nel paragrafo operativo R

**File:** `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`, riga **524** (§8.7),
con richiamo alla riga **371** (§7).

La riga 524 afferma ancora che R=1 porta il nucleo «da 5.184 a 1.296 chiamate»
e comprime la durata «da ~7 giorni a 2–3»; riga 371 ripete la durata e sostiene
che il volume non è più il vincolo. A D2=8 il nucleo R=1 è **1.728**, non 1.296;
5.184/1.728=3. La durata richiede le misure ancora pendenti di D9/T5.
Il nuovo §8.8 non elimina la contraddizione nel paragrafo che disciplina R.

**Prova primaria:** `PIANO_STATISTICO.md` §§7.2 e 10.2;
`BUDGET_RISORSE_REV10.md`, tabella «Blocchi a D2=8» e sezione «Totale e finestra
operativa». Inoltre `COORDINAMENTO_CHIUSURA_03_8.md:60` prescrive esplicitamente
proprio la correzione di §8.7 e la rimozione dell'estrapolazione di durata.
Ricalcolo indipendente: `1344+192+192=1728`, `1728*3=5184`.

**Correzione minima:** sostituire l'apertura §8.7 con 1.728/5.184 e fattibilità
misurata `1,20×T≤W`; correggere o marcare espressamente come storica la durata in §7.
Non introdurre una nuova previsione di giorni.

### R2 — Disegno e tabella dell'ablation conservano il ramo a sei run; scorte assenti

**File:** stesso piano generale, righe **341–342**, **399–401**, **424–428**
e **1139–1140**.

§6.9 continua a prescrivere «almeno 6» e le alternative 54/72; §8.1 conserva
«≥6 ... preferibilmente 8» e Normal «≥6». La tabella operativa dell'ablation
usa `8×6×1=48` e totale **132**, mentre con D2=8 occorrono **64+84=148**
a R=1, **444** a R=3. La sezione D2 è stata aggiornata a 64 fault +8 Normal,
ma il piano generale non riporta le **11 scorte** e il lotto **89**: la ricerca
mirata non trova né «11 scorte», né «undici [scorte]», né «89 run».
APERTURA, al contrario, riporta correttamente il lotto completo.

**Prova primaria:** `PIANO_STATISTICO.md` §§1, 7.3, 7.4 e 9.2;
`BUDGET_RISORSE_REV10.md`; `COORDINAMENTO_CHIUSURA_03_8.md:56` richiede
esplicitamente 72 primari +6 OOD +11 scorte =89 e nessuna osservazione aggiunta
dalle scorte. Il mandato C richiede le numerosità correnti anche nel piano generale.

**Correzione minima:** allineare §6.9/§8.1 a 8 run, 64 fault +8 Normal;
riportare 6 OOD e 11 scorte tecniche, con ordine freeze→03.11 e uso sostitutivo;
correggere la tabella §8.3 a 148/444 o specificare chiaramente R=1 e rinviare alla
formula corrente. Conservare il confronto 6/8 soltanto nei passaggi etichettati storici.

### R3 — Residui scientifici già risolti ancora descritti come non lavorabili o aperti

**File:** stesso piano generale, righe **518**, **1185–1189**, **1216–1218**,
**1275**.

§8.6 dice ancora che la scelta OOD dipende da un catalogo non fissato ed è
«non lavorabile oggi». La chiusa delle precedenze a riga 1275 ripete tale blocco
per S13 e S12. D12 si intitola ancora «aperta, lavorabile oggi», mentre lo schema
03.12 R4 è pubblicato e congelato. D11 conserva solo il futuro «vanno identificate»
senza riportare le coppie già confermate. Questi passaggi confliggono con §0.1,
con S12/S13/S17 aggiornati e con la matrice corretta dei residui.

**Prova primaria:** `PIANO_STATISTICO.md` §§8, 9, 15, 16; `CATALOG_FREEZE.json`;
tag R4 e `PUBBLICAZIONE_SCHEMA_INSIGHT.md`, verificati nella sezione B sotto.
La selezione D11 è compiuta; per OOD restano controlli tecnici 03.11 dopo il freeze,
non una nuova attesa di D1. Il pin adapter 03.10 resta un requisito distinto.

**Correzione minima:** aggiornare le chiuse di §8.6/§11, il titolo D12 e il breve
paragrafo D11 con stato e fonte correnti, preservando i controlli tecnici futuri.
Non ripristinare una dipendenza 03.8→03.11→03.8 e non riaprire decisioni approvate.

### R4 — Assegnazione dei ruoli a modelli nel disegno dichiarato definitivo

**File:** stesso piano generale, righe **359–361**, **394** e **434**.

§8.1 assegna ancora esplicitamente Qwen-2.4T a producer e consumer; §8.4 definisce
il confronto con una libreria «interamente da Qwen-2.4T», e §7 nomina quel modello
per pilot e produzione. Il nuovo paragrafo alle righe 448–450 dice correttamente
che i ruoli saranno fissati da D9, ma la specifica del disegno rimane incompatibile
con tale stato. Non è stato scelto un modello dalla review; il difetto è testuale.

**Prova primaria:** `BUDGET_RISORSE_REV10.md`, «Modelli e unità»;
`PIANO_STATISTICO.md:565–569`; `MATRICE_RESIDUI_CHIUSURA_03_8_REV10.md`,
«Dipendenze da D9»; `CONSEGNA_TECNICA_03_10_DA_REV10.md`, «Separazione D9».
Producer principale, consumer e alternativo restano ruoli non assegnati.

**Correzione minima:** usare i nomi dei ruoli nelle prescrizioni correnti, rinviando
identità/configurazione a D9. Le opzioni storiche/condizionali di D9 possono restare
come tali, senza trasformarle in assegnazioni già efficaci o nuove scelte automatiche.

Dopo le correzioni sarà necessario aggiornare report e impronte del manifest del
nuovo delta e sottoporre **un nuovo candidato** a review. Nessuna correzione è stata
applicata in questa sessione. I rilievi non invalidano l'OK sul recepimento A/B di
`6aaa5b3`; impediscono l'OK sull'allineamento di `4503cb6`.

## A. Perimetro, identità e preservazione

✅ `git diff --name-status 70c84e3..4503cb6`: esattamente **2 M +5 A**;
487 inserimenti e 70 cancellazioni. Modificati piano generale e APERTURA;
aggiunti consegna tecnica, istruzioni firma, manifest, matrice e report.
Nessun preflight, harness, codice, test, dato, file congelato o coppia walkthrough
MD/HTML nel delta. Il diff completo è stato esaminato; per i cinque file nuovi
è stato letto anche il contenuto integrale.

✅ Confronto dei byte del worktree con `git show 51782e8:<path>`:
tutte le 19 voci `files` del manifest statistico coincidono. Coincidono inoltre
manifest corrente, verbale rev.10, delta 03.10 e coordinamento preparatorio.
Le sette identità espressamente richieste sono:

| File nella cartella piano_statistico | Byte | SHA-256 ricalcolato |
| --- | ---: | --- |
| `PIANO_STATISTICO.md` | 81490 | `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` |
| `PIANO_STATISTICO_FREEZE.json` | 25894 | `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8` |
| `REPORT_PIANO_STATISTICO.md` | 11298 | `909cbe2a30bd517e6f4e100c9fd0794fac353e3d805d356ace1cbf9cb9e87e70` |
| `VERIFICA_PIANO_STATISTICO_REV10.md` | 12478 | `d269e26d8cb4e23370577e1e193d90d9357d66f7c739e9d0669970edf71b0066` |
| `DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md` | 4974 | `4a0a4e1fc2797ee7a81439110e164d43159c745007136c9dda7bed7759471cc8` |
| `BUDGET_RISORSE_REV10.md` | 8528 | `8d909d8f851b8b9c633687989d3a9f3221230b48e1f0595278e075556d283887` |
| `DELTA_HARNESS_03_10.md` | 7108 | `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e` |

✅ Manifest statistico: JSON valido, **19/19 files e 6/6 inputs_read** risolti
nel worktree, dimensioni e SHA-256 coincidenti. Gli input sono catalogo D1,
proposta OOD/D11, registro criteri, registro calibrazione, bootstrap e metrics
storici. Nessuna rigenerazione del disegno o prova su dati nuovi.

✅ I nove file acquisiti in `70c84e3` coincidono byte per byte sia con quel
commit sia con `51782e8`: bozza decisioni, DESIGN_RESOLUTION JSON/MD, verbali
rev.7/8/9, design_resolution.py, relativo test e sottofase_3_8.md. Sono tutti
contenuti anche nelle 19 voci verificate; nessun prerequisito mancante.

✅ Manifest del delta: JSON valido, **6/6 voci** per byte e SHA-256, insieme
esatto dei sei altri file del delta; il manifest non contiene se stesso nella
lista, né richiede il proprio hash o il commit che lo contiene. Restano
`freeze_effective=false`, `freeze_tag=null`, review pending e firma assente.

## B. Pubblicazioni e bibliografia

✅ `git ls-remote origin` in sola lettura ha confermato:

| Ref | Oggetto remoto | Peeled |
| --- | --- | --- |
| `refs/heads/main` | `a00605862f627710347bd63c49f79a6d0a00135f` | — |
| `studio2-fase03-baseline-numerica-frozen-001` | `124262f5a6172a20965d019f220ff93954284922` | `38cb5f5eaa2e5a7dddfd53564a7d020b6b50fa1e` |
| `studio2-fase03-schema-insight-frozen-001` | `4d15c4fb915ea9db9f7425225d231746778f0ba1` | `3c64390bc4dd58c48cc4e1e388a38989b32b3143` |

Entrambi gli oggetti sono di tipo `tag`. `git merge-base --is-ancestor` conferma
che i due peeled e i commit bibliografici `e37c3db66689325b703bb99f3750ca3b5b287aab`
e `40911d0e3e7b75960e6973f3fd8f609e65ab6e05` sono antenati della base main.
`4503cb6` non lo è. La query del tag statistico previsto non restituisce alcun ref.

✅ Letti i record di pubblicazione 03.9 e 03.12; manifest storico R4 ricalcolato:
`d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`.
La rev.5 efficace della baseline e il record esterno R4 restano distinti dai
manifest fotografati ai rispettivi checkpoint.

✅ Inventario `ACQUISIZIONE_LETTERATURA_03_8.json`: **23/23**, complessivi
**6.407.129 byte**, ricalcolati sia sui file della copia isolata sia sui blob
`a006058:<path>`. Anche i due PNG PHM sono presenti nei blob Git e corrispondono:
page-6 286.075 byte, `0d4174ce35e88e941540b722ff1d632b5a0ed6527f66aeed7d2089eb6d4f2bf8`;
page-7 557.127 byte, `020f08386172d87c5ca45fecabc30a402904498bbb60754a745a4520104bed91`.
Non è stata eseguita una nuova ricerca bibliografica o lettura scientifica dei paper.

✅ Verbale bibliografico: 30.107 byte,
`551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`.
Addendum F6/F4: 34.808 byte,
`f2c29416664e27c2ecac7d439939f51f1a3f7313e2aba669bb39db7106cf0b8e`.
Entrambi coincidono con main. La consegna bibliografica storica descrive
l'acquisizione locale di allora; storia Git e riscontro remoto provano che il
raccordo è avvenuto. La bibliografia **non è più pending** nella matrice corrente.
I pending conservati nei file statistici byte-identici restano stati storici,
non un motivo per ripetere l'acquisizione o cambiare quegli hash.

✅ `soglie_normal/INTEGRAZIONE_03_5.md` registra 03.5 chiusa/pubblicata;
il commit `c486eee` che contiene il record è antenato di main. 03.5, 03.9 e 03.12
hanno perimetri distinti da 03.8. Matrice, report, APERTURA e manifest mantengono
03.8/Fase 03 aperte. FAR, U3, A/B e gli artefatti qualificati non sono riaperti.
Non sono state rieseguite le review scientifiche delle pubblicazioni o i download dati.

## C. Conti, regole operative e firma

✅ Ricalcoli aritmetici indipendenti, senza simulazioni:

| Blocco | Formula a R=1 | R=1 | R=3 |
| --- | --- | ---: | ---: |
| Nucleo | 8×8×7×3 +8×8×1×3 +8×8×3 | 1.728 | 5.184 |
| Swap misura | 4×8×7 | 224 | 672 |
| Ablation | 8×8 +4×3×7 | 148 | 444 |
| OOD | 2×3×8×3 | 144 | 432 |
| Somma | quattro blocchi | 2.244 | 6.732 |

Formula completa conforme nel nuovo §8.8, nel piano statistico e nel budget:
`N=2244R+2k·1[R=1]+16S+8U_nonriusato+10d+G_P+G_A+P_tot+X+Q`.
Audit aggiuntivo soltanto a R=1, E5 a R=1, FULL/librerie riusabili solo con le
identità richieste, canary 10/giorno, richieste distinte aggregate per modello,
X/Q separati da pilot e conformità. Esempio k=173, S=12, d=10, riusi, P_tot=160,
X=100, Q=0: **3.142/7.284**; non è budget vigente né attestazione T5.
Differenze storiche: 3.555−2.853=702; 702/2.853×100=24,605678…%, quindi 24,6%;
3.232−2.594=638. Il tetto 3.700 è superato nei punti aggiornati. Restano però
le incongruenze locali R1/R2, che impediscono di attestare l'allineamento completo.

✅ D2, D11, F6/F4 condizionati, m=0,125, alpha 0,05, H1→H2→H3 e sensibilità
H3 a 0,025 sono corretti nel riepilogo del piano generale. APERTURA riporta le
decisioni e le numerosità del lotto: 64+8+6+11=89. Le scorte non aggiungono
osservazioni. Il piano statistico preserva Hoeffding/Tango e i rispettivi limiti;
nessuna nuova decisione scientifica è stata inferita da questa review.

✅ Catena in APERTURA e consegna 03.10: conformità → eventuale unica remediation
sul diff autorizzato → sonda 3/6/9 per triplette complete → unico gate 40×3.
T3 ≥114/120 e astensione parsata per condizione, T4 zero troncamenti, T6 su coppia
parsata/validità (tre invalidi non valutabili), T9 16/16 insight in 8 richieste,
T11 assenza di astensione A local-unseen come limite esplorativo, non blocco
tecnico automatico. Nessun riuso degli output pre-remediation.

✅ `P_tot=128+b+8r+8a+t`, `8r+t≤15`: a b=9 e riserva consumata i massimi sono
152/160. La sonda dispone di quota 7 anche senza remediation: al massimo due
triplette se integra. Nessun retry gate, automatico, reset o finanziamento dalla
quota alternativo. Hard stop 200 cumulativo separato; la differenza non è spendibile.
Ledger persistente/atomico e controllo crash/resume richiesti nella consegna tecnica.

✅ Matrice e APERTURA distinguono freeze statistico da esecuzione: freeze 03.8
fissa candidati/criteri/catene, poi 03.11 verifica generabilità/trip/ammissibilità
prima delle chiamate sui test. Sostituti verificati individualmente e distinti;
convergenza su F5/caso irrisolto richiede sospensione e decisione esplicita.
Il completamento 03.11 non è richiesto prima del tag 03.8. D9/T5/03.10/03.11
restano obbligatori nei rispettivi momenti, senza dipendenza circolare.

✅ La matrice separa correttamente i punti dipendenti da D9 (identità dei ruoli,
configurazione, capienza, allocazione X/Q, latenze, calendario e misure T5) dalle
attività completabili ora. La consegna tecnica non sceglie modelli; rimane R4 nel
piano generale, da correggere come indicato sopra.

✅ Atto non firmato di 4.974 byte, hash verificato nella tabella A: lega il piano
a `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`.
Le istruzioni richiedono copia separata, commit/manifest/verbale esatti, luogo/data
reali e firma effettiva; acquisizione e impronta successive separate. Le approvazioni
in conversazione non sono trasformate in firma. Firma, review OK del delta,
documentazione, pubblicazione e manifest/tag finali restano i residui del tag;
l'assenza della firma non è di per sé un difetto di questo candidato preparatorio.

## D. Controlli documentali

✅ `git diff --check 70c84e3..4503cb6`: exit 0, nessun output.
✅ Collegamenti Markdown locali: **6/6 risolti**, tutti nel piano generale alle
righe 292, 1119, 1120, 1121, 1124, 1346; nessun frammento anchor in questi sei
link, nessun ulteriore href/src o link reference-style locale nei file del delta.
I percorsi di futura firma in codice sono istruzioni di output, non link rotti.
✅ Nessuna coppia MD/HTML modificata: il walkthrough è il passo successivo all'OK;
la sua parità non è stata richiesta come prerequisito di questa review.

`python3 docs/test_explanation.py`, eseguito nella copia isolata: **exit 1**,
**35 test, 14 fallimenti, 1 skip, 0 errori**, 0,106 s. Il conteggio dei fallimenti
comprende subtest: non significa quattordici metodi distinti. Tutti appartengono
a `__main__.UnifiedConversationChecks` e coincidono con gli identificativi
registrati in `CONTROLLI_REV10.json` e con la ripartizione del report:

| Metodo | Numero | Subtest / identificativi |
| --- | ---: | --- |
| `test_condition_c_contract_and_caveats` | 1 | phrase='non un risultato empiricamente misurato' |
| `test_one_flow_and_ordered_step_headings` | 1 | metodo senza subtest |
| `test_step27_qwen_frozen_results_and_limitations` | 9 | phrase='0.944444'; '0.916667'; '0.833333'; 'zero astensioni'; 'C1–C4: 4/4 PASS'; 'controllo secondario distinto'; 'budget nominale di 1024'; '36 aggregati B non cappati sono corretti'; più metodo senza subtest |
| `test_step27_qwen_protocol_stable_facts` | 3 | doc='html'; doc='md'; più metodo senza subtest |

Skip: `setUpClass (__main__.TutorialChecks)`, motivo
`legacy part-1 walkthrough is not present in this checkout`.
SHA-256 della concatenazione stdout+stderr acquisita durante questa esecuzione:
`5a7d1f09186f101e5004d780d638985af743805143ead458d978f0aa3122f01e`.
Non è stato creato un file log aggiuntivo. Non si dichiara la suite tutta verde:
è **invariata** rispetto alla baseline 35/14/1. Il test non certifica i nuovi
allineamenti, come dimostrano R1–R4. I 26 test statistici non sono stati rieseguiti:
si riusa il loro verbale storico a byte invariati, senza nuova griglia o simulazione.

## Comandi e tracciabilità della review

Comandi eseguiti, con percorsi relativi riferiti al worktree di review salvo dove indicato:

```text
shasum -a 256 <prompt assoluto nella copia di consegna>
git -C <worktree consegna> status --short --branch
git -C <worktree consegna> rev-parse HEAD HEAD^{tree}
git -C <worktree consegna> cat-file -t 4503cb6
git -C <worktree consegna> rev-parse 4503cb6^{tree}
git -C <worktree consegna> worktree add --detach /Users/luker/fot-tep-verifica-allineamenti-03-8-rev10 4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8
git status --porcelain=v1 --untracked-files=all
git rev-parse HEAD HEAD^{tree} origin/main
git cat-file -t <commit indicati e oggetti tag>
git log -9 --format='%H %s'
git show --format=fuller --stat 70c84e3
git diff --name-status 70c84e3..4503cb6
git diff --numstat 70c84e3..4503cb6
git diff 70c84e3..4503cb6 -- <i due file modificati>
git diff --check 70c84e3..4503cb6
git ls-remote origin refs/heads/main 'refs/tags/studio2-fase03-baseline-numerica-frozen-001*' 'refs/tags/studio2-fase03-schema-insight-frozen-001*' 'refs/tags/studio2-fase03-piano-statistico-frozen-001*'
git merge-base --is-ancestor <pubblicazione> a006058
git show 51782e8:<percorso>
git show 70c84e3:<prerequisito>
git show a006058:<percorso bibliografico>
python3 docs/test_explanation.py
```

I controlli SHA/dimensioni sono stati eseguiti con Python standard library in
here-document, senza salvare script: `json.loads`, `Path.read_bytes`,
`hashlib.sha256`, confronto diretto dei byte con `subprocess.check_output`
di `git show`. Il controllo link ha estratto le destinazioni Markdown,
escluso gli URL esterni e risolto i percorsi relativi al file sorgente.
Ricalcoli numerici eseguiti con aritmetica Python, nessun generatore scientifico.
Letture mirate con `rg`, `cat`, `sed`, `nl`; nessun AGENTS.md applicabile trovato.

Letti: contratto MAINTENANCE e prompt Verifica/Fase/Documentazione/Commit/Prompt;
fonti e precedenze del walkthrough; consegna rev.10; piano statistico integrale,
manifest, report, verbale rev.10, atto, budget, coordinamento e delta harness;
tutti i nuovi documenti e il diff completo; sezioni operative pertinenti del
piano generale e APERTURA; inventario bibliografico e consegna di acquisizione;
record pubblicazione 03.9/03.12 e integrazione 03.5; controlli rev.10.
Improntati i byte dei paper/PNG senza esaminarne nuovamente il merito.
Costo di lettura: ordine di alcune decine di migliaia di parole, oltre alle
verifiche meccaniche dei blob; nessuna nuova lettura dei segnali sperimentali.

## Uscita e limite del verdetto

**NON OK sul solo candidato `4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8`.**
R1–R4 richiedono un allineamento circoscritto del piano generale e nuova review.
Bibliografia acquisita, approvazioni A/B e artefatti rev.10 non vanno riaperti.
Il documento non costituisce firma, pubblicazione, freeze, chiusura 03.8/Fase 03,
autorizzazione al pilot o alle chiamate sperimentali.

Unico file prodotto: questo verbale, lasciato non tracciato nella copia isolata.
Nessun file candidato corretto; nessun commit, tag, push, firma, simulazione,
pilot, chiamata API sperimentale o run finale eseguito.

Chiusura della redazione: 2026-09-14T23:45:04.823809+02:00 .
