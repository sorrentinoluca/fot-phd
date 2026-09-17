# Recepimento risposte Q1–Q3 — 2026-09-17

Base `1f9ebc51649fcc30a17949819a05eca2271daac0`, stessa worktree e branch.
Offline, solo documenti; nuovo commit; nessun push/merge/tag, codice, simulazione o chiamata.
Il mandato aggiornato è preservato integralmente nell’appendice del nuovo registro
`DECISIONI_AUTORE_7_3_REV2_Q1_Q3.md`, con SHA della fonte. Il prefisso è byte-identico alla
copia D1–D5, che resta invariata. Le risposte superano le proposte del REPORT_REV2 storico,
conservato intatto. Addendum revisione 1 recuperabile a 1f9ebc5, ora revisione 2.

Q1: entrambi gli intervalli sempre riportati; bootstrap descrittivo approssimato invariato,
Hoeffding bilaterale ampio (circa 0,34), nessuna selezione post-hoc.
Q2: Tango condizionato alla verifica indipendente; fallback deciso solo sull’intera griglia
al bordo **ICC=0**, tolleranza 0,055. ICC>0 stress descrittivo per Tango/Hoeffding H3 e H1/H2,
mai selettore di procedura. Distinti fattori condivisi fissi e casuali; seed/stream separati
sostengono l’indipendenza delle traiettorie, deriva LLM mitigata ma non eliminata. Il fallback
ripara l’eterogeneità delle celle e non la correlazione fra run.
Q3: audit invariato più reporting descrittivo per blocco/condizione su tutti i prompt;
meno di tre validi = invalid_incomplete_triplet anche con due concordi; nessuna confusione
con richieste di trasporto pendenti, che sospendono la chiusura.

`SPECIFICA_VERIFICA_SINTETICA_H3.md` concretizza senza dati la griglia, generazione marginale,
ICC operativa/fattibilità, seed, criteri, output e review. 1.620 scenari target, 108 punti
al bordo ICC=0 decisionali, 100.000 repliche per punto fattibile; lo script e le simulazioni
restano in sotto-fase separata. ICC è correlazione media delle coppie non degeneri,
non peso della miscela: non si simulano marginali impossibili né si falsifica l’ICC con clipping.
Per H1/H2 è specificato uno stress sui contrasti medi di cluster; non una simulazione FWER.

Controlli: hash delle 43 fonti, originale normativo e prefisso identici, fonte aggiornata
verbatim, link, assenza di domande Q1–Q3 pendenti, JSON/Markdown allineati. Guardian 35 test,
14 fallimenti e uno skip; identificativi dei 14 fallimenti identici al commit precedente.
Dettaglio in `CONTROLLI_RISPOSTE_Q1_Q3.json`. Nessuna verifica statistica eseguita o anticipata.

Restano PENDING S6/S10/S11 fino a verifica sintetica, review e recepimento del ramo;
commit/review 7.4-FIX, renderer B-noLF, quattro SHA finali, quota retry/backoff/timeout e T5,
verifica di pubblicazione/riscaricamento test-v1 e review finale. Nessuna nuova approvazione
richiesta per Q1–Q3. Questo recepimento non è il freeze né l’autorizzazione al batch.
