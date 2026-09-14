# Report di preparazione della chiusura 03.8

Data: **2026-09-14**. Preparatore: **Codex GPT-6**, questa sessione; profilo
decisionale/documentale con controlli offline. **03.8 aperta; nuove decisioni A/B
pending; nessuna revisione successiva alla 9 ancora prodotta.**

## Esito e decisioni

Preparati addendum breve A/B, documento da sottoscrivere, budget per blocco e
modello, inventario verificato del candidato bibliografico, delta per la 03.10,
allineamenti da integrare serialmente e prompt completo di verifica indipendente.
La richiesta di approvazione delle due formulazioni concrete è stata presentata
all'autore; nessuna risposta acquisita al checkpoint. Non si applicano A/B come
decisioni approvate e non si modifica il piano rev. 9.

Le decisioni storiche restano valide: D2=8; H1/H2 Hoeffding; H3 Tango, m=0,125,
α=0,05 e sensibilità separata 0,025; gerarchia; reporting agente/fault; D11;
OOD F6/F4 condizionati; politica R/audit/canary; soglie e ordine pilot;
remediation/riserva; seed e undici scorte; tetto 3.700 finché A non approvata.
La firma materiale resta pending. Nessuna nuova approvazione storica richiesta.

## Base, commit e catena delle impronte

Worktree iniziale pulito `/Users/luker/fot-tep-piano-statistico-fix`, branch
`codex/studio2-piano-statistico-fix`, HEAD
`0f1a9bae8b522f614720fa5efe7bd9d2577609ae`, coincidente con il mandato.

| Record preservato | Commit / SHA-256 |
| --- | --- |
| Candidato scientifico rev. 9 | `6015f8fdb1b28e0adad50219466bf13cd988c137` |
| Manifest sottoposto alla review rev. 9 | a `6015f8f`: `586a26239862ed981bed35614486b9596b8f3931d638107ea214c7cb1d40121c` |
| Verbale rev. 9 OK | preservato in `29249a9305c44a44b96e6f49f94e978956ed0ac2`; hash `289a74433d70e2bf911bdea893711ff7a294c75cf74d5e6fa0addbf3ede72a58` |
| Manifest dopo registrazione dell'OK | a `0f1a9ba`: `2b6ad396307be634428d9355d4aa65144b4956d675ccb9e4b47536e4bdaf8d76` |
| Bozza storica autore | `66e04dd2d8dd00fcf0edf6076a9e3f60bb6fd1fdf8c1e86028a9f80c8754fafb`, 43.136 byte |
| Verbale bibliografico OK esterno | `551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`, 30.107 byte |

Il manifest della preparazione è un file nuovo,
[MANIFEST_PREPARAZIONE_CHIUSURA_03_8.json](MANIFEST_PREPARAZIONE_CHIUSURA_03_8.json):
impronta gli artefatti nuovi e gli input protetti, con il precedente manifest
come input, senza includere la propria impronta. Non sostituisce
PIANO_STATISTICO_FREEZE.json. Il commit locale che introduce questo pacchetto
è identificabile con `git log -1 --format=%H --
studio2/fase03/piano_statistico/MANIFEST_PREPARAZIONE_CHIUSURA_03_8.json`;
SHA del commit e SHA del manifest vengono consegnati in chat, senza auto-riferimenti.
Messaggio: `studio2(piano-statistico): prepara decisioni residue e chiusura 03.8`.
Questo checkpoint è di **preparazione**, non commit di congelamento o documentazione finale.

## Budget e dipendenze

Il nucleo a R=3 è 5.184 richieste; aggiungendo swap misura 672, ablation 444 e
OOD 432 si arriva a 6.732, ancora prima di E5/produzione/pilot/canary/tecnica/retry.
L'audit riusa le tre ripetizioni già incluse; E5 resta R=1. Il prospetto completo
è parametrico dove mancano decisioni o misure. Lo scenario esplicitato nel
budget dà 3.142/7.284 prima di retry esterni al pilot, **non totali autorizzati**.
Le vecchie stime ~3.555 e i delta +702/+638 sono preservati come tali.
Il pilot mantiene 152/160 con riserva inclusa e hard stop 200; la sonda non usa
la quota 8 anche quando la remediation non avviene.

È identificato il ciclo presente nella rev. 9: §16 richiede controlli 03.11
prima del freeze e il freeze prima dei run 03.11. B propone una sequenza
senza ciclo, ma **il blocco normativo resta finché B è pending**.
Le condizioni prima del pilot restano distinte da quelle del freeze: il delta
03.10 conserva input di sviluppo, schema, mapping, capienza, identità del modello,
ledger e implementazione verificata delle regole 03.8. Nessun requisito rimosso
per dichiarare artificialmente completata la sotto-fase.

## File nuovi e ruolo

Tutti in `studio2/fase03/piano_statistico/`; nessun file preesistente modificato.

- [ADDENDUM_DECISIONI_RESIDUE_03_8.md](ADDENDUM_DECISIONI_RESIDUE_03_8.md): formulazioni A/B ancora pending.
- [BUDGET_RISORSE_03_8.md](BUDGET_RISORSE_03_8.md): richieste per blocco/modello/R, riusi, tempi e parametri mancanti.
- [DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE.md](DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE.md): atto predisposto, firma vuota e identificazione finale da completare.
- [ACQUISIZIONE_LETTERATURA_03_8.json](ACQUISIZIONE_LETTERATURA_03_8.json): 23 file candidati e 23 protetti, confronto sorgente/snapshot.
- [DELTA_HARNESS_03_10.md](DELTA_HARNESS_03_10.md): modifiche per file/funzione/config e casi offline per il proprietario.
- [COORDINAMENTO_CHIUSURA_03_8.md](COORDINAMENTO_CHIUSURA_03_8.md): delta piano/APERTURA, consegna Letteratura, dipendenze, ordine documentazione/pubblicazione e target.
- [PROMPT_VERIFICA_DELTA_03_8.md](PROMPT_VERIFICA_DELTA_03_8.md): incarico completo per altro modello/sessione; distingue verifica preparazione da verifica della futura revisione.
- [CONTROLLI_PREPARAZIONE_03_8.json](CONTROLLI_PREPARAZIONE_03_8.json): test statistici e identità dei fallimenti documentali prima/dopo.
- [check_preparazione_chiusura.py](check_preparazione_chiusura.py): controllo offline ripetibile di impronte, link, conti e stato pending.
- Questo report: esiti, provenienza e requisiti.
- [MANIFEST_PREPARAZIONE_CHIUSURA_03_8.json](MANIFEST_PREPARAZIONE_CHIUSURA_03_8.json): impronte del pacchetto e dei suoi input.

## Controlli locali, distinti dalla verifica indipendente

- 26/26 test statistici OK con Python 3.13.9 in `/Users/luker/fot-env/bin/python`.
  La suite compie solo i propri piccoli calcoli sintetici temporanei; nessuna
  nuova griglia Monte Carlo o modifica di DESIGN_RESOLUTION.
- Documentazione prima/dopo: 35 test, 14 fallimenti, 1 skip, identiche 14
  identità/subtest; dettagli in CONTROLLI_PREPARAZIONE_03_8.json. Il controllo
  non certifica la letteratura né il walkthrough studio2.
- Manifest rev. 9: **17/17 input/file integri**; manifest stesso con SHA atteso.
- Bibliografia: **23/23** identità sia in sorgente sia in snapshot, 6.407.129
  byte; **23/23 protetti** invariati in entrambe le copie rispetto alla base.
  Nessuna nuova valutazione scientifica delle fonti, nessuna copia di docs/.
- Link locali dei documenti nuovi, validità JSON, contabilità e `git diff --check`
  controllati tramite check_preparazione_chiusura.py e controllo finale del diff.
  Nessuna coppia MD/HTML toccata; nessun aggiornamento di indici necessario.

La nuova verifica indipendente non è stata svolta. Il prompt è pronto per una
finestra con modello distinto dopo l'acquisizione delle decisioni e la produzione
del candidato revisionato. Il preparatore non certifica sé stesso e non usa
l'OK rev. 9 come approvazione delle nuove proposte.

## Requisito di chiusura → prova → stato

| Requisito | Prova / azione residua | Stato |
| --- | --- | --- |
| Base rev. 9 e verbali preservati | 17 impronte + manifest atteso; nessun file storico modificato | **completato** |
| Approvazioni storiche mantenute | bozza autore intatta, riepilogo nell'atto | **completato** |
| Proposte concrete A/B | addendum predisposto e domanda presentata | **completato: preparazione** |
| Approvazione nuova A | risposta esplicita e data da registrare | **pending** |
| Approvazione nuova B | risposta esplicita; finché manca resta il ciclo del §16 | **pending** |
| Nuova revisione successiva alla 9 | dopo risposte A/B, delta e nuova catena impronte | **pending** |
| Firma materiale | atto predisposto; copia sottoscritta e hash da acquisire | **pending** |
| Condizione bibliografica F6 nel perimetro PHM | verbale OK e identità del candidato verificata | **completato** |
| Integrazione bibliografica e conservazione PNG | consegna coordinata predisposta; commit/acquisizione seriali da eseguire | **pending** |
| Piano generale/APERTURA | formulazioni concrete preparate; applicazione sul target corrente da coordinare | **pending: applicazione** |
| Harness 03.10 prima del pilot | delta preciso sul HEAD 5116087; implementazione/test nella finestra proprietaria | **pending** |
| Identità modello, D9 e T5 | dichiarazioni API separate dal vecchio server; pilot/tempi/config non verificati | **pending prima dell'esecuzione pertinente** |
| OOD tecnici e sostituti distinti | controlli 03.11 secondo ordine B se approvato | **pending; non surrogati da PHM** |
| Test statistici e controlli documentali di preparazione | 26/26, baseline documentale invariato, hash/link/conti | **completato** |
| Verifica indipendente del candidato nuovo | prompt completo, nessun nuovo verbale OK disponibile | **pending** |
| Walkthrough in coppia | contenuti e ordine preparati; solo dopo nuovo OK | **pending** |
| Commit finale in origin/main e tag previsto | presentare candidato verificato, target e prove prima delle operazioni esterne | **pending** |

Nessuna chiamata sperimentale, simulazione TEP, inferenza, scelta D9, modifica
03.5, push, merge o tag. Nessuna credenziale acquisita o registrata. Le copie
Letteratura, snapshot e harness non sono state modificate. Nessuna chiusura
dell'intera Fase 03 e nessuna pubblicazione dichiarata.

Letture: contratto e quattro prompt di ciclo più Prompt_LLM, walkthrough studio2
per fonti/stato, piano statistico e sezioni pertinenti del piano generale,
report/manifest/decisioni/verbali, inventario del verbale bibliografico e file
operativi mirati dell'harness. Costo indicativo: alcune decine di migliaia di
parole di documentazione e metadati; non rilettura del corpus dei paper, né
consultazione dei risultati sperimentali o degli output della 03.5.
