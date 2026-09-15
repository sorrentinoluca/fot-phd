# Verifica indipendente D03 — tecnico esatto e invariante delle prove zero-token

Incarico di review in altra finestra, preferibilmente altro modello. Sola lettura sul
candidato: nessuna correzione/commit/tag/push/merge/freeze/GO. Prove offline solo in nuovi
sandbox sacrificabili, output esterni. Il report della preparazione è oggetto della verifica.

## Identità

- Source `/Users/luker/fot-tep-harness-0310-d03`, branch codex/studio2-harness-0310-d03.
- **Candidato tecnico `23859a29225ccd9cd6f47e4a0b6e36258831dbab`; tree `fe66025f4925e27676b0be16428475e3fcaee060`.**
- Base documentale `e9b60c5db77edfd3c06a29857e6ba5f61ebe139a`.
- Acquisizione `efa9f6f94194985104047d831c0b087dc460532d`; contratto/test-first `567881abf06572812c00ccc0ed817d169b68fee6`.
- Manifest 83 membri, 20826 byte, SHA-256 `483c7db5ad4a763a8f41d084538c7a2cce6b2a7d799a5ba11d57da852cee3828`.
- [Report corrente](REPORT_CORREZIONE_D03.md).

Il source avrà un successore documentale di soli quattro file. Verificane parent/diff,
acquisisci i documenti via git show e usa un clone detached sul tecnico esatto, non sul
successore. Registra repository, HEAD/tree/status/branch/worktree e main sul remoto effettivo
GitHub, non origin di un clone locale. Main osservato a00605862f627710347bd63c49f79a6d0a00135f.
Preserva principale, source, review e prove precedenti.

## Fonti e integrità

Leggi MAINTENANCE e prompt pertinenti, mandato D03, [contratto iniziale](CONTRATTO_D03_PRIMA_DEL_CODICE.md),
[contratto corrente](CONTRATTO_ESECUZIONE_E_RIPRESA.md), inventario e codice.
[Verbale precedente](non_ok_a219bd4_20260915/files/VERIFICA_D02.md) integrale:
SHA-256 b88f046592ac9d1b0f784c1d127f83ea3cc609c93bd547bbc91c7541cfd0223f.
SHA256SUMS precedente: 4ed360ee40d521e989e38fa2a2a68d5a5c461a5a6397c94dd34a598300141776.
Verifica i membri su disco: 1.869 acquisiti, 116 copie/1.753 esterni, e tutti i membri
manifest/riproduzioni correnti. Le fixture SQL alterate sono prove, non input scientifici.

## Invariante da verificare

Acquisizione e riuso devono applicare gli stessi controlli di contenuto della prova e
dell’approvazione, con precondizioni di stato proprie dei chiamanti. La riconferma autentica
contenuti e legame durevole prima di qualsiasi server/stub o invio.

1. Verifica `_validate_zero_token_evidence` nei **tre percorsi**: reconcile_zero_token,
   `_validate_attempts`/antenati retry, `_gate_transport_record` del gate riconciliato.
   Il validatore deve controllare identità, tre int zero esclusi bool, ricevuta/evidenza,
   autore, decisione e binding del file. La guardia deve osservare lo stesso insieme di
   11 controlli effettivamente passati, non soltanto la presenza nominale di una funzione.
2. Verifica digest contenuti prova/approvazione distinti dagli hash dei file e legame
   reconciled_integrity. Ricalcolo e confronto, non sole stringhe reciprocamente uguali.
   Parsing/hash devono usare gli stessi byte letti una volta. Controlla atomicità di due
   eventi/cambio stato, lock e assenza di cache fra transazioni.
3. Riproduci W01/W02 con valori positivi/mancanti/bool e campi vuoti. Prova anche alterazioni
   apparentemente valide e hash locali riallineati con contenuti semanticamente invalidi.
   Gate INTENT riconciliato e FAILED già INVALID successivamente riconciliato sono entrambi
   nel raggio. Il record INVALID originario non deve cambiare e non deve diventare risposta.
4. Runner e CLI budget/stability --resume: HarnessError prima del server; richiedi
   `server_mock.assert_not_called()`, zero nuovi invii, contatori/database/output invariati.
   Esamina anche stadi aperti e assegnazione di nuovi retry, non solo gate già chiusi.
5. **Nuovo requisito storico autorizzato:** nessun backfill. Prove prive di digest/legame
   devono fallire in riconferma/retry/gate; lo sblocco richiede riconciliazione revisionata
   separata, non inclusa. Catene senza quelle prove mantengono i positivi. La nuova prova
   0c8157f genera una catena allora valida con retry e verifica rifiuto/132 intenti invariati.
6. Controlla inventario N/F, guardia sui campi nuovi e matrice generata: 69 voci, 56 con nuove
   mutazioni e 13 collegate a contratti storici (non nuove mutazioni individuali dichiarate).
   Valuta adeguatezza e limiti senza equiparare classificazione a esaustività combinatoria.
   Default DA_COPRIRE anche per nuove chiavi nominate di evidence/approval; payload opachi
   improntati ereditano N. Verifica positivi per timestamp/catture/note forensi.
7. Il campo quota_kind emerso dalla matrice deve coincidere col ruolo base/remediation/retry,
   senza modificare quote/contatori. Approfondisci guasti pertinenti senza riscrivere coerentemente
   l’intero database e tutte le impronte e chiamare questo un guasto a campo singolo.

## Prove richieste e dichiarazioni da controllare

Comandi completi in [d03_evidence/runs/COMANDI.md](d03_evidence/runs/COMANDI.md).
Python compatibile /opt/anaconda3/bin/python3, PYTHONDONTWRITEBYTECODE=1.
Per eseguire il nuovo file test sul vecchio codice, passare FOT_HARNESS_TARGET al clone
respinto, senza scrivere lì i test. Impostare esplicitamente il target anche nell’esecuzione
diretta sul corretto; FOT_D03_OBSERVATIONS sceglie un nuovo output JSON.

- Stessi test finali: **9 metodi/8 failure/zero errori su a219bd4; 9/9 sul corretto**.
- Mirati **120/120**, discovery **155/155**, inclusi tutti i sette D01 e otto D02.
- Intera matrice storica: **W01–W04 4/4, Y 7/7, Z 5/5**, script byte-identici.
- Applicabili **14/14**, 12 letterali e due precedenti adattamenti fixture/argomento.
- X: **23 letterali + X23 già adattato**, mantenere visibile la sola failure letterale
  obsoleta. Nessun nuovo adattamento di assertion. Per X23 copiare entrambi i moduli.
- Positivi: multi-hop dieci intenti/otto coppie, retry nove, gate INVALID/FAIL, remediation,
  sonda rimaterializzata dopo gate, stesso risultato senza nuovi invii/eventi.
- Guardiano **NON PASS**, 35 test/stessi 14 identificativi/1 skip/zero errori, non bloccante.
- 176 file protetti invariati; 93 Python live compilati.

Verifica la cronologia: contratto e test-first precedono il runtime. TEST_FIRST.json si
riferisce ai blob del commit 567881abf06572812c00ccc0ed817d169b68fee6; non confrontare l’hash iniziale del test con la
versione finale dopo la guardia annidata rafforzata. FINAL_TEST_PROVENANCE.json identifica
quella finale, rieseguita su entrambi i codici. Le esecuzioni precedenti e un errore iniziale
solo di import sono conservati e distinti, senza contarli come nuovi difetti o nuovi PASS.
Leggi JSON/log: gli script storici possono uscire 0 anche con assertion fallite.

## Consegna e confini

Produci verbale autonomo, matrice esplicita dei 50 metodi con corrispondenze/N48/adattamenti,
prove/log/manifest senza autoreferenze, stato Git iniziale/finale e OK o NON OK sul tecnico
esatto. Distingui metodi, sottocasi e suite sovrapposte; non dichiarare 50/50 letterali.
Dichiara modello/finestra/effort osservati. Preparer gpt-6-astra/xhigh, revisore precedente
stesso modello/high in altra finestra: causalità del modello non dimostrata. Nessuna promessa
che cambiare modello elimini i difetti; verifica il presidio di contratto indipendentemente.

Tre metriche qualificate e perimetri scientifici intatti. D9 approvata: 122B principale/consumer,
27B alternativo completo, Terra storico interno. D9 eseguibile, ordine label, qualificazioni,
T5 e pilot restano separati; preflight storico bloccato. Nessun freeze o GO.
