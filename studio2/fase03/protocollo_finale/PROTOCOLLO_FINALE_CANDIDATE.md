# Protocollo finale candidato — Studio 2, Fase 03

Data del candidato: 2026-09-17. Stato: **CANDIDATO DI FREEZE, NON EFFICACE E NON
AUTORIZZATIVO**. Questo documento non autorizza chiamate, materializzazione o esecuzione. Il
freeze diventa efficace soltanto dopo verifica indipendente di questo candidato, commit finale
accettato e tag annotato dell'autore; 7.2-R è già chiusa con l'evidenza di §2.

Tag proposto, **non creato**: `studio2-fase03-protocollo-finale-frozen-001`.

## 1. Perimetro e decisioni vincolanti

Il disegno usa Q8: otto agenti, otto fault in catalogo (`F1`, `F2`, `F3`, `F8`, `F10`,
`F13`, `F14`, `F15`), otto run primari per fault e otto run Normal. I fault OOD effettivi,
dopo la catena tecnica 03.11, sono `F5` e `F4`; `F6` è stato sostituito da `F5` e `F12` non è
stato eseguito. Le undici scorte del lotto 03.11 sono soltanto sostitutive e non aggiungono
osservazioni.

Le decisioni seguenti sono già prese e qui soltanto recepite:

- `R = 3` su tutto lo studio, perché `S2-P03-002` ha mostrato una divergenza di validità;
- finestra `W = 7 giorni = 168 h` e criterio T5 `1,20 × T <= W`;
- producer principale e consumer: `qwen3.5-122b`, fingerprint
  `vllm-0.27.1-934a3247`; producer alternativo: `fot-exp2-consumer`, fingerprint
  `vllm-0.28.0-5fc21ed4` (configurazione rev. 2);
- entrambi i producer: `enable_thinking=false`, `max_tokens=2560`; consumer nel regime
  qualificato: seed `20260829`, thinking-token budget `2048`, `max_tokens=2560`;
- il confronto 122B/27B è un confronto fra **pipeline configurate**, non un confronto isolato
  della sola taglia del modello;
- le chiamate sono eseguite soltanto da Luca dalla shell nativa; nessuna finestra LLM invia
  richieste;
- cap, schema, regole, casi, template e quote non cambiano dopo l'osservazione.

## 2. Riferimenti congelati e ambito degli hash

Gli SHA-256 sotto indicati sono SHA dei **byte del file**, salvo gli ambiti esplicitamente diversi.
Il manifest JSON affiancato conserva l'elenco meccanico completo.

| Oggetto | Riferimento | SHA-256 / ambito |
| --- | --- | --- |
| Piano consolidato | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | `d3cac5ba80c12ade2dfba2a1f8816b61a8466b5f5415d638209f692c1b5f902b` file |
| Piano statistico 03.8 | tag `studio2-fase03-piano-statistico-frozen-001`; `studio2/fase03/piano_statistico/PIANO_STATISTICO.md` | `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` file |
| Budget rev. 10 | `studio2/fase03/piano_statistico/BUDGET_RISORSE_REV10.md` | `8d909d8f851b8b9c633687989d3a9f3221230b48e1f0595278e075556d283887` file |
| Perimetro Q8 | `studio2/fase03/perimetro_q8/REPORT_PERIMETRO_Q8.md` | `d3ebdce17977cb8c14751161e324b5ceceac67e498ae27c5d1a36a8a41ab3b52` file |
| Catalogo D1 | tag `studio2-fase03-catalogo-D1-frozen-001`; `selection/CATALOG_FREEZE.json` | `68b8461a6382c93e1a5dd8dc6c9def66b26b2ec865f0bc0786dd88fa95acedda` file |
| Criteri di selezione | tag `studio2-fase03-criteri-selezione-frozen-001`; `selection/CRITERIA_FREEZE_rev002.json` | `67785912feae29212001f7deb0a21b468d4d768421269e900314bef88ea41d21` file |
| Soglie Normal | tag `studio2-fase03-soglie-normal-frozen-001`; `soglie_normal/THRESHOLD_FREEZE.json` | `ff5c27002a2548003e4bc5f54805cda3754fb19b9cb2559222996b9c7f7e14a9` file |
| Evidence di sviluppo | release `studio2-fase03-evidence-v2` | `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf` archivio tar |
| Pseudolabel e E | tag `studio2-fase03-pseudolabel-frozen-001`; `pseudolabel/PSEUDOLABEL_FREEZE.json` | `21c9e52f94f508e02ae98a3957e3e55c9661334a44fedc25011c033fc4fabaec` file |
| Baseline numerica | tag `studio2-fase03-baseline-numerica-frozen-001`; `baseline_numerica/BASELINE_FREEZE_rev005.json` | `c52c7231021f52fc7b60b3b55eb67b5205854176395eb809db4d20227978b7cc` file |
| Harness 03.10 | `harness/ACQUISIZIONE_OK_CHIUSURA_03_10.md` | `2e057a07224d113e817c645913f22e47c4438ead426f7559e45fdede4ea6440d` file |
| Lotto 03.11 | release `studio2-fase03-test-v1`; `fault_runs/SIGILLO_LOTTO_03_11.json` | `9bd02e900429e971c08cbb8fc81f5dec54b8dcfb30b90e19faf622bb8558739d` file |
| Schema insight R4 | tag `studio2-fase03-schema-insight-frozen-001`; `schema_insight/SCHEMA_FREEZE.json` | `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12` file |
| Pilot 03.13 | tag `studio2-fase03-pilot-v1`; `pilot/REPORT_PILOT_03_13.md` | `daf79ab1990ceb78712223067c024527d01eb2b67fa751eaa66f30615cf59049` file |
| Review scientifica pilot | `/Users/luker/.codex/worktrees/b567/fot-tep/studio2/fase03/pilot/VERIFICA_PILOT_03_13.md` | `944db3d73ecb389f450b95f7228095e279dfb181321d929cff0a03c7ceaaabb2` file |
| Esito tecnico pilot | `pilot/VERIFICA_ESITO_PILOT_03_13.md` | `1ce0a466586a65993d1269476f9de8a4812b9f64a20eae71cd9aec7e8bee4b70` file |
| Candidato librerie 7.2 | commit `c284523badefdf6b4f4e131e99ba4dfbda31300c`; `studio2/fase03/librerie/LIBRERIE_FINALI_CANDIDATE.json` | `235fb0de37080a0a2076332b8587fd5fa6457600ed2228a13d3042e18058a5a3` file |
| Decisione di riuso 7.2 | stesso commit; `studio2/fase03/librerie/RIUSO_LIBRERIE_7_2.md` | `90e939231c1b27d9ff2b58b6ce7dcde35c6dfc561576f8fe67cae4b744c7c036` file |
| Review indipendente 7.2-R | commit `f0d0393a3702bd349d93ec9e7e60a740580445fb`; `studio2/fase03/librerie/VERIFICA_LIBRERIE_7_2.md` | `fce3b955584bb8fd0fca8d98f9985f4f1ffc2da4f93a9daa99c67e414f4aaad9` file |
| FedAvg 03.14 | `fedavg/FEDAVG_FREEZE.json`; `fedavg/FINAL_PROTOCOL.json` | `6a93ef43177a3bbafa412d68cc3ab4bdf330fc5d718e3783ae1f9d2f652bf9a2`; `5eaa041852b6573314f07ee0bf39f20d1e78c5b260d476676fe911452c476f9a` file |
| Ordine di presentazione | `harness/PRESENTATION_ORDER_APPROVAL_2026-09-15.json` | `0f9f7b7f4036bd4172467dba80673af5d9ec3abb2bb854d6239da7ccec2977d1` file; `6ec43fb83af732788086138d4da60a2e9fbb4fd67e334ad513b0a240b8119f2a` solo array ordinato dichiarato |

Il renderer diagnostico vincolante è `studio2/fase03/protocol.py`, SHA file
`791fa347e97ca49e15a8b7ca1e02e0e38c0be37e23eece092c8a094e9a653d1e`. L'ordine prompt-facing
è, per tutte le condizioni e tutti gli agenti:

`MHMU4, HEW25, FD3GZ, 3ZGWQ, GSX3L, 4AMS4, TYFPG, QRCCB, Normal`, con prefisso
`S2-CLS-` sulle otto pseudolabel. L'ordine canonico evaluator-side non cambia.

## 3. Template e librerie

### 3.1 Consumer

Il prompt consumer è prodotto dal renderer vincolante sopra. A usa istruzione base, esempi locali,
label space, caso neutrale e schema d'uscita. B-LF ed E-LF aggiungono la stessa politica
local-first e quattordici peer insight. La politica local-first storica è anche conservata in
`phase_b/c06/prompts/B_LOCAL_FIRST_V1.txt`, SHA file
`4e6cc81f87033f0b3bcddebff694e7f446e31c228c5ac1f7560b9552aada6192`; l'oggetto eseguibile
del presente studio resta però il testo incorporato nel renderer 03.13, non una sostituzione a
runtime.

E-LF deriva da B-LF modificando soltanto `pseudolabel`, secondo
`pseudolabel/CONDITION_E_DERANGEMENTS.json`, SHA file
`34350c7e49b11d29b885da128d4b34ce3df31cd41df7c521cb66421aa1b9d001`.

### 3.2 Producer e chiusura 7.2-R

7.2-R ha accettato il riuso, senza nuove chiamate producer, delle due librerie del pilot:

| Ruolo | Path fisico | SHA file | SHA canonico |
| --- | --- | --- | --- |
| `G_P`, 122B principale | `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03/results/validated_insight_library_qwen_122b_primary_producer_remediation.json` | `1e97ddd3525c414f6d5ddd240e98d358720937e912edb4e27644374e8b2eea09` | `c2469737bcaab0df8d07a1c2493d2f95784aae07a55998aecf49cc53fa5d1a30` |
| `G_A`, 27B alternativo | `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03/results/validated_insight_library_qwen_27b_alternate_alternate_conformity.json` | `c697e803be178235c37d37caf7ec1ef65a0761db44e097f2d422e7498eef73c9` | `f860063befb6a409f4ecf824e4dd7b57002cc8e67809184dadd03d0b934a05f3` |

L'accettazione è attestata dalle tre fonti 7.2 in §2. La review ha rifatto i tredici criteri su
entrambe le librerie: 122B `OK`, 27B `OK con rilievo R1 non bloccante`. Non esiste un template
producer unico per questo batch e non vi sono chiamate producer nel batch finale. Il 122B è stato
generato col template di remediation, SHA
`4306c5da6f0ebefcbce75d26d585caf82cc05ff85d5e7e6639e3f65b2d66de12`; il 27B col template
base, SHA `e7e80d59b2def37bea8f20186fc297583e2c8b0dea390a3351c7843d841619e7`.

Al producer 122B, dopo il fallimento di validità sulla forma degli identificatori riscontrato in
due agenti su otto nel regime senza remediation, è stata aggiunta un'unica riga al template che
impone la forma canonica `XMEAS(N)`/`XMV(N)` e la citazione di ogni variabile dichiarata nella
narrativa; il 27B ha usato il template base, invariato. La differenza è dichiarata e non
ricalcolata a posteriori. Il validatore impone solo che le variabili citate siano un sottoinsieme
di quelle dichiarate, non il viceversa: la riga aggiunta correla con una copertura bidirezionale
più alta ma incompleta nel 122B (6/16 insight) contro nessuna nel 27B (0/16), un effetto che va
oltre la sola sintassi degli identificatori.

### 3.3 Allegato S18: diff B-LF ↔ E-LF

Il diff strutturale è stato rifatto con il renderer di §2, `G_P` di §3.2 e il manifest di input
congelato (SHA file `8417688869b75bda8235387ac830018ecdc9030442a860d495418f195f2b4014`).
Per ciascuno degli otto riceventi sono stati confrontati i quattordici insight peer selezionati:
**112/112** record cambiano nel solo campo `pseudolabel`; `insight_id`, `source_agent`,
`evidence_scope`, `variable_ids` e `observed_pattern` hanno **0 differenze**. Il controllo interno
di `peer_insights` rifiuta inoltre qualunque insieme di campi modificati diverso dal singleton
`{"pseudolabel"}`. Poiché per input identici il renderer costruisce entrambe le condizioni con le
stesse istruzioni, politica local-first, label space, esempi locali, caso e schema, questo chiude
S18 prima della materializzazione dei prompt finali. La permutazione E resta quella congelata in
`pseudolabel/CONDITION_E_DERANGEMENTS.json`, SHA in §3.1.

## 4. Blocchi eseguibili

In ogni riga il ricevente è il consumer 122B; `R=3`; la generazione del prompt usa il renderer di
§3.1 e l'ordine di presentazione di §2.

| Blocco | Casi e condizioni | Insight | Richieste |
| --- | --- | --- | ---: |
| Nucleo local-unseen | 8 fault × 8 run × 7 agenti non proprietari × A/B-LF/E-LF × 3 | nessuno / `G_P` / `G_P` permutata | 4.032 |
| Nucleo local-seen | 8 fault × 8 run × proprietario × A/B-LF/E-LF × 3 | come sopra | 576 |
| Nucleo Normal | 8 run × 8 agenti × A/B-LF/E-LF × 3 | come sopra | 576 |
| Producer-swap | `{F1,F8,F10,F13}`; 8 run × 7 non proprietari; B-LF × 3 | libreria completa `G_A` | 672 |
| Ablation B-senza-LF | local-seen: 8 fault × 8 run × proprietario; local-unseen: `{F1,F2,F14,F15}` × run 1–3 × 7 non proprietari; ×3 | `G_P`, senza politica local-first | 444 |
| OOD | `F5`, `F4` × 3 run × 8 agenti × A/B-LF/E-LF × 3 | come nucleo; astensione D10 disponibile sempre | 432 |

Il producer-swap è descrittivo e confronta B-LF con `G_A` contro B-LF con `G_P`, mantenendo
consumer, casi, schema, cardinalità e cap uguali. L'ablation B-senza-LF è descrittiva e non ha un
braccio E simmetrico. L'OOD è una sonda di esistenza su sei eventi, non una caratterizzazione
open-set generale.

L'autore ha fissato il producer-swap sui quattro fault di continuità `F1/F8/F10/F13`. La misura
resta descrittiva: il gruppo non contiene i fault sticking né i fault difficili `F3/F15`, limite
da dichiarare e non generalizzare agli otto fault in catalogo.

### 4.1 Esclusione di E5

L'ablazione testuale dei descrittori di §8.12 è dichiarata **approvata ma non congelata** nel
piano generale. Mancano il freeze della mappa famiglia–meccanismo, dei derangement per famiglia e
del controllo FULL. Pertanto E5 corrotto e FULL sono **fuori dal protocollo finale eseguibile**:
`S=0`, `U=0`. Gli accantonamenti `16S=192` e `8U=64` restano scenari storici di budget e non
autorizzano chiamate. E5 sarà eventualmente eseguita **dopo** il batch principale come studio
aggiuntivo con freeze proprio, sugli stessi run di test; `FULL` potrà riusare B-LF solo se la
coincidenza viene verificata. Non modifica nucleo, H1–H3, producer-swap, ablation local-first o
OOD.

## 5. Conteggio indipendente e T5

### 5.1 Conteggio futuro massimo congelato

| Voce | Formula | Valore | Identità destinataria |
| --- | --- | ---: | --- |
| Nucleo | `(8×8×7×3 + 8×8×1×3 + 8×8×3) × 3` | 5.184 | 122B consumer |
| Producer-swap | `4×8×7×3` | 672 | 122B consumer |
| B-senza-LF | `(8×8 + 4×3×7)×3` | 444 | 122B consumer |
| OOD | `2×3×8×3×3` | 432 | 122B consumer |
| Audit aggiuntivo | già assorbito da R=3 | 0 | 122B consumer |
| E5 corrotto / FULL | esclusi, `S=0`, `U=0` | 0 | — |
| Canary | `10×d`, `d=7` massimo | 70 | 122B consumer |
| Libreria principale | `G_P=0`; riuso accettato da 7.2-R | 0 | — |
| Libreria alternativa | `G_A=0`; riuso accettato da 7.2-R | 0 | — |
| Pilot storico | già eseguito e rendicontato; 156 intent nativi + 5 di lineage | 161 storico; 0 futuro | — |
| Verifiche tecniche | `X=100`, massimo prudenziale, non obiettivo di spesa | 100 | 122B |
| Retry fuori pilot | `Q=0`; nessun retry autorizzato nel batch | 0 | — |
| **Totale futuro massimo** | somma | **6.902** | **6.902 122B + 0 27B** |

Parametri congelati: `S=0`, `U=0`, `d=7`, `X=100`, `Q=0`, `G_P=0`, `G_A=0`. Il riuso è stato
dimostrato da 7.2-R; le sedici chiamate producer prima accantonate non sono trasferibili ad altre
chiamate.

Il totale 7.174 del `REPORT_PILOT_03_13.md` differisce di **−272**: `−256` perché il report
conservava gli accantonamenti prudenziali E5 `192+64`, qui esclusi, e `−16` perché 7.2-R ha
accettato il riuso di entrambe le librerie (`G_P=G_A=0`). Tutte le altre voci coincidono.

Il vecchio tetto storico di 3.700 è superato di **3.202 chiamate (+86,5%)**. È accettato perché
la rev. 10 ha sostituito quel tetto con conteggio completo e test temporale `1,20×T<=W`, e
l'autore ha dato GO al ramo R=3 con `W=7 giorni` dopo il pilot. Non è un'autorizzazione a
riutilizzare la differenza come riserva.

### 5.2 Fattibilità temporale

Calcolo sequenziale, senza vantaggi teorici di concorrenza:

- media: `(6902×26,209)/3600 = 50,248 h`; con margine 20%:
  **60,298 h < 168 h**;
- p95: `(6902×36,661)/3600 = 70,287 h`; con margine 20%:
  **84,345 h < 168 h**.

Non essendoci chiamate future 27B, la sua latenza non entra nel ricalcolo. T5 è **PASS nel massimo
conservativo** sia alla media sia al p95. Restano circa 107,7 h di margine alla media e 83,7 h al
p95 dopo il 20%; il margine temporale non crea quota di chiamate.

## 6. Canary T8

Il selettore congelato è `studio2/fase03/harness/sampling.py`, SHA file
`3ad3291f7084a2fa7865351734c6226a9efe0c9b176f241fe1bdbfe8500c6a8f`, namespace
`studio2-fase03-canary-v1`, bilanciamento A/B-LF/E-LF = 2/4/4 e copertura degli otto agenti.
Gli output attesi vengono dalle tre ripetizioni concordi del pilot; la tabella conserva coppia
parsata e hash della risposta grezza. L'hash grezzo è solo forense.

| Prompt | Condizione | Agente | SHA prompt | `abstain` | `predicted_label` | SHA risposta grezza attesa |
| --- | --- | --- | --- | --- | --- | --- |
| `S2-P03-006` | A | 2 | `83f1ba531ce0a92307aca8feefd4d591c2ef7d3634e94f546295e623f1643535` | true | null | `71a76533df65a4063f967a458878ea132e4336a492f4485c28434f556172144f` |
| `S2-P03-031` | A | 7 | `45fab8a3c81d929f78f9f20d4c551f9ebbed93a13e24cd4cf780286a51e3ee76` | false | `S2-CLS-4AMS4` | `6cd51196f38c6732f7df6401d1512672fc065d6db3334ed95cf9c786c8b154fb` |
| `S2-P03-037` | B-LF | 8 | `bad9d28b146367bbaeceea5ea9188e9c8821ecd32705150d4016b0a15f85122d` | false | `S2-CLS-HEW25` | `a49844d80f86440547819142538e007bcde00d3b266c36aeb4971c48035f3bcb` |
| `S2-P03-012` | B-LF | 3 | `9391f1b8c379262cde40d4764aa442e0b1bf04d9a2343b820f9e8d1d9914c2a1` | false | `S2-CLS-4AMS4` | `04876f98c504d0c353abd0f20f18428fac4371cd45e455916e2a58be8df2af75` |
| `S2-P03-022` | B-LF | 5 | `ce3248d5e95fdffb95b9cce7876bef8ccb67a538cfb6446fd13393c07770df6e` | true | null | `2f724a4a261da1502c78e246444c5bbe4661c39caf52e67c56e4ed80dbbce6ca` |
| `S2-P03-027` | B-LF | 6 | `89043dec743b84b3a5c2a72f8d9b27e6fa9bca84bc3f08ff9f0be63fc42393c0` | true | null | `12eac67cf626e692889fdd0be1415e1c92db69bc6e2c8f637c619ad4b5ef84d8` |
| `S2-P03-018` | E-LF | 4 | `e9e8a2586dc08f70b5644dae430d560fdb9672ef7ce7f368b2eb0fa16463cf0b` | false | `S2-CLS-FD3GZ` | `ba705ebfb3fb3896e33577c980c64037ff90191164939bca557445a8194c6cfa` |
| `S2-P03-003` | E-LF | 1 | `ddc6ed67ad84499ca462eface5cf8380b8cfaf0fe36dd74d11170111c1f77966` | false | `Normal` | `2517b9e5b1a51e97b7dabf4e6402fd2ab258b9382577389c9ff1e1fcf304fddd` |
| `S2-P03-015` | E-LF | 3 | `db07d10d4ed4ef69a4e9dd5b2b37c6e8c8d7d74df38cce580fdb0145d401ffbc` | false | `S2-CLS-QRCCB` | `2f586f2d771b286b6b1fc7e3f7ce36cf1609fd10e462da7955a641fdfdb1e0de` |
| `S2-P03-025` | E-LF | 5 | `114064dddd45c28a91455de329bd6df9943e46fc578f3eb9e800a190076606e5` | false | `S2-CLS-4AMS4` | `bc4575f0a4ebed9674862694624315ede64c8d748848fe814fcd7314f433e020` |

Regola giornaliera:

1. eseguire i dieci canary all'inizio di ogni giorno civile Europe/Rome in cui si inviano
   chiamate scientifiche, prima del primo lotto del giorno; al massimo sette giorni, quindi 70;
2. coppia parsata diversa dall'attesa in almeno un canary = giorno marcato; una variazione del
   solo hash grezzo è registrata ma non marca il giorno;
3. cambio di `returned_model` **o** `system_fingerprint` rispetto all'identità congelata = STOP
   immediato prima di altre chiamate;
4. il secondo giorno marcato = STOP prima del lotto successivo e decisione dell'autore prima di
   qualunque ripresa; un solo giorno marcato non cambia il protocollo;
5. le chiamate scientifiche eseguite dopo l'ultimo canary PASS e prima del canary fallito sono
   marcate. Restano nell'analisi primaria e sono escluse dall'analisi di sensibilità già
   pre-specificata. Lo STOP non invalida retroattivamente i dati; identità, intervalli e decisione
   dell'autore sono riportati.

## 7. Regole di esecuzione pre-registrate

### 7.1 Prerequisiti e ordine

Ordine obbligatorio:

1. review indipendente di questo candidato aggiornato e tag annotato dell'autore; una modifica a
   contenuto congelato è una nuova revisione, mai in place;
2. target finale fresco e ledger durevole con inventario, identità, quota e schedule autenticati;
3. canary iniziale PASS;
4. esecuzione delle tre passate scientifiche e dei canary giornalieri;
5. chiusura del ledger, verifica dei conteggi e solo dopo analisi.

L'inventario logico delle quattro misure contiene 2.244 prompt unici: 1.728 nucleo, 224 swap,
148 ablation e 144 OOD. L'ID stabile è la tupla canonica
`(block, condition, case_id, recipient_agent, library_role)`.

Le chiamate scientifiche si eseguono in tre passate, una per `repetition=1,2,3`. Un solo
`numpy.random.Generator(PCG64(20260913))`, namespace documentale
`studio2-fase03-final-order-v1`, viene inizializzato una volta; per ciascuna passata, nell'ordine
1→2→3, produce la permutazione dell'inventario prima ordinato lessicograficamente per ID stabile.
Si conserva SHA della schedule completa prima della prima chiamata. Il resume usa la stessa
schedule e salta soltanto gli intent già terminali: non ricalcola, non rimescola e non riusa slot.

Questa intercalazione impedisce che condizioni o blocchi siano eseguiti in un unico periodo. La
prima ripetizione è comunque definita dalla schedule, non dall'ordine di completamento.

### 7.2 Risposte, retry, quota e STOP

- Ogni invio conta nella contabilità, anche se fallisce. Le tre ripetizioni pianificate non sono
  retry.
- `Q=0`: nessun retry automatico o manuale è autorizzato nel batch congelato. Una risposta
  ricevuta non valida o troncata è terminale, resta nel proprio slot e non viene sostituita.
- Una risposta non valida conta come non corretta nel denominatore dell'accuratezza primaria, non
  come astensione; entra come non corretta anche nel denominatore dell'accuratezza sui soli non
  astenuti. Il suo tasso è il quarto numero descrittivo (`PIANO_STATISTICO.md` §3.3).
- Per una richiesta incerta/zero-token si usa soltanto la prova durevole e la riconciliazione
  `reconcile_zero_token` già definita dall'handoff §6.2. Con `Q=0` non segue un nuovo invio: si
  registra invalidità e si prosegue soltanto se il ledger è coerente; se la prova non chiude
  l'incertezza, STOP.
- Una sospensione d'identità provoca STOP. L'unico percorso ammesso è revisione approvata della
  configurazione e riconciliazione già implementata; la ripresa richiede decisione dell'autore e,
  se autorizza nuove chiamate o cambia identità, una revisione del protocollo/quota.
- Qualunque superamento della quota per stage o del totale 6.902, schedule non autenticata,
  candidato non verificato/taggato, canary identity STOP, secondo giorno marcato, ledger
  incoerente o perdita di provenienza = STOP del batch.
- `--resume` è ammesso solo sullo stesso target, schedule e binding verificati. La validazione dei
  prerequisiti deve precedere intent, bind e trasporto; storia incerta non viene riscritta o
  retrofittata.

`X=100` è un ceiling prudenziale per verifiche tecniche pianificate e identificate prima
dell'esecuzione; non finanzia retry, remediation, canary aggiuntivi o nuove analisi. Ogni chiamata
X effettiva è attribuita al modello e rendicontata separatamente.

### 7.3 Uso delle tre ripetizioni

Il rinvio normativo è `PIANO_STATISTICO.md` §§3.1–3.3, 10.3–10.5:

- l'unità di divergenza è il prompt; differenza nella coppia (`abstain`, `predicted_label`) o
  nella validità rende il prompt divergente;
- l'analisi primaria usa **repetition 1**; repetitions 2 e 3 non entrano nella stima primaria;
- il sottoinsieme audit deterministico del 10% resta quello 03.10; a R=3 non genera chiamate
  aggiuntive. Solo per quei prompt l'analisi di sensibilità sostituisce la prima ripetizione con la
  maggioranza delle tre, come §10.4; non si estende post-hoc la regola;
- le ripetizioni 2 e 3 di tutti i prompt alimentano il tasso descrittivo di divergenza/validità e
  la documentazione della variabilità del modello;
- il producer-swap resta esplorativo; si riporta come covariata descrittiva, senza aggiustamento
  degli endpoint confermativi, la copertura bidirezionale `variable_ids↔observed_pattern` già
  osservata nelle librerie (`G_P`: 6/16; `G_A`: 0/16);
- gli endpoint sono: accuratezza su tutti i tentativi (primario, astensione e invalidità non
  corrette), tasso di astensione, accuratezza sui non astenuti (descrittiva), più tasso di
  invalidità descrittivo. H1→H2→H3 resta la sequenza fissa a alpha 0,05.

## 8. Checklist GO/NO-GO

`PASS-C` significa soddisfatto nel candidato ma non efficace finché il candidato non è verificato
e taggato. Un requisito bloccante `PENDING` impedisce materializzazione/esecuzione.

### 8.1 Tecnici T1–T11

| ID | Stato | Evidenza puntuale | Bloccante ora? |
| --- | --- | --- | --- |
| T1 | PASS | tag `studio2-fase03-pilot-v1`; `pilot/REPORT_PILOT_03_13.md`, SHA in §2 | No; identità ricontrollata da canary |
| T2 | PASS | stesso tag/report; review SHA `944db3...abb2` | No |
| T3 | PASS | 119/120 valide, astensione in A/B-LF/E-LF; `pilot/VERIFICA_ESITO_PILOT_03_13.md`, SHA in §2 | No |
| T4 | PASS | 0/120 troncamenti; stesso esito | No |
| T5 | PASS-C | §5: 60,298 h media e 84,345 h p95, entrambe <168 h | Sì fino al freeze |
| T6 | PASS, ramo R3 | 1/40 divergente per validità; report/review pilot | No |
| T7 | PASS | logging durevole e identità verificati nel report/review pilot | No |
| T8 | PASS-C | set e regole in §6; `harness/sampling.py`, SHA in §6 | Sì fino al freeze |
| T9 | PASS pilot | 16/16 insight per entrambi nel pilot; report/review pilot | No per capability; S5/S19 restano aperti |
| T10 | PASS registrazione | report pilot §3/§4: configurazioni, seed/thinking e identità esposte | No; limite da riportare |
| T11 | PASS | gate: A ha 6/24 astensioni valide sui casi `matched_transfer`; report pilot §4 | No |

### 8.2 Scientifici S1–S19

| ID | Stato | Evidenza puntuale | Bloccante ora? |
| --- | --- | --- | --- |
| S1 | PASS | tag `studio2-fase03-catalogo-D1-frozen-001`; `selection/CATALOG_FREEZE.json`, SHA in §2 | No |
| S2 | PASS | release `studio2-fase03-evidence-v2`, SHA archivio completo in §2 | No |
| S3 | PASS | release `studio2-fase03-test-v1`; `fault_runs/SIGILLO_LOTTO_03_11.json`, SHA in §2 | No |
| S4 | PASS | tag `studio2-fase03-soglie-normal-frozen-001`; `soglie_normal/THRESHOLD_FREEZE.json`, SHA in §2 | No |
| S5 | PASS-C | `G_P/G_A` accettate senza nuove chiamate; §3.2 e review 7.2-R, SHA in §2 | Sì fino al freeze |
| S6 | PASS | tag `studio2-fase03-piano-statistico-frozen-001`; `PIANO_STATISTICO.md`, SHA in §2 | No |
| S7 | PASS | tag `studio2-fase03-pseudolabel-frozen-001`; `PSEUDOLABEL_FREEZE.json`, SHA in §2 | No |
| S8 | PASS-C | `protocol.py`, template e casi `F1/F8/F10/F13` sono completi in §§2–4 | Sì fino al freeze |
| S9 | PASS | tag `studio2-fase03-baseline-numerica-frozen-001`; `BASELINE_FREEZE_rev005.json`, SHA in §2 | No |
| S10 | PASS | piano statistico §§4–5, tag 03.8 | No |
| S11 | PASS | piano statistico §4.2, tag 03.8 | No |
| S11b | PASS | piano statistico §3.1, tag 03.8 | No |
| S12 | PASS | piano §9/D11; sigillo 03.11 | No |
| S13 | PASS | `F6→F5`, `F4` mantenuto; `fault_runs/ACQUISIZIONE_OK_ESECUZIONE_03_11.md`, SHA `ddd986c1fb54359d0dd059c58994136d6b71d0fccad8298665b6019848f81208` | No |
| S14 | PASS | piano statistico §12, tag 03.8 | No |
| S15 | PASS | `fedavg/FINAL_PROTOCOL.json`, SHA in §2 | No |
| S16 | PASS | `fedavg/FEDAVG_FREEZE.json`, SHA in §2 | No |
| S17 | PASS | tag `studio2-fase03-schema-insight-frozen-001`; `SCHEMA_FREEZE.json`, SHA in §2 | No |
| S18 | PASS-C | diff `G_P` B↔E: 112/112 record cambiano solo `pseudolabel`; §3.3 | Sì fino al freeze |
| S19 | PASS-C | 13/13 criteri su entrambe le librerie; asimmetria accettata e R1 dichiarato; §3.2 e review 7.2-R | Sì fino al freeze |

### 8.3 Organizzativi O1–O6

| ID | Stato | Evidenza puntuale | Bloccante ora? |
| --- | --- | --- | --- |
| O1 | PASS | D9 e identità effettive nel tag/report pilot | No |
| O2 | PASS-C | conteggio e T5 in §5 | Sì fino al freeze |
| O3 | PASS-C | ruoli qualificati nel pilot, W=7 giorni, canary §6 | Sì fino al freeze |
| O4 | PASS | freeze FedAvg 03.14 | No |
| O5 | PASS | `paper_sections/REPORT_PAPER_SECTIONS.md`, SHA `a15387ffcc237f001c0c8692f1b19edfdf2cd04fa1803a58a79920c403488b3d` | No |
| O6 | PASS | piano statistico congelato e decisioni recepite | No |

**Verdetto del candidato:** `READY FOR INDEPENDENT REVIEW`, ma ancora `NO-GO` alla
materializzazione finché questo candidato aggiornato non riceve review indipendente e tag
annotato dell'autore.

## 9. Deviazioni da dichiarare nel paper

1. Il gate del pilot ha osservato una divergenza di validità, quindi il piano è passato da R=1 a
   **R=3** per tutto lo studio.
2. Le identità operative sono 122B come producer principale/consumer e 27B come producer
   alternativo, in sostituzione dei modelli ipotizzati nelle versioni storiche del piano.
3. Entrambi i producer usano `enable_thinking=false` e `max_tokens=2560`; il consumer mantiene
   thinking nel regime qualificato. Il confronto producer è fra pipeline configurate.
4. La finestra organizzativa effettiva è `W=7 giorni`, con accettazione
   `1,20×T<=168 h`.
5. Dopo il fallimento di validità sulla forma degli identificatori in due agenti su otto, il
   producer 122B ha ricevuto una riga di remediation che impone forma canonica e citazione di ogni
   variabile dichiarata; il 27B ha mantenuto il template base. L'asimmetria non è stata ricalcolata
   a posteriori ed è un possibile confondente: copertura bidirezionale 6/16 contro 0/16.
6. Il massimo futuro 6.902 supera il tetto storico 3.700 di 3.202 chiamate (+86,5%); il tetto era
   stato sostituito prima del GO dalla regola di fattibilità temporale, che passa anche al p95.
7. La chiamata di gate fallita per trasporto resta nel conteggio del pilot; il pilot non è stato
   riavviato da zero.
8. E5 non entra nel protocollo finale perché approvata ma non congelata; i suoi 256 slot
   prudenziali non sono chiamate autorizzate. È pianificata soltanto dopo il batch principale,
   come studio aggiuntivo con freeze proprio e senza modificare le analisi qui congelate.
9. Il producer-swap descrittivo usa per decisione dell'autore i soli fault di continuità
   `F1/F8/F10/F13`; non include fault sticking né i fault difficili `F3/F15`, quindi non supporta
   generalizzazioni all'intero catalogo.

### 9.1 Threats to validity del producer-swap

Il confronto producer-swap 122B/27B usa librerie generate con template che differiscono di una
riga (identificatori canonici, presente solo nel 122B dopo la sua remediation); oltre alla
sintassi, questa riga correla con una copertura `variable_ids↔observed_pattern` più ampia nel 122B
(6/16 contro 0/16 insight), un possibile confondente se l'ampiezza descrittiva della narrativa
influenza l'uso a valle degli insight. Inoltre i quattro fault di continuità scelti non coprono i
fault sticking o i fault difficili `F3/F15`; la misura è esplorativa e descrittiva.

## 10. Domande aperte e chiusura del freeze

**Domande aperte per l'autore: nessuna.**

Azioni non discrezionali ancora necessarie: ottenere la review indipendente di questo candidato e
creare, solo su mandato dell'autore, il tag proposto. Fino ad allora il documento resta un
candidato e non autorizza materializzazione o chiamate.
