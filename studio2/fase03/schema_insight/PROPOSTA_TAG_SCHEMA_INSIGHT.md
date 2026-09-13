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
