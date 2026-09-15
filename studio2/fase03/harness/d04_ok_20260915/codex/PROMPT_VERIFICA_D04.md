# Review indipendente D04 — candidato esatto e decisioni negli stadi aperti

In altra finestra, preferibilmente altro modello. Prima di modificare qualsiasi cosa leggi
docs/MAINTENANCE.md e rispettalo. Questa è una review: candidato in sola lettura, output
solo in un nuovo contenitore esterno con fixture sacrificabili. Nessuna correzione, commit,
tag, push, merge, freeze o GO. Il report della preparazione è oggetto della verifica.

## Identità

- Source `/Users/luker/fot-tep-harness-0310-d04`, branch codex/studio2-harness-0310-d04.
- **Tecnico `aae29a908356e4a4842a214fdc3db9bff26ec3ca`, tree `4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`.**
- Base `97868f9d6ef281c2dd4ab1c6ffb67e2477ee5715`, acquisizione `f0dca4d2d46a290d2ffeb1840abd46eb7664f0ae`, test-first `bf7774f2d153ecc50f27ba095f77b612933b4d26`.
- Manifest: 98 membri, 24151 byte, SHA-256 `9fbad8c036075605a9bbdfdac84078259428b679fc33341ed98f21050a07efd6`.
- [Report](REPORT_CORREZIONE_D04.md); successore documentale di soli quattro file, da
  acquisire via git show. Clona detached il tecnico, non l’HEAD documentale.

Verifica repository/branch/HEAD/tree/status/worktree e main su GitHub effettivo, non su
origin di un clone locale. Main osservato a00605862f627710347bd63c49f79a6d0a00135f.
Preserva tutti i sorgenti/review e il verbale Claude untracked nel source D03.

## Fonti e integrità

Leggi i due verbali integrali acquisiti in non_ok_23859a2_20260915 e i contratti correnti.
Claude SHA bc3ee96afb2bd890d0b326ca4965d03c46d241f288a30c5ee1455a0c8ec9a47f;
Codex SHA 21e457af023a9a8fae3560f663784c55788408942f8c9e902b3d468764aceef9;
manifest Codex SHA 9334c9c57b159cf14f047d28646544615c99aaf751298753e573f893dbbb86a1.
Verifica tutti i membri delle acquisizioni/riproduzioni e le coordinate esterne.
Claude dà OK sul nucleo D03 con suite env-bloccate; Codex conferma D03 e apre D04 P2.
Non sommare i loro perimetri né convertire i limiti d’ambiente in PASS.

## D04 e invariante

Sul vecchio 23859a2, un solo quota_kind di retry passa da transport a base nello stadio
aperto. V05 consente l’ottavo retry senza rinuncia; V06 effettua un nuovo invio prima del
timeout. Le prove zero-token restano intatte. Valutare il nuovo controllo **prima** della
decisione di riserva/invio, non soltanto in chiusura.

1. `_validated_attempt_inventory` deve riusare l’intero `_validate_attempts` su tutti gli
   stadi che contribuiscono alla riserva cumulativa. Stadi aperti/partial coverage ammessi,
   senza imporre prematuramente outcome o PASS. Quote/ruoli confrontati con piano e catena.
2. Binding nuovo/ripreso prima di client/server; tutte le riserve base/remediation/retry e
   triplette atomiche prima della nuova riga. Verifica guardia simmetrica e reale lock sotto
   la transazione della decisione; guasto dopo precedente successo sulla stessa istanza.
3. Riproduci V01–V06 byte-identici: originali, crash veri, scrittore concorrente, D03 contenuti
   e V05/V06. Ottavo retry rifiutato, zero nuovi invii, otto intenti/sette retry reali e DB intatto.
4. Runner e CLI: client non costruito, server_mock.assert_not_called(), output/DB invariati.
   Esamina anche ingressi che non chiamano prima bind_stage e contributori di altro stadio.
5. Matrice generata da D04_DECISION_CONTRACT e JSON rosso/verde: 216 casi, 72 positivi,
   14 dipendenze. Guardie degli inventari, limiti espliciti e perimetri non coperti.
6. Positivi: rinuncia lecita fino a 15 trasporti, rifiuto del sedicesimo; sonda mai oltre sette,
   remediation e triplette invariate; nessuna riclassificazione automatica per mascherare il fault.
7. Snapshot è diagnostico: su V05/V06 rifiutate legge sei quota transport per sette retry reali.
   Valuta che non venga usato per autorizzare richieste e che la discordanza sia rifiutata
   negli ingressi normativi. Nessuna pretesa di autenticità di un dump SQL manomesso.

D03 deve rimanere invariato: tre percorsi, 11 controlli condivisi, digest ricalcolabili,
legame durevole, file letti una volta, no-backfill e rifiuto dello storico senza digest.
Non introdurre nuovi requisiti di resistenza a riscrittura arbitraria coerente dell’intera
catena; approfondire liberamente i guasti pertinenti, distinguendo riproduzioni e ipotesi.

## Risultati da riprodurre

[Comandi](d04_evidence/runs/COMANDI.md), inventario e prove inclusi. Python compatibile
/opt/anaconda3/bin/python3, PYTHONDONTWRITEBYTECODE=1; nuovi output, mai script in-place.
FOT_HARNESS_TARGET seleziona il codice per lo stesso file test D04; FOT_D04_OBSERVATIONS
sceglie il nuovo JSON. Verifica che il test non cambi fra rosso/verde e rispetto a test-first.

- D04: 8 metodi/240 assertion fallite/zero errori sul respinto; 8/8 sul corretto.
- Mirati 128/128; discovery 163/163. D01 7, D02 8, D03 9, D04 8 inclusi.
- V 6/6 (prima due failure), W 4/4, Y 7/7, Z 5/5, applicabili 14/14.
- X: 23 letterali + X23 già adattato; conservare la sola failure letterale obsoleta.
- Guardiano NON PASS: stessi 14 identificativi, 35 test, 1 skip, zero errori, non bloccante.
- 177 file protetti identici, 94 Python live compilati; solo runtime ledger.py +18/−3.

TEST_FIRST si verifica sul commit bf7774f2d153ecc50f27ba095f77b612933b4d26: fonti/test/prove precedono il runtime,
ledger identico a 23859a2. Leggi JSON/log: launcher storico può uscire zero con assertion
fallite. Il generatore D04 produce le stesse coordinate dalla nuova esecuzione.

## Consegna e confini

Verbale autonomo con verdetto in prima riga, OK/NON OK sul tecnico esatto; prove/log/manifest
senza autoreferenze, stati Git iniziali/finali, matrice esplicita dei 50 metodi con N48≡C02
e adattamenti dichiarati. Distinguere metodi/sottocasi/suite sovrapposte; non 50/50 letterali.
Dichiara modello/finestra/effort osservati e limiti d’ambiente. Preparatrice gpt-6-astra/xhigh;
le review del precedente candidato non sono una review di questi nuovi byte.

D9 approvata: 122B principale/consumer, 27B alternativo completo, Terra storico interno.
D9 eseguibile, ordine label, qualificazioni, T5/pilot separati; preflight storico bloccato.
Tre metriche e artefatti scientifici intatti. Nessun freeze o GO.
