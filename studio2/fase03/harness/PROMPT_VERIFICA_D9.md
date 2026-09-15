# Prompt di review indipendente — delta D9 eseguibile offline

Prima di modificare qualsiasi cosa leggi `docs/MAINTENANCE.md` nella versione
pertinente e rispettalo. Questa finestra è una **review read-only** del codice:
non correggere il candidato, non riaprire indiscriminatamente R01–R10/C01–D04.
Scrivi il verbale e le prove in una sede separata dal candidato.

## Identità da verificare prima delle prove

- Worktree preparatore `/Users/luker/fot-tep-harness-d9`.
- Branch `codex/studio2-harness-d9`.
- Tecnico `6a8031b25aa1208047d79cc7f030bf9cf7841e67`, tree `bb3872d8fc1cbddebb4b055a8edad372e5aad430`.
- Base documentale D04 `5886c6f9d078ee624deaec08763e04c14e96e4f0`;
  contratto/fonti/test-first `62343a7bb526d5285df547ceb8f5ea0341515cef`.
- Manifest `studio2/fase03/harness/HARNESS_D9_CANDIDATE.json`,
  SHA-256 `356e87d29028a80488a6acfde66b7551bacde94481eba3389922e04124625668`.
- Eventuale HEAD successore documentale non è il tecnico. Verifica branch,
  HEAD/tree, stato locale, remoto effettivo, worktree e altri writer. Non importare
  copie arretrate delle coppie condivise e non modificare il worktree D04.

Leggi skill `/Users/luker/.codex/skills/fot-tep-harness-lessons/SKILL.md` e riferimenti,
prompt Verifica_LLM, contratto D9 prima del codice, appendice dei campi, report D9,
SOURCES.json e fonti nelle versioni identificate, contratti D03/D04/R4 applicabili.
L'handoff rev03 aggiorna lo stato, non sostituisce fonti o decisioni scientifiche.
Le due review D04 acquisite riguardano solo `aae29a9`, tree
`4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`: nessun trasferimento automatico di OK.

## Oggetto e attese

Verifica autonomamente il delta delle configurazioni, acquisizione/persistenza,
rilettura/resume, validazione, runner/CLI, prompt, contabilità e decisioni di invio.
Segui ogni campo normativo D9 dal primo ingresso alla riserva durevole e al riuso;
considera anche più stadi e restart, non soltanto l'ingresso CLI felice.

Ruoli già approvati: P=C122B, P_alt27B completo16, consumer122B fisso sugli stessi
casi dello swap. Terra storico descrittivo interno; nessun fattoriale, consumer27B,
fallback o scelta dei ruoli dalle prestazioni. Payload122B senza temperature,
compreso null;0.6 dichiarato non diventa parametro operativo.

Verifica separazione R4/chat, libreria prodotta dalla conformità prima dei prompt
completi14peer, ordine1a con propria approvazione separata da canonical label_space,
mapping e derangement. Non rifare03.7. Verifica che alternate PENDING blocchi e
che pilot/deferred non implichino nuove decisioni su collocazione o budget.

Metadati reali incompleti e qualificazioni non svolte devono restare bloccanti.
Il config consegnato non autorizza servizi. Valuta specificamente la distinzione
tra documento del servizio e osservazione effettiva: alias/hash dichiarati non
provano i pesi né costituiscono prova zero-token. Il consumo storico S4/3 resta
non riconciliato; nessuna migrazione, azzeramento, backfill o duplicazione.

## Prove richieste e limiti della preparatrice

Usa fixture isolate e trasporti fittizi. Non chiamare servizi né effettuare
inferenze, simulazioni TEP, pilot o produzione di insight reali. Non toccare
ledger scientifici. Esegui suite mirata/discovery come in d9_evidence/COMANDI.md,
regressioni del delta e controlli positivi. Verifica il candidato esatto e i byte
TESTED_BYTES/manifest. Gli adattamenti di fixture e D01 legacy sono dichiarati
in ADATTAMENTI_E_LIMITI.md: valuta se conservano gli invarianti, non contarli
come prove storiche letterali. Le dipendenze locali delle fixture legacy devono
essere disponibili; se mancano, registra env-bloccato senza inventare esiti.

Sull'antecedente `aae29a9`, il file finale test_d9 produce3 assertion fallite e14
errori per API assenti: distingui quei risultati. Non sono17 regressioni D04.
Un eventuale nuovo difetto concreto deve essere riproducibile con positivi e,
quando pertinente, confronto con il tecnico precedente usando gli stessi test.
I log intermedi non sono esiti finali; le suite sovrapposte non si sommano.

D9_FIELD_CONTRACT descrive il confine dei nuovi binding; verificane copertura e
rifiuto al punto della decisione. Esamina in particolare riferimenti del provider,
config persistita, metadati alterati, riserve dirette, storia/quote e swap.
La helper swap non seleziona casi definitivi o avvia uno studio; il percorso
alternativo differito non è implementato senza specifica. Non interpretare
questi limiti come autorizzazione ad inventare decisioni mancanti.

Guardiano storico NON PASS:35test,14fallimenti,1skip,0errori. Confronta identificativi
in d9_evidence/guardian_comparison.json; non trasformarlo in PASS. Conserva tutte
le acquisizioni D04, NON OK, pending storici, manifest e byte certificati.
Niente push, merge, tag, invii a terzi o aggiornamenti condivisi della coppia MD/HTML.

## Verbale

Prima riga: verdetto sul solo delta offline (OK limitato / NON OK con rilievi),
modello dichiarato e identificativo della finestra. Specifica tecnico/tree,
ambiente, prove effettivamente eseguite, adattamenti, env-bloccati, limiti e
identificativi dei rilievi. Non rilasciare GO, freeze03.10 o qualifica scientifica.
Conserva comandi/log/raw di test e manifest con file recuperabili oltre agli hash.
