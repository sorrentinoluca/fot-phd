# Threats to validity

## Validità interna e inferenza

Con R=1 la variabilità della risposta del modello alla stessa richiesta non è stimata sul campione
completo. Il pilot, l'audit ripetuto su un sottoinsieme e il canary possono rilevare instabilità,
ma non rendono il singolo output equivalente a una media su repliche.
[Fonte: piano §8.7; 03.8 §14 punto 1]

Le sette decisioni agente-caso derivate dallo stesso run condividono l'evidence e sono correlate.
Il ricampionamento mantiene il run come cluster, ma la potenza dipende dalla correlazione
intra-cluster ignota; trattare le righe come indipendenti produrrebbe incertezza troppo ottimista.
[Fonte: 03.8 §2, §6, §14 punto 2]

H3 dispone di una sola osservazione local-seen per run e può avere poche coppie discordanti. Il test
score proposto evita di usare il percentile bootstrap come decisione, mentre un esito senza
discordanze deve essere riportato letteralmente. Per H1/H2 il test proposto è valido ma conservativo
e può non confermare effetti moderati pur stimandoli.
[Fonte: 03.8 §4, §7, §14 punto 3]

L'astensione conta come errore nell'endpoint primario in-catalogo. Questa scelta penalizza una
condizione che si astiene spesso, ma evita di premiare una diagnosi mancata; tasso di astensione e
accuratezza condizionata ai non astenuti devono sempre accompagnare il primario.
[Fonte: piano §8.5; 03.8 §3, §14 punto 4]

La politica local-first può spostare errori e astensioni in entrambe le direzioni. Tenerla costante
fra B-LF ed E-LF isola informazione e politica nel contrasto principale, mentre l'ablazione ne misura
l'effetto su un sottoinsieme pre-specificato senza dimostrarne innocuità generale.
[Fonte: piano §8.2–§8.3; 03.8 §14 punto 5]

Le molte viste per fault, agente, strato e analisi accessorie sono descrittive. Soltanto H1–H3,
se la gerarchia viene approvata e congelata, possono sostenere dichiarazioni confermative; nessuna
stima secondaria viene promossa dopo l'osservazione.
[Fonte: 03.8 §13–§14 punto 11]

## Costrutto e misurazione

Il verbalizzatore è deterministico ma comprime la traiettoria in feature, flag, JSON e testo. La
neutralità lessicale e la conformità allo schema non provano completezza semantica: un meccanismo
può non emergere nelle feature e una narrativa valida può non essere scientificamente fedele.
[Fonte: 03.6 `DIPENDENZE_EVIDENCE.md` §4; 03.12 `DECISIONE_SCHEMA_INSIGHT.md`; FaultExplainer in `docs/letteratura.md` §14.2]

Le pseudolabel sono opache rispetto alle guardie implementate, ma derivazione e mapping sono
riproducibili e non segreti. L'opacità riduce leakage nominale; non dimostra indipendenza statistica,
assenza di correlazioni accidentali o impossibilità di ricostruzione evaluator-side.
[Fonte: 03.7 `REPORT_PSEUDOLABEL.md` §1, «Osservazione e limite del controllo»]

Il controllo E modifica soltanto il campo di associazione nel file canonico, ma il suo effetto
dipende dal particolare derangement congelato. Un singolo sorteggio misura quella corruzione
realizzata e non la media su tutte le associazioni errate possibili.
[Fonte: 03.7 `SPECIFICA_PSEUDOLABEL.md` §5; piano §8.9; limite analogo in piano §8.12]

La conformità producer-side non coincide con la tracciabilità reporter-side di EviFDD-Agent e non
misura l'accuratezza diagnostica. Validità, retry, troncamenti e token devono restare metriche
operative separate dagli endpoint clinici o di processo.
[Fonte bibliografica: EviFDD-Agent, `docs/letteratura.md` §14.2; fonte di disegno: piano §8.9–§8.10]

## Validità esterna e scope federato

Sviluppo e test provengono dallo stesso simulatore TEP con configurazione invariata e seed disgiunti.
Questo controlla il riuso dei run ma non dimostra trasferimento a impianti reali, simulatori diversi,
drift operativo, rumore di sensori non modellato o altri processi industriali.
[Fonte: 03.8 §14 punto 9; piano §5 e §12.3]

Il catalogo copre otto classi e lo studio usa otto agenti logici. La scala è maggiore di quella
esplorativa ma resta piccola; non misura throughput di rete, nodi offline, latenza distribuita,
streaming o comportamento con decine o centinaia di partecipanti.
[Fonte: piano §5 G2, G3, CF2/C18; P065 in `docs/letteratura.md` §14.2]

La sonda OOD comprende due classi e tre run per classe. Può mostrare che l'astensione avviene in
alcuni eventi, ma non caratterizza copertura open-set, tasso di falsi positivi su una popolazione
ampia o generalizzazione a fault non catalogati.
[Fonte: piano §8.6; 03.8 §14 punto 6]

La difficoltà H è ereditata da tassi di rilevazione PCA pubblicati e non da diagnosi verbalizzate.
È adatta alla stratificazione descrittiva, non a prevedere quali classi saranno difficili per il
reasoner o a spiegare a posteriori un risultato.
[Fonte: piano §12.1–§12.4; 03.8 §14 punto 10]

Alcuni meccanismi hanno poche istanze nel catalogo; in particolare il drift lento è rappresentato
da una sola classe. Le conclusioni per quel meccanismo restano relative alla classe osservata e non
si estendono automaticamente alla famiglia intera.
[Fonte: piano §8.12; 03.8 §14 punto 7]

Lo studio simula una federazione di agenti senza server di aggregazione, rete o secure aggregation.
Che i raw non siano scambiati è una proprietà del protocollo, non una garanzia di privacy; CF1/CF5
sullo scope FL e G7 sulla privacy restano aperte.
[Fonte: piano §5 G3/G7/CF1/CF5, §12.8; DP-FPL e P065 in `docs/letteratura.md` §14.1–§14.2]

## Dipendenza dal modello e stabilità operativa

Un singolo modello principale può legare gli esiti alla sua tokenizzazione, istruzione, capacità di
seguire lo schema e stile di ragionamento. Il producer-swap stima soltanto una componente di questa
dipendenza; non dimostra portabilità end-to-end o generalità fra famiglie di modelli.
[Fonte: piano §5 G5, §8.4; P065/SYNAPSE in `docs/letteratura.md` §14.2]

Un provider può cambiare silenziosamente backend o comportamento durante l'esecuzione. ID restituito,
request ID, fingerprint, hash, timestamp e canary migliorano la ricostruzione forense e il rilevamento,
ma non impediscono il cambio né ne identificano sempre la causa.
[Fonte: piano §8.7; 03.8 §10, §14 punto 8]

> **VARIANTE Q8.** Dichiarare capacità dell'API, modello restituito e qualsiasi instabilità osservata
> nella configurazione Q8. `[RISULTATO: audit e canary]`.
>
> [Fonte: piano §8.7; D9]

> **VARIANTE TERRA-ONLY.** Dichiarare le capacità effettivamente esposte da Terra e che il fallback
> non costituisce una verifica cross-model indipendente. `[RISULTATO: audit e canary]`.
>
> [Fonte: piano D9 opzione 3; prompt 03.15]

