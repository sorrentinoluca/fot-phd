# Integrazioni seriali e allineamenti predisposti — 03.8

Data: 2026-09-14. **Preparazione locale, integrazioni non eseguite**.
Questo documento definisce il delta; non è una nuova fonte del disegno.
Fonte delle regole: piano statistico, con le sole nuove decisioni A/B se approvate.

> **Aggiornamento procedurale 2026-09-15.** L'autore ha stabilito che per 03.8
> l'approvazione documentata è sufficiente e non è richiesta una firma materiale.
> La [decisione corrente](DECISIONE_AUTORE_APPROVAZIONE_DOCUMENTATA_03_8_2026-09-15.md)
> sostituisce il solo residuo procedurale «firma» dopo verifica indipendente del
> nuovo delta. Piano rev.10, pacchetto firma e relativi verbali restano
> byte-identici; i record anteriori che indicano la firma come pending conservano
> il proprio significato storico.

## 1. Acquisizione del candidato bibliografico verificato

Sorgente: `/Users/luker/fot-tep-letteratura-fase03`, branch
`codex/studio2-letteratura-fase03`, HEAD
`a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155`. Al controllo: quattro file tracciati
modificati, 17 file nuovi non ignorati, due PNG ignorati; candidato non committato.
Snapshot separato: `/Users/luker/fot-tep-verifica-letteratura-fase03`, **senza .git**.
Verbale: `docs/lit_review/VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md` nello snapshot,
SHA-256 `551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`.

Identità ricontrollata: **23/23 file, 6.407.129 byte** corrispondono alla tabella
del verbale. Inventario completo e controlli di provenienza in
[ACQUISIZIONE_LETTERATURA_03_8.json](ACQUISIZIONE_LETTERATURA_03_8.json).
Questa è una verifica di identità, non una nuova review scientifica della letteratura.

Consegna pronta per la finestra Letteratura (da trasmettere dall'autore o in una
sessione coordinata; nessun messaggio inviato da questa finestra):

> Conservare il candidato alle 23 impronte indicate. Verificare nuovamente HEAD,
> stato e hash prima del commit; concordare una finestra esclusiva. Committare
> selettivamente i 21 file non ignorati del candidato e preservare byte-identico
> il verbale OK in un commit separato. Non importare uno snapshot intero di docs/.
> Conservare i due PNG indicati nell'inventario in un archivio/copia recuperabile
> con percorso e SHA-256 verificati; non forzare indiscriminatamente *_images/ in Git.
> Il percorso sorgente e lo snapshot sono le copie locali oggi verificate, non
> una pubblicazione durevole. Registrare il target di conservazione prima della
> consegna finale. Comunicare commit esatti, impronte e modifiche intervenute.

I quattro delta tracciati sono `docs/letteratura.md`, `docs/letteratura.html`,
`docs/paper/FoT_TEP_paper_blueprint.html`, `papers/README.md`; i primi due vanno
nello stesso commit. Integrare poi questi commit in modo seriale nel ramo
destinato a main, con controllo dei conflitti e parità MD/HTML sul contenuto.
Se il target ha nuove modifiche, applicare gli hunk bibliografici al contenuto
corrente e riverificare il delta: non ripristinare i quattro file dalla vecchia base.
Il verbale OK vale per le impronte originarie, non automaticamente per conflitti risolti.

F6 è bibliograficamente ammissibile entro PHM; nessuna prova tecnica OOD è
prodotta da questa integrazione. Preservare registro, H={F3,F9,F15}, D1 e addendum
F9–SPE (5,6% fonte contro 6,6% registro storico), senza correggere il registro congelato.

## 2. Delta del piano generale

Target: `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`, nel ramo di integrazione
esclusivo dopo la consegna Letteratura. Le localizzazioni si riferiscono alla
base statistica `0f1a9ba`; cercare per sezione nel target aggiornato.

| Punto | Testo sostitutivo / intervento concreto |
| --- | --- |
| §0.1, decisione 2 | «**8 run per fault confermati**: 64 cluster fault e 8 Normal primari; +638 prima del retry e +702 (+24,6%) fra le stime arrotondate storiche di §8.8. Approvazione documentata sufficiente; review del nuovo delta e congelamento pending.» |
| D2, titolo e primi due paragrafi | «**D2 — 8 run per fault confermati.** Il disegno comprende 64 run fault +8 Normal, 72 primari; 6 OOD separati e 11 scorte tecniche, 89 run complessivi del lotto con due OOD selezionati. Le scorte non aggiungono osservazioni. Il confronto 6/8 e la risoluzione restano documentati nel piano statistico §7. I totali storici sono ~2.853/~3.555 con retry, differenza +702 (+24,6%), e ~2.594/~3.232 pre-retry, differenza +638. Il calendario richiede verifica della generazione e dei tempi API, non segue dalla sola data D9.» |
| §8.8 introduzione | D2 è confermata a 8; la colonna 6 è confronto storico, non opzione ancora aperta; vecchie stime arrotondate distinte dal ledger completo |
| §8.8 frase «+590, +24%» | sostituire con «+702, +24,6% con retry; +638 prima del retry, differenze tra stime arrotondate» |
| D2, §11 T5/O2, §13 domanda 14 | correggere vecchi ~2.450/~3.040 e 3.500; rinviare a budget e regola vigente sotto, senza sostituire numeri di sezioni storiche sui disegni eliminati |
| §8.7 apertura | nucleo del disegno corrente 1.728 a R=1 /5.184 a R=3; eliminare estrapolazione di durata non misurata e 1.296 come valore corrente D2=8 |
| §8.4 tabella | distinguere misura swap 224×R da libreria alternativa: 8 richieste per 16 insight, se non già riusata; ~20 è vecchia stima con margine, non richieste del disegno |
| §8.8 tabella risorse | usare i blocchi e la formula di BUDGET_RISORSE_03_8.md, con parametri E5/riusi/giorni/X/Q e ripartizione per modello ancora pending |
| §0.1, decisioni 3/4/5/11 | OOD F6/F4 confermati condizionatamente, D11 coppie confermate, m/alpha/gerarchia confermati, politica conservativa non adottata; rimando alle approvazioni storiche e ai residui 03.8, senza marcarli frozen |
| §11 T3/T4/T6/T9/T11 | propagare letteralmente soglie e semantica dal piano statistico §11; conformità 16 insight/8 richieste e T6 non valutabile restano distinti |

**Budget secondo la sola decisione effettivamente approvata:** finché A è pending
o respinta, mantenere 3.700 come tetto vigente e ramo R3 sospeso per decisione
organizzativa; correggere soltanto il refuso 3.500. Se A è approvata, sostituire
nei punti correnti §8.8/D2/T5/O2/§13 il tetto con conteggio completo e compatibilità
temporale misurata +20%, sospensione organizzativa se non fattibile. Conservare
3.700 nelle note storiche con provenienza; non fare sostituzioni globali.

## 3. Delta APERTURA e dipendenze

Target `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`:

| Punto | Formulazione concreta da recepire |
| --- | --- |
| 03.8 | «D2=8 e D11 confermati; OOD F6/F4 condizionati; politica R confermata. Approvazione documentata sufficiente, senza firma materiale; review del nuovo delta e congelamento pending.» |
| 03.11, numerosità | «72 run primari (64 fault +8 Normal) +6 OOD +11 scorte tecniche =89 run del lotto, a candidati OOD selezionati; stream/seed disgiunti, identificativi sigillati, nessuna osservazione aggiunta dalle scorte.» |
| 03.13, catena | «input di sviluppo e schema congelati → conformità producer (8 richieste/16 insight) → eventuale unica remediation autorizzata sul diff → prompt definitivi e capienza offline → sonda budget 3–9 → freeze configurazione → unico gate 40×3 → T3/T4/T6/T11 e latenza → verifica organizzativa T5 e altri bloccanti → decisione GO/NO-GO. Conformità alternativa solo con D9 configurata, quota 8 separata.» |
| 03.13, risorse | massimi 152/160 con riserva inclusa, hard stop 200; durata nuova API pending; distinguere evidenza vecchio 27B FP8 e nuovo alias non identificato |
| §5, frase «tutto il resto indipendente dal pilot» | «La generazione dei test 03.11 non è input del pilot di sviluppo. Le regole statistiche di 03.8, incluse politica R, soglie, ordine e riserva, devono essere recepite/verificate nella 03.10 prima del pilot; il congelamento statistico segue i propri requisiti. 03.6/03.7/03.12, identità/configurazione e capienza restano prerequisiti del pilot.» |
| 7.4 (opzione non adottata) | sostituire la vecchia forchetta di costo con rinvio al ledger corrente senza cambiare lo stato dell'opzione |

Se B è approvata: 03.8 congela criteri/candidati/catene **prima** del primo run;
03.11 controlla generabilità/trip/ammissibilità **prima** delle chiamate, registra
esiti/sostituzioni senza scegliere su prestazioni. Se B non è approvata, il ciclo
di dipendenze del §16 rev. 9 resta un blocco dichiarato: non omettere la verifica
tecnica per far sembrare congelabile il piano.

La sequenza proposta con B non è circolare: decisioni A/B → candidato nuovo →
verifica indipendente → approvazione documentata e allineamenti delle regole → documentazione e
integrazione seriali → manifest/tag del disegno → 03.11 controlli tecnici →
chiamate sui test dopo gli altri GO. Il pilot di sviluppo ha la propria catena
03.6/03.7/03.12→03.10 conforme→03.13 e non richiede risultati dei test OOD.
Restano i requisiti operativi prima del pilot: separarli dal freeze statistico
non autorizza eliminarli. Nessuna attività su 03.5.

## 4. Documentazione e operazioni esterne successive

Dopo l'OK indipendente del candidato nuovo, usare Documentazione_LLM per la
coppia `docs/fot_walkthrough_conversazione_studio2.md`/`.html`, sottosezione
della Fase 03 dedicata alla 03.8, senza cambiare le sezioni delle altre finestre.
Struttura: riassunto, dettaglio, connessione alla letteratura, limiti/critiche,
artefatti e riproducibilità. Numeri dai file manifestati, stato delle condizioni
esplicito, **Fase 03 ancora aperta**. La sintesi divulgativa non richiede una
voce per questa preparazione interna. Nessun walkthrough aggiornato ora.

Ordine seriale: commit Letteratura + verbale → integrazione bibliografica
verificata → recepimento A/B e allineamenti → nuova verifica del candidato esatto
→ documentazione in coppia → controlli/commit finali → presentazione dei target
esterni all'autore. Se la review precede un'integrazione, riverificare il delta
che quella integrazione introduce nel candidato finale.

Target futuri da presentare **prima** di agire: repository remoto `origin`
(`https://github.com/sorrentinoluca/fot-phd.git`), ramo di integrazione esatto e
`refs/heads/main`; tag previsto
`refs/tags/studio2-fase03-piano-statistico-frozen-001` sul commit finale verificato.
Il SHA del commit finale è pending; non si propone oggi un push/merge/tag eseguibile.
Per gli asset ignorati concordare sede di conservazione concreta prima della
pubblicazione. La raggiungibilità locale non è raggiungibilità in origin/main.
Decisione documentata dell'autore, verifica nuova, condizioni approvate e
raggiungibilità prevista devono essere provate prima del tag; il manifest non
contiene la propria impronta.
