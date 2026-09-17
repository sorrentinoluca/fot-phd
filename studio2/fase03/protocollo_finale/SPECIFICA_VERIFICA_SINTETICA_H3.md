# Specifica della verifica sintetica indipendente H3 — Q2

Revisione 1, 2026-09-17. **SPECIFICA PRE-DATI, NON ESECUZIONE NÉ ESITO.**
Fonte: `DECISIONI_AUTORE_7_3_REV2_Q1_Q3.md`, appendice Q2; raccordo all’addendum revisione 2,
§4. La sotto-fase distinta dovrà produrre script riproducibile, risultati e review indipendente.
Qui non si scrive né si esegue lo script di simulazione. Fattori condivisi fissi sono condizionati; l’indipendenza dei run è un’assunzione per tutte
le procedure (addendum §1), sostenuta dagli stream distinti ma esposta alla deriva LLM
residua. Nessuna lettura di dati TEP, evidence,
risposte dei modelli o parametri stimati sul test, e nessuna modifica al piano 03.8 congelato.

## 1. Quantità, decisione e criteri già fissati dall’autore

N=64 coppie appaiate, una per cella di una matrice 8 fault × 8 posizioni. Definire
D=+1 per B corretto/A errato, D=−1 per B errato/A corretto, D=0 per concordanza;
Δ3=media delle 64 medie di cella; discordanza d=P(D≠0); m=0,125.
Tango è quello del piano 03.8 §§4.3–4.4, con formula/implementazione congelata da identificare
per commit e SHA nello script e controllare indipendentemente, incluse celle/conteggi degeneri.
Decisione nominale unilaterale alpha=0,05 (`Z > z_0,95`); sensibilità a 0,025 separata.

Livello: bordo Δ3=−0,125. Potenza: Δ3=0 e +0,05. Per ogni punto **100.000 repliche**,
mai meno. Successo richiesto: frequenza empirica di rifiuto **≤0,055 in ogni punto della
griglia al bordo a ICC=0**, nominale 0,05; nessuna media fra scenari, nessuna rimozione di punti
sfavorevoli. Riportare errore Monte Carlo `sqrt(phat*(1−phat)/100000)` e intervallo binomiale
Clopper–Pearson al 95% per punto. A p=0,055, MCSE≈0,000721. Il criterio dell’autore riguarda
phat, non il limite superiore dell’intervallo; non cambiarlo implicitamente. La griglia non
è una garanzia uniforme su tutte le distribuzioni. Nessuna soglia di potenza è imposta:
la potenza si riporta, non decide quale test scegliere.

## 2. Griglia numerica pre-specificata

La seguente concretizzazione usa esclusivamente distribuzioni sintetiche. Ordine degli assi:

| Asse | Valori |
| --- | --- |
| Δ3 | −0,125; 0; +0,05 |
| Discordanza media d | 0,15; 0,30; 0,60; 0,90 |
| Ampiezza eterogeneità discordanza a | 0; 0,5; 1 |
| Ampiezza eterogeneità effetto b | 0; 0,5; 1 |
| Pattern (z,v) | fault/tempo; tempo/interazione; interazione/fault |
| ICC target medio entro fault rho | 0; 0,05; 0,10; 0,20; 0,40 |

Totale cartesiano: **1.620 scenari target**, 540 al bordo e 1.080 di potenza;
**108 punti al bordo a ICC=0** decidono Tango/fallback. Massimo 162.000.000 repliche
se tutti i target ICC sono fattibili; fattibilità dei soli stress è verificata in §3.
Scenari con parametri ridondanti restano identificati e riportati, senza reinterpretarli come
prove indipendenti. Gli assi a=b=0 includono il riferimento omogeneo.

Per f,j=0,…,7, siano F_fj=−1 se f<4, +1 altrimenti; T_fj=−1 se j<4, +1 altrimenti;
I_fj=F_fj*T_fj. I tre pattern sono (F,T), (T,I), (I,F), tutti bilanciati.
Definire, nell’ordine:

- `A = min(d−abs(Δ3), 1−d)`;
- `d_fj = d + a*A*z_fj`; `d_min = d−a*A`;
- `B = d_min−abs(Δ3)`;
- `delta_fj = Δ3 + b*B*v_fj`;
- `p_plus_fj = (d_fj+delta_fj)/2`;
- `p_minus_fj = (d_fj−delta_fj)/2`; `p_zero_fj=1−d_fj`.

Controllare **prima** della simulazione: ogni probabilità finita in [0,1], somma=1 entro
1e−12, media d_fj=d e media delta_fj=Δ3 entro 1e−12. La costruzione garantisce
`abs(delta_fj)≤d_fj`, anche nei casi estremi; eventuali errori implementativi producono FAIL,
non clipping né eliminazione dello scenario. Per rappresentare la coppia binaria completa,
dividere p_zero fra entrambi corretti ed entrambi errati in parti uguali; lo score della
differenza dipende soltanto dai conteggi discordanti e da N.

## 3. Stress ICC: descrittivo per Tango, Hoeffding H3 e H1/H2

Gli ICC>0 sono **solo descrittivi** e non attivano il fallback. Con marginali eterogenee non
esiste automaticamente un unico ICC equicorrelato realizzabile. Definizione operativa:
rho è la **media delle correlazioni Pearson delle coppie di celle non degeneri entro ciascun
fault**, non una richiesta che tutte le correlazioni di coppia siano identiche. Il paper
riporta questa definizione, range delle correlazioni e modello generativo; non usa il peso
di una miscela come se fosse l’ICC.

Per ogni replica e fault, indipendentemente dagli altri fault, estrarre C_f~Bernoulli(lambda_f).
Con C_f=0 usare otto uniformi indipendenti; con C_f=1 un uniforme condiviso sulle otto celle.
Applicare le inverse CDF marginali nell’ordine −1,0,+1. Questa miscela mantiene esattamente
le probabilità di §2 e Δ3. A lambda_f=0 i run sono indipendenti.

**Calibrazione analitica, prima delle simulazioni:** calcolare le covarianze sotto uniforme
condiviso tramite intersezione degli intervalli CDF delle categorie. Sia c_f la media delle
correlazioni Pearson così ottenute sulle coppie con varianza non nulla. La miscela moltiplica
ciascuna covarianza per lambda_f; per il target rho scegliere `lambda_f=rho/c_f`.
Richiedere 0≤lambda_f≤1. Celle degeneri e coppie escluse dal calcolo sono elencate.
Se c_f=0 o non definito, solo rho=0 è applicabile; se rho>c_f, lo stress è **INFEASIBLE**
per quella matrice, non simulato né sostituito/clippato. Non è un FAIL di Tango e non
esclude alcun punto ICC=0 dal criterio. Riportare matrice/fault e limite massimo raggiungibile;
nessuna conclusione a ICC non raggiungibili. Per ogni stress fattibile usare 100.000 repliche
e verificare/riportare ICC realizzato e tutte le correlazioni di coppia. Nella review controllare
indipendentemente la calibrazione analitica della miscela.

Per D_i indipendenti, con medie mu_i e discordanza d_i:
`Var(sum_i D_i)=sum_i(d_i−mu_i²)≤N*(d_bar−mu_bar²)`;
il divario è `sum_i(mu_i−mu_bar)²`. Il confronto con le probabilità medie non prova il
livello finito di Tango con MLE vincolata. Con correlazione si aggiungono
`2*sum_{i<k} Cov(D_i,D_k)`: né questa argomentazione né Hoeffding N=64 garantiscono il livello.

**Procedure da valutare:**

- Per H3 al bordo −0,125: Tango e Hoeffding N=64 con m=0,125, entrambi a nominale 0,05;
  potenza di entrambi nei punti Δ3=0 e +0,05. Solo Tango a ICC=0 determina la scelta A/B.
- Per H1 e H2: Hoeffding N=64 al bordo della nulla Δ=0, usando gli scenari Δ=0 della
  griglia come esperimenti separati sui contrasti medi di cluster in [−1,1]. Per rappresentare
  P1, le sette righe ricevente di ogni run prendono lo stesso D sintetico: dipendenza
  intra-run perfetta, esplicitamente uno stress limitato, non modello completo del compito.
  H1/H2 hanno qui la stessa distribuzione marginale e soglia 0,305968…; riportare la
  coincidenza senza contare due simulazioni indipendenti o rivendicare verifica FWER congiunta.

Per ciascuna procedura/famiglia di matrici riportare phat, MCSE e CI ad ogni ICC, il massimo
ICC **testato** fino al quale tutti i punti applicabili della sequenza 0→rho restano ≤0,055,
e ogni eventuale comportamento non monotono. Riportare anche il peggiore scenario per ICC.
Non interpolare una soglia continua; distinguere assenza di robustezza a ICC=0 da stress
non fattibile. I risultati ICC>0 entrano nei threats: non selezionano la procedura e non
modificano il protocollo dopo i dati reali. Non stimano la dipendenza residua del servizio.

## 4. Riproducibilità e review

Seed principale sintetico **20260917**, namespace `studio2-fase03-h3-synthetic-q2-v1`.
Generatore `numpy.random.Generator(PCG64(SeedSequence([20260917, scenario_index])))`;
scenario_index zero-based nell’ordine cartesiano degli assi di §2, ultimo asse più rapido.
Ogni scenario ha stream separato. Congelare prima dell’esecuzione versione Python/numpy,
commit/SHA dello script, manifest dei 1.620 scenari target con fattibilità esplicita e consumo RNG interno (anche ordine delle
estrazioni e batch size), per consentire replay indipendente. Nessun riavvio con altro seed
per superare il criterio; crash tecnici si riprendono dallo stesso stream/stato autenticato.

Output per scenario: parametri/matrice delle probabilità, N, seed/index, repliche valide,
errori numerici, rifiuti, livello/potenza, MCSE, CI, correlazioni realizzate, conteggi degeneri,
statistiche di Tango e decisione PASS/FAIL per gli scenari al bordo. Nessuna replica numericamente
problematica viene scartata dal denominatore: errore non risolto → verifica incompleta/STOP.
Riepilogo del massimo phat al bordo con relativo scenario; output raw sintetici sufficienti
al replay o somme statistiche e generatore integralmente riproducibili; manifest/hash di tutto.

La review indipendente controlla marginali, Δ3, dipendenza, formula di Tango, casi degeneri,
contabilità delle repliche e regola di decisione, riproduce almeno gli estremi e verifica
l’intera tabella. Il calcolo del livello locale H3 non simula il FWER congiunto H1→H2→H3.
Alfa 0,025 e confronti di robustezza sono descrittivi; non si usano per recuperare un FAIL
di Tango a ICC=0. Hoeffding resta anche la procedura di fallback già decisa.

## 5. Regola di uscita vincolante, decisa prima del test reale

- Tutti i 108 punti al bordo a ICC=0 con phat≤0,055, implementazione verificata e review OK:
  mantenere **Tango** per H3. Il livello e il FWER completo restano **approssimati**, non
  «garantiti» dalla verifica finita.
- Anche un punto **al bordo a ICC=0** con phat>0,055: esito negativo, H3 passa all’**opzione B Hoeffding** già
  scelta dall’autore come fallback. Nessuna nuova selezione dopo le predizioni di test.
  Soglia a alpha=0,05: `Dbar3 + 0,125 ≥ sqrt(2*ln(20)/64)`, ossia Dbar3≥0,180968…;
  a alpha=0,025: Dbar3≥0,214525…. Margine e gerarchia non cambiano.
- Verifica incompleta o bug non risolto: **PENDING**, non un PASS né un fallimento statistico.
  S6/S10/S11 restano PENDING fino a esito e review, e recepimento del ramo risultante.

**Limite del fallback:** anche Hoeffding a N=64 richiede l’indipendenza delle coppie/run,
come addendum §1. Non è una cura automatica per dipendenza reale fra run. Un superamento di 0,055 negli
scenari correlati è un risultato descrittivo e **non** attiva fallback. Prima
di rivendicare la sua garanzia nel paper deve restare sostenibile l’assunzione di indipendenza
nel disegno reale. Se non lo è, la validità inferenziale resta aperta e il freeze non può
essere dichiarato scientificamente chiuso. Non sostituire autonomamente N=8 né cambiare m.

Motivazione dell’autore: usare B come prima scelta richiederebbe un miglioramento osservato
circa +18 punti per una conclusione di non inferiorità, rendendo H3 praticamente non
rifiutabile vicino a Δ3=0; non è un’impossibilità matematica per ogni alternativa. La verifica
serve a conservare Tango solo entro la tolleranza pre-specificata, con fallback deciso ora.
