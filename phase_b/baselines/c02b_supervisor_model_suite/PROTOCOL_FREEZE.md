# C02b — protocollo congelato per la suite richiesta dal supervisor

Stato: **FROZEN_BEFORE_MODEL_EVALUATION**  
Data: 2026-09-10  
Parent protocol: `c02b-shared-numeric-prototypes-1.0.0`

## Scopo

Questa suite aggiunge i riferimenti richiesti dal supervisor senza alterare il
confronto diretto class-disjoint già completato. I nuovi modelli sono addestrati
centralmente sui 25 casi development e pertanto sono **riferimenti descrittivi**:
non sono metodi federati e non dimostrano che FoT sia migliore o peggiore in
condizioni di isolamento locale.

## Modelli congelati

1. AdaBoost su firma numerica frozen 697-D.
2. Random Forest su firma numerica frozen 697-D.
3. MLP su firma 697-D standardizzata sul solo development.
4. Classificatore lineare logistico SGD con penalità elastic-net sulla stessa firma.
5. k-NN con `k=3` e voto pesato per distanza sulla stessa firma.
6. LSTM causale unidirezionale con attention su 120 passi × 41 XMEAS.
7. BiLSTM con attention sulla stessa sequenza; non viene chiamata causale perché
   il ramo backward usa informazione successiva nell'intervallo osservato.
8. BiLSTM multimodale con attention, che fonde sequenza numerica e testo neutro
   TF-IDF prodotto dal verbalizzatore frozen.

Gli iperparametri esatti sono in `protocol_config.json`. Non sono previste ricerca
di iperparametri, selezione post-hoc o early stopping sul test.

## Dati e preprocessing

- Development: batch 1–5 per F1/F8/F10/F13 e blocchi Normal N1–N5.
- Held-out: gli stessi PBH-001…PBH-015 usati da FoT.
- Target del training: soltanto pseudolabel opache.
- Firma tabellare: vettore V2 frozen 697-D, precedente alla resa testuale.
- Sequenza: intervallo `[10 h, 50 h)`, un campione ogni 20 minuti, 120 passi.
- Normalizzazione sequenziale: media/deviazione dei soli blocchi Normal N1–N5,
  clipping z-score a `[-10, 10]` e divisione per 10.
- TF-IDF: vocabolario appreso soltanto sui 25 testi development.
- Missing, non finiti, dimensioni o hash errati: arresto completo; nessuna
  imputazione o esclusione selettiva.

## Valutazione

Le predizioni held-out senza verità vengono scritte prima di caricare il manifest
evaluator-side. Sono riportate accuratezza sui 15 casi fisici, recall per classe,
matrice di confusione e accuratezza local-seen/local-unseen quando la predizione
centralizzata viene proiettata sui quattro agenti. Gli intervalli bootstrap
ricampionano i casi fisici e non le copie agente-caso.

Il modello principale class-disjoint rimane la baseline a prototipi condivisi.
Questa suite non cambia retroattivamente il suo protocollo né i suoi risultati.
