# C02b supervisor model suite

Riferimenti centralizzati richiesti dal supervisor, eseguiti sullo stesso split
development/held-out di FoT. La suite comprende AdaBoost, Random Forest, MLP,
lineare elastic-net, k-NN, LSTM causale con attention, BiLSTM con attention e
fusione multimodale BiLSTM+testo.

Questi modelli vedono tutte le pseudoclassi nel development: sono confronti
descrittivi e non sostituiscono la baseline class-disjoint a prototipi condivisi.

Esecuzione:

```bash
python -m phase_b.baselines.c02b_supervisor_model_suite.run_suite
```

Il runner verifica gli hash frozen, usa solo pseudolabel opache e scrive
`predictions_unscored.csv` prima di caricare la verità evaluator-side.
