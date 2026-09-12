# Modalità letteratura — progetto FoT-TEP

**Leggi prima `Prompt_LLM.md`**, in questa stessa cartella: contiene le regole comuni — costi,
precedenze, divieto di inventare riferimenti. Qui ci sono solo le regole del ciclo bibliografico.

**La procedura è `docs/MAINTENANCE.md` §6 e non la ripeto.** Questo file aggiunge i controlli
che §6 non copre e i criteri che altrimenti restano impliciti.

## Dove vive la letteratura

`docs/letteratura.md` ↔ `docs/letteratura.html`. **Luogo unico**: nessun altro file contiene
corpus. Vale per il primo studio, per lo studio 2 e per quelli successivi — non appartiene a
nessuno dei due walkthrough, che si limitano a rimandare.

La numerazione interna parte da **14.1** perché il corpus è stato spostato dal §14 del
walkthrough del primo studio senza rinumerare: decine di riferimenti nel repository citano
«§14.1», «§14.2», «§14.5». **Non rinumerare.**

| Sezione | Contenuto |
| --- | --- |
| §14.1 | Corpus completo, per categoria, con autori, anno e colore di vicinanza |
| §14.2 | Schede estese: solo i lavori 🟢 |
| §14.3 | Riferimenti metodologici e di dominio |
| §14.4 | Perimetro del corpus consultato |
| §14.5 | I lavori più vicini, con «claim che ci vieta / claim che resta» |
| §14.6 | Tenuta della novità |
| §14.7 | Priorità bibliografica |

## I tre colori, e come si decidono

- 🟢 **Vicino** — incide sul disegno **oppure** delimita un claim. Obbliga a una scheda §14.2.
- 🟡 **Adiacente** — condivide un asse (dominio, regime non-IID, payload) ma non cambia una
  scelta né vieta un'affermazione.
- 🔴 **Distante** — sfondo del campo, documenta il perimetro consultato.

**Il colore non è un giudizio di qualità**: dice quanto il lavoro tocca *questo* progetto. Un
articolo eccellente su un dominio estraneo è 🔴. Nel dubbio fra 🟢 e 🟡, chiediti: *se un revisore
mi mettesse davanti questo lavoro, dovrei cambiare una frase del paper?* Se no, è 🟡.

Ogni colore va **motivato in una riga** nella prosa di chiusura della categoria.

## Formato della scheda §14.2

```
**Titolo esatto**
*Autori, anno*

Autori per esteso, sede, DOI. Poi che cosa fa il lavoro, in concreto.

**Rapporto con questo lavoro** — *Somiglianza:* … *Differenza:* … *Implicazione:* …
```

L'*Implicazione* è la parte che conta: deve dire **che cosa non possiamo più affermare**, o
quale scelta di disegno il lavoro sostiene. Una scheda che descrive e basta è inutile.

## Controlli che §6 non copre

1. **Riconciliazione `papers/` ↔ §14.1.** Per ogni `.pdf` in `papers/`, verifica che il lavoro
   sia in §14.1. Il nome del file è la chiave, ma **il confronto per parole chiave produce falsi
   allarmi**: FD-LLM, Truth-Conditional Captions e TceOne compaiono in §14.1 con un titolo
   diverso dal nome del file. Quando un lavoro sembra assente, **aprilo e controlla** invece di
   assumere che sia un falso positivo: è così che è emerso FaultExplainer, mancante da sempre.
2. **Coppie complete.** Nessun `.md` senza `.pdf` e nessun `.pdf` senza `.md`. Se manca uno dei
   due, va **dichiarato** nella riga di `papers/README.md`.
3. **Conversioni inservibili.** Un `.md` di poche centinaia di byte è una conversione fallita, non
   un paper corto: le scansioni JSTOR e simili non hanno strato di testo. Controlla i byte
   estraibili (`pdftotext file.pdf - | wc -c`); sotto qualche migliaio, trattalo come «PDF senza
   `.md`» e dichiaralo. Il convertitore **non segnala l'errore**.
4. **Versioni omonime.** Conferenza e rivista dello stesso lavoro sono due pubblicazioni: se la
   numerazione di teoremi o proposizioni viene citata, va verificata **sulla versione che si
   cita**. Vedi Vovk 2012 (ACML) contro la versione estesa su arXiv.
5. **Somme e conteggi.** Dopo ogni inserimento: totale dichiarato in testa alla §14.1 = somma
   dei colori = somma dei conteggi di categoria = righe effettive nelle tabelle. E lo stesso in
   `.md` e in `.html`.
6. **Titoli divergenti.** Segnala sempre i casi in cui il titolo del catalogo non coincide con
   il nome del file: capita più spesso di quanto sembri.

## Chiusura

- parità `.md` / `.html` verificata **sul contenuto**, non sul diff: stesse categorie, stesso
  ordine, stessi conteggi, stesse schede;
- link risolti;
- `python3 docs/test_explanation.py` non peggiorato rispetto al numero di partenza;
- elenco dei file toccati e **che cosa hai letto**, con il costo approssimativo.

## Quando la letteratura tocca il resto

- Se un lavoro **delimita un claim**, aggiorna anche §14.5 e §14.6, e — se il claim è nel paper —
  `docs/paper/FoT_TEP_paper_blueprint.html` (corrente E del §2 e tabella dei riferimenti, con
  lo stato di verifica).
- Se riguarda il **disegno dello studio 2**, non scriverlo nel walkthrough: la fonte del disegno
  è `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`, e le decisioni stanno nei registri di
  `docs/lit_review/`. Segnala il punto, non modificarlo di tua iniziativa.
