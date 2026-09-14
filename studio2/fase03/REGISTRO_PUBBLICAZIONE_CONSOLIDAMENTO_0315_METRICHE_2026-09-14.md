# Registro di pubblicazione — consolidamento 03.15 e raccordo metriche

**Data:** 2026-09-14, Europe/Rome
**Perimetro:** Studio 2 FoT-TEP, Fase 03; pubblicazione del consolidamento locale verificato
**Esito del primo passaggio:** `origin/main` avanzato con fast-forward da
`c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` a
`07a64e96c39ad73889f88978cd2ecbc719201b3e`.

Questo record documenta una pubblicazione, non una nuova verifica scientifica o tecnica. Non
crea freeze, non qualifica l'harness completo e non chiude 03.9, 03.10, 03.15 o Fase 03.

## 1. Riferimenti Git

| Ruolo | Commit |
| --- | --- |
| `origin/main` precedente | `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` |
| Candidato tecnico qualificato dall'OK | `04dee86140b3ff18882f9d164beef5ab7bf33e00` |
| Consegna successiva al candidato | `380d162390048e8a7e9e9884b4e932867e63a821` |
| Acquisizione byte-identica del verbale e delle evidenze | `770d17ccfcc62d08be56be54c7f08e5b26ce40a9` |
| Record successivo dell'acquisizione | `07a64e96c39ad73889f88978cd2ecbc719201b3e` |
| Candidato completo pubblicato nel primo passaggio | `07a64e96c39ad73889f88978cd2ecbc719201b3e` |
| Record di pubblicazione | commit che contiene questo file, successore diretto di `07a64e9` |

Il worktree dedicato è
`/Users/luker/fot-tep-pubblicazione-consolidamento-0315-metriche`, sul branch locale `main`.
La copia principale `/Users/luker/fot-tep` è rimasta su
`codex/studio2-soglie-normal` a `819b12e97fb94d501032655ec2f226139e6c5ca5`, con i file
preesistenti non tracciati intatti. Un comando di fast-forward invocato inizialmente dalla copia
principale è stato rifiutato da Git prima di scrivere perché avrebbe sovrascritto file non
tracciati; l'integrazione effettiva è stata quindi eseguita soltanto nel worktree dedicato.
Nessun lock o worktree altrui è stato rimosso, riparato o spostato.

## 2. Modalità d'integrazione e riscontro remoto

Subito prima dell'integrazione e subito prima del push, `git ls-remote` ha confermato
`refs/heads/main` a `c486eee`. Tale commit era antenato del candidato completo. `main` è stato
quindi avanzato con `git merge --ff-only`, senza merge commit, cherry-pick, rebase o risoluzione
di conflitti. Il tree risultante, `49d9fea06c4d2e046185fa29f926c4531e459174`, coincide con il
tree di `07a64e9`.

Il primo push è stato un push ordinario del solo refspec `main:main`, senza force, `--all` o
`--tags`. La lettura remota successiva ha restituito
`07a64e96c39ad73889f88978cd2ecbc719201b3e` per `refs/heads/main`. Il digest SHA-256
dell'elenco dei tag remoti è rimasto
`f086f4d2f6dfb68370c5f1c60725c9f921b792c71731226657eb54cea0d260cd`; nessun tag è stato
creato o spostato.

## 3. Controlli conservativi

- `c486eee` è antenato di `07a64e9`; l'integrazione è un fast-forward puro.
- Il delta `04dee86..07a64e9` aggiunge soltanto consegna, prompt, verbale, bundle di evidenze e
  record di acquisizione. Non modifica pacchetti tecnici o scientifici preesistenti.
- Il manifest acquisito contiene 25 voci: tutte coincidono per dimensione e SHA-256 fra sorgente
  del revisore, copia acquisita e blob del commit `770d17c`. La directory contiene 25 file incluso
  il manifest; `770d17c` aggiunge 26 percorsi incluso il verbale esterno e `07a64e9` aggiunge un
  solo percorso.
- Sono antenati del candidato completo: candidato 03.6 `c66bd8d` e suo merge `7c99a83`; target
  R4 `3c64390`; candidato e verbale letteratura `e37c3db` e `40911d0`; pacchetto 03.15
  `d35b684` e raccordo `10582798`; raccordo metriche minimo `3360867`; candidato tecnico
  qualificato `04dee86`, consegna `380d162` e acquisizione `770d17c`.
- Sono stati riusati i controlli già acquisiti perché il fast-forward non ha modificato byte:
  pacchetto paper 17/17, raccordo metriche 14/14, evidence tree identico, R4 18/18, fonti
  03.15 44/8/2, sezioni 4.10 e 4.15 in ordine e in parità normalizzata MD/HTML, 20 ID HTML
  univoci, 475/475 link locali risolti, correzioni R1/R2 e `studio2/PROVENIENZA.md` preservate.
- I risultati acquisiti restano: test mirati metriche 9/9 OK e lint paper sections senza
  segnalazioni. Il guardiano documentale non è PASS: conserva 35 test, 14 failure storici,
  uno skip e zero errori, senza regressione rispetto alla base verificata.

Non sono state ripetute review scientifiche, estrazioni, bootstrap scientifici, simulazioni,
inferenze, ricerche bibliografiche o chiamate sperimentali.

## 4. Riferimenti ora raggiungibili in `origin/main`

- I sorgenti e la storia 03.6 sono raggiungibili, inclusi `c66bd8d` e `7c99a83`.
- Il target schema R4 `3c64390` e le relative prove sono pubblicati; il tag proposto per R4 non
  è stato creato.
- La storia bibliografica terminante in `40911d0` è raggiungibile.
- Il pacchetto 03.15 e le correzioni R1/R2 sono raggiungibili tramite `d35b684` e `10582798`.
- Il raccordo minimo metriche `3360867` è integrato. Questo non qualifica né importa il vecchio
  harness completo.
- Il candidato verificato `04dee86`, la consegna `380d162`, l'acquisizione `770d17c` e il suo
  record `07a64e9` sono raggiungibili dalla storia remota.

## 5. Limiti e residui aperti

03.9 resta aperta fino ai controlli e al freeze successivi. Anche 03.10, 03.15 e Fase 03 restano
aperte. Firma e freeze 03.8, decisione D9, qualificazione del servizio/server 122B, harness
completo, pin 03.12, controlli OOD, T5, ledger/calendario e raggiungibilità della revisione 10
restano attività separate. Lo schema R4 è pubblicato ma non taggato. Il raccordo metriche
pubblicato è soltanto quello minimo verificato. A/B, FAR e U3 non sono stati riaperti.

Il commit contenente questo file deve essere risolto dalla storia Git per evitare un
auto-riferimento. Il secondo passaggio autorizzato pubblica esclusivamente tale successore su
`main`, dopo un nuovo controllo del ref remoto.
