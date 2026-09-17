# Specifica del preflight tecnico OOD — sotto-fase 03.11

Stato: pre-specificato prima di ogni simulazione 03.11. Il preflight e distinto dal lotto
finale e non produce osservazioni scientifiche, feature, evidence o prompt.

## Oggetto e fonti normative

Il tag annotato `studio2-fase03-piano-statistico-frozen-001`, peeled commit
`11f504b2bf45a39c1bc4746952f50d58c5022743`, e efficace e raggiungibile da
`origin/main`. Il piano rev.10 prescrive F6/F4, le catene F6→F5→F12 e F4→F11→F5,
e i controlli tecnici prima del batch e di qualunque chiamata sui test.

La prima coppia di sonde e fissata nell'ordine F6, F4 con stream Philox disgiunti
`70000`, `70001`, chiave radice `0x464f545445503032`, identificativi
`preflight-F6-001`, `preflight-F4-001`. I sostituti non vengono eseguiti in anticipo:
si apre il membro successivo della sola catena attivata, e soltanto se la sua verifica
di rilevabilita richiesta dal piano e gia disponibile. Nessun esito puo cambiare ordine,
seed, durata o criterio.

## Configurazione e ammissibilita

Si usa il generatore qualificato dei fault di sviluppo: MATLAB R2025b arm64, Mode 1,
solver `ode45`, `Ts_base=0.0005 h`, salvataggio a `1/60 h`, stato iniziale qualificato,
MEX strumentato equivalente SHA-256
`834e2361915249402a1ec9074a4be04f22a6404deb841e5134bf34347dfde544`, un solo
IDV, innesco 25 h, stop 65 h, nessun cambio di setpoint.

Una sonda e tecnicamente ammissibile solo se: il manifest e tutti gli hash sono validi;
l'IDV prescritto e l'unico attivo ed e osservato all'innesco; il run raggiunge 65 h senza
trip fisico; tutte le otto finestre half-open da 5 h in `[25,65)` sono complete; non vi
sono errori tecnici o valori non finiti. Un trip e conservato come `physical_trip`, non
ritentato e non promosso. Non si ispezionano XMEAS, feature, score o separabilita.

F6 e F4 hanno gia la verifica bibliografica minima prescritta. I documenti congelati
dichiarano invece assente un numero riverificato per F5/F11/F12: se una sonda attiva
una di queste sostituzioni e tale prova e ancora assente, la procedura si ferma senza
promozione automatica e senza avviare il lotto da 89 run.

## Separazione delle fasi

Il preflight scrive nella destinazione esclusiva ignorata
`fault_runs/ood_preflight/ood_preflight_001`. Il batch finale, se autorizzabile, avra
un piano e una destinazione distinti. Audit e sigillo sono operazioni successive e
separate; nessuna chiamata Qwen o ad altro modello e ammessa in questa sotto-fase.
