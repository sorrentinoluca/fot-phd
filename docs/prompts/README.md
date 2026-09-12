# docs/prompts/ — prompt operativi

Strumenti operativi, non artefatti scientifici congelati. **Le regole stanno in
`docs/MAINTENANCE.md`**: questi file dicono *come si lavora* in un dato momento, non *cosa è
vero* né *cosa è congelato*. Se un prompt e MAINTENANCE si contraddicono, prevale MAINTENANCE.
In `MAINTENANCE.md §8` c'è il contratto del lavoro: questi file sono solo la traccia pratica
per aprire il file giusto nel momento giusto.

## Quale aprire, quando

Il ciclo di una fase dello studio 2 va in un ordine, e l'ordine conta:

```
Fase_LLM  →  Verifica_LLM  →  Documentazione_LLM  →  Commit_LLM
(si lavora)   (altra finestra)   (solo dopo l'OK)      (si salva)
     ↓              ↓                   ↑
 REPORT_FASE<N>.md  VERIFICA_FASE<N>.md ┘
      in studio2/fase<N>/
```

**Le finestre non si passano il contesto, si passano file.** Ogni tappa scrive il proprio esito in
`studio2/fase<N>/`, e la successiva lo legge da lì insieme agli artefatti che cita. È l'unica
ragione per cui il ciclo funziona con finestre e modelli diversi: ciò che esiste solo in una
conversazione non è verificabile né documentabile.

| File | Aprilo quando | Finestra |
| --- | --- | --- |
| **`Prompt_LLM.md`** | Sempre, per primo: instradamento per tipo di richiesta, costi, precedenze sui conflitti | qualsiasi |
| **`Fase_LLM.md`** | Devi lavorare una fase dello studio 2 | una per fase |
| **`Verifica_LLM.md`** | La fase si ritiene conclusa, tutte le sotto-fasi chiuse | **un'altra**, preferibilmente altro modello |
| **`Documentazione_LLM.md`** | Il verificatore ha detto **OK** | dopo la verifica |
| **`Commit_LLM.md`** | C'è da committare | qualsiasi |
| **`Questions_LLM.md`** | Devi fare domande senza modificare nulla | sola lettura |
| **`Letteratura_LLM.md`** | Hai aggiunto paper in `papers/`, o va verificata una citazione | episodica |

Con Claude Code la prima riga non serve: `CLAUDE.md` alla radice carica il contratto da sé.

## Storici

| File | Cos'è |
| --- | --- |
| `PROJECT_HANDOFF_PROMPT.md` | Handoff del primo studio. Riferimenti alla vecchia collocazione della letteratura: da leggere con quella riserva |
| `CODEX_PROMPT_EXP3_CLOSE_AND_V2.md` | Chiusura di Exp3 e avvio di Exp3v2, primo studio |
| `FoT_setup_prompt_server.md` | Setup lato server per l'esecuzione |

## Perché sono separati

Ogni file copre **un momento del ciclo**, non un argomento. È la ragione per cui `Verifica_LLM.md`
è un file a sé: la verifica indipendente va eseguita in un'altra finestra, e un prompt che si apre
insieme al lavoro non sarebbe indipendente. Ed è la ragione per cui nessuno di questi file ripete
le regole: duplicarle significa farle divergere.
