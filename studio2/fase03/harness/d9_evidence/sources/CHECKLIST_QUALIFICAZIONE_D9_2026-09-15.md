# Checklist preparatoria della futura qualificazione D9

**OFFLINE — NESSUNA PROVA DEL SERVIZIO ESEGUITA O AUTORIZZATA QUI**

15 settembre 2026, Europe/Rome. Tutte le caselle descrivono attività future; le verifiche documentali svolte in questa consegna sono nel rapporto dell'[inventario](INVENTARIO_SERVIZI_D9_2026-09-15.md), non segnano queste caselle come completate.

Fonti: record D9 D, contratto R4C/R4, piano statistico rev.10 PS §§10–11, budget B, delta DH; percorsi, commit e SHA-256 nel §7 dell'inventario. H10 è soltanto il contratto del candidato harness in review: non se ne importa codice, non se ne certifica l'esecuzione e non si assume che le sue fixture attestino il servizio reale. Il futuro recepimento deve verificare i pin allora approvati, senza applicare automaticamente una copia di lavoro parallela.

## 1. Ruoli e confini già fissati

| Servizio | Perimetro della qualificazione futura | Esclusioni conseguenti ai ruoli |
| --- | --- | --- |
| 122B | P: produzione conforme; C: consumo diagnostico e stadi di sonda/gate previsti | Nessuna superiorità dedotta dalla dimensione o dal nome. |
| 27B | P_alt: produzione della **libreria completa di 16 insight**, parità strutturale e provenienza | Nessun nuovo consumer sperimentale, fallback, gate diagnostico 40×3, audit/canary consumer dedicato al 27B. |
| Swap | C resta 122B, sui medesimi casi e condizioni previsti dal disegno; cambia la libreria producer | Nessun cambio simultaneo di consumer, casi, schema o cap. |
| Terra | Riferimento storico descrittivo interno, separato dalle stime del nuovo studio | Nessuna nuova produzione, chiamata o qualifica Terra. |

Due server non dimostrano modelli indipendenti né condizioni comparabili. La differenza producer-swap riguarda le librerie ottenute dalle configurazioni documentate: modello, quantizzazione, serving e sampling possono restare confondenti. Non presentare l'esito come effetto isolato della dimensione dei pesi. La presenza del medesimo 122B come P e C va documentata esplicitamente.

## 2. Dati da acquisire e controlli offline — nessun trasporto ai servizi

- [ ] Acquisire le attestazioni M01–M13 per il 122B e le riconferme del 27B, distinguendo data di dichiarazione, data del record e data di lettura. Registrare anche i campi non disponibili, senza sostituirli con valori inferiti.
- [ ] Collegare ogni ruolo al backend attestato: repository/revisione pesi, quantizzazione/calcolo, alias e mapping, versione/build/configurazione serving e parser. Il nome restituito dall'API sarà solo un elemento del confronto, non una prova autonoma dell'identità dei pesi.
- [ ] Acquisire e improntare tokenizer e template effettivi per ciascun servizio; verificare la serializzazione cui si riferisce ogni hash, gli override e i token aggiunti. Documentare posizione recuperabile dei file, non soltanto le impronte.
- [ ] Mantenere il **contatore canonico R4** dei campi insight (tokenizer 27B pinnato, `add_special_tokens=False`, senza template) distinto dal **conteggio della richiesta completa** del servizio effettivo. Quest'ultimo include chat template, special token, istruzioni/overhead e budget output/reasoning. Nessun fallback silenzioso al conteggio del solo testo.
- [ ] Verificare offline il builder producer con gli input development e il contratto congelati, poi la capienza del prompt completo di P e P_alt con i rispettivi tokenizer/template e limiti attestati. Una libreria già conforme non è prerequisito della chiamata che deve produrla; la libreria risultante valida serve successivamente per costruire i prompt consumer reali.
- [ ] Per C 122B, dopo la libreria valida, ricostruire i prompt diagnostici development previsti con 14 peer insight per destinatario, escludendo i propri 2; conservare prompt e hash. Verificare input completo+budget output+margine nei limiti effettivi. 131072/16384 dichiarati non bastano da soli.
- [ ] Nel recepimento operativo 122B verificare sui byte della richiesta che `temperature` sia **assente**: non null, stringa vuota o 0.6. Registrare separatamente default server 0,6 dichiarato e altri parametri attestati. Non trasferire seed 20260829, T=0 o budget storici 27B per eredità.
- [ ] Preparare validazione distinta dell'output producer e consumer, con conservazione raw e campi reasoning separati. Per P_alt verificare schema insight, campi fissi, identificatori, cap e leakage; non imporgli risposte diagnostiche o astensioni da consumer.
- [ ] Predisporre logging di ruolo/modello, intenti, request/response ID, configurazione/prompt, usage se esposto, finish reason, fingerprint, errori, durata misurata e imputazione contabile. Campi assenti/null restano assenti/null, non zeri. Un fingerprint del processo non è quello dell'API né la revisione pesi.
- [ ] Riconciliare ledger e consumo storico prima di futuri invii, compresa la sonda S (4 richieste riportate, 3 inferenze completate). Non dedurre dal record di avvio “zero POST” che l'intera storia sia a zero; non aggiungere due volte una spesa già presente nel ledger. Non migrare o azzerare ledger del candidato in review con questo documento.

La verifica R4 già documentata resta valida nel suo perimetro contrattuale e nelle sue impronte; non sostituisce questi controlli di capienza né dimostra che il tokenizer del servizio corrente coincida con quello del test storico.

## 3. Comportamenti da verificare sul servizio — soltanto con autorizzazione futura

Questa sezione elenca osservabili, **non un nuovo stadio di test**. Prima di ogni eventuale chiamata, la finestra competente deve assegnarla a uno stadio già previsto, con input, quota e autorizzazione. Un controllo non coperto non si esegue “gratis” o “di servizio”: resta pendente fino a una decisione esplicita, senza usare lo spazio sotto l'hard stop come riserva libera.

| Osservabile | Dove raccoglierlo nel flusso già previsto | Criterio di documentazione |
| --- | --- | --- |
| Identità esposta e binding | Richieste autorizzate P 122B, P_alt 27B e C 122B | Confronto con manifest attestato; eventuali differenze o cambio backend sospendono l'uso, senza fallback automatico. L'API non certifica da sola i file pesi. |
| Produzione insight | Conformità producer principale/alternativo | Raw conservati, 16 insight distinti e completi per libreria, campi fissi e cap R4, nessun leakage; template e parametri improntati. |
| Formato e thinking | Chiamate producer per contratto insight; sonda/gate C per schema diagnostico | Parser sul campo corretto, reasoning separato, budget realmente applicato; missing content/usage o comportamento non attestato registrati come tali. |
| Capienza/troncamenti | Conformità P/P_alt e sonda/gate C, sui rispettivi input ammessi | Confronto token offline/usage ove possibile, finish reason, completezza input/output, segni di tagli silenziosi. Non equiparare `stop` a prova assoluta di input integro. Nessun test oltre limite aggiuntivo qui. |
| Stabilità diagnostica | **Solo gate C 122B** e audit/canary già previsti | Unità e firma semantica PS; nessun pannello diagnostico aggiunto per 27B. La stabilità dei producer si documenta con identità/configurazione e output previsti, senza repliche extra. |
| Latenza e disponibilità | Ogni richiesta autorizzata, distinta per ruolo/blocco, anche quando P=C | Misure end-to-end e attese, carico documentato, conteggi per blocco/modello; latenze storiche 27B consumer non sostituiscono quelle di P_alt. |
| Errori/zero token | Errori eventualmente incontrati nel flusso autorizzato | Conservare intento ed evidenza del gestore correlata a richiesta; timeout, assenza response o completion_tokens=0 da soli non provano tutti i token zero e mancata generazione. Nessuna provocazione di errori o retry automatico. |
| Aggiornamento backend | Identità/config durante l'attività e canary C previsti | Applicare le sospensioni del protocollo; non attribuire automaticamente al modello differenze dovute a routing/carico/configurazione. |

## 4. Stadi già previsti e quote da preservare

La fonte delle quote è PS/B/DH; i ruoli applicabili sono quelli del record D, non l'inventario superato nei vecchi file. Questa tabella non approva l'avvio né inventa un budget producer nuovo.

| Stadio | Modello/ruolo | Controllo e contabilità già previsti |
| --- | --- | --- |
| Conformità principale | 122B/P | 8 richieste per 16 insight; output/errori conservati, contratto vigente invariato. |
| Remediation eventuale, prima di sonda/gate | 122B/P | Una sola ripetizione completa degli 8 casi, solo dopo diagnosi ammessa e autorizzazione scritta sul diff concreto del prompt; schema/campi fissi/cap/validatore non cambiano. Output iniziali esclusi dalla libreria successiva. Nessuna seconda riserva per P_alt. |
| Sonda budget | 122B/C | 3/6/9 richieste, triplette complete A/B-LF/E-LF; procedura di selezione da recepire prima delle chiamate; budget scelto dalla sonda e congelato prima del gate. Vecchi candidati thinking 2048/3072/4096 non diventano parametri 122B approvati. |
| Gate tecnico unico | 122B/C | 40 prompt×3=120 richieste, configurazione/prompt/template improntati; nessun retry gate. |
| Conformità alternativa | 27B/P_alt | 8 richieste accantonate per libreria completa 16; collocazione nel pilot (`a=1`) o differimento da esplicitare nel recepimento competente. Nessuna trasformazione in un secondo gate consumer. Riportare una sola volta le chiamate se differite. |
| Produzione/swap, dopo prerequisiti e GO | P 122B, P_alt 27B; C 122B invariato | Riutilizzo librerie solo se consentito e tracciato; stessi casi previsti, parità schema/cap e campi fissi; nessun nuovo braccio. |
| Audit e canary | C 122B | Audit 10% del nucleo e 10 canary/giorno secondo PS/B; selezione e contabilizzazione nel calendario. R=3 non moltiplica i canary in 30/giorno né le librerie producer in tre. |

Contabilità pilot: `P_tot = 128 + b + 8r + 8a + t`, con `b` pari a 3/6/9, `r,a` pari a 0/1 e `8r+t≤15`. Massimi pianificati **152 senza /160 con alternativo**; **200 è hard stop cumulativo**, non autorizza le 40 richieste di differenza. Le 8 dell'alternativo non finanziano retry. Le quote non si azzerano cambiando producer, alias, directory o riavviando.

Retry trasporto soltanto secondo PS/B/DH e prova zero token: nella sonda per triplette complete, quota 8 remediation sempre protetta, quindi verificare `trasporto_già_consumato+3≤7`. Al massimo due triplette ripetute se la quota è integra; nessun retry gate. Timeout senza prova richiesta è guasto irrisolto, non difetto di prompt e non autorizzazione di reinvio. La riconciliazione esterna documentata dal candidato H10 è futura, non una garanzia fornita oggi dai servizi.

Sul gate C 122B mantenere distinti:

- **T3:** almeno 114/120 valide al primo tentativo e copertura della parsabilità di `abstain=true, predicted_label=null` per ciascuna condizione secondo PS §11; eventuale prompt di prova dedicato già previsto va collocato e contabilizzato esplicitamente, senza aggiunte arbitrarie. Invalidità di trasporto nel denominatore.
- **T4:** zero troncamenti sulle 120 richieste al budget scelto.
- **T6:** divergenza della coppia parsata `(abstain, predicted_label)` o della validità, non dei soli byte/reasoning/finish reason. 0 prompt divergenti su 40 valutabili → R=1; almeno 1 → R=3, pendente fattibilità. Un gruppo di tre invalidi rende T6 non valutabile e impedisce GO. Assenza di controlli temperatura/seed da sola non impone R=3.
- **T5 e altri prerequisiti:** conteggi completi per blocco/modello, latenza effettiva più attese e finestra disponibile W, con `1,20×T≤W`. R=3 richiede fattibilità; non autorizza una riduzione automatica del disegno, un cambio di consumer o un'estensione di calendario. T11 e A/B/FAR/U3 rimangono quelli già fissati.

## 5. Passaggi separati prima dell'esecuzione

- [ ] Acquisizione metadati tecnici e riconferme: completare M01–M14 quanto al perimetro attestabile; assenze motivate restano visibili.
- [ ] Recepimento seriale nelle finestre 03.8/03.10/03.15, con verifica dei riferimenti correnti. La review harness non è sostituita da questa checklist.
- [ ] Firma materiale 03.8 e ordine label 1a nelle rispettive sedi, senza dedurli da D9.
- [ ] Scelta/approvazione dei dettagli operativi ancora aperti: configurazioni effettive e loro pin, finestra/calendario e collocazione contabile dell'alternativo. Un hash da acquisire è un dato tecnico, non una domanda all'autore sui ruoli.
- [ ] Autorizzazione esplicita alle chiamate e verifica dei prerequisiti degli stadi; applicazione del ledger e dei limiti prima dell'invio. Nessun invio è autorizzato dal presente documento.

Al termine della futura qualificazione, produrre evidenze per **ruolo e configurazione**, con raw recuperabili, hash, consumo e limiti osservati. Una verifica documentale, un PASS su fixture o una dichiarazione “operativo” non vanno registrati come GO del nuovo studio.
