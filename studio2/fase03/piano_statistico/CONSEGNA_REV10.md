# Consegna della revisione 10 — record esterno al candidato

Data: 14 settembre 2026. Questo record è successivo al candidato e ne identifica
l'esatto contenuto senza modificarne il manifest dopo la verifica.

## Decisioni e candidato

Luca ha approvato senza modifiche A/B dell'addendum al commit
`526561feabeb6b4083170b1817b8abdac1a2a4c7`, il **14 settembre 2026**.
Il record di approvazione è nel commit
`f37e7e00cbdd959ef6fdb7cc96ce42ed521075d6`.

- Candidato rev. 10: `6aaa5b3eebfed4ba502c25c0443caabd0051af21`.
- Tree candidato: `24847ce0cc4ff7b6defea4d65f3f41cb9ccd1c1a`.
- Manifest: `PIANO_STATISTICO_FREEZE.json`, SHA-256
  `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`.
- Piano SHA-256: `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`.
- Copia isolata del revisore: `/Users/luker/fot-tep-verifica-piano-statistico-rev10`,
  detached HEAD sul candidato.

## Verifica indipendente

**OK — recepimento A/B della revisione 10, nessun rilievo bloccante.**
Revisore: **gpt-5.6-sol**, sessione agent `/root/revisore_rev10`, distinta dal
preparatore Codex GPT-6 entro la stessa task utente; copia detached isolata.
Verbale [VERIFICA_PIANO_STATISTICO_REV10.md](VERIFICA_PIANO_STATISTICO_REV10.md),
acquisito byte per byte, **12.478 byte**, SHA-256
`d269e26d8cb4e23370577e1e193d90d9357d66f7c739e9d0669970edf71b0066`.

La verifica comprende l'intero delta baseline→candidato, 19+6 impronte correnti,
catene storiche, invarianti, conti e ordine OOD; **26/26 test statistici OK**,
35 test documentali con gli stessi 14 fallimenti preesistenti e 1 skip.
L'OK non certifica firma materiale, freeze, chiusura o autorizzazione di esecuzione.

Il manifest e il report candidati conservano lo stato di review pending che
avevano al momento della consegna: questo record e il verbale successivo
registrano l'esito senza cambiare gli hash del candidato. Una modifica successiva
al candidato non eredita automaticamente tale esito.

## Residui e passaggio alle finestre successive

| Requisito | Prova | Stato corrente |
| --- | --- | --- |
| Approvazioni A/B | record Luca e commit f37e7e0 | completato |
| Recepimento rev. 10 | candidato 6aaa5b3 e manifest identificato sopra | completato |
| Firma materiale | atto rev. 10 predisposto con hash del piano; copia firmata assente | pending |
| Congelamento statistico | §16.1: firma, regole allineate, bibliografia, documentazione/integrazione e tag | pending |
| Fattibilità T5/D9 | regola A recepita, misure/configurazione/calendario ancora da verificare | pending operativo |
| OOD tecnici | regola B recepita; esiti 03.11 dopo freeze e prima delle chiamate ancora assenti | pending operativo |
| Harness 03.10 | delta preciso predisposto, implementazione nella finestra proprietaria | pending prima del pilot |
| Bibliografia/PNG | candidato identificato; acquisizione seriale e conservazione da completare | pending |
| origin/main/tag | nessuna pubblicazione effettuata | pending |

Per gli allineamenti, applicare al target corrente le formulazioni di
`COORDINAMENTO_CHIUSURA_03_8.md` con A/B **approvate**, senza nuove richieste su
quelle decisioni. Fonte delle regole: piano rev. 10 e relativo allegato contabile;
`DELTA_HARNESS_03_10.md` resta specifica per il solo worktree proprietario.
Nessuna scrittura simultanea ai branch delle altre finestre.

Dopo l'OK del recepimento, la documentazione 03.8 è predisposta dal report corrente
(secondo la sequenza Documentazione_LLM: riassunto, dettaglio, letteratura,
critiche/limiti, artefatti). Quando la finestra coordinata aggiornerà la coppia
walkthrough MD/HTML, dovrà indicare distintamente approvazioni, recepimento,
verifica, firma e freeze e dichiarare la Fase 03 ancora aperta. Il contenuto non
va presentato come piano già congelato o pubblicato; la sintesi divulgativa non
richiede una voce per questo passaggio interno. Ogni ulteriore delta derivante
da integrazioni o risoluzione di conflitti va verificato prima del tag finale.

Il tag previsto resta `studio2-fase03-piano-statistico-frozen-001`, non creato.
Nessun push, merge, simulazione, inferenza, scelta D9 o modifica 03.5.
