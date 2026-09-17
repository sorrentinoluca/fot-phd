# Report verifica sintetica H3

## Esito §5

**PENDING.** I 108/108 punti al bordo con ICC=0 soddisfano `phat ≤ 0,055` e il controllo
dell'implementazione non ha rilevato errori, ma la review indipendente `b567` non è ancora stata
eseguita. Non si autocertifica quindi **TANGO MANTENUTO**. Nessun punto ICC>0 modifica l'esito.

Sono stati completati 1.596 scenari fattibili × 100.000 repliche = **159.600.000** repliche
valide, con zero errori numerici. I 24 target ICC non fattibili sono registrati in
`SCENARI_INFEASIBLE.csv`; nessun target ICC=0 è escluso. Il massimo al bordo decisivo è
**phat=0,05128** (5.128/100.000; MCSE 0,00069750; Clopper–Pearson 95%
[0,04992096; 0,05266514]) nello scenario 380: Δ3=−0,125, d=0,60, a=1, b=0,5,
pattern tempo/interazione, ICC=0.

## Robustezza descrittiva ICC

La tabella riporta, a ogni ICC, il massimo `phat` tra i punti applicabili e lo scenario che lo
produce. Gli intervalli sono Clopper–Pearson 95%; il dettaglio per tutte le 324 famiglie è in
`TABELLA_ROBUSTEZZA_ICC.csv`.

| Procedura | ICC 0 | ICC 0,05 | ICC 0,10 | ICC 0,20 | ICC 0,40 | massimo ICC testato con tutti i punti ≤0,055 |
|---|---:|---:|---:|---:|---:|---:|
| Tango H3 | 0,05128 (380) | 0,07976 (451) | 0,10565 (412) | 0,14699 (363) | 0,21383 (104) | **0** |
| Hoeffding H3 | 0,00505 (455) | 0,01533 (416) | 0,02696 (407) | 0,05143 (418) | 0,09651 (419) | **0,20** |
| Hoeffding H1/H2 | 0,00503 (945) | 0,01426 (1041) | 0,02542 (952) | 0,05025 (953) | 0,09696 (1049) | **0,20** |

Le sequenze dei massimi non sono non-monotone. A livello di singola famiglia, Tango non mostra
decrementi; Hoeffding H3 ne mostra 6 (calo massimo 0,00002) e Hoeffding H1/H2 3 (calo massimo
0,00001), compatibili con la granularità Monte Carlo e riportati senza interpolazione. Per H1/H2
sono applicabili 108 famiglie a ICC=0 e 102 agli ICC positivi; le altre 6 famiglie generano i 24
target `INFEASIBLE`. H1 e H2 coincidono e non sono contati come simulazioni indipendenti.

## Riproducibilità

Il run usa lo script e il manifest congelati nel commit 1 `b465f90373debfe4ae252389cda4b13154a0e13b`,
seed 20260917, PCG64 con stream per scenario e batch 10.000. Il tempo di calcolo registrato è
192,3 s; per la review indipendente si attende circa **4–5 minuti**, oltre al confronto degli
artefatti. Comando unico di replay su una directory nuova:

```bash
bash studio2/fase03/protocollo_finale/verifica_sintetica_h3/REPLAY_B567.sh /tmp/h3-b567-replay
```

La verifica è solo locale H3 e non simula il FWER congiunto H1→H2→H3.
