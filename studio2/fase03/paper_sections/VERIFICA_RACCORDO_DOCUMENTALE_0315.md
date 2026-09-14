NON OK su A — due correzioni documentali circoscritte richieste. OK su B come sola consegna esterna identificata per impronta; B non sana i rilievi del candidato A.

# Verifica indipendente del raccordo documentale 03.15

**Sottofase:** S2-F03-0315, studio 2 FoT-TEP, Fase 03. **Data:** 14 settembre 2026, Europe/Rome.
**Perimetro:** genealogia, conservazione e documentazione successive agli OK scientifici.
Nessuna nuova review di e82b5a0, cf79e81 o 91a880b; nessun verdetto negativo sul loro merito scientifico.

## 1. Identificazione, isolamento e preflight

| Oggetto | Riferimento effettivo |
| --- | --- |
| Base comune già verificata documentalmente | `e82b5a08bf642ad45f77e71832958207beb1181c` |
| Pacchetto con OK scientifico acquisito | `d35b684acbfd1f357bc34f3a21cebb18e8a6bea0` |
| Merge locale | `18aa3bbf1284a41e20bdc4fc521c98c315ca9614` |
| Acquisizione consegna | `705f1c4ca61375d51bb69f20e0de613cfb39bf1a` |
| Documentazione MD/HTML | `532cc77bc3d5d046161b6334e1a7b24ac1e7019f` |
| **A, candidato Git** | **`9b6bd64c3e23f03d09272dda43c1a043305add50`** |
| Worktree sorgente, solo letto | `/Users/luker/fot-tep-raccordo-0315-local` |
| Branch sorgente | `codex/studio2-raccordo-0315-local` |
| Nuova copia isolata del verificatore | `/Users/luker/fot-tep-verifica-raccordo-0315-9b6bd64` |
| Branch/HEAD del verificatore | nessun branch; detached esattamente ad A |
| Base per il solo guardiano comparativo | `/Users/luker/fot-tep-verifica-raccordo-e82b5a0`, detached a e82b5a0; file tracciati intatti |

Prima di creare la copia sono stati letti branch, HEAD, stato, lista worktree, remoti e main
remoto. Il sorgente aveva una sola modifica tracciata: la consegna corrente; nessuno staged e
nessun non tracciato. `origin` è `https://github.com/sorrentinoluca/fot-phd.git`.
Tracking ref e `git ls-remote --heads origin main` concordavano su
`c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` alle **2026-09-14T17:42:52Z**.
Il controllo finale alle **2026-09-14T17:49:24.185489+00:00** conferma lo stesso main; i branch remoti
`codex/studio2-raccordo-0315-local` e `codex/studio2-paper-sections` non sono pubblicati.
Nessun checkout altrui spostato; worktree locked/prunable e cantieri concorrenti preservati.

**Verificatore:** Codex Desktop, provider runtime `openai`, modello `gpt-6-astra`, `effort=high`.
Sessione **`01a0a0e2-5a0b-7bc3-a111-b41f24734216`**. Prova locale: log
`/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T19-06-23-01a0a0e2-5a0b-7bc3-a111-b41f24734216.jsonl`,
`session_meta` riga 1 e `turn_context` del presente incarico riga 256.
Il cwd iniziale del runtime era `/Users/luker/fot-tep`; i controlli sul candidato sono stati
eseguiti nella copia isolata sopra indicata.

**Esecutore del raccordo/documentazione:** `openai`, `gpt-5.6-sol`, `effort=medium`, sessione
`01a0a0e3-c3bd-7523-90ca-b5f28a40461f`. Prova: log
`/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T19-07-56-01a0a0e3-c3bd-7523-90ca-b5f28a40461f.jsonl`,
turn context alle righe 8 e 379; output della creazione di 9b6bd64 riga 329.
Estratti selettivi conservati in `metadata_runtime.json`. Modello e finestra del raccordo sono
diversi da quelli del verificatore. Non si deduce l'indipendenza dal solo worktree; non si
attesta l'identità del backend oltre ai metadati esposti. La precedente verifica documentale
della base fu eseguita in questa stessa finestra: viene utilizzata come prova già acquisita,
non ripresentata come una seconda verifica indipendente della base.

## 2. Acquisizione separata della consegna esterna B

Prima della review sostanziale, alle **2026-09-14T17:43:17.293681+00:00**, è stata acquisita senza normalizzazioni
la versione corrente di:
`/Users/luker/fot-tep-raccordo-0315-local/studio2/fase03/paper_sections/CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md`.

| Oggetto | Copia conservata sotto `evidenze_verifica_raccordo_0315/` | Byte | SHA-256 |
| --- | --- | ---: | --- |
| Blob della consegna in A | `CONSEGNA_GIT_A.md` | 5484 | `11143a5a3304370c23845b6a7b571aabe05fa48d6aa98027634c892fb5aa632d` |
| **B, consegna esterna corrente** | **`CONSEGNA_ESTERNA_B.md`** | **11046** | **`b7398a24f57f18b59be4cd77e40785a286805e619f76eb65d8642f0d941ba607`** |

B **non è una semplice appendice byte-prefix**: aggiunge ID/attività/esito, sostituisce la riga
«Stato» nell'apertura, esplicita il commit corrente e aggiunge §§6–9. Il delta completo è
`delta_B.patch`. B non è stata sovrapposta al file tracciato nella copia A. Il controllo finale
conferma i byte di B ancora identici al sorgente, con la stessa unica modifica iniziale.

**Esito distinto di B: OK come record esterno.** La tabella §6 coincide esattamente con tutti i
**22 percorsi** del diff e82b5a0→A; §7 distingue correttamente commit, file modificato, staged e
non tracciati; §§8–9 conservano il carattere locale e i residui. Le impronte citate coincidono.
B §2 descrive correttamente entrambe le consegne aggiunte al pacchetto. Non attribuisce nuovi OK
scientifici al merge o al walkthrough. L'OK di B vale esclusivamente per l'impronta sopra:
non approva A e non equivale alla sua acquisizione in Git.

## 3. Rilievi documentali che impediscono l'OK di A

### R1 — la raggiungibilità delle fonti è dichiarata in modo eccessivo

**Localizzazione:** `docs/fot_walkthrough_conversazione_studio2.md:1413` e replica
`docs/fot_walkthrough_conversazione_studio2.html:1101` (§4.15, riassunto).
Il testo afferma: «Questa operazione rende storia, fonti, bozze e verbali raggiungibili da un
candidato locale». Nel contesto esplicito di un raccordo Git, la frase include indebitamente
l'intero insieme delle fonti nella raggiungibilità dal candidato.

**Prova primaria:** `FONTI_DELTA_0315.json` contiene 54 fonti. Il riscontro byte/SHA-256 è positivo
per tutte, ma `git merge-base --is-ancestor <commit-fonte> 9b6bd64` distingue:

- **44 fonti** a commit antenati di A;
- **8 fonti** a commit presenti nel repository locale ma **non antenati di A**;
- **2 fonti locali prive di commit**, H e PROMPT-0315, non contenute nel tree A.

Le otto fonti esterne all'ascendenza sono:

| Percorso | Commit pinnato, non antenato di A |
| --- | --- |
| `studio2/fase03/piano_statistico/PIANO_STATISTICO.md` | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` |
| `studio2/fase03/piano_statistico/PIANO_STATISTICO_FREEZE.json` | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` |
| `studio2/fase03/piano_statistico/BUDGET_RISORSE_REV10.md` | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` |
| `studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md` | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` |
| `studio2/fase03/piano_statistico/APPROVAZIONE_ADDENDUM_03_8.md` | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` |
| `studio2/fase03/piano_statistico/ADDENDUM_DECISIONI_RESIDUE_03_8.md` | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` |
| `studio2/fase03/piano_statistico/CONSEGNA_REV10.md` | `51782e8c40069c0a2310afafc36907a61d517ff6` |
| `studio2/fase03/piano_statistico/VERIFICA_PIANO_STATISTICO_REV10.md` | `51782e8c40069c0a2310afafc36907a61d517ff6` |

Le due fonti prive di commit sono l'handoff rev02 e
`/Users/luker/fot-tep/studio2/fase03/paper_sections/sottofase_3_15.md`.
Le loro copie di prova sono conservate in questa sede di verifica, senza incorporarle in A.
Il fatto che `git show <pin>:<path>` funzioni nel repository condiviso non significa che quei
commit siano raggiungibili partendo da A. Non è un problema delle impronte né dell'OK
scientifico: è una confusione introdotta dalla nuova formulazione documentale.

**Correzione necessaria, solo MD/HTML:** restringere l'affermazione alla storia e ai 17 file
03.15 effettivamente acquisiti; dichiarare che il registro delle fonti è conservato, mentre
le fonti S08/S08-consegna restano ai pin esterni alla storia del candidato e H/PROMPT-0315 sono
fonti locali senza commit. Distinguere disponibilità locale, riferimento pinnato e ascendenza.
**Non è richiesto integrare 03.8 né cambiare le fonti o i loro manifest per risolvere R1.**

### R2 — l'eccezione all'identità della cartella è incompleta al candidato finale

**Localizzazione:** `docs/fot_walkthrough_conversazione_studio2.md:1455` e replica
`docs/fot_walkthrough_conversazione_studio2.html:1135` (§4.15, artefatti).
La cartella è detta identica a d35b684 «salvo questa consegna», riferita a
`CONSEGNA_0315_2026-09-14.md`.

**Prova primaria:** `git diff --name-status d35b684 9b6bd64 -- studio2/fase03/paper_sections/`
mostra **due** aggiunte: la consegna storica acquisita in 705f1c4 e
`CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md` creata in 9b6bd64.
L'affermazione era esatta al commit documentale 532cc77, prima della seconda consegna, ma non è
delimitata temporalmente nel testo del candidato finale. A §2 e B §2 già dichiarano correttamente
due aggiunte: la coppia walkthrough deve avere lo stesso perimetro esplicito.

**Correzione necessaria, solo MD/HTML:** dire che i 17 file del pacchetto d35b684 sono invariati e
che le due consegne sono aggiunte successive; in alternativa delimitare esplicitamente il
confronto al commit 532cc77 e registrare la seconda acquisizione. Nessuna riscrittura delle
consegne storiche, dei report improntati o delle bozze.

## 4. Controlli positivi e conservazione

### 4.1 Genealogia e ambito del diff — ✅

Il merge 18aa3bb ha **esattamente due genitori ordinati**: e82b5a0, d35b684.
La catena successiva è lineare: 18aa3bb → 705f1c4 → 532cc77 → 9b6bd64.
La catena paper è preservata: cf79e81 → 50f07a9 → 1d480fd → bcb462d → 91a880b → dc6e30c → d35b684.
Tutti i candidati e i verbali 03.15 sono recuperabili da A, così come le storie 03.6, schema R4
e letteratura già acquisite nella base. L'eccezione sulle fonti statistiche è precisamente R1.
Genitori e ascendenze complete dei 18 riferimenti controllati sono in `integrity.json`.

705f1c4 aggiunge soltanto `CONSEGNA_0315_2026-09-14.md`; 532cc77 modifica soltanto la coppia
walkthrough; 9b6bd64 aggiunge soltanto il record di integrazione corrente. Nel diff base→A:
**3 documenti condivisi modificati + 17 file paper importati + 2 consegne aggiunte = 22 percorsi**.
Zero percorsi inattesi. Nessuna promozione in `docs/paper/`, nessun delta nei pacchetti degli
altri cantieri, nel corpus, nei PNG bibliografici o negli artefatti congelati della base.
Questo è un confronto di conservazione, non una nuova verifica del loro contenuto scientifico.

### 4.2 Identità del pacchetto — ✅

I **17/17 file** del pacchetto d35b684 coincidono byte per byte nel merge 18aa3bb, nel blob A
e nel checkout isolato. Il registro delle fonti e i suoi stati storici sono invariati.
Impronte calcolate direttamente dai blob e dai file, senza eseguire codice scientifico:

| File sotto `studio2/fase03/paper_sections/` | Byte | SHA-256 in A, identico a d35b684 |
| --- | ---: | --- |
| `ACQUISIZIONE_VERIFICA_DELTA_0315.md` | 6764 | `debb9e19bb08062ea8091d593b2eddd3d56c5f717675c5e2c411b70e601a489d` |
| `ACQUISIZIONE_VERIFICA_PAPER_SECTIONS.md` | 6546 | `808f75b57500bacf48369a4892ee0416a7c9beffae436a4aa79bf4c85aacdb9e` |
| `CONTROLLI_DELTA_0315.json` | 14284 | `13bd666acfab1d11cb3ea655df5d3bdac0e636d33df68346ee3057f74974e63f` |
| `FONTI_DELTA_0315.json` | 15039 | `dc01cd71e1b7bae0b65a56de0de50c6db8ac2db426cb471b5110fc7a8d694610` |
| `PIANO_SEZIONI.md` | 8853 | `a7deb8fe2c9643626e47c111ed0f7dfd24f5b6f4db4a42de09b372983c1ed6a8` |
| `PROMPT_VERIFICA_DELTA_0315.md` | 10564 | `cc6a13cea07fe72a02269b3ebf8ba0e96e0a1273b9ba2a3d9b6b2ee5745b79ab` |
| `REPORT_ACQUISIZIONE_VERIFICA_PAPER_SECTIONS.md` | 2360 | `6b0800fd8b8359e839b799b0a95be5de04406d2509f56352ea27cc56d3bd1f89` |
| `REPORT_DELTA_0315.md` | 15498 | `1f59eabf8070f1f4b7b77d89564d4e3593308469e8d8aee56676c93dbabd40f1` |
| `REPORT_PAPER_SECTIONS.md` | 10005 | `a15387ffcc237f001c0c8692f1b19edfdf2cd04fa1803a58a79920c403488b3d` |
| `VERIFICA_DELTA_0315.md` | 12311 | `00553079e88a58a68762ba9a3400c04cb22b91f6a99f37f191b67cfd12ca9770` |
| `VERIFICA_PAPER_SECTIONS.md` | 13949 | `8faca80c87071d87bf66d97848c290a5724f6569be6f6040cfb6568bad022cb1` |
| `lint_paper_sections.py` | 4771 | `514782cffb66db518997102be32b5b55e09ef6c2da1be54d3edd43f830304905` |
| `method.md` | 7557 | `db697de1d124150bf8e754154c21a2d07cfaa0a79034bf32d3a6c5a449331938` |
| `protocol.md` | 17418 | `ddcaf1c2790d7e3fe966ed80bb91d3ae7316090d4b9dc554b85f8dd030ca5468` |
| `related_work.md` | 8052 | `52e0e9ba81948a7f26392884a518682ea5a9f25eaa6a49a5ce3d70a29236f842` |
| `threats.md` | 9221 | `915b7484ee3bff65c2633405db027c3e797d927bc56548238da2d631c06b2c35` |
| `verbalizer.md` | 7227 | `1b48085cd90e8dda183a482be333169a382d3c8a0e3f32cc433cec7eb01118f0` |

La consegna storica acquisita in 705f1c4 coincide con il file del worktree proprietario:
**16.615 byte**, SHA-256 `7469790613d644673bec6629ac7fb1ceae53aefdcbe45ae94239b687705aef2b`.
È separata dal pacchetto scientifico e dal record corrente A/B.

Le **54/54 fonti** coincidono per dimensione/SHA-256 ai riferimenti del registro: 52 blob Git
ai rispettivi pin, due file esterni. Non sono stati rieseguiti controlli numerici sulle fonti.
Sono stati verificati esistenza, impronta e collocazione nella storia; disponibilità locale
non equivale a inclusione in A (R1).

### 4.3 Composizione di PROVENIENZA — ✅

Il contenuto e82b5a0 di `studio2/PROVENIENZA.md` è prefisso byte-identico di A: **§§1–13
conservate integralmente**. La coda della provenienza 03.15 coincide con quella di d35b684 dopo
le sole sostituzioni dei due titoli: §14 per la provenienza originaria e §14.1 per il delta.
Il rinvio a `fase03/paper_sections/FONTI_DELTA_0315.json` risolve; §11 citata al pin c486eee
resta distinta dalla numerazione corrente. Nessun titolo duplicato o marker di conflitto.
La composizione osservata non altera contenuti scientifici o decisioni di altri cantieri.

Gli stati antecedenti conservati nella provenienza/report («verifica pending», vecchia fonte
schema, valori FAR omessi) restano record storici: §14.1 dichiara l'addendum senza riscrittura;
acquisizione, consegna corrente e nuovo walkthrough registrano l'OK successivo e i pin correnti.
Non sono stati trattati come nuovi obblighi di ripetere la review scientifica.

### 4.4 Walkthrough, ordine, parità e collegamenti — ✅ strutturale, con R1/R2 sul contenuto

La nuova §4.15 segue §4.12 e precede la sintesi. Indice HTML, apertura di stato MD/HTML,
tabella riassuntiva e voce §6.12 puntano a `paper-sections-0315` e mantengono il candidato locale.
**Tutte le nove sotto-sezioni precedenti** (4.1–4.7, 4.9, 4.12) sono identiche alla base in
MD/HTML; nessuna intestazione precedente persa. Nessun nuovo blocco MD non corrisposto in HTML
rispetto alla base; le differenze di presentazione preesistenti non sono state corrette.

La nuova §4.15 ha **15/15 blocchi** equivalenti, nello stesso ordine. Con la normalizzazione
`' '.join(parsed.get_text(' ', strip=True).split())` usata per verificare il conteggio dichiarato,
risultano **4.132 caratteri in entrambe le forme**, testo esattamente uguale. Il conteggio alternativo
per blocchi conserva 4.113 caratteri in entrambi i formati: cambia la separazione del markup,
non la parità. Numeri, riferimenti Git, impronte e limiti della sintesi corrispondono ai report
acquisiti; gli unici rilievi correnti sono R1 e R2, presenti identicamente nelle due forme.

HTML: **19 ID, nessun duplicato; 237 collegamenti locali**, dei quali **186 verso percorsi**
(il conteggio di A/B §4) e 51 frammenti sulla stessa pagina; **zero mancanti**.
Coppia walkthrough e PROVENIENZA: 460 collegamenti locali, tutti risolti; base 440, tutti risolti.
Nei record pertinenti controllati: 4 link interni risolti e 10 link assoluti verso il worktree
proprietario esistenti. Questi ultimi sono accessibili su questo dispositivo, non dichiarati
portabili ad altri filesystem; i blob dei report e verbali sono comunque acquisiti in A.
Non sono stati verificati URL bibliografici esterni né ripetuta la ricerca.

### 4.5 Distinzione fra i diversi OK e stati — ✅, salvo la raggiungibilità di R1

- `VERIFICA_PAPER_SECTIONS.md`: OK storico su **cf79e81**, con precedente NON OK conservato;
  non viene esteso al nuovo delta.
- `VERIFICA_DELTA_0315.md`: nuovo OK scientifico su **bcb462d..91a880b**, più coerenza delle
  cinque sezioni risultanti, fonti main c486eee. La sua firma è quella del revisore Anthropic
  dichiarato nel verbale, non del preparatore né di questa review documentale.
- **dc6e30c** consegna report/prompt/controlli dopo il candidato scientifico;
  **d35b684** acquisisce verbale e record successivi senza alterare le bozze.
- **532cc77** introduce la nuova documentazione, da valutare separatamente; **A** e **B**
  non trasformano gli OK scientifici in approvazione automatica del merge o del manoscritto.

Restano espliciti: 03.15 e Fase 03 aperte; nessuna promozione in docs/paper; D9/ruoli, identità e
qualificazione del servizio non decisi; firma materiale e freeze 03.8 pendenti. FAR e A/B non
sono riaperti. Nessun nuovo risultato diagnostico, abstract, conclusione o esecuzione dichiarati.
Soglia e FAR già documentati non sono stati confusi con prestazioni diagnostiche dei modelli:
la precisazione è nel record di acquisizione del verbale e resta invariata.

La lettura delle ref conferma main remoto fermo a c486eee e i due branch paper locali non
pubblicati; nessun tag locale contiene 91a880b. La fotografia delle ref/tag remote è conservata.
Non viene attestata una chiusura o un freeze nuovo sulla sola base dell'esistenza dei commit.

## 5. Controlli documentali eseguiti e limiti

**Guardiano:** `/usr/local/bin/python3`, Python **3.11.5**; comando
`python3 docs/test_explanation.py` su e82b5a0 e su A. Stesso script per byte.

| Oggetto | Test | Failure | Errori | Skip | Exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| Base e82b5a0 | 35 | 14 | 0 | 1 | 1 |
| A 9b6bd64 | 35 | 14 | 0 | 1 | 1 |

I log completi coincidono dopo la sola sostituzione del percorso di checkout (anche i tempi
misurati coincidono in queste due esecuzioni). Identificativi e parametri dei subtest sono
identici fra base e candidato e a `CONTROLLI_DELTA_0315.json`, non solo i conteggi:

- `test_condition_c_contract_and_caveats (__main__.UnifiedConversationChecks.test_condition_c_contract_and_caveats) (phrase='non un risultato empiricamente misurato')`
- `test_one_flow_and_ordered_step_headings (__main__.UnifiedConversationChecks.test_one_flow_and_ordered_step_headings)`
- `test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='0.944444')`
- `test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='0.916667')`
- `test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='0.833333')`
- `test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='zero astensioni')`
- `test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='C1–C4: 4/4 PASS')`
- `test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='controllo secondario distinto')`
- `test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='budget nominale di 1024')`
- `test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='36 aggregati B non cappati sono corretti')`
- `test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations)`
- `test_step27_qwen_protocol_stable_facts (__main__.UnifiedConversationChecks.test_step27_qwen_protocol_stable_facts) (doc='html')`
- `test_step27_qwen_protocol_stable_facts (__main__.UnifiedConversationChecks.test_step27_qwen_protocol_stable_facts) (doc='md')`
- `test_step27_qwen_protocol_stable_facts (__main__.UnifiedConversationChecks.test_step27_qwen_protocol_stable_facts)`

Skip comune: `TutorialChecks.setUpClass` — `legacy part-1 walkthrough is not present in this checkout`.
**La suite resta FAILED, non PASS.** Sono fallimenti/skip storici, nessuna regressione del delta;
non giustificano R1/R2 e non provano la correttezza scientifica. Non sono emersi errori di ambiente.

**Lint documentale** del pacchetto contro il corpus corrente: cinque file, zero segnalazioni,
exit 0. È il lint minimale già presente, eseguito per controllare il raccordo con il corpus
integrato; non verifica semantica, scientificità o ogni forma di leakage.
**`git diff --check`** su e82b5a0→A e 705f1c4→532cc77: exit 0, nessuna segnalazione.
Parità, link, riferimenti e impronte sono nei risultati JSON e negli script della verifica.

Il primo lancio dello script di integrità del verificatore si è fermato su un selettore di
intestazione che non riconosceva il titolo non numerato del ramo paper; è stato corretto lo
script di verifica e il controllo è stato completato. Non è un errore del candidato né un PASS
attribuito al tentativo interrotto. Nessun candidato è stato corretto.

## 6. Correzioni e sola riverifica richiesta

**Per ottenere l'OK di A servono soltanto R1 e R2 nella coppia MD/HTML.**
Produrre un nuovo delta documentale tracciato, preservando A, la copia B, questo NON OK e tutti
i report/verbali/pacchetti già improntati. Nel record successivo distinguere il nuovo commit
dalla versione B qui verificata; non riscrivere B retroattivamente.

La riverifica necessaria riguarda esclusivamente quel delta: accuratezza di raggiungibilità e
perimetro, parità MD/HTML, link/anchor, assenza di altri cambiamenti e confronto del guardiano
per identificativi/subtest. **Non serve ripetere la review scientifica di cf79e81 o 91a880b,
né rifare la review della base e82b5a0, integrare il piano 03.8, ricalcolare risultati o avviare
pilot.** Nessuna decisione scientifica dell'autore è richiesta per queste due precisazioni.
Integrazione, pubblicazione e freeze non sono stati eseguiti da questa verifica e non fanno
parte della correzione richiesta.

## 7. Prove conservate, fonti e stato finale

Prove in `/Users/luker/fot-tep-verifica-raccordo-0315-9b6bd64/studio2/fase03/paper_sections/evidenze_verifica_raccordo_0315`:
snapshot A/B, patch esterna, diff dei documenti condivisi, preflight e ref, estratti di metadata,
script `audit_integrity.py`/`audit_documents.py`, `integrity.json`, `documents.json`, `supplement.json`,
log guardiano/lint/diff, copie delle due fonti locali e copia byte-identica del verbale della
base. `MANIFEST_EVIDENZE.json` registra dimensioni e SHA-256 di queste prove e del presente verbale.

Il verbale della base, già accettato, è stato soltanto letto/conservato: **21.639 byte**, SHA-256
`7c1d6ebf90ccb29d2b3f418b0b6740b62435626db8e9a6b7f6abdd8512a27511`.
Nessuna nuova esecuzione delle verifiche evidence/schema/letteratura della base.

Fonti lette nel perimetro del raccordo: handoff rev02; MAINTENANCE §§1–5, 8 e prompt
Verifica/Prompt; consegna corrente Git ed esterna; consegna storica 03.15, report e record di
acquisizione, report del delta, verbali storico e del delta per oggetto/esiti/limiti; registro
FONTI e identificativi del guardiano in CONTROLLI; PROVENIENZA e diff/coppia walkthrough.
Le 54 fonti sono state lette come byte per esistenza/impronta, senza ricalcolarne il merito.
Costo di lettura indicativo: alcune decine di migliaia di token, non misura del consumo fatturato.

Unici nuovi file: questo verbale e le prove nella copia isolata, intenzionalmente non tracciati.
Il candidato Git e i suoi file tracciati restano invariati; il sorgente conserva HEAD A e la sola
modifica B iniziale con SHA-256 invariato. Nessuna scrittura nei worktree sorgente o metriche;
nessuna modifica alla base verificata, nessun commit, merge, push, tag, simulazione, calcolo
scientifico, inferenza o chiamata API. Gli unici accessi remoti sono letture di ref tramite Git.
