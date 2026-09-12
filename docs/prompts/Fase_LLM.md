# Modalità fase — studio 2 FoT-TEP

**Leggi prima `Prompt_LLM.md`**, in questa cartella: instradamento, costi, precedenze. Qui ci sono
solo le regole di come si lavora una fase.

## Apertura: cosa leggere, in quest'ordine

1. `docs/MAINTENANCE.md` §1, §2 e §8 — cosa è congelato, il perimetro `studio2/`, le regole di commit.
2. `docs/fot_walkthrough_conversazione_studio2.md` **§0** (fonti e precedenze), **§0.1** (punti
   aperti) e **§2–12** (l'elenco delle fasi, per sapere dove sei).
3. Solo la sezione del piano che riguarda la fase in corso. Il piano è ~32k token: non aprirlo tutto.

## Regola sui dati del primo studio

Se la fase usa dati, soglie, insight o risultati del primo studio, **il walkthrough
`docs/fot_walkthrough_conversazione_v2.md` va letto**, nella sezione pertinente, e gli artefatti
vanno aperti e verificati. Non si ipotizza, non si ricostruisce a memoria, non si deduce da come
«dovrebbe» essere andata. Per come è stata costruita la pipeline, la fonte è la prima esposizione
`docs/fot_walkthrough_conversazione.md` (§6, §8, §9, §29): la v2 quello strato lo ha perso.

Ogni dato riusato va registrato in `studio2/PROVENIENZA.md` con origine, commit, impronta e la
marca **pre-specificato / post-hoc** dell'analisi che lo usa (MAINTENANCE §8.2).

## Sotto-fasi: elencare prima, procedere una alla volta

1. **In apertura, elenca le sotto-fasi** della fase in corso e fermati: conferma l'elenco prima di
   iniziare. Elencare non è decidere — è il piano di lavoro, non l'esito.
2. **Poi procedi una sotto-fase alla volta.** Chiusa una, si passa alla successiva.
3. **Non anticipare decisioni o discussioni delle sotto-fasi successive**, e non riorganizzare
   l'ordine per comodità. L'eccezione è una sola: quando la sotto-fase corrente **non è
   risolvibile** senza fissare qualcosa che appartiene a una successiva. In quel caso **dillo
   esplicitamente**, spiega la dipendenza, e chiedi — non decidere di tua iniziativa.
4. Le dipendenze del piano restano vincolanti anche dentro una fase: se §6.1 non è congelata, le
   decisioni che la presuppongono non sono lavorabili oggi, per quanto sembrino indipendenti.

## Batch: conta prima di partire

Vale la regola di `Prompt_LLM.md`, e in una fase è dove si perdono i budget: generazione di run,
batch di inferenze, verifica su tutti i prefissi, conversioni su molti file. **Conta gli elementi e
stima il totale prima del primo**, e se il ciclo passa dai tuoi turni proponi lo script
parallelizzabile invece di eseguirlo tu.

Il resto — comandi singoli, anche lenti, e tutto ciò in cui la decisione sta nell'operazione — lo
esegui senza chiedere.

## Modello e ragionamento consigliati

Per **tipo di compito**, non per nome di prodotto — i nomi invecchiano.

| Compito | Cosa serve |
| --- | --- |
| Scelte di disegno, criteri, piano statistico, lettura critica di letteratura | Il modello più capace disponibile, ragionamento **esteso**. Sono decisioni che si congelano: costano poco adesso e molto dopo |
| Implementazione, harness, script di analisi | Modello capace, ragionamento **medio**, con i test eseguiti e non immaginati |
| Modifiche meccaniche: rinomine, allineamento coppie MD/HTML, conteggi, indici | Modello economico, ragionamento **basso**. Sono operazioni verificabili con un comando |
| Verifica indipendente | **Un'altra finestra e preferibilmente un altro modello** — vedi `Verifica_LLM.md` |

## Chiusura della finestra

Quando **tutte** le sotto-fasi sono chiuse — non prima — **scrivi il report di chiusura in un file**:
`studio2/fase<N>/REPORT_FASE<N>.md`. Non lasciarlo solo in chat: le finestre di verifica e di
documentazione non ereditano questo contesto, leggono il repository. **Ciò che esiste solo nella
conversazione non è verificabile né documentabile.** Il report è solo Markdown, non è una coppia
con un `.html`.

Il report contiene:

1. **Riassunto e risultati**, organizzati **seguendo le sotto-fasi eseguite**, nello stesso ordine.
2. **File toccati**, uno per riga, e cosa è cambiato in ciascuno.
3. **Cosa è rimasto fuori** e perché.
4. **Decisioni ancora necessarie**, se ce ne sono.
5. `python3 docs/test_explanation.py` confrontato con il numero di partenza.
6. **La decisione se committare, con il messaggio proposto** nel formato
   `studio2(<ambito>): <azione concreta>` di MAINTENANCE §8.3.

In chat lascia solo il percorso del report e le tre righe di sintesi. Tutto il resto sta nel file.

⚠️ **Prima di chiudere, verifica che tutto sia su disco.** Codice, configurazioni, risultati, log:
quello che hai solo raccontato non esiste per le finestre successive.

⚠️ **Non aggiornare il walkthrough adesso.** L'ordine è: fase conclusa → **verifica indipendente**
(`Verifica_LLM.md`, altra finestra) → OK del verificatore → **aggiornamento documentazione**
(`Documentazione_LLM.md`). Scrivere il walkthrough prima della verifica significa documentare
qualcosa che potrebbe non reggere.
