# Prompt autonomo — verifica indipendente del candidato di finalizzazione 03.8

Modello suggerito: **gpt-6-astra**. Reasoning suggerito: **high**. Il compito
richiede confronto di provenienza, Git, impronte, documenti accoppiati e
contratti di freeze; privilegia accuratezza e controllo dei limiti del verdetto.

---

Proseguiamo Studio 2 FoT-TEP, Fase 03. Esegui una review indipendente e
read-only del solo candidato locale di finalizzazione 03.8.

Non modificare il candidato e non committare il verbale. Non effettuare push,
merge, tag, freeze, firma, chiamate ai servizi, inferenze, simulazioni, pilot o
run finali.

## Identità obbligatorie

- repository remoto atteso: `https://github.com/sorrentinoluca/fot-phd.git`;
- base del delta: `6490af4889fd679d491f63b9debdf2314eaf7aca`;
- candidato: `4c9e7a1f1d8bd07b7d6be8df724f743986717da8`;
- tree candidato: `03b215980ae170db2e1284dd7bd5eb07b830fb28`;
- genitore unico atteso: `6490af4889fd679d491f63b9debdf2314eaf7aca`;
- `origin/main` osservato in preparazione:
  `a00605862f627710347bd63c49f79a6d0a00135f`.

Lavora in un worktree nuovo, isolato e detached sul candidato esatto. Prima di
valutare il delta leggi integralmente `docs/MAINTENANCE.md` del candidato, i
prompt pertinenti in `docs/prompts`, il report, il manifest e le fonti che
quest'ultimo indica. La consegna e il presente prompt sono istruzioni esterne
nel branch successore: non includerli nel tree verificato e non estendere a essi
il verdetto.

Ricontrolla remoto effettivo, commit, tree, genitore, stato del worktree e main
remoto corrente. Se `origin/main` è avanzato, registra il fatto e stabilisci se
serve un successivo delta di integrazione/review; non sostituire il candidato e
non assumere che un vecchio controllo provi la pubblicabilità sul nuovo main.

## Perimetro della review

Leggi il diff integrale `6490af4..4c9e7a1`. Deve contenere esattamente:

- `docs/fot_walkthrough_conversazione_studio2.md`;
- `docs/fot_walkthrough_conversazione_studio2.html`;
- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`;
- `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`;
- `studio2/fase03/piano_statistico/COORDINAMENTO_CHIUSURA_03_8.md`;
- `studio2/fase03/piano_statistico/MATRICE_RESIDUI_03_8_DOPO_D9.md`;
- `studio2/fase03/piano_statistico/MANIFEST_CANDIDATO_FREEZE_03_8.json`;
- `studio2/fase03/piano_statistico/REPORT_FINALIZZAZIONE_03_8.md`.

Non ripetere gli audit scientifici rev.10, R1–R4, D9 o approvazione
documentata. Verifica invece che le loro identità e portate siano riportate
senza estendere gli OK a byte successivi.

## Controlli richiesti

1. Verifica che il piano rev.10 resti di 81.490 byte con SHA-256
   `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`
   e che `PIANO_STATISTICO_FREEZE.json` resti di 25.894 byte con SHA-256
   `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`.
   Controlla inoltre la preservazione di `DELTA_HARNESS_03_10.md`, della coppia
   `DESIGN_RESOLUTION`, delle decisioni, dei verbali e delle acquisizioni.
2. Valida `MANIFEST_CANDIDATO_FREEZE_03_8.json`: 12.382 byte, SHA-256
   `bcc9ef183190e2fd0997b2e600fc53498e4a6194993e997820255a4b6d124dc6`;
   JSON valido, 23/23 artefatti, 20/20 genitori della catena e nessun
   auto-riferimento. Deve mantenere `freeze_effective=false` e nulli commit
   pubblicato, target, oggetto e peeled del tag.
3. Controlla che il raccordo descriva fedelmente: D2=8; D11; F6/F4
   condizionati; margine, alpha, gerarchia e politica R; nessun tetto rigido
   vigente di 3.700; conteggio completo e fattibilità `1,20 × T ≤ W`; controlli
   OOD nella 03.11 dopo freeze e prima delle chiamate; nessuna dipendenza
   circolare dal completamento 03.11 prima del tag.
4. Controlla D9 senza riaprirla: 122B producer principale e consumer, 27B
   producer alternativo della libreria completa di 16 insight, Terra soltanto
   storico descrittivo interno. L'OK documentale non qualifica il runtime.
5. Controlla che l'approvazione documentata dell'autore sostituisca la firma
   materiale senza creare o richiedere
   `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.*`; il pacchetto firma deve restare
   storico. La decisione non approva ordine label 1a o esecuzioni.
6. Verifica che 03.8 sia sempre “in finalizzazione locale”, Fase 03 aperta, e
   che pubblicazione e freeze non siano anticipati. Il candidato harness
   `6a8031b` resta esterno e NON OK R-D9-01/R-D9-02.
7. Verifica parità semantica e testuale delle modifiche MD/HTML, navigazione,
   anchor, link relativi e markup bilanciato. Non modificare il walkthrough
   divulgativo né i file `paper_sections/`.
8. Esegui `git diff --check`. Esegui il guardiano su base e candidato e
   confronta identificativi e sottocasi, non solo i totali. L'atteso storico è
   **NON PASS**, 35 test, 14 fallimenti e 1 skip; non definirlo PASS. Ogni nuova
   firma di fallimento è bloccante finché diagnosticata.
9. Verifica che tutte le fonti siano recuperabili dal candidato o dalla sua
   storia destinata all'integrazione, senza dipendenze operative da `/tmp` o da
   altri worktree. Verifica l'assenza del tag remoto previsto senza crearlo.
10. Valuta la sequenza proposta nel report: review → acquisizione →
    pubblicazione autorizzata → eventuale manifest efficace e sua review → tag
    annotato sul futuro commit esatto → verifica remota di oggetto e peeled.
    Segnala qualunque auto-riferimento, target inventato o byte normativo che
    verrebbe pubblicato senza review.

## Verdetto e output

Scrivi un solo nuovo file non tracciato:
`studio2/fase03/piano_statistico/VERIFICA_FINALIZZAZIONE_03_8.md`.

Apri con **OK** oppure **NON OK** e limita esplicitamente il verdetto al commit
`4c9e7a1f1d8bd07b7d6be8df724f743986717da8`, tree
`03b215980ae170db2e1284dd7bd5eb07b830fb28`, contro base `6490af4` e agli otto
file del delta. Riporta prove, comandi essenziali, impronte, esito del guardiano,
limiti e rilievi bloccanti/non bloccanti.

Non dichiarare pubblicata, chiusa o congelata 03.8 e non dichiarare chiusa la
Fase 03. Non committare il verbale: comunica percorso, dimensione e SHA-256 per
la successiva acquisizione byte-identica.
