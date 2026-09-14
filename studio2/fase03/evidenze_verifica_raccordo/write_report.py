from pathlib import Path
import json,datetime,hashlib
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent
j=json.loads((O/'integrity.json').read_text());s=json.loads((O/'supplement.json').read_text());a=json.loads((O/'acquisizione.json').read_text())
rows='\n'.join(f"| `{x['path']}` | {x['bytes']} | `{x['sha256']}` |" for x in j['historical_deliveries'])
fails='\n'.join('- `'+x.removeprefix('FAIL: ')+'`' for x in j['guardian']['failure_ids'])
text=f'''OK — A: candidato Git e82b5a0; B: aggiornamento esterno della sola consegna. Verdetti limitati al raccordo documentale locale.

# Verifica indipendente circoscritta — 03.6 → 03.12 R4 → letteratura

Data: 2026-09-14, Europe/Rome. **Fase 03 aperta. Nessuna nuova certificazione scientifica.**

## 1. Oggetto esatto e indipendenza

- **A:** `e82b5a08bf642ad45f77e71832958207beb1181c`, confrontato con la base
  `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`: 64 percorsi, 28 commit raggiungibili aggiuntivi.
- **B:** file esterno
  `/Users/luker/fot-tep-raccordo-036-0312-letteratura/studio2/fase03/CONSEGNA_RACCORDO_03_6_03_12_LETTERATURA_2026-09-14.md`.
  È una modifica non committata; non appartiene al tree di A e non è stata sovrapposta al checkout verificato.
- **Sede effettiva della verifica:** `{R}`, nuovo worktree detached esattamente ad A.
  Base dei test in un secondo nuovo worktree detached:
  `/Users/luker/fot-tep-verifica-raccordo-base-c486eee`, esattamente alla base indicata.
- **Verificatore:** Codex Desktop, provider runtime `openai`, modello `gpt-6-astra`, reasoning
  esposto come `effort=high`. Sessione `01a0a0e2-5a0b-7bc3-a111-b41f24734216`.
  Prova: log `/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T19-06-23-01a0a0e2-5a0b-7bc3-a111-b41f24734216.jsonl`,
  riga 1 `session_meta`, riga 8 `turn_context`; estratti selettivi in `evidenze_verifica_raccordo/runtime_metadata.json`.
  L'identità del backend effettivamente servito oltre ai metadati runtime non è attestata.
- **Esecutore del raccordo:** provider `openai`, modello `gpt-5.6-sol`, `effort=high`, sessione
  `01a0a0b9-fc72-79b1-81b4-a4d5daa38f94`: modello e sessione distinti dal verificatore.
  Prova locale letta in sola lettura: log
  `/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T18-22-18-01a0a0b9-fc72-79b1-81b4-a4d5daa38f94.jsonl`,
  `turn_context` alle righe 8 e 347; output del commit e82b5a0 alle righe 317–318.
  Estratto in `evidenze_verifica_raccordo/esecutore_metadata.json`.

L'indipendenza riguarda questa valutazione del raccordo. Non è dedotta dal solo worktree e non
riapre né sostituisce le firme dei verbali scientifici precedenti.

## 2. Preflight e acquisizione separata di B

Prima di scrivere è stato verificato che:

- `/Users/luker/fot-tep` era sul branch `codex/studio2-soglie-normal`, HEAD
  `819b12e97fb94d501032655ec2f226139e6c5ca5`, con i numerosi non tracciati preesistenti;
- il sorgente era sul branch `codex/studio2-raccordo-036-0312-letteratura`, HEAD A, con la sola
  consegna modificata, nessuno staged e nessun non tracciato;
- `origin` era `https://github.com/sorrentinoluca/fot-phd.git`; tracking ref e `git ls-remote --heads origin main`
  concordavano sulla base `c486eee…` (osservazione iniziale 2026-09-14T17:06:47Z);
- l'elenco dei worktree comprendeva i cantieri concorrenti e le voci locked/prunable storiche:
  nessuna è stata spostata, ripulita o rimossa.

Prima della review sostanziale, alle **{a['time_utc']}**, sono stati letti i byte del file esterno,
confrontati con `git show e82b5a0:<percorso>` e conservati nella sede di verifica:

| Oggetto | Copia conservata | Byte | SHA-256 |
| --- | --- | ---: | --- |
| Consegna Git A | `evidenze_verifica_raccordo/CONSEGNA_GIT_A.md` | {a['A']['bytes']} | `{a['A']['sha256']}` |
| Consegna esterna B | `evidenze_verifica_raccordo/CONSEGNA_ESTERNA_B.md` | {a['B']['bytes']} | `{a['B']['sha256']}` |

B conserva **tutti i byte di A come prefisso** e aggiunge 7.352 byte / 117 righe (§8). Nessuna riga
preesistente sostituita. La patch è conservata in `delta_B.patch`; il controllo finale conferma
che la sorgente B è ancora byte-identica alla copia acquisita. Il file canonico della consegna
nel checkout A conserva il blob Git originale.

## 3. Esito distinto sui due oggetti

**A — OK documentale locale.** Storie raggiungibili, pacchetti preservati, conflitti documentali
composti senza perdita delle sezioni, rinvii nuovi funzionanti e stati delimitati correttamente.
L'OK non dichiara A scientificamente verificato in ogni sua parte: conserva l'applicabilità dei
verbali alle rispettive impronte e valuta solo il raccordo richiesto.

**B — OK documentale esterno**, esclusivamente per la copia di 17.597 byte con SHA-256
`{a['B']['sha256']}`.
L'inventario §8.3 coincide, percorso e stato A/M, con tutti i 64 percorsi del diff base→A.
§8.4 identifica correttamente HEAD, branch avanti di 28 commit, la sola consegna modificata e
l'assenza di staged/non tracciati nel sorgente. I rinvii §8.2 identificano report e verbali
esistenti. «Completato localmente» è coerente; B dichiara espressamente che l'aggiornamento non è
committato e non attesta integrazione/pubblicazione in main o freeze.

## 4. Controlli e fonti verificabili

### 4.1 Storia e conservazione dei pacchetti — ✅

`git merge-base --is-ancestor` conferma tutti i 19 riferimenti controllati in `integrity.json`,
compresa la base: catena evidence `cf1f70f → daf5dc5 → d54fa4a → 2f6dd8d → 54bbd0c → bb6d9e7 → c66bd8d`,
merge `7c99a83`; R4 `3c64390`, evidenze `43b31af`, preparazione `c0f4da0`, storico NON OK `9b1fac9`,
documentazione `c9f83c6`; letteratura `e37c3db` e verbale `40911d0`; raccordi `5806871`, `903f37f`
e acquisizione `601fb70`. I genitori effettivi sono registrati nello stesso JSON.
Il candidato bibliografico e il suo verbale restano due commit distinti; `601fb70` conserva le
consegne, senza riscrivere i commit delle sottofasi.

- **Evidence:** 13/13 file a `c66bd8d` identici per byte e SHA-256 in A; il solo percorso
  aggiuntivo nella cartella è la consegna storica. Contro il target scientifico `2f6dd8d`, i dieci
  file diversi dallo storage sono immutati; `ARTIFACT_STORAGE.json` incorpora il packaging v2
  già acquisito in `bb6d9e7`, non un nuovo delta di questa review. Manifest conservativo:
  1.283 percorsi unici, 61.208.618 byte; sono conteggi del manifest, non una nuova verifica del payload.
- `extract_evidence.py` SHA-256 `46b451c2d6d8b1627993828ac9bac39532562f2fa1b27955b8a20f098ba24e97` e
  `leakage.py` SHA-256 `c77ae5b11186c5b0df87b2f1df8800cb45fb25317e248fe8484d3e8283073887` coincidono
  con i pin di `extract_normal_evidence.py`, freeze 03.9 rev. 2/3 e verbale 03.9.
  Anche i quattro sorgenti congelati riusati coincidono con `PHASE_B_PROTOCOL_HASHES.json`;
  le nove impronte sorgente del freeze baseline rev. 3 coincidono.
- **Schema:** 20/20 file a `c9f83c6` identici; sola aggiunta della consegna storica. Manifest rev. 5,
  decisione e report sono byte-identici a `3c64390`. Le **18/18** impronte e dimensioni sono verificate
  ai riferimenti corretti: 10 al target R4, 6 a `d815ce96d928254de79209f02e11a561445764cd`,
  2 a `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155` e al frozen 03.7 `c16b533…`.
  Catena `previous_manifest_sha256` verso il manifest rev. 4 di `e058cb0` confermata.
  **Piano generale e letteratura correnti non coincidono con gli snapshot storici d815ce9:**
  è atteso per documenti viventi; non sono stati usati al posto dei blob pinnati.
- **Letteratura:** 23/23 file, **6.407.129 byte**, identici a `e37c3db` e alle impronte
  dell'inventario autorevole `ACQUISIZIONE_LETTERATURA_03_8.json` nel worktree piano-statistico-fix.
  Le quattro versioni di base dei documenti condivisi erano identiche fra `a572d1c` e `c486eee`;
  i quattro risultati finali sono identici al candidato. I 19 file aggiunti sono immutati.
  Verbale separato: 30.107 byte, SHA-256
  `551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`.
  Tutte le 23 impronte protette dell'inventario sono conservate.

Il diff globale contiene solo i pacchetti, le acquisizioni e i documenti previsti, zero percorsi
inattesi. Nessun delta nei pacchetti congelati del primo studio, selection, pseudolabel, baseline,
harness, piano statistico o paper-sections rispetto alla base. Identità dei file importati e
lettura degli hunk confermano l'assenza di nuove decisioni scientifiche nel raccordo.

### 4.2 Composizione PROVENIENZA e walkthrough — ✅

`studio2/PROVENIENZA.md` contiene la base come prefisso byte-identico: §§1–11 conservate.
Contiene anche la versione `7c99a83` come prefisso byte-identico: **§12 evidence** conservata.
La coda **§13 schema** coincide con §12 di `c9f83c6` dopo la sola rinumerazione del titolo.
Nessun duplicato nei tredici titoli numerati, nessun marker di conflitto nei tre documenti condivisi.

**§4.6** è identica a `7c99a83` e **§4.12** a `c9f83c6`, in MD e HTML; **§§4.5, 4.7, 4.9** sono
identiche alla base (impronte delle sezioni in `supplement.json`). Nessuna intestazione
preesistente persa. Gli hunk rimossi sono stati letti: riguardano aggiornamenti di stato U3,
rinvii all'estrazione/prototipi già esistenti, navigazione e sintesi; non eliminano altre sezioni.
Ordine delle sotto-sezioni: 4.1, 4.2, 4.3, 4.4, **4.5, 4.6, 4.7, 4.9, 4.12**.
La correzione F6 già nella base resta conservata; il vecchio collegamento errato non è reintrodotto.

### 4.3 Parità, conteggi, link e anchor — ✅ sul delta; ⚠️ arretrato noto

Controllo del contenuto con parser Markdown e HTML, non soltanto dei nomi dei file:

- §4.6: **56/56 blocchi** equivalenti e nello stesso ordine, includendo celle, titoli e liste;
- §4.12: **14/14 blocchi** equivalenti e nello stesso ordine;
- la sola equivalenza di presentazione normalizzata è `letteratura.md` ↔ `letteratura.html`;
  numeri, prosa e punteggiatura non sono sostituiti;
- letteratura: **182/182 righe tabellari** uguali cella per cella; **40/40 titoli di scheda** nello
  stesso ordine; **128 voci e 13 categorie**; nessun nuovo blocco MD del walkthrough privo del
  corrispondente HTML rispetto alla base.

Nei tre HTML modificati sono controllati **292 collegamenti locali**: **224 verso percorsi**
(è il conteggio dichiarato in A) e 68 frammenti sulla stessa pagina. **Zero percorsi o anchor
mancanti e zero ID duplicati**. Le coppie e PROVENIENZA producono complessivamente 535 occorrenze
locali; i soli 11 errori sono gli anchor legacy di `docs/letteratura.md`, tutti già presenti
nella base e dichiarati dal verbale bibliografico. Nessun nuovo errore. L'elenco esatto è in
`documents.json` (`existing_link_errors`); non vengono chiamati PASS né corretti qui.

I primi confronti testuali con stripping generico producevano falsi scarti di markup/spazi e
conteggi che includevano la legenda o ignoravano titoli non h4: non sono stati usati come esito.
`parity.json` contiene il confronto finale tramite parser, con legenda esclusa e titoli h4/strong
riconosciuti. `git diff --check` termina con **exit 2**, non PASS: whitespace nei file raw,
log e consegne/verbale acquisiti, già presente nei rispettivi oggetti di origine. Il log
`diff_check.log` contiene anche byte non UTF-8 del PDF trattato da Git come testo; tale limite
è dichiarato e il file è conservato raw. Nessuna normalizzazione del candidato.

### 4.4 Acquisizioni storiche e PNG — ✅

Confronto integrale tra copie sorgenti ancora presenti, blob del commit di acquisizione
`601fb70` e A: **3/3 consegne byte-identiche**, con dimensioni e SHA-256 seguenti.

| Percorso nel repository | Byte | SHA-256 |
| --- | ---: | --- |
{rows}

I percorsi sorgenti sono registrati in `integrity.json`. Non si interpreta lo stato storico
«non tracciato / non integrato» delle tre consegne come lo stato attuale di A.

Entrambi i PNG bibliografici sono file Git ordinari **100644**, recuperabili da A e da `e37c3db`,
non soltanto impronte senza payload:

| File, sotto `papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/` | Byte | SHA-256 |
| --- | ---: | --- |
| `page-6.png` | 286075 | `0d4174ce35e88e941540b722ff1d632b5a0ed6527f66aeed7d2089eb6d4f2bf8` |
| `page-7.png` | 557127 | `020f08386172d87c5ca45fecabc30a402904498bbb60754a745a4520104bed91` |

Log R4 server e verbale OK coincidono con `43b31af`: rispettivamente **7.459 byte** /
`a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972` e **21.288 byte** /
`d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e`.
Il precedente NON OK è conservato separatamente, identico anche alla copia del precedente
verificatore: **19.064 byte**, SHA-256 `5bd196820f74b7fbd5ee6736df2b72afc64afbbfb26459dc69f1fe5e15dafd19`.

### 4.5 Stati, ambito degli OK e futuro tag — ✅

La consegna A §§6–7 e B §8 mantengono queste distinzioni:

| Ambito | Stato supportato dalle prove |
| --- | --- |
| Raccordo A | committato e integrato soltanto nel branch locale dedicato |
| Aggiornamento B | esterno, sola consegna modificata non committata |
| Codice/documentazione 03.6, 03.12 e letteratura in main remoto | non integrati: i target sono antenati di A, non della base che è tuttora main remoto |
| Dati evidence-v2 e normal-dev-v1 | pubblicazione/riscaricamento già documentati nei record acquisiti; nessun nuovo download o controllo remoto dei payload in questa review |
| Schema R4 | OK sul target verificato; manifest rev. 5 pending e `tag_created=false` invariati |
| Freeze 03.12 | tag assente localmente e sul remoto; nessun freeze efficace/pubblicato attestato |
| 03.8, 03.9, Fase 03 | restano aperte; nessuna firma, allineamento, qualifica API o tag anticipati |

Ultimo riscontro remoto registrato: **{s['remote_observation']['utc']}**, `main` ancora
`c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`, nessuna ref del tag schema né peeled.
La proposta storica rev. 3 nomina `e058cb0`, ma è esplicitamente conservata come superata;
non è il target operativo. Prompt R4 corrente, preparazione, consegna A e B convergono sul solo
futuro destinatario consentito:

**`studio2-fase03-schema-insight-frozen-001` → `3c64390bc4dd58c48cc4e1e388a38989b32b3143`.**

Mai HEAD, merge, commit evidenze `43b31af` o candidato A. Un eventuale record di pubblicazione
va scritto dopo i riscontri effettivi. Questa verifica non autorizza né esegue il tag.

I conteggi test scientifici di A §5.2 sono trattati come risultati storici dell'integratore e
dei verbali, non come suite rieseguite dal sottoscritto. In particolare **25 PASS + 1 SKIP locale**
resta distinto da **26/26 senza skip nella trascrizione server**: quest'ultima non è un originale
scaricato dal server, non prova capienza dei prompt reali e non qualifica il servizio 122B.
L'OK bibliografico conserva i limiti Yin/Maurer/Westfall/Kish e non approva OOD, generabilità,
fattibilità o piano statistico. La discrepanza PHM F9–SPE resta nell'addendum; registro congelato
intatto. U3, FAR e A/B non sono ridecisi né estesi.

## 5. Guardiano confrontato con la base — nessuna regressione, suite NON PASS

Eseguito solo il controllo documentale richiesto:
`/usr/local/bin/python3` (Python **3.11.5**), comando `python3 docs/test_explanation.py`,
una volta su ciascuno dei due checkout isolati. Lo script è byte-identico fra base e A.

| Oggetto | Test | Failure | Errori | Skip | Exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| Base c486eee | 35 | 14 | 0 | 1 | 1 |
| A e82b5a0 | 35 | 14 | 0 | 1 | 1 |

I log completi coincidono dopo la sola normalizzazione del percorso di checkout e del tempo
trascorso. Coincidono **identificativi, parametri dei subtest, messaggi di errore e skip**,
non soltanto il numero. I 14 failure sono:

{fails}

Skip comune: `TutorialChecks.setUpClass`, motivo
`legacy part-1 walkthrough is not present in this checkout`. Non è un test superato.
Log integrali: `guardiano_base.log`, `guardiano_A.log`; confronto strutturato in `integrity.json`.
Il guardiano non certifica §14 né il contenuto scientifico dei nuovi pacchetti; i controlli
documentali specifici sono quelli di §4.3. Non sono stati rilanciati test evidence, baseline,
schema, regressioni scientifiche, estrazioni, calcoli, ricerca bibliografica o rendering dei PDF.

## 6. Rilievi puntuali, limiti e residui

**Nessun rilievo bloccante su A o B.** Restano visibili e fuori dal nuovo OK:

1. **Arretrato documentale:** 14 failure e uno skip storici del guardiano; 11 anchor Markdown
   bibliografici legacy; differenze di layout preesistenti fra rappresentazioni; whitespace raw
   preservato. Nessuna regressione attribuibile al raccordo.
2. **Pubblicazione non avvenuta:** l'ascendenza locale non soddisfa ancora la raggiungibilità
   in main richiesta da MAINTENANCE §8.5. Ricontrollare il remoto prima dell'eventuale integrazione;
   un avanzamento della base richiede review del nuovo raccordo, non un'estensione automatica di questo OK.
3. **B non acquisita in Git:** questo verdetto identifica la copia esterna tramite hash;
   la sua eventuale acquisizione successiva deve preservare questi byte o far verificare il nuovo delta.
4. **Residui delle sottofasi:** tag schema sul solo target R4 dopo gli atti richiesti;
   raccordi/pin 03.10 in attività separata; chiusure 03.8/03.9 e Fase 03 ancora pendenti.
   Il presente verbale non è `VERIFICA_FASE03.md` e non chiude la fase.
5. **Limite probatorio:** identità Git e byte dimostrano la conservazione locale dei pacchetti,
   non ripetono la verifica scientifica né attestano da sole ogni operazione passata narrata
   dall'integratore. Le prove di pubblicazione dei dati restano quelle storiche conservate.

Se un futuro delta ricevesse NON OK, preservare A, B e questo verbale; richiedere correzione
tracciata e **riverifica del solo delta**. Nessuna correzione è stata applicata mentre si verificava.

## 7. File prodotti, preservazione e letture

Prodotti esclusivamente questo verbale e la directory `evidenze_verifica_raccordo/` nella nuova
copia di verifica: snapshot A/B, patch, estratti metadata, script di controllo documentale,
impronte, risultati JSON e log. `MANIFEST_EVIDENZE.json` enumera dimensioni e SHA-256 delle
prove. Gli script non importano la pipeline scientifica.

Nessuna modifica a file tracciati del candidato o della base; nessuna scrittura nei worktree
sorgente, harness o paper-sections; nessun checkout altrui spostato, commit, merge, push, tag,
simulazione o chiamata API. Unico accesso remoto: lettura ref tramite protocollo Git (`ls-remote`).
Il sorgente conserva HEAD A e la sola modifica B iniziale, con SHA-256 invariato.

Letti: handoff rev02 esterno; MAINTENANCE e prompt Verifica/Prompt; consegna A e B; tre consegne
storiche; report, verbali e manifest pertinenti di evidence, schema R4 e letteratura, inclusi
precedente NON OK, preparazione e prompt/tag; inventario bibliografico 03.8 e pin/manifest baseline
03.9; contenuti e diff dei tre documenti condivisi; coppia letteratura, rinvii blueprint e README;
metadati runtime selettivi. La lettura dei verbali è mirata a oggetto, provenienza, risultati,
limiti e residui; nessuna rilettura scientifica dei paper. I file voluminosi sono letti come byte
per le impronte, senza estrarne o ricalcolarne i risultati. Costo di lettura indicativo:
alcune decine di migliaia di token; non è una misura del consumo fatturato.
'''
p=R/'studio2/fase03/VERIFICA_RACCORDO_DOCUMENTALE_036_0312_LETTERATURA.md';p.write_text(text)
print(p,len(p.read_bytes()),hashlib.sha256(p.read_bytes()).hexdigest())
