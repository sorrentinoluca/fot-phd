# Acquisizione della verifica indipendente del delta 03.15

Data: 2026-09-14, Europe/Rome. **OK indipendente acquisito** sul delta
`bcb462d..91a880b` e sulla coerenza delle cinque sezioni comuni risultanti,
con fonti main a `c486eee`. La sotto-fase 03.15 e la Fase 03 restano aperte.
Questo record registra una verifica esterna; non è una nuova certificazione del preparatore.

## Oggetto e acquisizione byte-identica

| Elemento | Identificazione |
| --- | --- |
| Base scientifica immediata | `bcb462da3f3c329af5b80d9cb028bb8893a8d09d` |
| Candidato verificato | `91a880b136dee5d805b54040f5e32345be361eb2` |
| Consegna report, prompt e controlli | `dc6e30c60de79df00841981ac0305f127f811a06` |
| HEAD destinatario prima dell'acquisizione | `dc6e30c60de79df00841981ac0305f127f811a06` |
| Branch destinatario | `codex/studio2-paper-sections` |
| Worktree destinatario | `/Users/luker/fot-tep-paper-sections`, pulito prima della scrittura |
| Verbale acquisito | [VERIFICA_DELTA_0315.md](VERIFICA_DELTA_0315.md) |
| Dimensione | **12.311 byte** |
| SHA-256 | **`00553079e88a58a68762ba9a3400c04cb22b91f6a99f37f191b67cfd12ca9770`** |

Sorgente letta:
`/Users/luker/fot-tep/.worktrees/verifica-delta-0315-91a880b/studio2/fase03/paper_sections/VERIFICA_DELTA_0315.md`.
Copia binaria senza normalizzazione di newline, intestazioni o contenuto; byte,
dimensione e SHA-256 confrontati con la sorgente. L'impronta completa coincide
con il prefisso `00553079` e la dimensione comunicati dall'autore.

Il report consegnato resta invariato, SHA-256
`1f59eabf8070f1f4b7b77d89564d4e3593308469e8d8aee56676c93dbabd40f1`.
Il suo stato «preparato per verifica» è storico: il presente record registra
l'esito successivo senza riscriverlo. Fonti, controlli del preparatore, prompt e
bozze non sono stati modificati per acquisire l'OK.

## Revisore e limiti d'identificazione

Il verbale identifica **Anthropic**, configurazione di sessione
**`claude-opus-4-8` (Claude Opus 4.8)**, sessione
`session_0156FoAbkYa4cWpud246SqXC`, task/mount
`rcw-0156foabkya4cwpud246sqxc`, ruolo di revisore indipendente.
Reasoning/effort **non esposto/non verificabile**. Il revisore precisa che
l'identità del modello che serve il singolo turno può differire dalla
configurazione e non è esposta al runtime: qui non viene attribuita una precisione
maggiore. Le fonti dichiarate sono configurazione/system prompt di sessione,
metadati dispositivo e Git; questa acquisizione non ha accesso ai metadati cloud
per una verifica ulteriore.

Provider e sessione dichiarati sono distinti dall'esecutore OpenAI `gpt-6-astra`,
`high`, task `01a0a0bb-1683-7dd0-b29b-edfffb83de56`. L'OK è quello del revisore
esterno, non una rilettura dell'esecutore.

## Esito e perimetro preservato

Il verbale riporta otto controlli scientifici positivi, 54/54 fonti confermate
per byte/SHA-256, lint di cinque file senza segnalazioni, diff senza errori di
whitespace e guardiano con 35 test, 14 fallimenti storici, un salto e zero errori,
con identificativi e subtest coincidenti. Questi sono esiti attribuiti alla
verifica esterna, non test scientifici ripetuti durante l'acquisizione.

La frase sintetica del verbale «nessun numero di esito nelle bozze» va letta nel
perimetro diagnostico esplicitato dal verbale stesso: il suo controllo 3 verifica
espressamente soglia e FAR già prodotti in 03.5 e presenti in `verbalizer.md`.
Il testo indipendente resta byte-identico; non si cancellano quei riscontri di
calibrazione né si trasformano in prestazioni dei modelli.

L'OK storico su `cf79e81f917c7969dfd375e38db54315c28d4c07` resta distinto e
preservato, insieme al precedente NON OK. Il relativo verbale
`VERIFICA_PAPER_SECTIONS.md` conserva **13.949 byte**, SHA-256
`8faca80c87071d87bf66d97848c290a5724f6569be6f6040cfb6568bad022cb1`.
L'acquisizione attuale non estende l'OK ad altri commit scientifici o a future integrazioni.

## Preflight e portabilità dei percorsi

Al momento dell'acquisizione `origin/main` locale e `git ls-remote origin
refs/heads/main` coincidono su `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`.
Il branch locale `main` resta a `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155`:
non è stato usato come fonte aggiornata né spostato.

La sessione di review poteva accedere alla sola cartella `/Users/luker/fot-tep`:
il revisore dichiara di avere recuperato prompt, report e candidato dagli oggetti
Git, verificando le impronte, e usato il worktree isolato interno a `.worktrees/`.
Durante questa acquisizione il file `.git` del worktree di verifica e il relativo
backlink `gitdir` puntano ancora al mount `/sessions/rcw-0156foabkya4cwpud246sqxc/...`.
Per questo `git status`/`rev-parse` lanciati dalla cartella macOS sorgente falliscono;
il file amministrativo locale `.git/worktrees/verifica-delta-0315-91a880b/HEAD`
contiene `91a880b136dee5d805b54040f5e32345be361eb2`, coerente con il verbale.
Si distingue questo riscontro dall'esito Git della sessione remota.

Nessuna riparazione dei puntatori, rimozione di lock o cancellazione del worktree
è stata eseguita in questa acquisizione. Il messaggio dell'autore riferisce la
rimozione successiva di lock orfani, mentre il verbale conserva lo stato rilevato
prima: non si riscrive il verbale per aggiornare l'igiene successiva. Worktree,
verbale sorgente e nota `claude/sessione_2026-09-14_verifica_delta_0315.md` restano
fuori dal commit di acquisizione e non sono rimossi.

Per sessioni che montano solo la cartella principale, recuperare il verbale dal
commit locale di acquisizione indicato nella consegna, senza affidarsi a un
percorso fratello o a un HEAD mobile:

```bash
git -C /Users/luker/fot-tep show <commit-acquisizione>:studio2/fase03/paper_sections/VERIFICA_DELTA_0315.md
```

## Controlli dell'acquisizione e residui

Controlli locali: copia binaria e impronte coincidenti; lint cinque file/zero
segnalazioni; guardiano prima/dopo 35 test, stessi 14 fallimenti e un salto,
zero errori, con preambolo e identificativi dei subtest identici; link del record
risolto; `git diff --check` del nuovo record senza segnalazioni. Le bozze e tutti
i file già tracciati sono byte-identici a `dc6e30c`.

Il commit comprende soltanto il nuovo verbale e il presente record. Nessuna
modifica al walkthrough, alle bozze, al raccordo seriale, ai manifest o ai report
storici; nessun merge, push, tag, simulazione, inferenza o chiamata sperimentale.

Restano aperti documentazione e integrazione coordinate della 03.15, D9 e
qualificazione/identità dei modelli, firma e freeze statistico, fattibilità T5,
ledger/calendario, raccordi 03.10 e controlli tecnici OOD secondo B. FAR, A/B e le
altre approvazioni restano ferme. L'OK non autorizza pilot o pubblicazione, non
produce risultati diagnostici e non chiude la sotto-fase 03.15 o la Fase 03.
