# Specifica della sotto-fase 03.7 — pseudolabel opache, assegnazione degli agenti e derangement di E

Data: **2026-09-13**. Piano §6.5, D10, §8.1, §8.2, §8.4. Base: `d815ce9` (attuazione 03.4) sul
branch `codex/studio2-pseudolabel`. Catalogo D1: `studio2/fase03/selection/CATALOG_FREEZE.json`,
tag `studio2-fase03-catalogo-D1-frozen-001` (commit `ab43f0b20f45cdb475c0caf52c6f7afcbae50891`),
SHA-256 `68b8461a6382c93e1a5dd8dc6c9def66b26b2ec865f0bc0786dd88fa95acedda`.

Questa specifica è scritta **prima** di eseguire il generatore. Ogni scelta con un grado di
libertà è fissata qui; il codice la implementa e il log (`DRAW_LOG.json`) la registra. Nessuna
chiamata a modelli linguistici, nessuna simulazione, nessun dato del primo studio viene letto:
il solo pattern riusato è la funzione `derive_opaque_pseudolabel` di `phase_b/config/protocol.py`
(letta, non importata; riscritta qui per MAINTENANCE §8.2).

## 1. Costanti congelate

| Costante | Valore | Nota |
| --- | --- | --- |
| `NAMESPACE` | `studio2-fase03-pseudolabel-v1` | cambia solo con una nuova versione (v2, mai in luogo) |
| `SEED` | `20260913` | intero fissato qui, stessa convenzione (data ISO) del sorteggio D1; entra soltanto nei derangement |
| Prefisso | `S2-CLS-` | come `protocol.PSEUDOLABEL` (`^S2-CLS-[A-Z0-9]{5}$`) |
| Lunghezza suffisso | 5 caratteri | alfabeto base32 RFC 4648 (`A–Z`, `2–7`) ⊂ `[A-Z0-9]` |
| Identificatore del fault | campo `label` del catalogo (`F1`, `F2`, `F3`, `F8`, `F10`, `F13`, `F14`, `F15`) | letto da `CATALOG_FREEZE.json`, non trascritto a mano |
| Normal | letterale `Normal` | come nel primo studio (D10); ultima posizione di `label_space` |
| Unknown | **non esiste come label** | è l'astensione `abstain=true`, `predicted_label=null` (D10) |
| Agenti | `agent_1` … `agent_8` | `protocol.AGENT_IDS` |
| Peer per agente | 7 | gli otto fault meno quello locale (§8.1) |

## 2. Guardia sul catalogo

Prima di derivare qualsiasi cosa il generatore legge `CATALOG_FREEZE.json`, ne calcola la SHA-256
e la confronta con `68b8461a…`; confronta inoltre la lista `catalog` con `[1, 2, 3, 8, 10, 13, 14, 15]`
e le otto `label` con `F1, F2, F3, F8, F10, F13, F14, F15`. Se una delle tre condizioni fallisce il
generatore si ferma senza scrivere nulla. Il tag e il commit del catalogo sono registrati nel log e
nel freeze come `catalog_tag` / `catalog_commit`.

## 3. Derivazione delle nove label

Per ciascun fault, nell'ordine di elaborazione del catalogo (`idv` crescente — è solo l'ordine in
cui il ciclo gira, non entra nel messaggio e non lascia traccia nella label):

1. `counter = 0`;
2. `message = f"{NAMESPACE}|label|{identifier}|{counter}"`, codificato UTF-8;
3. `digest = SHA-256(message)`; `suffix = base32(digest)[:5]` (senza padding);
4. la candidata è `S2-CLS-` + `suffix`. Viene **rifiutata**, e `counter` incrementato di 1 tornando
   al punto 2, se:
   - **collisione**: `suffix` coincide con quello di una label già accettata;
   - **guardia di opacità**: `suffix` contiene come sottostringa le cifre decimali dell'`idv` del
     proprio fault (es. `2` per F2, `14` per F14);
5. la prima candidata non rifiutata è la label del fault. Ogni tentativo (messaggio, digest,
   suffisso, esito, motivo del rifiuto) va nel log; il contatore finale per fault è
   `label_counters` nel log.

`Normal` non passa dalla derivazione: è letterale.

**Ordine di `label_space`.** Le otto label opache sono ordinate **lessicograficamente (ASCII)**
sulla stringa della label, poi `Normal` in nona e ultima posizione, coerente con
`protocol._validate_label_space`. L'ordinamento sulla stringa opaca non porta informazione sul
catalogo: la label di F1 non è «prima» se non per caso del digest.

## 4. Assegnazione fault ↔ agente

Biiezione deterministica dal digest, non scelta a mano:

1. per ciascun fault `key = SHA-256(f"{NAMESPACE}|assignment|{identifier}")` in esadecimale;
2. gli otto fault sono ordinati per `key` crescente (stringa esadecimale, confronto ASCII);
3. il fault in posizione *k* (1-based) è il **fault locale** di `agent_k`.

Il risultato è una biiezione per costruzione (otto chiavi distinte: una coincidenza di SHA-256 tra
otto messaggi diversi è esclusa in pratica; il codice la verifica comunque e si ferma). Ogni agente
possiede quindi esattamente una pseudolabel di fault, come richiede `validate_pilot_input_manifest`
(«the eight agents must own the eight fault pseudolabels one-to-one»).

## 5. Derangement per la condizione E

Per ciascun agente, i **7 peer** sono le pseudolabel di fault diverse da quella locale, ordinate
secondo la loro posizione in `label_space` (ordine lessicografico, §3). Il derangement è una
permutazione dei 7 peer **senza punti fissi**, campionata **uniformemente** fra tutti i derangement
di 7 elementi (sono !7 = 1854; il codice li enumera e verifica il conteggio), **non** la rotazione
di un passo usata dalla fixture sintetica e dal primo studio.

Campionamento, per `agent_id` in ordine `agent_1 … agent_8`:

1. si enumerano i 1854 derangement di `(0, 1, …, 6)` in ordine lessicografico della tupla;
2. `i = 0`; `word = primi 4 byte big-endian di SHA-256(f"{NAMESPACE}|{SEED}|derangement|{agent_id}|{i}")`,
   intero in `[0, 2^32)`;
3. se `word ≥ 2^32 − (2^32 mod 1854)` la parola è **rifiutata** (rejection sampling, che rende
   la scelta esattamente uniforme), `i += 1`, si torna al punto 2; altrimenti
   `index = word mod 1854`;
4. la permutazione `perm = derangements[index]` definisce la mappa `peers[j] → peers[perm[j]]`.

Ogni parola estratta (accettata o rifiutata) e l'indice scelto vanno nel log. Il seed entra solo
qui: le label e l'assegnazione dipendono dal solo namespace.

**Controlli** eseguiti dal generatore e dai test: chiavi esattamente `AGENT_IDS`; per ogni agente
dominio = codominio = i suoi 7 peer; nessun punto fisso; la label locale non compare né come
chiave né come valore; ogni mappa è una biiezione. Formato identico a quello atteso da
`protocol._validate_derangements` e usato da `protocol.peer_insights` (dizionario
`pseudolabel → pseudolabel` per agente).

## 6. Artefatti prodotti (tutti evaluator-side, mai nei prompt)

| File | Contenuto |
| --- | --- |
| `PSEUDOLABEL_MAP.json` | `identifier → label` per gli otto fault più `Normal`, `label_space` (9), `idv` per fault |
| `AGENT_ASSIGNMENT.json` | `agent_k → {identifier, idv, local_fault_label}`; forma `agents` compatibile con il manifest del pilot |
| `CONDITION_E_DERANGEMENTS.json` | `derangements` per agente (pseudolabel → pseudolabel) più una vista leggibile `identifier → identifier` |
| `DRAW_LOG.json` | namespace, seed, ordine di elaborazione, tutti i tentativi, contatori, parole rifiutate, impronta del catalogo |

Serializzazione: JSON UTF-8, `indent=2`, `ensure_ascii=False`, chiavi nell'ordine di inserimento,
newline finale. Il comando `--check` rigenera tutto in memoria e confronta **byte per byte** con
i file su disco (replay byte-identico).

## 7. Criteri di collisione e contatori dichiarati

- `label_counters[identifier]`: numero di rifiuti (collisione o opacità) prima dell'accettazione;
- `derangement_rejections[agent_id]`: parole rifiutate dal rejection sampling;
- entrambi partono da 0 e sono registrati in `DRAW_LOG.json`. Il loro valore non è scelto: è
  l'esito deterministico delle regole sopra.

## 8. Che cosa questa sotto-fase NON fissa

- lo **schema degli insight** (campi, cardinalità, cap): è 03.12 (D12, §8.9);
- il **contenuto** degli insight e dei prompt;
- gli **esempi locali** per agente, i casi di sviluppo e i casi di trasferimento (03.6, 03.10);
- l'uso delle label nei prompt del pilot: il mapping resta evaluator-side.

Interfaccia con 03.12: se 03.12 cambia il **formato** della pseudolabel (regex di `protocol.py`),
questa generazione si rifà **con un nuovo namespace `studio2-fase03-pseudolabel-v2`**, in una
nuova cartella o con nuovi nomi di file, senza sovrascrivere né i file v1 né questa specifica.

## 9. Congelamento

`PSEUDOLABEL_FREEZE.json` registra le SHA-256 dei tre artefatti, del log, del codice e dei test,
il commit sorgente e `catalog_tag`, con stato `frozen_pending_independent_verification`. Nessun
tag viene creato in questa finestra; il tag proposto è `studio2-fase03-pseudolabel-frozen-001`,
alle condizioni di MAINTENANCE §8.4: verifica indipendente OK (`VERIFICA_PSEUDOLABEL.md`),
commit raggiungibile da `origin/main`, replay `--check` superato sul commit taggato.
