# Riverifica indipendente — correzioni R-D9-01 / R-D9-02

Destinazione: stessa finestra `01a0a579-3fd7-7461-8c26-5449bd3d2b7a`,
«Review indipendente D9 — candidato 6a8031b». Il mandato dell'autore richiede
correzioni e riconsegna a questa finestra indipendente; non è una nuova decisione D9.

Prima del lavoro leggere MAINTENANCE nella versione candidata e skill
fot-tep-harness-lessons con i riferimenti pertinenti. Review del codice in sola
lettura: scrivere verbale/prove in una sede separata, senza modificare la candidata.

- Worktree: `/Users/luker/fot-tep-harness-d9-correzioni`.
- Branch: `codex/studio2-harness-d9-correzioni`.
- **Tecnico:** `16c98f39c044d812458705234b1a3f8ee4940b34`.
- **Tree:** `1dd8f84d991190d9d8316e6c56899bc115232716`.
- Manifest: `studio2/fase03/harness/d9_corrections/CANDIDATO_CORREZIONI_D9.json`; SHA-256 `a2fbabcaa997831446c4c2775d62fa6fc2078229a4c71187337be30a9ae7e4e1`,
  1062 membri. Il successore documentale non cambia il tecnico.
- Respinto preservato: `6a8031b25aa1208047d79cc7f030bf9cf7841e67`.
- Originale verbale/prove: `d9_corrections/non_ok_6a8031b/` sotto harness;
  acquisizione e SHA in ACQUISIZIONE_NON_OK.json. Anche la copia originale della
  review è invariata. L'archivio candidato da244MB resta recuperabile localmente
  nei percorsi dichiarati; non è committato o pubblicato, le altre prove sì.

Verificare branch, HEAD/tree, remoto effettivo, writer e byte prima delle prove.
Leggere CONTRATTO_CORREZIONI_D9.md, REPORT_CORREZIONI_D9.md, consegna JSON e
contratto D9 originario. Conservare il NON OK, gli OK D04 e i pending storici
senza trasferirli al nuovo tecnico.

Verificare R-D9-01: sentinel con spazi/tab/NBSP e case diverso, positivi reali,
rifiuto prima di effetti. Verificare R-D9-02 nel controllo comune del binding:
file R4 e chat distinti, pin del ruolo attivo, assenza/alterazione, nuova riserva,
riuso/rebind chiuso, restart, successo→nuovo guasto e percorso reale di trasporto.
Il nuovo tokenizer_snapshot nel binding è richiesto; non c'è backfill dei vecchi
binding D9, né migrazione o reset. Il template inline già pinnato resta legittimo.
I file sono ricontrollati al confine; non si rivendica un lock globale sul filesystem.

Risultati preparatore: mirati156/156, discovery191/191; stesso test finale correzioni
11 metodi sul respinto con32 assertion fallite/0errori e sul corretto11/11;
U01–U08 originali byte-identici:8 metodi,3fallimenti sul respinto,8/8 sul corretto;
regressione trasporto nuova con SDK fittizio:3 metodi,2fallimenti sul respinto,3/3
sul corretto. Non sommare suite sovrapposte o subtest. I log intermedi falliti e
le revisioni dei test restano disponibili; valutare i **byte finali identici**.
Il rosso è eseguito su08670fb, con differenza verso6a8031b verificata composta
soltanto da5 documenti: codice tecnico identico. Riferimenti in PRESERVATION.json.

Rieseguire le prove finali e le suite complete mirata/discovery sui byte candidati,
con fixture sacrificabili e SDK fittizi. I comandi sono nei record *_command.json
in results; aggiunto test_d9_corrections alla stessa suite mirata già nota.
Non eseguire run_full_suites.py alla lettera: contiene il percorso/output del
preparatore. Usare i medesimi comandi nella propria copia isolata. Per U01–U08
usare FOT_D9_TARGET e PROBE_OUTPUT assoluto in una nuova destinazione: non
sovrascrivere le fixture della review. La nuova prova transport_boundary_regression
usa FOT_D9_TARGET e TRANSPORT_RESULTS. Conservare comandi, log e impronte.

Guardiano35test/14fallimenti storici/1skip/0errori, NON PASS invariato. Le segnalazioni
di whitespace nei log grezzi e nelle fixture deliberatamente corrotte sono conservate;
diff check di codice/Markdown passa. Non correggere quelle prove per rendere verde
un controllo cosmetico. Verificare la conservazione e distinguere integrità locale,
provenienza e recuperabilità remota non ancora pubblicata.

Nessun contatto con servizi, SSH, endpoint, inferenza, sonda, pilot o ledger
scientifico. Ruoli già approvati immutati; temperature122B omessa, ordine1a e
metadati/qualifiche reali pendenti, S4/3 non riconciliato. Nessun GO/capienza/T5,
nuovo braccio, aggiornamento condiviso, push, merge o tag.

Consegna un nuovo verbale circoscritto (OK limitato oppure NON OK con rilievi),
identità/indipendenza e limiti dichiarati, tecnico/tree, prove e manifest recuperabili.
Non richiedere di nuovo i ruoli e non riaprire una campagna storica senza difetto concreto.
