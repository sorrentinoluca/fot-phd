# Proposta non vincolante — fault OOD (§8.6, S13) e coppie confondibili (D11)

Data: **2026-09-13**. Profilo: **decisionale**. Stato: **proposta da confermare in un passaggio
separato**. Non fa parte del congelamento D1, non è registrata in `CATALOG_FREEZE.json` e non
chiude la decisione 3 né la decisione 4 di §0.1 del piano. Fonte delle proprietà: la sola tabella 8
di Downs & Vogel (1993) come trascritta nel registro dei criteri §2, più le indicazioni del piano
§8.3, §8.6 e D11. Nessun risultato per-fault dei nostri esperimenti è stato consultato.

Catalogo D1 di riferimento: **F1, F2, F3, F8, F10, F13, F14, F15**
(3 step / 2 random / 1 drift / 2 sticking; H = {F3, F15}).

## 1. Perché è una proposta e non una decisione

Il piano definisce i due requisiti solo per esempi e per esclusione: «meccanicamente distinto da
tutti gli 8» (F2 non lo è rispetto a F1, entrambi step sul flusso 4) e «fuori dal gruppo compensato
dal controllo» (H). Il registro §2 dichiara espressamente che la chiave di identità **non**
definisce né la distinzione OOD né le coppie confondibili. Applicare i requisiti al catalogo
richiede quindi di fissare **che cosa conta come "meccanicamente distinto"**, ed è una decisione di
disegno che spetta all'autore. Qui si mostrano le conseguenze delle letture possibili.

Un fatto strutturale condiziona tutto: il catalogo D1 copre **tutti e quattro i meccanismi** della
tabella 8. Se «meccanicamente distinto» significasse «meccanismo di tipo diverso», nessun fault di
IDV(1)–IDV(15) sarebbe ammissibile e bisognerebbe uscire dall'universo del registro (IDV(16)–(20)
hanno variabile e tipo non specificati; IDV(21) non appartiene alla tabella). La lettura coerente
con l'esempio F1/F2 del piano è invece: **variabile perturbata e apparato/flusso coinvolto**
diversi da quelli di ogni fault in catalogo.

## 2. Fault OOD: candidati fuori catalogo

Fuori catalogo in IDV(1)–IDV(15): F4, F5, F6, F7, F9, F11, F12. F9 è escluso dal secondo vincolo
di §8.6 (gruppo H). Per gli altri, che cosa condividono con il catalogo:

| Candidato | Variabile (tabella 8) | Meccanismo | Condivide con il catalogo | Lettura |
| ---: | --- | --- | --- | --- |
| **F6** | perdita alimentazione A, flusso 1 | step | solo il tipo di meccanismo (step, con F1/F2/F3); flusso 1 non compare in catalogo; nessuna variabile o apparato in comune | **distinto** sotto la lettura variabile/apparato |
| F7 | pressione/disponibilità C, flusso 4 | step | flusso 4 con F1, F2, F8, F10; stesso tipo di F1/F2 | non distinto nel senso dell'esempio F1/F2 |
| F4 | temperatura ingresso acqua reattore | step | circuito di raffreddamento del reattore con F14 (valvola acqua reattore) | distinto per variabile, **non** per apparato |
| F11 | temperatura ingresso acqua reattore | random variation | circuito di raffreddamento del reattore con F14 | idem |
| F5 | temperatura ingresso acqua condensatore | step | circuito di raffreddamento del condensatore con F15 | idem |
| F12 | temperatura ingresso acqua condensatore | random variation | circuito di raffreddamento del condensatore con F15 | idem |

**Proposta.** F6 è l'unico candidato distinto da tutti gli 8 sia per variabile sia per apparato.
Per il secondo fault non esiste un candidato altrettanto pulito dentro IDV(1)–IDV(15): tutti gli
altri condividono o il flusso 4 (F7) o un circuito di raffreddamento con una valvola in catalogo
(F4/F11 con F14, F5/F12 con F15). Le opzioni da sottoporre all'autore sono:

- **Opzione a — F6 + uno fra F4/F5/F11/F12**, dichiarando che la distinzione richiesta è per
  variabile perturbata e non per apparato, e registrando la vicinanza alla valvola corrispondente
  come limite; fra questi, F4 è l'unico con rilevabilità già documentata nel pacchetto congelato
  (PHM 2023: DAE 100 %, T² 18 %, SPE 100 %; dipendente dal metodo).
- **Opzione b — F6 + F7**, dichiarando che la distinzione riguarda la variabile fisica (pressione
  di testata, non composizione né temperatura) e accettando la condivisione del flusso 4, che è
  proprio il caso che il piano usa come controesempio.
- **Opzione c — F6 + un fault fuori da IDV(1)–IDV(15)**, che richiederebbe di estendere
  l'universo e di documentare variabile e meccanismo da una fonte diversa dalla tabella 8.

Il secondo vincolo di §8.6 chiede anche «rilevabilità documentata». Nel pacchetto congelato i
soli valori esterni riverificati sono quelli di F3, F9, F15 e F4; per F6, F5, F7, F11, F12 non è
stato verificato alcun numero in questa sotto-fase. Qualunque opzione va quindi accompagnata da
una citazione esterna verificata (§12.4: solo fonti con numeri specifici) prima di essere fissata.

## 3. Coppie confondibili per D11 (4 fault, §8.3: 4 × 3 × 7 = 84 chiamate)

Criterio del piano: coppie che condividono **variabile perturbata o meccanismo** secondo Downs &
Vogel, dichiarate prima delle confusioni del test. Nel catalogo nessuna coppia condivide la chiave
di identità esatta (vincolo §4.3). Le condivisioni residue, in ordine di quanto è condiviso:

| Coppia | Condivide | Note |
| --- | --- | --- |
| **F1 / F2** | flusso 4, meccanismo step, natura compositiva dell'intervento (rapporto A/C vs composizione B) | è l'esempio esplicito del piano §8.6 di confusione «ragionevole» |
| **F14 / F15** | meccanismo sticking valve, stesso tipo di apparato (valvola acqua di raffreddamento), reattore vs condensatore | entrambi soggetti alla nota Downs & Vogel su perturbazione congiunta e 24–48 h |
| F8 / F10 | flusso 4, meccanismo random variation | composizione vs temperatura |
| F1 / F8 | flusso 4, natura compositiva | step vs random: meccanismo diverso |
| F2 / F8 | flusso 4, composizione (B vs A/B/C) | step vs random |
| F3 / F1, F3 / F2 | solo il meccanismo step | flussi diversi (2 vs 4) |
| F13 | nessuna condivisione strutturale con altri | il drift resta senza coppia |

**Proposta.** Le due coppie con il maggior numero di attributi condivisi sono **{F1, F2}** e
**{F14, F15}**: quattro fault distinti, come richiede il conteggio di §8.3. Alternativa con la
stessa logica ma un attributo condiviso in meno: {F1, F2} + {F8, F10}, che concentra l'ablation
sul flusso 4 e lascia fuori le valvole. La scelta fra le due dipende da che cosa si vuole che
l'ablation local-first metta alla prova (confusione compositiva sullo stesso flusso, oppure
confusione fra apparati omologhi), e va presa dall'autore prima di ogni run.

## 4. Che cosa serve per chiudere

1. Una definizione scritta di «meccanicamente distinto» (variabile? apparato? tipo di meccanismo?)
   nel piano §8.6 o in un registro di `docs/lit_review/`.
2. Una fonte esterna con numeri verificati per la rilevabilità del secondo fault OOD.
3. La scelta delle due coppie D11 con la motivazione strutturale, registrata prima dei run.

Fino ad allora la decisione 3 e la decisione 4 di §0.1 restano **aperte**; questa nota serve a
renderle lavorabili, non a chiuderle.
