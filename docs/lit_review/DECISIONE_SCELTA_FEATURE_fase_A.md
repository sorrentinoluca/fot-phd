# Decisione: scelta dei descrittori di Fase A

**Data**: 2026-09-11 / 2026-09-12 · **Stato**: decisione presa; verifica prospettica approvata e **non congelata**
**Oggetto**: se conservare o sostituire i quattro descrittori calibrati di Fase A (`shift_sigma`, `slope_sigma_h`, `residual_std_ratio`, `diff_std_ratio`) più la derivata `rapid`
**Esito**: **si conservano.** La giustificazione è di progetto, non di criterio; l'utilità diagnostica è un'ipotesi da verificare, non un risultato.

> **Come leggere questo file.** È un **registro di decisione** per la review: dice *che cosa è stato deciso, quando, su quale base e che cosa resta aperto*. Non contiene la motivazione bibliografica (in `criteri_scelta_descrittori.md`) né il disegno sperimentale (in `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` §8.12). Se un contenuto compare in due posti, questo file è quello sbagliato: correggere qui.

---

## 1. Stato delle decisioni

| # | Decisione | Stato | Dove |
| --- | --- | --- | --- |
| 1 | **Conservare i quattro descrittori + `rapid`** anziché sostituirli | ✅ decisa 2026-09-11 | `criteri_scelta_descrittori.md` §5.1 · §0.1 del piano autorevole |
| 2 | Giustificazione riformulata come **copertura di quattro aspetti scelti** fra quelli che la pipeline perde — non chiusura completa | ✅ decisa 2026-09-12 | §2.1 qui · §5.1(a) |
| 3 | Ablazione esistente conservata come **evidenza sulla separabilità 1-NN, esplorativa** | ✅ decisa | `analysis/feature_ablation/` · §5.2 |
| 4 | Verifica affidata a un'**ablazione testuale prospettica** (Experiment 5) | ✅ approvata come disegno | §8.12 del piano autorevole |
| 5 | E5-A — statuto del braccio di omissione | ✅ chiusa | §8.12 |
| 6 | E5-B — `rapid` ricalcolata, mai trasportata | ✅ chiusa | §8.12 |
| 7 | Derangement **disgiunto per classe**, seme congelato | ✅ chiusa 2026-09-12 | §8.12 |
| 8 | IDV(13): risultato **esplorativo**, senza run dedicati | ✅ chiusa 2026-09-12 | §8.12 |
| 9 | E5-C1 — **Δ ≥ 0,10** come **soglia di annotazione** di rilevanza pratica sulla tabella descrittiva, non regola di decisione | ✅ chiusa 2026-09-12 | §8.12 |
| 10 | E5-C2 — soglia lunghezza **≤ 5% per caso**; si chiude con **sole lunghezze**, tokenizer e prompt effettivi, sui dati di sviluppo | ⏳ **provvisoria** | §8.12 |
| 11 | E5-C3 — statuto **DESCRITTIVO** (deciso 2026-09-12): tabella degli effetti per famiglia e meccanismo, intervalli esplorativi, **nessun test, nessuna correzione per molteplicità**. Restano da fissare mappa famiglia–meccanismo e regola di aggregazione | ⬜ **aperta** | §8.12 |
| 12 | Congelamento `exp5-protocol-frozen` | ⬜ non raggiunto | §8.12 |

---

## 2. La domanda e il suo esito

La domanda era se la letteratura offrisse un criterio migliore per *scegliere* i descrittori. **Nel corpus esaminato non emerge**, e va enunciato con precisione: non è un'assenza generale. Ricerca 2010–2026, 30 risultati (25 Scopus, 5 arXiv; OpenAlex 503), più lettura integrale di cinque paper del corpus locale. In quel corpus la scelta delle feature non è una decisione documentata: è l'architettura della rete, e dove il contributo per feature viene quantificato è attribuzione post-hoc su modello addestrato — inutilizzabile sotto la disciplina di congelamento della Fase A. Dettaglio e citazioni verbatim in `criteri_scelta_descrittori.md` §§1–3.

Due qualificazioni obbligatorie.

**Un criterio esiste, fuori da questo filone, e non è trasferibile.** catch22 seleziona 22 descrittori da un catalogo di migliaia con criterio dichiarato. Non è trasferibile per due ragioni: opera su serie z-normalizzate ed esclude di proposito le feature sensibili a media e varianza, cioè proprio gli aspetti di livello e dispersione che questo strato deve recuperare; e i suoi criteri di selezione — prestazione, complementarità, interpretabilità, costo, su classificazione numerica — non includono la verbalizzabilità in testo neutro. Criteri attribuiti a Lubba et al. §§2.2–2.6 **come letti dalla prima review**, non verificati in questa sessione. Lubba, Sethi, Knaute, Schultz, Fulcher & Jones (2019), *catch22: CAnonical Time-series CHaracteristics*, Data Mining and Knowledge Discovery 33(6), 1821–1852, doi:10.1007/s10618-019-00647-x — **DOI da verificare prima della submission**.

**Un'alternativa pertinente esiste nel corpus e non è stata adottata.** S2S-FDD porta la catena segnale→testo→diagnosi zero-shot su un processo industriale: non adottata perché centralizzata e su altro banco — **motivazione da approfondire sul testo prima della submission**.

Conseguenza: non essendoci un criterio migliore *e trasferibile*, **sostituire i descrittori sarebbe stato un cambio senza base**. Si conservano, e si sposta l'onere della prova dalla *selezione* alla *verifica dell'utilità*.

---

## 2.1 La motivazione di progetto, enunciata con precisione

I quattro descrittori **coprono quattro aspetti scelti** fra quelli che la nostra pipeline perde. Per ciascuno, l'operazione che lo perde:

| Aspetto | Operazione della pipeline che lo perde | Descrittore |
| --- | --- | --- |
| scostamento di livello dal regime normale | aggregazione in finestre da 5 h e rendering neutro senza valori | `shift_sigma` |
| tendenza interna alla finestra | l'aggregazione sostituisce la finestra con una sintesi e appiattisce l'andamento | `slope_sigma_h` |
| dispersione attorno alla retta locale | la stessa aggregazione; il detrending lineare è ciò che la isola | `residual_std_ratio` |
| dispersione fra campioni consecutivi | l'aggregazione; non ricostruibile dalla precedente, che non distingue ruvidezza a cadenza alta da deviazione lenta dalla retta | `diff_std_ratio` |

**Non è una chiusura.** I quattro descrittori coprono quattro aspetti scelti del segnale, **senza conservarne integralmente l'informazione**: non rappresentano esplicitamente le correlazioni temporali fra sensori, né consentono di ricostruire l'andamento completo e i valori campione per campione. Va detto così e non come «perde la struttura fra sensori»: alcuni pattern congiunti possono restare leggibili nelle descrizioni dei singoli sensori. «Copertura di quattro aspetti scelti» è la formulazione corretta; «chiusura sui canali di perdita» sovra-afferma e va evitata nel paper.

**Non è equivalenza metodologica con Pappa et al.** Da lì viene la *forma* dell'argomento e il precedente che regge in revisione, non una validazione del nostro contenuto. I setting differiscono su tre assi: dominio HAR e non diagnosi industriale; modello messo a punto con fine-tuning e non LLM congelato interrogato a prompt; e la perturbazione di Pappa §6.3 conserva la lunghezza della sequenza simbolica, mentre il nostro derangement conserva il multinsieme dell'evidenza primaria entro S_F **senza garantire la conservazione della lunghezza dei prompt**, verificata tramite E5-C2.

---

## 3. Cronologia delle correzioni — la parte che la review deve guardare

Il percorso ha prodotto più correzioni che conferme. Sono elencate perché una review che non le vede rischia di riaprire questioni già chiuse, o di fidarsi di formulazioni che sono state ritirate.

### 3.1 Errori dell'assistente, corretti dall'autore

| # | Affermazione errata | Correzione |
| --- | --- | --- |
| 1 | I 30 risultati caratterizzati come «scelta feature = discesa del gradiente» | **Inferenza dai titoli**: Scopus `view=STANDARD` non restituisce abstract. Solo i 5 arXiv avevano l'abstract; nessuno dei 30 letto in full text |
| 2 | `catch22`/`tsfresh`/SPC raccomandati come letteratura d'appoggio | **Non venivano da alcuna ricerca**, ma dalla memoria del modello. Nel corpus locale `tsfresh` compare 3 volte in modo incidentale; `catch22` e `hctsa` mai |
| 3 | L'ablazione definita prima «refutazione», poi «artefatto» | Entrambe sbagliate nello stesso modo: trattavano un endpoint come verdetto. È **valida sulla separabilità 1-NN**, che non è la domanda |
| 4 | `residual`/`diff` descritte come «bassa e alta frequenza» | Non sono risolte in banda; il freeze dichiara «No FFT, wavelet…». Sono **due dispersioni che differiscono per ciò che rimuovono prima di misurare** |
| 5 | FaultExplainer usato come difesa del nostro set | Dimostra che l'evidenza PCA povera **limita** F10 e F13, non che i nostri descrittori **colmino** il vuoto. È motivazione di un'ipotesi. Precisazioni verificate sul testo il 2026-09-12: l'evidenza sono **sei variabili scelte per contributo al T² della PCA**, senza alcun confronto fra descrittori; **F10 fallisce in entrambe le condizioni**; **F13 è corretto in top-3 solo con il catalogo di 15 cause** e fallisce senza; esistono **conteggi top-3** (7/11 e 9/11 con catalogo, 8/11 entrambi senza), quindi la valutazione non è solo qualitativa. Alias accettati come corretti; denominatore = soli 11 fault rilevati dalla PCA |
| 6 | Pappa citato come prova di necessità | Fornisce la **forma** dell'argomento e il precedente che regge in Q1, non il contenuto |
| 7 | «Le finestre non sono indipendenti» come causa di invalidità conformal | Il criterio è la **scambiabilità**, non l'indipendenza. Il cambio della funzione di score basta da solo |
| 8 | Nota che difendeva il test binomiale pilota come «conservativo» | Il documento di decisione lo aveva **già ritirato**; una soglia più severa non corregge la dipendenza |
| 9 | Le tre voci di E5-C dichiarate tutte dipendenti da D1/D2 | Solo E5-C3 lo è. C1 e C2 erano lavorabili subito |
| 10 | E5-C2 segnata `✅ chiusa` mentre il 5% poteva ancora cambiare | Marcata `⏳ provvisoria` |

### 3.2 Vincoli emersi dalla verifica, non previsti all'inizio

- **IDV(13) è l'unico fault documentato del meccanismo slow drift.** La copertura a due fault per meccanismo è insoddisfacibile proprio dove serve a `slope_sigma_h`, il descrittore con meno evidenza a favore.
- **Circa 17 dei 30 risultati della ricerca erano già nel corpus locale** in full text. `papers/` contiene 52 file (~483.000 parole), non i 15 che un listato troncato aveva mostrato.
- **La regola del 5% è a scatto singolo** e può declassare un'intera famiglia: richiede una verifica di fattibilità prima del freeze.

---

## 4. Che cosa è stabilito e che cosa no

| Affermazione | Stato |
| --- | --- |
| Nel corpus esaminato non emerge un criterio di selezione applicabile a priori | **Stabilito** (per questo corpus; catch22 esiste fuori, e la sua trasferibilità a questo specifico strato testuale non è dimostrata — §2) |
| La *forma* «copertura degli aspetti persi» è un argomento pubblicabile | **Stabilito** (Pappa, ESWA) — la forma, non il contenuto né l'equivalenza di setting |
| Un'evidenza PCA povera limita la diagnosi su F10 (entrambe le condizioni) e su F13 (senza catalogo; con catalogo è corretto in top-3) | **Stabilito** (FaultExplainer, Tab. 1–2) |
| I nostri quattro descrittori colmano quel vuoto | **Ipotesi** — è ciò che E5 verifica |
| Rimuovere l'evidenza residual è associato al collasso del margine di F8/B2 verso F1 — `drop_residual_only` 1-NN 0,960 e margine −0,01503; `drop_residual` coerente 1-NN 1,000 e margine −0,01150 | **Indizio**, non necessità individuale (`analysis/feature_ablation/`) |
| `slope_sigma_h` contribuisce | **Non sostenuta** allo stato attuale |

Nota sull'ultima riga: rimuovere `slope_sigma_h` **alza** il margine di F13, da 0,03300 a 0,03922. È il dato più scomodo del fascicolo e va lasciato visibile.

> **Pre-impegno, registrato prima dell'esecuzione.** Un risultato nullo o sfavorevole di E5 su un qualunque descrittore **non ne comporta la rimozione dal set**, né una nuova valutazione dello stesso descrittore sullo stesso test. La permanenza nel set poggia sulla motivazione di progetto di §2.1; E5 misura l'utilità diagnostica, non decide la composizione del set. Senza questo impegno dichiarato in anticipo, un esito sfavorevole seguito da una rivalutazione sarebbe selezione sull'esito.

---

## 5. Che cosa resta aperto

1. **E5-C2** — conferma o revisione del 5%, **solo** sulla base di misure di lunghezza con tokenizer e prompt effettivi sui dati di sviluppo. Mai su risultati diagnostici. Da registrare prima del freeze.
2. **E5-C3** — statuto **descrittivo** (deciso 2026-09-12): tabella degli effetti per famiglia e meccanismo con intervalli riportati come esplorativi, nessun test di ipotesi, nessuna correzione per molteplicità. Restano da fissare mappa famiglia–meccanismo e regola di aggregazione (per fault, run, ricevente). Dipende da D1, D2, C1, C2.
3. **`exp5-protocol-frozen`** — nessun run va aperto prima.

Ordine: verifica di fattibilità di E5-C2 → chiusura di E5-C2 → D1 e D2 → E5-C3 → freeze.

---

## 6. Dove vive cosa

| Contenuto | File |
| --- | --- |
| Motivazione bibliografica, schede dei 5 paper, stato epistemico | `docs/lit_review/criteri_scelta_descrittori.md` |
| Ablazione eseguita: script, risultati, report | `analysis/feature_ablation/` |
| Disegno di Experiment 5 (**autorevole**) | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` §8.12 |
| Tracciamento fra le decisioni | idem, §0.1 |
| Rimando, senza duplicazione del disegno | `docs/paper/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md` §7 |
| Calibrazione delle soglie (questione separata, toccata solo per terminologia) | `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md` |

Non toccati: §14 del walkthrough, `README.md`, `DOCUMENTATION_INDEX.md`, tutti gli artefatti congelati.

---

## 7. Su che cosa concentrare la review

In ordine di esposizione, dal punto più attaccabile al meno.

1. **`slope_sigma_h`.** Nessuna evidenza a favore, e il meccanismo che dovrebbe sostenerlo ha un solo fault con 6–8 unità indipendenti. Il risultato resterà descrittivo. Domanda onesta da porsi: se resta descrittivo e non mostra nulla, che cosa si fa del descrittore?
2. **La fattibilità del 5%.** Se la verifica mostra che non è raggiungibile, il braccio principale nasce declassato. Va misurato prima di congelare, non dopo.
3. **L'asimmetria del braccio di omissione.** Rimuove una famiglia primaria *più* il canale derivato `rapid`, mentre la permutazione ne altera una sola. I due bracci non sono simmetrici e i loro risultati non sono direttamente confrontabili.
4. **La forza dell'argomento di progetto.** «Chiusura sui canali di perdita» è una forma valida e pubblicata, ma resta un argomento di design: non dimostra che i canali siano quattro né che siano quelli giusti.
5. **La generalizzabilità.** Quattro meccanismi su 28 guasti, un solo dataset, un solo verbalizzatore.
