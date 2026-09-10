# C02b — confronti richiesti dal supervisor

## Esito in breve

Sono stati eseguiti tutti i gruppi richiesti: boosting, MLP, Random Forest, lineare elastic-net, k-NN, LSTM causale con attention, BiLSTM con attention e una BiLSTM multimodale sequenza+testo. I risultati sotto sono riferimenti centralizzati: vedono tutte le pseudoclassi nei soli dati development e non sono presentati come metodi federati.

## Risultati held-out

| Modello | 15 casi | 12 fault | Local-unseen proiettato | Train | Modello byte | Bootstrap 95% |
|---|---:|---:|---:|---:|---:|---:|
| AdaBoost | 15/15 (100.0%) | 12/12 (100.0%) | 36/36 (100.0%) | 100.0% | 155892 | [100.0%, 100.0%] |
| Random Forest | 15/15 (100.0%) | 12/12 (100.0%) | 36/36 (100.0%) | 100.0% | 678428 | [100.0%, 100.0%] |
| MLP | 15/15 (100.0%) | 12/12 (100.0%) | 36/36 (100.0%) | 100.0% | 1591028 | [100.0%, 100.0%] |
| Lineare elastic-net | 15/15 (100.0%) | 12/12 (100.0%) | 36/36 (100.0%) | 100.0% | 46146 | [100.0%, 100.0%] |
| k-NN | 15/15 (100.0%) | 12/12 (100.0%) | 36/36 (100.0%) | 100.0% | 157548 | [100.0%, 100.0%] |
| LSTM causale + attention | 15/15 (100.0%) | 12/12 (100.0%) | 36/36 (100.0%) | 100.0% | 39999 | [100.0%, 100.0%] |
| BiLSTM + attention | 14/15 (93.3%) | 11/12 (91.7%) | 33/36 (91.7%) | 100.0% | 53857 | [80.0%, 100.0%] |
| BiLSTM multimodale + attention | 14/15 (93.3%) | 11/12 (91.7%) | 33/36 (91.7%) | 100.0% | 108201 | [80.0%, 100.0%] |

## Confronti già disponibili

La baseline class-disjoint a prototipi condivisi rimane il confronto diretto: 36/36 local-unseen (100%). FoT-B ha ottenuto 31/36 (86,1%). Questi denominatori sono viste agente-caso; l'incertezza continua a usare i 12 casi fisici fault. Non si deve usare la tabella centralizzata per sostenere una superiorità federata.

## Recall per pseudoclasse

| Modello | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |
|---|---:|---:|---:|---:|---:|
| AdaBoost | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Random Forest | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| MLP | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Lineare elastic-net | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| k-NN | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| LSTM causale + attention | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| BiLSTM + attention | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 |
| BiLSTM multimodale + attention | 3/3 | 3/3 | 3/3 | 2/3 | 3/3 |

## Matrici di confusione

Righe = verità, colonne = predizione; ogni riga contiene tre casi fisici.

### AdaBoost

| Vera \ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |
|---|---:|---:|---:|---:|---:|
| CLS-ZOGAA | 3 | 0 | 0 | 0 | 0 |
| CLS-OJNSG | 0 | 3 | 0 | 0 | 0 |
| CLS-R463B | 0 | 0 | 3 | 0 | 0 |
| CLS-Z3ISU | 0 | 0 | 0 | 3 | 0 |
| Normal | 0 | 0 | 0 | 0 | 3 |

### Random Forest

| Vera \ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |
|---|---:|---:|---:|---:|---:|
| CLS-ZOGAA | 3 | 0 | 0 | 0 | 0 |
| CLS-OJNSG | 0 | 3 | 0 | 0 | 0 |
| CLS-R463B | 0 | 0 | 3 | 0 | 0 |
| CLS-Z3ISU | 0 | 0 | 0 | 3 | 0 |
| Normal | 0 | 0 | 0 | 0 | 3 |

### MLP

| Vera \ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |
|---|---:|---:|---:|---:|---:|
| CLS-ZOGAA | 3 | 0 | 0 | 0 | 0 |
| CLS-OJNSG | 0 | 3 | 0 | 0 | 0 |
| CLS-R463B | 0 | 0 | 3 | 0 | 0 |
| CLS-Z3ISU | 0 | 0 | 0 | 3 | 0 |
| Normal | 0 | 0 | 0 | 0 | 3 |

### Lineare elastic-net

| Vera \ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |
|---|---:|---:|---:|---:|---:|
| CLS-ZOGAA | 3 | 0 | 0 | 0 | 0 |
| CLS-OJNSG | 0 | 3 | 0 | 0 | 0 |
| CLS-R463B | 0 | 0 | 3 | 0 | 0 |
| CLS-Z3ISU | 0 | 0 | 0 | 3 | 0 |
| Normal | 0 | 0 | 0 | 0 | 3 |

### k-NN

| Vera \ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |
|---|---:|---:|---:|---:|---:|
| CLS-ZOGAA | 3 | 0 | 0 | 0 | 0 |
| CLS-OJNSG | 0 | 3 | 0 | 0 | 0 |
| CLS-R463B | 0 | 0 | 3 | 0 | 0 |
| CLS-Z3ISU | 0 | 0 | 0 | 3 | 0 |
| Normal | 0 | 0 | 0 | 0 | 3 |

### LSTM causale + attention

| Vera \ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |
|---|---:|---:|---:|---:|---:|
| CLS-ZOGAA | 3 | 0 | 0 | 0 | 0 |
| CLS-OJNSG | 0 | 3 | 0 | 0 | 0 |
| CLS-R463B | 0 | 0 | 3 | 0 | 0 |
| CLS-Z3ISU | 0 | 0 | 0 | 3 | 0 |
| Normal | 0 | 0 | 0 | 0 | 3 |

### BiLSTM + attention

| Vera \ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |
|---|---:|---:|---:|---:|---:|
| CLS-ZOGAA | 3 | 0 | 0 | 0 | 0 |
| CLS-OJNSG | 0 | 3 | 0 | 0 | 0 |
| CLS-R463B | 0 | 0 | 2 | 0 | 1 |
| CLS-Z3ISU | 0 | 0 | 0 | 3 | 0 |
| Normal | 0 | 0 | 0 | 0 | 3 |

### BiLSTM multimodale + attention

| Vera \ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal |
|---|---:|---:|---:|---:|---:|
| CLS-ZOGAA | 3 | 0 | 0 | 0 | 0 |
| CLS-OJNSG | 0 | 3 | 0 | 0 | 0 |
| CLS-R463B | 0 | 0 | 3 | 0 | 0 |
| CLS-Z3ISU | 0 | 1 | 0 | 2 | 0 |
| Normal | 0 | 0 | 0 | 0 | 3 |

## Interpretazione e limiti

- I modelli hanno soltanto cinque casi development per classe: il confronto è molto piccolo e gli intervalli riflettono appena 15 casi held-out.
- LSTM causale e BiLSTM sono varianti separate: una rete bidirezionale non è causale in senso stretto.
- La variante multimodale usa due rappresentazioni degli stessi sensori (sequenza numerica e testo neutro), non una seconda sorgente fisica indipendente.
- MLP, lineare e k-NN usano scaling fit solo sul development; nessun metodo usa il test per preprocessing, tuning o vocabolario.
- Questi modelli centralizzano i dati e quindi non risolvono da soli C02b. Lo stato resta **Mitigata**, non 'risolta sperimentalmente'.

## Riproducibilità

Protocollo, configurazione, predizioni non valutate e valutate, metriche, matrici, modelli serializzati, storie di training e hash SHA-256 sono nella presente cartella.
