# Decisioni dell'autore 7.3 rev3 — chiusura dei segnaposto

Data: 2026-09-17, sera. Questo record aggiunge le decisioni seguenti senza modificare le
decisioni precedenti, il piano statistico 03.8, il candidato eseguibile 7.4 o i relativi
artefatti.

## D6 — verifiche tecniche pianificate

`X = 0`. Lo stage `technical_verification` resta definito con quota zero, così non può essere
legato né consumato. Una futura verifica tecnica richiede una revisione dichiarata del
protocollo: il margine temporale e la quota retry non la autorizzano implicitamente.

Motivazione: nessuna verifica tecnica è oggi identificata prima dei dati; mantenerne una
riserva numerica senza elenco consentirebbe usi discrezionali incompatibili con il freeze.

## D7 — retry tecnici

Quota cumulativa separata: **400** tentativi, solo per richieste con prova durevole e
request-bound di zero token generati, ragionamento incluso. Le attese sono 30, 60, 120 e 240
secondi, poi crescono fino al tetto di 15 minuti per attesa. Il contatore deriva dal ledger e non da
stato volatile. Dopo **5 fallimenti tecnici consecutivi per servizio** la campagna va in STOP;
il quinto fallimento impedisce il sesto invio automatico.

Motivazione: nel pilot i fallimenti pre-generazione sono stati 8 su 156 richieste, 5,13%; su
6.802 chiamate base si attendono circa 349 eventi allo stesso tasso. Quota 400 aggiunge circa
il 15% senza confondere retry, ripetizioni scientifiche o nuove verifiche. Timeout o consumo
incerto non sono prova di zero token e impongono sospensione e riconciliazione.

## D8 — barriera canary giornaliera

Ogni giorno civile Europe/Rome con chiamate scientifiche richiede prima un canary PASS dello
stesso giorno. Nessun lotto parte in un giorno senza quel PASS. Restano il massimo di sette
giorni, lo STOP immediato per cambio d'identità e lo STOP al secondo giorno distinto marcato.

Motivazione: una verifica soltanto iniziale non protegge dalla deriva fra giorni; la barriera
giornaliera rende preventivo il controllo senza reinterpretare ex post i risultati.

## D9 — massimo e fattibilità

Massimo: **7.202 = 6.732 scientifiche + 70 canary + 0 verifiche tecniche + 400 retry**.
Sulle latenze pilot 26,2086 s medie e 36,6609 s p95, il tempo sequenziale è 52,4318 h e
73,3422 h; con margine 20% è **62,9181 h** e **88,0106 h**, entrambi inferiori a 168 h.
Il margine temporale non crea quota.

## D10 — materializzazione dopo il tag

Configurazione eseguibile del target finale, contratto di generazione e dieci prompt canary
byte-identici al pilot sono prerequisiti di **7.4-MAT**, da produrre e autenticare dopo il tag.
Sono prerequisiti operativi della materializzazione, non difetti o segnaposto del protocollo.

## D11 — esito H3 e limite

La verifica sintetica ha completato 1.596 scenari, con 24 stress ICC non fattibili e zero
errori numerici. I 108/108 punti decisionali al bordo e ICC=0 hanno `phat <= 0,055`; massimo
0,05128. Aggiornamento del 2026-09-18: la review indipendente finale
`VERIFICA_FINALE_PROTOCOLLO_RUNNER_H3.md` ha concluso **TANGO MANTENUTO**. Gli stress ICC sono
descrittivi: massimo ICC testato con tutti i livelli <=0,055 pari a 0 per Tango H3 e 0,20 per
Hoeffding H3 e H1/H2. La verifica è locale a H3; livello e FWER completo restano approssimati,
non garantiti. Non si cambia procedura.

Motivazione: H3 dipende dall'indipendenza fra run ed è sensibile anche a correlazione entro
fault piccola; H1/H2 risultano più robusti fino a ICC moderato nella griglia, senza che lo
stress stimi la dipendenza reale del servizio.
