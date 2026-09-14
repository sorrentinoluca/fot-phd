# Conteggio completo delle richieste — allegato contabile alla revisione 10

Data: 2026-09-14. Prospetto contabile, **non autorizzazione di spesa o di esecuzione**.
A è approvata da Luca il 14 settembre 2026: il tetto rigido 3.700 è sostituito
dalla regola di conteggio completo e fattibilità misurata del piano §7.2.
Fonte: [APPROVAZIONE_ADDENDUM_03_8.md](APPROVAZIONE_ADDENDUM_03_8.md).
Gli scenari e i parametri operativi sottostanti non diventano per questo approvati
o misurati. La versione preparatoria resta intatta al commit `526561f`.
Fonti: piano statistico rev. 9 §§7–11; piano generale §§8.3–8.4, 8.7–8.8 e 8.12;
decisioni storiche, Allegato B. Nessun pilot eseguito per compilare questa tabella.

## Modelli e unità

C = consumer definitivo; P = producer principale; A = producer alternativo.
Sono **ruoli**, da aggregare per identità effettiva del modello senza contare due
volte le richieste se C=P. D9 resta aperta; nessun confronto completo aggiuntivo.
Il nuovo candidato dichiarato dal referente è `qwen3.8-27b`, contesto 262144,
output massimo 32768: dati comunicati, non capacità misurate in questa sessione.
Non identifica pesi/revisione/quantizzazione. La precedente osservazione
`Qwen/Qwen3.8-27B-FP8`, revisione
`017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, riguarda il vecchio server,
non prova identità del nuovo servizio né disponibilità di Qwen3.8-2.4T-A95B.

Una richiesta inviata conta anche se fallisce. Riparsare localmente non invia
richieste. R conta ripetizioni di inferenza del disegno, non retry, giorni,
insight prodotti o run simulati. Token disponibili ≠ chiamate ≠ tempo disponibile.

## Blocchi a D2=8

| Blocco / modello destinatario | Regola | R studio=1 | R studio=3 |
| --- | --- | ---: | ---: |
| Nucleo local-unseen / C | 8×8×7×3×R | 1.344 | 4.032 |
| Nucleo local-seen / C | 8×8×1×3×R | 192 | 576 |
| Nucleo Normal / C | 8×8×3×R | 192 | 576 |
| **Nucleo totale / C** | 1.728×R | **1.728** | **5.184** |
| Audit aggiuntivo / C | 173 prompt del nucleo portati a 3 ripetizioni | 346 | 0 |
| Misura producer-swap / C | 4×8×7×R, B-LF con libreria A | 224 | 672 |
| Ablation B-senza-LF / C | (8×8 + 4×3×7)×R | 148 | 444 |
| OOD / C | 2×3×8×3×R | 144 | 432 |
| E5 corrotto / C | **R E5=1**: 16×S, S=Σ(m_F+c_F) | 16S | 16S |
| E5 FULL aggiuntivo / C | 8×U se non riusabile, U=numero fault distinti nell'unione; altrimenti 0 | 0…64 | 0…64 |
| Canary / C | 10 richieste per giorno di esecuzione d | 10d | 10d |
| Produzione libreria principale / P | G_P richieste ulteriori rispetto a conformità già conteggiata | G_P | G_P |
| Produzione libreria alternativa / A | G_A richieste ulteriori rispetto a conformità già conteggiata | G_A | G_A |
| Pilot / C, P, A | tabella sotto, richieste effettive una volta sola | P_tot | P_tot |
| Verifiche tecniche ulteriori / rispettivo modello | X, escludendo quelle già nel pilot | X | X |
| Retry ulteriori fuori pilot / rispettivo modello | Q, solo entro politica operativa congelata 03.10 | Q | Q |

Il campione audit definitivo è selezionato deterministicamente e bilanciato dalla
03.10: 173 è il conteggio di pianificazione arrotondato da 172,8; se la selezione
documenta k prompt, usare `2k` a R=1 e zero aggiuntivo a R=3. A R=3 si riusano
le tre ripetizioni già previste, conservando selezione e reporting dell'audit.
Le misure swap, ablation e OOD seguono R dello studio; E5 conserva l'eccezione
esplicita R=1. Il set canary resta 10/giorno, non 30/giorno.

Il margine storico di ~20 per la libreria alternativa e ~30 per quella principale
era una stima, non una cardinalità da triplicare. Il contratto corrente produce
16 insight in 8 richieste per libreria. Con riuso valido degli output di conformità
G_P/G_A=0; senza riuso, 8 ciascuno prima di eventuali retry contabilizzati in Q.
Riuso solo con identità di casi, input, template, schema e configurazione e
provenienza verificata: gli output scartati prima della remediation non sono riusabili.
Se le otto richieste alternative sono differite dal pilot alla produzione, spostarle
fra P_tot e G_A, senza sommarle in entrambi. La parità strutturale resta obbligatoria.

Per E5 S e U restano parametrici: 192 è accantonamento prudenziale (S=12),
176 è scenario S=11, nessuno dei due sceglie la mappa finale o un controllo extra.
FULL si riusa soltanto se coincidono caso, ricevente, prompt completo, modello/config,
decoding e aggregazione. A R=3 l'aggregazione deve ancora essere verificata:
non si assume il riuso solo perché la condizione si chiama B-LF. Nessun audit E5
aggiunto; il limite di stabilità non misurata su E5 resta dichiarato.

## Pilot: conteggio per modello e riserva unica

| Blocco | Destinatario | Richieste |
| --- | --- | ---: |
| Conformità principale | P | 8 |
| Remediation completa, se autorizzata sul diff | P | 8r, r∈{0,1} |
| Sonda budget | C | b∈{3,6,9} |
| Gate unico 40×3 | C | 120 |
| Conformità alternativa, se D9 configurata | A | 8a, a∈{0,1} |
| Trasporto documentato | modello della richiesta | t=t_P+t_C+t_A |

`P_tot=128+b+8r+8a+t`, con `8r+t≤15` e **hard stop cumulativo 200**.
Il trasporto è ammesso solo negli stadi e con le prove previste dall'Allegato B;
la sua attribuzione contabile ad A non autorizza una procedura alternativa nuova.
Sonda: solo triplette complete e prova zero token; gate: nessuna ripetizione.
Per la sonda la quota 8 resta indisponibile anche se r=0: ogni tripletta ripetuta
richiede `t_già_consumato+3≤7`, dunque al massimo due triplette se non è stato
consumato trasporto precedente. Le 15 ripetizioni senza remediation sono
consentite nella sola conformità, non nella sonda.
Le 8 richieste accantonate all'alternativo non finanziano altri blocchi.

| Caso | a=0 | a=1 |
| --- | ---: | ---: |
| r=0, t=0, b=3…9 | 131…137 | 139…145 |
| r=1, t=0, b=3…9 | 139…145 | 147…153 |
| b=9, riserva interamente consumata (`8r+t=15`) | **152** | **160** |

Le 40 richieste fra 160 e hard stop 200 non sono spendibili per differenza.
I massimi di tabella includono già la riserva: non aggiungere un altro 10% al pilot.
Richieste già inviate nella storia del pilot devono entrare nello stesso ledger:
nuova directory, template o processo non azzerano il contatore. Il prospetto
parametrico non certifica che oggi siano disponibili tutte le 200 richieste.

## Totale e finestra operativa

Con k=173: `N = 2244R + 346·1[R=1] + 16S + 8U_nonriusato + 10d
+ G_P + G_A + P_tot + X + Q`.
Per modello: C riceve le misure, E5, audit, canary, `120+b+t_C`;
P riceve `8+8r+t_P+G_P`; A riceve `8a+t_A+G_A`. Ripartire X e Q per modello;
se due ruoli coincidono, sommare le loro richieste distinte nello stesso ledger.

Esempio contabile **non approvato né previsione definitiva**: S=12, d=10,
FULL riusabile, librerie riusabili, P_tot=160, X=100, Q=0:
**3.142 a R=1; 7.284 a R=3**, prima di retry fuori pilot. Senza FULL aggiungere
al massimo 64; senza entrambe le librerie aggiungere 16. I 160 comprendono già
la conformità alternativa. X=100 e d=10 sono le vecchie ipotesi prudenziali,
non misure sul servizio nuovo; S e riuso restano da congelare.

I totali storici ~2.594/~3.232 pre-retry e ~2.853/~3.555 con +10% restano
ricostruibili nella tabella §8.8, comprese le stime di produzione ~30/~20,
pilot ~200 e canary ~100. I delta fra quelle stime arrotondate sono +638,
+702 (+24,6%). Non sono totali esatti del nuovo ledger e il +10% storico
non è un'autorizzazione a retry automatici o a moltiplicare riserve già comprese.
Il ledger finale deve assegnare Q alle sole richieste eleggibili, indicando
la politica, la capienza e il tempo; senza questi dati il totale con retry è pending.

Per la fattibilità usare tempi misurati per blocco/modello/configurazione, non
trasferire le latenze del vecchio server. In esecuzione sequenziale:
`T=Σ N_(blocco,modello) × latenza_media_(blocco,modello)`, con tempi di
attesa/remediation e altri vincoli operativi espliciti; verificare `1,20×T≤W`,
dove W è la finestra effettivamente disponibile del piano. Qualunque vantaggio
da concorrenza richiede misura, non divisione teorica per numero di worker.
La generazione TEP ha un proprio cammino temporale e non consuma richieste API.
I giorni d vanno ricavati dal calendario candidato, includendo i canary nel
tempo, fino a un calendario coerente: non lasciare d=10 se il calendario cambia.
Modello D9, X/Q, mappa E5, riusi, latenza, disponibilità e calendario sono pending;
nessun GO T5 può derivare dalla sola disponibilità di token.
