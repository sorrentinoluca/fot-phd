Verdetto: **OK**, limitato al solo delta `af50d54..3180aea` (tre file aggiunti).

Review indipendente e **read-only** del solo nuovo delta operativo-documentale
D9. L'OK è circoscritto al commit `3180aeaacbec25a5907d556e8ca2aa7060a04865`,
tree `460a1a1d20eb7a3c6587a13682c31f398261498c`, contro la base
`af50d54f1efea2c489b04f54e16cd99778f20c31`, e ai soli tre file aggiunti. Non si
estende a runtime, ledger, servizi, qualifiche, pubblicazioni, tag, né agli OK/
NON OK storici. Nessun commit sul candidato, push, merge, tag, firma, chiamata a
servizi/endpoint, SSH, inferenza, simulazione TEP o pilot. Il verbale non è
tracciato dal candidato.

## Perimetro

- Repository sorgente: `/Users/luker/fot-tep-harness-d9-correzioni`,
  branch `codex/studio2-harness-d9-correzioni`.
- Base: `af50d54f1efea2c489b04f54e16cd99778f20c31`.
- Candidato: `3180aeaacbec25a5907d556e8ca2aa7060a04865` (punta del branch).
- Tree: `460a1a1d20eb7a3c6587a13682c31f398261498c`; genitore unico `af50d54`.
- Delta (`diff --name-status af50d54..3180aea`): **3 file, tutti aggiunti (A)**,
  nessuna modifica al runtime:
  1. `studio2/fase03/config/pilot_d9_decisions_received.json`
  2. `studio2/fase03/harness/HISTORICAL_S_SOURCE_INVENTORY_2026-09-15.json`
  3. `studio2/fase03/harness/PRESENTATION_ORDER_APPROVAL_2026-09-15.json`

## Identità e indipendenza della sessione (dichiarate, non attestate da terzi)

- Modello effettivo: **claude-opus-4-8** (Claude Opus 4.8), provider **Anthropic**,
  sessione **Claude (Cowork)** `https://claude.ai/code/session_01H6p2273pdNzgi85fei134V`.
  **Non** è il modello suggerito (`GPT-5.6 Sol`, reasoning high): divergenza di
  esecuzione dichiarata, non rivendicata come prova di diversità.
- Indipendenza: finestra nuova che non ha preparato `3180aea`; analisi condotta
  leggendo gli oggetti Git dall'object database e da archivi isolati
  (`git archive`) dei due commit, senza modificare il worktree preparatore.
- **Limite di attestazione:** non è stato possibile leggere la skill
  `/Users/luker/.codex/skills/fot-tep-harness-lessons/SKILL.md` (fuori dalle
  cartelle connesse; richiesta di accesso non riscontrata in tempo). La verifica
  non ne dipende: si fonda su blob fissati, sonde offline e guardiano.

## Controlli 1–8

**1 — Integrità e provenienza.** I tre JSON sono validi. Impronte ricalcolate dai
blob: config 2.456 B / `9d3870b6…`; PRESENTATION 1.009 B / `0f9f7b7f…`; INVENTORY
3.595 B / `ae8b89f2…`. Pin incrociati verificati: il config punta a PRESENTATION
(`0f9f7b7f…`) e a INVENTORY (`ae8b89f2…`) con SHA coincidenti; PRESENTATION punta
al registro `REGISTRO_DECISIONI_AUTORIALI_D9_2026-09-15.md` nella **base**
`af50d54`, SHA `feea9dcb…` (riscontrato byte per byte, e il registro è
**invariato** nel candidato). L'hash d'ordine `ordered_labels_sha256`
`6ec43fb8…` corrisponde esattamente alla serializzazione JSON compatta
(`json.dumps(labels, separators=(",",":"))`) dell'array; le altre serializzazioni
non corrispondono. INVENTORY punta alle fonti
`provisional_stress_probe_{summary,attempts,records}` con SHA `c9adf2a8…`,
`cc3a21d8…`, `825b649e…`, tutte **byte-identiche** ai blob nel candidato e
coerenti con `records_sha256`/`attempt_journal_sha256` interni al summary. Un hash
ricalcolato ora **non** è trattato come autorizzazione storica.

**2 — Ordine di presentazione.** I nove valori `S2-CLS-MHMU4, HEW25, FD3GZ,
3ZGWQ, GSX3L, 4AMS4, TYFPG, QRCCB, Normal` coincidono con l'ordine 1a approvato
nel registro. `scope` = «prompt-facing presentation order only; identical across
agents and conditions»; `canonical_label_space_unchanged=true`. Non vengono
toccati label canoniche, assignment o derangement. `execution_authorized=false`:
l'approvazione della presentazione non autorizza esecuzioni.

**3 — Contratto degli ingressi.** Nessun loader del runtime referenzia
`pilot_d9_decisions_received.json` per nome (grep sull'intero tree candidato: il
nome compare solo nel file stesso). Il file è quindi un **prospetto documentale
sospeso**, non una configurazione auto-caricata. Le sue diciture dichiarano
onestamente il ruolo: `status=SUSPENDED_…`, `d9.status=PENDING_BLOCKING_PREREQUISITES`,
`qualification=NOT_PERFORMED`, `pilot_go=false`,
`implementation_status=AUTHOR_DECISIONS_RECEIVED_FAIL_CLOSED`,
`missing_requirements` non vuoto. Il gate del runtime che consumerebbe una tale
struttura è `harness/d9.py::validate_config`, che è normativo su: ruoli fissi,
`missing_requirements==[]` e `status=='DOCUMENTED_FOR_AUTHORIZED_STAGE'`, R4
tokenizer/snapshot pinnati, servizi 122B/27B completi, `producer_configs`,
riconciliazione storica `RECONCILED` con `request_identities`. I campi nulli del
file sono esattamente quelli richiesti da quei gate.

**4 — Rifiuto preventivo (fail-closed).** Sonda offline con **socket disabilitati
prima dell'import** dell'harness (`evidence/fail_closed_probe.py`): passando il
config consegnato a `validate_config` si ottiene
`D9: prerequisites remain incomplete` **senza alcun tentativo di rete**.
Difesa in profondità: forzando `status=DOCUMENTED_FOR_AUTHORIZED_STAGE` e
`missing_requirements=[]`, il rifiuto persiste su
`canonical R4 tokenizer must remain separate and pinned` (e a seguire su servizi/
riconciliazione nulli). Sono **gate indipendenti multipli**: la sospensione è
implementata, non un errore accidentale di schema. Servizi, configurazioni,
tokenizer e riconciliazione nulli impediscono gli ingressi esecutivi prima di
qualunque interrogazione dei servizi.

**5 — Budget e conformità alternativa.** I numeri risalgono al piano rev.10:
`BUDGET_RISORSE_REV10.md` (fonte nell'evidence del candidato) è **byte-identico**
al budget pubblicato (`8d909d8f…`). Dalla tabella: colonna con alternativo (a=1),
`r=0,t=0,b=3…9` → **139…145** = `future_base_total_with_alternate_range`;
`b=9`, riserva interamente consumata (`8r+t=15`) → **160** =
`future_planned_max_with_shared_reserve`. Aggiungendo lo storico S (4, addebitato
**una sola volta**): 139+4/145+4 → **[143,149]** e 160+4 → **164**
(`cumulative_*`). Hard stop **200** non spendibile per differenza (coerente con
«le 40 richieste fra 160 e 200 non sono spendibili»). Le tre inferenze completate
sono **sottoinsieme** delle quattro richieste (non tre addebiti ulteriori);
riserva remediation unica (`8r+t≤15`); le otto richieste 27B (`8a`) collocate nel
pilot e non finanziano altri blocchi. I componenti sono verificati alla fonte, non
solo per coerenza aritmetica interna.

**6 — Fonti storiche S.** `summary`, `attempts`, `records` byte-identici ai pin.
Le tre correlazioni COMPLETED hanno `raw_output_sha256` **ricalcolati dal raw
output** e coincidenti col record e con l'inventario (`61666e03…`, `b573b0eb…`,
`5049a49b…`); timestamp, response ID e token corrispondono al summary. La
ordinale 1 è `REJECTED_BEFORE_INFERENCE` (errore 400 grammar, `inference_completed=false`,
nessun token/response id): `zero_token_proof_for_rejected_request=NOT_ESTABLISHED`
— **non** promossa a prova e **non** autorizza retry. Nessun request_id/identity
hash inventato; `ledger_mutated=false`, `backfill_performed=false`,
`reset_performed=false`.

**7 — Lacune e percorso di riconciliazione.** L'inventario tiene
`pilot_ledger=null`, `request_identities=null`, `reviewer=null` e
`missing_for_reconciliation` elenca il necessario (path/pilot_id del ledger
autorizzato, quattro `request_id` durevoli e relativi hash d'identità, revisione
della mappatura, prova zero-token valida per ogni pretesa di retry sulla ordinale
1). Distingue «non disponibile nelle fonti esaminate» da «mai esistito» e non
progetta né implementa una migrazione. Il gate `validate_config` esige comunque
una riconciliazione `RECONCILED` con `request_identities` pari alle 4 richieste:
la lacuna è dichiarata e **bloccante**, coerente con lo stato sospeso; non è un
difetto del candidato.

**8 — Preservazione e perimetri.** Il delta aggiunge solo tre JSON: **nessun file
runtime `.py`, ledger o documento condiviso è modificato**. Nessuna qualifica
reale, disponibilità, approvazione esecutiva, GO o chiusura 03.10 è dedotta dalle
decisioni. Freeze statistico 03.8 e servizi restano filoni separati; nessuna firma
materiale richiesta. L'OK offline del runtime `16c98f3` (acquisito in `846895a2`)
e il precedente NON OK restano preservati; R-D9-01/R-D9-02 e D04 non sono riaperti
(nessun difetto nuovo).

## Guardiano

`docs/test_explanation.py` (guardiano del contratto) su base e candidato:
**NON PASS in entrambi — 35 test, 14 fallimenti storici (walkthrough v1), 1 skip**,
flussi per-test **identici**, nessuna regressione. Non classificato PASS. Il delta
è composto da soli JSON non letti dal guardiano. `git diff --check af50d54..3180aea`:
non produce errori (il delta aggiunge solo file JSON).

## Rilievi

**Bloccanti:** nessuno, entro il perimetro del delta.

**Osservazioni non bloccanti:**

1. `pilot_d9_decisions_received.json` non è collegato ad alcun loader: è un record
   documentale. È corretto e onesto (diciture di sospensione esplicite) e, se
   sottoposto al gate reale `validate_config`, fallisce comunque chiuso. Da tenere
   presente che la barriera esecutiva effettiva resta `validate_config`, non la
   semplice presenza del file.
2. La riconciliazione durevole dello storico S (ledger, `request_id`, revisione)
   è un passo futuro esplicito ancora mancante: necessario prima di qualsiasi
   contabilizzazione esecutiva, ma fuori dal perimetro di questa review.
3. Divergenza modello di sessione rispetto al suggerito (vedi sopra).

## Portata e limiti

La review **non conferisce autorizzazioni esecutive** e non certifica qualifiche,
disponibilità dei servizi, GO, pilot o chiusure. Non riapre gli audit rev.10,
R1–R4, D9 o le decisioni dell'autore. Le impronte remote e lo stato dei servizi
non sono oggetto di questo delta. Prove nuove conservate accanto a questo verbale
in `evidence/` (sonda fail-closed e log, sintesi guardiano).

## Consegna

File nuovo, non tracciato dal candidato, in sede separata dal candidato. Percorso
assoluto, dimensione e SHA-256 sono comunicati nella nota di consegna della
sessione per la successiva acquisizione byte-identica (l'hash non è incluso nel
corpo per evitare auto-riferimento). Nessun commit, push o acquisizione eseguiti.
