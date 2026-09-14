# Consegna del nuovo candidato — correzioni R1–R4, 03.8 rev.10

Data: **2026-09-15**, Europe/Rome. **Preparazione locale completata; review
indipendente pending.** 03.8 e Fase 03 rimangono aperte.

| Oggetto | Identità esatta |
| --- | --- |
| Worktree | `/Users/luker/fot-tep-allineamenti-038-r1-r4` |
| Branch | `codex/studio2-allineamenti-038-r1-r4` |
| Base pubblicata osservata, origin/main e main remoto | `a00605862f627710347bd63c49f79a6d0a00135f` |
| Consegna precedente | `2520e7abc1cd68785f2789448b509dea5e55ee7d` |
| Commit documentale di acquisizione NON OK | `1a21fd260ad2df6a3b04ffb6fa5e2d642a3f63b1` |
| **Candidato corretto** | **`9a56d12d0633a0c9790c48792182f26fc6eb424a`** |
| **Tree candidato** | **`e35e5ca661325657715dce6723e4e8ec09540101`** |
| Diff da verificare | `1a21fd260ad2df6a3b04ffb6fa5e2d642a3f63b1..9a56d12d0633a0c9790c48792182f26fc6eb424a` |

La catena è lineare: candidato NON OK 4503cb6 → consegna 2520e7a → acquisizione
1a21fd2 → correzione 9a56d12 → commit documentale contenente questa consegna
 e il prompt. L'ultimo non cambia il tree normativo candidato e non ne è la base.

## Artefatti consegnati

- Report e matrice R1–R4: [REPORT_CORREZIONI_ALLINEAMENTI_03_8_REV10.md](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/REPORT_CORREZIONI_ALLINEAMENTI_03_8_REV10.md).
- Manifest del nuovo delta: [MANIFEST_CORREZIONI_ALLINEAMENTI_03_8_REV10.json](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/MANIFEST_CORREZIONI_ALLINEAMENTI_03_8_REV10.json).
- Controlli e subtest: [CONTROLLI_CORREZIONI_ALLINEAMENTI_03_8_REV10.json](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/CONTROLLI_CORREZIONI_ALLINEAMENTI_03_8_REV10.json).
- Prompt per la nuova task: [PROMPT_VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/PROMPT_VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md).
- Verbale NON OK acquisito: [VERIFICA_ALLINEAMENTI_03_8_REV10.md](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/VERIFICA_ALLINEAMENTI_03_8_REV10.md).
- Record di acquisizione: [ACQUISIZIONE_NON_OK_ALLINEAMENTI_03_8_REV10.md](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/ACQUISIZIONE_NON_OK_ALLINEAMENTI_03_8_REV10.md).
- OK statistico storico preservato: [VERIFICA_PIANO_STATISTICO_REV10.md](/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/VERIFICA_PIANO_STATISTICO_REV10.md).

| Artefatto | Byte | SHA-256 |
| --- | ---: | --- |
| `REPORT_CORREZIONI_ALLINEAMENTI_03_8_REV10.md` | 12419 | `19d69fc5cb2d3deee514044ccb47e1e9b61eab2df996c0834e4594d03ac23dc4` |
| `MANIFEST_CORREZIONI_ALLINEAMENTI_03_8_REV10.json` | 10112 | `d422279aa15c94cbafe5afb0a1b61fb105967804709762d7942a9cef53b55303` |
| `CONTROLLI_CORREZIONI_ALLINEAMENTI_03_8_REV10.json` | 36542 | `deedf2961ba4a4d1a4a460fc32dff80c54d64208e9b8b8338308920c9a8db93e` |
| `PROMPT_VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md` | 8674 | `1c51a17295c0a3038b7183e75bdda542daa26d4c8d73769c6b404d9cebcff23d` |
| `VERIFICA_ALLINEAMENTI_03_8_REV10.md` | 22063 | `52944646527d0e73d6508ae53669f47f5e8661050ff777c75a448ca535ca9c13` |

## Commit separati e stato Git

1. Acquisizione: due file nuovi, verbale NON OK byte-identico e provenienza.
2. Correzione: due file normativi modificati (piano generale e APERTURA), cinque
   nuovi (report, manifest, controlli JSON, log prima/dopo). Nessun altro file.
3. Consegna: questo record e il prompt indipendente, in commit soltanto documentale.

Dopo il commit di consegna, questi file sono tutti tracciati e committati,
inclusi report e consegna; nessun modificato, staged o non tracciato residuo nel
worktree di preparazione. Il commit finale di consegna è quello contenente
questo documento, successore diretto del candidato; il suo hash è comunicato
all'orchestratore senza introdurre un autoriferimento nel file.
Copia principale, worktree di chiusura, review precedente e finestre parallele
sono preservati. Gli script temporanei di preparazione restano fuori Git in
`/tmp/fot-tep-038-r1-r4`; ogni prova necessaria alla review è committata nel pacchetto.

## Controlli e limiti

Guardiano prima/dopo: **35 test, 14 fallimenti storici, 1 skip, 0 errori,
exit 1**, stessi identificativi e subtest; **non PASS**. I log conservano
stdout+stderr con tre spazi finali rimossi per file; originali ricostruibili
tramite righe e impronte nel JSON. Diff completo `--check` pulito, 6/6 link
locali risolti nel candidato, conti 1.728/5.184, 148/444 e 72+6+11=89 verificati.
27 fonti pinnate, 6/6 file nel nuovo manifest. 38/38 file statistici preesistenti
e 19+6 elementi del manifest rev.10 byte-identici. Nessuna suite statistica,
review bibliografica, simulazione, inferenza o API sperimentale rieseguita.

## Stato effettivo e passaggio all'orchestratore

Nessun push, merge su main o tag. Il candidato non è integrato/pubblicato.
Nessuna firma sostitutiva e nessun freeze statistico efficace. Il tag statistico
previsto non risulta presente nella query remota. Gli stati chiusi 03.5/03.9 e
R4 pubblicata sono preservati, senza riaprire A/B, FAR o U3.

Ruoli approvati dal mandato: **122B principale/consumer, 27B alternativo con
16 insight, consumer 122B fisso nello swap**. Terra è soltanto storico descrittivo
interno, separato dalle nuove stime. Registro formale ancora in acquisizione
nell'altra finestra, non importato; qualificazioni tecniche, ordine label e
firma materiale sono distinti. Nessuna nuova scelta dei ruoli è richiesta.

**Prossimo passo:** eseguire il prompt in una nuova task indipendente, su copia
isolata del candidato esatto, e acquisire poi il verbale byte-identico. Non
ripetere la vecchia review o l'OK statistico. Dopo un nuovo OK, coordinare firma
materiale, walkthrough/documentazione e integrazione seriale autorizzata sul
main effettivo, riverificando ogni ulteriore raccordo. Harness e registro D9
restano cantieri separati. Freeze statistico prima dei run 03.11; controlli OOD
dopo freeze e prima delle chiamate, con tutti gli altri GO e T5 misurato.
Se T5 non è fattibile o le catene OOD convergono su F5/caso irrisolto, sospendere
per decisione esplicita dell'autore secondo la rev.10, senza fallback automatici.
