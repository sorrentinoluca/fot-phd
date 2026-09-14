# Controlled evaluation protocol

## Catalogo e dati di sviluppo

Il catalogo contiene otto fault scelti mediante criteri congelati prima dell'estrazione D1: quattro
classi di continuità e quattro nuove classi estratte dallo spazio ammissibile. I criteri impongono
copertura dei meccanismi, evitano duplicazioni di identità e includono uno strato di difficoltà
documentato esternamente; non usano separabilità o risultati interni per-fault.
[Fonte: tag `studio2-fase03-catalogo-D1-frozen-001`; `selection/REPORT_CATALOGO_D1.md`; piano §2.2, D1, §12.1–§12.4]

I run fault di sviluppo comprendono cinque realizzazioni per ciascuna classe, per un totale di
quaranta simulazioni. Ogni run usa un solo IDV, stato iniziale qualificato, solver `ode45`, campionamento
a un minuto, innesco a 25 h e 40 h post-fault. Il generatore usa Philox4x32-10 con chiave radice e
stream separato per run; i quaranta stream di sviluppo occupano l'intervallo 30000–30039.
[Fonte: `fault_runs/SPECIFICA_RUN_FAULT.md`, `REPORT_RUN_FAULT.md`, `SOURCE_AUDIT.json`]

Per le sticking valve il protocollo devia esplicitamente dalla raccomandazione di Downs e Vogel di
usare un disturbo congiunto o un cambio di setpoint: mantiene un solo IDV e conserva anche segnali
deboli, assenti o trip. Questa scelta delimita ciò che il test può generalizzare sul meccanismo.
[Fonte bibliografica: Downs & Vogel, `docs/letteratura.md` §14.3; fonte operativa: `fault_runs/SPECIFICA_RUN_FAULT.md` §2]

## Separazione sviluppo–calibrazione–test

Sviluppo, calibrazione Normal e test hanno ruoli distinti. I dati di sviluppo servono a evidence,
insight e prototipi; `cal_thr` fissa la soglia e `far_ver` ne verifica il comportamento senza
ricalibrazione; i run di test sono nuovi, hashati e sigillati e non possono orientare soglie,
insight, prompt, endpoint o analisi.
[Fonte: piano §8.1, §13 risposte 4–5; 03.5; `fault_runs/REPORT_RUN_FAULT.md`]

Seed e stream di sviluppo, calibrazione e test sono disgiunti e registrati. Le assegnazioni
donatore–ricevente e le mappe evaluator-side sono costruite sui soli identificativi prima del
freeze; i segnali e i risultati del test non vengono ispezionati per decisioni progettuali.
[Fonte: piano §8.8, §13 risposta 5; 03.7 `DRAW_LOG.json`; 03.8 §1]

`[DECISIONE: D2 — sei oppure otto run di test per fault]`. Un run simulato è il cluster fisico e
tutte le righe agente-caso derivate dallo stesso run restano unite nel ricampionamento. La proposta
di 03.8 raccomanda otto run e sessantaquattro cluster, ma resta pendente finché l'autore non la
congela.
[Fonte: piano §0.1, §8.1, §8.5; 03.8 §2, §7 e §15]

## Popolazioni, condizioni ed endpoint

La popolazione primaria è local-unseen: per ogni caso fault, il proprietario della classe è
local-seen e gli altri sette agenti sono local-unseen. Normal, fault fuori catalogo e ablazioni
costituiscono popolazioni secondarie o descrittive e non vengono mescolate all'endpoint primario.
[Fonte: piano §8.5–§8.6; 03.8 §2]

Le condizioni A, B-LF ed E-LF sono valutate sulle stesse coppie agente-caso. Per ogni condizione si
riportano separatamente: accuratezza su tutti i tentativi, con astensione come errore; tasso di
astensione; accuratezza sui soli casi non astenuti. Una risposta non valida resta un errore di
formato, non un'astensione, e viene riportata separatamente.
[Fonte: piano §8.5; 03.8 §3]

Il reporting è stratificato fra classi di continuità, classi nuove e aggregato, oltre alle viste
per fault e per agente. La stratificazione rende visibile se il risultato aggregato dipende dalla
selezione storica, ma non trasforma i sottogruppi in test confermativi.
[Fonte: piano §8.5; 03.8 §12–§13]

## Ipotesi e inferenza pre-specificate

H1 verifica la superiorità di B-LF su E-LF nei local-unseen; H2 la superiorità di B-LF su A nella
stessa popolazione; H3 la non inferiorità di B-LF rispetto ad A sui local-seen. L'ordine proposto è
H1→H2→H3, procedendo soltanto se il test precedente passa. `[DECISIONE: confermare gerarchia,
livello unilaterale, test locali e margine m]`.
[Fonte: piano §8.5; 03.8 §4–§5, stato `proposed_pending_author_decisions`]

La proposta statistica usa medie appaiate per cluster e un test di Hoeffding per H1/H2, un test score
per proporzioni appaiate per H3 e bootstrap stratificato per cluster per gli intervalli. Il bootstrap
mantiene insieme le sette righe local-unseen di ciascun run e misura variabilità fra run simulati,
non variabilità delle risposte ripetute del modello. `[DECISIONE: confermare specifica 03.8]`.
[Fonte: 03.8 §4, §6 e §14; stato proposto]

`[DECISIONE: margine m]` è giustificato operativamente e controllato rispetto alla risoluzione del
disegno; non viene calibrato sui risultati storici. `[RISULTATO: stime, intervalli, decisioni H1–H3
e stato della sequenza]`.
[Fonte: piano §8.5; 03.8 §5]

## Controlli e analisi descrittive

Il test OOD presenta due fault fuori catalogo in tutte e tre le condizioni e misura astensione,
falsi positivi in-catalogo e diagnosi forzate. `[DECISIONE: fault OOD e sostituti]`. Con sei eventi
fisici è una sonda di esistenza e non una caratterizzazione dell'open set.
[Fonte: piano §8.6; 03.8 §8 e §14]

L'ablazione local-first valuta B senza la politica sui local-seen e su coppie confondibili definite
meccanicamente prima dell'apertura del test. `[DECISIONE: coppie D11 e sottoinsieme]`. Essa misura
come la politica sposta errori e astensioni; non neutralizza il loro rischio.
[Fonte: piano §8.3; 03.8 §9 e §14]

Le baseline comprendono un comparatore numerico a prototipi sulle stesse feature, una rete locale,
FedAvg e la stessa rete addestrata sui dati aggregati. Tutte usano solo sviluppo per il fit e gli
stessi casi di test per la valutazione; non si effettua tuning sul test. `[RISULTATO: valori e
intervalli delle quattro baseline]`.
[Fonte: piano §9.1–§9.3; riferimento bibliografico FedAvg da integrare tramite Letteratura_LLM]

Il producer-swap usa una libreria completa per ciascun producer e misura una differenza appaiata su
dati vergini, sotto parità di schema e cap. Conformità, retry, troncamenti, token, ID del modello,
request ID, fingerprint, timestamp e hash della risposta sono registrati. `[RISULTATO: effetto del
producer e tabella di conformità]`.
[Fonte: piano §8.4, §8.7, §8.9]

`[DECISIONE: politica R]`. Il pilot tecnico usa ripetizioni dello stesso prompt per decidere se il
nucleo può procedere con R=1 e audit continuo oppure richiede R=3. L'assenza di divergenze osservate
non dimostra determinismo; il set canary rileva cambi di comportamento durante l'esecuzione senza
poterli prevenire.
[Fonte: piano §8.7; 03.8 §10, §14]

Q8 designa lo scenario con otto agenti e otto fault; identità del modello, API e controlli di
determinismo sono registrati separatamente nel ramo D9 effettivamente attivato.
[Fonte: piano §8.1, §8.7 e D9]

> **VARIANTE D9.1 — Qwen-2.4T.** Attivare soltanto se disponibile e promosso dal pilot entro la data
> prevista. Registrare versione/API e controlli effettivi; il producer alternativo non è configurato
> da D9 in questo ramo. `[DECISIONE: esito del gate]`.
>
> [Fonte: piano revisione 7, D9 opzione 1]

> **VARIANTE D9.2 — Qwen-27B + Terra.** Attivare soltanto dopo pilot positivo. Qwen-27B è producer
> principale e consumer; Terra è producer alternativo esclusivamente nel braccio swap. L'handoff
> 03.13 documenta il pilot Qwen-27B FP8 locale e l'indisponibilità di Qwen-2.4T, non un GO/NO-GO.
>
> [Fonte: piano revisione 7, D9 opzione 2; handoff 03.13]

> **VARIANTE D9.3 — arresto dell'espansione.** Se Qwen-27B fallisce parsing, stabilità o contesto,
> arrestare l'espansione e lasciare all'autore la scelta fra Terra-only e una submission successiva.
> Nell'eventuale Terra-only registrare solo i controlli disponibili e non presupporre uno swap.
>
> [Fonte: piano revisione 7, D9 opzione 3; prompt 03.15]
