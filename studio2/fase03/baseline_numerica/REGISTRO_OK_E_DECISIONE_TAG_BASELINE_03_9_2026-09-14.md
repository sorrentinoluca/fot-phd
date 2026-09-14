# Registro OK residui 03.9 e decisione autoriale sul tag

**Data:** 2026-09-14, Europe/Rome

**Stato:** OK indipendente acquisito localmente; nome e regola del target approvati;
pubblicazione, tag e revisione di efficacia ancora da eseguire. La sotto-fase 03.9 resta aperta.

Questo è un record additivo successivo a `BASELINE_FREEZE_rev004.json`. Non modifica la rev.4,
non rende efficace il freeze e non sostituisce il verbale indipendente. Il commit contenente
questo file si risolve dalla storia Git; il suo SHA non è autoriferito nel contenuto.

## Candidato e base verificati

| Ruolo | Commit |
| --- | --- |
| Base pubblicata, incluso il record finale 03.12 | `f1746e1e76c5657e5cb74ed765d2f22143f979ce` |
| Candidato residui 03.9 verificato | `49bc53b6d4630e7675eb5cf59c6d483d694ab042` |
| Commit locale di acquisizione dell'OK | `9370346c61d6edfdb0521aea812003a5f013748d` |
| Commit locale di questo record | risolvere il primo commit successivo a `9370346` che contiene questo file |

Il candidato verificato aggiunge esclusivamente i cinque file elencati da `integrity.json`; la
review ha confermato 25.912 byte aggiunti, nessuna modifica o cancellazione e `git diff --check`
pulito. Il richiamo descrittivo a `4f98a297` nella rev.4 è stato valutato non bloccante dal
revisore e viene conservato byte-identico, come richiesto.

## OK indipendente acquisito

- **Verdetto:** `OK`, limitato al delta
  `f1746e1e76c5657e5cb74ed765d2f22143f979ce..49bc53b6d4630e7675eb5cf59c6d483d694ab042`.
- **Verbale:**
  `evidenze_verifica_residui_49bc53b/VERIFICA_RESIDUI_BASELINE_03_9_2026-09-14.md`.
- **Revisore:** OpenAI Codex Desktop, modello esposto `gpt-6-astra`, reasoning `high`, provider
  `openai`.
- **Sessione indipendente:** `01a0a199-006e-74c0-841b-f166692301ea`, agente `/root`.
- **Produttore distinto:** sessione `01a0a18c-3719-7611-a52e-3b4b42ccd180`, modello esposto
  `gpt-5.6-sol`, reasoning `high`.
- **Perimetro dell'OK:** sola acquisizione della fonte normativa rev.10, record di acquisizione,
  matrice dei requisiti e rev.4 non efficace. Non è un OK scientifico nuovo di `normal_dev`,
  evidence o prototipi, né dell'intero harness 03.10 o piano 03.8.

Il verbale conserva la richiesta allora pendente di nome e target del tag. Non viene riscritto:
la decisione successiva dell'autore è registrata nella sezione dedicata sotto.

## Acquisizione e integrità

Sede dedicata:
`studio2/fase03/baseline_numerica/evidenze_verifica_residui_49bc53b/`.
Il manifest `SHA256_PROVE.txt` è stato controllato prima della copia. Sono stati acquisiti soltanto
il verbale e i sette file adiacenti pertinenti; nessun rollout completo o materiale estraneo.

| File | Byte | SHA-256 |
| --- | ---: | --- |
| `VERIFICA_RESIDUI_BASELINE_03_9_2026-09-14.md` | 12.169 | `2131277d6d8840e767e73e3b0ab9e421f4b27acaa39a18faa770f19a69dd536a` |
| `SHA256_PROVE.txt` | 519 | `04938e06781958108a9223b3dd375c91630ddfb292ea7cac9d52efd0c0500cdd` |
| `integrity.json` | 4.533 | `d99d294598da76f0be9b2281b2c76491f62a523b6a63d0f651ebed97d7d78714` |
| `runtime_e_consegna.json` | 3.840 | `b2fa2b8d8435ce2ee422a14bd449107b42a8ba9baf6b7cb62ce295e887f1ea4b` |
| `ref_remoti.txt` | 244 | `463e33dd938a5c65f5226a0bafefa5163c78212204d1aa816156b71de903f604` |
| `guardiano_base.log` | 2.582.291 | `3fc478293a281169e2ffac65a317bff7eb66d8c0555875041bf4f3506f653097` |
| `guardiano_candidato.log` | 2.582.109 | `7cbeee279679edc11dbb87083d93801a8b9377d1541c1d385aca223d176f6467` |
| `guardiano_comparison.json` | 153 | `996b5c6502cf89176ba55e603673090155f11c78818930f2663453ebdc988e21` |

Per ciascun file, sorgente del revisore, copia acquisita e blob del commit `9370346` coincidono
per dimensione e SHA-256. `integrity.json` è coerente con i cinque blob del candidato; prima riga
del verbale `VERDETTO: OK`. Il confronto del guardiano registra 35 test, 14 failure storici,
1 skip, 0 errori, log normalizzati identici e nessuna regressione. I 19 test mirati e le verifiche
scientifiche già concluse non sono stati rieseguiti in questa acquisizione.

## Decisione dell'autore sul tag

La decisione è approvata dall'autore nella conversazione corrente, successivamente al verbale:

- **nome letterale:** `studio2-fase03-baseline-numerica-frozen-001`;
- **regola del target:** il commit pubblicato contenente il candidato verificato, l'acquisizione
  dell'OK e tutti i prerequisiti, precedente alla successiva rev.5 di efficacia.

La richiesta storica del verbale è quindi **soddisfatta quanto a decisione**, non ancora quanto a
esecuzione. Lo SHA del target finale resta intenzionalmente non valorizzato: dovrà essere risolto
dalla storia Git dopo il completamento e l'eventuale raccordo dei record sul `main` allora
corrente. Non può essere sostituito dal tag dati `studio2-fase03-normal-dev-v1`, dal candidato
tecnico `49bc53b` isolato o da uno SHA inventato in anticipo.

## Stato e sequenza residua

Al momento di questo record:

- `BASELINE_FREEZE.json`, rev.2, rev.3 e rev.4 restano byte-identici; rev.4 è `effective=false`;
- `origin/main` osservato resta `f1746e1e76c5657e5cb74ed765d2f22143f979ce`;
- il candidato e i due commit locali successivi non sono pubblicati;
- il tag `studio2-fase03-baseline-numerica-frozen-001` non è creato né pubblicato;
- oggetto e peeled del futuro tag non esistono ancora nel record;
- `BASELINE_FREEZE_rev005.json` non è creato;
- walkthrough, piano 03.8, D9, 122B, harness completo e Fase 03 non sono modificati o chiusi.

La finestra successiva dovrà: ricontrollare il `main` remoto; raccordare senza riscrivere il
candidato verificato, il commit di acquisizione e questo record; pubblicare i commit autorizzati;
verificarne la raggiungibilità; risolvere dalla storia lo SHA conforme alla regola del target;
verificare l'assenza locale e remota del nome approvato; creare e pubblicare soltanto quel tag;
verificarne oggetto e peeled remoti; infine registrare l'efficacia in una rev.5 additiva, senza
modificare gli snapshot storici.
