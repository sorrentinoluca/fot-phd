# Consegna — acquisizione OK e recepimento documentale D9, 03.8

**Studio 2 FoT-TEP · Fase 03 · sottofase 03.8 · 2026-09-15 (Europe/Rome).**
Esito del preparatore: acquisizioni byte-identiche completate; nuovo delta
locale pronto per verifica indipendente, **non autocertificato**. 03.8 e Fase 03
restano aperte. Questa consegna successiva preserva tutti i rapporti improntati.

## Reperimento e catena esatta

- Repository comune: `/Users/luker/fot-tep`.
- Worktree proprietario: `/Users/luker/fot-tep-allineamenti-038-r1-r4`.
- Branch: `codex/studio2-allineamenti-038-r1-r4`.
- Candidato storico verificato R1–R4:
  `9a56d12d0633a0c9790c48792182f26fc6eb424a`, tree
  `e35e5ca661325657715dce6723e4e8ec09540101`.
- Successore storico di consegna: `16f227439357b07b7dc945f67ab5a4368c12b684`.
- **Commit acquisizione OK:** `5b784219b08de1249636536ac98e9a546b4d4577` (verbale + record).
- **Commit acquisizione D9:** `dc4d6560af73579300e33a0a81fc9c3b4316722d` (tre artefatti + record).
- **Nuovo candidato:** `8a20c125bd294191c67ebdbf571832b1e32ac0f1`.
- **Tree candidato:** `f58eedf88d8c9c30767425c945b5ee5c421cf0b7`.
- Base del recepimento: `dc4d6560af73579300e33a0a81fc9c3b4316722d`. Base complessiva per le acquisizioni:
  `16f227439357b07b7dc945f67ab5a4368c12b684`. Fonte D9: `aaba893dff8c62f9f9281eec7423eee020235e03`.

Catena lineare: `4503cb6 → 2520e7a → 1a21fd2 → 9a56d12 → 16f2274 →
5b78421 → dc4d656 → 8a20c12`. Il NON OK e il successivo OK conservano il proprio
perimetro. Il commit che contiene questa consegna e il prompt è il successore
di sola consegna del candidato, identificabile senza autoriferimenti con
`git log -1 --format='%H %T' -- studio2/fase03/piano_statistico/CONSEGNA_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md`.
Non usare quel successore come nuovo candidato documentale da verificare.

## File e impronte di consegna

Il [report del nuovo delta](REPORT_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md) contiene attività, matrice
file→modifica→motivazione→controllo, fonti, limiti e residui.
[Manifest](MANIFEST_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json) e [controlli](CONTROLLI_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json) fissano artefatti e riscontri.
[Prompt indipendente](PROMPT_VERIFICA_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md) pronto per una task distinta.

| Documento nella cartella piano_statistico | Impronta |
| --- | --- |
| REPORT_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md | 10773 byte; SHA-256 `97564d55fa400980b4c0a8106ab8074c226df7d4f0d9d09544956fb7f0856308` |
| MANIFEST_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json | 24446 byte; SHA-256 `bb5e4d9668f9714cead929bb575d44e497823376cda062c1443c0666dadc343a` |
| CONTROLLI_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json | 32478 byte; SHA-256 `2f81b3d9d4da1864a485726f6a10ff9dcf3afd4213580197d0c34a8b795ee897` |
| PROMPT_VERIFICA_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md | 9012 byte; SHA-256 `c0a25d1db83ae49f987a9415d4ed68f4f8f9f3364bf8b83c6e694803d47ae098` |

File del candidato rispetto alla sua base (M modificato, A creato):

```text
M	docs/paper/FoT_TEP_Review_Piano_Sperimentale.md
M	studio2/fase03/APERTURA_SOTTOFASI_FASE03.md
A	studio2/fase03/piano_statistico/CONSEGNA_TECNICA_03_8_D9_PER_03_10.md
A	studio2/fase03/piano_statistico/CONTROLLI_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json
A	studio2/fase03/piano_statistico/MANIFEST_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json
A	studio2/fase03/piano_statistico/MATRICE_RESIDUI_03_8_DOPO_D9.md
A	studio2/fase03/piano_statistico/REPORT_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md
```

Le acquisizioni sono nei commit separati:
- [verbale OK](VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md) e
  [record OK](ACQUISIZIONE_OK_CORREZIONI_ALLINEAMENTI_03_8_REV10.md);
- [record D9](../DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md),
  [consegna/matrice D9](../CONSEGNA_RECEPIMENTO_D9_2026-09-14.md),
  [impronte D9](../IMPRONTE_DECISIONE_D9_2026-09-14.json) e
  [provenienza dell'acquisizione](ACQUISIZIONE_D9_ALLINEAMENTI_03_8.md).

Tutti i percorsi relativi di questa consegna si risolvono sotto
`/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico`. Sorgente del verbale:
`/Users/luker/fot-tep-verifica-correzioni-allineamenti-03-8-rev10/studio2/fase03/piano_statistico/VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`;
sorgenti D9 in `/Users/luker/fot-tep-proposta-d9/studio2/fase03/`, al commit
esatto sopra. I record riportano SHA-256 completi e dimensioni. L'OK acquisito
è 20.816 B, `9248c42572a20388ddf5af976840e68fdc908e545312a63234167778ce53a256`.

## Attività, controlli e limiti

Recepiti stato e provenienza D9 in piano generale/APERTURA; creati successori
espliciti della matrice residui e della consegna tecnica 03.8. Ruoli già
approvati non cambiati: 122B principale e consumer; 27B alternativo con
libreria completa 16 insight; 122B consumer fisso nello swap; Terra solo
storico descrittivo interno, senza nuove chiamate. Il 27B non è un fallback C.
Nessun file del cantiere harness importato o modificato.

- Quattro acquisizioni confermate per byte, dimensioni e SHA-256, contro le
  sorgenti e i blob esatti; due impronte dichiarate nel manifest D9 riscontrate.
- **47 file** preesistenti della cartella statistica preservati a 16f2274;
  **19 artefatti +6 input** rev.10 identici a manifest e blob pinnati. Verbali,
  report e manifest storici intatti, nessun esito cancellato.
- Guardiano documentale prima/dopo: **35 test, 14 fallimenti storici, 1 skip,
  0 errori, exit 1**; identità completa di test e sottocasi: **non PASS**.
  Log grezzi in `/tmp/fot-tep-038-d9/`, non committati; identità e confronto
  persistono nei controlli JSON. Non occorre conservare i log temporanei per
  rigenerare il confronto dal candidato.
- Tredici occorrenze di nuovi link locali del candidato risolte. Un link
  ereditato nel record D9 punta alla proposta non acquisita: è documentato,
  recuperabile da `95ff8571af02bab79094ed1a6be3f6a7b410c711`, preservato per
  byte-identità. Non è presentato come link locale funzionante. Vecchi rinvii
  harness non attestano lo stato del cantiere parallelo.
- Diff/index senza errori di whitespace, JSON validi, sei impronte manifest
  confermate. Nessuna coppia MD/HTML toccata. Controlli della consegna/prompt:
  riferimenti, impronte e diff; nessuna ripetizione del guardiano già eseguito
  sul candidato per i due soli documenti di trasporto.
- Nessun test scientifico o review di sottofasi chiuse; nessuna API, inferenza,
  simulazione, misura sui servizi o produzione di risultati.

La nuova review resta da svolgere. L'OK storico è indipendente dal preparatore
ma nella stessa sessione del precedente NON OK, come dichiarato nel verbale:
non è descritto come nuovo revisore senza contesto o modello diverso.

## Stato Git, integrazione e congelamento

Preflight worktree pulito a 16f2274. Al checkpoint candidato 8a20c12 il worktree
è nuovamente **pulito**, tutti i sette file del delta (incluso il report) e le
sei acquisizioni/record sono committati. Questa consegna e il prompt sono i
soli due nuovi file del commit successivo di consegna. Dopo quel commit lo
stato finale del worktree, controllato a chiusura, è:
**committati tutti i file indicati; modificati 0; non tracciati 0** nel worktree
proprietario. Nessun file temporaneo di controllo è stato inserito nel repo.
Il commit successivo identifica sé stesso tramite il comando sopra.

Origin/main e main remoto osservati ai controlli:
`a00605862f627710347bd63c49f79a6d0a00135f`. Main locale:
`4f98a2973d2e1ca7932f19c34e9dd4c0498b8b43`, non mosso.
Copia principale su `codex/studio2-soglie-normal`, HEAD
`819b12e97fb94d501032655ec2f226139e6c5ca5`, con non tracciati preesistenti:
non effettuati checkout/scritture lì. Le finestre sorgente/revisore/parallele
restano alle rispettive attività; nessuna loro mutazione è operata qui.

**Nuovo candidato solo locale, non integrato o pubblicato.** Nessun push,
merge su main, tag, firma o freeze. I freeze delle altre sottofasi rimangono
intatti; il nuovo delta non li amplia. L'OK D9 futuro non firma materialmente
03.8 e non costituisce GO, ordine label o qualifica.

## Residui e prossimo passo

Cinque stati: ruoli approvati; record acquisito; recepimento documentale locale
preparato; recepimento eseguibile harness pendente; identità/configurazioni,
qualificazioni e fattibilità ancora da documentare/misurare. **Ordine label
1a non approvato**, firma materiale 03.8 e autorizzazioni alle chiamate/pilot
restano atti separati. Dettagli `a`, riusi, X/Q, quartetto swap, calendario e
qualifiche non vengono dedotti dai ruoli: rintracciare le decisioni già
registrate; solo per scelte effettivamente mancanti e necessarie il passo
successivo deve indicare fonte e conseguenza all'autore. Nessuna nuova scelta
serve per consegnare questo recepimento.

Prossimo passo per l'orchestratrice: affidare il prompt alla review indipendente
**delle acquisizioni e del solo nuovo delta D9**, al candidato esatto, poi
acquisire il nuovo verbale. Preservare l'OK storico senza ripeterlo o estenderlo.
Harness R01–R10, raccordo paper 03.15 e walkthrough sono passi distinti.
A/B, FAR, U3, 03.5, 03.9 e 03.12 non si riaprono. Integrazione/pubblicazione,
firma e freeze richiederanno i propri passaggi effettivi. Nessuna dipendenza
circolare: freeze statistico → 03.11/OOD → chiamate dopo T5 e altri GO.
