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

Il lotto reale `normal_dev`, generato il 14 settembre 2026, comprende 40 run Normal
preassegnati, cinque in esclusiva a ciascun agente, con stream Philox4x32-10 60000–60039
e chiave `0x464f545445503032`. La configurazione Mode 1 usa `Ts_base=0.0005 h`, solver
`ode45` e uscita al minuto. Ogni run dura 65 h: burn-in `[0,20)` e controllo `[20,25)`
sono esclusi; le otto finestre half-open da 5 h in `[25,65)` danno 320 finestre, ma
soltanto 40 cluster fisici. Non sono 320 repliche indipendenti.
[Fonte: S09 `SPECIFICA_NORMAL_DEV.md`, `plans/normal_dev.csv`, `AUDIT_NORMAL_DEV.json`, `BASELINE_FREEZE_rev003.json`; pin in `FONTI_DELTA_0315.json`]

Il lotto serve esclusivamente a prototipi Normal, esempi locali e classe Normal delle
baseline neurali locali, FedAvg e centralizzata. Sono vietati fit della normalizzazione,
scelta/calibrazione delle soglie, verifica FAR, selezione del protocollo e uso come test.
L'audit ha verificato identità piano–manifest–workbook, configurazione e impronte; le
deviazioni di pathname e tracciabilità del comando/MATLABPATH sono state accettate
esplicitamente, senza convertirle in conformità o provare il checkout al lancio.
[Fonte: S09 `SPECIFICA_NORMAL_DEV.md`, `DECISIONE_ACCETTAZIONE_NORMAL_DEV.md`, `REPORT_BASELINE_NUMERICA.md`]

La 03.9 è integrata e i dati sono pubblicati con riscaricamento verificato; il manifest
rev. 3 conserva `effective=false`. Alla fonte S09 restano raccordo dei nomi delle metriche
in 03.10, raggiungibilità in main dei sorgenti 03.6 e successivo tag della baseline.
La pubblicazione dei dati non rende efficace il freeze della baseline.
[Fonte: S09 `CONSEGNA_INTEGRAZIONE_03_9.md`, `BASELINE_FREEZE_rev003.json`, `VERIFICA_RISCARICAMENTO_NORMAL_DEV.json`]

## Separazione sviluppo–calibrazione–test

Sviluppo, calibrazione Normal e test hanno ruoli distinti. I dati di sviluppo servono a evidence,
insight e prototipi; `cal_thr` fissa la soglia e `far_ver` ne verifica il comportamento senza
ricalibrazione; i run di test dovranno essere nuovi, hashati e sigillati e non potranno orientare soglie,
insight, prompt, endpoint o analisi.
[Fonte: piano §8.1, §13 risposte 4–5; 03.5; `fault_runs/REPORT_RUN_FAULT.md`]

Seed e stream dei nuovi lotti devono essere disgiunti e registrati; quelli dei test
saranno fissati in 03.11 contro l’inventario dei lotti già esistenti. Le assegnazioni
donatore–ricevente e le mappe evaluator-side sono costruite sui soli identificativi prima del
freeze; i segnali e i risultati del test non vengono ispezionati per decisioni progettuali.
[Fonte: piano §8.8, §13 risposta 5; 03.7 `DRAW_LOG.json`; S08 `PIANO_STATISTICO.md` §§1, 7.4, 16]

La soglia Normal è stata congelata prima dell'apertura analitica registrata di `far_ver`;
i file erano già generati e accessibili. Il sigillo attesta identità e le tracce documentano
l'ordine delle analisi, senza dimostrare l'assenza assoluta di consultazioni non registrate.
L'autore ha accettato questo limite mantenendo soglia e risultati FAR invariati; 03.5 è chiusa.
[Fonte: S05 `THRESHOLD_FREEZE.json`, `DECISIONE_AUTORE_FAR.md`, `INTEGRAZIONE_03_5.md`]

D2=8 è approvata: otto run di test per fault, 64 cluster fault, più otto run Normal primari,
per 72 run primari complessivi. Un run simulato è il cluster fisico: tutte le righe
agente-caso derivate da quel run restano unite nel ricampionamento. Approvazione, firma
materiale e congelamento statistico sono distinti: firma e freeze/tag restano pendenti.
[Fonte: S08 `PIANO_STATISTICO.md` §§2, 7, 15–16; S08-consegna `CONSEGNA_REV10.md`]

## Popolazioni, condizioni ed endpoint

La popolazione primaria è local-unseen: per ogni caso fault, il proprietario della classe è
local-seen e gli altri sette agenti sono local-unseen. Normal, fault fuori catalogo e ablazioni
costituiscono popolazioni secondarie o descrittive e non vengono mescolate all'endpoint primario.
[Fonte: piano §8.5–§8.6; 03.8 §2]

Le condizioni A, B-LF ed E-LF sono valutate sulle stesse coppie agente-caso. Per ogni condizione si
riportano separatamente: accuratezza su tutti i tentativi, con astensione come errore; tasso di
astensione; accuratezza sui soli casi non astenuti. Una risposta non valida conta come errore nel primo e nel terzo numero, entra nel
denominatore dei non astenuti e non è un'astensione; il suo tasso è riportato separatamente.
I conteggi includono corretti, astenuti, non astenuti, invalidi e totale. Il raccordo 03.10
richiesto dalla 03.9 è `accuracy`→`accuracy_all`, `n`→`total`, `abstentions`→`abstained`,
con gestione esplicita di `non_abstained` e `invalid`.
[Fonte: S08 `PIANO_STATISTICO.md` §3; S09 `CONSEGNA_INTEGRAZIONE_03_9.md`]

Il reporting è stratificato fra classi di continuità, classi nuove e aggregato, oltre alle viste
per fault e per agente. La stratificazione rende visibile se il risultato aggregato dipende dalla
selezione storica, ma non trasforma i sottogruppi in test confermativi.
[Fonte: piano §8.5; 03.8 §12–§13]

## Ipotesi e inferenza pre-specificate

H1 verifica la superiorità di B-LF su E-LF nei local-unseen; H2 la superiorità di B-LF
su A nella stessa popolazione; H3 la non inferiorità di B-LF rispetto ad A sui local-seen.
La sequenza approvata è H1→H2→H3, a livello unilaterale α=0,05: ci si arresta al primo
non-rifiuto. Le ipotesi successive conservano stime e intervalli senza dichiarazione
confermativa. Non si cambia la sequenza dopo l'osservazione.
[Fonte: S08 `PIANO_STATISTICO.md` §§4, 15; `DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md`]

Per H1/H2 si applica Hoeffding alle medie appaiate di cluster in [−1,1], con nulla debole
sulla media Δ≤0 e indipendenza fra cluster richiesta. La garanzia finita sul livello
ammette dipendenza interna al cluster, ma non prova l'indipendenza effettiva né la potenza.
H3 usa lo score di Tango su coppie local-seen, con margine approvato `m=0,125` come
massima perdita media netta aggregata, con uguale peso agli otto fault. Non è una garanzia
per agente né una soglia validata di adottabilità industriale. Il controllo complessivo
della sequenza è approssimato per la componente Tango, il cui test è asintotico.
[Fonte: S08 `PIANO_STATISTICO.md` §§4–5, 15; L `docs/letteratura.md` §14.2, pin in `FONTI_DELTA_0315.json`]

H3 ha una sensibilità separata a α=0,025, senza sostituire l'esito primario; A2-bis non
è adottato. Il bootstrap appaiato stratificato per classe conserva le sette righe
local-unseen di ogni cluster e usa 10.000 repliche, seed 20260913, per gli intervalli;
non decide H1–H3. Misura variabilità fra run simulati, con copertura approssimata,
non la variabilità delle risposte ripetute del modello. Gli esiti degeneri, incluse
zero coppie discordanti, e le discordanze tra test e intervalli sono riportati come tali.
`[RISULTATO: stime, intervalli, decisioni H1–H3 e stato della sequenza]`.
[Fonte: S08 `PIANO_STATISTICO.md` §§4.3–4.4, 6, 12–15]

Per agente/fault si riportano casi guadagnati (A errato, B-LF corretto), persi (A corretto,
B-LF errato) e saldo guadagnati−persi. Un saldo≤−2 su otto casi è segnalato descrittivamente,
senza convertirlo in un gate o in un test individuale.
[Fonte: S08 `PIANO_STATISTICO.md` §§5, 12–13, 15]

## Controlli e analisi descrittive

I candidati OOD approvati condizionatamente sono F6/F4, con catene F6→F5→F12 e
F4→F11→F5. Candidati, criteri e catene vanno congelati prima della generazione;
secondo B, i controlli tecnici di generabilità, trip e ammissibilità avvengono nella
03.11 dopo il freeze statistico e prima di qualunque chiamata sui test. La verifica
bibliografica entro PHM non qualifica l'eseguibilità tecnica. Ogni sostituto deve
superare le proprie verifiche e i due OOD devono restare distinti; se entrambe le
catene arrivano a F5 o il caso non è risolto dalle regole, si sospende per una decisione
dell'autore. Non si seleziona su prestazioni o separabilità e non si sostituisce dopo le chiamate.
[Fonte: S08 `PIANO_STATISTICO.md` §§8, 16; L `docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md`]

La sonda comprende tre run per ciascuno dei due OOD e tutte le tre condizioni:
sei eventi fisici, una sonda di esistenza, non una caratterizzazione dell'open set.
Si riportano astensione e destinazioni delle attribuzioni errate, separando `Normal`
dai fault in catalogo; la condivisione del circuito fra F4 e F14 resta un limite
esplicito. Le undici scorte tecniche del lotto test sostituiscono run prima delle chiamate,
non aggiungono osservazioni e non coincidono con le catene di sostituzione dei fault.
[Fonte: S08 `PIANO_STATISTICO.md` §§7.4, 8, 14, 16]

L'ablazione local-first valuta B-senza-LF su tutti i local-seen e, sui local-unseen,
sui quattro fault delle coppie D11 approvate `{F1,F2}` e `{F14,F15}`, run sigillati 1–3.
Misura descrittivamente spostamenti di errori, catture del partner e astensioni; non
neutralizza il rischio della politica né entra nella sequenza confermativa.
[Fonte: S08 `PIANO_STATISTICO.md` §§9, 13, 15]

Le baseline comprendono un comparatore numerico a prototipi sulle stesse feature, una rete locale,
FedAvg e la stessa rete addestrata sui dati aggregati. Tutte usano solo sviluppo per il fit e gli
stessi casi di test per la valutazione; non si effettua tuning sul test. `[RISULTATO: valori e
intervalli delle quattro baseline]`.
[Fonte: piano §9.1–§9.3; L `docs/letteratura.md` §14.1–§14.2, McMahan; corpus esterno al branch, pin in `FONTI_DELTA_0315.json`]

Il producer-swap usa una libreria completa per ciascun producer e misura una differenza appaiata su
dati vergini, sotto parità di schema e cap. Conformità, retry, troncamenti, token, ID del modello,
request ID, fingerprint, timestamp e hash della risposta sono registrati. `[RISULTATO: effetto del
producer e tabella di conformità]`.
[Fonte: piano §8.4, §8.7, §8.9]

## Ripetizioni, contabilità e fattibilità

La politica R è approvata. Nel gate su 40 prompt con tre ripetizioni, divergenza significa
cambio della coppia parsata `(abstain, predicted_label)` o della validità: zero prompt
divergenti valutabili consente R=1 con audit, almeno uno attiva R=3, soggetto a fattibilità
e agli altri requisiti di GO. Una tripletta mista per validità diverge; tre invalidi
rendono T6 non valutabile e bloccano il GO tecnico. Le sole differenze nei byte o nel testo
restano forensi. L'assenza di controlli temperatura/seed non attiva R=3 da sola.
[Fonte: S08 `PIANO_STATISTICO.md` §§10–11, 15]

L'audit porta a tre ripetizioni il 10% del nucleo, selezionato deterministicamente e
bilanciato; a R=1 l'analisi primaria usa la prima risposta e la maggioranza sull'audit
è una sensibilità. Non si cambia R a studio iniziato. Dieci canary al giorno sondano
cambiamenti senza prevenirli; sospensioni e reporting seguono la specifica approvata.
L'assenza di divergenze osservate non dimostra determinismo.
[Fonte: S08 `PIANO_STATISTICO.md` §10; `BUDGET_RISORSE_REV10.md`]

A sostituisce il tetto rigido storico di 3.700 con conteggio completo per blocco e
modello effettivo. Il nucleo conta 1.728 chiamate a R=1 e 5.184 a R=3, non il totale.
Il totale parametrico è `N = 2244R + 2k·1[R=1] + 16S + 8U_nonriusato + 10d + G_P + G_A + P_tot + X + Q`:
`k` è il campione audit (circa 173 prompt); `S=Σ(m_F+c_F)` per E5; `U_nonriusato`
conta i fault distinti con FULL da rieseguire; `d` i giorni; `G_P/G_A` le richieste
ulteriori per le librerie; `P_tot` il pilot; `X` le verifiche tecniche ulteriori e `Q`
i retry ammessi fuori pilot. I 2.244 per R comprendono nucleo, misura swap, ablazione
e OOD. E5 conserva R=1; audit già incluso a R=3 e librerie/FULL validamente riusabili
non si ricontano. Ogni invio, anche fallito, conta una volta nel ledger del modello;
ruoli coincidenti si aggregano senza duplicare richieste. Parametri, riusi e calendario
restano da fissare/verificare secondo l'allegato, senza assumere uno scenario numerico.
[Fonte: S08 `PIANO_STATISTICO.md` §7.2; `BUDGET_RISORSE_REV10.md`]

Il pilot segue conformità→eventuale remediation→sonda→gate unico. La riserva è unica,
`8r+t≤15`, con una sola remediation sul prompt producer, da autorizzare sul diff concreto,
e ripetizione di tutti gli otto casi; gli output sostituiti non si riusano. La sonda
ammette ripetizioni solo di triplette complete per trasporto documentato con prova zero token,
preservando le otto richieste di remediation; il gate non ammette retry. Un timeout senza
prova zero token è un guasto tecnico irrisolto. I massimi pianificati 152/160 senza/con
alternativo restano distinti dall'hard stop cumulativo 200, che non finanzia altre chiamate.
[Fonte: S08 `PIANO_STATISTICO.md` §11.1; `BUDGET_RISORSE_REV10.md`]

La fattibilità T5 richiede tempi misurati per blocco/modello/configurazione: in sequenza,
`T=Σ N_blocco,modello × latenza_media_blocco,modello`, con attese e vincoli espliciti,
e `1,20×T≤W` sulla finestra disponibile. Concorrenza e calendario richiedono misure;
la generazione TEP ha un proprio percorso temporale. Se il disegno non è fattibile,
si sospende per una decisione organizzativa dell'autore, senza ridurre automaticamente
il disegno, estendere la finestra o dichiarare NO-GO scientifico. Firma materiale,
freeze statistico, implementazione 03.10, qualificazione, D9 e controlli OOD restano
requisiti distinti; A/B approvate non ne attestano il completamento.
[Fonte: S08 `PIANO_STATISTICO.md` §§7.2, 16; `BUDGET_RISORSE_REV10.md`; S08-consegna `CONSEGNA_REV10.md`]

Q8 designa lo scenario con otto agenti e otto fault; identità del modello, API e controlli di
determinismo sono registrati separatamente nel ramo D9 effettivamente attivato.
[Fonte: piano §8.1, §8.7 e D9]

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

> **VARIANTE D9.1 — Qwen-2.4T.** Attivare soltanto se disponibile e promosso dal pilot entro la data
> prevista. Registrare versione/API e controlli effettivi. Il braccio producer-swap resta nel
> protocollo, ma D9 non nomina il producer alternativo per questo ramo. `[DECISIONE: esito del gate
> e producer alternativo del ramo D9.1]`.
>
> [Fonte: piano §8.4, §8.10 punto 3 e D9 opzione 1]

> **VARIANTE D9.2 — opzione storica Qwen-27B + Terra.** Il piano prevede, solo se
> l'autore attiva questo ramo e dopo pilot positivo, Qwen-27B come producer principale
> e consumer e Terra come producer alternativo nel solo swap. Qwen-27B non è un modello
> «nuovo». Il pilot 03.13 non è avviato; la disponibilità dichiarata del 122B richiede
> una decisione D9 esplicita e non sostituisce automaticamente il candidato storico.
>
> [Fonte: piano D9 opzione 2; H §§4.9, 5]

> **VARIANTE D9.3 — arresto dell'espansione.** Se Qwen-27B fallisce parsing, stabilità o contesto,
> arrestare l'espansione e lasciare all'autore la scelta fra Terra-only e una submission successiva.
> Nell'eventuale Terra-only registrare solo i controlli disponibili e non presupporre uno swap.
>
> [Fonte: piano D9 opzione 3; prompt 03.15]
