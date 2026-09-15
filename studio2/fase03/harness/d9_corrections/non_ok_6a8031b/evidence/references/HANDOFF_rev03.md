# Handoff Fase 03 — Studio 2 FoT-TEP — revisione 03

**Snapshot: 15 settembre 2026, Europe/Rome. Fase 03 aperta.**

Consegna locale richiesta da Luca per proseguire il coordinamento in un’altra finestra.
Sostituisce lo stato operativo di [HANDOFF_FASE03_2026-09-14_rev02.md](/Users/luker/fot-tep/studio2/fase03/HANDOFF_FASE03_2026-09-14_rev02.md), che rimane storico. Non sostituisce fonti scientifiche, contratti, manifest o verbali; non è una verifica indipendente, una firma o un’autorizzazione alle esecuzioni.

Fonti: conversazione e consegne dell’autore, handoff rev02, lettura delle ultime consegne e dei due verbali D04, istruzioni firma, checklist servizi, stato Git e query del remoto effettivo. Le verifiche scientifiche e i test riportati sotto sono attribuiti ai rispettivi verbali: **non sono stati rieseguiti per questo handoff**. Nessuna credenziale inclusa.

## 0. Ripartenza: cosa è cambiato e cosa non rifare

1. **03.9 è chiusa, pubblicata e congelata**, con rev.5 efficace. Non rifare normal_dev, prototipi, raccordo metriche o tag.
2. **03.12 R4 è chiusa, pubblicata e congelata**, sul target esatto 3c64390. Lo stato pending del manifest storico è intenzionalmente preservato.
3. **03.6, acquisizioni bibliografiche, raccordo documentale 03.15 e raccordo minimo metriche sono già integrati e pubblicati.** I vecchi residui del rev02 sono superati.
4. **D9 è approvata e registrata:** 122B producer principale e consumer; 27B producer alternativo per una libreria completa di 16 insight; consumer 122B fisso nello swap; Terra solo storico descrittivo interno. Non chiedere nuovamente questi ruoli.
5. **03.8:** allineamenti R1–R4 e recepimento documentale D9 hanno OK indipendenti già acquisiti. La nuova copia materiale per la firma è preparata, ma **non ancora firmabile**: richiede review del delta 8a3f7ba..7cf5238. L’atto originario ha stati temporali superati ed è preservato.
6. **03.10:** candidato aae29a9 ha ottenuto **OK limitato offline** dopo R01–R10 e C01–D04. Non risulta altro lavoro correttivo richiesto su quegli stessi byte. Restano da acquisire le due review D04 e registrare l’OK separatamente dalla consegna storica pending. Non riaprire il vecchio NON OK come se mancassero ancora le correzioni.
7. **Inventario servizi, richiesta metadati e checklist sono preparati e committati**, ma il messaggio non è stato inviato e i servizi non sono qualificati da quei documenti.
8. D9 **eseguibile**, ordine label 1a, metadati/configurazioni effettive, insight reali, capienza, T5 e pilot restano aperti. Un OK offline non è un GO e non chiude l’intera 03.10.

**Main GitHub verificato in questa sessione:** `a00605862f627710347bd63c49f79a6d0a00135f`.
I nuovi lavori 03.8/harness/D9 descritti sotto sono ancora locali. Prima di qualsiasi scrittura ricontrollare remoto e attività concorrenti.

## 1. Contratto, autorizzazioni e disciplina delle finestre

- Leggere [MAINTENANCE.md](/Users/luker/fot-tep/docs/MAINTENANCE.md), soprattutto §§1–5 e 8.1–8.6, e i prompt pertinenti in [docs/prompts](/Users/luker/fot-tep/docs/prompts). La copia principale è arretrata: per attività sui candidati leggere anche il contratto nella loro versione Git.
- Ciclo per sottofase: preparazione → review indipendente → correzione e review del delta → documentazione → commit/integrabilità → pubblicazione e freeze quando richiesti e ammessi. Distinguere sempre candidato tecnico, tree, successore documentale, stato locale, main e tag.
- Usare la finestra preparatrice per modifiche; conservare la finestra revisore indipendente. Non correggere il candidato durante la sua review. Dichiarare identità runtime effettiva e limiti, senza inventare modelli o sessioni.
- Conservare verbali NON OK, copie originali, manifest storici e acquisizioni byte-identici. Un pending storico non si cancella retroattivamente: aggiungere un record successivo.
- Per harness leggere la [skill fot-tep-harness-lessons](/Users/luker/.codex/skills/fot-tep-harness-lessons/SKILL.md) e, quando pertinente, i suoi riferimenti. È memoria di processo, non autorizzazione scientifica o sostituto del contratto. Nessuna nuova campagna di test è richiesta dal solo fatto che la skill esista.
- Walkthrough MD/HTML sempre insieme; integrazioni dei file condivisi seriali, un solo writer. Non sovrascrivere il walkthrough corrente con copie vecchie di un ramo.
- Il primo studio resta conservato e consultabile; Terra è riferimento descrittivo **interno**, non un braccio del nuovo studio o pooling nelle H1–H3. Riuso di dati solo con origine, commit, impronta, destinazione, ruolo e distinzione pre-specificato/post-hoc secondo MAINTENANCE.
- Nessun nuovo mandato a push, merge, tag, invii a terzi, API, inferenze o simulazioni deriva da questo handoff. Le approvazioni specifiche già registrate restano valide nel loro perimetro. Non chiedere di nuovo A/B, FAR, U3 o D9; non inferire firma o ordine label dalle approvazioni già date.
- Il perimetro storico della Fase 03 comprende preparazione e capability pilot fino al GO/NO-GO; produzione definitiva, studio finale e analisi seguono il piano. Report e verifica della Fase 03 sono futuri e devono verificare la coerenza delle sottofasi senza ripetere gli audit già conclusi.

## 2. Git, copie e fonti correnti

Repository codice: `https://github.com/sorrentinoluca/fot-phd.git`.
Repository dati: `https://github.com/sorrentinoluca/fot-tep-data`.

| Uso | Radice assoluta | Branch / HEAD dello snapshot |
|---|---|---|
| Copia principale, NON main aggiornato | /Users/luker/fot-tep | codex/studio2-soglie-normal / 819b12e; molti untracked preesistenti |
| Ultima pubblicazione baseline | /Users/luker/fot-tep-finalizzazione-baseline-039 | codex/studio2-finalizzazione-baseline-039 / a006058 |
| Allineamenti 03.8 e pacchetto firma | /Users/luker/fot-tep-allineamenti-038-r1-r4 | codex/studio2-allineamenti-038-r1-r4 / 7cf5238; pulito |
| Fonte statistica rev.10 | /Users/luker/fot-tep-piano-statistico-fix | codex/studio2-piano-statistico-fix / 51782e8 |
| Harness finale offline D04 | /Users/luker/fot-tep-harness-0310-d04 | codex/studio2-harness-0310-d04 / feaf1d3; pulito |
| D9 e inventario servizi | /Users/luker/fot-tep-proposta-d9 | codex/studio2-proposta-d9 / b65834d; pulito |
| Origine harness recuperato | /Users/luker/fot-tep/.worktrees/studio2-harness | codex/studio2-harness / 1ac06eb |
| Pubblicazione schema R4 | /Users/luker/fot-tep-pubblicazione-schema-insight-0312 | codex/studio2-pubblicazione-schema-insight-0312 / f1746e1 |
| Paper sezioni sorgente | /Users/luker/fot-tep-paper-sections | codex/studio2-paper-sections / d35b684 |
| FedAvg | /Users/luker/fot-tep/.worktrees/studio2-fedavg | codex/studio2-fedavg / bfbde77 |

Il branch locale main nel worktree di pubblicazione del consolidamento è fermo a 4f98a29: non è il main remoto corrente. Alcuni worktree storici puntano a mount /sessions e sono locked/prunable: non fare prune, rimuovere lock o riscrivere gitdir per comodità. Se una copia non è accessibile, usare `git show COMMIT:PERCORSO` dal repository che possiede gli oggetti.

“Harness completo non trovato” nei vecchi prompt significava assente da main o dal mount della finestra, **non inesistente**. La fonte 1ac06eb esiste; il recupero e le correzioni sono già eseguiti. Main contiene il raccordo minimo metriche, non ancora l’intero candidato D04.

## 3. Stato delle sottofasi

| Sottofase | Stato e residuo attuale |
|---|---|
| 03.1 Criteri | Chiusa, integrata e congelata. |
| 03.2 Catalogo D1 | Chiusa, integrata e congelata. |
| 03.3 Run fault sviluppo | Chiusa; 40 run verificati e release conservate. |
| 03.4 Perimetro Q8 | Chiusa, decisione attuata e integrata. |
| 03.5 Soglie Normal | Chiusa, pubblicata e congelata; FAR accettata e verificata. |
| 03.6 Evidence 697-D | Pacchetto verificato, dati v2 pubblicati/riscaricati, sorgenti e raccordo integrati. Non ripetere acquisizione o estrazione. |
| 03.7 Pseudolabel/agenti/derangement | Chiusa e taggata; ordine prompt-facing 1a ancora distinto e non approvato. |
| 03.8 Piano statistico | Rev.10 OK; allineamenti e D9 documentale OK acquisiti; copia firma proposta da verificare. Firma, raccordo finale, pubblicazione e freeze pendenti. |
| 03.9 Baseline numerica | Chiusa, tag remoto verificato, rev.5 effective=true pubblicata. |
| 03.10 Harness | Correzioni offline aae29a9 OK; due review da acquisire. Recepimento eseguibile D9 e qualificazioni ancora aperti. Nessun freeze. |
| 03.11 Finali/OOD | Non avviata; controlli dopo freeze statistico e prima delle chiamate sui test. |
| 03.12 Schema R4 | Chiusa, integrata, pubblicata, tag esatto verificato. |
| 03.13 Pilot | Non avviato come nuovo pilot qualificato. Prerequisiti e mandato ancora necessari; riconciliare eventuale consumo storico. |
| 03.14 FedAvg | OK locale acquisito sul pacchetto; smoke reale, valutazioni pertinenti e freeze pendenti. |
| 03.15 Paper | Delta e raccordo documentale precedente verificati/integrati/pubblicati; aggiornamenti alle nuove decisioni e stati ancora da fare. Nessun risultato nuovo da scrivere. |
| Letteratura | Acquisizione e integrazione completate, inclusi PNG; nessuna nuova ricerca richiesta per sanare vecchi pending. |

03.0 indica il preflight preliminare, non una sottofase sperimentale già qualificata. I record storici non vanno resi eseguibili per eredità.

## 4. Pubblicazioni concluse: riferimenti da preservare

### 4.1 Consolidamento 03.6 → 03.12 → letteratura, metriche e 03.15

Il raccordo seriale e la conservazione delle acquisizioni sono già arrivati in main. Candidato di consolidamento `04dee86140b3ff18882f9d164beef5ab7bf33e00`, OK indipendente, acquisizione `770d17c`, record `07a64e96c39ad73889f88978cd2ecbc719201b3e`, pubblicazione e relativo record `4f98a2973d2e1ca7932f19c34e9dd4c0498b8b43`.
Fonte: [registro pubblicazione consolidamento](/Users/luker/fot-tep-pubblicazione-consolidamento-0315-metriche/studio2/fase03/REGISTRO_PUBBLICAZIONE_CONSOLIDAMENTO_0315_METRICHE_2026-09-14.md).

Il raccordo minimo metriche qualifica mapping accuracy→accuracy_all, n→total, abstentions→abstained, non_abstained=total−abstained. Gli invalidi non diventano astensioni; general harness e baseline valid-only mantengono i loro perimetri. Non riaprire la qualificazione per il solo fatto di integrare il full harness.

Evidence: 40 run fault, 320 finestre, 697 componenti; release v2 con 1.283 file scientifici identici, già riscaricata. Fonti di provenienza e blob sono raggiungibili dalla storia pubblicata. Letteratura/PNG già integrati: vecchie richieste di acquisirli non sono correnti. Conservare la discrepanza bibliografica F9-SPE 5,6% nella fonte contro 6,6% nel registro congelato, senza riscrivere quest’ultimo.

### 4.2 Freeze 03.9

- Tag: `studio2-fase03-baseline-numerica-frozen-001`.
- Oggetto annotato remoto: `124262f5a6172a20965d019f220ff93954284922`.
- Peeled/commit pubblicato prima del tag: `38cb5f5eaa2e5a7dddfd53564a7d020b6b50fa1e`.
- Efficacia rev.5: `a00605862f627710347bd63c49f79a6d0a00135f`.
- [BASELINE_FREEZE_rev005.json](/Users/luker/fot-tep-finalizzazione-baseline-039/studio2/fase03/baseline_numerica/BASELINE_FREEZE_rev005.json): SHA-256 `c52c7231021f52fc7b60b3b55eb67b5205854176395eb809db4d20227978b7cc`.
- [PUBBLICAZIONE_BASELINE_03_9.md](/Users/luker/fot-tep-finalizzazione-baseline-039/studio2/fase03/baseline_numerica/PUBBLICAZIONE_BASELINE_03_9.md): SHA-256 `d99786ccac8ac0d2e076735daec8e2d25fe4da359025ba465494d09ebb7425f4`.

normal_dev: 40 run stream 60000–60039, 320 finestre, evidence/normal_dev_002; 9 prototipi globali e 16 locali. Media aritmetica, L1 media, pareggio assoluto 1e-12→astensione; nessuna soglia di distanza o fallback globale delle classi locali assenti. Release normal-dev-v1 1.336 file già verificati. DELTA_HARNESS rev.10 acquisito, non congelamento dell’intero piano 03.8. Rev.1–4 e pin storico rev.3 intatti.

### 4.3 Freeze 03.12

- Tag: `studio2-fase03-schema-insight-frozen-001`.
- Oggetto annotato remoto: `4d15c4fb915ea9db9f7425225d231746778f0ba1`.
- Peeled esatto: `3c64390bc4dd58c48cc4e1e388a38989b32b3143`.
- Evidenze `43b31afc1ff271594cb4bd21a39fa4469a8c83bc`; record pubblicazione `f1746e1e76c5657e5cb74ed765d2f22143f979ce`.
- [PUBBLICAZIONE_SCHEMA_INSIGHT.md](/Users/luker/fot-tep-pubblicazione-schema-insight-0312/studio2/fase03/schema_insight/PUBBLICAZIONE_SCHEMA_INSIGHT.md).
- Manifest storico rev.5: SHA-256 `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`; validatore `cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508`.

18/18 voci e 10/10 artefatti verificati; locale 25 PASS+1 SKIP, server 26/26 da trascrizione fornita dall’autore. Non è qualifica del nuovo servizio 122B né del futuro prompt completo. SCHEMA_FREEZE.json storico resta byte-identico e pending.

### 4.4 Altre chiusure

Tag selezione→`9faecaf7337e5864b7a3ad44cadb8971853dd260`; catalogo→`ab43f0b20f45cdb475c0caf52c6f7afcbae50891`; pseudolabel→`c16b533016db4617deb1ba96853253f117e8e32b`.
03.5: tag `studio2-fase03-soglie-normal-frozen-001`, oggetto `199c71b5f49537f2d77e5e4473446ab4a5509ecd`, peeled `98d958d870a10ada0d095893af9edb05a68ebc67`. Soglia 13.623626738268857, rango334/350, regola stretta S>threshold; FAR11/150 e secondario108/1500. Limiti già accettati in DECISIONE_AUTORE_FAR; non ricalibrare. Dettagli scientifici restano nelle fonti e nel rev02, non nelle vecchie liste di attività da fare.

## 5. 03.8: catena verificata e nuovo ostacolo prima della firma

Radice corrente: `/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/`.

| Passo | Commit / esito |
|---|---|
| Piano rev.10 originario | 6aaa5b3eebfed4ba502c25c0443caabd0051af21; OK, A/B approvate |
| Allineamento respinto | 4503cb6; NON OK R1–R4, acquisito e conservato |
| Correzioni allineamenti | 9a56d12d0633a0c9790c48792182f26fc6eb424a, tree e35e5ca661325657715dce6723e4e8ec09540101; OK |
| Acquisizione OK R1–R4 | 5b78421 |
| Acquisizione D9 | dc4d656 |
| Recepimento documentale D9 | 8a20c125bd294191c67ebdbf571832b1e32ac0f1, tree f58eedf88d8c9c30767425c945b5ee5c421cf0b7; OK |
| Consegna D9 | 7d9100a |
| Acquisizione OK D9 | 8a3f7ba706570201c5b622c4e0fc79529b1c8cfd |
| Nuovo pacchetto firma, NON verificato ancora | 7cf523805710633ec3b4fecd4eb8b7c9504076bf; parent 8a3f7ba |

Il verbale OK D9 acquisito è 21.644 byte, SHA-256 `bb8555792c5dad78fc3ffeaf5f797e3da427ef79ec1d3ebe7c840810f77c53e3`. Non ripetere questa acquisizione.

**Firma:** l’atto originario DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md (4.974 byte, hash 4a0a4e1fc2797ee7a81439110e164d43159c745007136c9dda7bed7759471cc8) contiene stati superati su D9, bibliografia e review. È preservato, non va semplicemente consegnato per la firma.

Nuova [copia proposta per firma](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_COPIA_FIRMA_REV10.md): 6.585 byte, SHA-256 `d470a6ce477f31f85951df8d877d786429a56e2f34a369407ae590494c39f605`.
[Inventario firma](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/INVENTARIO_PACCHETTO_FIRMA_03_8_REV10.json): 6.622 byte, SHA-256 `e83420d7d151bac88dea297bc880b8dc1dcde4d3999b61c32b96f76249ce00aa`.
[Istruzioni](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/ISTRUZIONI_FIRMA_MATERIALE_REV10.md).

**Prossima operazione:** review indipendente del solo delta 8a3f7ba..7cf5238, confronto integrale con atto originario, catena e impronte; nessuna firma o modifica del revisore. Dopo OK acquisito, Luca compila personalmente soltanto luogo/data effettivi e firma su copia separata. Destinazione normalmente DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.md nella stessa cartella; se PDF/scansione/firma digitale, conservarne formato e sorgente, senza ricostruzione artificiale in Markdown.

Dopo firma: acquisizione verificata, raccordo finale MD/HTML, integrazione/pubblicazione autorizzata, manifest finale e tag statistico al target da determinare correttamente. Il tag `studio2-fase03-piano-statistico-frozen-001` non risulta sul remoto interrogato. Non inventare target finale o retrodatare la firma.

### Regole statistiche già decise

Piano rev.10 SHA-256 `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`; DELTA_HARNESS rev.10 `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`.
D2=8; D11 {F1,F2}+{F14,F15}; m=0,125; α=0,05 unilaterale, sensibilità0,025; H1→H2→H3. A/B già approvate:
- A: contabilità completa per blocco/modello, nessun tetto corrente 3700; fattibilità misurata 1,20×T≤W. Nucleo1728/5184 a R1/R3, non totale; ablation148/444. Formula del budget: N=2244R+2k·1[R=1]+16S+8U_nonriusato+10d+G_P+G_A+P_tot+X+Q. Parametri operativi da istanziare, non numeri liberi o già approvati.
- B: freeze criteri/candidati OOD prima di generazione; 03.11 dopo freeze e prima delle chiamate sui test. Nessuna dipendenza circolare.
Se tempo non fattibile, sospensione organizzativa e decisione autore; non ridurre il disegno, cambiare R o allungare calendario automaticamente.

## 6. Harness 03.10: OK offline finale e acquisizioni da fare

[Consegna D04](/Users/luker/fot-tep-harness-0310-d04/studio2/fase03/harness/CONSEGNA_D04.json).

- Branch `codex/studio2-harness-0310-d04`, worktree `/Users/luker/fot-tep-harness-0310-d04`.
- Base documentale `97868f9d6ef281c2dd4ab1c6ffb67e2477ee5715`.
- Acquisizione review D03 `f0dca4d2d46a290d2ffeb1840abd46eb7664f0ae`.
- Contratto/test-first D04 `bf7774f2d153ecc50f27ba095f77b612933b4d26`.
- **Candidato tecnico OK `aae29a908356e4a4842a214fdc3db9bff26ec3ca`.**
- **Tree `4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`.**
- Successore documentale `feaf1d3c56ff142e1d1b4bc4dd243348c20bcb98`, escluso dal candidato tecnico.
- Manifest: 98 membri, 24.151 byte, SHA-256 `9fbad8c036075605a9bbdfdac84078259428b679fc33341ed98f21050a07efd6`.

La catena parte dal NON OK59b6b93, passa per correzioni0c8157f e ulteriori C01–C03/D01–D04. R01–R10 e successivi sono chiusi nei casi verificati sul candidato finale: non trasferire retroattivamente l’OK ai candidati respinti.

### Due review finali da acquisire separatamente

1. [Verbale Codex D04](/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/VERIFICA_D04.md): **21.340 byte**, SHA-256 `2fc9ed8e3303a779833f1b1dced7f9a70022603118d985280722bed0156a8fef`.
   Sessione revisore01a0a1ec-35a4-7870-9c39-9bf922d36c85, GPT-6 Astra/high; preparatrice sessione distinta01a0a204-abda-7a00-8466-f52f5bc84812, stesso modello/xhigh. Indipendenza di finestra, non diversità di modello.
   Esecuzioni macOS Python3.13.9/SQLite3.51.0: **128/128 mirati,163/163 discovery**, D04 8/8; differenziale respinto240 assertion fallite in6 degli8 metodi; V6/6,W4/4,Y7/7,Z5/5,U5/5. X01–X18 letterali18/18; X19–X24 conserva X23 letterale obsoleto fallito e adattamento già verificato1/1. Non dire “24/24 letterali” o “50/50 letterali”. Matrice nominativa dei50 metodi e limiti nel verbale. Guardiano eseguito NON PASS invariato.
2. [Verbale Claude D04](/Users/luker/fot-tep-harness-0310-d04-checks/VERIFICA_D04.md): **11.864 byte**, SHA-256 `0ce2cb9485e5047c5e87eed6f69d0f8ddd3e1b09a2c4a005f0a42e92ef4dc83c`.
   Configurazione dichiarata claude-opus-4-8, backend non dimostrabile dall’interno; VM Linux Python3.10.12/SQLite3.37.2. OK D04 circoscritto, differenziale e sonda propria. 128 mirati raccolti:127 verdi+1 env-bloccato da percorso hard-coded. Limiti su discovery scientifica, launcher dedicati e guardiano: non convertirli in PASS. Il verbale Codex offre esecuzioni correnti complete nell’ambiente di riferimento, ma non riscrive i risultati Claude.

**Residuo immediato:** acquisizione byte-identica dei due verbali, provenienza/impronte e prove pertinenti; record documentale successivo dell’OK limitato offline. CONSEGNA_D04.json registra ancora pending: conservarne lo storico, registrare il nuovo stato senza alterare i byte certificati. Preservare fixture volutamente false fuori dagli input scientifici. Coordinare un solo writer nella finestra preparatrice; non riavviare tutta la campagna di review in assenza di nuovo delta o difetto concreto.

D04 sposta la verifica dell’inventario dei tentativi al punto di decisione, in transazione, includendo gli stadi contribuenti alla quota. D03 conserva digest ricalcolabili e binding durevole delle prove zero-token; legacy senza digest/link fail-closed e niente backfill. Le lezioni persistenti precisano transazioni, raw durevoli, retry, validazione agli ingressi, prove rosso/verde e limiti degli OK.

**Non ancora fatto:** D9 nei percorsi eseguibili, ordine label, configurazioni/identità reali, produzione insight reali, qualificazioni e fattibilità, pubblicazione/freeze del full harness. Il preflight storico resta bloccato. Non basta sostituire UNDECIDED con un nome per qualificare il sistema.

## 7. D9 e servizi: decisioni ferme, metadati ancora da acquisire

[Record D9](/Users/luker/fot-tep-proposta-d9/studio2/fase03/DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md), commit `aaba893dff8c62f9f9281eec7423eee020235e03`.
Proposta originale `95ff8571af02bab79094ed1a6be3f6a7b410c711`, preservata ma raccomandazione27B principale superata dalla scelta dell’autore. Anche la vecchia proposta harness con Terra alternativo è superata.

**D9:** P=C=122B; P_alt=27B; nuova libreria alternativa completa16 insight; stessi casi previsti per lo swap e C122B fisso. Non è un confronto fattoriale2×2, non stima l’effetto consumer e non prova universalità del metodo. Non scegliere i ruoli in base all’accuratezza del pilot. Il27B non ha automaticamente un gate consumer o funzione di fallback. Terra non richiede nuove chiamate/qualificazioni.

Inventario preparatorio committato `b65834d954b48c7daae748c80c3e7e7c568f8d47`,26 riferimenti controllati:
- [Inventario servizi](/Users/luker/fot-tep-proposta-d9/studio2/fase03/INVENTARIO_SERVIZI_D9_2026-09-15.md).
- [Richiesta metadati, NON INVIATA](/Users/luker/fot-tep-proposta-d9/studio2/fase03/RICHIESTA_METADATI_QWEN_DA_INOLTRARE_2026-09-15.md).
- [Checklist qualificazione futura](/Users/luker/fot-tep-proposta-d9/studio2/fase03/CHECKLIST_QUALIFICAZIONE_D9_2026-09-15.md).
Questi documenti precedono l’OK D04 e possono descrivere l’harness ancora in review: è stato temporale storico, da raccordare quando recepiti, non motivo di rifare D04.

122B dichiarato operativo: base URL `http://cygnusx1.portici.enea.it:8000/v1`, alias `qwen3.5-122b`, modello annunciato Qwen3.5-122B-A10B-FP8,131072 contesto/16384 output. **Omettere temperature dal payload**, non null/0.6/stringa vuota;0,6 è default dichiarato. Quota token detta illimitata e assenza cache dichiarata non eliminano limiti, tempi o ledger.
27B storico: Qwen/Qwen3.8-27B-FP8, revision017b9c7af6b5689d5dd426a76e0bc077eb5ca20a, alias fot-exp2-consumer, vLLM0.28.0, contesto16384, loopback8001 da riconfermare. Il nome e l’architettura registrata Qwen3_5ForConditionalGeneration richiedono chiarimento del gestore, non correzione intuitiva. Accesso Windows storico non prova disponibilità SSH dal Mac.

Acquisire pesi/revisioni, tokenizer/template e byte/hash, serving/parser/thinking, limiti combinati, sampling, identità/usage/fingerprint, errori/prove zero-token, disponibilità/calendario. Il contatore canonico R4 dei campi insight resta distinto dal tokenizer/template del prompt completo del servizio effettivo.

**Consumo storico:** la checklist segnala una sonda S con4 richieste riportate/3 inferenze completate. È un record storico da riconciliare con fonti e ledger prima di nuovi invii, non una nuova esecuzione di questo handoff o un pilot già qualificato. Non assumere contatore totale zero dal fatto che le finestre correnti non abbiano inviato richieste; non ricontare due volte consumi acquisiti.

**Ordine label 1a ancora non approvato:** MHMU4, HEW25, FD3GZ, 3ZGWQ, GSX3L, 4AMS4, TYFPG, QRCCB, poi Normal; identico fra agenti/condizioni. Separato da label_space canonico, mapping, assignment e derangement. Non rifare sorteggio03.7 né dedurre approvazione dalle fixture. Presentare la decisione concreta all’autore quando necessaria.

## 8. Sequenze operative future e sottofasi rimanenti

### 8.1 Pilot 03.13 e harness eseguibile

Acquisire OK offline → recepimento D9 eseguibile in delta separato con configurazioni documentate e barriere → review del nuovo delta. Non trasferire l’OK aae29a9 ai futuri byte.

Prima degli invii: fonti di sviluppo/schema congelati, metadati e permessi/configurazioni pertinenti, ordine label e ledger riconciliato. Sequenza prevista: conformità producer principale8 richieste/16 insight → eventuale unica remediation autorizzata sul diff concreto e stessi8casi → prompt consumer completi/capienza → sonda3/6/9 → freeze configurazione → gate unico40×3 → criteri, latenze e T5/altri prerequisiti. La libreria non può essere prerequisito della chiamata che deve crearla; è invece necessaria per i prompt consumer completi con14peer.

Conformità alternativo27B8richieste per16insight: collocazione nel pilot o differimento da esplicitare e contabilizzare una sola volta. Nessuna seconda riserva remediation o gate consumer27B.
P_tot=128+b+8r+8a+t;8r+t≤15; massimi152/160; hard stop200 cumulativo distinto, differenza non spendibile. Sonda retry soltanto per triplette complete con prova zero-token e riserva protetta; nessun retry gate, nessun reset per alias/directory/restart. Timeout senza prova resta irrisolto.
T3≥114/120 e copertura astensione parsata per condizione;T4zero troncamenti;T6validità/coppia(abstain,predicted_label), non differenze raw. Tre invalidi→non valutabile, niente GO. Divergenza→R3 pendente fattibilità;T11 resta nel ruolo esplorativo previsto, non nuovo blocco automatico.

### 8.2 03.11

Dopo freeze statistico:64fault+8Normal=72primari,+6OOD+11scorte=89run nel caso previsto con2OOD. Scorte sostitutive, non osservazioni aggiuntive. F6→F5→F12;F4→F11→F5; controllo tecnico individuale e OOD distinti. Convergenza aF5 richiede decisione, non duplicazione. Nessuna scelta su prestazioni. Generazione dall’autore secondo mandato; verificare inventario seed/stream corrente e disgiunzione, non copiare un elenco storico come nuovo allocatore. Dati del pilot sono development, non test finali.

### 8.3 03.14 FedAvg

Fonte `/Users/luker/fot-tep/.worktrees/studio2-fedavg/studio2/fase03/fedavg/`, candidato OKd56354934d2b5f88dace3f9b312fcf64ce3cf42b, acquisizionebfbde772bf14c496ff0b255008904d3deb424e54. Verifica11/11 e fixture non equivalgono a smokeTEP reale. Normal_dev ormai pubblicato: quel vecchio blocco è superato. Prima dello smoke leggere ricetta, interfacce, sbilanciamento320Normal/40finestre per fault; non cambiarli per migliorare prestazioni. Esecuzioni, valutazioni e freeze richiedono mandato e prerequisiti.

### 8.4 03.15 e chiusura della fase

Sezioni scientifiche e raccordo precedente già pubblicati attraverso consolidamento. Da recepire successivamente D9 effettiva, stato03.8 e harness qualificato nei rispettivi limiti, con nuovi delta verificati; non inventare risultati, abstract/conclusioni o riclassificare Terra come nuovo braccio. Coordinare serialmente piano, paper e walkthrough; non sovrascrivere acquisizioni e §4.12 dello schema.
Alla chiusura Fase03: report indice delle sottofasi, verifica di coerenza e documentazione di fase, poi pubblicazione richiesta. Nessuna chiusura anticipata per il solo OK del codice.

## 9. Prime operazioni eseguibili in parallelo

| Ramo | Operazione immediata | Finestra |
|---|---|---|
| A — harness | Acquisire entrambe le review D04 con impronte/provenienza e record separato dell’OK offline; preservare il candidato e il pending storico | Preparatrice harness D04, non revisore |
| B — firma03.8 | Review indipendente delta8a3f7ba..7cf5238; confronto atto e inventario, senza firmare | Revisore03.8 rimasto indipendente o nuova finestra |
| C — servizi | Usare richiesta già pronta; raccogliere risposte/metadati quando disponibili. Nessun nuovo inventario duplicato o invio non autorizzato | FinestraD9; messaggio all’autore/gestore solo su mandato |

Dopo B: acquisire OK e chiedere la firma reale sulla copia verificata; non ancora prima. Dopo A: preparare recepimento eseguibileD9 e sua review, con dati mancanti espliciti e servizi bloccati finché necessario. Ordine label è una decisione separata presentabile all’autore. Preparazioni in worktree distinti possono sovrapporsi; merge/pubblicazione, aggiornamenti condivisi e tag restano seriali e autorizzati.

Preferenze di coordinamento: Luca usa finestre già esistenti e chiede prompt distinti da inoltrare; non aprire nuove task o inviare messaggi alle altre finestre automaticamente. Riutilizzare la preparatrice informata per implementazione e la revisore informata per nuove review, preservando indipendenza. I modelli consigliati per le finestre non sono i modelli oggetto dell’esperimento.

## 10. Guardiano e limiti dello snapshot

Guardiano documentale:35test,14fallimenti storici,1skip,0errori nei verbali correnti; **NON PASS non bloccante per questi delta**, non suite verde. Confrontare identificativi/subtest, non solo conteggio; nuovi fallimenti richiedono diagnosi. Le suite harness non dimostrano qualifica scientifica dei servizi. Non sommare metodi, sottocasi, assertion, processi e suite sovrapposte.

Questa finestra ha verificato in sola lettura main/tag remoti, worktree principali interessati e impronte dei due verbali D04 e dei due artefatti firma. Non ha acquisito le review nei branch, eseguito test, chiamato servizi o pubblicato alcunché. La creazione di questo handoff lascia inalterati i pacchetti sperimentali e non è un nuovo OK. Le letture di fonti storiche conservano i loro limiti dichiarati.

## 11. Messaggio per la nuova finestra

```text
Stiamo proseguendo lo Studio 2 FoT-TEP, Fase 03.
Leggi /Users/luker/fot-tep/studio2/fase03/HANDOFF_FASE03_2026-09-15_rev03.md.
Sostituisce lo stato operativo del rev02, non le fonti scientifiche.
Verifica branch, worktree e main sul remoto effettivo prima di scrivere.
03.9 e03.12 sono già chiuse/pubblicate/congelate; non rifare i relativi lavori.
D9 è approvata:122B producer principale e consumer,27B producer alternativo,
Terra solo storico descrittivo interno. Non chiedere nuovamente i ruoli.
Harness aae29a9 ha OK limitato offline: acquisire le due review e registrarlo;
non riavviare le correzioni già concluse. D9 eseguibile e qualificazioni restano aperte.
La copia firma03.8 a7cf5238 è una proposta ancora da verificare, non ancora firmabile.
Inventario servizi e richiesta metadati sono pronti; nessun invio è stato autorizzato.
Inizia indicando soltanto le prime operazioni eseguibili e quali possono procedere
in parallelo. Quando chiedo prompt, produci messaggi distinti e indica finestra adatta.
Non riaprire A/B,FAR,U3 o approvazioni già registrate. Nessuna simulazione,
inferenza,pilot,push,merge o tag è autorizzato dalla sola lettura dell’handoff.
```
