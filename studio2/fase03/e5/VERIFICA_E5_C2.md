# Verifica di fattibilità E5-C2 — controllo di lunghezza (gate G0)

Verdetto in prima riga: **E5-C2 chiusa il 2026-09-19 al 5 %, massimo osservato 1,42 % su
254.400 composizioni.** La prova ha contato prompt completi composti, per 300 coppie di
sviluppo e tutti gli 848 portanti B-LF reali; nessuna chiamata al modello e nessun esito del
lotto test sono stati letti.

Data: 2026-09-19. Nessuna chiamata al modello. Solo dati di sviluppo. Ambito: **lunghezze**,
nient'altro — nessuna etichetta predetta, nessuna accuratezza, nessuna anteprima
dell'endpoint (§8.12: solo misure di lunghezza possono motivare una revisione del 5 %).

## 1. Che cosa è stato misurato

| | |
| --- | --- |
| Popolazione | i **40 run di sviluppo** di `fault_runs/MANIFEST_FAULT_DEV.csv` (8 fault × 5 run), pipeline congelata 03.6: orizzonte `[25, 65)`, finestre da 5 h, baseline Normal legacy |
| Unità | **una finestra per run**, campionata a ogni replica — la geometria che D1 impone al lotto test |
| Repliche | 150 (sottoinsiemi S_F proposti) + 25 (tutte e otto le classi); semi base `20260919`, `20260969`, `20261019` |
| Coppie | 9.000 (S_F) + 4.000 (tutte le classi) |
| Corruzione | scambio della colonna della famiglia fra donatore e ricevente, **a monte** del verbalizzatore congelato; derangement disgiunto per classe, campionato **uniformemente** per rifiuto |
| Conteggio | tokenizer locale dello snapshot 122B `a099dee7…`, backend `tokenizers`, nessuna rete |
| Artefatti | `VERIFICA_E5_C2_SF.json`, `VERIFICA_E5_C2_ALL.json`, coppie grezze in `raw_e5_c2_*.jsonl.gz`, indice unità in `DEV_UNITS_INDEX.json` |

**Riproducibilità.** Il seme del derangement di ogni famiglia è derivato con SHA-256 da
(namespace, seme base, famiglia) ed è registrato in ogni riga grezza come `family_seed`: una
riesecuzione con gli stessi semi base dà le stesse coppie, su qualunque macchina. *(Una prima
versione di questo script derivava il seme da `hash()`, che Python sala per processo: le sue
misure non erano riproducibili esattamente. Corretto, e la misura rifatta da zero.)*

## 2. Risultato: la differenza è piccola e quantizzata

| Famiglia | coppie | token testo FULL (p50) | \|Δ\| p50 | \|Δ\| p95 | \|Δ\| max |
| --- | ---: | ---: | ---: | ---: | ---: |
| level | 3.000 | 208 | 1 | 48 | **48** |
| trend | 1.500 | 296 | 1 | 48 | **48** |
| residual | 2.250 | 297 | 1 | 68 | **68** |
| diff | 2.250 | 202 | 24 | 61 | **61** |

I valori di Δ non sono continui: 0, 1, ~24, ~31, ~47-48, ~60-68. Il testo neutrale è una
sequenza fissa di frasi templatizzate, quindi la lunghezza si sposta solo quando **una frase
compare o scompare**: la frase lunga di una famiglia sostituita dal suo ripiego («Nessuna
XMEAS supera la soglia di …», ≈ 47 token), o la frase derivata di `rapid` che compare o cade
(≈ 24 token). Per questo `diff` ha mediana 24 e non 1: permutare `diff` cambia quasi sempre lo
stato di `rapid`.

Con i sottoinsiemi S_F proposti la mediana è 1 token per tre famiglie su quattro. Conta la
coda, perché la regola è a scatto singolo.

## 3. Perché la misura sul testo non basta — e come si chiude davvero

Fra FULL e PERM cambia solo il blocco del caso: il renderer congelato inserisce il testo
neutrale nella sezione `CASE TO DIAGNOSE` e tutte le altre sezioni sono identiche byte a byte.
Da qui la tentazione di scrivere `|Δ| sul prompt = |Δ| sul testo` e di tradurre il criterio in
una soglia sulla «parte costante» ottenuta come `token(prompt) − token(blocco del caso)`.
**Non si può.** Con un tokenizer BPE i conteggi non sono additivi ai confini fra prefisso,
blocco del caso e suffisso: una sottrazione del genere è un'approssimazione, e una soglia
derivata da essa non è una prova.

Le voci `indicative_prefix_for_5pct_NOT_A_PROOF` nei riepiloghi JSON conservano quel calcolo
come **ordine di grandezza** (≈ 800–1.200 token, secondo la famiglia), etichettato per quello
che è.

**La verifica vera** compone i prompt dei due bracci e li conta interi:

    Δ = token(prompt con testo PERM) − token(prompt con testo FULL)
    rapporto = |Δ| / token(prompt con testo FULL)

`verifica_e5_c2_prompt.py` fa esattamente questo, prendendo come **portante** un prompt B-LF
già reso e sostituendone il blocco del caso (con verifica di round-trip: reinserendo il testo
originale il portante deve tornare identico byte a byte). Due passaggi:

```bash
# 1. prima del freeze: portanti reali, testi di sviluppo, TUTTI i portanti.
#    Esaustivo: e' questo che puo' chiudere il 5 %. Le repliche sono poche perche' il
#    costo e' repliche x coppie x portanti; le coppie sono una simulazione, i portanti no.
python3 studio2/fase03/e5/verifica_e5_c2_prompt.py \
  --dev-units ~/e5_work/dev_units \
  --prompts /Users/luker/fot-tep-runtime/prepared-7-4/final_prompts.jsonl \
  --carrier-mode all --seeds 5 \
  --out studio2/fase03/e5/VERIFICA_E5_C2_PROMPT.json

# 2. a G3: stessa strada, con i testi FULL/PERM realmente prodotti sul lotto test
python3 studio2/fase03/e5/verifica_e5_c2_prompt.py \
  --case-texts studio2/fase03/e5/CASE_TEXTS_E5.jsonl \
  --prompts /Users/luker/fot-tep-runtime/prepared-7-4/final_prompts.jsonl \
  --carrier-mode all \
  --out studio2/fase03/e5/VERIFICA_E5_C2_G3.json
```

**Quale portante, e come si chiama il risultato.** Il denominatore è il prompt composto,
quindi il caso peggiore è il portante che con *quel* testo compone il prompt più corto — e per
la stessa non-additività non lo si trova contando prefisso e suffisso a parte.

| modo | che cosa fa | come va chiamato il risultato |
| --- | --- | --- |
| `all` | ogni portante su ogni coppia | **prova**: il 5 % è verificato su ogni coppia e ogni portante |
| `candidates` | rosa dei portanti più corti **dopo composizione** su testi sonda, valutata su ogni coppia, con il peggiore per coppia | **controllo di fattibilità**: scorciatoia informata, non esaustiva |
| `sample` | portanti a caso per coppia | solo smoke |

Entrambi i passaggi che devono chiudere il 5 % — quello pre-freeze e G3 — usano `all`.
`candidates` serve a girare in fretta su molte repliche mentre si mette a punto qualcosa, e un
suo esito va riportato come fattibilità, mai come prova. Il riepilogo espone
`carrier_ranking.rank_stability`: se è falso, i testi sonda non concordano su quale sia il
portante più corto, il che è la ragione per cui `candidates` tiene una rosa e non un portante
solo — e un motivo in più per non fidarsene come prova. Su una fixture con dodici portanti di
taglie diverse i due modi danno lo stesso rapporto massimo, il che è un indizio, non una
garanzia.

**Costo di `all`.** È repliche × coppie × portanti × 2 composizioni. Con 848 prompt B-LF, 5
repliche danno ≈ 300 coppie e ≈ 500 mila conteggi: pesante ma fattibile in una sessione.
Cinquanta repliche con `all` non sono praticabili — e non servono: le repliche campionano la
finestra e il derangement, che sulla lunghezza contano meno del portante, e sono comunque una
simulazione, mentre l'insieme dei portanti è quello vero.

A G3 il file `--case-texts` è un JSONL con i testi FULL e PERM effettivamente prodotti per i
casi del lotto (formato in `pairs_from_case_texts`): nessun testo viene ricalcolato dai dati
di sviluppo, e il riepilogo lo registra come `measurement: G3`.

Nessuno dei due passaggi contatta un servizio o apre il ledger.

## 4. Quanto vale davvero il residuo di confine

L'approssimazione additiva è stata **misurata**, non assunta. Componendo i prompt con portanti
sintetici di tre taglie (1.241, 3.653 e 9.053 token) e confrontando il Δ del prompt composto
con il Δ del solo testo, su **3.600 osservazioni**:

    residuo = Δ_prompt − Δ_testo  ∈  {0}      (minimo 0, massimo 0, nessuna osservazione ≠ 0)

Era prevedibile: i byte di giunzione sono fissati dal renderer congelato (`CASE TO DIAGNOSE` +
due a capo … due a capo + `OUTPUT SCHEMA`) e non dipendono dal contenuto del prefisso. Ma
prevedibile non è misurato, e ora è misurato — su quei portanti. Artefatto:
`VERIFICA_E5_C2_PROMPT_SINTETICO.json`.

Questo **non** trasforma la stima in verifica: i portanti sono sintetici, quindi i rapporti di
quelle prove non dicono nulla sul prompt reale. Dice solo che, sui prompt reali, la parte
critica sarà il denominatore vero, non l'effetto di confine.

Per orientamento, con quei portanti sintetici il rapporto massimo su tutte le coppie era
4,6 % con il portante da 1.241 token, 1,7 % con quello da 3.653, 0,7 % con quello da 9.053.
Il prompt B-LF reale ha `max_prompt_tokens` 5.284, quindi il 5 % ha buone probabilità di
reggere — probabilità, non verifica.

## 5. Troncamento: nessuna differenza, strutturalmente

Contesto qualificato del target 131.072 token, 2.560 riservati all'output, prompt più lungo
del batch 5.284, Δ massimo 68. Margine di oltre 123.000 token: **zero differenze di
troncamento** è una conseguenza aritmetica. (Il piano rev2 §6 riportava 16.384: errore, la
fonte autorevole è il RUNBOOK 7.4.)

## 6. Controllo diagnostico «`rapid` congelata»

Rimettendo la frase di `rapid` al valore vero dentro il testo permutato (controllo
**diagnostico**, non un braccio, §8.12), rapporto sul solo testo:

| Famiglia | p50 | max |
| --- | ---: | ---: |
| residual | 0,3 % | 19,6 % |
| diff | 11,7 % | 21,6 % |

Per `diff` la quota maggiore dello scostamento viene dal **ricalcolo di `rapid`**, non dalla
colonna scambiata; per `residual` no. È da riportare accanto al contrasto, non un motivo per
cambiare qualcosa: `rapid` va ricalcolata (E5-B) e resta ricalcolata.

## 7. Stato dopo la chiusura

E5-C2 è chiusa prima del freeze con la misura registrata in prima riga. La misura qui è sui
**dati di sviluppo**, come il piano prescrive. Sul lotto test si rifà
dopo il freeze (G3, §3 passo 2): una violazione produce un'avvertenza, non una
rigenerazione.
