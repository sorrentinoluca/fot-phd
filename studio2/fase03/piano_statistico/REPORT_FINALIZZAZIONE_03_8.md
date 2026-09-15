# Report del candidato locale di finalizzazione — 03.8

Data: 2026-09-15. Stato: **candidato locale, non ancora verificato,
pubblicato o congelato**. La sotto-fase 03.8 è in finalizzazione locale e la
Fase 03 resta aperta.

## Esito della preparazione

È stata ricostruita sul Git reale una catena lineare di 20 commit fra il main
remoto osservato `a00605862f627710347bd63c49f79a6d0a00135f` e l'acquisizione
`6490af4889fd679d491f63b9debdf2314eaf7aca`. Su quella punta è stato preparato
il solo raccordo ancora necessario: stato corrente, walkthrough 03.8 in coppia
MD/HTML e manifest candidato non efficace.

Il commit e il tree esatti del candidato sono registrati nella successiva
`CONSEGNA_FINALIZZAZIONE_03_8.md`, così questo report e il manifest non devono
contenere il proprio hash. Il worktree preparatore, `main` locale e i worktree
paralleli non sono stati modificati.

## Catena inclusa

I checkpoint sostanziali, tutti raggiungibili dalla punta di acquisizione, sono:

| Ambito | Candidato o sorgente | Acquisizione / successore | Stato |
| --- | --- | --- | --- |
| rev.10 | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` | consegna `51782e8`; verbale rev.10 nella catena | OK nel proprio perimetro |
| correzioni R1–R4 | `9a56d12d0633a0c9790c48792182f26fc6eb424a` | `5b784219b08de1249636536ac98e9a546b4d4577` | OK acquisito |
| record D9 | sorgente `aaba893dff8c62f9f9281eec7423eee020235e03` | `dc4d6560af73579300e33a0a81fc9c3b4316722d` | acquisito byte-identico |
| recepimento documentale D9 | `8a20c125bd294191c67ebdbf571832b1e32ac0f1` | `8a3f7ba706570201c5b622c4e0fc79529b1c8cfd` | OK acquisito |
| pacchetto firma storico | `7cf523805710633ec3b4fecd4eb8b7c9504076bf` | `2af85459a14b9d9b567c6a0234154968b4d585d0` | OK storico; non più operativo |
| approvazione documentata | `270bd2bb0c5f9ff4541d709052cdf144142b1d88`, tree `0cf2a5656059fb6d5521062227095c0eeede0f92` | prompt `85a89da`; acquisizione `6490af4` | OK sul solo delta `2af8545..270bd2b` |

La sequenza completa con ogni genitore è nel
[`MANIFEST_CANDIDATO_FREEZE_03_8.json`](MANIFEST_CANDIDATO_FREEZE_03_8.json).
I verdetti restano separati: nessun OK precedente è esteso al presente delta.

## Delta effettivo

Il candidato modifica soltanto:

- `docs/fot_walkthrough_conversazione_studio2.md` e `.html`, insieme: nuova
  §4.8, navigazione, sintesi e raccordo §6.6;
- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`: stato dell'approvazione
  documentata e della finalizzazione;
- `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`: 03.8 in finalizzazione locale;
- `COORDINAMENTO_CHIUSURA_03_8.md`: sequenza corrente review → acquisizione →
  pubblicazione → manifest efficace → tag;
- `MATRICE_RESIDUI_03_8_DOPO_D9.md`: residui reali dopo gli OK acquisiti;
- il presente report e il nuovo manifest candidato.

Non modifica harness, configurazioni, `paper_sections/`, walkthrough divulgativo,
artefatti congelati, codice scientifico, decisioni, verbali o acquisizioni.

## Preservazione e fonti

Dieci fonti sensibili confrontate per blob con la base `6490af4` sono
byte-identiche: piano rev.10, manifest storico, `DELTA_HARNESS_03_10.md`, coppia
`DESIGN_RESOLUTION`, decisione sull'approvazione documentata e i quattro verbali
rev.10/R1–R4/D9/approvazione documentata. Il piano conserva 81.490 byte e
SHA-256 `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`;
il manifest storico conserva 25.894 byte e SHA-256
`a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`.

Le fonti D9 e tutte le prove necessarie sono tracciate nella storia candidata;
non esiste una dipendenza operativa da `/tmp` o da un altro worktree. Non esiste
`DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.*`: l'approvazione documentata è
sufficiente e il pacchetto firma rimane soltanto storico.

## Manifest candidato

`MANIFEST_CANDIDATO_FREEZE_03_8.json` misura **12.382 byte** e ha SHA-256
`bcc9ef183190e2fd0997b2e600fc53498e4a6194993e997820255a4b6d124dc6`.
Le sue 23 voci di artefatto coincidono per percorso, dimensione e SHA-256; la
catena di 20 commit coincide con i genitori Git. Il manifest esclude se stesso,
questo report, la consegna, il prompt e i futuri record, evitando riferimenti
autoreferenziali.

Lo stato è deliberatamente `freeze_effective=false`. `candidate_commit`,
`candidate_tree`, `published_commit`, `target_commit`, `tag_object` e
`peeled_commit` non sono inventati: i primi due saranno nel record successore;
gli altri dipendono da review acquisita, pubblicazione e tag reali.

## Controlli offline

- JSON del manifest valido; 23/23 impronte conformi.
- Catena Git: 20/20 genitori lineari; `origin/main` è antenato della base e la
  divergenza osservata è 20 avanti, 0 indietro.
- `git diff --check`: pulito.
- Link e anchor nuovi: 17 controlli, 0 errori; il test mirato
  `test_valid_markup_links_and_unique_anchors` è OK.
- §4.8 MD/HTML: testo normalizzato identico; coppia aggiornata insieme.
- Guardiano completo sulla base e sul candidato: **NON PASS** in entrambi, 35
  test, 14 fallimenti storici e 1 skip; i 14 identificativi e sottocasi sono
  identici, senza regressioni. Questo non viene definito PASS.
- Tag remoto previsto: assente, coerentemente con lo stato non congelato.
- File sottoscritto: assente, come richiesto dalla decisione dell'autore.

Nessun audit scientifico concluso è stato ripetuto e nessun servizio, inferenza,
simulazione, pilot o run finale è stato eseguito.

## Residui e sequenza proposta

1. Sottoporre a revisore indipendente il commit candidato esatto indicato nella
   consegna, contro la base `6490af4`.
2. Se il verdetto è OK, acquisirlo byte-identico in un commit documentale
   separato, senza estenderlo alla consegna o all'acquisizione.
3. Prima della pubblicazione, ricontrollare `origin/main`. Se non è più la base
   osservata, integrare sul contenuto corrente, risolvere solo conflitti reali e
   far verificare qualunque nuovo byte; quindi pubblicare soltanto con
   autorizzazione esplicita.
4. Verificare che la catena e il candidato siano raggiungibili da
   `refs/remotes/origin/main` dopo il push autorizzato.
5. Preparare il manifest efficace come delta separato, sostituendo solo i campi
   determinabili dagli eventi reali e mantenendo una condizione di efficacia
   esterna; sottoporlo a review se introduce nuovi byte normativi.
6. Dopo pubblicazione e acquisizione dell'ultimo verdetto applicabile, creare il
   tag annotato `studio2-fase03-piano-statistico-frozen-001` sul commit finale
   allora identificato, pubblicarlo soltanto con autorizzazione e verificare sul
   remoto sia l'oggetto tag sia il `^{}` peeled uguale al target previsto.
7. Registrare commit pubblicato, oggetto tag e peeled in un record successore,
   senza riscrivere manifest o verbali storici.

Restano separati e non bloccano circolarmente il tag statistico: ordine label
1a, correzioni e qualifica del runtime harness D9, identità/configurazioni dei
servizi, T5, pilot e controlli OOD 03.11. Il candidato harness `6a8031b` resta
NON OK per R-D9-01/R-D9-02 e non è stato importato.

Nessun push, merge su `main`, tag, firma, pubblicazione o esecuzione è stato
effettuato. Questo report non dichiara un OK indipendente.
