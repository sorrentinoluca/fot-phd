OK

# Settima verifica indipendente conclusiva della sotto-fase 03.8 — piano statistico

Data: **2026-09-14**. Modello verificatore: **Codex, GPT-5**, finestra separata,
ragionamento esteso. Oggetto: revisione 7 non committata nel worktree
`/Users/luker/fot-tep-piano-statistico-fix`, branch
`codex/studio2-piano-statistico-fix`, con HEAD `dd82cd1`.

Verifica svolta sui file del worktree e sul diff rispetto a HEAD. Non sono stati
aperti `fault_runs/runs/`, `soglie_normal/runs/`, `evidence/output/` né risultati
per-fault del primo studio. Nessuna chiamata a modelli. L'unico file modificato dal
verificatore è questo verbale.

La revisione 7 risolve il solo difetto bloccante della sesta verifica: il campo
serializzato è ora `one_sided_bound_distance`, con valore
`z_(1-alpha_one_sided) * SE` e copertura unilaterale `1-alpha_one_sided`. La
regressione controlla nome, assenza del vecchio campo, metadato e valore sia a
`alpha=0,05` sia a `alpha=0,025`. Non risultano ulteriori difetti bloccanti.

## 1. Perimetro del diff — ✅

- Otto file modificati, tutti in `studio2/fase03/piano_statistico/`: piano,
  generatore, test, JSON e Markdown generati, manifest, report e verbale.
- Nessuna modifica a `PROVENIENZA.md`, `protocol.py`, `schemas/`, harness, fonti
  autorevoli, walkthrough o artefatti congelati.
- `git diff --check` passa. Nessun commit, tag, merge o freeze è stato creato.
- La verifica riguarda lo stato corrente del worktree; HEAD resta `dd82cd1`.

## 2. Correzione della revisione 7 — ✅

Il dataclass `AnalyticRow`, la generazione JSON e le tabelle Markdown usano il nome
neutro `one_sided_bound_distance`. Nel JSON pubblicato:

- sono presenti **120/120** chiavi `one_sided_bound_distance`;
- sono presenti **0/120** chiavi `one_sided_bound_distance_95`;
- `alpha_one_sided` dichiara il livello usato nel calcolo;
- `two_sided_halfwidth_95` resta correttamente distinto e fissato al 95% bilaterale.

Il nuovo test end-to-end usa `statistics.NormalDist().inv_cdf(1-alpha)` come
controllo indipendente dal calcolo applicativo. A `alpha=0,025` verifica quindi la
distanza al 97,5%, eliminando l'ambiguità accertata nel sesto verbale.

La sola sostituzione testuale della nuova chiave con il nome precedente ricostruisce
il JSON della revisione 6 byte per byte:

`17e020311b59724482606db6e3230d2eb669dc3da687e99a4d1e1e631aff6fb8`.

Questo conferma che le 120 modifiche del JSON sono soltanto rinomine e che valori,
ordine e simulazioni non sono cambiati. Il Markdown conserva l'impronta della
revisione 6.

## 3. Matematica, alpha e implementazione — ✅

Restano confermate le conclusioni della sesta verifica:

- H1/H2 adottano il test di Hoeffding sulla media delle medie di cluster,
  limitate in `[-1,1]`, sotto indipendenza fra cluster e dipendenza intra-cluster
  arbitraria; la garanzia finito-campione riguarda il livello, non la potenza;
- H3 usa il test score di Tango; nel caso senza discordanti la statistica è finita,
  `sqrt(N*m/(1-m))`;
- `alpha` è propagato ad analitico, MDE, Hoeffding, Tango, bootstrap e simulazioni;
- la semiampiezza centrale 90% resta distinta dal livello decisionale;
- le righe impossibili con `|Delta|>d` sono escluse;
- MDE normale e MDE Hoeffding sono distinti, e l'MDE Hoeffding è dichiarato come
  approssimazione, non garanzia esatta di potenza;
- la guardia applicativa copre `builtins.open`, `io.open`, `pathlib`, letture e
  modalità update; il limite rispetto a una sandbox di sistema è dichiarato.

La conclusione scientifica resta prudente: otto run aumentano la potenza ma non
garantiscono l'80% in tutti gli scenari, in particolare per effetti medi e alcuni
scenari H3.

## 4. Simulazioni e riproducibilità — ✅

È stata eseguita una rigenerazione completa indipendente in directory temporanea,
con seed 20260913, `alpha=0,05`, 158 scenari, 400 repliche per scenario e 2.000
bootstrap per replica. Risultati:

- `DESIGN_RESOLUTION.json`: byte-identico, 126.303 byte, SHA-256
  `8bf79dc958e045598cf7538b72752caa902d2f8b134f642e54daaf0274fddbde`;
- `DESIGN_RESOLUTION.md`: byte-identico, 27.356 byte, SHA-256
  `9ed15d15e8a6210e79573c9e4b3d073dfb8d8d9ed680735d83dc7c35358febb7`.

Il confronto strutturale conferma 120 righe analitiche ammissibili e 158 scenari
simulati. Le tabelle H3 nel piano sono protette da un test di corrispondenza con il
JSON.

## 5. Verifica dei punti del mandato — ✅

1. **Fedeltà al piano:** scelte di progetto e decisioni dell'autore restano
   distinte; nessuna decisione aperta è chiusa implicitamente.
2. **Tango e dati sintetici:** formula, MLE vincolata, distribuzione su
   `{+1,-1,0}` e mescolanza intra-cluster restano coerenti.
3. **Margine, alpha e gerarchia:** `m=0,125`, `6/48=8/64`, alternativa
   `alpha=0,025` e fixed sequence sono descritti correttamente; la componente H3
   conserva una garanzia asintotica/approssimata.
4. **Bootstrap e unità:** cluster fisico run×fault, otto strati, sette righe P1,
   astensioni e risposte non valide sono coerenti; il bootstrap è intervallare.
5. **OOD:** sette candidati inclusi F9, esclusioni F7/F9, rilevabilità documentata
   di F4, incertezza su F6 e sostituti pre-chiamata sono corretti.
6. **D11:** `{F1,F2}`, `{F14,F15}`, `4×3×7=84` e `8n+84=132/148` tornano;
   l'analisi resta descrittiva.
7. **Politica R e GO/NO-GO:** T9 e T3 sono distinti; T9 resta una soglia severa e
   una decisione aperta dell'autore.
8. **Budget:** 2.853 contro 3.555 chiamate con retry, incremento 702 (24,6%);
   incremento pre-retry 638; il tetto derivato è 3.700 e 3.500 è segnalato come
   refuso storico.
9. **Threats e descrittive:** soltanto H1-H3 sono confermative; OOD, ablation,
   producer-swap, E5, baseline, Normal e strati restano descrittivi.
10. **Riferimenti:** il report conta otto riferimenti metodologici esterni; la
    verifica mirata non sostituisce il loro ingresso nel corpus secondo
    `MAINTENANCE.md` §6.

## 6. Test, report e manifest — ✅ sul candidato pre-review

- Suite statistica: **26/26 OK** con `/Users/luker/fot-env/bin/python`.
- La regressione nuova a `alpha=0,025` passa.
- `docs/test_explanation.py`: **35 test, 14 fallimenti, 1 skip**; insieme
  documentale preesistente e invariato, estraneo alla statistica della sotto-fase.
- Manifest: **14/14** impronte e dimensioni prima della sostituzione del sesto
  verbale; otto file più sei input, tutte le decisioni `open`, stato
  `proposed_pending_author_decisions`, `freeze_tag: null`.
- Il report segue i sette punti di `Fase_LLM.md`, documenta la correzione, i file
  modificati, i limiti scientifici e tutte le decisioni ancora aperte.

Il manifest impronta intenzionalmente il sesto verbale storico. La scrittura di
questa settima verifica nello stesso percorso rende non più coincidente quella sola
impronta. È un effetto meccanico della review, non un difetto del candidato
verificato: l'impronta del verbale conclusivo va aggiornata dopo la sua
stabilizzazione, senza cambiare gli artefatti sostanziali.

## 7. Decisioni e passaggi successivi

L'**OK** riguarda coerenza tecnico-scientifica, implementazione e documentazione del
candidato. Non chiude le decisioni riservate all'autore: D2, OOD, D11, margine e
alpha, test e gerarchia, politica R, soglie GO/NO-GO, seed e scorte.

Prima del freeze restano necessari:

1. conferma esplicita delle decisioni dell'autore;
2. aggiornamento meccanico dell'impronta di questo verbale nel manifest;
3. commit identificabile, raggiungibile secondo la policy del manifest;
4. eventuale tag annotato di freeze solo dopo i passaggi previsti.

## Chiusura secondo `Fase_LLM.md` 1–7

1. **Risultato:** correzione verificata; nessun difetto residuo bloccante.
2. **File toccato:** soltanto questo verbale nel worktree dedicato.
3. **Modello/profilo:** Codex GPT-5, verifica indipendente decisionale,
   ragionamento esteso.
4. **Fuori:** nessun dato reale, nessuna chiamata a modelli, nessuna modifica agli
   altri artefatti.
5. **Decisioni:** tutte quelle del manifest restano aperte; otto run sono una
   raccomandazione senza garanzia universale dell'80%.
6. **Test:** 26/26; suite documentale 14 failure/1 skip; rigenerazione completa
   byte-identica; manifest 14/14 sul candidato pre-review.
7. **Commit/tag:** nessun commit o tag creato; candidato idoneo ai passaggi di
   conferma e stabilizzazione, non ancora congelato.

## Verdetto finale

**OK.** Percorso del verbale:
`studio2/fase03/piano_statistico/VERIFICA_PIANO_STATISTICO.md`.
