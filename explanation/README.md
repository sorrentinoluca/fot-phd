# Explanation — percorsi pedagogici FoT / TEP

## Inizia qui

[Guida passo per passo, Parte 1](fot_walkthrough_part1.html) — dal problema di
ricerca al confine fra rappresentazione e reasoning (§0–15 della narrativa).
Aprire l'HTML in un browser: funziona anche offline, senza installazioni o API.
Le interazioni mostrano finestre e scelte LOBO già definite: non fanno tuning.

Il filo conduttore è F1 batch 1, con un ingrandimento su XMEAS-1. È un esempio
development, non un caso final held-out. I numeri vengono dagli artefatti già
committati; il testo neutrale coincide con EXM-001. Normal di calibrazione,
caso illustrato e nuovo held-out non vengono confusi o riutilizzati come se
fossero lo stesso dato. La Parte 1 non esegue né illustra una nuova diagnosi.

Fonti autorevoli, in ordine:

1. [Freeze Phase A](../VERBALIZER_V2_FREEZE.md),
   [freeze Phase B](../phase_b/PHASE_B_PROTOCOL_FREEZE.md) e artefatti scientifici;
2. [narrativa tecnica canonica](../docs/FOT_PROJECT_TECHNICAL_NARRATIVE.md);
3. [companion LLM](../docs/FOT_PROJECT_LLM_REFERENCE.md).

Questa cartella è un supporto didattico post-results, non un nuovo protocollo,
configurazione, risultato o freeze. In caso di conflitto prevalgono gli artefatti
scientifici frozen. Il commit sorgente della guida è
`10acccdd3dd8b8bab9ee0b584c99899d59d8c906`.

## Materiale precedente conservato

I tre file precedentemente locali in `docs/` sono stati raccolti in `archive/`
senza cambiare un byte:

| File | Uso | SHA-256 |
|---|---|---|
| [fot_7_flow_svg.html](archive/fot_7_flow_svg.html) | Schema precedente; contiene tre figure e le ambiguità discusse nell'audit | `9178397d2d3e6bb764fbf91814aa468fa5a0a78769dbc12a73dcd355b7412ae8` |
| [explain_1.png](archive/explain_1.png) | Immagine storica Phase B, non descrizione normativa dell'esecuzione finale | `32151e73101f0882abe9fc4f44b9eddb0aab0b3fbf7c70bd3c835ed4d8e0f3bd` |
| [explain_2.png](archive/explain_2.png) | Immagine storica Phase A, non tutorial completo | `63a5a7990c85fd7965978ede9967c37b99ba05fbe516fbcba48989a46b9292d6` |

Attenzione: `explain_1.png` dice che Phase B non è ancora stata eseguita e può
suggerire una generazione di insight dal caso held-out. Non è lo stato finale:
gli insight finali provengono da development; il test non alimenta la libreria.
`explain_2.png` colloca visivamente la calibrazione dopo il caso: non leggerla
come calibrazione online. L'HTML storico chiama genericamente ogni caso “8
finestre” e “540 richieste”; la nuova guida distingue i contesti. Nella campagna
finale furono 540 repetition e 541 provider attempt, includendo un retry.

## Verifica didattica, non nuova evaluation

Da root:

```bash
python explanation/test_explanation.py
```

I test leggono gli artefatti esistenti, controllano soglie, otto righe
dell'esempio, conteggi temporali, testo, link e hash dell'archivio. Non aprono
workbook raw, non fanno API call, non rigenerano risultati e non scrivono file.

La prosecuzione naturale (Parte 2, non creata qui) sarà §16 e seguenti:
pseudolabel, esempi locali, insight, A/B/E, validazione dell'output, R=3,
prediction freeze e ground-truth evaluation.
