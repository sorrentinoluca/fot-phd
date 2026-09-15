# Acquisizione della riverifica D9 — OK limitato offline

**15 settembre 2026 — record documentale successivo. R-D9-01 e R-D9-02 chiusi nei casi offline verificati dal revisore. 03.10 e Fase 03 restano aperte; nessun GO o freeze.**

## Oggetto, provenienza e pin

Acquisizione su mandato esplicito di Luca, ricevuto in questa conversazione;
data e ora effettive del controllo locale sono registrate nell'[inventario](d9_ok_20260915/ACQUISITION_INVENTORY.json).
Non sono una firma o un timestamp attribuito all'autore.

| Oggetto | Identità |
| --- | --- |
| Tecnico corretto oggetto dell'OK | `16c98f39c044d812458705234b1a3f8ee4940b34` |
| Tree tecnico | `1dd8f84d991190d9d8316e6c56899bc115232716` |
| Successore documentale precedente / base dell'acquisizione | `cf763333b7951b4cf711e1286657f6afc6a9df87` |
| Tree della base documentale | `aed9e805c7846fd4cb211ef1dc13440dcfb6aead` |
| Tecnico respinto, NON OK preservato | `6a8031b25aa1208047d79cc7f030bf9cf7841e67` |
| Worktree | `/Users/luker/fot-tep-harness-d9-correzioni` |
| Branch | `codex/studio2-harness-d9-correzioni` |

Il nuovo commit documentale è quello che introduce questo record, recuperabile
con `git log --diff-filter=A -- studio2/fase03/harness/ACQUISIZIONE_OK_CORREZIONI_D9.md`.
Non cambia il tecnico, i test, le fixture certificate o i manifest preesistenti.

Fonte originale: `/Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review/outputs/d9-corrections-review`.
Letti integralmente verbale e consegna; il manifest è stato letto e verificato
meccanicamente per ogni membro, non soltanto campionato.

| Fonte acquisita byte-identica | Byte | SHA-256 |
| --- | ---: | --- |
| [Verbale](d9_ok_20260915/review/VERIFICA_CORREZIONI_D9.md) | 13627 | `55331f43053a8daeb36bc0af7771f3d4c099b6524d998d53109da5c9b18b9f32` |
| [Manifest della review](d9_ok_20260915/review/MANIFEST.json) | 101057 | `7f83eb38458011fdd4cc70221b1070193dcd630d6392e3110a4e5fee07ef105d` |

La [consegna originale](d9_ok_20260915/review/CONSEGNA.json) collega questi due oggetti.
Il manifest della **review ha 446 membri**, oltre ai due file esterni al suo
elenco MANIFEST.json e CONSEGNA.json. Il [manifest del candidato corretto](d9_corrections/CANDIDATO_CORREZIONI_D9.json)
ha invece **1062 membri**, 282272 byte, SHA-256
`a2fbabcaa997831446c4c2775d62fa6fc2078229a4c71187337be30a9ae7e4e1`.
Sono perimetri diversi. Né questi inventari né i 425 Python inventariati nella
review rappresentano un conteggio di test eseguiti.

Il verbale dichiara revisore Codex, agente basato su GPT-6, task
`01a0a579-3fd7-7461-8c26-5449bd3d2b7a`, «Review indipendente D9 — candidato 6a8031b»:
stessa finestra del precedente NON OK, distinta dalla preparatrice. Conserva
il limite sull'identificazione di variante, pesi e backend e non rivendica
diversità di famiglia del modello. Questa acquisizione è della task
`01a0a1c2-a5fd-7621-a360-ce326c026188`: non è un'altra review indipendente.
L'integrità locale rispetto a mandato, consegna e manifest è verificata;
non equivale ad autenticazione crittografica della provenienza.

## Risultati attribuiti al revisore, non rieseguiti qui

I [risultati verificati dal revisore](d9_ok_20260915/review/evidence/RESULTS_VERIFIED.json),
i rispettivi comandi e i log originali sono conservati.

| Prova del revisore | Risultato acquisito |
| --- | --- |
| Mirata completa sul corretto | 156/156, zero fallimenti/errori/skip |
| Discovery completa sul corretto | 191/191, zero fallimenti/errori/skip |
| Correzioni, stessi byte finali | Respinto: 11 metodi, 32 assertion/subtest falliti, 0 errori; corretto: 11/11 |
| U01–U08 originali byte-identici | Respinto: 8 metodi, 3 fallimenti, 0 errori; corretto: 8/8 |
| Trasporto reale con SDK fittizio, stessi byte finali | Respinto: 3 metodi, 2 fallimenti, 0 errori; corretto: 3/3 |
| Due controlli indipendenti aggiuntivi | 2/2 sul corretto; non parte del differenziale rosso/verde |
| Guardiano su respinto e corretto | **NON PASS storico invariato: 35 test, 14 fallimenti, 1 skip, 0 errori** |

Mirata e discovery si sovrappongono e non si sommano. Metodi, assertion, sottocasi
e invii fittizi restano distinti. Il revisore ha eseguito il rosso direttamente
sull'archivio del tecnico `6a8031b`, mentre il preparatore aveva usato il successore
`08670fb` con identità del codice verificata: i due resoconti non vengono confusi.

R-D9-01 riguarda il rifiuto preventivo dei placeholder anche con spazi, tab,
NBSP e differenze di maiuscole, senza normalizzare i documenti acquisiti.
R-D9-02 riguarda la riconferma degli snapshot R4 e chat, con pin del ruolo,
al confine di riserva/riuso. Era un difetto **preesistente**, osservato anche
prima di D04: non viene registrato come nuova regressione D04.

Conservati gli adattamenti dichiarati: la prova trasporto è un nuovo test del
preparatore, non lo script osservazionale originale rinominato; i due controlli
aggiuntivi del revisore conservano v1, errore `/var` contro `/private/var`, log,
fixture e aspettativa finale con `Path.resolve()`. ResourceWarning e log
intermedi rimangono originali. Collegamenti ulteriori letti nel codice non
diventano combinazioni di comportamento dichiarate come eseguite.

Il template inline già pinnato resta un positivo legittimo. I binding D9 legacy
senza `tokenizer_snapshot` restano rifiutati, senza backfill, migrazione o reset.
La riconferma dei byte non crea un lock globale contro un writer successivo.

## Conservazione e recuperabilità

**55 file copiati byte-identici** (11541562 byte), compresi verbale, manifest,
consegna, script, comandi, log e inventari. **393 membri esterni** (270679146 byte)
sono conservati e verificati nelle sedi originali: archivio tecnico, fixture
e materiali annidati. Ogni riga dell'inventario distingue copia e conservazione
esterna, fonte, posizione recuperabile, dimensione e SHA-256; i byte sono stati
riletti prima e dopo. Le fixture deliberate non sono metadati, autorizzazioni
o insight reali. Nessuno script acquisito è stato eseguito.

L'[archivio tecnico conservato](</Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review/outputs/d9-corrections-review/candidate_16c98f3.tar.gz>)
ha 253146318 byte, SHA-256
`8b73abf885fec6871538500fe9f31f93d25a7c9d993a721258fe4c734deddb5f`.
Non è duplicato in Git. I link del verbale byte-identico vanno interpretati
nel pacchetto originale completo: in particolare il link relativo all'archivio
non indica una copia nella cartella acquisita. L'inventario fornisce il percorso
assoluto verificato e la mappa per ricostruire il pacchetto senza alterare il verbale.
Le sedi esterne sono necessarie alla recuperabilità dell'acquisizione locale.
Non sono una pubblicazione o garanzia remota: MAINTENANCE §8.5 resta un requisito
per la futura consegna integrata, da attuare con mandato separato.

Preservati e ricontrollati i 591 membri del precedente NON OK, sia nell'originale
sia nella [copia già acquisita](d9_corrections/non_ok_6a8031b/VERIFICA_D9.md), oltre a
manifest e consegna. Il verbale precedente resta 18659 byte, SHA-256
`9e1de541cdebef75eac560aa9eb6261db3da5e3f04484e9fee006dd748e65b45`,
e il relativo archivio da 244633206 byte resta recuperabile localmente.
Le [acquisizioni D04](ACQUISIZIONE_OK_D04.md) mantengono i propri esiti, ambienti
e limiti, incluso il tecnico `aae29a9` e il commit di acquisizione
`5886c6f9d078ee624deaec08763e04c14e96e4f0`.
Nessun pending storico viene riscritto o OK trasferito retroattivamente.

## Controlli dell'acquisizione

[Precontrolli](d9_ok_20260915/PRECHECKS.json) e [controlli finali](d9_ok_20260915/ACQUISITION_CHECKS.json)
distinguono verifiche locali da risultati della review. HEAD, tree tecnico,
branch, pulizia e assenza di acquisizione precedente sono stati verificati prima
delle scritture. Remoto effettivo `https://github.com/sorrentinoluca/fot-phd.git`;
`git ls-remote origin refs/heads/main` ha restituito
`a00605862f627710347bd63c49f79a6d0a00135f`. Questa query Git di sola lettura non
è un contatto con i servizi sperimentali.

Lista task e campionamento descriptor: revisore D9 e preparatrice harness idle;
attività 03.8 distinta, lasciata al proprio writer. Rilevati soltanto cwd dei
processi di questa acquisizione, non file aperti nel candidato. Il primo controllo
automatico troppo restrittivo sul semplice stdout di lsof si è fermato prima
delle scritture; i descriptor sono stati poi interpretati e il campione grezzo
conservato. Non si rivendica un lock globale.

Eseguito soltanto il guardiano documentale prima/dopo, richiesto da MAINTENANCE §5:
NON PASS invariato, stessi 14 identificativi/subtest della review. Non copre questa
acquisizione né i documenti `_v2`; non è prova sufficiente della sua correttezza.
Verificati dimensioni/impronte, provenienza, riferimenti del record e recuperabilità
dei membri esterni. `git diff --check` integrale conserva le segnalazioni nei log
grezzi acquisiti; il controllo dei nuovi record documentali è pulito. Nessuna
normalizzazione delle prove per rendere verde il controllo cosmetico.

Letti contratto del worktree, handoff rev03, skill, prompt di riverifica,
Prompt_LLM/Commit_LLM/Documentazione_LLM/Verifica_LLM e §0 del walkthrough;
letture narrative nell'ordine di 80–100 kB, oltre ai confronti meccanici dei byte.
Nessuna coppia MD/HTML modificata, nessuno spostamento, nuova categoria di indice
o chiusura della fase. Walkthrough, piano, paper e finalizzazione statistica 03.8
restano ai rispettivi writer; questa acquisizione non li aggiorna.

## Residui operativi

Restano metadati e qualificazioni dei servizi, ordine label 1a, collocazione
operativa dell'alternativo, riconciliazione S4/3, autorizzazioni esecutive, insight
reali, capienza e T5. La scelta della collocazione operativa non riapre i ruoli
approvati: 122B producer principale e consumer; 27B alternativo per 16 insight,
senza essere consumer di fallback; consumer 122B fisso nello swap; Terra solo
storico descrittivo interno. Temperature122B omessa; 0,6 dichiarato, non misurato.
Contatore canonico R4 e tokenizzazione del prompt completo restano distinti.
Il consumo S non viene azzerato o duplicato. Nessuna approvazione è dedotta dalle
fixture, nessuna qualifica di servizio o chiusura di 03.10 deriva dall'OK offline.

Nessuna nuova correzione, suite harness, review, inferenza, simulazione, sonda,
pilot, modifica di ledger operativo, invio a terzi, push, merge o tag.
