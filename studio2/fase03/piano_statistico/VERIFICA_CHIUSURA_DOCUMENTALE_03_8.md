# Verifica indipendente della chiusura documentale 03.8 — **OK**

**Verdetto: OK**, limitato al delta esatto
`2edd4550cabfd065fafa1834609e9789149611ee..b2184360e6b857fd6f9e8c25903dbd428735ccf5`.
L'OK non si estende a questo prompt, al presente verbale, a future acquisizioni
o a nuovi byte.

## Modello, ambiente e ruolo

- Revisore: **Claude, modello configurato `claude-opus-4-8`, provider Anthropic**
  (l'identità del modello suggerita dal prompt, `gpt-6-astra`, non si applica e
  non viene attestata). Reasoning/effort effettivo non separatamente attestabile:
  non dichiarato come dato certo.
- Ambiente: sessione Cowork (app desktop Claude) collegata al dispositivo
  `macbook-pro-local`; lavoro eseguito via shell locale sul repository
  dell'utente. Finestra distinta da quella preparatrice.
- Ruolo: revisore indipendente, sola lettura del solo candidato di chiusura
  documentale 03.8. Nessun commit, push, merge, tag, firma, chiamata ai
  servizi, inferenza, simulazione, pilot o run è stato eseguito. Il tag non è
  stato modificato. La Fase 03 non è stata dichiarata chiusa.

## Identità Git e copia isolata

- Repository: `/Users/luker/fot-tep`; remoto `origin` =
  `https://github.com/sorrentinoluca/fot-phd.git`.
- `origin/main` = `2edd4550cabfd065fafa1834609e9789149611ee` = **base pubblicata
  attesa** (coincidono).
- Candidato `b2184360e6b857fd6f9e8c25903dbd428735ccf5` (tipo commit); tree
  `a976d5d6c0a7d75d4f37b58be7b76ede5ed29c5d` (= atteso); **genitore unico**
  `2edd4550cabfd065fafa1834609e9789149611ee` (= atteso).
- Branch preparatore `codex/studio2-chiusura-documentale-038` =
  `41dbe1df044fcc11c5074b54764748010a42e571`: un solo commit successore
  ("prepara review chiusura 03.8") sopra il candidato, che ne è antenato.
  Coerente con la nota del prompt secondo cui il prompt di review è un
  successore documentale esterno al candidato. Non incide sul perimetro.
- Verifica condotta su copia isolata **detached** del candidato (worktree
  indipendente creato da questa finestra), stato pulito; copia detached
  separata sulla base per il confronto del guardiano. La copia principale è su
  altro branch (`codex/studio2-soglie-normal`) e non è stata toccata.

## Perimetro e impronte — esatti

Delta = esattamente cinque file; diffstat **184 inserimenti, 55 rimozioni**;
nessun piano, manifest, verbale, acquisizione, record certificato, harness,
configurazione o risultato modificato.

| Stato | File | Byte | SHA-256 | Esito |
| --- | --- | ---: | --- | :---: |
| M | `docs/fot_walkthrough_conversazione_studio2.html` | 144.132 | `8509…b148` | ✅ |
| M | `docs/fot_walkthrough_conversazione_studio2.md` | 117.940 | `e625…c705` | ✅ |
| M | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | 175.642 | `d3ca…f902` | ✅ |
| M | `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` | 13.716 | `11c1…4a1c` | ✅ |
| A | `studio2/fase03/piano_statistico/CHIUSURA_DOCUMENTALE_03_8.md` | 4.632 | `81bf…d2d5` | ✅ |

Byte e SHA-256 coincidono con la tabella del prompt per tutti e cinque i file.
Ripartizione per-file: html 40/22, md 40/22, paper 18/8, APERTURA 16/3,
CHIUSURA 70/0 (nuovo).

## Controlli richiesti

1. **Identità, perimetro, impronte** — verificati (sopra). ✅
2. **Record nuovo e diff dei quattro documenti** — letti integralmente. Le
   affermazioni sono sostenute dalle fonti pubblicate: piano rev.10, manifest
   pre-tag, prova/record post-tag, verbale OK e acquisizione hanno i byte e le
   impronte pubblicati (punto 9). Le impronte citate nei documenti (manifest
   pre-tag `087d268d…`, tag oggetto `bfcf6e5b…`, peeled `11f504b2…`)
   corrispondono. ✅
3. **Distinzione temporale** — i flag `record_verified=false`,
   `record_published=false`, `subphase_03_8_closed=false` (e
   `phase_03_closed=false`) restano byte storici nei file non modificati
   (`PROVA_REMOTA_FREEZE_…json`, `MANIFEST_FINALE_PRE_TAG_03_8.json`,
   `CONSEGNA_*`, `VERIFICA_*`), tutti invariati base→candidato. Il nuovo record
   e i walkthrough li descrivono come fotografie storiche non riscritte; verbale,
   acquisizione e raggiungibilità da `origin/main` provano gli eventi
   successivi. Nessuna riscrittura retroattiva. ✅
4. **Chiusura solo documentale** — 03.8 è dichiarata "chiusa nel candidato
   documentale"; la dichiarazione richiede ancora review indipendente,
   acquisizione e pubblicazione. La Fase 03 è esplicitamente aperta in tutti i
   documenti toccati. ✅
5. **Approvazione dell'autore** — resta sufficiente
   (`DECISIONE_AUTORE_APPROVAZIONE_DOCUMENTATA_03_8_2026-09-15.md`, presente e
   invariato); nessuna firma materiale reintrodotta ("nessuna firma materiale"
   ribadito nei diff; nessun nuovo requisito di sottoscrizione). ✅
6. **Decisioni non riaperte** — A/B, D2=8, D11={F1,F2}/{F14,F15}, m=0,125,
   alpha, gerarchia, politica R e ruoli D9 non sono riaperti. L'ordine label 1a
   è dichiarato decisione D9 separata che **non** autorizza esecuzioni
   ("non autorizzati da questa chiusura"). ✅
7. **Semantica operativa** — conteggio completo e `1,20 × T ≤ W` vigenti; 3.700
   solo tetto storico; controlli OOD in 03.11 dopo il freeze e prima delle
   chiamate; nessun ciclo 03.8→03.11→03.8 (dipendenza circolare esplicitamente
   negata). ✅
8. **Parità coppia walkthrough MD/HTML** — parità sostanziale sui sette blocchi
   modificati: stesso testo, stesse impronte, stessi link e ancore. Le dodici
   ancore referenziate esistono in entrambi i file; i dieci target di link in
   `piano_statistico/` risolvono. `git diff --check` pulito. ✅
9. **Byte/impronte già pubblicati** — verificati sui blob del candidato
   (invariati rispetto alla base):
   - `PIANO_STATISTICO.md` = 81.490 byte, `675dbbcc…d032a` ✅
   - `MANIFEST_FINALE_PRE_TAG_03_8.json` = 14.768 byte, `087d268d…c1413d` ✅
   - `PIANO_STATISTICO_FREEZE.json` (manifest storico) = `a69c4f68…f80f8` ✅
   - `PROVA_REMOTA_FREEZE_…json` = 6.773 byte, `2c011bba…a44f97` ✅
   - `VERIFICA_RECORD_EFFICACIA_FREEZE_03_8.md` = 6.850 byte, `e34b791e…c4229` ✅
   - `ACQUISIZIONE_OK_RECORD_EFFICACIA_FREEZE_03_8.md` = `7c5d6510…9dd838` ✅
10. **Tag annotato** `studio2-fase03-piano-statistico-frozen-001` invariato:
    tipo `tag`; oggetto `bfcf6e5b3840c5b7dc3f7ace1085843d18cfddc7` (= atteso);
    peeled `11f504b2bf45a39c1bc4746952f50d58c5022743` (= atteso). ✅
11. **Antenati esclusi** — `7c37ee64da86fab1452f69ca50721ec2af01bf7f` e
    `f944efd2872786d439c22b38302d33e91d08cfab` **non** sono antenati del
    candidato. ✅
12. **Guardiano storico** — `git diff --check` pulito; `python3
    docs/test_explanation.py`: **NON PASS**, `Ran 35 tests`,
    `FAILED (failures=14, skipped=1)`, 0 errori (exit 1). Gli identificativi e i
    sottocasi dei 14 fallimenti sono **identici** a quelli della base (tutti
    `UnifiedConversationChecks` sui walkthrough del primo studio:
    `test_condition_c_contract_and_caveats`,
    `test_one_flow_and_ordered_step_headings`,
    `test_step27_qwen_frozen_results_and_limitations`,
    `test_step27_qwen_protocol_stable_facts`); skip = "legacy part-1 walkthrough
    is not present in this checkout". Il candidato **non introduce nuovi
    fallimenti**. Non è PASS e non sono state sommate suite sovrapposte. ✅

## Limiti del guardiano

Il guardiano resta un controllo storico **NON PASS**: i 14 fallimenti sono
preesistenti e relativi ai walkthrough del primo studio (v1), come documentato
in `docs/MAINTENANCE.md` §5 (14 fallimenti al 2026-09-11). Non attesta la
correttezza scientifica del contenuto studio2; attesta soltanto che il candidato
non peggiora lo stato del guardiano rispetto alla base. Confronto effettuato per
identificativo e sottocaso, non per soli totali.

## Osservazioni non bloccanti

- Il branch preparatore punta a un commit successore (`41dbe1d`) che aggiunge il
  prompt di review; il candidato ne è antenato. Coerente con il prompt; nessun
  impatto sul perimetro.
- La registrazione dei due worktree di verifica ha scritto metadati sotto
  `.git/worktrees/` del repository (inevitabile con `git worktree`); non è stato
  modificato alcun contenuto tracciato, ref, tree o commit. I lock non sono stati
  toccati; eventuale `git worktree prune` è a discrezione dell'autore.

## Passo successivo

L'OK abilita l'acquisizione byte-identica di questo verbale e, solo dopo, una
pubblicazione non forzata del solo delta di chiusura. Il tag esistente resta
invariato; la Fase 03 resta aperta.
