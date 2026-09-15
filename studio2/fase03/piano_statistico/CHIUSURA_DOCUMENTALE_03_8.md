# Chiusura documentale della sotto-fase 03.8

Data: 2026-09-15. Stato: **candidato locale di chiusura, da sottoporre a
verifica indipendente**.

## Dichiarazione e perimetro

Alla base pubblicata `2edd4550cabfd065fafa1834609e9789149611ee` sono
completati i requisiti documentali e di congelamento del piano statistico 03.8.
Il presente delta può quindi dichiarare **chiusa la sotto-fase 03.8**, senza
dichiarare chiusa la Fase 03.

La dichiarazione diventa parte dello stato pubblico soltanto dopo verifica
indipendente del candidato esatto, acquisizione del relativo verbale e
pubblicazione autorizzata. Non modifica il freeze già efficace, il commit
taggato o il tag annotato.

## Matrice requisito/prova/stato

| Requisito | Prova pubblicata | Stato |
| --- | --- | :---: |
| Piano statistico rev.10 definito e verificato | `PIANO_STATISTICO.md`, 81.490 byte, SHA-256 `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`; verifica rev.10 e successive verifiche circoscritte | ✅ |
| Decisioni A/B, D2, D11, margine, alpha, gerarchia e politica R | piano rev.10 e record dell'approvazione documentata dell'autore | ✅ |
| Approvazione dell'autore sufficiente, senza firma materiale | `DECISIONE_AUTORE_APPROVAZIONE_DOCUMENTATA_03_8_2026-09-15.md`; relativo OK acquisito e pubblicato nella catena | ✅ |
| Ruoli D9 recepiti senza riaprire la decisione | record D9 e relativo recepimento documentale con OK acquisito | ✅ |
| Finalizzazione documentale verificata e pubblicata | candidato `4c9e7a1f1d8bd07b7d6be8df724f743986717da8`; OK acquisito nel successore `8dbd2b49176c16f9e100e5f181c729b99d406a35` | ✅ |
| Manifest finale pre-tag verificato | `MANIFEST_FINALE_PRE_TAG_03_8.json`, 14.768 byte, SHA-256 `087d268d438ca6e98063346a5547849a05235a43712aebe56e007c46dcc1413d`; catena pubblicata fino a `11f504b2bf45a39c1bc4746952f50d58c5022743` | ✅ |
| Freeze statistico efficace | tag annotato `studio2-fase03-piano-statistico-frozen-001`; oggetto `bfcf6e5b3840c5b7dc3f7ace1085843d18cfddc7`; peeled `11f504b2bf45a39c1bc4746952f50d58c5022743` | ✅ |
| Efficacia del freeze registrata e verificata | `PROVA_REMOTA_FREEZE_PIANO_STATISTICO_03_8_2026-09-15.json`, 6.773 byte, SHA-256 `2c011bba8b02e3c357cfe62ea90d63f75527d0690186846d5e385e8e79a44f97`; verbale OK 6.850 byte, SHA-256 `e34b791e5e45bca2c3f94585815c1502623c4739ca1e9bbe8cd69a6f4c2f4229`; acquisizione SHA-256 `7c5d65100144c87a4d7f4cc4fcf9a3f7997f68cf420a15ad0eb1f3e2ae9dd838`; tutti pubblicati attraverso `2edd4550cabfd065fafa1834609e9789149611ee` | ✅ |
| Chiusura documentale 03.8 | presente candidato; verifica, acquisizione e pubblicazione ancora da eseguire | ⏳ |

## Lettura corretta dei record storici

I manifest e i record certificati restano byte-identici. I valori temporali
`record_verified=false`, `record_published=false` e
`subphase_03_8_closed=false` nel record post-tag descrivono il momento precedente
alla sua verifica, acquisizione e pubblicazione; non vengono riscritti a
posteriori. Il verbale, la sua acquisizione e la raggiungibilità da
`origin/main` documentano gli eventi successivi.

Il manifest storico `PIANO_STATISTICO_FREEZE.json` resta una fotografia del
proprio checkpoint. Il manifest finale pre-tag resta una fotografia precedente
alla creazione del tag. Nessuno dei due viene trasformato in un registro
auto-referenziale.

## Effetti e confini

- È vigente il conteggio completo delle chiamate e la fattibilità
  `1,20 × T ≤ W`; 3.700 è soltanto un tetto storico.
- I controlli tecnici OOD su F6/F4 e sostituti appartengono alla 03.11, dopo il
  freeze statistico e prima delle chiamate sui test. Non erano prerequisiti del
  tag e non esiste una dipendenza circolare 03.8→03.11→03.8.
- L'ordine label 1a è stato approvato nel proprio record D9 distinto. Questa
  chiusura non lo riapprova e non autorizza esecuzioni.
- Il freeze 03.8 non qualifica harness 03.10, servizi, configurazioni, T5,
  ledger, pilot, inferenze, simulazioni o run finali.
- La Fase 03 resta aperta e prosegue secondo i propri prerequisiti e gate.

## Confine Git e passo successivo

La base è il `main` remoto pubblicato
`2edd4550cabfd065fafa1834609e9789149611ee`. Il candidato di chiusura deve
contenere soltanto il presente record e gli allineamenti documentali correnti;
non deve contenere i successori esclusi
`7c37ee64da86fab1452f69ca50721ec2af01bf7f` e
`f944efd2872786d439c22b38302d33e91d08cfab`.

Il prossimo gate è una verifica indipendente limitata al delta esatto di
chiusura. Solo dopo l'acquisizione byte-identica dell'OK potrà essere proposta
una pubblicazione non forzata. Il tag esistente resta invariato.
