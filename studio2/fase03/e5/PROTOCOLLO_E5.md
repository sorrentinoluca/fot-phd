# Protocollo E5 — ablazione testuale dei descrittori (candidato, NON congelato)

Stato: **CANDIDATO**. Diventa congelabile (`exp5-protocol-frozen-001`) quando le decisioni
A–G di `DECISIONI_AUTORE_E5.md` sono prese. **E5-C2 chiusa il 2026-09-19 al 5 %, massimo
osservato 1,42 % su 254.400 composizioni.** Disegno autorevole: piano §8.12; dove questo
documento aggiunge, lo dice.

## 1. Perimetro

Si altera **solo il caso interrogato**. Esempi locali, libreria di insight, contesto e
politica local-first restano fissi e identici in tutti i bracci. La manipolazione avviene
**a monte del verbalizzatore congelato**, sulla tabella di evidenza `EVT-xxxx.features.csv`
che l'estrattore del lotto test scrive per ogni caso; il testo non si tocca mai.

Nessun artefatto esistente viene modificato: `protocol.py`, `protocol_bnolf.py`,
`code/tep_verbalize_v2.py`, le soglie, `protocollo_finale/`, l'inventario, lo schedule, il
ledger del batch e il lotto test restano intatti. Tutto ciò che E5 aggiunge vive in
`studio2/fase03/e5/`.

## 2. Bracci

| Braccio | Definizione | Statuto |
| --- | --- | --- |
| FULL | B-LF r1-r3 riusato dopo le sei identità (`VERIFICA_FULL_BLF.md`); r1 primario, maggioranza 2/3 solo sensibilità (B2 fissata) | riferimento |
| PERM_F | la colonna della famiglia F sostituita con quella di un altro caso, secondo il derangement disgiunto per classe | **primario** |
| OMIT_F | il testo neutrale privato delle frasi di F e delle sue derivate | **secondario**, confondente dichiarato (lunghezza) |

Il ricevente è lo **stesso** in FULL, PERM e OMIT e per tutte le famiglie in cui quel run
compare.

## 3. Famiglie, colonne e derivate

Definizione operativa in `family_map.json`. Quattro famiglie: `level` (`shift_sigma`),
`trend` (`slope_sigma_h`), `residual` (`residual_std_ratio`), `diff` (`diff_std_ratio`).

`raw_std_ratio` **non appartiene a nessuna famiglia**: non si permuta e non si omette mai. Una
quota del testo resta quindi invariata in ogni braccio, e va dichiarato.

**Grandezze derivate inter-famiglia** — in ogni braccio sono **ricalcolate dall'evidenza
effettivamente presente**, mai trasportate (E5-B esteso):

| Derivata | Genitori | In PERM | In OMIT |
| --- | --- | --- | --- |
| `rapid` (residual ∧ diff) | residual, diff | ricalcolata | cade con il genitore |
| episodi di drift coerente, `strict_global_drift` | trend, level | ricalcolati | cadono con il genitore |
| transitorio di assestamento | residual, diff | ricalcolato | cade con il genitore |
| valori per fase di residual/diff | residual, diff | ricalcolati | cade la quota del genitore |

Le ultime tre **non sono nominate in §8.12**: sono un'aggiunta di questo protocollo, dovuta
alla lettura del verbalizzatore congelato.

## 4. Permutazione

Per ogni famiglia F, una permutazione π_F sui casi del sottoinsieme valutato S_F che è un
**derangement** (nessun punto fisso) e **disgiunto per classe** (nessun caso riceve evidenza
dalla propria classe). Campionamento **uniforme sull'insieme ammissibile**, per rifiuto da
permutazioni uniformi (`e5_derangement.py`); seme documentato e congelato; derangement
indipendente per famiglia; costruito **sui soli identificativi**, prima di aprire il test.

La disgiuntività è **per classe, non per meccanismo**: il donatore può condividere il
meccanismo del ricevente. La matrice degli abbinamenti è pubblicata in `DERANGEMENTS_E5.json`.

Posizione temporale del donatore: **nessun vincolo** (decisione F), posizione riportata.

## 5. Omissione

`protocol_omit.py`, file nuovo, schema di `protocol_bnolf.py`: il testo OMIT è definito per
**sottrazione letterale** dal testo congelato, e ogni frase rimossa è rigenerata con gli
helper congelati e tolta una sola volta; una frase che non compare esattamente una volta è un
errore e il rendering fallisce. Il renderer verifica l'hash del verbalizzatore congelato e si
blocca se è cambiato.

Cade: la frase della famiglia, più la frase di `rapid` quando il genitore è `residual` o
`diff`. Restano: la frase di apertura sull'intervallo e la frase sulla dispersione.

## 6. Esiti e regola di lettura

Tabella per famiglia F e meccanismo M: accuratezza FULL, FULL − PERM, FULL − OMIT e
(FULL−PERM) − (FULL−OMIT). Statuto **descrittivo**: intervalli esplorativi, nessun test di
ipotesi, nessuna correzione per molteplicità. Effetto minimo di interesse E5-C1: Δ ≥ 0,10,
soglia di rilevanza e non di significatività; valori negativi riportati come tali.

Regola pre-specificata di §8.12: cali concordi → sensibilità della diagnosi; penalizzazione
maggiore sotto PERM → compatibile con un effetto dell'evidenza incompatibile, riportato con
grandezza e incertezza; esiti discordanti → non conclusivi.

**Intervalli.** Bootstrap a blocchi sui **cicli della permutazione** π_F, ricampionando la
coppia FULL/PERM intera: ogni caso è sia ricevente sia donatore, quindi il run fisico non è
un'unità indipendente e il blocco deve contenere il legame. Gli intervalli sono
**condizionati al derangement realizzato** (seme unico) e vanno riportati così; il numero di
blocchi — non il numero di coppie — è la numerosità effettiva. Dettaglio in
`DECISIONI_AUTORE_E5.md` §E.

## 7. Controllo di lunghezza (E5-C2)

Criterio, per ogni coppia FULL/PERM_F e per ogni caso, **sul prompt completo**:
`|token_PERM − token_FULL| / token_FULL ≤ 5 %`, e zero differenze di troncamento.

Il conteggio si fa **su prompt composti e contati interi** (`verifica_e5_c2_prompt.py`): non
si somma il prefisso al testo né si sottrae il blocco del caso dal prompt, perché con un
tokenizer BPE i conteggi non sono additivi ai confini. Misura di fattibilità sui testi di
sviluppo: `VERIFICA_E5_C2.md`. **E5-C2 chiusa il 2026-09-19 al 5 %, massimo osservato 1,42 %
su 254.400 composizioni.** La verifica sul lotto test è a G3.

Violazione → avvertenza esplicita di confondimento con la lunghezza accanto al contrasto
stratificato; **non** si rigenera il derangement, **non** si riscrive il prompt.

Il controllo con `rapid` congelata al valore vero è **diagnostico**: non è un braccio e non
entra in nessun contrasto riportato.

## 8. Limiti dichiarati

- **Seme unico di derangement:** il risultato è relativo alla corruzione realizzata, non alla
  media su tutte le corruzioni possibili.
- **Donatori di stesso meccanismo:** la disgiuntività è per classe; matrice pubblicata.
- **Meccanismi con un solo fault:** la conclusione riguarda **quella classe**. Per il drift
  lento vale su IDV(13), non sui drift lenti in generale.
- **S_F a due classi per `trend`:** perturbazione specifica fra due classi, non corruzione
  rappresentativa.
- **`raw_std_ratio` mai ablato:** una quota del testo è invariata in ogni braccio.
- **Ricevente:** il bilanciamento riduce la concentrazione, non elimina l'effetto del
  ricevente.

## 9. Pre-impegno sugli esiti

Registrato il 2026-09-12 e qui riaffermato: gli esiti di E5, inclusi effetti nulli, negativi o
discordanti, saranno riportati senza modificare retroattivamente descrittori, soglie,
sottoinsiemi o criteri. Eventuali revisioni successive saranno dichiarate esplorative.
