OK

# Review indipendente del pacchetto materiale per la firma 03.8 — rev.10

Il pacchetto al candidato **7cf523805710633ec3b4fecd4eb8b7c9504076bf**, tree **5c8c49ff33ac01c3a778515688e5c064ccbb0be4**, è idoneo alla successiva firma personale di Luca nei limiti delle istruzioni verificate. Il confronto integrale con l'atto originario non mostra nuove decisioni scientifiche o autorizzazioni. Nessun rilievo bloccante individuato nel delta **8a3f7ba..7cf5238**.

**L'OK riguarda il pacchetto proposto, non una firma acquisita, un freeze statistico o un GO sperimentale.** Non si trasferisce a modifiche successive. Il prossimo passo è l'acquisizione separata di questo verbale nella finestra preparatrice; poi Luca potrà produrre la copia personale firmata, senza riscrivere proposta e originale.

## Identità runtime e indipendenza

- Revisore: Codex; modello esposto **gpt-6-astra**, provider **openai**, effort esposto **high**.
- Sessione/task: **01a0a1d9-8ccd-7893-b504-4fde93380ea0**.
- Fonte effettivamente letta: `session_meta` e ultimo `turn_context` nel file `/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T23-36-24-01a0a1d9-8ccd-7893-b504-4fde93380ea0.jsonl`, limitatamente ai campi di identità. Modello e identificativo non sono ricavati dal nome della finestra né copiati dagli antecedenti.
- **Questa sessione non ha preparato il pacchetto 7cf5238.** Ha emesso i precedenti verbali NON OK R1–R4, OK delle correzioni e OK del recepimento documentale D9. Resta indipendente dalla preparazione del nuovo candidato; conserva quel contesto e non è una review senza antecedenti o una seconda opinione di altro modello. Nessun sottoagente impiegato.
- Worktree del revisore: `/Users/luker/fot-tep-verifica-pacchetto-firma-038`, detached HEAD sul candidato esatto; repository comune `/Users/luker/fot-tep`.
- Fonte/preparatore: `/Users/luker/fot-tep-allineamenti-038-r1-r4`, branch `codex/studio2-allineamenti-038-r1-r4`, preservato. Unica scrittura della review nel checkout isolato: questo verbale, non tracciato. Non acquisito nella finestra preparatrice.

## Mandato, contratto e preflight

Letto l'handoff `/Users/luker/fot-tep/studio2/fase03/HANDOFF_FASE03_2026-09-15_rev03.md`, SHA-256 al riscontro `a16565239866e88679c7e98543ba3015e435ed2a1d9c332a8d36ff87ead46620`. È usato come aggiornamento operativo, non come fonte delle decisioni scientifiche. Per il pacchetto sono state usate le fonti esatte e gli antecedenti acquisiti.

Letti `docs/MAINTENANCE.md` e `docs/prompts/Verifica_LLM.md` **dal candidato**; contratto byte-identico a quello già esaminato nella review D9. Applicati §§1–2, 5 e 8.6 del contratto: preservazione, controlli documentali e verbale nella cartella della sottofase in copia separata. Le regole pertinenti di Prompt/Fase/Documentazione/Commit e le prevalenze walkthrough già lette in questa sessione restano applicabili; nessuna nuova review harness o bibliografica è stata aperta. Nessun AGENTS.md trovato nelle directory antenate e nella catena della destinazione.

Il worktree preparatore era pulito, sul branch atteso e al commit richiesto. Creata una copia isolata detached mediante `git worktree add --detach`, verificati HEAD/tree e stato iniziale pulito. Nessun checkout nel worktree preparatore o nella copia principale. `origin/main` e `git ls-remote origin refs/heads/main` coincidono a **a00605862f627710347bd63c49f79a6d0a00135f**: nessun avanzamento remoto rispetto alla base operativa dichiarata.

| Oggetto | Commit | Tree | Parent |
| --- | --- | --- | --- |
| Base immediata, acquisizione OK D9 | `8a3f7ba706570201c5b622c4e0fc79529b1c8cfd` | `9120edadbf65c7001302e57a9d3e21f256123602` | `7d9100a4d2c3f8dd8f61e4f9316ebd8549c1da90` |
| **Pacchetto firma verificato** | `7cf523805710633ec3b4fecd4eb8b7c9504076bf` | `5c8c49ff33ac01c3a778515688e5c064ccbb0be4` | `8a3f7ba706570201c5b622c4e0fc79529b1c8cfd` |

✅ Parentela diretta, unico parent. Delta esatto: **2 file aggiunti +1 modificato**, tutti in `studio2/fase03/piano_statistico/`:

- aggiunta `DECISIONI_AUTORE_03_8_COPIA_FIRMA_REV10.md`;
- aggiunta `INVENTARIO_PACCHETTO_FIRMA_03_8_REV10.json`;
- modifica `ISTRUZIONI_FIRMA_MATERIALE_REV10.md`.

Nessun cambiamento a piano rev.10, atto originario, budget, delta harness, verbali, acquisizioni, file scientifici, codice, paper_sections o walkthrough. L'aggiornamento delle istruzioni è il delta esplicito in review; la loro precedente versione rimane recuperabile dalla base 8a3f7ba e non viene presentata come byte-identica alla nuova.

## Confronto integrale atto originario / copia proposta

Letti entrambi i testi per intero e prodotto il diff completo in memoria con `difflib.unified_diff`. Oltre al giudizio semantico, confrontati meccanicamente la sezione 1 e il blocco dichiarazione/campi della sezione 4: identici.

| Parte della copia proposta | Esito | Differenza e valutazione |
| --- | --- | --- |
| Titolo e intestazione, righe 1–9 | ✅ | Dichiara derivazione dall'originale con byte/hash, natura separata e proposta non firmata da verificare. Non retrodata una firma né cancella l'originale. |
| §1, righe 11–32 | ✅ | **Integralmente identico all'originale**: fonti, tabella degli esiti, condizioni e rinvio alla bozza completa con Allegati A/B. D2, H1–H3, margine, alpha, gerarchia, OOD, D11, R, audit, canary, pilot, riserva e scorte non cambiano. |
| §2, riga 46 | ✅ | Unica variazione della sezione: “tempi e D9 non ancora verificati” diventa distinzione fra tempi/fattibilità non verificati e ruoli D9 approvati successivamente, separati dalla qualifica. È sostenuta dal record D9 aaba893 e dalla sua acquisizione/OK documentale, non modifica A. Testo di approvazione A/B, fonte e riga B identici. Il titolo storico “Nuove decisioni” non richiede una nuova approvazione: la data del 14 settembre e l'esito già approvato restano espliciti. |
| §3, righe 49–74 | ✅ | Sostituisce i campi tecnici vuoti con candidato/tree statistico, dimensioni/hash di piano, manifest e verbale rev.10, e catena degli OK R1–R4/D9. Tutti i valori sono verificati sui blob. Nessuna firma su un testo futuro indeterminato; il manifest mantiene i propri stati storici pending/non congelato. |
| §3, righe 76–88 | ✅ | Aggiorna i ruoli già acquisiti e distingue esplicitamente label 1a, metadati/qualifiche/T5, harness, OOD e autorizzazioni. Restano acquisizione della firma, raccordo, integrazione/pubblicazione e freeze come eventi futuri separati. Ordine freeze statistico→03.11→chiamate rispettato; nessuna dipendenza circolare introdotta. |
| §4, righe 90–103 | ✅ | Dichiarazione, nome autore e campi vuoti di luogo/data e firma invariati. Cambia soltanto il testo di acquisizione futura, precisando nome della copia restituita e registrazione di dimensione/hash alla ricezione. Non viene inserita alcuna firma o data per Luca. |

La sostituzione del vecchio §3 non cancella condizioni scientifiche: il piano è vincolato per hash, il §1 mantiene le catene OOD e i requisiti propri/distinti, la bozza completa rimane il riferimento degli esiti e le prove tecniche non vengono attestate. Nessuna riapertura di A/B, FAR, U3 o ruoli D9; **ordine label 1a ancora distinto e non approvato**. Non viene aggiunto un confronto, una quota, un retry, un calendario o un nuovo parametro sperimentale.

## Fonti degli aggiornamenti temporali e catena acquisita

✅ L'atto originario è preservato nel candidato e coincide con il blob statistico 6aaa5b3 e quello della storia corrente 767e1d0: 4.974 byte e hash atteso. Il suo presente temporale su review/allineamenti/D9/bibliografia è precedente ai record successivi; la copia proposta lo aggiorna senza riscriverlo.

| Stato richiamato | Evidenza riscontrata | Esito |
| --- | --- | --- |
| A/B già approvate | `APPROVAZIONE_ADDENDUM_03_8.md`, 2.830 byte, hash `df2a754d3ad2d2215def012eb4d6e887c77d93ebdcad4a6811c5cbc18786a70a`; riferisce l'addendum esatto 526561f, approvato senza modifiche da Luca il 14 settembre 2026 | ✅ Nessuna nuova richiesta di approvazione |
| Rev.10 verificata | candidato `6aaa5b3eebfed4ba502c25c0443caabd0051af21`, tree `24847ce0cc4ff7b6defea4d65f3f41cb9ccd1c1a`; OK acquisito a `51782e8c40069c0a2310afafc36907a61d517ff6` | ✅ Identità, hash e stato del manifest storico corretti |
| R1–R4 OK acquisito | 9a56d12 candidato, 16f2274 sola consegna; verbale di 20.816 byte, hash `9248c42572a20388ddf5af976840e68fdc908e545312a63234167778ce53a256`, acquisito a 5b78421 | ✅ Antecedente integro; audit non ripetuto |
| D9 approvata/acquisita/recepita | record sorgente aaba893, acquisizione dc4d656, candidato documentale 8a20c12; ruoli P=C=122B e P_alt=27B full16, Terra storico interno | ✅ Nessuna qualifica o nuova approvazione dedotta |
| OK documentale D9 acquisito | verbale di 21.644 byte, hash `bb8555792c5dad78fc3ffeaf5f797e3da427ef79ec1d3ebe7c840810f77c53e3`, acquisito a 8a3f7ba | ✅ Confrontato anche con l'originale nella copia del revisore e con il blob di acquisizione |
| Integrazione bibliografica non più pendente | antecedente `VERIFICA_ALLINEAMENTI_03_8_REV10.md`, sezione B (23/23 e integrazione già constatata); registro pubblicazione consolidamento letto da a006058; commit bibliografici e37c3db e 40911d0 antenati del main remoto osservato | ✅ Stato di pubblicazione sostenuto, senza rifare l'audit dei paper |

La nuova acquisizione **7d9100a→8a3f7ba** aggiunge esclusivamente il verbale D9 e `ACQUISIZIONE_OK_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md`. Quest'ultimo è stato letto integralmente: candidata/base/tree, provenienza, dimensione/hash e limiti del verdetto coincidono. L'OK D9 non certificava il pacchetto firma successivo; questo verbale lo esamina separatamente.

## Inventario, impronte e riferimenti

✅ `INVENTARIO_PACCHETTO_FIRMA_03_8_REV10.json` è JSON valido. Controllate **11/11 voci dotate di percorso/byte/SHA-256**: copia, originale, piano, manifest, OK rev.10, bozza, addendum, approvazione A/B, record D9, OK R1–R4 e OK D9. Ogni impronta e dimensione coincide con il candidato. Per ogni pin di fonte/acquisizione/storia corrente associato al file è stata confrontata anche l'identità byte per byte con `git show <commit>:<path>`; tutti coincidono. Verificata l'ascendenza dei pin della storia corrente.

Il `candidate_commit` delle voci di review identifica l'oggetto verificato, mentre `acquisition_commit` identifica il blob del verbale successivo: i due non sono confusi. Il tree statistico è stato risolto con Git. Il manifest rev.10 contiene effettivamente `freeze_effective=false`, `freeze_tag=null` e review rev.10 storicamente pending. L'inventario non include il proprio hash; la sua identità è fissata dalle istruzioni e dal commit, senza ciclo di auto-impronta. Le istruzioni sono vincolate dal candidato e vengono improntate anche nella tabella seguente.

| Artefatto | Byte verificati | SHA-256 verificato |
| --- | ---: | --- |
| Atto originario | 4974 | `4a0a4e1fc2797ee7a81439110e164d43159c745007136c9dda7bed7759471cc8` |
| Copia proposta | 6585 | `d470a6ce477f31f85951df8d877d786429a56e2f34a369407ae590494c39f605` |
| Inventario | 6622 | `e83420d7d151bac88dea297bc880b8dc1dcde4d3999b61c32b96f76249ce00aa` |
| Istruzioni firma | 3763 | `601754706b7c590bc338021cdf51327a82beffdc4fca475451752e8cf2df2082` |
| Piano rev.10 | 81490 | `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` |
| Manifest rev.10 | 25894 | `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8` |
| OK rev.10 | 12478 | `d269e26d8cb4e23370577e1e193d90d9357d66f7c739e9d0669970edf71b0066` |

✅ Tre impronte attese dall'autore coincidenti. Tre link Markdown della copia risolti (bozza, addendum e approvazione); le istruzioni usano percorsi testuali e contengono zero link Markdown. Verificati i rinvii alle fonti tramite i percorsi dell'inventario e i blob pinnati. Il percorso assoluto della proposta nelle istruzioni esiste nella copia preparatrice e ne identifica gli stessi byte. Il percorso di restituzione è **futuro**, non un artefatto firmato già presente o da creare dal revisore.

## Procedura di firma e ricezione

✅ `ISTRUZIONI_FIRMA_MATERIALE_REV10.md` è stato letto integralmente e confrontato con la sua versione alla base. Le istruzioni:

1. escludono la firma dell'atto originario con stati superati e subordinano la nuova copia all'OK sul delta esatto;
2. richiedono controllo di byte/hash e creazione di **copia separata**;
3. limitano la compilazione personale di Luca a **luogo/data effettivi e firma effettiva**; `Autore: Luca` non è una sottoscrizione;
4. vietano modifiche al testo e agli identificativi/impronte delle fonti;
5. prevedono restituzione normalmente come `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.md`, oppure formato realmente prodotto (PDF/scansione/contenitore digitale), conservando la sorgente e documentando la trasformazione;
6. impongono alla ricezione controllo di provenienza, presenza dei campi personali, confronto del testo, formato, dimensione/hash e record separato, senza auto-riferimenti o firme apposte dal preparatore.

Non è richiesta a Luca la compilazione di hash o commit tecnici: sono ora fissati nel testo. Per la copia Markdown le differenze ammesse sono solo nei due campi personali; per altri formati non è ammessa una ricostruzione artificiale in Markdown. Il presente controllo riguarda la procedura proposta: **nessuna firma ricevuta o autenticata in questa review**.

## Controlli eseguiti e limiti

✅ `git diff --check 8a3f7ba 7cf5238`: exit 0, nessun output. Pulito anche il delta di acquisizione 7d9100a→8a3f7ba. Confronto per blob dei tre file oggetto e delle fonti; verifica ulteriore di preservazione rispetto alla base per originale, piano, manifest, budget, delta harness e due OK antecedenti. Il diff limita le scritture preparatorie ai tre file elencati.

⚠️ Guardiano documentale rieseguito secondo Verifica_LLM: **35 test, 14 fallimenti storici, 1 skip, 0 errori, exit 1 — NON PASS**. Confrontati identificativi completi e sottocasi, non solo conteggio: oggetto ricostruito identico sia a `guardian_before` sia a `guardian_after` di `CONTROLLI_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json`. Stessa ripartizione 1/1/9/3 nei quattro metodi UnifiedConversationChecks; stesso skip TutorialChecks per walkthrough legacy assente. Stdout+stderr catturati in memoria. Nessuna regressione osservata dal guardiano; ciò non sostituisce il confronto materiale e normativo.

Comandi/procedure principali:

```text
git show 7cf523805710633ec3b4fecd4eb8b7c9504076bf:<path>
git show -s --format='%H %T %P' 7cf5238
git diff --name-status 8a3f7ba 7cf5238
git worktree add --detach /Users/luker/fot-tep-verifica-pacchetto-firma-038 7cf523805710633ec3b4fecd4eb8b7c9504076bf
git rev-parse HEAD HEAD^{tree}
git status --short
git rev-parse origin/main
git ls-remote origin refs/heads/main
git log --format='%H %T %P %s'
git show <pin>:<percorso fonte>
git merge-base --is-ancestor <pin> <candidato o main pinnato>
git diff --check 8a3f7ba 7cf5238
python3 docs/test_explanation.py
```

Script Python di sola lettura con pathlib/json/hashlib/subprocess/difflib hanno verificato voci dell'inventario, dimensioni/hash, identità dei blob, confronto integrale dei due atti e risoluzione dei link. Nessun esperimento, test statistico, prova harness, chiamata a servizi, invio a terzi, push, merge o tag. Nessuna firma/data compilata per Luca. Nessuna modifica o acquisizione nel worktree preparatore. I precedenti audit sono antecedenti con i loro limiti, non campagne rieseguite.

Letti handoff operativo, contratto e prompt pertinenti, quattro documenti del pacchetto, nuova acquisizione dell'OK D9, record di approvazione A/B, fonti/identità dell'inventario e sezioni di stato degli antecedenti. Letture documentali nell'ordine di alcune migliaia di parole; nessuna nuova ricerca scientifica. La review non qualifica formati firmati ancora inesistenti, autenticità di una firma futura, servizi o metadati tecnici.

## Prossimo passo consentito

**La finestra preparatrice può acquisire questo verbale byte-identico in un passaggio separato, registrandone provenienza, dimensione e SHA-256. Questa sessione non compie tale acquisizione.** Dopo tale passaggio, Luca può verificare l'impronta della proposta 6.585 byte / `d470a6ce477f31f85951df8d877d786429a56e2f34a369407ae590494c39f605`, crearne una copia separata e compilare personalmente soltanto luogo/data effettivi e firma, secondo le istruzioni verificate.

Destinazione normalmente prevista: `/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.md`, oppure stesso stem ed estensione reale per altro formato. Dopo la restituzione occorre la verifica/acquisizione effettiva dell'artefatto firmato; raccordo documentale, integrazione/pubblicazione e manifest/tag finali restano passaggi distinti soggetti ai propri requisiti. Nessuna autorizzazione a svolgerli è esercitata qui.

**03.8 e Fase 03 restano aperte.** L'OK sul pacchetto non firma, non congela, non approva l'ordine label 1a, non riapprova A/B/FAR/U3/D9 e non autorizza pilot o altre esecuzioni. Il verbale è lasciato non tracciato nella copia isolata; dimensione e SHA-256 sono comunicati fuori dal file.

Emissione della review: 2026-09-15T15:32:57+02:00 (Europe/Rome; non data della firma di Luca).
