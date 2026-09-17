# Correzione rilievi bloccanti successor 122B — Qwen D9 03.13

## Esito

**READY FOR NEW INDEPENDENT REVIEW.** Sono stati corretti P1-02a/b, P2-01, P2-02 e
l'ambiguità di `identity_sha256` sul candidato respinto
`a6bc817165fcab820b9c4bbe7209fc7ca53d7d1d`, tree
`e2c4ecadbadfbac15947cdaff589256f91ffe9d3`, parent
`72fb93c6d26ceb220ed2cece1dac2ef6614c791f`.

Il verbale indipendente è conservato byte-identico in
`harness/reviews/VERIFICA_MIRATA_RILIEVI_CLAUDE_03_13.md`, SHA-256
`ada613c3d1542d209756b1f3d85ac8631edc4cf7013e104c1426f263aab3d107`.
Il manifest è
`CORREZIONE_RILIEVI_BLOCCANTI_SUCCESSOR_122B_QWEN_D9_03_13.manifest.json`, SHA-256
`a4414fe59a66d6fa00de75b3580f90238b6f2fc21f9c07533785155efff37099`.

Questa consegna non materializza il target reale, non crea authorization e non esegue chiamate
scientifiche.

## P1-02a/b — gate e pubblicazione atomica

Il materializzatore richiede ora entrambi:

```text
--execute --acknowledge MATERIALIZE_PHASE03_122B_SUCCESSOR_OFFLINE
```

Il gate precede qualunque lettura del predecessore o mutazione del target. La costruzione avviene
in una directory privata sorella `.studio2-fase03-d9-pilot-002.staging-*`; soltanto dopo la
validazione completa viene pubblicata con un singolo rename sotto lock. Una failure elimina solo
lo staging verificato e lascia assente il target finale. Un target preesistente viene rifiutato
prima di invocare il builder e viene riconfermato sotto lock prima della pubblicazione.

Per evitare riferimenti durevoli alla directory temporanea, `PilotLedger` distingue il path fisico
SQLite dal suo `identity_path` finale. Package, approval, configurazione e summary conservano i
path pubblicati; durante lo staging i byte effettivi sono validati tramite sorgenti fisiche
esplicite con gli stessi hash. Dopo il rename i riferimenti coincidono con i file pubblicati.

## P2-01 — contratto contabile per evento

`validate_tokenizer_accounting_evidence` non riusa più il guard del chiamante su tutto il ledger.
Per ogni evento:

1. autentica lineage durevole, binding dello stage e identità completa della richiesta;
2. classifica se il contratto no-thinking è richiesto;
3. costruisce il guard esatto per quell'evento;
4. riconteggia e confronta la prova persistita.

Gli eventi technical/producer successor 122B richiedono
`{"enable_thinking": false}`; gli eventi consumer mantengono il template originario senza quella
kwarg. Il resume di un ledger misto non genera più uno STOP globale falso. Acquisizione e prova
persistita continuano a rifiutare il producer senza il controllo esatto.

## P2-02 — recovery idempotente del PASS tecnico

Quando raw, accounting, record e request `COMPLETED` sono già durevoli ma outcome o summary
mancano per crash, il resume:

- rivalida integralmente accounting e record;
- ricostruisce lo stesso summary deterministico dai record dello stage;
- registra idempotentemente lo stesso outcome PASS;
- riscrive atomicamente lo stesso file summary;
- non invoca il transport, non crea intent e non consuma nuova quota.

Lo stesso helper chiude sia il percorso ordinario sia il recovery, eliminando due implementazioni
divergenti del summary.

## Semantica fissata di `identity_sha256`

La scelta non è stata fatta tra tre hash concorrenti in modo arbitrario. La proposta revisionata
nomina espressamente `qualification_supplement_candidate` e ne pubblica il digest canonico. Di
conseguenza `identity_sha256` autentica esclusivamente:

```text
SHA-256(canonical JSON del valore
PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.json["qualification_supplement_candidate"])
= d180061348b15bb0322cb75ae700bb97b1328994c8d572c98741455d5b0ef579
```

Gli altri due valori restano distinti e non vengono rinominati come identità:

- SHA-256 dei byte del file standalone supplemento:
  `dd9c53f0e4262fffe592a04298f8d7a4cfd428ccf5c487faacfe68ca357decb7`;
- SHA-256 del JSON canonico dell'intero documento standalone:
  `79515feb95b1048f67e8c01446be580dcbb73def188a13175b842b58a5356a40`.

Il binding autentica il file proposta (SHA-256 `77d72204…`), la chiave sorgente, l'oggetto
canonico, l'`allowed_identity_update`, i byte del supplemento standalone e il suo digest canonico.
La validazione D9 del servizio successor 122B riesegue questi controlli; una mutazione di uno dei
digest fallisce chiuso.

## Verifiche

| Verifica | Risultato osservato |
|---|---|
| Test finali sul candidato respinto | 28 metodi, 5 failure comportamentali attese, 0 errori, 5,060 s |
| Successor mirata corretta | 28/28 PASS in 4,863 s |
| Discovery package harness | 188/188 PASS in 460,996 s |
| Regressione pertinente esplicita, 15 moduli | 205/205 PASS in 463,089 s |
| `py_compile` dei moduli modificati | PASS |
| Validazione JSON manifest | PASS |
| `git diff --check` | PASS |

I `ResourceWarning` SQLite storici osservati nella suite non sono failure o errori del runner.

## Invarianti e limiti

Non sono cambiati disegno scientifico, quote, ruoli 122B/27B, prompt scientifici, denominatori,
ordine degli stage o decisione autoriale. Il massimo cumulativo resta 166, l'hard stop 200 e il
margine non spendibile 34.

Durante la correzione non sono stati aperti, letti, hashati o modificati ledger e configurazioni
runtime private. `server_enea.json` non è stato letto. Nessun provider, VPN o servizio esterno è
stato contattato: zero token, nessun tunnel, nessuna authorization e nessuna esecuzione
scientifica. Il target fresco reale non è stato creato né materializzato.

Il passo successivo ammesso è una nuova review indipendente sui byte finali. Commit, tree e stato
del candidato sono riportati nell'handoff finale dopo la finalizzazione degli artefatti.
