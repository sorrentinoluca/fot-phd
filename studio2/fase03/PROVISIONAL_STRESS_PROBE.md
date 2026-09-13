# Fase 03 — sonda tecnica provvisoria sulla fixture di stress

Stato: **PASS tecnico provvisorio; ripetizione sui 40 prompt reali obbligatoria prima del gate**.

La sonda è stata eseguita il 13 settembre 2026 esclusivamente sulla fixture sintetica
`cap_stress`. Non congela la configurazione di generazione, non autorizza il gate 40×3 e non
supporta alcuna conclusione scientifica.

## Perimetro e contatore

- piano: `SYNTHETIC_CAP_STRESS_TECHNICAL_PROBE_ONLY`, 40 prompt sintetici;
- prompt massimi scelti: A 6.579 token, B-LF 9.875, E-LF 9.875;
- richieste API complessive: 4;
- inferenze completate: 3;
- primo POST: HTTP 400 prima dell'inferenza, perché vLLM 0.28.0 non implementa la keyword JSON
  Schema `uniqueItems` nella grammatica guidata;
- tre POST successivi: HTTP 200, senza retry;
- chiamate al gate di stabilità: 0;
- chiamate al producer: 0.

Il contratto canonico non è stato allentato: conserva `uniqueItems=true` e il parser locale
rifiuta autonomamente ID duplicati. Solo la copia dello schema inviata alla grammatica vLLM
omette la keyword incompatibile. SHA-256 dello schema canonico:
`c4f73e784d281983a0a564c96ac59f2653871ecc6cc8936c9254278ce9e3e60a`; SHA-256 canonico
della variante per la grammatica:
`4bde5d3a53372bb1629502f305bbab2539f74b7db3f33d5a00c55ee58230c9a3`.

## Risultato

| Condizione | Prompt | Input | Completion | Latenza | Finish | Parsing primo tentativo |
| --- | --- | ---: | ---: | ---: | --- | --- |
| A | `S2-P03-031` | 6.579 | 409 | 32,8 s | `stop` | valido |
| B-LF | `S2-P03-004` | 9.875 | 2.174 | 152,5 s | `stop` | valido |
| E-LF | `S2-P03-005` | 9.875 | 835 | 62,3 s | `stop` | valido |

Il primo candidato, `thinking_token_budget=2048`, `max_tokens=2560`, temperatura 0 e seed
20260829, soddisfa sulla fixture sintetica la regola «tutte e tre le condizioni terminano con
`stop` e sono valide al primo parsing». È quindi una selezione **provvisoria**, non un budget
congelato. I candidati 3072 e 4096 non sono stati chiamati.

Gli artefatti macchina sono `results/provisional_cap_stress/provisional_stress_probe_records.jsonl`
e `results/provisional_cap_stress/provisional_stress_probe_summary.json`. L'hash del file dei
prompt è `90744d3d3f708d09fa45f45928dda05a8f8ae023c117a147a92af57e91d625e0`; quello dei record è
`825b649e409e462b953da263fd01d11b9d92563fd930747da17e36f93d94b158`; quello del riepilogo è
`c9adf2a8f07d9058257cc2c51a00064662874611875a715c716a1f1ea4828368`. Il fingerprint del processo
è `39b59324e643e892bfdd05beac763aa9ca80092941f28ce01f582f0f3a593017`.

Non esiste `frozen_gate_config.json`: il runner registra esplicitamente
`generation_budget_frozen=false`, `stability_gate_authorized=false` e
`scientific_claims_authorized=false`.

## Durata e pianificazione

Le tre latenze sommano 247,7 secondi, circa 4 minuti e 8 secondi. Proiettando le latenze dei tre
prompt massimi sulla composizione 8 A + 16 B-LF + 16 E-LF e su tre ripetizioni, il solo gate a
2048 vale circa 3,08 ore sequenziali. È una proiezione da tre osservazioni sintetiche, influenzata
anche dalla compilazione JIT tardiva segnalata dal server, e non una misura sufficiente per il
dimensionamento definitivo.

Per pianificare la ripetizione reale si mantengono intervalli cautelativi: 4–7 minuti se passa il
primo candidato e 20–35 minuti se servono tutti e nove i tentativi; gate 40×3 circa 3–5 ore a
2048, 4,5–7 ore a 3072 e 6–9 ore a 4096. La vecchia stima unica di 3–6 ore non copriva in modo
esplicito prompt da 9.875 token e thinking massimo. Il costo API diretto dell'endpoint locale è
€0; energia e costo-opportunità della GPU restano non prezzati.

## Condizione necessaria per procedere

Dopo la sessione decisionale su catalogo definitivo e producer alternativo occorre creare e
congelare il manifest scientifico, renderizzare i 40 prompt reali e ripetere la sonda su quei
prompt. Solo quella ripetizione può selezionare il budget, scrivere `frozen_gate_config.json` e
rendere presentabile una richiesta di autorizzazione separata per il gate 40×3.
