# Integrazione e conservazione della sotto-fase 03.9

Stato al 2026-09-14: **pacchetto integrato e dati pubblicati; 03.9 ancora aperta,
freeze inefficace**. La Fase 03 resta aperta.

Il candidato `459947af892e33ed23a8bdf998db49aabf923c68`, con l'OK indipendente sul
contenuto scientifico di `ba1a206e1fe31c062d5491b4fb821ff925149982`, è stato integrato
in `origin/main` tramite `5bd1648c54a0673ebd66df3655cf8258dfa48d3b`.
Tutti i file del pacchetto 03.9 sono byte-identici nel merge; la provenienza passa a §11
per conservare §9 (03.7) e §10 (03.5). Walkthrough MD/HTML integrati insieme, §4.9.

## Conservazione completata

Pubblicata la [release normal-dev-v1](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-normal-dev-v1)
con archivio e checksum separato. SHA-256:
`eef69b42d8506c993ac45d77208df982d138b4354d7d4134bd67ba421dc91a03`.
Archivio: 151.500.800 byte. Riscaricati da GitHub in una nuova directory esterna e
verificati **1.336/1.336 file, 150.575.225 byte di contenuto**, zero mismatch, extra,
AppleDouble o header PAX. Verificati anche l'asset checksum e l'inventario congelato.

Prova: [VERIFICA_RISCARICAMENTO_NORMAL_DEV.json](VERIFICA_RISCARICAMENTO_NORMAL_DEV.json).
I metadati correnti sono in [ARTIFACT_STORAGE.json](ARTIFACT_STORAGE.json) e
[BASELINE_FREEZE_rev003.json](BASELINE_FREEZE_rev003.json). I manifest storico e rev. 2
restano invariati come fotografie dei rispettivi candidati; la rev. 3 registra soltanto
integrazione, pubblicazione e condizioni residue. L'OK storico non è presentato come una
nuova verifica indipendente della rev. 3.

Controlli: **10/10 test PASS**; guardiano **35 test, stessi 14 fallimenti preesistenti e
1 skip**. Nessun nuovo dato di test aperto, fit, simulazione, inferenza o calcolo di
prestazioni. Prototipi, piano, handoff, audit, decisioni e verbale indipendente preservati.

## Perché il freeze non è ancora efficace

1. **03.10 deve adottare e testare i nomi delle metriche.** Il requisito era già presente
   nel manifest rev. 2 e nel verbale OK: `accuracy` → `accuracy_all`, `n` → `total`,
   `abstentions` → `abstained`, con gestione esplicita di `non_abstained` e `invalid`.
   Il semplice confronto in `INTERFACE_CHECK.json` non è l'implementazione del raccordo.
2. **I sorgenti riusati di 03.6 devono raggiungere main.** `extract_normal_evidence.py`
   richiede l'estrattore e il controllo leakage con le impronte fissate nel manifest.
   Sono presenti nel candidato evidence `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb`, ma
   quel candidato non è ancora integrato. La release evidence-v2 conserva i dati;
   non sostituisce la raggiungibilità dei sorgenti richiesta da MAINTENANCE §8.5.
3. Dopo questi requisiti e i controlli previsti, pubblicare il **tag di freeze della
   baseline** e registrarne l'efficacia in una revisione successiva. Il tag della
   release dati non è il tag di freeze della baseline.

Nessuna modifica al branch harness o al branch evidence è stata inclusa per dichiarare
artificialmente soddisfatte queste dipendenze. I loro candidati, i worktree sorgente e
gli artefatti ignorati restano preservati. I report precedenti descrivono la loro consegna
locale; il presente documento e la rev. 3 aggiornano lo stato operativo successivo.
