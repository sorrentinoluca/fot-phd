# Specifica eseguibile della catena OOD e del lotto 03.11

Stato: congelata prima delle nuove sonde. Preserva lo STOP F6 e il lotto 0/89 attestati
dal candidato `1cdf597b9a95e7f1c9a3d6711c2f840c8b5ab6aa` e dal relativo OK acquisito.

## Catena e criteri tecnici invariati

La catena resta `F6→F5→F12`; F4 resta il secondo OOD. F5 usa lo stream 70002 e ID
`chain-F5-001`. F12, eseguibile soltanto se F5 fallisce, usa lo stream 70003 e ID
`chain-F12-001`. Una sonda passa soltanto con manifest/hash validi, unico IDV corretto,
attivazione osservata, nessun trip, fine a 65 h, 8/8 finestre complete e nessun valore
non finito o errore tecnico. Non si leggono prestazioni diagnostiche, feature, score o
separabilita. Non esistono retry o cambi di stream.

La verifica primaria F5 e registrata in `VERIFICA_RILEVABILITA_F5_03_11.md`. Se F5 passa
anche tecnicamente, F5 sostituisce F6 e F12 non viene eseguito. Se F5 fallisce si conserva
l'esito e si verifica F12, che richiede prima la propria prova di rilevabilita. Se F12 non
supera entrambe le condizioni, si mantiene STOP.

## Piani alternativi del lotto, entrambi sigillati prima della sonda

Il lotto attivo dopo PASS F5 e `test_batch_f5`, stream 71000-71088. L'alternativa dopo
fallimento F5 e successivo PASS F12 e `test_batch_f12`, stream 72000-72088. Ciascun piano
contiene esattamente 89 righe in ordine fisso:

- 64 primari fault: catalogo D1 `F1,F2,F3,F8,F10,F13,F14,F15`, 8 run ciascuno;
- 8 primari Normal;
- 6 OOD: 3 run del sostituto attivo e 3 run F4;
- 11 scorte: una per ciascun fault D1, una Normal e una per ciascun OOD.

Le scorte sono soltanto sostitutive secondo il piano rev.10. Tutti i run usano MATLAB
R2025b arm64, il MEX qualificato `834e2361...1d11e`, Mode 1, `ode45`, chiave Philox
`0x464f545445503032`, onset 25 h e stop 65 h. I run Normal mantengono tutti gli IDV a zero.
Nessuna chiamata a Qwen o ad altro modello e ammessa.
