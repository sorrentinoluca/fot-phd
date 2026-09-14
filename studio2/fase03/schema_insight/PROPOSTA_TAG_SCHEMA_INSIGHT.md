# Proposta sospesa — tag dello schema insight, contratto revisione 4

Data 2026-09-14. Il tag `studio2-fase03-schema-insight-frozen-001` **non è stato creato**.
La revisione 4 è implementata ma attende riverifica indipendente R4-V e qualifica col
tokenizer pinnato; questa proposta non autorizza tag, push, merge o produzione di insight.

## Target superato e identificazione del nuovo oggetto

Il vecchio target `e058cb07dceeefa8eb4a4b6d1f6fcab5aad483db` riguardava il contratto
revisione 3, manifest revisione 4, SHA-256
`d6ef52de0f573edf3e5d6eb5ad3530400c5f63e6bcfa6579a93f21fdfb8865b5`.
È **superato** dal rilievo bloccante di 03.10: `context_check` non accettava la label
letterale `Normal` congelata da 03.7.

Il nuovo oggetto proposto è il contratto revisione 4 descritto da
`SCHEMA_FREEZE.json`, manifest revisione 5, con
`previous_manifest_sha256 = d6ef52de0f573edf3e5d6eb5ad3530400c5f63e6bcfa6579a93f21fdfb8865b5`.
L’impronta del manifest rev. 5 identifica i byte della revisione e viene riportata nella
consegna. Lo SHA Git del commit che contiene questo documento non è scritto al suo interno,
per evitare un auto-riferimento circolare: va acquisito da Git nella consegna e confermato
dal verificatore R4-V.

## Condizioni ancora necessarie

1. Riverifica indipendente R4-V, in altra finestra e con modello diverso, con verdetto OK.
2. Esecuzione della suite R4 col tokenizer pinnato: il test locale corrente ha 25 PASS,
   0 FAIL e 1 SKIP su 26 perché lo snapshot non è disponibile. I 23 PASS Qwen della
   revisione 3 sono storici e non qualificano il codice/test R4.
3. Eventuale aggiornamento delle impronte pinnate nell’adapter 03.10 in un commit proprio,
   soltanto dopo la pubblicazione del tag; non fa parte di questa patch.
4. Autorizzazione dell’autore all’attuazione della procedura di integrazione/tag.

La riverifica deve accertare che il delta funzionale in `validator.py` sia confinato a
`context_check`, che la fixture derivi dai byte 03.7 in `main` e ne controlli il tag, e che
schema JSON, cap, regex, `leakage_rules_v1.json`, scanner e logica del diff siano immutati.
Deve inoltre confermare 16 insight totali, due per ciascuna owner fault e nessun insight
Normal, oltre alla catena delle impronte del manifest.

I verbali e i log precedenti restano fotografie storiche, non approvazioni della revisione 4.
Il nuovo log locale è `TEST_RESULTS_rev004.txt`. Dopo un OK indipendente, il prompt di
integrazione/tag dovrà essere aggiornato con SHA del commit e impronta del manifest rev. 5
verificati; solo allora potrà riprendere la procedura già definita sotto.

Testo indicativo dell’annotazione futura: `studio2(fase03): schema insight contratto rev004
verificato; context_check allineato alla label Normal di 03.7; manifest rev005 e qualifica
Qwen verificati; Fase 03 aperta`.

---

## Record storico della proposta per la revisione 3

# Proposta autorizzata — tag dello schema insight, contratto revisione 3

L’autore ha autorizzato la **proposta**, con la procedura già usata per 03.7,
dopo l’OK indipendente sul delta e il test col tokenizer pinnato. Questo record
non attesta creazione o pubblicazione del tag né integrazione in main.

## Oggetto esatto

Tag annotato proposto: `studio2-fase03-schema-insight-frozen-001`.
Commit destinatario: `e058cb07dceeefa8eb4a4b6d1f6fcab5aad483db`.
Contratto revisione 3; manifest revisione 4.
SHA-256 del manifest a quel commit:
`d6ef52de0f573edf3e5d6eb5ad3530400c5f63e6bcfa6579a93f21fdfb8865b5`.

Il target resta il commit indicato dall’autore e dal verificatore: il successivo
commit che acquisisce il verbale e questa proposta non cambia l’artefatto verificato.
Il verbale acquisito è `VERIFICA_SCHEMA_INSIGHT_rev003.md`, §9, modello Claude
(Cowork, sessione claude-fable-5-1), finestra distinta dall’esecutore Codex/GPT-6.
Il precedente `VERIFICA_SCHEMA_INSIGHT.md` resta la fotografia della prima verifica.

## Controlli soddisfatti

- OK indipendente della prima revisione e del delta; osservazioni (a)–(c) chiuse.
- Log originale `TEST_RESULTS_qwen_rev003.txt`: 23 PASS, zero skip, 4,065 secondi.
- Impronte tokenizer nel log coincidenti con quelle del preflight.
- Sonde: stringa vuota 0 token, `a` 1, `XMEAS(7)` 6.
- Tutti i 16 record sintetici: 84 token/record, 20 narrativa, 4 evidence_scope.
- Quindici impronte e dimensioni del manifest ricalcolate: 15/15 coincidono.
- Schema, cap e interfacce immutati; nessuna produzione di insight o inferenza.

La qualifica riguarda implementazione e fixture: non dimostra ottimalità dei cap,
capienza dei prompt reali o validità semantica degli insight.

## Limitazioni accolte e passaggio a 03.10

Resta conservativo il rifiuto delle parole normal/unknown, valve/valvola, feed,
step, A/B e delle sequenze x + spazi + mv/meas anche entro parole comuni
(esempi: «six MV values», «exmv»). Questi vincoli vanno dichiarati esplicitamente
nel prompt del producer in 03.10. Non si modifica di nuovo la regex dopo l’OK.
Il limite lessicale non dimostra assenza di ogni possibile leakage semantico.

I byte originali del log restano invariati, incluso lo spazio finale alla riga 16
segnalato da `git diff --check`: non è una correzione da applicare a un raw log.
Il rifiuto strutturale va loggato; il pilot conserva zero retry automatici.

## Procedura successiva, come 03.7

1. Conservare verifica e decisione di accettazione separatamente dal manifest.
2. Dopo l’autorizzazione all’attuazione, aggiornare la documentazione della sotto-fase
   nelle coppie previste e integrare la storia verificata in main, preservando gli
   altri cantieri. Pubblicare main e accertare che il target e il verbale siano
   raggiungibili da origin/main.
3. Ricontrollare al target le impronte e che il tag non esista già; creare il tag
   annotato sull’esatto e058cb0 e pubblicarlo. Nessuno spostamento di tag esistenti.
4. Verificare con ls-remote oggetto tag e commit peeled; registrare separatamente
   la pubblicazione effettiva con identificativi e controlli, come
   `PUBBLICAZIONE_PSEUDOLABEL.md` per 03.7.

Il manifest resta la fotografia storica pending: non se ne riscrivono stato,
log o impronte per attestare il tag. Verbale e futuro record di pubblicazione
attestano i passaggi successivi. La Fase 03 resta aperta.

Il tag deve precedere qualunque insight scientifico, incluse le otto chiamate
producer di conformità del pilot. Questa proposta non autorizza quelle chiamate.

## Testo proposto dell’annotazione

studio2(fase03): schema insight contratto rev003 verificato; qualifica Qwen 23/23,
conteggi e impronte tokenizer nel log, 15 impronte artefatti OK; falsi positivi
conservativi dichiarati per 03.10; Fase 03 aperta.
