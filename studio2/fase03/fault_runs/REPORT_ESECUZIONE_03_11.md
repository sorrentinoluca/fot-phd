# Rapporto unico — esecuzione sotto-fase 03.11

Data: 2026-09-15. Esito: **STOP prespecificato prima del batch — sostituto OOD non
risolto dalle prove autorizzate**. La Fase 03 resta aperta.

## Esito e conteggi

Il worktree dedicato parte da `origin/main` `15e56a89b0f377e6d90eef28ed941d4d54b5b00c`.
La specifica e i due identificativi del preflight sono stati congelati prima delle simulazioni
nel commit `3618e424748fe02d745f09542ce15d30da032492`, tree
`28e87bbd346e3ffa614626b2f2a7db8c7fa878bf`.

Sono state eseguite **2 sonde tecniche OOD**, zero run del lotto finale e zero chiamate a
Qwen o ad altri modelli:

| Sonda | Stream | Stato | Fine | Trip | Finestre complete | Ammissibile |
| --- | ---: | --- | ---: | --- | ---: | :---: |
| F6 | 70000 | `physical_trip` | 32,1095 h | codice 8 a 32,1095 h | 1/8 | no |
| F4 | 70001 | `complete` | 65 h | nessuno | 8/8 | si |

Il batch prespecificato resta **0/89**: 0/72 primari, 0/6 OOD, 0/11 scorte.
Il trip di F6 attiva la catena congelata `F6→F5→F12`. Il membro successivo e F5, ma
`DECISIONI_AUTORE_03_8_bozza.md` registra esplicitamente che per F5/F11/F12 manca un numero
di rilevabilita riverificato e vieta l'uso del sostituto prima della propria verifica.
Non esiste nel worktree un record approvato per F5. La regola non risolve quindi il caso e
impone lo stop senza promozione automatica.

## Preflight, audit e sigillo

- piano: `plans/ood_preflight_03_11.csv`, 2 righe, SHA-256
  `876a05f22c40662685c541fb522ffdb3117f9499adaef1a4d630a3436083ad3f`;
- MATLAB: R2025b Update 6 arm64 (`MACA64`); MEX qualificato
  `834e2361915249402a1ec9074a4be04f22a6404deb841e5134bf34347dfde544`;
- audit: `PREFLIGHT_AUDIT_03_11.json`, esito `BLOCKED_UNRESOLVED_SUBSTITUTE`;
- sigillo: `SIGILLO_PREFLIGHT_03_11.json`;
- lotto locale: `studio2/fase03/fault_runs/ood_preflight/ood_preflight_001`;
- archivio locale: `ood_preflight/ood_preflight_001.tar`, 7.426.560 byte, SHA-256
  `16acf7c1e18923b606a47fe3fb0efaa83b99e8ee19024f11f4d8f3fd675929df`.

L'audit generico ha verificato 2/2 manifest e tutti gli hash: 1 completo, 1 trip fisico,
0 errori tecnici, 0 non eseguiti. Il suo `accepted=true` significa soltanto che il trip e
correttamente conservato e tracciato; il gate specifico OOD resta bloccato.

L'archivio e presente nel worktree ma non e pubblicato su `fot-tep-data`; la recuperabilita
esterna resta quindi un'anomalia aperta, non una consegna definitiva del dato voluminoso.

## Verifica e documentazione

I test del generatore e del protocollo sono **23/23 PASS**. Il guardiano documentale parte da
35 test, 14 fallimenti e 1 skipped, tutti preesistenti; viene rieseguito alla chiusura.
Non e stata prodotta una verifica indipendente in un'altra finestra. Per questo non si aggiorna
il walkthrough e non si dichiara chiusa la sotto-fase. Questo rapporto registra un arresto
operativo, non un risultato scientifico e non un OK indipendente.

Profilo eseguito: **esecutivo-batch**, Codex nella finestra corrente. Preflight, batch, audit e
sigillo sono rimasti distinti: il batch non e stato aperto dopo il fallimento del gate.

## File toccati e decisione di commit

Sono toccati soltanto i file 03.11 sotto `studio2/fase03/fault_runs/` e le estensioni additive
del generatore qualificato necessarie alla nuova classe `ood_preflight`. Gli output voluminosi
e il runtime restano ignorati e fuori dal commit; audit, sigillo, piano, specifica, launcher,
test e questo rapporto entrano nel commit esplicito proposto:

`studio2(test-run): registra stop OOD 03.11 prima del batch`

Restano fuori: il lotto finale 89, il sostituto F5, qualunque feature/evidence, qualunque
chiamata modello, il paper, il walkthrough, tag, push, merge e guardian estranei.
