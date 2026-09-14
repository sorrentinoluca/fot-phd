# Piano delle sezioni comuni del paper — sotto-fase 03.15

Stato: bozza redazionale indipendente dal modello. Le sezioni qui mappate descrivono lo scenario
Q8 — otto agenti e otto fault — e devono poter essere riusate nei diversi rami di modello previsti
da D9; le sole differenze ammesse sono raccolte nei blocchi «VARIANTE» sotto. Nessun risultato del
nuovo studio è disponibile.
[Fonte: prompt 03.15; piano §0.1, §8.10; blueprint §C]

## Convenzioni editoriali

`[RISULTATO]` indica una frase o un valore che potrà essere completato soltanto dopo l'esecuzione e
la verifica. `[DECISIONE: …]` indica una scelta ancora dell'autore o subordinata a un gate. Ogni
paragrafo delle bozze termina con una fonte di lavoro fra parentesi quadre, da rimuovere quando le
citazioni saranno convertite nello stile bibliografico finale. «Pre-specificato» è usato per un
protocollo fissato internamente prima dell'apertura del test; non si usa «preregistrato».
[Fonte: piano §5 C06, §8.1, §8.5; Fase_LLM]

I soli numeri storici ammessi come motivazione sono quelli autorizzati dal piano: B = 86,1% nello
studio esplorativo e B = 94,4% nella replica, sempre accompagnati dalla formula «dichiarato
descrittivo». Non entrano altri numeri di esito, né del primo studio né del nuovo.
[Fonte: piano §8.10 punto 1; walkthrough v2 §7.3 e §8.3]

## Mappa

| Sezione comune | File | Stato ora | Fonti principali | Segnaposto obbligatori |
| --- | --- | --- | --- | --- |
| Related work | `related_work.md` | scrivibile | letteratura §14.1–§14.6; piano §12.5–§12.9; blueprint §E | eventuali metadati non verificati; nessun risultato |
| Metodo FoT-TEP | `method.md` | scrivibile, salvo identità del modello | piano §8.1–§8.4, §8.6, §8.9; 03.7; 03.12 | `[DECISIONE: modello]`; identità del producer alternativo |
| Verbalizzatore ed evidence | `verbalizer.md` | scrivibile | 03.6; codice congelato del primo studio; MAINTENANCE §8.2; letteratura §14.2 | soglia numerica e FAR non riportati; esiti di conformità come `[RISULTATO]` |
| Protocollo | `protocol.md` | disegno scritto, scelte aperte marcate | D1; run fault; 03.5; 03.7; 03.8 proposto; piano §8.5–§9 | run per fault, *m*, α/gerarchia/test, OOD/D11, politica R, modello; tutti gli endpoint osservati |
| Threats to validity | `threats.md` | scrivibile | 03.8 §14; piano §2, §5, §8.6–§8.9, §12 | dipendenza effettiva dal modello e impatto delle decisioni ancora aperte |
| Controllo redazionale | `lint_paper_sections.py` | da eseguire dopo le bozze | prompt 03.15 | nessuno |
| Chiusura | `REPORT_PAPER_SECTIONS.md` | da compilare dopo lint e test | Fase_LLM punti 1–7 | collocazione futura in `docs/paper/`; decisioni dell'autore |

[Fonte: prompt 03.15; piano §0.1, §8.10; 03.8 `PIANO_STATISTICO.md` stato proposto]

## Contenuto già scrivibile

La related work può attribuire FoT, distinguere federazione parametrica, distillazione/prototipi,
federazione testuale, TS→testo e diagnosi LLM. Il claim resta sull'intersezione fra esperienza
temporale multivariata class-disjoint, trasferimento testuale e controllo di specificità; non si
rivendicano l'invenzione di FoT, la verbalizzazione, la portabilità cross-model, l'efficienza o la
privacy.
[Fonte: letteratura §14.4–§14.6; piano §12.7–§12.9]

Il metodo può descrivere gli otto agenti, il possesso locale di Normal e di una classe di fault,
le condizioni A/B-LF/E-LF, la politica local-first, lo scambio peer-only, le pseudolabel opache, lo
schema a sei campi, la parità fra producer e il diff B→E limitato al campo pseudolabel. L'identità
del modello non è parte della definizione comune.
[Fonte: piano §8.1–§8.4, §8.9; 03.7; 03.12]

Il verbalizzatore può descrivere la catena deterministica serie → feature per finestra → JSON →
testo neutrale → firma 697-D, la baseline N1–N5 usata solo per normalizzazione sotto U3 e le guardie
anti-leakage. La soglia dello score Normal si descrive solo nella forma economica di calibrazione e
nella regola stretta `S > soglia`; valore e FAR restano esclusi finché la verifica indipendente di
03.5 non è OK.
[Fonte: 03.6 `DIPENDENZE_EVIDENCE.md`, `REPORT_EVIDENCE.md`; 03.5 a `9507143`; MAINTENANCE §8.2]

Il protocollo può descrivere catalogo e criteri congelati, quaranta run fault di sviluppo, innesco,
orizzonte, finestre, Philox, separazione dei seed, pseudolabel e endpoint. Le proposte di 03.8 sono
riportate come pre-specificazioni pendenti e mai come decisioni congelate.
[Fonte: tag catalogo D1; `fault_runs/SPECIFICA_RUN_FAULT.md` e `REPORT_RUN_FAULT.md`; 03.8]

## Segnaposto e dipendenze

- `[DECISIONE: modello e data di attivazione del piano B]` nella descrizione della configurazione.
- `[DECISIONE: D2 — sei oppure otto run di test per fault]` e conseguente numero di cluster.
- `[DECISIONE: margine m, livello unilaterale, gerarchia H1→H2→H3 e test locali]`.
- `[DECISIONE: fault OOD, coppie D11 e politica R in assenza di controlli API]`.
- `[RISULTATO: H1, H2, H3 e intervalli]`, `[RISULTATO: astensione e accuratezza condizionata]`.
- `[RISULTATO: baseline numerica, FedAvg, pavimento e soffitto]`.
- `[RISULTATO: producer-swap, conformità, retry, troncamenti e token]`.
- `[RISULTATO: sonda OOD e ablazione local-first]`.

[Fonte: piano §0.1, §8.4–§8.9, §9; 03.8 §15–§16]

## Varianti controllate

Q8 identifica sempre lo scenario sperimentale con otto agenti e otto fault, non un modello. Lo
scenario resta comune ai rami seguenti, che sono condizionati dalla decisione D9 e dal relativo
pilot.
[Fonte: piano §8.1 e D9]

> **VARIANTE D9.1 — Qwen-2.4T.** Inserire soltanto se Qwen-2.4T diventa disponibile e supera il
> pilot entro la data prevista. Qwen-2.4T è producer principale e consumer; D9 non configura un
> producer alternativo per questo ramo. `[DECISIONE: disponibilità, pilot, versione/API]`.
>
> [Fonte: piano revisione 7, D9 opzione 1]

> **VARIANTE D9.2 — Qwen-27B con producer alternativo Terra.** Inserire soltanto dopo esito positivo
> del pilot Qwen-27B: Qwen-27B è producer principale e consumer, mentre Terra è producer alternativo
> nel solo braccio producer-swap. L'handoff 03.13 registra Qwen-27B FP8 locale come combinazione in
> prova e Qwen-2.4T come non disponibile; non anticipa il GO/NO-GO.
>
> [Fonte: piano revisione 7, D9 opzione 2; handoff 03.13]

> **VARIANTE D9.3 — arresto dell'espansione.** Se anche Qwen-27B fallisce i criteri di parsing,
> stabilità o contesto, l'espansione si arresta e l'autore sceglie fra Terra-only e una submission
> successiva. Terra-only non è automaticamente attivo, non è una replica cross-model e il ruolo
> del producer-swap va qualificato secondo la configurazione effettivamente approvata.
>
> [Fonte: piano revisione 7, D9 opzione 3; prompt 03.15]

Fuori da questi blocchi non devono comparire frasi specifiche del modello. In particolare, related
work, definizione di A/B-LF/E-LF, verbalizzatore, pseudolabel, schema, endpoint e threats strutturali
sono identici nei rami D9.
[Fonte: prompt 03.15; piano §8.1–§8.10]

## Confine del pacchetto

Restano fuori risultati, abstract, conclusioni e figure. La futura promozione delle bozze in
`docs/paper/` è una decisione dell'autore dopo verifica indipendente; questa sotto-fase non la
anticipa.
[Fonte: prompt 03.15; MAINTENANCE §1 e §8.6]
