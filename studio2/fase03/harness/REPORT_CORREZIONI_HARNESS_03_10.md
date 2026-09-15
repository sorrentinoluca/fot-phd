> **Documento storico del candidato 0c8157f, respinto NON OK.** Il secondo verbale smentisce la sostituzione normativa di N48 e apre C01–C03. Il delta corrente è descritto nella [matrice C01–C03](MATRICE_R01_R10_C01_C03.md); la nuova consegna documentale è un successore separato.

# Report di implementazione — correzioni harness offline 03.10

**Candidato locale consegnato per una nuova verifica indipendente. Il NON OK originario non è dichiarato superato.**

15 settembre 2026. Esecutore: Codex, questa finestra di implementazione, agente /root.
Nessun sottoagente e nessun uso della finestra del revisore. Il modello esatto e l’effort
non vengono dedotti dal nome del prodotto: non si attribuiscono metadati runtime non
acquisiti in questa consegna. Profilo: implementativo, test offline con stub.

## 1. Identità, catena e isolamento

| Elemento | Identità |
| --- | --- |
| Repository principale | /Users/luker/fot-tep; HEAD 819b12e97fb94d501032655ec2f226139e6c5ca5, branch codex/studio2-soglie-normal; non tracciati preesistenti preservati |
| Remoto effettivo | https://github.com/sorrentinoluca/fot-phd.git; main verificato prima delle scritture e dopo le prove con git ls-remote |
| Main GitHub osservato | a00605862f627710347bd63c49f79a6d0a00135f |
| Candidato respinto / tree | 59b6b93cd9c215e8b687e540f7cd579804b7c66a / cf08c14a8deb18145189afbe9722d7da46bc2f82 |
| Base immediata del lavoro | 288dc1926bfd7ab4ce43bb4377a9a0064313ad69, consegna documentale discendente del candidato respinto |
| Worktree nuovo | /Users/luker/fot-tep-harness-0310-correzioni |
| Branch | codex/studio2-harness-0310-correzioni |
| Acquisizione separata | ec012911444de6baf1751ae4bf4aee8e9c24adbb |
| **Candidato tecnico** | **0c8157f23bee49a3a5a2df648525c34706da29d7** |
| **Tree tecnico** | **a1573b49615a875f24ee97f9f1cd4bab399be93d** |
| Parent del candidato tecnico | ec012911444de6baf1751ae4bf4aee8e9c24adbb |
| Stato al termine del commit tecnico | HEAD sul candidato, worktree pulito |
| Manifest candidato | HARNESS_OFFLINE_CANDIDATE.json; 11662 byte, SHA-256 **8ed9fbc37ee14d162ce65f55430159bb1e2507e95cf65aa8d72df3743170dbe1**; **44 membri verificati** |

Questo report e PROMPT_VERIFICA_CORREZIONI_HARNESS_03_10.md appartengono a una consegna
documentale successiva: non cambiano il tree tecnico sopra. Il suo commit/HEAD finale è
comunicato in chat, evitando un hash autoreferenziale nel report o nel manifest.

Sono rimasti invariati gli snapshot Git di copia principale, worktree della consegna
288dc192 e clone del revisore. Quest’ultimo conserva origin locale: non è stato usato
per attestare main GitHub. Nessun merge, fetch di delta paralleli, push, tag o riscrittura
di storia. Nessuna modifica alle correzioni 03.8 o al record D9.

## 2. Acquisizione e riproduzione del NON OK

Acquisito [verbale originale](non_ok_20260915/evidence/VERIFICA_HARNESS_OFFLINE_03_10.md),
SHA-256 fc9725d5412ff30b789977cf12e6ae4742f8063cce7b6e5e2242aeddb3d61547, insieme al
manifest SHA256SUMS originale, SHA-256
0d25177f41ef9651ee246d5ad8610c020e43c931e168f3c18ba9098d871f0223.

Verificati prima dell’uso e ricontrollati alla consegna **2.754 membri / 129.997.935 byte**.
1.471 membri sono copiati byte-identici; 1.283 membri reference restano alla collocazione
esatta del revisore per evitare duplicazione dei dati development già conservati.
[ACQUISIZIONE.json](non_ok_20260915/ACQUISIZIONE.json) elenca ogni percorso, SHA-256,
dimensione, ruolo, stato acquisito/esterno e motivazione. SHA256SUMS è preservato intatto,
non riscritto per nascondere i riferimenti esterni. Le cache escluse dal manifest originale
non sono acquisite. Le fixture false/alterate sono separate e marcate **non scientifiche**.

La riproduzione usa una copia sacrificabile degli script/prove con candidate puntato al
clone respinto esatto: nessuna scrittura nel revisore. Risultato: **50 metodi, 32 metodi
non conformi, 34 failure di assertion, zero errori**; anche l’insieme degli identificativi
non conformi coincide con l’originale. Log e JSON sono in correzioni_evidence/reproduced_non_ok.*.

Runtime compatibile: /opt/anaconda3/bin/python3, **3.13.9 arm64**, SQLite **3.51.0**.
Non è ripetuto il tentativo con rpds di architettura incompatibile del Python di sistema:
quella prova storica è acquisita separatamente e non confusa con un difetto del candidato.
Il nuovo ingresso R4 controlla anche la dipendenza prima del trasporto; un test ne verifica
il rifiuto con zero invii stub.

## 3. Correzioni e prove

La [matrice R01–R10 e delle 50 riproduzioni](MAPPA_RIPRODUZIONI_R01_R10.md) collega
ogni requisito a codice, prove ed esito locale. Il [contratto eseguibile e di ripresa](CONTRATTO_ESECUZIONE_E_RIPRESA.md)
descrive gli ingressi, il protocollo di crash e le prove necessarie alla riconciliazione.

Il delta di correzione è un commit coerente: separare ledger e runner avrebbe lasciato
commit intermedi con API incompatibili. Codice, fixture e regressioni sono quindi insieme;
l’acquisizione forense resta un commit distinto e la consegna documentale segue il candidato.

| Controllo | Risultato dell’esecutore |
| --- | --- |
| Suite mirata, inclusa nuova regressione | **82/82**, nessuna failure o errore |
| Discovery Fase03 | **117/117**, nessuna failure o errore |
| Metodi originali applicabili | **14/14**: 12 senza modifica del metodo; N20/N21 con soli argomento/campione di fixture adattati |
| Raccordo metriche qualificato | 9/9 nei test; i suoi tre file sono byte-identici alla base |
| Processi concorrenti | Riserve/ritenti esclusivi e chiusura stadio esercitati con writer separati |
| Crash reali | os._exit(23) nei punti del lifecycle e nei runner producer, sonda e gate; intenti e raw già persistiti sopravvivono |
| Ripresa | Raw ricevuti rivalutati senza nuovo invio; timeout incerto blocca; retry soltanto dopo prova e selezione esplicite; ripristino del file di freeze da stadio chiuso senza nuove chiamate |
| CLI con stub | Preflight storico rifiutato a zero invii; flusso producer/sonda approvato esclusivamente in fixture usa lo stesso ledger |
| Alterazioni | Fonti, tokenizer, R4, manifest/handoff, template, configurazione congelata e triplette rifiutati nei percorsi pertinenti |
| Compilazione | compileall completato, cache esterna al candidato |
| Whitespace del delta | Codice/documenti conformi; log forensi byte-identici conservano whitespace emesso da unittest, dichiarato e non ripulito |
| Guardiano documentale | **35 test, stessi 14 identificativi di fallimento storico, 1 skip, 0 errori: NON PASS** |

I conteggi delle diverse suite si sovrappongono e non vanno sommati come difetti o prove
indipendenti. Le modifiche delle fixture sono motivate nella matrice: le asserzioni non
sono state indebolite. N48 è ora rappresentato come richiesta FAILED contata e gate
incompleto, senza fabbricare raw o una valutazione completa 120/120; la semantica qualificata
dei denominatori resta nei tre file metriche invariati.

[Comandi/runtime](correzioni_evidence/COMMANDS.json),
[log mirati](correzioni_evidence/targeted.log), [discovery](correzioni_evidence/discovery.log),
[metodi originali](correzioni_evidence/applicable_original.log),
[confronto documentale per identificativo](correzioni_evidence/DOCUMENTATION_COMPARISON.json)
e [provenienza/perimetro](correzioni_evidence/PROVENANCE_AND_SCOPE.json) sono acquisiti e
improntati nel manifest. I log documentali completi restano esterni ai percorsi/impronte
esatti del confronto, poiché ripetono grandi assertion storiche già conservate.

## 4. Perimetro e file

Diff tecnico rispetto all’acquisizione: **30 percorsi, 3.750 inserimenti e 1.195 rimozioni**,
comprendenti codice, test, contratto, matrice, manifest e prove. L’acquisizione forense è
separata: il suo inventario esplicito sostituisce l’elenco in prosa di migliaia di file.
La consegna successiva aggiunge questo report, il nuovo prompt di review e il manifest documentale CONSEGNA_CORREZIONI_HARNESS_03_10.json (hash/dimensioni dei due documenti, senza autoreferenze).

- `studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md` — Contratto delle barriere, transizioni, crash, riconciliazione e limiti.
- `studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json` — Manifest revisione 2: 44 hash/dimensioni, esclusione del proprio hash.
- `studio2/fase03/harness/MAPPA_RIPRODUZIONI_R01_R10.md` — Matrice R01–R10 e corrispondenza delle 50 prove originali.
- `studio2/fase03/harness/correzioni_evidence/COMMANDS.json` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/correzioni_evidence/DOCUMENTATION_COMPARISON.json` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/correzioni_evidence/PROVENANCE_AND_SCOPE.json` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/correzioni_evidence/applicable_original.json` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/correzioni_evidence/applicable_original.log` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/correzioni_evidence/discovery.log` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/correzioni_evidence/reproduced_non_ok.json` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/correzioni_evidence/reproduced_non_ok.log` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/correzioni_evidence/targeted.log` — Prova/log o metadati di verifica locale; provenienza e ruolo nel manifest.
- `studio2/fase03/harness/gate_rules.py` — Autenticità di campione, identità e triplette con T3/T4/T6 preservati.
- `studio2/fase03/harness/guards.py` — Approvazione esecuzione/ordine, coordinate ledger e identità risposta.
- `studio2/fase03/harness/inputs.py` — Pin delle sorgenti, JSON evidence, inventario autenticato e handoff dal ciclo attivo.
- `studio2/fase03/harness/insight_adapter.py` — Risoluzione della dipendenza R4 prima del trasporto oltre ai pin esistenti.
- `studio2/fase03/harness/ledger.py` — Macchina a stati atomica, piani immutabili, quote, raw/record/receipt, riconciliazione e autenticazione degli stadi.
- `studio2/fase03/harness/ledger_cli.py` — Comandi locali per stato, riconciliazione zero-token e autorizzazione del diff remediation.
- `studio2/fase03/harness/offline_fixtures.py` — Helper sacrificabili marcati, nessun input scientifico.
- `studio2/fase03/harness/preparation.py` — Verifica delle fonti e del manifest eseguibile prima della preparazione e del reload.
- `studio2/fase03/harness/producer.py` — Template esplicito e verificabile senza cambiare i byte del template iniziale.
- `studio2/fase03/harness/render.py` — Controllo dell’approvazione e contatori distinti per chat e campo insight.
- `studio2/fase03/harness/runtime.py` — Lifecycle comune, fsync dei journal, resume conservativo e controllo risposta.
- `studio2/fase03/harness/test_harness_offline.py` — Stessi metodi, fixture conformi alle nuove API e al campione congelato.
- `studio2/fase03/harness/test_revisions.py` — 37 regressioni R01–R10 incluse CLI, processi, crash, artefatti e riprese.
- `studio2/fase03/prepare_gate.py` — Autenticazione input, renderer R4 e pin tokenizer senza fallback silenzioso.
- `studio2/fase03/producer_probe.py` — Conformità, remediation e libreria collegate a guardie, piano e persistenza.
- `studio2/fase03/protocol.py` — API ordinaria instradata al renderer R4; primitive sintetiche restano offline.
- `studio2/fase03/run_pilot.py` — Sonda/gate con guardie, risultati autenticati, sospensione identità e ripresa esplicita.

Confrontati con la base e preservati: metric_adapter.py, metrics.py, test_metric_raccordo.py;
piano generale e statistico rev.10, APERTURA, walkthrough, D9, 03.7, baseline 03.9 e schema
03.12. Nessuna variazione di A/B, FAR, U3 o dei freeze. L’inventario pending originale e il
preflight storico non sono cambiati. Le sole ricostruzioni development avvengono su fixture
per provare il delta R02/R03: nessun download, nuovo audit scientifico, estrazione o produzione
di risultati delle sottofasi chiuse.

## 5. Residui e limiti della consegna

- Serve una **nuova review indipendente** del candidato esatto; questa finestra implementa e
  testa, non emette un OK indipendente sul proprio lavoro.
- D9 è **già approvata** nei ruoli 122B principale/consumer, 27B alternativo completo, Terra
  storico interno. Il record aaba893dff8c62f9f9281eec7423eee020235e03 è stato letto; nessuna
  richiesta di nuova scelta. Il recepimento nei file eseguibili resta un delta successivo;
  la nuova barriera non lo anticipa e non sblocca il preflight storico.
- L’ordine label 1a reale resta non approvato. Tutte le approvazioni dei test sono fixture.
- Non sono prodotti insight reali o qualificati servizi, tokenizer/chat template, capacità,
  identità/fingerprint, stabilità, latenza o fattibilità T5 con margine del 20%.
- I ledger legacy sono preservati e rifiutati, non migrati automaticamente. Una migrazione
  reale richiede una riconciliazione e un delta verificati. Gli errori incerti non autorizzano
  reinvii: dove la risposta non è mai arrivata su disco non si finge di averne recuperato i raw.
- L’autenticazione è rispetto ad approvazioni e prove locali acquisite, non una firma remota
  dei pesi o del provider. Le prove zero-token devono essere realmente fornite e approvate;
  codice e test non possono inventare quella prova esterna.

**Nessuna chiamata a provider, inferenza o simulazione scientifica. Nessun push, merge,
tag, freeze, GO, chiusura 03.10/Fase03 o aggiornamento walkthrough.**

Letture: contratto MAINTENANCE della copia principale e del candidato, prompt pertinenti,
verbale e riproduzioni, specifica/rapporto/manifest/consegna del candidato respinto, delta
normativo 03.10, record D9 e codice coinvolto. Ordine di alcune centinaia di kB di testo
pertinente; gli inventari e i log voluminosi sono verificati anche meccanicamente per hash,
identificativi e risultati. Nessuna rilettura della letteratura o del piano generale intero.
