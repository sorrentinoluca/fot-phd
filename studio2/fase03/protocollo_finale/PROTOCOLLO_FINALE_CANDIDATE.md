# Protocollo finale candidato rev4 — Studio 2, Fase 03

Data del candidato: 2026-09-18. Revisione documentale 4, recepimento dei rilievi A e C1 della
review finale sul candidato `9edf31e`; predecessore iniziale
`e0db132fc6ef477bc054d8c02b3fb62f8c39da06`. Stato: **CANDIDATO DI FREEZE, NON EFFICACE E NON
AUTORIZZATIVO**. Questo documento non autorizza chiamate, materializzazione o esecuzione. Il
freeze diventa efficace soltanto dopo review indipendente dei soli delta rev4, integrazione,
commit finale accettato e tag annotato dell'autore; 7.2-R è già chiusa con l'evidenza di §2.

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

### 1.1 Decisioni e motivazioni dell’autore

Fonte normativa integrale: [DECISIONI_AUTORE_7_3_REV2_2026-09-17.md](DECISIONI_AUTORE_7_3_REV2_2026-09-17.md),
SHA `535939de1d8c1e6f8185fd838a6bd20caca85b5f09c7908f679f251761aaccb2`, copiata byte-identica.
D1–D5 prevalgono sulle formulazioni del candidato rev1. Le motivazioni sono parte del protocollo,
non note sacrificabili. L’[addendum statistico](ADDENDUM_PIANO_STATISTICO_FINESTRE.md) verifica le
conseguenze. Q1–Q3 sono ora approvate in
[DECISIONI_AUTORE_7_3_REV2_Q1_Q3.md](DECISIONI_AUTORE_7_3_REV2_Q1_Q3.md), con motivazioni
e copia integrale delle risposte. La copia D1–D5 byte-identica non è stata modificata.
L’addendum è alla revisione 2: bootstrap descrittivo invariato e intervallo bilaterale Hoeffding
sempre affiancati (semiampiezza ≈0,34 sotto le assunzioni dichiarate); la review finale ha
stabilito **TANGO MANTENUTO** sulla verifica sintetica a ICC=0, con fallback Hoeffding già
deciso; reporting D4 esteso
descrittivamente. Indipendenza fra run dichiarata per H1/H2/H3/fallback: fattori condivisi
fissi condizionano l’estimando, stream del simulatore separati sostengono l’indipendenza,
deriva LLM mitigata da schedule/canary ma non eliminata. Stress ICC>0 solo descrittivo.
Le decisioni serali D6–D11 sono registrate nel nuovo
[DECISIONI_AUTORE_7_3_REV3.md](DECISIONI_AUTORE_7_3_REV3.md): `X=0`, quota retry 400,
backoff 30/60/120/240 s fino a 15 min, STOP a cinque fallimenti tecnici consecutivi per
servizio, barriera canary per giorno civile, massimo 7.202 e collocazione di 7.4-MAT dopo il tag.

### 1.2 D1 — un caso per run

**Assegnazione casuale bilanciata per posizione, separatamente per fault**: gli otto run di
ciascun fault e gli otto Normal, ordinati per `run_id`, ricevono ciascuno una delle otto
finestre da 5 h mediante permutazione casuale con seme congelato. Per ciascun fault OOD si
assegnano tre posizioni distinte fra otto. Nessun vincolo di colonna, quindi non «quadrato latino».
L’assegnazione usa solo identificativi, va committata **prima** dell’apertura dei segnali/evidence
di test e resta identica fra A/B-LF/E-LF/B-noLF, agenti, G_P/G_A e ripetizioni. Deve essere
confermata tecnicamente la disponibilità di otto finestre per ogni run; altrimenti STOP.
Finestre mancanti o run interrotti non si sostituiscono selettivamente. Le scorte non sono
nuove osservazioni né rimedio discrezionale dopo aver visto i segnali.

Quantità stimata: media uniforme sulle otto posizioni post-guasto, senza assumere stazionarietà.
La media sul campione finito è imparziale rispetto all’assegnazione; garanzie inferenziali su
nuovi run e relative assunzioni sono distinte nell’addendum §§1–4. Un caso per run non basta
per affermare «piano statistico invariato». La curva per posizione è secondaria descrittiva:
56 valutazioni local-unseen per condizione derivano da otto run fisici, non da 56 repliche
indipendenti; non separa variabilità fra run ed evoluzione entro run.

Motivo: otto finestre porterebbero il solo nucleo a 41.472 chiamate e, mantenendo swap,
ablation, OOD, canary e X ai valori a una finestra, la campagna a circa 377 h con margine 20%,
oltre W=168 h. Due finestre corrispondono illustrativamente a circa 105/147 h negli scenari
media/p95, calcolati come `2 × 7.202`; il p95 per chiamata non è un percentile della durata totale.
Una finestra bilanciata evita di privilegiare l’esordio e conserva margine operativo. Due
finestre aumenterebbero copertura, non necessariamente potenza: i run indipendenti restano 64.

Appoggi e limiti: Downs & Vogel tabella 8 sostiene un orizzonte 24–48 h, non le finestre di
5 h; Kaur/CODiT offre un precedente di una finestra per traiettoria, non garanzie conformal
per questo test; RBC-AD distingue finestre campionate e flusso completo, non dimostra
sufficienza di una finestra. Rinvii bibliografici e prova statistica nell’addendum §6.

Testo per i metodi, da usare solo dopo il freeze e l’esecuzione della procedura:
> Per stimare la prestazione media lungo l’orizzonte post-guasto entro il budget computazionale
> disponibile, abbiamo selezionato una finestra per run mediante assegnazione casuale bilanciata
> sulle otto posizioni temporali, separatamente per fault. L’assegnazione è stata congelata prima
> dell’ispezione dei dati di test e mantenuta identica fra condizioni e riceventi. Il disegno non
> valuta il monitoraggio continuo né il ritardo di rilevazione; le analisi per posizione temporale
> sono descrittive.

L’assegnazione è stata committata in `7e497dc`, prima di ogni lavoro sugli input test:
`PCG64(20260917)`, namespace `studio2-fase03-window-assignment-v1`, una `permutation(8)`
per gruppo in ordine lessicografico, primi tre valori per ciascun fault OOD. Sono assegnati
78 run; le 11 scorte sono escluse e mai sostitutive. La verifica successiva ha confermato
89/89 run con otto finestre e l’estrazione di 78/78 unità sulla sola finestra assegnata.
SHA tabella assegnazione `1ba7669ae9715e4c6313b6746a05f8d390eeee2877d7f41cc554146c9e35836b`;
SHA file `ASSEGNAZIONE_FINESTRE_7_4.json`
`c809e79d2c03d74f4a5a37988eca809bda336468ab0060f794d3c214f9a6a775`.

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
| Criteri di selezione | commit `ab43f0b20f45cdb475c0caf52c6f7afcbae50891` (tag catalogo-D1); `selection/CRITERIA_FREEZE_rev002.json` | `67785912feae29212001f7deb0a21b468d4d768421269e900314bef88ea41d21` file |
| Soglie Normal | tag `studio2-fase03-soglie-normal-frozen-001`; `soglie_normal/THRESHOLD_FREEZE.json` | `ff5c27002a2548003e4bc5f54805cda3754fb19b9cb2559222996b9c7f7e14a9` file |
| Evidence di sviluppo | release `studio2-fase03-evidence-v2` | `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf` archivio tar |
| Pseudolabel e E | tag `studio2-fase03-pseudolabel-frozen-001`; `pseudolabel/PSEUDOLABEL_FREEZE.json` | `21c9e52f94f508e02ae98a3957e3e55c9661334a44fedc25011c033fc4fabaec` file |
| Baseline numerica | commit `a00605862f627710347bd63c49f79a6d0a00135f`; `baseline_numerica/BASELINE_FREEZE_rev005.json` | `c52c7231021f52fc7b60b3b55eb67b5205854176395eb809db4d20227978b7cc` file |
| Harness 03.10 | `harness/ACQUISIZIONE_OK_CHIUSURA_03_10.md` | `2e057a07224d113e817c645913f22e47c4438ead426f7559e45fdede4ea6440d` file |
| Lotto 03.11 | release `studio2-fase03-test-v1`; `fault_runs/SIGILLO_LOTTO_03_11.json`; aggiornamento pubblicazione/riscaricamento 2026-09-17 | `9bd02e900429e971c08cbb8fc81f5dec54b8dcfb30b90e19faf622bb8558739d` sigillo; `1c382fda87bc99d2177461c44fdef1ae50e977abfa9b5113a57587dab3e0bc2c` aggiornamento |
| Schema insight R4 | tag `studio2-fase03-schema-insight-frozen-001`; `schema_insight/SCHEMA_FREEZE.json` | `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12` file |
| Pilot 03.13 | tag `studio2-fase03-pilot-v1`; `pilot/REPORT_PILOT_03_13.md` | `daf79ab1990ceb78712223067c024527d01eb2b67fa751eaa66f30615cf59049` file |
| Review scientifica pilot | `protocollo_finale/VERIFICA_PILOT_03_13.md` (copia byte-identica da b567, committata con rev2) | `944db3d73ecb389f450b95f7228095e279dfb181321d929cff0a03c7ceaaabb2` file |
| Esito tecnico pilot | `pilot/VERIFICA_ESITO_PILOT_03_13.md` | `1ce0a466586a65993d1269476f9de8a4812b9f64a20eae71cd9aec7e8bee4b70` file |
| Candidato librerie 7.2 | commit `c284523badefdf6b4f4e131e99ba4dfbda31300c`; `studio2/fase03/librerie/LIBRERIE_FINALI_CANDIDATE.json` | `235fb0de37080a0a2076332b8587fd5fa6457600ed2228a13d3042e18058a5a3` file |
| Decisione di riuso 7.2 | stesso commit; `studio2/fase03/librerie/RIUSO_LIBRERIE_7_2.md` | `90e939231c1b27d9ff2b58b6ce7dcde35c6dfc561576f8fe67cae4b744c7c036` file |
| Review indipendente 7.2-R | commit `f0d0393a3702bd349d93ec9e7e60a740580445fb`; `studio2/fase03/librerie/VERIFICA_LIBRERIE_7_2.md` | `fce3b955584bb8fd0fca8d98f9985f4f1ffc2da4f93a9daa99c67e414f4aaad9` file |
| Runner finale 7.4 | commit finale `74c5d3dca78fc22c3de1e675e50e7d0870f45ecc`; codice FIX-3 `7d58efd`; `REPORT_7_4_FIX.md` §FIX-3 | parte del freeze; report `482ff5d804a0ba0df502510e47f8418806cd2f27d76c7cb19b6723a97c04ec07`; suite Mac pre-FIX-3 `50601686…` e post-FIX-3 `66c34927…` entrambe incluse nella catena da integrare |
| Assegnazione finestre 7.4 | `batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json` | `c809e79d2c03d74f4a5a37988eca809bda336468ab0060f794d3c214f9a6a775` file; `1ba7669ae9715e4c6313b6746a05f8d390eeee2877d7f41cc554146c9e35836b` tabella canonica |
| Input test 7.4 | `evidence/output_test/INPUT_MANIFEST_TEST_7_4.json` | `67e7584a80d743efc06edc4c97019c20803cc4787c1d70c8d924ad23736612e8` file |
| Inventario / schedule finali | generati da `a51ffd1` con NumPy 2.2.6 | `227e5e9c797dbfd8be746d85b77298f5dfb091846dc301f0b2e31ea1dbc6df3f`; `1acfc4044c53f113016ed0bfab58863291a9060a9edc9abadb68a21d30687819`, ambito artefatto canonico |
| Mappa canonica dei prompt finali | mappa identificativo→SHA riprodotta dalla review | `b819200396da480d3ed9d4aa8f6b6aac8c135d97f0876b734a9b607b75736489` mappa canonica vincolante; `final_prompts.jsonl` è prodotto di 7.4-MAT e il suo SHA sarà registrato alla materializzazione |
| Verifica sintetica H3 | commit script/manifest `b465f90`; risultati `d0cfeab`; `verifica_sintetica_h3/` | script eseguito `847bc294948303a1d4763cc223893eeffc167c42f4e3b1540f73ed31feb53c5f`; Tango sorgente `25a648b99fcb86f8111eaaf2f712183d6c3e0a0af5960b6b84c424c38fb1e613` |
| Review finale protocollo/runner/H3 | `protocollo_finale/VERIFICA_FINALE_PROTOCOLLO_RUNNER_H3.md` | `a2fe4b6753cdbac04f0eaddd9902f735adeb0c201bc220d882532ec8f81fba6a` file; A/B OK con rilievi, C OK, **TANGO MANTENUTO** |
| FedAvg 03.14 | `fedavg/FEDAVG_FREEZE.json`; `fedavg/FINAL_PROTOCOL.json` | `6a93ef43177a3bbafa412d68cc3ab4bdf330fc5d718e3783ae1f9d2f652bf9a2`; `5eaa041852b6573314f07ee0bf39f20d1e78c5b260d476676fe911452c476f9a` file |
| Ordine di presentazione | `harness/PRESENTATION_ORDER_APPROVAL_2026-09-15.json` | `0f9f7b7f4036bd4172467dba80673af5d9ec3abb2bb854d6239da7ccec2977d1` file; `6ec43fb83af732788086138d4da60a2e9fbb4fd67e334ad513b0a240b8119f2a` solo array ordinato dichiarato |

Il renderer diagnostico congelato di base per A/B-LF/E-LF è `studio2/fase03/protocol.py`, SHA file
`791fa347e97ca49e15a8b7ca1e02e0e38c0be37e23eece092c8a094e9a653d1e`. L'ordine prompt-facing
è, per tutte le condizioni e tutti gli agenti:

`MHMU4, HEW25, FD3GZ, 3ZGWQ, GSX3L, 4AMS4, TYFPG, QRCCB, Normal`, con prefisso
`S2-CLS-` sulle otto pseudolabel. L'ordine canonico evaluator-side non cambia.

### 2.1 Coordinate di conservazione e stato reale

Il manifest JSON registra repository, tag, commit dichiarato se disponibile, asset, byte e SHA,
oltre alla fonte locale hashata. Un URL basato su tag non è immutabile da solo: l’identità
normativa è la coppia coordinate + digest atteso; un contenuto differente deve essere rifiutato.
I nomi release appartengono a `sorrentinoluca/fot-tep-data`, non ai tag Git di questo repository.

- `evidence-v2`: release ID 388257324, commit dati `6d238929285e57c6c70f4d563ef7e30b59da6ac5`,
  asset `studio2-fase03-evidence-v2.tar`, 62.185.472 byte, SHA in §2;
  `evidence/ARTIFACT_STORAGE.json` registra riscaricamento, 1.283 file e zero mismatch.
- `test-v1`: Luca ha riscaricato i tre asset il 2026-09-17; gli SHA ricalcolati coincidono
  con `fault_runs/ARTIFACT_STORAGE.json`: `ac1e7c0c…`, `242f689a…`, `16acf7c1…`.
  **C3/R2 è chiuso**. Il verbale storico `ACQUISIZIONE_OK_ESECUZIONE_03_11.md` resta immutato;
  il successivo
  [aggiornamento datato](../fault_runs/AGGIORNAMENTO_PUBBLICAZIONE_E_RIVERIFICA_03_11_2026-09-17.md),
  SHA `1c382fda…bc2c`, registra pubblicazione e riverifica per riscaricamento, tre asset su tre
  OK. Questo branch propone nel medesimo JSON il passaggio da `publication_pending_author` a
  `public_release_verified_by_redownload`, senza inventare release ID, commit o timestamp
  remoto non presenti nella verifica offline.

La review pilot SHA `944db3…abb2` è ora copiata byte-identica in questa cartella: sarà
raggiungibile da main con l’integrazione del candidato; non si dichiara già integrata.
I tag storici criteri/baseline restano invariati: la rev002 criteri e la rev005 baseline sono
riferite ai commit che contengono davvero quei file, verificati offline con `git show`.

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

### 3.1-bis D2 — B-noLF

Token esatto `B-noLF`, libreria `G_P`: il prompt deve essere B-LF meno il solo blocco
`DECISION POLICY` local-first. Istruzioni, esempi, insight, ordine, caso, schema e ogni altro
byte restano identici. Nuovo file/revisione del renderer, **mai modifica in luogo** di
`protocol.py` SHA `791fa347…53d1e`: `studio2/fase03/protocol_bnolf.py`, commit `a51ffd1`,
SHA `b716200e6fdb34fa6dc0e7264612820306026f1851b188ef772016fc633fca8c`.
La prova di diff B-LF↔B-noLF passa su 148 prompt e il logging ammette il quarto token.
Il numero di token del prompt completo deve essere misurato col tokenizer qualificato per
ogni prompt e conservato; non è deducibile come somma/sottrazione di token del blocco isolato.
Il token era già nell’inventario 7.4-PREP, quindi questa decisione non cambia da sola lo SHA
storico della schedule. S8 è soddisfatto; la review finale lo ha confermato e FIX-3 non tocca
il renderer.

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

`LIBRERIE_FINALI_CANDIDATE.json` conserva un `library_path` assoluto: sarà corretto alla prossima
revisione dichiarata di quel file. Il rilievo non blocca questo protocollo perché identità fisica
e contenuto canonico delle due librerie sono congelati dai digest sopra.

### 3.3 Allegato S18: diff B-LF ↔ E-LF

Il diff strutturale è stato rifatto con il renderer di §2, `G_P` di §3.2 e il manifest di input
congelato (SHA file `8417688869b75bda8235387ac830018ecdc9030442a860d495418f195f2b4014`).
Per ciascuno degli otto riceventi sono stati confrontati i quattordici insight peer selezionati:
**112/112** record cambiano nel solo campo `pseudolabel`; `insight_id`, `source_agent`,
`evidence_scope`, `variable_ids` e `observed_pattern` hanno **0 differenze**. Il controllo interno
di `peer_insights` rifiuta inoltre qualunque insieme di campi modificati diverso dal singleton
`{"pseudolabel"}`. Poiché per input identici il renderer costruisce entrambe le condizioni con le
stesse istruzioni, politica local-first, label space, esempi locali, caso e schema, questo verifica il renderer di base sugli input di sviluppo. Sul manifest test finale il diff B↔E
passa su **624** celle appaiate, con zero differenze fuori dal blocco `PEER INSIGHTS`; il diff
B-noLF passa su 148 prompt. Il massimo è 5.284 token e il p95 5.219. La review finale ha
confermato questi risultati. La permutazione E resta quella congelata in
`pseudolabel/CONDITION_E_DERANGEMENTS.json`, SHA in §3.1.

## 4. Blocchi congelati (efficacia condizionata alle review)

In ogni riga il ricevente è il consumer 122B; `R=3`; la generazione usa i renderer di
§§3.1–3.1-bis e l’ordine di §2. Il runner finale è `74c5d3d` (codice `7d58efd`); B1–B7 sono
recepiti per rinvio a `REPORT_7_4_FIX.md` §FIX-3. L'inventario finale contiene 2.244 prompt unici e lo
schedule 6.732 richieste scientifiche.

| Blocco | Casi e condizioni | Insight | Richieste |
| --- | --- | --- | ---: |
| Nucleo local-unseen | 8 fault × 8 run × 7 agenti non proprietari × A/B-LF/E-LF × 3 | nessuno / `G_P` / `G_P` permutata | 4.032 |
| Nucleo local-seen | 8 fault × 8 run × proprietario × A/B-LF/E-LF × 3 | come sopra | 576 |
| Nucleo Normal | 8 run × 8 agenti × A/B-LF/E-LF × 3 | come sopra | 576 |
| Producer-swap | `{F1,F8,F10,F13}`; 8 run × 7 non proprietari; B-LF × 3 | libreria completa `G_A` | 672 |
| Ablation B-noLF | local-seen: 8 fault × 8 run × proprietario; local-unseen: `{F1,F2,F14,F15}` × run 1–3 × 7 non proprietari; ×3 | `G_P`, senza politica local-first | 444 |
| OOD | `F5`, `F4` × 3 run × 8 agenti × A/B-LF/E-LF × 3 | come nucleo; astensione D10 disponibile sempre | 432 |

Il producer-swap è descrittivo e confronta B-LF con `G_A` contro B-LF con `G_P`, mantenendo
consumer, casi, schema, cardinalità e cap uguali. L'ablation B-noLF è descrittiva e non ha un
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

### 5.1 Conteggio finale e massimo

| Voce | Formula | Valore | Identità destinataria |
| --- | --- | ---: | --- |
| Nucleo | `(8×8×7×3 + 8×8×1×3 + 8×8×3) × 3` | 5.184 | 122B consumer |
| Producer-swap | `4×8×7×3` | 672 | 122B consumer |
| B-noLF | `(8×8 + 4×3×7)×3` | 444 | 122B consumer |
| OOD | `2×3×8×3×3` | 432 | 122B consumer |
| Audit aggiuntivo | già assorbito da R=3 | 0 | 122B consumer |
| E5 corrotto / FULL | esclusi, `S=0`, `U=0` | 0 | — |
| Canary | `10×d`, `d=7` massimo | 70 | 122B consumer |
| Libreria principale | `G_P=0`; riuso accettato da 7.2-R | 0 | — |
| Libreria alternativa | `G_A=0`; riuso accettato da 7.2-R | 0 | — |
| Pilot storico | già eseguito e rendicontato; 156 intent nativi + 5 di lineage | 161 storico; 0 futuro | — |
| Verifiche tecniche | `X=0`; una futura verifica richiede revisione dichiarata | 0 | — |
| Retry fuori pilot | solo zero-token provati; quota separata `Q=400` | 400 | 122B |
| **Base pianificata senza retry** | `6.732 + 70` | **6.802** | 122B; 0 27B |
| **Totale futuro massimo** | `6.732 + 70 + 400` | **7.202** | 122B; 0 27B |

Parametri recepiti: `S=0`, `U=0`, `d=7`, `X=0`, `G_P=0`, `G_A=0`, `Q=400`.
D3 limita i retry ai trasporti con zero token generati provato. La quota deriva dal pilot:
`8/156 = 5,13%`, circa 349 tentativi attesi su 6.802 slot pianificati, più 15% e
**arrotondato per difetto a 400 (401,35 al +15 %)**. È un tetto, non un obiettivo né una
previsione garantita. Il riuso delle
librerie è stato dimostrato da 7.2-R; le sedici chiamate producer prima accantonate non sono
trasferibili ad altre chiamate.

Il massimo 7.202 rispetto al totale storico 7.174 del `REPORT_PILOT_03_13.md` differisce di
**+28**: `−256` per gli accantonamenti E5 esclusi, `−16` per il riuso delle librerie,
`−100` per `X=0`, `+400` per la quota retry.

La base pianificata 6.802 supera il vecchio tetto storico 3.700 di **3.102 chiamate (+83,8%)**;
il massimo 7.202 lo supera di **3.502 (+94,6%)**. È accettato perché
la rev. 10 ha sostituito quel tetto con conteggio completo e test temporale `1,20×T<=W`, e
l'autore ha dato GO al ramo R=3 con `W=7 giorni` dopo il pilot. Non è un'autorizzazione a
riutilizzare la differenza come riserva.

### 5.2 Fattibilità temporale

Calcolo sequenziale, senza vantaggi teorici di concorrenza:

- media: `(7202×26,2086)/3600 = 52,432 h`; con margine 20%:
  **62,918 h (62,9 h) < 168 h**;
- p95: `(7202×36,6609)/3600 = 73,342 h`; con margine 20%:
  **88,011 h (88,0 h) < 168 h**.

La seconda è una proiezione basata sulla latenza p95 individuale, **non** il p95 del tempo
complessivo. Il backoff è regolato separatamente e monitorato nel tempo civile; non crea quota.
Distribuite sui sette giorni civili massimi, le proiezioni richiedono circa **9,0 h/giorno**
sulla media e **12,6 h/giorno** sulla p95; oltre il settimo giorno la quota canary ferma il
batch.
Con il massimo di 7.202 chiamate entrambe le proiezioni con margine restano sotto `W=168 h`:
**T5 PASS**, confermato dalla review finale. Nessuna chiamata 27B futura.

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

Regola giornaliera (piano §10.5, D3; decisione D8 rev3):

1. Dieci slot canary all’inizio di ogni giorno civile Europe/Rome con chiamate scientifiche,
   prima del primo lotto; massimo sette giorni civili, non automaticamente tutti i giorni
   contenuti in una finestra mobile di 168 h. Oltre sette giorni o W: STOP, nessuna quota implicita.
2. Dieci risposte valide concordi con la coppia attesa → PASS. Almeno una coppia diversa o
   una risposta generata invalida/troncata → giorno MARKED (causa distinta: discordanza o
   invalidità). L’hash grezzo è solo forense. Un errore di trasporto non dimostra deriva:
   prova zero-token → slot recuperabile entro `Q=400`; consumo incerto → STOP immediato.
   Fino alla risoluzione dei dieci slot nessun verdetto giornaliero né invio scientifico.
3. Ogni tentativo consuma contabilità: primo invio nello slot dei 70, retry nella riserva Q,
   mai nuovo slot canary né azzeramento del numero di giorni. Una risposta generata invalida
   non si ripete. Errori permanenti/identità cambiate impongono STOP immediato anche nel canary.
4. `returned_model` o `system_fingerprint` diverso → STOP durevole prima di ulteriori invii.
   Il primo giorno di campagna deve essere PASS; un primo MARKED iniziale non sblocca il batch.
   Dopo un PASS iniziale, un singolo giorno MARKED consente la prosecuzione marcata; il
   secondo giorno distinto MARKED sospende prima del lotto successivo, fino a decisione autore.
5. **Maschera primaria della sensibilità canary:** `primary_mask_request_ids`, tutte le chiamate
   scientifiche del giorno civile MARKED, anche successive al canary, come piano §10.5.
   **Maschera forense distinta:** `forensic_mask_request_ids`, chiamate fra l’ultimo set canary
   PASS completato e il canary fallito (timestamp/ordine eventi del ledger); in assenza di
   precedente PASS, dall’inizio campagna. Le due maschere e la loro unione descrittiva
   `union_descriptive_request_ids` vanno esportate separatamente senza riscrivere record
   terminali. L’unione non
   sostituisce tacitamente la sensibilità del piano e non decide H1–H3. Un’eventuale analisi
   dell’unione è descrittiva, separatamente etichettata. La primaria mantiene tutti i casi.
6. I dieci prompt sono quelli del pilot, copiati byte-identici nel nuovo target e autenticati
   contro la tabella prima della materializzazione; non si rigenerano dal nuovo manifest test.

La barriera per giorno civile, le due maschere e i casi invalidi sono implementati al commit di
codice `7d58efd`; la suite Mac finale è documentata in `74c5d3d`. B1–B7 sono recepiti per
rinvio a `REPORT_7_4_FIX.md` §FIX-3. Nessun lotto scientifico può iniziare in
un giorno civile privo di canary PASS di quello stesso giorno.
Le maschere individuano richieste/risposte; qualsiasi contrasto ricalcolato dopo esclusioni
mantiene solo coppie complete, con denominatori e motivi di esclusione espliciti; è sensibilità,
non cambia la popolazione primaria. Nessuna sostituzione opportunistica con repetitions 2/3.

## 7. Regole di esecuzione pre-registrate

### 7.1 Prerequisiti e ordine

Ordine obbligatorio:

1. La review finale di protocollo, runner e verifica sintetica è acquisita in
   `VERIFICA_FINALE_PROTOCOLLO_RUNNER_H3.md`; i rilievi B1–B7 sono chiusi da FIX-3. Prima del
   merge resta la review indipendente dei soli delta: codice `7d58efd`, sua evidenza documentale
   finale `74c5d3d` e questa revisione 4.
2. Integrare rem6 **fino a `74c5d3dca78fc22c3de1e675e50e7d0870f45ecc`**, poi il branch del
   protocollo. In `main` devono risultare raggiungibili sia
   `batch_finale/SUITE_MAC_a51ffd1.txt` (commit `7925124`) sia
   `batch_finale/SUITE_MAC_7d58efd.txt` (commit `74c5d3d`). Solo dopo creare il tag annotato
   `studio2-fase03-protocollo-finale-frozen-001` sul commit in main, su mandato dell’autore.
3. Dopo il tag, la fase **7.4-MAT** produce il target finale fresco: configurazione eseguibile,
   contratto di generazione e copia autenticata dei dieci prompt canary del pilot; quindi ledger,
   inventario, identità, quote e schedule autenticati. Questi prodotti post-tag non sono difetti
   né prerequisiti del protocollo. Canary giornaliero PASS, poi le tre passate; infine chiusura
   del ledger e analisi. Questo incarico non materializza, integra o crea tag.

Il ref `main` contiene già 03.11 (`ea90761d`): sigillo
`9bd02e900429e971c08cbb8fc81f5dec54b8dcfb30b90e19faf622bb8558739d`, audit
`420a61eb65a47961092ee042f7fa08797a25b350f875cad76c0954f7f3eeb6e3` e piano F5
`ef0b28529b6a48932d6fb7483c1fef44e331db089f284cc3d7a06a6e20879572`.

Il runner finale è **parte del freeze**: nuovi entrypoint `run_final_batch.py`,
`run_final_canary.py`, `materialize_final_target.py`, inventario e adattamenti del ledger,
non una capacità già dimostrata dal pilot. Il commit finale è `74c5d3d`; il codice è
`7d58efd`, mentre `74c5d3d` aggiunge soltanto documentazione e l’esito della suite Mac
post-FIX-3. La review finale originaria e la successiva review dei soli delta restano distinte.

L’inventario ha 2.244 prompt logici: 1.728 nucleo, 224 swap, 148 B-noLF, 144 OOD.
ID stabile: tupla `(block, condition, case_id, recipient_agent, library_role)` di stringhe,
ordinata lessicograficamente **come tupla**, non testo concatenato; nessun campo contiene `|`.
Valori block: `nucleus`, `producer_swap`, `ablation_b_no_lf`, `ood`.
`library_role`: `none` per A, `G_P` per B-LF/E-LF/B-noLF principali, `G_A` solo swap.
`case_id=run_id` del sigillo, la finestra assegnata è nel manifest autenticato.

Schedule: numpy **2.2.6** come ambiente di riferimento PREP, un solo
`numpy.random.Generator(PCG64(20260913))`, namespace `studio2-fase03-final-order-v1`.
Per passate 1→2→3, chiamare **`Generator.permutation(n)`**, n=2244, sugli indici
nell’inventario ordinato; mai re-inizializzare il generatore fra passate.
Stage: `final_batch_r1`, `final_batch_r2`, `final_batch_r3`, ciascuno 2.244 slot logici;
`final_canary` 70; `technical_verification` 0; quota trasporto `Q=400` separata e condivisa,
non moltiplicata per stage. La passata successiva richiede chiusura della precedente.

Pin finali verificati: inventario `227e5e9c797dbfd8be746d85b77298f5dfb091846dc301f0b2e31ea1dbc6df3f`,
schedule `1acfc4044c53f113016ed0bfab58863291a9060a9edc9abadb68a21d30687819`.
Il token B-noLF era già presente: non cambia da solo la schedule. Differenze future vanno
spiegate e riviste, mai coperte sovrascrivendo gli SHA storici. Registrare versione numpy effettiva.
Come documentato da `REPORT_7_4_FIX.md` §FIX-3/B7, `numpy_version` e il riferimento storico
`e0db132` sono parte dei payload hashati: i pin sono riproducibili sotto NumPy 2.2.6 e quel
riferimento non va corretto sovrascrivendo gli artefatti.
Resume: stessa schedule persistita, nessun rimescolamento/riuso slot; retry come tentativo
figlio della stessa richiesta logica. Repetition 1 è quella assegnata, non la prima a completare.

### 7.2 D3 — risposte, retry, quota e STOP

| Esito | Regola vincolante |
| --- | --- |
| Errore tecnico con prova che non è avvenuta generazione | Retry entro `Q=400` dopo riconciliazione |
| Timeout senza prova di mancata generazione | Sospendere e riconciliare, nessun reinvio automatico |
| Risposta generata invalida o troncata | Fallimento terminale, nessuna rigenerazione |
| Risposta valida errata o astenuta | Esito scientifico definitivo |

Zero token significa zero token **generati, ragionamento incluso**, con prova durevole
collegata alla richiesta; risposta vuota, usage assente e timeout non bastano. Fonte operativa:
`harness/ledger.py::reconcile_zero_token` e
`harness/CONTRATTO_ESECUZIONE_E_RIPRESA_REV2_BATCH_FINALE.md` per gli stage del profilo
`final_batch`; il contratto storico senza suffisso resta congelato per il pilot.
Stessa validazione semantica di prova e binding in acquisizione, retry e resume; nessuna
ricostruzione retroattiva di prove mancanti. Questo estende solo il batch finale, non il gate.

Motivo: evitare seconde possibilità selettive a risposte già generate e non trasformare
errori pre-generazione provati in errori diagnostici. Ogni tentativo è comunque contato;
le tre ripetizioni scientifiche non sono retry. Una risposta generata invalida resta non
corretta nel denominatore primario e in quello dei non astenuti, mai astensione (§3.3 del piano).
Una richiesta recuperabile ma senza quota resta pendente con STOP; non si omette dall’analisi.

STOP operativo dopo **5 tentativi tecnici consecutivi falliti per servizio**, retry inclusi;
contatore persistente, conservato al riavvio, reset soltanto dopo trasporto completato
con identità verificata (la validità diagnostica non è criterio di reset). Attesa crescente
registrata: 30, 60, 120, 240 secondi, poi crescita fino al tetto di 15 minuti; tetto cumulativo
`Q=400` separato. La quinta
occorrenza impedisce il sesto invio automatico. Il numero 5 è una protezione operativa,
non una soglia statistica. STOP conserva risultati e richieste pendenti, non cancella la campagna.

STOP immediato: errore permanente, identità cambiata (`returned_model` **o** fingerprint),
consumo incerto, quota superata, schedule non autenticata, prerequisiti mancanti, secondo
canary-day marcato, ledger incoerente, provenienza persa. Ripresa soltanto sullo stesso
binding/schedule e dopo risoluzione documentata; non autorizza una nuova configurazione.
La quota si valida atomicamente attraverso tutti gli stage prima del nuovo intent/trasporto;
restart/alias/directory diversi non creano quota. Implementazione finale al commit di codice
`7d58efd`, esito suite Mac acquisito in `74c5d3d`; vedi `REPORT_7_4_FIX.md` §FIX-3.

`X=0`: non esiste riserva tecnica. Qualunque futura verifica tecnica richiede una revisione
dichiarata del protocollo; non può finanziare retry, remediation, canary extra o nuove analisi.

### 7.3 D4 — uso delle tre ripetizioni

Primaria **sempre repetition 1**, anche se le altre due concordano contro di lei; mai sostituita
per invalidità, errore o astensione. Divergenza: coppia (`abstain`, `predicted_label`) o
validità diversa, come piano §10.3. Le altre ripetizioni documentano la variabilità del modello.

Aggregatore di sensibilità, su **tre esiti validi**: maggioranza 2 su 3 della coppia parsata,
altrimenti astensione per disaccordo, mai spareggio con repetition 1.

| Tre esiti validi | Aggregato |
| --- | --- |
| F1, F1, F8 | F1 |
| F1, F8, F13 | Astensione per disaccordo |
| F1, F8, astensione | Astensione per disaccordo |
| Astensione, astensione, F1 | Astensione del modello per maggioranza |

Categorie distinte: astensione del modello, astensione per disaccordo, output invalido.
Accuratezza primaria conta astensioni/invalidità non corrette; riportare anche copertura,
accuratezza sui non astenuti e invalidità, senza eliminare gli invalidi (§3.3).

**Regola Q3 approvata:** meno di tre risposte valide dopo risoluzione delle richieste
pendenti → `invalid_incomplete_triplet`, non astensione, anche con due valide concordi.
Nessuna rigenerazione o voto «errato» come etichetta. Invalidità aggregata non corretta nei
denominatori totale e non astenuti; astensioni aggregate escluse soltanto dal secondo.
Conservare numero di votanti validi e cause. La primaria non cambia per questa scelta. Con D3, triplette incomplete terminali derivano
solo da risposte generate e invalide; richieste di trasporto pendenti bloccano la chiusura.

Ambito già previsto: piano §10.4, sensibilità sui soli prompt audit deterministici del 10%
del nucleo, senza nuove chiamate a R=3. **Q3 approvata:** mantenere quella sensibilità
e aggiungere una tabella descrittiva dell’aggregazione su tutti i prompt, separata per blocco,
senza nuove ipotesi o sostituzione dei risultati confermativi. Recepito nell’addendum rev2 §§5 e 7. Riportare per blocco e condizione accuratezza, copertura,
accuratezza sui non astenuti, astensione del modello, astensione per disaccordo e invalidità
aggregata; nessuna fusione dei blocchi né test confermativo aggiuntivo.

La self-consistency di Wang et al., ICLR 2023, è un precedente del voto in ragionamento
aritmetico/commonsense, non una garanzia TEP né della prima risposta in caso di disaccordo.
La regola evita di trasformare disaccordo completo in una diagnosi senza consenso.
Producer-swap resta esplorativo, con covariata di copertura bidirezionale 6/16 vs 0/16 e
asimmetria dei template dichiarate, senza aggiustamenti confermativi. H1→H2→H3, alpha e m
non si cambiano: le condizioni di validità e il residuo H3 sono nell’addendum §§2–4.

## 8. Checklist GO/NO-GO

`PASS-C` significa soddisfatto nel candidato ma non efficace finché il candidato non è verificato
e taggato. Un requisito bloccante `PENDING` impedisce materializzazione/esecuzione.

### 8.1 Tecnici T1–T11

| ID | Stato | Evidenza puntuale | Bloccante ora? |
| --- | --- | --- | --- |
| T1 | PASS | tag `studio2-fase03-pilot-v1`; `pilot/REPORT_PILOT_03_13.md`, SHA in §2 | No; identità ricontrollata da canary |
| T2 | PASS documentale | report pilot e review byte-identica tracciata in questa cartella, §2.1 | Integrazione richiesta prima del tag |
| T3 | PASS | 119/120 valide, astensione in A/B-LF/E-LF; `pilot/VERIFICA_ESITO_PILOT_03_13.md`, SHA in §2 | No |
| T4 | PASS | 0/120 troncamenti; stesso esito | No |
| T5 | PASS-C | massimo 7.202: 62,918/88,011 h con margine 20%, entrambe <168 h, §5; review finale favorevole | Sì, fino a review dei delta, integrazione e tag |
| T6 | PASS, ramo R3 | 1/40 divergente per validità; report/review pilot | No |
| T7 | PASS | logging durevole e identità verificati nel report/review pilot | No |
| T8 | PASS-C | selezione e barriera giornaliera implementate in `7d58efd`, §6; B1–B7 in `REPORT_7_4_FIX.md` §FIX-3 | Sì, fino a review dei delta, integrazione e tag |
| T9 | PASS pilot | 16/16 insight per entrambi nel pilot; report/review pilot | No per capability; S5/S19 sono condizionati alla review |
| T10 | PASS registrazione | report pilot §3/§4: configurazioni, seed/thinking e identità esposte | No; limite da riportare |
| T11 | PASS | gate: A ha 6/24 astensioni valide sui casi `matched_transfer`; report pilot §4 | No |

### 8.2 Scientifici S1–S19

| ID | Stato | Evidenza puntuale | Bloccante ora? |
| --- | --- | --- | --- |
| S1 | PASS | tag `studio2-fase03-catalogo-D1-frozen-001`; `selection/CATALOG_FREEZE.json`, SHA in §2 | No |
| S2 | PASS | release `studio2-fase03-evidence-v2`, SHA archivio completo in §2 | No |
| S3 | PASS | sigillo verificato; tre asset test-v1 riscaricati e verificati il 2026-09-17 (§2.1) | No |
| S4 | PASS | tag `studio2-fase03-soglie-normal-frozen-001`; `soglie_normal/THRESHOLD_FREEZE.json`, SHA in §2 | No |
| S5 | PASS-C | `G_P/G_A` accettate senza nuove chiamate; §3.2 e review 7.2-R, SHA in §2 | Sì fino al freeze |
| S6 | **TANGO MANTENUTO** | 108/108 punti ICC=0 passano, massimo `phat=0,05128`; review finale §C.5 | No; restano livello e FWER approssimati e verifica locale a H3 |
| S7 | PASS | tag `studio2-fase03-pseudolabel-frozen-001`; `PSEUDOLABEL_FREEZE.json`, SHA in §2 | No |
| S8 | PASS-C | `protocol.py` intatto; renderer B-noLF e 148 diff verificati, runner finale `74c5d3d` (§3.1-bis) | Sì, fino a review dei delta, integrazione e tag |
| S9 | PASS | commit a00605862f627710347bd63c49f79a6d0a00135f, BASELINE_FREEZE_rev005.json (§2) | No |
| S10 | **TANGO MANTENUTO** | m e gerarchia invariati; validità assume indipendenza fra run; review finale §C.5 | No; l’assunzione resta dichiarata |
| S11 | **TANGO MANTENUTO** | sequenza invariata; Tango H3 supera il bordo ICC=0; verifica locale a H3, senza garanzia FWER generale | No; limiti non attenuati |
| S11b | PASS | piano statistico §3.1, tag 03.8 | No |
| S12 | PASS | piano §9/D11; sigillo 03.11 | No |
| S13 | PASS | `F6→F5`, `F4` mantenuto; verbale storico `fault_runs/ACQUISIZIONE_OK_ESECUZIONE_03_11.md`, SHA `ddd986c1…`; aggiornamento pubblicazione/riverifica 2026-09-17, SHA `1c382fda…bc2c`, tre asset su tre OK | No |
| S14 | PASS | piano statistico §12, tag 03.8 | No |
| S15 | PASS | `fedavg/FINAL_PROTOCOL.json`, SHA in §2 | No |
| S16 | PASS | `fedavg/FEDAVG_FREEZE.json`, SHA in §2 | No |
| S17 | PASS | tag `studio2-fase03-schema-insight-frozen-001`; `SCHEMA_FREEZE.json`, SHA in §2 | No |
| S18 | PASS-C | finali: B↔E 624/624 e B-noLF 148/148; max 5.284, p95 5.219 token | Sì, fino a review dei delta, integrazione e tag |
| S19 | PASS-C | 13/13 criteri su entrambe le librerie; asimmetria accettata e R1 dichiarato; §3.2 e review 7.2-R | Sì fino al freeze |

### 8.3 Organizzativi O1–O6

| ID | Stato | Evidenza puntuale | Bloccante ora? |
| --- | --- | --- | --- |
| O1 | PASS | D9 e identità effettive nel tag/report pilot | No |
| O2 | PASS-C | `Q=400`, massimo 7.202 e T5 62,9/88,0 h §5 | Sì, fino a review dei delta, integrazione e tag |
| O3 | PASS-C | ruoli qualificati nel pilot, W=7 giorni, canary §6 | Sì fino al freeze |
| O4 | PASS | freeze FedAvg 03.14 | No |
| O5 | PASS | `paper_sections/REPORT_PAPER_SECTIONS.md`, SHA `a15387ffcc237f001c0c8692f1b19edfdf2cd04fa1803a58a79920c403488b3d` | No |
| O6 | PASS-C | D1–D11 recepite; quota e verifica H3 chiuse documentalmente; **TANGO MANTENUTO** | Sì, fino a review dei delta, integrazione e tag |

**Verdetto rev4:** i rilievi A1–A6 e C1 sono recepiti; B1–B7 sono chiusi in
`REPORT_7_4_FIX.md` §FIX-3. La review finale mantiene Tango. Restano la review indipendente dei
soli delta, l’integrazione nell’ordine di §7.1, il tag annotato e poi 7.4-MAT.

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
6. La base pianificata 6.802 supera il tetto storico 3.700 di 3.102 (+83,8%); il massimo
   congelato 7.202 lo supera di 3.502 (+94,6%). Il tetto storico è sostituito da T5 temporale;
   il massimo passa a 62,9 h sulla media e 88,0 h sulla p95, margine 20% incluso.
7. La chiamata di gate fallita per trasporto resta nel conteggio del pilot; il pilot non è stato
   riavviato da zero.
8. E5 non entra nel protocollo finale perché approvata ma non congelata; i suoi 256 slot
   prudenziali non sono chiamate autorizzate. È pianificata soltanto dopo il batch principale,
   come studio aggiuntivo con freeze proprio e senza modificare le analisi qui congelate.
9. Il producer-swap descrittivo usa per decisione dell'autore i soli fault di continuità
   `F1/F8/F10/F13`; non include fault sticking né i fault difficili `F3/F15`, quindi non supporta
   generalizzazioni all'intero catalogo.

10. Una finestra per run, randomizzazione bilanciata per posizione entro fault: endpoint
    uniforme sulle otto posizioni, non monitoraggio continuo; assunzioni e limiti inferenziali
    nell’addendum, curva temporale soltanto descrittiva.
11. D3 sostituisce Q=0 assoluto con `Q=400`: retry solo con zero-token provati, contabilità separata,
    STOP dopo cinque fallimenti tecnici per servizio e STOP immediati; nessun retry di output
    generato invalido. Backoff 30/60/120/240 secondi fino a 15 minuti.
12. D4 completa la sensibilità: 2/3 o astensione per disaccordo; primaria sempre repetition 1.
    Triplette incomplete e reporting globale sono approvati con Q3; non introdotti
    dopo l’osservazione dei risultati. Canary: maschera giorno come piano, intervallo forense
    separato; nessuna sovrascrittura implicita della sensibilità §10.5.

### 9.1 Threats to validity del producer-swap

Il confronto producer-swap 122B/27B usa librerie generate con template che differiscono di una
riga (identificatori canonici, presente solo nel 122B dopo la sua remediation); oltre alla
sintassi, questa riga correla con una copertura `variable_ids↔observed_pattern` più ampia nel 122B
(6/16 contro 0/16 insight), un possibile confondente se l'ampiezza descrittiva della narrativa
influenza l'uso a valle degli insight. Inoltre i quattro fault di continuità scelti non coprono i
fault sticking o i fault difficili `F3/F15`; la misura è esplorativa e descrittiva.

### 9.2 Threats to validity della verifica H3

La verifica sintetica ha completato 1.596 scenari, con 24 stress INFEASIBLE e zero errori
numerici. Al bordo ICC=0, Tango H3 passa 108/108 punti (`phat` massimo 0,05128), ma il massimo
ICC descrittivo testato con livello ≤0,055 è 0 per Tango H3 e 0,20 per Hoeffding H3 e H1/H2.
H3 vale dunque sotto indipendenza fra run ed è sensibile anche a piccola correlazione entro fault;
H1/H2 risultano descrittivamente robusti fino a correlazione moderata. Ciò non cambia la
procedura e non garantisce il FWER completo. La review finale ha concluso **TANGO MANTENUTO**;
la verifica resta locale a H3 e il livello/FWER completo restano approssimati, non garantiti.

## 10. Risposte Q1–Q3 e chiusura del freeze

**Nessuna risposta Q1–Q3 ancora richiesta all’autore.** Recepimento normativo nel file nuovo
`DECISIONI_AUTORE_7_3_REV2_Q1_Q3.md`; non viene riscritta la copia originale.

1. **Q1 sì:** bootstrap §6 invariato, descrittivo approssimato e non garantito conservativo;
   intervallo bilaterale Hoeffding affiancato, sempre entrambi, nessuna scelta post-hoc.
   Il quantile bootstrap non decide H1/H2/H3; nel paper si dichiara la semiampiezza ≈0,34.
2. **Q2 A:** Tango è mantenuto per H3 dopo la verifica sintetica indipendente pre-dati
   definita in [SPECIFICA_VERIFICA_SINTETICA_H3.md](SPECIFICA_VERIFICA_SINTETICA_H3.md).
   N=64, griglia eterogenea fault×posizione con correlazione entro fault, bordo −0,125 e
   potenza a 0/+0,05, 100.000 repliche per punto, livello empirico ≤0,055 su tutta la griglia **ICC=0**.
   Esito negativo a ICC=0 → fallback B Hoeffding deciso ora, non dopo i dati reali.
   Stress ICC=0/0,05/0,1/0,2/0,4 su Tango, Hoeffding H3 e H1/H2 descrittivo, senza
   cambiare procedura né attivare fallback; riportato nei threats. S6/S10/S11 sono
   **TANGO MANTENUTO** per rinvio alla review finale; Tango non rende garantito il FWER
   completo. Il fallback richiede ancora
   l’indipendenza effettiva dei run: non sana automaticamente correlazioni reali.
3. **Q3 sì:** audit 10% invariato e reporting D4 su tutti i prompt, descrittivo per blocco e
   condizione; meno di tre validi → invalid_incomplete_triplet, anche con due concordi,
   non corretto e distinto dalle astensioni, con numero di risposte valide registrato.

La verifica H3 è stata eseguita con script congelato SHA
`847bc294948303a1d4763cc223893eeffc167c42f4e3b1540f73ed31feb53c5f` e implementazione Tango
SHA `25a648b99fcb86f8111eaaf2f712183d6c3e0a0af5960b6b84c424c38fb1e613`.
Lo script trascrive Tango invece di importarlo e non verifica a runtime gli SHA dichiarati;
l’identità matematica e gli SHA sono stati verificati dalla review finale. Lo script non viene
modificato perché il suo SHA è pinnato nei risultati. Esito §5: **TANGO MANTENUTO**.

Non restano segnaposto. Restano aperti soltanto:

1. review indipendente dei soli delta FIX-3/rev4;
2. integrazione nell’ordine **rem6 fino a `74c5d3d` → branch del protocollo**, con entrambi i
   log della suite Mac raggiungibili da `main`;
3. tag annotato `studio2-fase03-protocollo-finale-frozen-001` in `main`;
4. fase post-tag **7.4-MAT**, incluso `final_prompts.jsonl` con SHA registrato alla
   materializzazione.

Nessun merge o tag è eseguito da questo incarico.
