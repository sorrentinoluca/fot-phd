# Consegna locale — consolidamento 03.15 e raccordo metriche

**ID operativo:** Studio 2 FoT-TEP, Fase 03 — consolidamento 03.6→03.12→letteratura + 03.15 +
03.9→03.10  
**Data:** 2026-09-14, Europe/Rome  
**Esito:** candidato locale concreto e reviewabile; non integrato in `main`, non pubblicato e non
congelato. 03.9, 03.10, 03.15 e Fase 03 restano aperte.

## 1. Riferimenti Git e ambiente

| Voce | Valore |
|---|---|
| Repository | `/Users/luker/fot-tep` |
| Worktree dedicato | `/Users/luker/fot-tep-consolidamento-0315-metriche` |
| Branch locale | `codex/studio2-consolidamento-0315-metriche` |
| `origin/main` al preflight | `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` |
| `main` remoto al controllo finale (`git ls-remote`) | `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` |
| Base comune | `e82b5a08bf642ad45f77e71832958207beb1181c` |
| Candidato 03.15 corretto | `10582798eb5a4b52672bfbcb1cc028adcb73e9f1` |
| Pacchetto 03.15 | `d35b684acbfd1f357bc34f3a21cebb18e8a6bea0` |
| Candidato metriche minimo | `3360867751c66a39e819247f86dab8e936f8cbb3` |
| Merge di consolidamento | `4ba2ad6e4a298411b4f0f7572ad3ef8e55948015` |
| Candidato tecnico completo di acquisizioni e raccordi | `04dee86140b3ff18882f9d164beef5ab7bf33e00` |
| Commit del presente record | commit che contiene questo file, successore diretto di `04dee86`; l'hash non è incorporato per evitare auto-riferimento |

Il lavoro è partito dalla base esatta `e82b5a0`, non dal branch locale `main` e non dalla copia
principale sporca. Il merge `4ba2ad6` ha due genitori nell'ordine `10582798`, `3360867`; entrambi,
insieme a `e82b5a0` e `d35b684`, sono antenati del candidato. Nessun worktree sorgente o di
revisione è stato scritto o riparato.

## 2. Sequenza dei commit

| Ordine | Commit | Scopo |
|---:|---|---|
| 1 | `4ba2ad6e4a298411b4f0f7572ad3ef8e55948015` | merge locale delle storie 03.15 e metriche; risoluzione della sola sintesi iniziale MD/HTML |
| 2 | `1e4afa8c6c069cacc3702481e4de5f5794adda61` | acquisizione byte-identica di verbali e directory di evidenza |
| 3 | `8a99df01a0f2bd7781e713a4aee7e22f9a7b2998` | acquisizione distinta delle consegne esterne successive |
| 4 | `d3bc506558dd1a26192ce6ab84552a20ecc73d0f` | acquisizione distinta del report d'integrazione metriche |
| 5 | `73dc4e50718aedc43da70956ac9fb799831f6a2e` | record mirato delle identità runtime e dei limiti |
| 6 | `04dee86140b3ff18882f9d164beef5ab7bf33e00` | sola correzione tipografica di parità §4.10 HTML |
| 7 | commit che contiene questo file | presente consegna e prompt di verifica circoscritta |

La storia di `10582798` conserva a sua volta il merge `18aa3bb` della base comune con
`d35b684`, l'acquisizione `705f1c4`, il walkthrough `532cc77`, il record `9b6bd64` e il delta
correttivo R1/R2. La catena `e82b5a0 → fae8ae8 → f4bca45 → f890a3d → 3360867` resta integra
come secondo ramo del merge.

## 3. Attività e delta effettivamente nuovo

Sono state unite le due storie preservando tutti i file già verificati. Gli unici conflitti
effettivi erano nella frase di stato iniziale dei due walkthrough: la risoluzione contiene insieme
il rinvio §4.10 e il rinvio §4.15. L'indice HTML è stato unito automaticamente nello stesso ordine.

La sezione §4.10 Markdown coincide con `3360867` e §4.15 Markdown coincide con `10582798`; la
parte §4.15 HTML coincide con `10582798`. In §4.10 HTML sono stati aggiunti soltanto tre spazi
tipografici attorno alle frecce del mapping, isolati in `04dee86`, per ottenere parità normalizzata
esatta con il Markdown. Non sono cambiati significato, numeri o codice.

`studio2/PROVENIENZA.md` è byte-identico a `10582798` e conserva §§1–14. La frase storica sui
17 file del pacchetto più due consegne resta delimitata al candidato 03.15 verificato; le nuove
acquisizioni sono inventariate separatamente in questo record. La ripartizione delle 54 fonti
03.15 è stata ricalcolata sia contro `10582798` sia contro il candidato consolidato: **44 commit
antenati / 8 commit esterni / 2 fonti locali senza commit** in entrambi i perimetri.

Non è stato importato il vecchio harness completo. Il codice runtime acquisito resta quello del
candidato minimo: `common.py`, `metric_adapter.py`, `metrics.py`, `__init__.py` e il test mirato;
configurazioni pilot, endpoint, input pending, vecchi pin 03.12, ledger e componenti completi non
sono entrati nel consolidamento.

## 4. Inventario delle acquisizioni

Tutti i byte indicati sono stati inventariati prima della copia. Dopo i commit sono stati
confrontati sorgente esterna, copia nel worktree e blob `HEAD`.

| Ruolo | Destinazione | Byte | SHA-256 |
|---|---|---:|---|
| A — OK raccordo comune | `studio2/fase03/VERIFICA_RACCORDO_DOCUMENTALE_036_0312_LETTERATURA.md` | 21.639 | `7c1d6ebf90ccb29d2b3f418b0b6740b62435626db8e9a6b7f6abdd8512a27511` |
| Manifest evidenze A | `studio2/fase03/evidenze_verifica_raccordo/MANIFEST_EVIDENZE.json` | 5.566 | `6512effee4adcb1d4407cc29689228ac28514f54a60bc647f8c0f3dcc7a8860d` |
| Snapshot B verificato A | `studio2/fase03/evidenze_verifica_raccordo/CONSEGNA_ESTERNA_B.md` | 17.597 | `46185e3d15867253e98f5c9f08df5ab8ed8a6a6643a15d5011079341045514e6` |
| B — NON OK storico 03.15 | `studio2/fase03/paper_sections/VERIFICA_RACCORDO_DOCUMENTALE_0315.md` | 24.282 | `1b6125541df01b1172af3bfa5639cd0ff200657820d977dadcf277f5b399d7d3` |
| Manifest evidenze B | `studio2/fase03/paper_sections/evidenze_verifica_raccordo_0315/MANIFEST_EVIDENZE.json` | 7.753 | `44ed2a0bd01472b1d6ccafb6f0b3adc4e63d26a825b2bf627170e086af0bc04d` |
| Snapshot B verificato 03.15 | `studio2/fase03/paper_sections/evidenze_verifica_raccordo_0315/CONSEGNA_ESTERNA_B.md` | 11.046 | `b7398a24f57f18b59be4cd77e40785a286805e619f76eb65d8642f0d941ba607` |
| C — OK correttivo R1/R2 | `studio2/fase03/paper_sections/VERIFICA_DELTA_RACCORDO_0315.md` | 7.415 | `efd16ffb46dbcef940e326e51d319a4f33ca7f64cf4f4a230bf548aba0ac0129` |
| D — controllo esecutore metriche | `studio2/fase03/harness/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE_ESECUTORE.md` | 7.975 | `d8b9c34f7af69de3ef749efe21e9e645c828bbf942086671311d094422883862` |
| E — verifica successiva metriche | `studio2/fase03/harness/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE_INDIPENDENTE.md` | 7.351 | `0c1b760368b38e842df3f73196286e83995974cf25efc0dedd571e17276e4d98` |
| Consegna comune viva successiva | `studio2/fase03/CONSEGNA_RACCORDO_03_6_03_12_LETTERATURA_2026-09-14.md` | 17.597 | `46185e3d15867253e98f5c9f08df5ab8ed8a6a6643a15d5011079341045514e6` |
| Consegna 03.15 viva successiva | `studio2/fase03/paper_sections/CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md` | 11.801 | `8f2c1082606eea5554f0213d66a0f8dac5d66adc5ade4d35bca0a832bb4bdb71` |
| Consegna acquisizione OK metriche | `studio2/fase03/harness/CONSEGNA_ACQUISIZIONE_OK_RACCORDO_METRICHE.md` | 10.164 | `d3294a90ebd46c0e2892ee4c33ecc2ddd7ce5bfdea0d7fad205745f9ad101972` |
| Report integrazione metriche | `studio2/fase03/harness/REPORT_INTEGRAZIONE_RACCORDO_METRICHE.md` | 8.871 | `96f9867e06a8060fd2383416592564ba1d09c40128b08715509e339f07b2e7c9` |

La directory A contiene 30 file; il manifest, escluso dal proprio elenco per evitare
auto-riferimento, verifica 30 percorsi registrati (verbale principale più 29 file della directory)
senza mismatch. La directory B contiene 28 file e il relativo manifest verifica 28 percorsi
registrati (verbale principale più 27 file della directory) senza mismatch. Snapshot A e B,
patch, script, risultati e metadati restano nei percorsi relativi originali. La consegna viva
03.15, aggiornata dopo lo snapshot B, è acquisita come documento successivo e non ha sostituito
retroattivamente lo snapshot da 11.046 byte.

D ed E avevano lo stesso nome sorgente: sono conservati con suffissi distinti senza cambiare un
byte. I verbali scientifici e tecnici già presenti nei candidati non sono stati duplicati.

## 5. Tracciabilità delle sessioni

Il record dedicato è:

`studio2/fase03/ACQUISIZIONE_IDENTITA_RUNTIME_CONSOLIDAMENTO_2026-09-14.md`.

Riscontri principali:

- l'esecutore della correzione `9b6bd64..10582798` è collegato dal log runtime locale a OpenAI
  Codex Desktop, sessione `01a0a0e3-c3bd-7523-90ca-b5f28a40461f`, modello
  `gpt-5.6-sol`, effort `medium`; la chiamata e l'output registrano direttamente il commit;
- C dichiara Claude Cowork, modello configurato `claude-opus-4-8`, sessione
  `session_013BLwcitiaqnqjNBLvV2mhH`; effort non esposto;
- D dichiara Claude Cowork/Agent SDK, modello configurato `claude-opus-4-8`, sessione
  `session_01CHTctYBYq1nnbumDuHrCsC`; resta un controllo non indipendente dell'esecutore;
- E dichiara soltanto OpenAI Codex, modello basato su GPT-5. Le occorrenze nei log locali sono
  letture successive del verbale o contesto orchestratore e non ne provano la paternità: ID
  sessione/task, modello preciso ed effort restano non verificabili.

Non sono stati copiati log di conversazione o directory di sessione. Nessuna identità è stata
dedotta dal committer Git o dallo stile. La copia isolata descritta da E è una prova tecnica del
contenuto, non da sola una prova d'indipendenza personale.

## 6. Controlli eseguiti ed esiti

| Controllo | Esito |
|---|---|
| Ascendenze | `e82b5a0`, `d35b684`, `10582798`, `3360867`: 4/4 antenati |
| Pacchetto 03.15 | 17/17 file presenti a `d35b684` byte-identici |
| Import minimo metriche | 14/14 file presenti a `3360867` byte-identici; le aggiunte posteriori sono solo documenti acquisiti |
| Evidence scientifica | albero `studio2/fase03/evidence` identico a `e82b5a0` |
| Fonti pinnate 03.9 e 03.6 | 4 impronte del contratto 03.9 + `extract_evidence.py` + `leakage.py`: 6/6 |
| Contratto R4 | 10/10 file correnti identici al target `3c64390`; 8/8 fonti storiche verificate nei riferimenti; manifest identico al target |
| Fonti 03.15 | 44/8/2 sia a `10582798` sia al candidato consolidato |
| Acquisizioni | 9/9 file principali sorgente=copia=blob; bundle evidenze 30/30 e 28/28 |
| Lint paper sections | 5 file, 0 segnalazioni |
| Parità walkthrough | §4.10: 16 blocchi uguali; §4.15: 15 blocchi uguali; ordine corretto, 20 ID HTML univoci, link locali risolti, 0 marker di conflitto |
| Test metriche | da copia isolata `git archive`: 9 test, 9 OK, 0 failure/error/skip |
| Dipendenze metriche | stdlib + import relativo `common`; 0 percorsi assoluti, checkout fratelli, rete o subprocess nel codice/test mirato |
| Guardiano baseline/finale | entrambe 35 test, 14 failure, 1 skip, 0 errori; identificativi e subtest identici |
| Stato del worktree prima del record | pulito a `04dee86` |

Il guardiano `python3 docs/test_explanation.py` esce 1 e **non è una suite PASS**. I 14 failure e
lo skip sono storici; il confronto baseline/finale è positivo soltanto come controllo di non
regressione. I log temporanei sono `/tmp/fot_tep_guard_baseline_20260914.log` e
`/tmp/fot_tep_guard_final_20260914.log`. Il test metriche è stato eseguito anche nella copia senza
`.git` `/tmp/fot-tep-consolidamento-check.80AfzB`.

Non sono state ripetute review scientifiche, estrazioni, bootstrap, ricerche bibliografiche,
riscaricamenti, simulazioni o chiamate sperimentali.

## 7. File modificati o creati e documenti pertinenti

Il merge modifica la coppia:

- `docs/fot_walkthrough_conversazione_studio2.md`;
- `docs/fot_walkthrough_conversazione_studio2.html`.

Integra inoltre per storia il pacchetto `studio2/fase03/paper_sections/` di `d35b684` e i 14 file
minimi `studio2/fase03/harness/` di `3360867`. Le acquisizioni successive sono quelle della tabella
in §4 e le due directory di evidenza. I nuovi record operativi sono:

- `studio2/fase03/ACQUISIZIONE_IDENTITA_RUNTIME_CONSOLIDAMENTO_2026-09-14.md`;
- `studio2/fase03/CONSEGNA_CONSOLIDAMENTO_0315_METRICHE_2026-09-14.md` (questo file);
- `studio2/fase03/PROMPT_VERIFICA_CONSOLIDAMENTO_0315_METRICHE.md`.

Il prompt limita la prossima review al candidato tecnico `04dee86`, quindi non riapre gli OK
scientifici precedenti e non crea una dipendenza circolare dal commit documentale che lo contiene.

## 8. Stato Git finale

Al completamento della consegna:

- **committati:** merge, acquisizioni, record runtime, correzione di parità, presente report e
  prompt, secondo la sequenza in §2;
- **modificati tracciati:** nessuno;
- **staged:** nessuno;
- **non tracciati nel worktree dedicato:** nessuno, incluso il presente report;
- **branch:** soltanto `codex/studio2-consolidamento-0315-metriche`;
- **main:** non modificato;
- **push:** non eseguito;
- **tag/freeze:** non creati.

Il commit contenente questo file è intenzionalmente identificato dalla sua posizione Git, non da
un hash auto-incorporato. L'orchestratore deve risolverlo con
`git log -1 --format=%H -- studio2/fase03/CONSEGNA_CONSOLIDAMENTO_0315_METRICHE_2026-09-14.md`
e verificare che sia successore diretto di `04dee86`.

## 9. Stato effettivo, residui e prossimo passo

| Ambito | Stato effettivo |
|---|---|
| Consolidamento locale | preparato e committato sul branch dedicato |
| Review del nuovo raccordo finale | non ancora eseguita; prompt circoscritto disponibile |
| Integrazione in `main` | non eseguita |
| Pubblicazione | nessun push |
| Congelamento | nessun tag o freeze; il futuro tag schema resta destinato esclusivamente a `3c64390bc4dd58c48cc4e1e388a38989b32b3143` |
| Chiusura | 03.9, 03.10, 03.15 e Fase 03 restano aperte |

Restano fuori incarico e irrisolti: firma/freeze 03.8, decisione D9, qualificazione del 122B,
harness completo, pin 03.12, controlli OOD, simulazioni e chiamate sperimentali. A/B, FAR e U3 non
sono stati riaperti. Restano inoltre la raggiungibilità della rev. 10 e delle fonti 03.6 dalla
futura base seriale/remota richiesta per i freeze, e l'identità runtime non esposta del revisore E.

Non è emersa la necessità di modificare codice o contenuto scientifico verificato. L'unica nuova
decisione richiesta all'autore, dopo una review OK del raccordo, sarà se autorizzare una futura
integrazione in `main`; tale autorizzazione non è stata data in questo incarico.

**Prossimo passo:** aprire una verifica indipendente del solo candidato tecnico `04dee86` usando
`studio2/fase03/PROMPT_VERIFICA_CONSOLIDAMENTO_0315_METRICHE.md`. Soltanto dopo un verbale
circostanziato e una decisione esplicita dell'autore si potrà valutare un'integrazione separata;
pubblicazione e congelamento resteranno comunque operazioni autonome.
