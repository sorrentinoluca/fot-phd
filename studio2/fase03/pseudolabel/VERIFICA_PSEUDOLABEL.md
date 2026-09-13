OK

# Verifica indipendente della sotto-fase 03.7

Data: 2026-09-13. Revisore: **Codex, agente basato su GPT-6**, contesto di
revisione separato dall’autore originale **Claude, finestra Cowork**. Verifica
eseguita come sottoagente con propria sessione e worktree detached
`/Users/luker/fot-tep-pseudolabel-review`, HEAD
`fdf06b82a35a92508a8de602a594adba44c08fe6`. Non è stata aperta né simulata una
seconda finestra GUI. L’agente d’integrazione ha corretto soltanto la documentazione;
il revisore ha letto le rettifiche e ha scritto soltanto questo verbale.

## 1. Oggetto e portata del verdetto

Sono stati verificati gli artefatti originali di `fdf06b82`, risalendo a codice,
specifica, catalogo, commit e file del primo studio. Il report originale conteneva
formulazioni da correggere: il verdetto comprende il **riesame delle rettifiche**
nel worktree `/Users/luker/fot-tep-pseudolabel-integrazione`, nei file
`REPORT_PSEUDOLABEL.md` e `DECISIONE_ACCETTAZIONE_V1.md` della stessa sottofase.
Queste rettifiche non sono attribuite retroattivamente al commit originale.
L’OK riguarda questa sottofase e consente la successiva documentazione; non chiude
Fase 03, non approva il pilot e non attesta una pubblicazione ancora da eseguire.

## 2. Riscontri sulle fonti primarie

| Esito | Punto e prova |
| :---: | --- |
| ✅ | **Perimetro.** `git diff --name-status d815ce9 HEAD` contiene esclusivamente gli undici percorsi dichiarati: dieci nuovi file in `studio2/fase03/pseudolabel/` e l’aggiunta §9 a `studio2/PROVENIENZA.md`. Nessuna modifica a `phase_b/`, `code/`, protocollo Q8, schemi, piano o coppie MD/HTML. Worktree inizialmente pulito. |
| ✅ | **Pre-specificazione registrata.** Il commit `221bf58` aggiunge soltanto la specifica; precede `8c90ece`, che contiene codice, test e quattro artefatti; `fdf06b82` aggiunge freeze, report e provenienza. La specifica è invariata tra `221bf58` e HEAD. Questo dimostra l’ordine nella storia Git. |
| ✅ | **Catalogo D1.** Il tag annotato `studio2-fase03-catalogo-D1-frozen-001` risolve ad `ab43f0b20f45cdb475c0caf52c6f7afcbae50891`; il blob `CATALOG_FREEZE.json` al tag è identico al file letto. SHA-256 `68b8461a6382c93e1a5dd8dc6c9def66b26b2ec865f0bc0786dd88fa95acedda`; catalogo `[1,2,3,8,10,13,14,15]`. `git ls-remote origin` conferma tag remoto e commit peeled. Non si interpreta lo stato pending del manifest storico come stato attuale del tag. |
| ✅ | **Label.** Ricostruzione indipendente, senza chiamare il generatore, con SHA-256/base32 dei messaggi della specifica: tutte le otto label coincidono con `PSEUDOLABEL_MAP.json`. Nove valori distinti includendo `Normal`, otto stringhe opache di lunghezza 12, `Normal` di lunghezza 6 e in ultima posizione; `Unknown` assente. Nessun contatore di rifiuto diverso da zero. |
| ✅ | **Assegnazione.** Riordinando indipendentemente i digest `namespace|assignment|identifier` si ottiene F10, F3, F2, F8, F13, F15, F14, F1 per agent_1…agent_8: biiezione completa, conforme a `AGENT_ASSIGNMENT.json` e al blocco `agents` atteso dal protocollo. |
| ✅ | **E.** Enumerazione indipendente dei derangement di sette elementi: 1854. Ricostruiti digest e parole a 32 bit, soglia di accettazione e indici `[1619,1422,1716,1201,919,620,1203,1196]`. Tutte le mappe coincidono, dominio e codominio sono i sette peer, nessun punto fisso, nessuna label locale o `Normal`, nessuna rotazione di un passo. Vista per identificatore coerente. |
| ✅ | **Replay.** `python3 -m studio2.fase03.pseudolabel.pseudolabel_draw --check`: quattro artefatti byte-identici. Nessun comando di scrittura o nuovo sorteggio usato nella verifica. |
| ✅ | **Freeze.** Verificati separatamente SHA-256 e dimensioni di tutti i sette file elencati in `PSEUDOLABEL_FREEZE.json`; ciascuno è anche byte-identico al proprio blob nel `source_commit` `8c90ecec421980211258e9323d4266a32ba70ccd`. Specifica e artefatti v1 non sono stati corretti in luogo. |
| ✅ | **Provenienza.** Letti `phase_b/config/protocol.py` e `phase_b/config/evaluator_side/condition_e_derangements.json`, confrontati con i blob a `c431cd87ee0ef563ad77cc6b0b330e6b61bf9735`: SHA `fa2488d1…` ed `e8a0bdbf…` coincidono con §9 di `PROVENIENZA.md`. Il nuovo codice riscrive il pattern senza import da `phase_b/`; non usa run, soglie, insight o risultati pregressi. La marca pre-specificato riguarda il pattern e la forma dell’artefatto, non l’accettazione successiva della correlazione. |
| ✅ | **Contratto Q8 e precedenze.** Piano §6.5, §8.1–8.4 e D10; walkthrough studio2 §0; `protocol._validate_label_space`, `_validate_derangements`, `peer_insights`: nove label, astensione separata e corruzione dei sette peer che modifica soltanto pseudolabel. Calibrazione e descrittori non sono utilizzati; nessuna precedenza attribuita al piano superato o alla §5.5 dei descrittori. Il test dei validator non equivale a validare un manifest reale o prompt futuri. |

## 3. Test eseguiti

- `python3 -m unittest studio2.fase03.pseudolabel.test_pseudolabel -v`: **21/21 OK**.
- `python3 -m unittest discover -s studio2/fase03/tests`: **16/16 OK**.
- Replay `--check`: **4/4 artefatti byte-identici**.
- `python3 docs/test_explanation.py` prima del verbale: **35 test, 14 fallimenti,
  1 skipped**. Rieseguito dopo: stesso esito e stessi identificativi dei fallimenti.
  La suite non copre questa sottofase; il risultato invariato non prova la sua correttezza.

I test esistenti sono stati letti oltre che eseguiti. In particolare il nome
`test_opacity_no_correlation_with_catalog_order` eccede l’asserzione verificata;
`test_not_the_one_step_rotation` richiede soltanto che non siano tutte rotazioni,
mentre il controllo indipendente sugli otto artefatti conferma che non lo è nessuna.
La guardia di generazione rifiuta le cifre del proprio idv, non ogni stringa
`F` seguita da cifra: quest’ultima proprietà è verificata sulle label v1 realizzate,
non garantita per qualsiasi namespace futuro.

## 4. Rilievi originali e riesame delle rettifiche

1. **❌ originale → ✅ rettifica: lunghezze e confine evaluator-side.** Il report
   dichiarava nove label di uguale lunghezza e «mai in un prompt». Il test e
   `protocol.py` mostrano che l’uguaglianza riguarda le otto opache e che le label
   operative devono poter comparire nei prompt. La rettifica distingue il mapping
   evaluator-side dalle label e rende esplicita l’eccezione `Normal`.
2. **❌ originale → ✅ rettifica: correlazione e ricostruibilità.** Dai ranghi
   ricostruiti su `PSEUDOLABEL_MAP.json`, Spearman è esattamente **−5/6**.
   `|rho|<1` esclude solo una relazione monotona perfetta: non dimostra assenza di
   correlazione. Namespace, algoritmo e dominio pubblico dei fault permettono
   di ricostruire il mapping, anche senza il file evaluator-side. Il report
   corretto e la decisione d’accettazione riconoscono entrambi questi limiti;
   il codice/test v1 restano testimonianza immutata del controllo originale.
3. **⚠️ ordine dichiarato → ✅ anticipo delimitato.** `APERTURA_SOTTOFASI_FASE03.md`
   §5 propone 03.12 → 03.7, mentre la tabella attribuisce a 03.7 dipendenze solo
   da 03.4 e D1. La stessa apertura distingue le proposte dalle decisioni
   confermate. Il report rettificato verbalizza l’anticipo combinatorio:
   schema e contenuto degli insight non sono congelati, la compatibilità con
   03.12 va verificata prima del pilot. Un cambio di formato richiede nuova
   revisione, namespace e file, come già previsto da specifica §8.

**Valutazione della decisione dell’autore.** Conservare v1 è difendibile: non vi
è una soglia pre-specificata di bassa correlazione da applicare, e selezionare
ora un altro namespace o un ordine ad hoc aggiungerebbe una scelta guidata dal
risultato. La decisione registra onestamente che l’accettazione è successiva
all’osservazione e che il requisito letterale iniziale di assenza di correlazione
non è soddisfatto. Questo non cancella la correlazione forte né prova assenza di
effetti di posizione. Le conclusioni future restano riferite alla realizzazione
v1; l’eventuale controllo della posizione va deciso in 03.10/03.12 prima del
pilot, con regola generale riproducibile comune alle condizioni. Nessun
riordinamento compensativo viene richiesto o implementato da questa verifica.

## 5. Limiti della verifica e passaggi successivi

- ⚠️ **Singola esecuzione storica:** storia e log mostrano una specifica precedente
  e un unico insieme registrato; non possono provare che non siano mai avvenute
  esecuzioni non registrate. Il replay deterministico non è evidenza di un nuovo
  sorteggio né una prova retrospettiva del numero di esecuzioni.
- ⚠️ **Uniformità:** il rejection sampling elimina il bias della riduzione modulo
  sotto l’assunzione di parole uniformi; qui le parole vengono da SHA-256 con
  input fissati. È una costruzione pseudocasuale riproducibile, non una prova
  empirica di casualità o indipendenza fra gli otto derangement.
- ⚠️ **Confine dei prompt:** nessuna chiamata a modelli o simulazione è presente
  nella pipeline letta/eseguita. L’assenza di mapping e ingredienti di derivazione
  dai prompt reali va verificata nell’harness futuro; il campo `scope` nei JSON
  non impone tecnicamente questa separazione.
- ✅ Nessun tag pseudolabel esisteva al controllo. Prima di pubblicarlo restano
  le condizioni del freeze: verbale OK integrato, commit sorgente raggiungibile
  da `origin/main`, replay al commit effettivamente taggato. Questo verbale non
  attesta anticipatamente quei fatti.

## 6. Conclusione e tracciabilità

**OK per artefatti v1 più rettifiche documentali riesaminate.** Nessuna correzione
scientifica o di codice agli artefatti v1 è necessaria. Le correzioni richieste
al report sono state lette nella versione integrativa e risolvono i rilievi;
non resta un impedimento a documentare la sottofase. La verifica della futura
integrazione/pubblicazione e l’interfaccia 03.12 restano nei loro passaggi.

Letti: MAINTENANCE e i due prompt richiesti integralmente; specifica, generatore,
test e report della sottofase integralmente; i cinque JSON operativi e freeze
tramite lettura strutturata e confronto; provenienza §9; apertura sottofasi;
walkthrough studio2 §0 e stato; piano nei punti pertinenti; validator Q8 e
funzioni originarie; decisione d’accettazione e diff del report integrativo.
Costo indicativo della lettura: circa 25–30 mila token; nessuna lettura del
corpus bibliografico o dei dati numerici, perché il compito è combinatorio e
le fonti primarie pertinenti sono codice, specifica e artefatti.

Unico file scritto dal revisore:
`studio2/fase03/pseudolabel/VERIFICA_PSEUDOLABEL.md`.
Nessun commit, merge o tag; nessuna modifica di altri artefatti.

Versioni documentali integrative riesaminate (SHA-256):

- `REPORT_PSEUDOLABEL.md`: `67e450ff7a8b8acd3083de90b88fcdd481c09b05aa23400762fcd4b6497196f1`.
- `DECISIONE_ACCETTAZIONE_V1.md`: `151e4eaa77d9e47613909b68700f654973f3133be9f1eb8411be1a5cf3c9b2e1`.
