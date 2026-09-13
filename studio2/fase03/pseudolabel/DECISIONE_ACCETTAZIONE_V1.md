# Decisione dell’autore — conservazione del sorteggio pseudolabel v1

Data: 2026-09-13. Autorizzazione: l’autore ha risposto «Procedi così» alla proposta di
mantenere v1 e il sorteggio unico, registrare correlazione e limite del test, svolgere
la verifica indipendente e integrare/congelare soltanto dopo esito positivo.

## Decisione e momento della decisione

Si conservano senza modifiche namespace, seed, mapping, assegnazione agenti,
derangement e log della versione v1. Non si cercano candidati alternativi.
Questa accettazione è **successiva all’osservazione delle label**: non viene presentata
come un criterio statistico pre-specificato né cambia retroattivamente la specifica.
Il replay in memoria per verificare gli stessi byte non è una nuova selezione.

## Correlazione osservata e limite del controllo

Sulle otto label dei fault, esclusa `Normal`, la correlazione di Spearman fra rango
di catalogo e rango lessicografico è −0,833333… (−5/6). F15, F14 e F13 occupano
le prime tre posizioni lessicografiche. Fonte: `PSEUDOLABEL_MAP.json`; il calcolo
è riproducibile anche nel test `test_opacity_no_correlation_with_catalog_order`.

Quel nome di test eccede ciò che viene controllato: `|rho| < 1` esclude soltanto
l’ordine perfettamente crescente o decrescente. **Non dimostra assenza di correlazione**
e non soddisfa letteralmente la richiesta iniziale «nessuna correlazione con
l’ordine del catalogo». L’autore accetta esplicitamente questa differenza,
conservando il risultato unico e rendendone visibile il limite. Non si introduce
una nuova soglia di accettazione dopo aver osservato il risultato.

Le stringhe non contengono un identificatore esplicito del proprio fault secondo
le guardie implementate; questo non equivale a indipendenza statistica né a
segretezza crittografica. Namespace, algoritmo e insieme degli identificatori
consentono di ricostruire il mapping. Il confine operativo resta evaluator-side:
non fornire mapping, log, identificatori reali o istruzioni di derivazione nei
prompt del modello sottoposto all’esperimento.

## Interfaccia con 03.10 e 03.12

Non si cambia ora l’ordine per compensare la correlazione osservata. `label_space`
e tutti gli artefatti v1 restano invariati. Se occorre controllare la posizione
nei prompt, 03.10/03.12 dovranno fissare prima del pilot una regola generale,
riproducibile e comune alle condizioni confrontate, distinguendo presentazione
da mapping e derangement congelati. Questa decisione non sceglie quella regola.

## Condizioni per integrazione e tag

Verifica indipendente delle fonti primarie, eventuali correzioni tracciate e
riesame con esito OK precedono aggiornamento del walkthrough, integrazione e tag.
Si applicano le condizioni di `PSEUDOLABEL_FREEZE.json`: verifica OK registrata,
commit sorgente raggiungibile da `origin/main` e replay `--check` al commit taggato.
Il freeze originale resta una fotografia dello stato pending; il verbale e il
successivo record di pubblicazione documenteranno il completamento dei controlli,
senza riscriverne le impronte. La Fase 03 resta aperta.
