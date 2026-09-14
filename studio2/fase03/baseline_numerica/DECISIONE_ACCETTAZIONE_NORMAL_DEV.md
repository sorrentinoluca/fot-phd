# Decisione di accettazione — `normal_dev`

**Provenienza della decisione:** messaggio dell'autore nella conversazione corrente: «3.9 - OK».
Questa registrazione non attribuisce una firma e non retrodata la decisione. Data di registrazione:
2026-09-14.

## Separazione degli esiti

Il lotto conserva due esiti distinti:

- **PASS tecnico:** `AUDIT_NORMAL_DEV.json` attesta 40/40 run e 320/320 finestre, identità
  piano–manifest–workbook, griglia, finitezza e impronte;
- **deviazioni procedurali accettate:** l'autore accetta il riuso del pathname
  `normal_dev_001` dopo il tentativo pre-start e considera sufficiente la tracciabilità disponibile
  del comando riuscito e del `MATLABPATH`, mantenendo il limite esplicito che log e manifest non
  provano da soli il checkout Git e il comando effettivamente avviato.

L'accettazione delle deviazioni non le converte in conformità e non modifica i log, il recovery o
la storia audit. I file restano preservati nel candidato di conservazione.

## Controllo specifico del warning `Variable Time Delay`

Il controllo è documentato in `SIMULATOR_WARNING_CHECK.json` ed è stato svolto senza simulazioni.
Il modello ha SHA-256
`c58826748edd306b723da2f0199a0fb2dc193a51dc5c28dbde8ac821e39dfafd`, uguale al freeze di Fase
02 e ai 40 manifest. Il blocco è `VariableTransportDelay` configurato come `Variable time delay`,
con `MaximumDelay=20`, buffer iniziale di 1.024 punti e `FixedBuffer=off`. La simulazione è in
modalità `normal`, solver variable-step `ode45`. Il generatore qualificato, SHA-256
`923d657608f5bbf30869c8cdf2772dd5cacd2a98b4ef62dc85540dc812eda837`, non sovrascrive modalità
o parametri del blocco; imposta soltanto solver, stop function e stop time. Non è stata invocata
code generation.

La documentazione MathWorks del [Variable Transport Delay](https://www.mathworks.com/help/simulink/slref/variabletransportdelay.html)
specifica che il blocco conserva coppie tempo/ingresso e, con buffer non fisso, alloca memoria
aggiuntiva quando l'allocazione iniziale non basta. L'extrapolazione lineare associata a perdita di
storia riguarda invece il buffer fisso pieno; ERT/GRT usa comunque un buffer fisso. La pagina
[Variable Time Delay](https://www.mathworks.com/help/simulink/slref/variabletimedelay.html)
conferma che i due nomi di libreria sono configurazioni dello stesso blocco.

Il log riuscito contiene 40 riallocazioni a 63.488/64.512 punti, una per run, e nessun errore,
trip, clipping, buffer overwrite, messaggio di extrapolazione o approssimazione. Gli altri messaggi
sono un warning di accesso alla directory MATLAB e due warning Java/X11. Ne segue una conclusione
circoscritta: il warning è **accettabile per questo lotto in simulazione normal mode**, perché
segnala riallocazione dinamica e costo di memoria, non perdita di storia. Non è un'accettazione per
code generation o target embedded, né una prova generale sul modello. L'interpolazione ordinaria
del blocco continuo resta parte del suo comportamento documentato, non un'approssimazione causata
dal warning.

Non serve un replay per questa conclusione circoscritta: il tipo di buffer, la modalità e l'assenza
di segnali di perdita/errore sono verificabili staticamente. Nessun parametro del simulatore
qualificato è stato modificato per eliminare l'avviso.

## Decisione operativa

Il lotto è accettato come input di sviluppo della 03.9, soggetto alle dipendenze U3/R2 già fissate.
La nuova destinazione del riuso è
`studio2/fase03/baseline_numerica/evidence/normal_dev_002/`; usa l'estrattore 03.6 verificato per
hash e non sostituisce né altera la release fault `studio2-fase03-evidence-v2`.

Questa decisione non dichiara pubblicazione, integrazione in `main`, freeze efficace o chiusura
della Fase 03.
