# Recepimento eseguibile D9 — consegna locale per review indipendente

**Candidato tecnico locale, verifiche offline della preparatrice. Review indipendente
PENDING. Nessun GO, qualifica di servizio o freeze della 03.10.**

## Identità e base

- Worktree `/Users/luker/fot-tep-harness-d9`, branch `codex/studio2-harness-d9`.
- Base acquisita D04 `5886c6f9d078ee624deaec08763e04c14e96e4f0`, preservata
  nel ramo/worktree D04 pulito. L'OK offline D04 riguarda soltanto
  `aae29a908356e4a4842a214fdc3db9bff26ec3ca`, tree
  `4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`.
- Contratto/fonti/test-first: `62343a7bb526d5285df547ceb8f5ea0341515cef`,
  precedente a qualsiasi modifica runtime D9.
- **Tecnico D9: `6a8031b25aa1208047d79cc7f030bf9cf7841e67`; tree `bb3872d8fc1cbddebb4b055a8edad372e5aad430`.**
- Questo report e la consegna JSON appartengono a un successore documentale:
  non sostituiscono il tecnico. Il commit documentale è quello che introduce
  questo file, ricavabile con `git log --diff-filter=A -- studio2/fase03/harness/REPORT_D9.md`.
- Preparatrice: Codex, sessione `01a0a53e-927d-7493-a50a-34617bbac13f`;
  non è una review indipendente del proprio lavoro.

Prima delle scritture verificati base, ramo, stato pulito, worktree, remoto
`https://github.com/sorrentinoluca/fot-phd.git` e attività concorrenti.
L'osservazione remota di main era `a00605862f627710347bd63c49f79a6d0a00135f`;
nessun fetch/integrazione indiscriminata di altri rami. Attività 03.8 su altro
worktree e successivamente idle; nessun altro writer D9 rilevato. Questi controlli
non costituiscono un lock globale sulle applicazioni.

## Fonti e contratto

Letti MAINTENANCE nella base pertinente, handoff rev03 come stato operativo,
skill fot-tep-harness-lessons e relativo riferimento; prompt Fase, Prompt,
Verifica, Documentazione e Commit; contratti harness/R4/D03/D04. Fonti D9,
piano rev.10, budget e DELTA_HARNESS, inventario/checklist/richiesta dei servizi
sono conservati separatamente con commit, dimensioni e SHA-256 in
[SOURCES.json](d9_evidence/SOURCES.json). Le sette copie coincidono con i blob
indicati. Non sono nuove versioni concorrenti dei documenti autorevoli.

Il [contratto prima del codice](CONTRATTO_D9_PRIMA_DEL_CODICE.md) ricostruisce
configurazione → acquisizione → binding/ledger → rilettura/resume →
validazione → CLI/runner → prompt → contabilità → invio.
Il [contratto dei campi D9](d9_evidence/D9_FIELD_CONTRACT.json) classifica i nuovi
valori normativi e i punti di decisione. Le colonne, eventi, prove raw, retry,
quote cumulative e regole di transazione D04 restano nella loro versione.

## Modifiche implementate

1. Ruoli fissi P=C=122B, P_alt=27B: configurazioni producer improntate per ruolo,
   due servizi documentati distinti, nessun consumer 27B, Terra o fallback.
   La sola promozione nominale APPROVED del vecchio config viene rifiutata.
2. Prerequisiti D9 riletti all'ingresso, nel binding persistito e nelle decisioni
   del ledger, compresi i contributori alla quota e il riuso dopo restart.
   I byte del provider persistito devono coincidere con il file autorizzato.
3. I payload 122B omettono `temperature`; anche null o 0.6 nella generazione
   sono rifiutati. Seed e thinking sono espliciti, senza inventare supporto.
   La chat usa i pin del servizio; la validazione degli insight usa separatamente
   il tokenizer R4 canonico. Capienza completa e massimo output sono controllati.
4. La conformità produce la libreria: non ne richiede una preesistente.
   Primaria e alternativa sono autenticate separatamente dai raw e dai rispettivi
   PASS, 16 insight ciascuna. I successivi prompt consumer completi mantengono
   14 peer. `swap_manifest` sostituisce soltanto gli insight e conserva i casi
   forniti, con consumer 122B fisso; non sceglie nuovi casi.
5. Collocazione alternativa esplicita: PENDING blocca; `pilot` esige il PASS
   alternativo prima della sonda; `deferred` vieta quella conformità nel pilot.
   Nessun nuovo stadio differito o contabilità in G_A viene deciso implicitamente.
6. Contabilità derivata dagli intenti durevoli, inclusi incerti/retry, per ruolo e
   modello nominale; P+C aggregati a 122B. Riconciliazione S deve riferire i quattro
   request ID e le identità già presenti nel ledger autorizzato. Nessun reset,
   importazione, backfill o riscrittura viene eseguito per soddisfare il requisito.
7. Le CLI accettano `--config`; il nuovo
   [config pending](../config/pilot_d9_pending.json) espone ruoli approvati e
   lacune, ma impedisce l'esecuzione prima di creare un ledger. L'ordine 1a
   richiede un proprio documento di approvazione e non deriva dal label_space.
   Mapping, derangement e sorteggio 03.7 rimangono invariati.

`server_contract` conserva ora provenienza **documentata**, marcata
`DOCUMENTED_NOT_LIVE_VERIFIED`. Non inventa PID, fingerprint di processo,
revisioni o osservazioni API per servizi remoti. La qualificazione reale resta
necessaria nei futuri stadi autorizzati; una corrispondenza dell'alias restituito
non prova crittograficamente i pesi. Nessuna dichiarazione generica vale come
prova zero-token D03.

## Prove realmente eseguite

| Prova finale | Esito | Log |
| --- | --- | --- |
| Suite mirata, 145 metodi | 145/145; 0 errori/fallimenti; 453.539 s | [targeted.log](d9_evidence/targeted.log) |
| Discovery, 180 metodi | 180/180; 0 errori/fallimenti; 452.525 s | [discovery.log](d9_evidence/discovery.log) |
| D9 discriminanti, 17 metodi (inclusi sopra) | 17/17; 6.657 s | [d9_final.log](d9_evidence/d9_final.log) |

Ambiente finale: Python Anaconda 3.13.9, SQLite 3.51.0, macOS arm64;
[runtime](d9_evidence/runtime.json), [comandi](d9_evidence/COMANDI.md) e log
sono conservati. Suite sovrapposte, non sommabili; conteggi dei metodi distinti
da assertion, sottocasi e processi. La prova consumer include l'adattatore reale
con SDK fittizio e tre payload catturati senza temperature, oltre ai controlli
negativi e ai positivi di libreria/resume/contabilità.

Stessi byte finali di `test_d9.py` sull'antecedente tecnico esatto:
17 metodi, **3 fallimenti comportamentali + 14 errori per API D9 assenti**.
I tre fallimenti sono approvazione nominale senza D9, temperature 122B ammessa,
provider principale utilizzabile come alternativo. Non sono nuovi NON OK D04;
il requisito scientifico D9 è un delta. Le API nuove non hanno un positivo
eseguibile sull'antecedente: questo limite è dichiarato, non convertito in un
confronto comportamentale. Sul delta gli stessi metodi passano.

[Adattamenti e limiti](d9_evidence/ADATTAMENTI_E_LIMITI.md): fixture runner D9
sintetiche; C01/D02 dichiarano pilot prima del binding; D01 legacy scientifico
senza D9 si arresta prima della precedente rematerializzazione. Positivi del
ledger generico e assertion D02/D03/D04 mantenuti. Non si descrive l'intera suite
come ripetizione letterale delle fixture D04. I log intermedi includono errore
ABI Python di sistema, NameError corretto, run interrotto e fixture D02 corretta;
nessuno di questi è conteggiato come verde finale.

Guardiano **NON PASS invariato**, 35 test, 14 fallimenti, 1 skip, 0 errori.
Tutti gli identificativi e i subtest coincidono prima/dopo e con D04:
[confronto nominativo](d9_evidence/guardian_comparison.json).
Compilazione in memoria: 98 sorgenti, zero errori. Nessuna compilazione esegue
script forensi. Link nuovi e perimetro controllati; nessun aggiornamento di coppie
MD/HTML o indici generali, dato che non cambia la struttura autorevole.

## Integrità e manifest

[HARNESS_D9_CANDIDATE.json](HARNESS_D9_CANDIDATE.json): SHA-256 `356e87d29028a80488a6acfde66b7551bacde94481eba3389922e04124625668`,
141 membri, ciascuno con dimensione e impronta. Include i file diretti del
precedente manifest alle loro versioni attuali e i nuovi artefatti D9; non
riscrive il manifest D04. Esclude se stesso e il successore documentale per
non creare riferimenti circolari. `CONSEGNA_D9.json` lega manifesto e tecnico.
I file Python inventariati all'avvio delle suite sono confrontati coi byte finali;
il manifest lega quei byte al commit tecnico, senza chiamare eseguiti tutti i
file semplicemente inventariati.

Confrontati 2.822 file harness non modificati con i blob della base durante
l'audit di conservazione. Le successive scritture riguardano solo D9. Acquisizioni
D04, NON OK, CONSEGNA_D04 con pending storico, manifest certificati, preflight,
schema, metriche e ledger scientifici reali preservati. I due verbali restano:

- Codex: 21.340 byte, `2fc9ed8e3303a779833f1b1dced7f9a70022603118d985280722bed0156a8fef`.
- Claude: 11.864 byte, `0ce2cb9485e5047c5e87eed6f69d0f8ddd3e1b09a2c4a005f0a42e92ef4dc83c`.

Il loro record mantiene distinti Codex 128/128 mirati e 163/163 discovery da
Claude 127 verdi + 1 env-bloccato fra 128 mirati. Restano risultati attribuiti
alle review D04; non sono il risultato della preparatrice D9. Non sono riaperte
le chiusure R01–R10/C01–D04, né rieseguiti i launcher storici per estenderle.

## Prerequisiti e limiti ancora bloccanti

- Metadati effettivi dei due servizi, configurazioni esatte, pesi/revisioni,
  tokenizer/template recuperabili, identità, parametri e limiti documentati;
  verifiche e qualificazioni reali ancora non svolte. 0.6 è default dichiarato.
- Approvazione dell'ordine prompt-facing 1a separata da label_space e mapping.
- Decisione esplicita sulla collocazione della conformità alternativa e relativa
  contabilità; eventuale percorso post-gate non implementato in assenza di specifica.
- Riconciliazione S: quattro richieste riportate, tre inferenze completate.
  Il delta valida un futuro raccordo alle identità durevoli, ma non produce quel
  raccordo e non migra una storia che non soddisfa D03/D04. Necessaria acquisizione
  e review separata della riconciliazione; la storia fittizia vuota vale solo nei test.
- Insight reali, capienza effettiva, T5 e qualificazioni, autorizzazione esatta
  per il pilot; review indipendente di questo candidato prima della documentazione
  condivisa. Nessuna selezione dei ruoli dalle prestazioni.
- La helper swap conserva casi già forniti; selezione definitiva e runner dello
  studio finale restano fuori da questo delta. Test finiti non dimostrano tutti
  gli interleaving, tutte le alterazioni coordinate di fonti o uso arbitrario di
  metodi interni fuori da `execute_request` e dai runner autorizzati.
- Conservazione esterna/futura integrazione resta soggetta a MAINTENANCE §8.5;
  le prove locali e gli hash non sono pubblicazione di un pacchetto remoto.

Nessuna chiamata a servizi, inferenza, simulazione TEP, pilot, produzione di
insight reali, invio a terzi, push, merge o tag. La consegna termina al candidato
locale e al prompt per la successiva review indipendente, senza autoattribuire OK.

Il controllo whitespace del tecnico segnala soltanto tre righe del log grezzo
del guardiano e una riga vuota finale del run interrotto: byte conservati.
Il controllo dei nuovi record documentali è separato; nessun errore di codice
o formattazione dei nuovi Markdown viene mascherato da questi log.

[Controlli della consegna documentale](d9_delivery/CHECKS.json): manifest e
byte testati confrontati con il tecnico, link risolti e guardiano ripetuto
dopo la scrittura dei nuovi record, con gli stessi identificativi storici.
