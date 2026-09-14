# Residui della baseline numerica 03.9 — candidato di chiusura

**Data:** 2026-09-14, Europe/Rome

**Base verificata:** `origin/main` = `f1746e1e76c5657e5cb74ed765d2f22143f979ce`,
record finale pubblicato della 03.12

**Stato:** candidato locale preparato; `BASELINE_FREEZE_rev004.json` resta
`effective=false`; nessun push e nessun tag.

Questo rapporto chiude la ricognizione dei residui, non la sotto-fase. Distingue i controlli
eseguiti ora dalle verifiche scientifiche già acquisite e prepara il delta minimo che deve essere
verificato indipendentemente. Non riapre `normal_dev`, FAR, A/B, U3, estrazioni, prototipi,
bootstrap o prestazioni.

## Matrice requisito → prova → esito

| Requisito | Prova primaria | Controllo eseguito ora | Esito |
| --- | --- | --- | --- |
| Adozione del mapping 03.9 → 03.10 | `metric_adapter.py`, `metrics.py`, `SPECIFICA_HARNESS.md` §8; candidato minimo `3360867`; consolidamento qualificato `04dee86`; verbali del raccordo | Letti i punti effettivi di produzione/consumo; eseguiti i 9 test di `test_metric_raccordo.py` | **Soddisfatto in `origin/main`**: `accuracy→accuracy_all`, `n→total`, `abstentions→abstained`; valori numerici copiati dopo validazione |
| `non_abstained` e invalidità | Stesse fonti; `CONTRATTO_RACCORDO_METRICHE.md`; verifica indipendente `VERIFICA_RACCORDO_METRICHE.md` | Ispezione del codice effettivamente pubblicato e test dei casi con invalidi, insieme vuoto e tutto astenuto | **Soddisfatto**: `non_abstained=total-abstained`; l'invalido generale non è corretto né astenuto e resta nel denominatore; l'adapter emette `invalid=0` solo per la 03.9 valid-only fail-closed |
| Semantica baseline | `SPECIFICA_BASELINE_NUMERICA.md`, `baseline.py`, `BASELINE_FREEZE_rev003.json` | Ispezione e 10 test baseline/piano/guardia estrattore | **Preservata**: astensione solo per pareggio entro `1e-12`, distanza mean L1, nessun cutoff di distanza, classi locali assenti non candidate e nessun fallback globale |
| Sorgenti 03.6 raggiungibili | `c66bd8d` e integrazione `7c99a83`; `extract_evidence.py`; `leakage.py` | Verificata ancestry verso `origin/main` e ricalcolati SHA-256 | **Soddisfatto**: entrambi i commit sono antenati di `origin/main`; impronte `46b451…24e97` e `c77ae5…3887` coincidono con i pin della rev.3 e con la guardia di `extract_normal_evidence.py` |
| Altri sorgenti richiesti dalla baseline | Elenco `source_files` di `BASELINE_FREEZE_rev003.json`, pseudolabel e specifiche | Verificata presenza nel tree pubblicato; i test mirati coprono produttore, piano e guardie | **Soddisfatto**, senza ricostruire artefatti già verificati |
| Conservazione `normal_dev` | `ARTIFACT_STORAGE.json`, `MANIFEST_CONSERVAZIONE.csv`, `VERIFICA_RISCARICAMENTO_NORMAL_DEV.json` | Riuso dei record pubblicati; nessun nuovo download | **Soddisfatto per riuso**: release dati distinta dal freeze baseline, archivio SHA-256 `eef69b…a03`, 1.336/1.336 file già riscaricati e verificati |
| Fonte normativa rev.10 | `DELTA_HARNESS_03_10.md` al commit `6aaa5b3`, blob `780e08a`, SHA-256 `e92661f…55e` | Verificato che il commit non è antenato di `origin/main`; acquisita nel candidato la sola sorgente allo stesso path, byte e blob | **Bloccante prima del delta; risolta solo nel candidato locale**. Serve verifica indipendente e pubblicazione in `main`; non è stato integrato né congelato il piano 03.8 completo |
| Revisione successiva | Catena SHA-256 di `BASELINE_FREEZE.json`, rev.2 e rev.3 | Creata rev.4 additiva, senza modificare snapshot storici né il pin rev.3 dell'adapter | **Candidato preparato, non efficace**, pending review indipendente |
| Nome del tag baseline | Fonti 03.9 sopra e `APERTURA_SOTTOFASI_FASE03.md` | Ricerca puntuale nelle fonti e nei ref remoti | **Manca una fonte autorevole per il nome esatto**. La release `studio2-fase03-normal-dev-v1` non è il tag baseline; nessun nome viene inventato |
| Target e pubblicazione del tag | MAINTENANCE §§8.4–8.6; freeze storici; rev.3 | Nessuna creazione: il candidato non ha ancora OK, non è in `main` aggiornato post-03.12 e il nome manca | **Pending**. Il target proposto è il commit di chiusura residui verificato e raggiungibile in `main`, precedente al successivo record di efficacia; richiede conferma autoriale |

## Esito concreto della dipendenza rev.10

Il raccordo pubblicato è autosufficiente come implementazione operativa: codice, specifica 03.10
e test fissano mapping, denominatori e comportamento fail-closed. L'intero piano statistico 03.8
non è prerequisito del freeze 03.9 e non viene acquisito, approvato o congelato qui.

Resta però una lacuna di provenienza verificabile: contratto, registro OK e walkthrough dichiarano
`DELTA_HARNESS_03_10.md` come fonte **normativa** dell'autonomia dell'invalidità rispetto
all'astensione. Il solo commit locale `6aaa5b3` non soddisfa MAINTENANCE §8.5. Per evitare di far
dipendere la verifica finale da un branch temporaneo, il candidato aggiunge soltanto quel file,
nello stesso path, con lo stesso blob `780e08a` e SHA-256 `e92661f…55e`, più un record di
acquisizione. Questa operazione non importa le altre sette modifiche della rev.10, non chiude il
piano, non decide D9 e non autorizza il pilot.

## Controlli eseguiti ora e risultati riusati

Eseguiti ora su `origin/main` `f1746e1e` dopo il turno di pubblicazione 03.12:

- ancestry di `c66bd8d`, `7c99a83`, `3360867` e `04dee86`: tutti antenati;
- SHA-256 dei sorgenti 03.6 e dei punti di raccordo: coincidenti con i pin pubblicati;
- suite mirata combinata: **19/19 PASS** (9 raccordo metriche + 10 baseline/piano/guardie);
- guardiano documentale: **35 test, 14 failure storici, 1 skip, 0 errori**, invariato;
- identità dell'acquisizione rev.10: source/candidato blob `780e08a`, SHA-256
  `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`.

Riutilizzati, non rieseguiti: audit 40/40 e 320/320, estrazione/leakage delle 320 evidence,
ricalcolo dei 25 prototipi, verifica 1.336/1.336 membri della release, equivalenza esaustiva del
raccordo (12.341 valid-only + 10.626 con invalidi) e review del consolidamento `04dee86`.

## Candidato, review e sequenza di pubblicazione

Il candidato esatto è il commit che conterrà i cinque nuovi file elencati sotto, costruito sopra
`f1746e1e`; il suo hash viene riportato nella consegna Git e deve essere usato letteralmente dalla
verifica indipendente:

1. `piano_statistico/DELTA_HARNESS_03_10.md` — copia byte-identica della fonte;
2. `ACQUISIZIONE_DELTA_HARNESS_03_10.json` — pin e limiti dell'acquisizione;
3. `BASELINE_FREEZE_rev004.json` — candidato non efficace e catena revisioni;
4. `RAPPORTO_RESIDUI_BASELINE_03_9_2026-09-14.md` — matrice e consegna del candidato;
5. `PROMPT_VERIFICA_RESIDUI_BASELINE_03_9.md` — review circoscritta.

Dopo un OK indipendente: acquisire verbale e record OK senza riscrivere la rev.4; aggiornare il
delta su un eventuale nuovo `origin/main` preservando il record 03.12 `f1746e1e`; pubblicare i
soli commit 03.9 e verificarne la reachability. Solo dopo la decisione sul nome e target,
verificare l'assenza del tag, creare e pubblicare il solo tag baseline, controllare oggetto e
peeled remoti, quindi registrare l'efficacia in `BASELINE_FREEZE_rev005.json` o successiva.

## Decisione autoriale ancora necessaria

Le fonti autorevoli della 03.9 impongono un tag di freeze della baseline ma non ne riportano il
nome esatto. Occorre fornire il **nome letterale** del tag e confermare che debba puntare al commit
pubblicato che contiene candidato verificato, acquisizione dell'OK e tutti i prerequisiti, mentre
il record `effective=true` rimane nel commit successivo. Fino a tale decisione nessun tag può
essere creato senza inventare nome o target.
