# Addendum 03.8 — due proposte da approvare

Preparato il 2026-09-14. Stato: **PROPOSTA; A e B pending**. Base: revisione 9,
commit `0f1a9bae8b522f614720fa5efe7bd9d2577609ae`.
Le approvazioni storiche di Luca restano valide e non vengono richieste nuovamente.
Questo testo non modifica ancora il piano e non è coperto dall'OK della rev. 9.

## A — Risorse e ramo R=3

Si propone di sostituire il tetto rigido di pianificazione di 3.700 chiamate con
un prospetto completo delle richieste, distinto per blocco e modello, e una verifica
del tempo necessario fondata sulle misure del pilot della configurazione effettiva.
La dichiarazione del referente «non hai limiti di utilizzo in token» riguarda i
token: non autorizza questa modifica né garantisce numero di richieste, velocità,
concorrenza o disponibilità temporale illimitati.

R=3 resta attivato esclusivamente dalla divergenza della coppia parsata
(`abstain`, `predicted_label`) o della validità secondo §10–11: non dalla sola
assenza di temperatura/seed. Il ramo è eseguibile soltanto se il conteggio completo
e il tempo misurato risultano compatibili con la finestra operativa del piano,
incluso il margine temporale del 20%. La finestra non viene estesa automaticamente.
Se il ramo non è fattibile, si sospende per ragioni organizzative e si rimette la
decisione all'autore, senza ridurre automaticamente il disegno né dichiarare un
fallimento scientifico. Restano invariati l'hard stop cumulativo di 200 richieste
del pilot, la riserva unica `8 × remediation + trasporto ≤ 15`, i massimi 152/160,
le regole sui retry e tutte le altre condizioni di GO.

L'approvazione di A autorizzerebbe questa regola organizzativa; non attesterebbe
la fattibilità ancora da misurare e non sceglierebbe il modello definitivo D9.
Il [prospetto di budget](BUDGET_RISORSE_03_8.md) esplicita i parametri ancora mancanti.

## B — Ordine OOD e congelamento

Si propone di correggere §16: prima del primo run di test si congelano candidati
OOD F6/F4, criteri tecnici, catene F6→F5→F12 e F4→F11→F5, regole di sostituzione,
campioni, scorte e ogni altra scelta statistica. In 03.11, **dopo questo
congelamento e prima di qualunque chiamata ai modelli sui test**, si verificano
generabilità, trip nella finestra prescritta e ammissibilità tecnica dei run.

I controlli sono esclusivamente tecnici e tracciati: prestazioni diagnostiche,
separabilità e risultati dei modelli non possono essere usati per scegliere i
fault. Ogni sostituto deve superare le proprie verifiche di rilevabilità e
ammissibilità; i due OOD restano distinti. Si applicano solo gli impedimenti e
le catene già pre-specificati. Un caso non risolto dalla regola, incluse catene
che arrivino entrambe a F5, impone sospensione e decisione esplicita dell'autore.
Non è consentita una modifica silenziosa del piano né una sostituzione dopo le
chiamate. Le undici scorte sostituiscono run, senza aggiungere osservazioni.

La verifica bibliografica di F6 è soddisfatta nel perimetro PHM; non surroga i
controlli tecnici. Questi diventerebbero condizioni di esecuzione delle chiamate
di test, conservate e registrate separatamente dalle condizioni di congelamento
del disegno. La correzione elimina la dipendenza circolare 03.8→03.11→03.8;
non chiude retroattivamente una condizione della review rev. 9.

## Registrazione delle nuove decisioni

| Proposta | Esito espresso dall'autore | Data effettiva | Riferimento della risposta |
| --- | --- | --- | --- |
| A | pending | — | — |
| B | pending | — | — |

La revisione successiva alla 9 sarà prodotta solo dopo le risposte necessarie,
riportando il delta effettivamente approvato. Firma materiale: **pending**,
distinta dall'eventuale approvazione in conversazione.
