# Piano delle sezioni comuni del paper — sotto-fase 03.15

Stato: bozza redazionale indipendente dal modello. Le sezioni qui mappate descrivono lo scenario
Q8 — otto agenti e otto fault — e devono poter essere riusate nei diversi rami di modello previsti
da D9; le sole differenze ammesse sono raccolte nei blocchi «VARIANTE» sotto. Nessun risultato diagnostico del
nuovo studio è disponibile; soglia e FAR della 03.5 sono già verificati e recepiti.
[Fonte: prompt 03.15; piano §0.1, §8.10; blueprint §C]

## Convenzioni editoriali

`[RISULTATO]` indica una frase o un valore che potrà essere completato soltanto dopo l'esecuzione e
la verifica. `[DECISIONE: …]` indica una scelta ancora dell'autore o subordinata a un gate. Ogni
paragrafo delle bozze termina con una fonte di lavoro fra parentesi quadre, da rimuovere quando le
citazioni saranno convertite nello stile bibliografico finale. «Pre-specificato» è usato per un
protocollo fissato internamente prima dell'apertura del test; non si usa «preregistrato».
[Fonte: piano §5 C06, §8.1, §8.5; Fase_LLM]

Il delta recepisce i soli riscontri già prodotti su sviluppo e calibrazione. I numeri
storici Terra restano nei record interni e non sono usati per raccontare l'origine del
disegno nel paper o per costruire un nuovo braccio controllato. Risultati diagnostici,
abstract e conclusioni restano esclusi. Fonti del delta: sigle H, S05, S09, S08,
S08-consegna, S06, S12 e L risolte a commit/path/SHA-256 in `FONTI_DELTA_0315.json`.
Le fonti di lavoro ereditate non toccate conservano il perimetro dell'OK su `cf79e81`.
[Fonte: mandato delta 03.15; MAINTENANCE §8.2; H §5]

## Mappa

| Sezione comune | File | Stato ora | Fonti principali | Segnaposto obbligatori |
| --- | --- | --- | --- | --- |
| Related work | `related_work.md` | scrivibile | letteratura §14.1–§14.6; piano §12.5–§12.9; blueprint §E | eventuali metadati non verificati; nessun risultato |
| Metodo FoT-TEP | `method.md` | scrivibile, salvo identità del modello | piano §8.1–§8.4, §8.6, §8.9; 03.7; 03.12 | `[DECISIONE: modello]`; identità del producer alternativo |
| Verbalizzatore ed evidence | `verbalizer.md` | scrivibile | 03.6; codice congelato del primo studio; MAINTENANCE §8.2; letteratura §14.2 | normal_dev e soglia/FAR recepiti; prestazioni e conformità restano `[RISULTATO]` |
| Protocollo | `protocol.md` | disegno scritto, scelte aperte marcate | D1; run fault; 03.5; 03.7; 03.8 rev. 10 approvata, non congelata; piano §8.5–§9 | firma/freeze, fattibilità, OOD tecnici, D9; tutti gli endpoint diagnostici osservati |
| Threats to validity | `threats.md` | scrivibile | 03.8 §14; piano §2, §5, §8.6–§8.9, §12 | dipendenza effettiva dal modello e impatto delle decisioni ancora aperte |
| Controllo redazionale | `lint_paper_sections.py` | da eseguire dopo le bozze | prompt 03.15 | nessuno |
| Chiusura | `REPORT_DELTA_0315.md` | nuovo delta da verificare; report storico preservato | Fase_LLM punti 1–7 | collocazione futura in `docs/paper/`; decisioni dell'autore |

[Fonte: prompt 03.15; piano §0.1, §8.10; S08 `PIANO_STATISTICO.md` rev. 10; S08-consegna `CONSEGNA_REV10.md`]

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

Il verbalizzatore descrive la catena deterministica, le evidence fault e Normal reali,
i prototipi, la dipendenza N1–N5/soglie V2 sotto U3 e la guardia R2. La 03.5 è chiusa:
valore della soglia e FAR primario/secondario sono recepiti con i loro limiti; la 03.9
è integrata e pubblicata ma il freeze della baseline resta inefficace nello snapshot S09.
[Fonte: S05, S09, S06; `FONTI_DELTA_0315.json`; MAINTENANCE §8.2]

Il protocollo recepisce D2, test, margine, alpha, gerarchia, reporting, D11, politica R e
A/B della rev. 10 come approvati. Firma, freeze e requisiti operativi restano distinti:
conteggio completo e fattibilità misurata, OOD tecnici dopo il freeze statistico e prima
delle chiamate, D9 aperta. Non si producono nuovi esiti né si riaprono le approvazioni.
[Fonte: S08 `PIANO_STATISTICO.md`, `BUDGET_RISORSE_REV10.md`; S08-consegna `CONSEGNA_REV10.md`]

## Segnaposto e dipendenze

- `[DECISIONE: modello e data di attivazione del piano B]` nella descrizione della configurazione.
- Firma materiale e freeze statistico rev. 10, senza nuova approvazione di D2, m, α, gerarchia, D11, R o A/B.
- Fattibilità temporale T5, requisiti operativi e controlli tecnici OOD nella 03.11.
- Casi non risolti dalle catene OOD: sospensione e decisione esplicita, se si presentano.
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

> **VARIANTE D9 — stato aperto, inventario al 14 settembre 2026.** Il servizio 122B è
> dichiarato operativo dall'autore, alias API `qwen3.5-122b`, contesto 131.072 e output
> massimo 16.384; il parametro temperatura va omesso secondo la comunicazione ricevuta.
> Il 27B resta sull'altro server. Identità completa di pesi/revisione/quantizzazione,
> tokenizer/template, serving, capienza e qualificazione del servizio restano da verificare.
> Questi dati comunicati non assegnano ruoli sperimentali a 27B, 122B o Terra. Il 2.4T
> risulta non ospitabile dalla macchina; le opzioni storiche sotto non sono rami attivati.
> `[DECISIONE: D9, producer principale, consumer, producer alternativo e configurazione]`.
> Il producer-swap resta nel disegno e la decisione sull'alternativo D9.1 resta mancante.
> I risultati storici Terra non costituiscono un braccio controllato dello studio 2.
>
> [Fonte: H §§4.9, 5, impronta in `FONTI_DELTA_0315.json`; piano D9; S08-consegna `CONSEGNA_REV10.md`]

> **VARIANTE D9.1 — Qwen-2.4T.** Inserire soltanto se Qwen-2.4T diventa disponibile e supera il
> pilot entro la data prevista. Qwen-2.4T è producer principale e consumer; il braccio
> producer-swap resta nel disegno, mentre D9 non nomina il producer alternativo per questo ramo.
> `[DECISIONE: disponibilità, pilot, versione/API e producer alternativo del ramo D9.1]`.
>
> [Fonte: piano §8.4, §8.10 punto 3 e D9 opzione 1]

> **VARIANTE D9.2 — opzione storica Qwen-27B + Terra.** Il piano prevede, solo se
> l'autore attiva questo ramo e dopo pilot positivo, Qwen-27B come producer principale
> e consumer e Terra come producer alternativo nel solo swap. Qwen-27B non è un modello
> «nuovo». Il pilot 03.13 non è avviato; la disponibilità dichiarata del 122B richiede
> una decisione D9 esplicita e non sostituisce automaticamente il candidato storico.
>
> [Fonte: piano D9 opzione 2; H §§4.9, 5]

> **VARIANTE D9.3 — arresto dell'espansione.** Se anche Qwen-27B fallisce i criteri di parsing,
> stabilità o contesto, l'espansione si arresta e l'autore sceglie fra Terra-only e una submission
> successiva. Terra-only non è automaticamente attivo, non è una replica cross-model e il ruolo
> del producer-swap va qualificato secondo la configurazione effettivamente approvata.
>
> [Fonte: piano D9 opzione 3; prompt 03.15]

Fuori da questi blocchi non devono comparire frasi specifiche del modello. In particolare, related
work, definizione di A/B-LF/E-LF, verbalizzatore, pseudolabel, schema, endpoint e threats strutturali
sono identici nei rami D9.
[Fonte: prompt 03.15; piano §8.1–§8.10]

## Confine del pacchetto

Restano fuori risultati, abstract, conclusioni e figure. La futura promozione delle bozze in
`docs/paper/` è una decisione dell'autore dopo verifica indipendente; questa sotto-fase non la
anticipa.
[Fonte: prompt 03.15; MAINTENANCE §1 e §8.6]
