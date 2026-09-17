# Aggiornamento pubblicazione e riverifica — esecuzione finale 03.11

Data dell'aggiornamento: **2026-09-17**.

Questo record aggiorna lo stato di conservazione successivo al verbale storico
`ACQUISIZIONE_OK_ESECUZIONE_03_11.md`, senza modificarlo in luogo. La release
`studio2-fase03-test-v1` è stata pubblicata e, il 2026-09-17, tutti e tre gli asset sono stati
riscaricati dall'autore e verificati contro gli SHA-256 registrati in `ARTIFACT_STORAGE.json`:

| Asset | Byte | SHA-256 | Esito |
| --- | ---: | --- | --- |
| `test_batch_f5_001.tar.gz` | 141.191.097 | `ac1e7c0c4575ab746ee24a8bb5ce7f09289919773bc4d8c61ba86f7a93218a55` | **OK** |
| `chain_f5_001.tar.gz` | 1.579.326 | `242f689a8737739f51eb6b3acefaf34cea4c06e9ebd547beccbcf1760a473aec` | **OK** |
| `ood_preflight_001.tar` | 7.426.560 | `16acf7c1e18923b606a47fe3fb0efaa83b99e8ee19024f11f4d8f3fd675929df` | **OK** |

Esito complessivo: **3/3 asset OK**, 150.196.983 byte verificati, zero mismatch. Lo stato
successivo applicabile è `public_release_verified_by_redownload`. `release_id`,
`release_commit` e `published_at_utc` restano `null`: questo aggiornamento non inventa metadati
remoti non presenti nella verifica offline.
