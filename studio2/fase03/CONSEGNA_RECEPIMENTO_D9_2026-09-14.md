# Consegna locale D9 — matrice di recepimento e rapporto

**Data di completamento della consegna: 15 settembre 2026, Europe/Rome.**
Il suffisso 2026-09-14 identifica la data di acquisizione della decisione, riscontrata
dall’orologio prima del cambio di giorno; non retrodata la preparazione finale.

**Ruoli acquisiti: P=C=122B; P_alt=27B; Terra solo storico descrittivo interno.**
Fonte autorizzativa: [record dell'autore](DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md),
acquisizione 14 settembre 2026 Europe/Rome. Non richiedere di nuovo l'approvazione dei ruoli.
Questa consegna riguarda un record successivo; **nessun recepimento canonico è eseguito**.

## 1. Preflight e perimetro

| Oggetto | Stato verificato prima di scrivere |
| --- | --- |
| Worktree esclusivo | `/Users/luker/fot-tep-proposta-d9` |
| Branch | `codex/studio2-proposta-d9` |
| HEAD iniziale | `95ff8571af02bab79094ed1a6be3f6a7b410c711`, pulito; proposta presente e byte-identica al blob |
| Main remoto e tracking locale | `a00605862f627710347bd63c49f79a6d0a00135f`; verificato con `git ls-remote origin refs/heads/main` e `git rev-parse origin/main` |
| 03.8, sola lettura | `/Users/luker/fot-tep-piano-statistico-chiusura`, branch `codex/studio2-piano-statistico-chiusura-rev10`, HEAD `2520e7abc1cd68785f2789448b509dea5e55ee7d`, pulito al riscontro |
| 03.10, sola lettura | `/Users/luker/fot-tep-harness-0310-offline`, branch `codex/studio2-harness-0310-offline`, HEAD `288dc1926bfd7ab4ce43bb4377a9a0064313ad69`, pulito al riscontro |
| Candidato harness in review | `59b6b93cd9c215e8b687e540f7cd579804b7c66a`, distinto dal successivo rapporto a HEAD 288dc19; nessun esito di review attribuito qui |
| Candidato allineamenti 03.8 | `4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8` nella consegna letta; piano generale in correzione secondo il mandato. Nessuna verifica o importazione di quel lavoro eseguita qui |

Letto il contratto richiesto in `/Users/luker/fot-tep/docs/MAINTENANCE.md` e confrontato
con quello del worktree D9: la copia principale è storica (`819b12e`); il contratto in D9
include anche i vincoli aggiunti sul codice congelato. Entrambi sono rispettati e improntati.
Letti inoltre `docs/prompts/Commit_LLM.md` e §0 del walkthrough come regole, senza modificarli.
Nessun AGENTS.md applicabile trovato nelle directory antenate del file di destinazione.

## 2. Matrice dei recepimenti successivi

Le righe descrivono **lavoro futuro**. I percorsi sono relativi alla radice del worktree
della finestra indicata; non invitano a scrivere nelle altre copie da questa finestra.
Prima di applicare: verificare HEAD/stato/nuove consegne, acquisire il record e le impronte,
identificare il delta rispetto al candidato allora verificato, un solo writer per target.
Non sovrascrivere snapshot in correzione o in review con file di questa vecchia base.

| Finestra / file | Modifica necessaria dopo l'acquisizione | Controllo richiesto nel recepimento |
| --- | --- | --- |
| **03.8 — `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`**, D9, §§7/8.1/8.4/8.10 e rinvii checklist | Registrare P=C=122B, P_alt=27B e Terra interno; sostituire il valore operativo dei rami superati e distinguere ruoli acquisiti da identità/qualifica pendenti. Eliminare l'efficacia automatica dei rinvii al fallback 27B/Terra; preservarne la storia. | Ricerca delle occorrenze D9/2.4T/Terra/27B/122B; nessuna domanda di riapprovazione ruoli, nuovo consumer o nuova produzione Terra; Q8, swap, controlli e statistiche invariati. Delta separato dalla correzione in corso, da verificare. |
| **03.8 — `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`** e `piano_statistico/MATRICE_RESIDUI_CHIUSURA_03_8_REV10.md` | Cambiare il residuo “ruoli non scelti” in “ruoli acquisiti; recepimento/configurazione/qualifica pendenti”, citando il record esatto. | Non trasformare D9 in firma o freeze 03.8; preservare la separazione dai controlli OOD dopo freeze e dai prerequisiti operativi T5. |
| **03.8 — `piano_statistico/CONSEGNA_TECNICA_03_10_DA_REV10.md`**, stato in nuova consegna successiva | Trasmettere l'assegnazione approvata e distinguere dati nominali/tecnici dai ruoli. Usare un record successivo per aggiornare lo stato delle consegne già improntate. | Pin/byte storici preservati, nessun trasferimento dell'OK a un futuro delta senza verifica. |
| **03.8 — `piano_statistico/PIANO_STATISTICO.md`, `BUDGET_RISORSE_REV10.md`, `DELTA_HARNESS_03_10.md`, manifest e atto rev.10** | Non riscrivere il candidato rev.10 verificato per inserirvi D9 retroattivamente: affiancare un recepimento successivo e il futuro prospetto per modello. P e C confluiscono nel 122B, P_alt nel 27B; Terra escluso dalle nuove produzioni. | Impronte rev.10 preservate; formula, A/B, quote, hard stop, R e campi di firma invariati. Nessun parametro operativo approvato per deduzione; eventuale revisione normativa segue procedura autonoma. |
| **03.10 — `studio2/fase03/harness/DECISIONE_D9_ORDINE_LABEL_PENDING.md`**, `SPECIFICA_HARNESS.md`, `REPORT_HARNESS_OFFLINE_03_10.md` | Dopo la review del candidato, predisporre un successore che registri D9 acquisita e superi Terra alternativo/27B fallback. Tenere ordine label 1a come decisione separata ancora pendente. | Nessuna riscrittura del candidato `59b6b93` o dei suoi hash durante la review; diff esatto sul target aggiornato, verifica del nuovo delta, cronologia dei report preservata. |
| **03.10 — `studio2/fase03/config/pilot_preflight.json`**, `PREFLIGHT_03_0.md` e configurazioni provider per ruolo ancora da predisporre | Rappresentare separatamente approvazione dei ruoli e prontezza tecnica. Recepire D9 senza attivare l'esecuzione e senza far diventare `candidate` storico del 27B il consumer corrente. Configurazioni effettive ancora da documentare. | Fail-closed per metadati/qualifiche/autorizzazioni mancanti; nessun semplice “UNDECIDED→GO”; pin distinti pesi/alias/tokenizer/template/serving, omissione temperatura 122B secondo inventario, nessun default o fallback implicito. Nessuna chiave JSON nuova è prescritta da questo record. |
| **03.10 — `harness/PILOT_INPUT_SOURCES.pending.json`, `inputs.py`, `producer.py`, `insight_adapter.py`** | Associare input e librerie ai ruoli 122B principale/27B alternativo. Stesso contratto R4, librerie complete distinte e provenienza; conservare l'assenza degli insight reali finché non prodotti e validati. | 16 insight per libreria, 14 peer; nessuna libreria Terra/mista/fixture promossa a scientifica. Cap/tokenizer canonico R4 separato dalla capienza con tokenizer/template effettivi del consumer 122B. |
| **03.10 — `run_pilot.py`, `producer_probe.py`, `harness/guards.py`, `ledger.py`, `logging_v1.py`** | Collegare il futuro manifest dei ruoli; attribuire le richieste ai modelli effettivi, mantenere consumer 122B nello swap e tutte le guardie. Risolvere i metadati tecnici prima dei futuri stadi autorizzati. | Prove offline del delta: niente fallback 27B, niente invii Terra, niente duplicazioni P=C, reset ledger o nuovi retry; ordine stadi, riserve e gate invariati. L'OK offline non qualifica servizio o T5. |
| **03.10 — `harness/ordering.py`, `render.py`, inventario input (`presentation.author_decision`) e test pertinenti** | Nessuna approvazione 1a da questa D9; preservare il blocco indipendente finché manca una decisione specifica sull'ordine. | D9 acquisita non deve impostare `author_decision=accepted`; mapping/owner/derangement 03.7 byte-identici, nessun nuovo sorteggio. |
| **03.10 — `harness/HARNESS_OFFLINE_CANDIDATE.json`**, report/consegna/test successivi | Dopo il recepimento, identificare nuovo candidato, manifest e prove; conservare il precedente candidato e verbale nel loro perimetro. | Hash e test riferiti al nuovo delta; non trasferire la review in corso ai byte modificati. Controlli documentali e `git diff --check`. |
| **03.15 — `studio2/fase03/paper_sections/protocol.md`, `method.md`, `threats.md`** | Recepire P=C=122B, P_alt=27B, consumer invariato nello swap; Terra esclusivamente storico interno. Sostituire placeholder di scelta ruoli con fonte acquisita, lasciando pendenti metadati, qualifiche e risultati; rami storici non attivi. | Coerenza dei tre testi; nessuna superiorità presunta, confronto aggiunto, pooling Terra/nuovo, qualifica o risultato inventato. Preservare limiti su modello/configurazione/server e parità fra producer; verifica del delta. |
| **03.15 — `FONTI_DELTA_0315.json`**, report e consegne di `paper_sections/` | Conservare il manifest delle fonti già verificato; produrre un successivo inventario/fonti del nuovo delta che citi questo record al suo commit e SHA-256. Aggiornare stato con consegna successiva. | Fonte decisionale distinta da fonte tecnica; vecchi pin/verbali conservati. Walkthrough MD/HTML solo nel passo pertinente dopo verifica, non in questo incarico. |

## 3. Residui: scelte ulteriori, dati e verifiche

| Residuo | Natura e trattamento | Effetto sulla registrazione D9 |
| --- | --- | --- |
| Ordine label 1a | **Scelta ulteriore dell'autore**, non coperta dal mandato. La domanda deve riguardare solo l'ordine, senza riproporre i ruoli. | Nessuno; resta un prerequisito separato del rendering/freeze dei prompt. |
| Eventuale consumer fallback | **Nuova scelta** soltanto se diventa necessaria. Non predisporre un passaggio automatico a 27B. | Nessuno; il consumer approvato è 122B. |
| Quartetto di fault della misura swap | **Rintracciare una scelta pre-specificata**; se manca davvero, occorre una scelta strutturale ulteriore prima della misura. Non dedurla da D11 o dai fault di continuità. Questo mandato conserva i medesimi casi del disegno, non ne nomina nuovi. | Nessuno; non si riapre la scelta dei ruoli né si selezionano casi qui. |
| Collocazione conformità alternativa, `a`, riusi, X/Q, calendario | **Specificazione operativa ulteriore** entro le regole vigenti; distinguere scelte non ancora fissate da calcoli derivati e disponibilità da acquisire. La scelta dei ruoli non approva `a=1` né costi/retry extra. | Nessuno; prima dell'esecuzione pertinente, senza modificare il budget per deduzione. |
| Firma materiale 03.8 | **Atto personale separato**, non un dato tecnico o una seconda approvazione D9. | Nessuno; la firma del piano resta pendente. |
| Repository/revisione pesi, quantizzazione, tokenizer/template, serving, fingerprint e controlli API | **Dati tecnici da acquisire**, non domande per far scegliere all'autore valori ignoti. Distinguere dichiarazione del gestore e riscontro effettivo. | Nessuno; configurazione eseguibile resta incompleta. |
| Limiti input/output/thinking, troncamenti, conformità, stabilità e latenza/T5 | **Verifiche e misure future autorizzate**, con i dati del servizio effettivo e il ledger vigente. | Nessuno; GO e fattibilità non attestati. |

La sola approvazione D9 non stanzia prove. Nessuna data operativa viene inventata o prorogata.
La regola A/B rev.10, FAR, U3 e freeze restano validi; 03.8, 03.10 e 03.15 proseguono nei
rispettivi perimetri senza attendere una seconda decisione sui ruoli già acquisiti.

## 4. Rapporto sintetico e verifica documentale

Il delta aggiunge soltanto:

- [record D9](DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md);
- questa consegna, con matrice e rapporto;
- [impronte e controlli](IMPRONTE_DECISIONE_D9_2026-09-14.json).

Le fonti consultate sono identificate nel JSON per commit, percorso, byte e SHA-256,
comprese le versioni distinte del contratto, la proposta storica e la proposta harness superata.
Il mandato utente non ha un file originale o timestamp di messaggio esposto: il record ne
trascrive il blocco decisionale; l'impronta del record non viene spacciata per hash del messaggio
originale. I metadati tecnici nominali provengono dalla proposta preservata e dal preflight
storico, non da nuove osservazioni dei servizi.

La verifica è documentale dell'esecutore, **non una review scientifica indipendente**.
Nessun walkthrough o coppia MD/HTML modificati, nessun file spostato, nessuna struttura di
cartelle nuova: aggiornamento indici e parità di coppie non applicabili a questo delta.
Controlli finali e impronte degli artefatti sono registrati nel JSON, senza auto-improntare
il manifest. Il commit locale identifica anche il manifest stesso, evitando un autoriferimento.

Il guardiano `python3 docs/test_explanation.py` è stato eseguito prima e dopo: **35 test,
14 failure storici, 1 skip, zero errori**, con identici identificativi e subtest; nessuna
regressione, ma non è una suite PASS. Verificati 17/17 snapshot fonte, 6/6 link e 28/28
percorsi destinatari; proposta preservata byte per byte; `git diff --check` sul delta staged
senza rilievi. Nessuna suite sperimentale o prova sui modelli eseguita. Dettagli nel JSON.

Nessun push, merge su main, tag, importazione del lavoro parallelo, chiamata a servizi,
inferenza, simulazione o comunicazione a terzi. HEAD finale è il commit che contiene questi
file, da risolvere con `git log -1 --format=%H -- studio2/fase03/DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md`;
non viene auto-incorporato. Branch resta `codex/studio2-proposta-d9`; stato finale e hash
sono comunicati nella consegna della task. Il prossimo passo è il recepimento seriale nelle
finestre proprietarie, su incarico pertinente e target aggiornati.
