# Matrice corrente dei residui 03.8 dopo acquisizione D9

Data: 2026-09-15. **03.8 e Fase 03 aperte; nuovo delta D9 da verificare**.
Successore documentale della [matrice rev.10](MATRICE_RESIDUI_CHIUSURA_03_8_REV10.md),
che resta byte-identica e descrive il suo checkpoint, non lo stato corrente D9.
Fonte decisionale: [record D9](../DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md),
commit sorgente `aaba893dff8c62f9f9281eec7423eee020235e03`, SHA-256
`fcb113636de80cc87709905324436555e0ba103bd46de3ac079ce0ef7f60f1b8`.

| Stato distinto | Evidenza | Esito locale e residuo |
| --- | --- | --- |
| 1. Scelta dei ruoli | record D9 §§1–2 | **Approvata:** P=C=122B, P_alt=27B, libreria alternativa completa 16 insight, consumer 122B fisso nello swap; Terra solo storico interno separato, senza nuove chiamate. Nessuna riapprovazione richiesta |
| 2. Acquisizione del record | ACQUISIZIONE_D9_ALLINEAMENTI_03_8.md; tre blob aaba893 | **Completata** byte per byte nel ramo 03.8, con provenienza |
| 3. Recepimento documentale | piano generale, APERTURA, questa matrice e consegna tecnica successiva | **Preparato localmente, review del nuovo delta pending**; non eredita l’OK precedente |
| 4. Recepimento eseguibile | finestra proprietaria delle correzioni harness R01–R10 | **Pendente/non attestato da questa consegna**; nessun suo file o candidato importato |
| 5. Identità, configurazioni, qualifica e fattibilità | record D9 §§4–5; rev.10 e budget preservati | **Da documentare/verificare/misurare** sui servizi effettivi; nomi nominali e operatività dichiarata non sono qualifica |

## Vincoli e residui separati

- **Ordine label 1a:** ancora non approvato; non deriva dalla scelta dei ruoli.
- **Firma materiale 03.8:** atto personale ancora da acquisire; non è sostituita
  dal record D9 o dall'OK indipendente.
- **Qualifica e autorizzazione:** nessun GO, pilot o chiamata autorizzata da questa
  acquisizione; nessuna configurazione, revisione o metadato tecnico inventati.
- **Contabilità:** P e C sono 122B; richieste distinte aggregate per modello
  senza duplicarle. Nessun budget aggiuntivo, reset ledger o modifica di R,
  quote, riserva e hard stop. Collocazione della conformità alternativa (`a`),
  riusi, X/Q e calendario non sono approvati dalla sola D9.
- **Consumer fallback:** 27B non approvato; se un cambio di ruoli si rendesse
  necessario richiederebbe una nuova decisione, non una riapprovazione di D9.
- **Quartetto dello swap:** rintracciare la scelta pre-specificata come da
  consegna D9; se mancante, decisione strutturale prima della misura. Non
  dedurlo da D11 o dai fault di continuità e non sceglierlo in questa sessione.

## Verifiche e freeze

L'OK R1–R4 su `9a56d12d0633a0c9790c48792182f26fc6eb424a` è acquisito nel
[verbale](VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md), con il limite di
indipendenza dichiarato dal revisore. Non certifica acquisizioni e delta D9
successivi, per cui è richiesto un nuovo esito indipendente.
L'OK statistico rev.10 e tutti i byte verificati sono preservati. A/B, FAR,
U3, 03.5, 03.9 e 03.12 non sono riaperti; nessun test scientifico ripetuto.

Prima del freeze statistico restano firma materiale, verifica indipendente dei
nuovi delta, documentazione pertinente, integrazione/pubblicazione autorizzata
su main effettivo e manifest/tag finali secondo la procedura. Nessuno di questi
passaggi è compiuto o autorizzato dalla sola D9.
Il recepimento harness e le condizioni operative restano necessari prima dei
rispettivi stadi, senza diventare una dipendenza circolare del freeze statistico.
**Freeze statistico → run e controlli tecnici 03.11 → chiamate sui test dopo
T5 e tutti gli altri GO.** Le verifiche OOD restano dopo freeze e prima delle
chiamate, con catene e criteri rev.10 intatti.

Prossimo passo: review indipendente limitata alle due acquisizioni e al nuovo
delta D9. Harness, paper 03.15 e walkthrough sono passi distinti e non sono
modificati da questa consegna. Nessun push, merge su main, tag o esecuzione.
