OK

# Verifica indipendente della revisione 10 — recepimento A/B

Data della verifica: **2026-09-14**, fuso `Europe/Rome`.
Revisore: **gpt-5.6-sol**, sessione agent **`/root/revisore_rev10`**, distinta dal
preparatore **Codex GPT-6** nella stessa task utente. Verifica svolta nella copia
detached `/Users/luker/fot-tep-verifica-piano-statistico-rev10`, senza correggere
né autoapprovare i file del candidato.

**Verdetto:** il commit candidato recepisce fedelmente e in modo circoscritto le
formulazioni A e B approvate da Luca. Questo OK riguarda esclusivamente il
recepimento A/B della revisione 10; non costituisce firma materiale, congelamento,
chiusura della sotto-fase 03.8 o della Fase 03, né autorizzazione all'esecuzione.

## 1. Identificazione dell'oggetto verificato

| Elemento | Identità verificata |
| --- | --- |
| Baseline approvata | `526561feabeb6b4083170b1817b8abdac1a2a4c7` |
| Commit di registrazione dell'approvazione | `f37e7e00cbdd959ef6fdb7cc96ce42ed521075d6` |
| Candidato revisione 10 | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` |
| Tree del candidato | `24847ce0cc4ff7b6defea4d65f3f41cb9ccd1c1a` |
| Manifest corrente | `studio2/fase03/piano_statistico/PIANO_STATISTICO_FREEZE.json` |
| SHA-256 del manifest corrente | `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8` |

✅ La copia era su `HEAD` detached esattamente al candidato ed era pulita prima
della scrittura di questo solo verbale. La catena Git è lineare
`526561f` → `f37e7e0` → `6aaa5b3`: il primo delta aggiunge soltanto il record
dell'approvazione; il secondo contiene il recepimento. Il manifest dichiara
`revision=10`, `freeze_effective=false`, `freeze_tag=null` e review rev. 10
`pending`. Non contiene il proprio percorso fra le voci `files`, il proprio
SHA-256 o il commit candidato, evitando l'auto-riferimento.

## 2. Approvazione e identità dell'addendum

✅ Fonte primaria: blob
`ADDENDUM_DECISIONI_RESIDUE_03_8.md` al commit baseline. Il blob e la copia nel
candidato sono byte-identici: SHA-256
`6035967ceb390de69e63cac9f828b17386ab8a76bb1999db524597770fc782f8`,
3.768 byte.

✅ `APPROVAZIONE_ADDENDUM_03_8.md` trascrive esattamente il messaggio autorizzativo
ricevuto: A e B approvate senza modifiche al commit completo `526561f`,
registrazione a nome Luca con data effettiva **14 settembre 2026**, nuova revisione
da sottoporre a verifica indipendente e firma materiale separata. Il record è
invariato dal commit `f37e7e0` al candidato; SHA-256
`df2a754d3ad2d2215def012eb4d6e887c77d93ebdcad4a6811c5cbc18786a70a`.
Non è stata aggiunta alcuna firma e non è stata richiesta una seconda approvazione.

## 3. Perimetro del delta baseline → candidato

✅ Il diff completo modifica soltanto nove file nella cartella
`studio2/fase03/piano_statistico/`: record di approvazione, piano, report,
manifest rev. 10, copia storica del manifest rev. 9, allegato contabile, atto
rev. 10 non firmato, controlli del preparatore e prompt di verifica. Nessun file
congelato di `phase_b/`, `icl/`, `ablation/`, `tep_*_v2/`, nessuna coppia
Markdown/HTML e nessun artefatto fuori dal perimetro risultano modificati.

✅ Il confronto del piano mostra modifiche soltanto nell'intestazione/stato e nei
punti necessari a registrare A/B: quadro iniziale e vincolo verso 03.11, §7.2,
§8.2, §10.2, T5 e chiusa di §11.1, tabella §15 e §16. Non emergono nuove decisioni
su D9, E5, ipotesi, margine, alpha, test, campioni, scorte o criteri scientifici
OOD. Il nuovo `BUDGET_RISORSE_REV10.md` conserva il contenuto contabile della
preparazione al commit `526561f`; il suo delta sostanziale aggiorna soltanto
titolo e stato per registrare A come approvata, mantenendo parametri e misure
pending.

## 4. Recepimento A — risorse e ramo R=3

✅ Il valore 3.700 è mantenuto soltanto come tetto storico e dichiarato non più
vigente. La regola corrente richiede il conteggio completo per blocco e modello,
con R distinto, e la verifica di fattibilità sui tempi misurati nel pilot della
configurazione effettiva, con margine temporale del 20%. La finestra non si
estende automaticamente.

✅ Il trigger di R è invariato: R=3 si attiva soltanto per divergenza della coppia
parsata (`abstain`, `predicted_label`) o della validità secondo §10–11, non per
la sola indisponibilità di temperatura/seed. Se R=3 non è fattibile, la regola
impone sospensione organizzativa e decisione esplicita dell'autore, senza
riduzione automatica del disegno, scelta D9, estensione automatica della finestra
o dichiarazione di fallimento scientifico.

✅ T5 usa conteggi completi e tempi effettivamente misurati; non dichiara tali
misure già disponibili. Il candidato comunicato resta non identificato in modo
sufficiente per D9 e non eredita le prestazioni del vecchio server.

## 5. Contabilità indipendentemente ricalcolata

✅ Con D2=8, i conteggi derivati dalle formule sono:

| Blocco consumer | R=1 | R=3 |
| --- | ---: | ---: |
| Nucleo: local-unseen + local-seen + Normal | 1.728 | 5.184 |
| Producer-swap, sola misura | 224 | 672 |
| Ablation B-senza-LF | 148 | 444 |
| OOD | 144 | 432 |
| Somma dei quattro blocchi | 2.244 | 6.732 |

Il nucleo deriva da `8×8×7×3 + 8×8×1×3 + 8×8×3 = 1.728`; swap da
`4×8×7 = 224`; ablation da `8×8 + 4×3×7 = 148`; OOD da
`2×3×8×3 = 144`.

✅ L'audit aggiunge `2k` soltanto a R=1 e zero a R=3; E5 resta parametrico a
R=1 (`16S`); FULL aggiunge `8U` soltanto se non riusabile e il riuso richiede
identità di caso, ricevente, prompt completo, modello/configurazione, decoding e
aggregazione. I canary restano 10 al giorno. Produzione e conformità, pilot,
riserva e retry sono separati senza doppio conteggio; `Q` comprende soltanto retry
ulteriori fuori pilot ammessi dalla futura politica 03.10.

✅ Lo scenario esplicitamente non definitivo con `S=12`, `d=10`, riusi completi,
`P_tot=160`, `X=100`, `Q=0` dà 3.142 a R=1 e 7.284 a R=3. I valori sono presentati
come esempio contabile, non come budget, misure o autorizzazione approvati.

✅ La riserva resta `8r+t≤15`; la sonda usa soltanto triplette complete entro la
quota 7 anche se non avviene remediation, quindi al massimo due triplette con quota
integra. I massimi ricalcolati sono 152 senza producer alternativo e 160 con
producer alternativo. L'hard stop cumulativo 200 resta separato, non finanzia
altre 40 richieste e non consente reset. Nessun retry automatico o retry del gate.

## 6. Recepimento B — ordine OOD e assenza di ciclo

✅ Il piano congela prima del primo run di test candidati F6/F4, criteri tecnici,
catene F6→F5→F12 e F4→F11→F5, regole di sostituzione, campioni, undici scorte e
scelte statistiche. In 03.11, dopo il congelamento e prima di qualunque chiamata
ai modelli sui test, si eseguono controlli tecnici tracciati di generabilità,
trip nella finestra e ammissibilità.

✅ Prestazioni diagnostiche, separabilità e risultati dei modelli sono esclusi
dalla selezione. Ogni sostituto deve superare verifiche proprie; i due OOD devono
restare distinti. Un caso non risolto, incluse catene che convergano entrambe su
F5, impone sospensione e decisione esplicita dell'autore. Restano vietate modifica
silenziosa e sostituzione dopo le chiamate. Le scorte sostituiscono run e non
aggiungono osservazioni.

✅ La sequenza risultante è aciclica:
criteri/candidati/catene congelati → run e controlli tecnici 03.11 → chiamate sui
test dopo gli altri GO. La verifica bibliografica di F6 entro PHM è mantenuta
distinta e non viene presentata come GO tecnico OOD.

## 7. Dipendenze, invarianti e condizioni conservate

✅ Il candidato distingue correttamente i requisiti del congelamento statistico
dalle condizioni operative. Prima del pilot restano obbligatori input di sviluppo,
schema, mapping, identità/configurazione, capienza, implementazione 03.10 e relativi
test; prima delle chiamate sui test restano obbligatori i controlli OOD 03.11 e gli
altri GO. T5 resta da misurare. A/B non autorizzano chiamate sperimentali.

✅ Sono risultati byte-identici alla baseline tutti i 28 blocchi statistici
elencati in `CONTROLLI_REV10.json`, fra cui popolazione, endpoint, ipotesi,
gerarchia, statistiche, margine, bootstrap, D2, D11, reporting, validità,
remediation, gate, audit e canary. Sono invariati anche codice, test e artefatti
`DESIGN_RESOLUTION`: JSON
`8bf79dc958e045598cf7538b72752caa902d2f8b134f642e54daaf0274fddbde`,
Markdown `9ed15d15e8a6210e79573c9e4b3d073dfb8d8d9ed680735d83dc7c35358febb7`,
generatore `25a648b99fcb86f8111eaaf2f712183d6c3e0a0af5960b6b84c424c38fb1e613`
e test `569d63e60a2028958f3e41b92b6fa38628cd8ce3ad5d3546328308eaf39cf06f`.

## 8. Manifest, catena storica e impronte

✅ Ricalcolo indipendente delle voci del manifest rev. 10: **19/19 `files`** e
**6/6 `inputs_read`** coincidono per SHA-256 e dimensione.

✅ Il manifest storico rev. 9 è byte-identico al blob
`PIANO_STATISTICO_FREEZE.json` del commit `0f1a9bae8b522f614720fa5efe7bd9d2577609ae`:
SHA-256 `2b6ad396307be634428d9355d4aa65144b4956d675ccb9e4b47536e4bdaf8d76`,
18.817 byte. Risolte a quel commit, coincidono anche tutte le sue voci: 11/11
`files` e 6/6 `inputs_read`.

✅ Il manifest preparatorio è byte-identico alla copia del commit baseline:
SHA-256 `a570c0c91f3a45d4435d318e628cdad37ef7be0dceda17fcb62cf50350dead93`,
8.501 byte; risolte al commit `526561f`, coincidono 10/10 voci `files` e 20/20
`protected_inputs`. I verbali storici restano integri, incluso rev. 9
`289a74433d70e2bf911bdea893711ff7a294c75cf74d5e6fa0addbf3ede72a58`
al checkpoint `29249a9305c44a44b96e6f49f94e978956ed0ac2`.

## 9. Allineamenti esterni e stati non sovradichiarati

✅ Piano generale e `APERTURA_SOTTOFASI_FASE03.md` non sono stati modificati e
conservano valori/ordini da allineare. `COORDINAMENTO_CHIUSURA_03_8.md` contiene
rami espliciti condizionati all'approvazione: dopo il record di Luca è applicabile
il ramo A per §8.8/D2/T5/O2/§13 e il ramo B per OOD/APERTURA. Il report dichiara
queste applicazioni pending e seriali. `DELTA_HARNESS_03_10.md` resta una specifica,
non un'implementazione o un GO.

✅ Integrazione bibliografica, conservazione esterna dei PNG, allineamenti
normativi, implementazione 03.10, walkthrough, pubblicazione, raggiungibilità da
`origin/main` e tag restano dichiarati pending. Il candidato non è raggiungibile
da `origin/main`; il tag `studio2-fase03-piano-statistico-frozen-001` è assente.
Nessuna firma, integrazione o pubblicazione è dichiarata compiuta.

## 10. Test e controlli eseguiti dal revisore

✅ `/Users/luker/fot-env/bin/python -m unittest studio2.fase03.piano_statistico.test_design_resolution`:
**26 test eseguiti, 26 OK**. La suite ha scritto soltanto artefatti sintetici in
directory temporanee; non è stata rigenerata la griglia completa.

✅ `python3 docs/test_explanation.py`: **35 test, 14 fallimenti, 1 skip**. I 14
identificatori/subtest coincidono esattamente e nello stesso ordine con quelli
registrati in `CONTROLLI_REV10.json` e con il baseline dichiarato: 1
`test_condition_c_contract_and_caveats`, 1
`test_one_flow_and_ordered_step_headings`, 9
`test_step27_qwen_frozen_results_and_limitations`, 3
`test_step27_qwen_protocol_stable_facts`.

✅ `git diff --check` baseline→candidato: OK. I tre JSON del delta sono validi;
11 collegamenti Markdown locali nei file modificati risolvono; nessun nuovo file
di griglia, dato reale, inferenza o simulazione TEP compare nel diff. Durante
questa verifica non sono state eseguite chiamate a modelli sui dati, inferenze,
simulazioni TEP o test su dati reali.

## 11. Limiti del verdetto e rilievi

Nessun rilievo bloccante o raccomandazione correttiva sul recepimento A/B.

Restano aperti, e questo OK non li certifica: firma materiale; integrazione
bibliografica e PNG; allineamenti del piano generale e di APERTURA; implementazione
e verifica 03.10 con prerequisiti del pilot; scelta D9; conteggio/calendario e
fattibilità T5 misurati; controlli tecnici OOD 03.11; walkthrough, acquisizione
seriale, pubblicazione in `origin/main`, manifest effettivo e tag di freeze.

Fonti lette: `docs/MAINTENANCE.md`, `docs/prompts/Prompt_LLM.md`,
`docs/prompts/Verifica_LLM.md`, `PROMPT_VERIFICA_REV10.md`, report e manifest
correnti, addendum e record d'approvazione, piano e suo diff completo, allegato
contabile, atto non firmato, controlli rev. 10, manifest storici, delta di
coordinamento e harness, punti pertinenti di piano generale e APERTURA. Nessun
paper né risultato sperimentale reale è stato aperto.
