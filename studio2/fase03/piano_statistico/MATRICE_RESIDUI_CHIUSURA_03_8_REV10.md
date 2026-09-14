# Matrice dei residui reali di chiusura 03.8 — rev.10

Data: 2026-09-14, Europe/Rome. Stato: preparazione locale, **03.8 aperta**.
Base di integrazione osservata: `origin/main`
`a00605862f627710347bd63c49f79a6d0a00135f`. Candidato statistico verificato:
`6aaa5b3eebfed4ba502c25c0443caabd0051af21`; acquisizione e verbale:
`51782e8c40069c0a2310afafc36907a61d517ff6`.

Questa matrice aggiorna lo stato operativo senza riscrivere il candidato rev.10.
Approvazione, verifica, firma, pubblicazione e freeze sono eventi distinti.

| Requisito | Prova primaria | Stato reale al candidato di allineamento |
| --- | --- | --- |
| Identità piano rev.10 | `PIANO_STATISTICO.md`, SHA-256 `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` | ✅ acquisito byte-identico |
| Manifest rev.10 | `PIANO_STATISTICO_FREEZE.json`, SHA-256 `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8` | ✅ acquisito byte-identico; stato storico pending preservato |
| Verifica indipendente rev.10 | `VERIFICA_PIANO_STATISTICO_REV10.md`, SHA-256 `d269e26d8cb4e23370577e1e193d90d9357d66f7c739e9d0669970edf71b0066` | ✅ OK sul recepimento A/B; non è firma o freeze |
| Approvazioni scientifiche e organizzative | record A/B e decisioni storiche: D2=8, D11, F6/F4 condizionati, m=0,125, alpha, gerarchia, politica R | ✅ approvate e recepite; nessuna nuova approvazione richiesta |
| Bibliografia e addendum F6/F4 | 23/23 file dell'inventario `ACQUISIZIONE_LETTERATURA_03_8.json`; verbale `551f7da9…ddaf`; addendum `f2c29416…0b8e` | ✅ presenti in `origin/main` corrente, impronte e dimensioni coincidenti; nessuna nuova ricerca/conservazione |
| 03.5 | artefatti e consegne proprie già pubblicate | ✅ chiusa; FAR e U3 non riaperti |
| 03.9 | `PUBBLICAZIONE_BASELINE_03_9.md`; tag remoto `studio2-fase03-baseline-numerica-frozen-001`, peeled `38cb5f5e…1e` | ✅ chiusa, pubblicata e congelata |
| 03.12 R4 | `PUBBLICAZIONE_SCHEMA_INSIGHT.md`; tag remoto `studio2-fase03-schema-insight-frozen-001`, peeled `3c64390b…143` | ✅ pubblicata e congelata; pin adapter resta 03.10 |
| Firma materiale | atto rev.10 non firmato, SHA-256 `4a0a4e1f…1cc8`; nessuna copia sottoscritta | ❌ blocca il tag 03.8 |
| Piano generale | delta in `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | ⏳ candidato preparato; richiede verifica indipendente |
| APERTURA | delta in `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` | ⏳ candidato preparato; richiede verifica indipendente |
| Documentazione walkthrough MD/HTML | coppia non modificata in questa preparazione | ⏳ da aggiornare in parità **dopo** l'OK del delta normativo |
| Regole per 03.10 | fonte immutata `DELTA_HARNESS_03_10.md`, SHA-256 `e92661fe…355e`; consegna corrente separata | ✅ consegna predisposta; implementazione/verifica appartengono a 03.10 e precedono il pilot |
| D9 | nessun producer, consumer o alternativo scelto qui | ⏳ finestra parallela; non blocca il tag statistico, blocca configurazione e misure operative |
| T5 / ramo R=3 | formula e regola A fissate; identità modelli, X/Q, giorni, latenze, calendario e finestra non misurati | ⏳ prima dello studio; non attestabile prima di D9/pilot |
| OOD tecnici | regola B e catene fissate; generabilità/trip/ammissibilità non eseguiti | ⏳ in 03.11 **dopo** il freeze e prima delle chiamate; non crea dipendenza circolare dal tag |
| Verifica del delta normativo corrente | prompt separato, da eseguire su copia isolata | ❌ blocca documentazione di chiusura e tag |
| Pubblicazione 03.8 | candidato non ancora raggiungibile da `origin/main` | ❌ blocca il tag |
| Manifest/tag efficaci | `freeze_effective=false`, `freeze_tag=null`; tag previsto assente | ❌ ultimo passaggio, solo dopo firma, review, documentazione e pubblicazione |

## Dipendenze da D9

Dipendono da D9: identità e configurazione effettive dei ruoli producer,
consumer e alternativo; aggregazione delle chiamate se i ruoli coincidono;
tokenizer/capienza; endpoint e fingerprint; allocazione per modello di X/Q;
latenze, concorrenza misurata, giorni e finestra W; T5 e fattibilità del ramo
R=3; esecuzione delle conformità e dei gate pertinenti.

Non dipendono da D9 e sono completabili ora: preservazione/acquisizione rev.10,
verifica delle pubblicazioni 03.9/03.12 e della bibliografia, firma materiale,
allineamento normativo e sua review, documentazione di chiusura, pubblicazione
del piano e tag statistico. I controlli OOD dipendono dal freeze, non da un
risultato 03.11 precedente al tag.

## Residui che impediscono il tag 03.8

1. copia materialmente sottoscritta dell'atto rev.10, acquisita e improntata;
2. verifica indipendente OK del candidato di allineamento;
3. documentazione di chiusura aggiornata dopo l'OK, inclusa parità walkthrough
   Markdown/HTML e controllo dei link;
4. commit finale pubblicato e raggiungibile da `origin/main` senza sovrascrivere
   il main con snapshot precedenti;
5. manifest finale non autoreferenziale e tag annotato pubblicato, con prova
   remota di oggetto e peeled.

D9, T5, implementazione 03.10 e controlli tecnici OOD 03.11 restano obbligatori
nei rispettivi momenti, ma la regola B evita di usarli come prerequisiti
circolari del tag statistico.
