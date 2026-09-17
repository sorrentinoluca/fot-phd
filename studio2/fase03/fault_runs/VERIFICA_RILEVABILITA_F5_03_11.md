# Verifica prescritta di rilevabilita F5 — 03.11

Data: 2026-09-15. Perimetro: sola condizione bibliografica minima richiesta al primo
sostituto della catena congelata `F6→F5→F12`. Questa verifica non seleziona su risultati
del nostro simulatore e non cambia criteri, catena o soglie.

Fonte primaria: Xiao, Kordon e Sen (2023), *Fault Detection and Diagnosis in Tennessee
Eastman Process with Deep Autoencoder*, Annual Conference of the PHM Society 15(1),
DOI `10.36001/phmconf.2023.v15i1.3578`. PDF locale: 721.381 byte, SHA-256
`e11310c44cebca7a6ebc368b3862dc2edc0003a4ee31cb9223feb6d5e0ae7b78`.

La Tabella 2 a p. 6 e stata controllata visivamente sulla pagina renderizzata. Le colonne
sono i fault; la colonna F5 appartiene al gruppo *Back to control Faults*. Le righe sono i
tre rivelatori. Per F5 la tabella riporta FDR: **DAE 100%, PCA-T2 29%, PCA-SPE 31%**.
La stessa pagina riporta FAR **3,1%, 1,9%, 6,3%** e ritardo **0 min** per tutti e tre.

Esito della sola condizione prescritta: **PASS**. Esiste un numero esterno primario
riverificato per F5, come richiesto per rendere utilizzabile il sostituto. Non viene imposta
una soglia FDR universale: il 29-31% dei due rilevatori PCA mostra dipendenza dal metodo e
vieta di descrivere F5 come uniformemente facile. Questi numeri non provano generabilita,
ammissibilita tecnica o prestazione FoT; la sonda tecnica successiva resta obbligatoria.
