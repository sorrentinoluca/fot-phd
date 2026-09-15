# Specifica della sotto-fase 03.10 — candidato harness offline

Data: **2026-09-14**. Base di assemblaggio: `origin/main`
`a00605862f627710347bd63c49f79a6d0a00135f`. Stato: **candidato offline da
verificare indipendentemente**. Nessuna chiamata API, inferenza o simulazione è
stata eseguita. Il raccordo metriche già qualificato resta invariato e il suo OK
non è esteso all'harness completo.

## 1. Fonti e perimetro di recupero

Il package preesistente è stato letto dal worktree
`/Users/luker/fot-tep/.worktrees/studio2-harness`, branch
`codex/studio2-harness`, commit
`1ac06ebdc92f73d3b630ccca9bf75f413bea170b`. È una fonte di codice, non un
ramo da fondere. Sono stati recuperati e adattati i moduli `canary.py`,
`guards.py`, `inputs.py`, `insight_adapter.py`, `logging_v1.py`, `ordering.py`,
`producer.py`, `render.py` e `sampling.py`. Non sono stati recuperati i vecchi
freeze, report, manifest di stato o documenti sopra le pubblicazioni correnti.

Sono nuovi in questo delta `ledger.py`, `gate_rules.py` e
`test_harness_offline.py`. Sono adattati anche `protocol.py`, `run_pilot.py`,
`producer_probe.py`, `config/pilot_preflight.json` e i test delle guardie. I
moduli qualificati `metric_adapter.py`, `metrics.py` e
`test_metric_raccordo.py` non sono modificati.

## 2. Dipendenze effettive e pin

L'harness usa i riferimenti completi, non il solo nome dei tag:

- base di assemblaggio `a00605862f627710347bd63c49f79a6d0a00135f`;
- evidence 03.6: sorgente `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb`,
  integrazione `7c99a8318cbe24bf864790566302f72614d963ed`, release v2 e
  archivio SHA-256
  `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf`;
- schema insight R4: target
  `3c64390bc4dd58c48cc4e1e388a38989b32b3143`, manifest
  `SCHEMA_FREEZE.json` SHA-256
  `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`,
  tag annotato `studio2-fase03-schema-insight-frozen-001`, oggetto
  `4d15c4fb915ea9db9f7425225d231746778f0ba1`, peeled sul target R4;
- validatore R4 SHA-256
  `cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508`;
- handoff Normal 03.9: sorgente
  `6372cb3c457a30b39c838e066b613c61313c35db`, file
  `NORMAL_DEV_HANDOFF.json` SHA-256
  `e2409c64ad4e36e0f3b597a5e0b9745d866af72f4da717fc7a128b25753c166a`;
- piano statistico rev.10: candidato
  `6aaa5b3eebfed4ba502c25c0443caabd0051af21`, tree
  `24847ce0cc4ff7b6defea4d65f3f41cb9ccd1c1a`, piano SHA-256
  `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`,
  manifest SHA-256
  `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`;
- `DELTA_HARNESS_03_10.md` al candidato rev.10, blob Git
  `780e08ae9e176a819a745ab2054a2e6ae79a8a9a`, SHA-256
  `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`.

Ogni dipendenza scientifica è verificata per impronta prima dell'uso; mismatch,
input final/test/OOD, provenienza sintetica o requisito mancante causano un
arresto fail-closed.

## 3. Input reali e separazione producer/libreria

`PILOT_INPUT_SOURCES.pending.json` collega 320 finestre fault di sviluppo, due
esempi fault per ciascuno degli otto agenti, gli otto esempi Normal verificati
da 03.9 e sedici contratti fissi per gli insight. Gli esempi Normal sono il primo
run assegnato e la prima finestra `[25,30)` per agente, come congelato
dall'handoff; N1–N5, `cal_thr`, `far_ver` e i casi del pilot non sono
riclassificati come esempi locali.

Gli input di conformità del producer sono evidence, esempi locali e contratti
fissi. La libreria di sedici insight R4 è invece l'output futuro delle otto
richieste di conformità. Il manifest resta `INCOMPLETE`, manca soltanto
`16 real schema-valid producer insights`, e non viene promosso a manifest
scientifico eseguibile. Questo evita di assumere insight conformi e di creare
una dipendenza circolare.

Il validatore R4 controlla i byte di schema, regole, validatore e manifest e
valida separatamente ciascuna coppia prodotta. Solo 16/16 insight validi al
primo tentativo possono costruire la libreria; non sono ammesse riparazioni o
tagli nascosti.

## 4. Ordine delle label e D9

`label_space`, mapping, owner, assignment e derangement congelati in 03.7 non
cambiano. L'ordine prompt-facing è un parametro separato e non può mutare il
manifest evaluator-side. La proposta 1a, calcolata una sola volta col namespace
`studio2-fase03-presentation-v1`, resta:

1. `S2-CLS-MHMU4`
2. `S2-CLS-HEW25`
3. `S2-CLS-FD3GZ`
4. `S2-CLS-3ZGWQ`
5. `S2-CLS-GSX3L`
6. `S2-CLS-4AMS4`
7. `S2-CLS-TYFPG`
8. `S2-CLS-QRCCB`
9. `Normal`

La correlazione di Spearman sugli otto fault è
`-0.38095238095238093`, descrittiva. Non si ripete il sorteggio 03.7 e non si
cerca un namespace più favorevole. Il renderer rifiuta l'uso finché
`author_decision` non vale `accepted` e verifica che l'ordine sia una
permutazione esatta con `Normal` ultimo.

D9 resta `UNDECIDED`: il codice non assegna ruoli ai modelli e non eredita il
vecchio Qwen-27B come scelta corrente. Identità, revisione, ruolo, endpoint,
tokenizer, chat template, limiti e fingerprint devono essere congelati dopo una
decisione esplicita e qualificati sul servizio reale.

## 5. Sequenza e contabilità rev.10

L'ordine obbligatorio è: **conformità producer → eventuale remediation → sonda
budget → unico gate 40×3**. L'alternativa producer è un blocco di conformità
separato e non finanzia retry.

Il ledger SQLite richiede un percorso assoluto condiviso, usa WAL e
`synchronous=FULL`, isola ogni `pilot_id` e registra in transazione l'intento
prima di invocare il trasporto. Conserva richieste e risultati attraverso stadi,
processi, riavvii e directory; richieste logiche duplicate, intenti irrisolti e
sequenze fuori ordine bloccano lo stadio successivo.

La riserva unica applica `8 × remediation + transport <= 15`, con
`remediation ∈ {0,1}`. Finché si preserva la remediation, il trasporto
cumulativo è al massimo 7. Dopo l'ottava richiesta di trasporto nella
conformità serve un waiver esplicito che rinuncia alla remediation. Una sola
remediation completa di otto richieste è autorizzabile dopo un esito di
conformità `FAIL`, con hash di diff, approvazione e template; nessuna seconda
remediation è possibile.

Non esistono retry automatici. Un timeout è ripetibile soltanto con prova
persistita di zero token e nei casi documentati. Nella sonda budget si ripete
solo l'intera tripletta A/B-LF/E-LF, mai una parte, e le sette richieste residue
consentono al massimo due triplette. Il gate non è ripetibile neppure con prova
di zero token.

I conteggi base sono 131–137 senza producer alternativo e 139–145 con
alternativo. Con remediation completa diventano 139–145 e 147–153; con le
sette richieste di trasporto residue i massimi pianificati sono 152 e 160. Il
limite cumulativo 200 è un hard stop distinto, non un budget pianificato.

## 6. Gate e risultati non validi

Il gate richiede esattamente 120 record, tre per ognuno dei 40 prompt. La
divergenza usa solo la validità e la coppia parsata
`(abstain, predicted_label)`. JSON equivalente o differente, finish reason,
testo libero e hash raw restano forensi ma non cambiano la divergenza.

- T3: almeno 114/120 valide al primo tentativo e almeno un'astensione valida in
  ciascuna condizione;
- T4: zero troncamenti per lunghezza su 120;
- T6: una tripletta con validità mista diverge; una tripletta tutta invalida è
  non valutabile e impedisce il GO tecnico;
- una o più triplette divergenti richiedono R=3, subordinato alla fattibilità;
- T5 non è misurabile offline: latenza, stabilità e margine temporale del 20%
  richiedono il servizio e la configurazione effettivi.

L'evaluatore offline non emette mai un GO finale. I tre endpoint e i conteggi
grezzi usano il raccordo metriche qualificato già in `main`; l'harness non
ridefinisce tale semantica.

## 7. Capienza, log e guardie

Capienza e tokenizer non sono qualificati offline. Solo dopo D9 il server deve
fornire revisione reale del modello, tokenizer, chat template, context limit,
configurazione, vLLM/provider e fingerprint. Il conteggio usa quei byte reali e
il prompt finale; stime per caratteri o la vecchia fixture non congelano nulla.

Ogni tentativo conserva identificativi, modello richiesto e restituito,
fingerprint/versione, configurazione, hash e byte di prompt/risposta, tempi,
token, finish reason, troncamento, validità ed errore. Il JSONL è append-only con
`flush` e `fsync`; il ledger è la fonte contabile cumulativa, non la directory
dei risultati.

## 8. Stato

Sono verificabili offline: import controllato, pin e incompatibilità R4,
inventario input, separazione producer/libreria, rendering parametrico,
contabilità persistente, ordine degli stadi, riserva/remediation/retry, regole
T3/T4/T6 e regressione del raccordo metriche.

Restano aperti: approvazione ordine label, D9, sedici insight reali, tokenizer e
capienza, qualificazione producer e consumer, fingerprint, sonda budget,
stabilità, latenza e fattibilità temporale. Non c'è freeze dell'harness, non c'è
GO del pilot; 03.10 e Fase 03 restano aperte.
