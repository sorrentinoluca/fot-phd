# Acquisizione delle due review D04 — OK limitato offline

**15 settembre 2026 — consegna locale documentale. 03.10 e Fase 03 restano aperte; nessun GO o freeze.**

## Oggetto e provenienza

Si acquisiscono i due OK indipendenti sul solo candidato tecnico
`aae29a908356e4a4842a214fdc3db9bff26ec3ca`, tree
`4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`.
La base di questa acquisizione è `feaf1d3c56ff142e1d1b4bc4dd243348c20bcb98`,
successore documentale, non candidato tecnico. Il nuovo commit documentale è il commit
che introduce questo record, identificabile con `git log --diff-filter=A -- studio2/fase03/harness/ACQUISIZIONE_OK_D04.md`.

| Revisore | Originale letto integralmente | Copia separata | Byte | SHA-256 |
| --- | --- | --- | ---: | --- |
| Codex | `/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/evidence/VERIFICA_D04.md` | [Verbale Codex](d04_ok_20260915/codex/VERIFICA_D04.md) | 21340 | `2fc9ed8e3303a779833f1b1dced7f9a70022603118d985280722bed0156a8fef` |
| Claude | `/Users/luker/fot-tep-harness-0310-d04-checks/VERIFICA_D04.md` | [Verbale Claude](d04_ok_20260915/claude/VERIFICA_D04.md) | 11864 | `0ce2cb9485e5047c5e87eed6f69d0f8ddd3e1b09a2c4a005f0a42e92ef4dc83c` |

Impronte confrontate con il mandato prima della copia, poi rilette su originali e copie.
Nessuna riscrittura dei verbali, compresi formulazioni, percorsi assoluti e limiti storici.
L'[inventario di acquisizione](d04_ok_20260915/ACQUISITION_INVENTORY.json) registra
origine, destinazione, byte, SHA-256 e modalità di conservazione di ogni membro.

Identità **dichiarate e documentate nelle fonti**, non dedotte dai risultati:

- Codex: sessione revisore `01a0a1ec-35a4-7870-9c39-9bf922d36c85`, `gpt-6-astra/high`;
  preparatrice distinta `01a0a204-abda-7a00-8466-f52f5bc84812`, `gpt-6-astra/xhigh`.
  Indipendenza di finestra, nessuna diversità di modello. Conservato [runtime.json](d04_ok_20260915/codex/runtime.json).
- Claude: sessione configurata `claude-opus-4-8`; backend effettivamente servito non
  dimostrabile dall'interno. Il verbale non fornisce un identificativo univoco di sessione.
- Questa acquisizione: Codex, sessione `01a0a53e-927d-7493-a50a-34617bbac13f`,
  incarico documentale sul worktree preparatore; non è una terza review indipendente.
  La sessione attuale è distinta dalla precedente preparatrice: non ne assume l'identità.

## Risultati acquisiti, non rieseguiti in questa finestra

| Ambiente della review | Risultato attribuito | Limiti conservati |
| --- | --- | --- |
| Codex, macOS, Python 3.13.9 / SQLite 3.51.0 | 128/128 mirati; 163/163 discovery; D04 8/8 | Suite sovrapposte, non sommabili. Differenziale: 240 assertion fallite in 6 degli 8 metodi sul respinto. |
| Claude, VM Linux, Python 3.10.12 / SQLite 3.37.2 | 128 mirati raccolti: 127 verdi + 1 env-bloccato; D04 8/8 e sonda propria | `test_D03_real_legacy_proofs_rejected_without_rewriting_history` bloccato dal percorso hard-coded. Discovery scientifica e singoli launcher V/W/Y/Z/X non convertiti in PASS. |

Codex conserva V 6/6, W 4/4, Y 7/7, Z 5/5 e nuove U 5/5.
X01–X18: 18 letterali verdi; X19–X24: cinque letterali verdi e X23 letterale obsoleto
fallito; X23 già adattato: 1/1. Non sono «24/24 letterali».
Applicabili: 14/14, dodici letterali e N20/N21 con sola fixture/argomento adattati.
La matrice nominativa dei 50 metodi conserva dodici letterali, due adattamenti di
fixture/argomento, 35 adattati/accorpati e N48 equivalente a C02 nella nuova API:
non «50/50 letterali». Metodi, coordinate, sottocasi, assertion e processi restano distinti.

Il guardiano nella review Codex è **NON PASS**, 35 test, 14 fallimenti storici,
1 skip, 0 errori, identificativi invariati; non bloccante per quel delta offline.
Claude non lo ha eseguito e ne riporta lo stato storico: il suo limite resta tale.
Le esecuzioni macOS documentate da Codex forniscono il riscontro nell'ambiente di
riferimento richiesto dalla conclusione Claude, senza riscrivere i risultati Linux.

L'OK registra la chiusura D04 nei casi e ingressi verificati: inventario dei tentativi
validato al punto della decisione, nella transazione, includendo gli altri stadi
contribuenti. D03 conserva digest ricalcolabili e legame durevole delle prove zero-token;
legacy senza digest/link resta fail-closed, senza backfill. Non vengono riaperti
R01–R10/C01–D04 né trasferiti gli OK ai candidati respinti o a byte futuri.

## Conservazione delle prove e dello storico

Acquisiti **80 file byte-identici**: 79 del pacchetto Codex (verbale, risultati,
log, comandi, script, matrici, inventario e SHA256SUMS), più il verbale Claude.
Verificati tutti i 1.962 membri dell'inventario originale Codex e tutti i membri
SHA256SUMS; gli ulteriori due file sono inventario e SHA256SUMS stessi.
Le **1.885 fixture** restano esterne nelle coordinate originali registrate, rilette
per dimensione/impronta, non soltanto elencate. Otto symlink sono registrati con target,
verificati senza attraversarli né materializzarli nella copia.
Le fixture volutamente false sono prove forensi: non sono input scientifici né
configurazioni autorizzate. Nessuno script acquisito è stato eseguito.

Per Claude è disponibile qui il verbale, **non i log scratch della sua VM**.
Gli altri file in `fot-tep-harness-0310-d04-checks` sono le prove macOS della
preparatrice già conservate dalla consegna D04: non sono nuove prove Claude.
Nessuna fonte mancante è ricostruita. Le coordinate esterne sono recuperabili e
verificate localmente oggi; questo non è pubblicazione né garanzia di conservazione
remota. Per futura integrazione/freeze resta da soddisfare MAINTENANCE §8.5 sul
pacchetto completo, senza pretendere che gli hash sostituiscano gli artefatti.

[CONSEGNA_D04.json](CONSEGNA_D04.json) mantiene
`LOCAL_TECHNICAL_CANDIDATE_PENDING_INDEPENDENT_REVIEW` e il pending interno storico.
Questo record successivo registra `ACQUIRED_OK_LIMITED_OFFLINE`; non modifica la
consegna, il manifest tecnico, i precedenti NON OK, gli originali o altri byte certificati.

## Controlli di questa acquisizione

Prima delle scritture: worktree `/Users/luker/fot-tep-harness-0310-d04`, branch
`codex/studio2-harness-0310-d04`, HEAD atteso e tree tecnico verificati; stato locale
pulito, acquisizione non ancora presente, nessun index.lock. Remoto effettivo
`https://github.com/sorrentinoluca/fot-phd.git`; `git ls-remote origin refs/heads/main`
restituisce `a00605862f627710347bd63c49f79a6d0a00135f`.
Inventario dei worktree e attività consultati: preparatrice e revisore Codex idle;
la task orchestratrice consultata ha terminato la preparazione dei prompt, senza
scritture D04. Nessuna attività concorrente di scrittura rilevata nel worktree;
controllo ripetuto di HEAD/stato prima di scrivere e del perimetro prima del commit.
Non si pretende un lock globale su tutte le applicazioni.

Eseguito soltanto `python3 docs/test_explanation.py` prima/dopo, come richiesto da
MAINTENANCE §5: **35 test, 14 fallimenti, 1 skip, 0 errori**, NON PASS invariato,
confrontati identificativi e subtest, anche contro la review Codex.
Log e confronto in [controlli](d04_ok_20260915/ACQUISITION_CHECKS.json).
Controllati link del nuovo record, copie/impronte e assenza di delta sui file già
tracciati. Nessuna suite harness, inferenza, simulazione, API provider o pilot.
`git diff --cached --check` segnala soltanto whitespace nei byte originali delle
prove acquisite e nei log grezzi del guardiano: conservati intenzionalmente.
Il controllo sui nuovi record Markdown/JSON è pulito.

Letti MAINTENANCE del worktree, handoff rev03, skill e prompt pertinenti
Prompt_LLM/Commit_LLM/Documentazione_LLM/Verifica_LLM, §0 del walkthrough e prompt
D04; entrambi i verbali integralmente, inventari e prove documentali pertinenti.
Lettura narrativa dell'ordine di 100 kB; confronti meccanici dei byte separati.
Il mandato termina all'acquisizione: nessun aggiornamento condiviso, nessuna copia
arretrata del walkthrough importata. La coppia MD/HTML e la sintesi divulgativa
restano intatte; nessuna chiusura di sottofase o fase da documentare in questa sede.
La nuova cartella è un contenitore di prove dentro l'harness già censito, non una
nuova categoria dell'indice generale.

## Residui per il successivo delta D9

D9 approvata: 122B producer principale e consumer; 27B producer alternativo con
libreria completa di 16 insight; consumer 122B fisso nello swap; Terra storico
interno. I ruoli non richiedono nuova approvazione. Restano separati recepimento
**eseguibile** D9 e sua review sul nuovo delta, ordine label 1a ancora non approvato,
metadati/configurazioni reali, tokenizer/template/identità, insight reali, capienza,
qualificazioni e T5, riconciliazione del consumo storico e mandato per il pilot.
Il preflight storico resta bloccato. Nessun push, merge, tag, invio a terzi,
freeze dell'intera 03.10 o GO è effettuato o autorizzato da questo record.
