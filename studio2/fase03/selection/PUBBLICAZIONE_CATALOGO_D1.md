# Pubblicazione e congelamento del catalogo D1

Data: **2026-09-13**. Responsabile: **Codex**. Operazioni autorizzate dall'autore:
`Documentazione_LLM` → `Commit_LLM`, tag dedicato e integrazione in `origin/main`.

**D1 è congelata e pubblicata.** Il catalogo è F1, F2, F3, F8, F10, F13, F14, F15.
Il tag annotato `studio2-fase03-catalogo-D1-frozen-001`, oggetto
`b6828afc3062e1e6371376638c42eab529635e32`, punta al commit
`ab43f0b20f45cdb475c0caf52c6f7afcbae50891`. Dopo il push atomico di main e tag,
il server remoto ha restituito questi stessi riferimenti; il commit era la punta di
`origin/main`. L'[attestazione leggibile da macchina](CATALOG_PUBLICATION.json) registra
riferimenti, istante di osservazione, impronte e condizioni di efficacia.

## Documentazione e controlli

La documentazione della sotto-fase era già completa e aveva ricevuto l'OK di
[VERIFICA_CONSEGNA_D1.md](VERIFICA_CONSEGNA_D1.md), dopo l'OK scientifico di
[VERIFICA_CATALOGO_D1.md](VERIFICA_CATALOGO_D1.md). Non sono stati ripetuti
estrazione, enumerazione, digest, replay, test di regressione o audit indipendente.
Le impronte hanno confermato l'identità dei 16 file consegnati con i blob committati e
contenuti nel tag. Sono stati controllati anche i collegamenti dei manifest alle fonti
storiche e agli artefatti; nessuna discrepanza.

I manifest e i verbali **non sono stati riscritti dopo il tag**. I campi
`reviewed_pending_commit_and_publication` e `catalog_frozen=false` restano il loro stato
storico, precedente alla pubblicazione. Le condizioni `effective_when` sono ora soddisfatte:
OK indipendente, commit raggiungibile da `origin/main` e tag annotato pubblicato.
`CATALOG_PUBLICATION.json`, prodotto dopo la verifica remota, attesta quindi
`catalog_frozen=true`. È un'attestazione amministrativa successiva, non una revisione del
catalogo, dei criteri o dei verbali indipendenti. Il tag resta sul pacchetto verificato;
questa attestazione viene integrata in main con un commit successivo.

La coppia walkthrough è aggiornata insieme, con lo stato efficace e il rinvio a questa
attestazione; il piano cambia soltanto nello stato D1, senza modificare il disegno.
La nuova nota in PROVENIENZA registra l'identità pubblicata, senza nuovi riusi.
Il §0.1 del walkthrough non contiene un blocco D1 da rimuovere; gli altri punti restano aperti.
La sintesi divulgativa resta invariata: si tratta di preparazione del protocollo, senza un
nuovo risultato scientifico. Non cambia la struttura degli indici.

La parità della coppia e i collegamenti sono controllati sul contenuto aggiornato;
i dettagli sono in `CATALOG_PUBLICATION.json`, campo `documentation_checks`.
Dopo le sole modifiche di stato documentale, `python3 docs/test_explanation.py` registra
**35 test, 14 fallimenti preesistenti, 1 skipped**, invariati rispetto alla baseline
committata in `D1_DELIVERY_CHECK.json`. Questo test generale non copre D1.

## Commit e file inclusi

**`a980a20b723e30a24ea75da72ff5b32f145a5082` — registra il catalogo D1 e la verifica indipendente.**
Codice, log, manifest e relativa verifica rimangono nello stesso commit.

- `studio2/fase03/selection/CATALOG_FREEZE.json` — catalogo e impronte verificati.
- `studio2/fase03/selection/CRITERIA_FREEZE_rev002.json` — revisione amministrativa tracciata; rev1 intatta.
- `studio2/fase03/selection/D1_DRAW_LOG.json` — record originario dell'unico sorteggio.
- `studio2/fase03/selection/D1_REVIEW_CHECK.json` — controlli del riesame già eseguiti.
- `studio2/fase03/selection/PROPOSTA_OOD_D11.md` — proposta non approvata, esclusa dal perimetro decisionale del freeze.
- `studio2/fase03/selection/REPORT_CATALOGO_D1.md` — report dell'esecuzione e delle correzioni.
- `studio2/fase03/selection/VERIFICA_CATALOGO_D1.md` — verifica indipendente, NON OK iniziale e OK finale.
- `studio2/fase03/selection/draw_d1.py` — revisione corretta del replay già verificata.
- `studio2/fase03/selection/execution_snapshot/draw_d1.py` — byte dello script originariamente eseguito.
- `studio2/fase03/selection/test_draw_d1.py` — quattro regressioni già verificate.
- `studio2/PROVENIENZA.md` — fonti e natura prespecificata di D1.
- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` — stato D1 verificato, ancora precedente alla pubblicazione.

**`ab43f0b20f45cdb475c0caf52c6f7afcbae50891` — documenta il catalogo D1 verificato.**
È il commit del tag; include insieme la coppia e la verifica documentale.

- `docs/fot_walkthrough_conversazione_studio2.md` — §4.2 e raccordo con lo stato storico §4.1.
- `docs/fot_walkthrough_conversazione_studio2.html` — replica con contenuto allineato.
- `studio2/fase03/selection/D1_DELIVERY_CHECK.json` — impronte e controlli della consegna prima del push.
- `studio2/fase03/selection/VERIFICA_CONSEGNA_D1.md` — OK indipendente della consegna documentale.

**Commit successivo al tag — attesta la pubblicazione del catalogo D1.**
Il commit che introduce questo resoconto registra quanto osservato sul remoto dopo il push;
non sposta il tag e non contiene modifiche agli artefatti congelati.

- `studio2/fase03/selection/CATALOG_PUBLICATION.json` — riferimenti remoti verificati, efficacia e controlli documentali.
- `studio2/fase03/selection/PUBBLICAZIONE_CATALOGO_D1.md` — questo resoconto, con file e limiti della consegna.
- `docs/fot_walkthrough_conversazione_studio2.md` — stato D1 congelato e pubblicato.
- `docs/fot_walkthrough_conversazione_studio2.html` — medesimo aggiornamento della replica.
- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` — solo stato D1, senza modifiche ai criteri o ad altre decisioni.
- `studio2/PROVENIENZA.md` — nota con tag, commit e attestazione di efficacia.

## Perimetro e lavoro ancora aperto

Nessuna modifica estranea incorporata o lasciata in sospeso. La proposta OOD/D11 è conservata
per tracciabilità, ma il fatto che sia raggiungibile dal tag non la rende una decisione
approvata. Nessun risultato per-fault è stato consultato per questa pubblicazione;
nessuna simulazione o inferenza scientifica è stata eseguita.

D1 chiude soltanto la scelta del catalogo. Restano D2, le due classi OOD, le coppie D11,
il producer alternativo, la specifica di generazione con il rapporto alla nota Downs & Vogel
su IDV(14)–IDV(15), nuovi run ed evidence e il gate reale 03.0. La Fase 03 e il protocollo
scientifico restano aperti; questo congelamento non autorizza nuovi run.

Letture: prompt Documentazione/Commit e Prompt_LLM, MAINTENANCE, sezioni pertinenti del
walkthrough Studio 2, report e verifiche D1, manifest e controlli di consegna, soli passaggi
di stato D1 nel piano e §6 di PROVENIENZA. Costo documentale nell'ordine di decine di migliaia
di token; nessuna nuova ricerca bibliografica, lettura dei risultati o inferenza sperimentale.
