# Related Work

## Dalla federazione parametrica alla conoscenza testuale

Il federated learning canonico coordina l'apprendimento tramite aggregazione di parametri; lavori
successivi hanno spostato l'oggetto condiviso verso logit e prototipi. Questo
studio occupa un'estremità diversa della stessa traiettoria: non aggrega pesi e usa record testuali
ispezionabili come interfaccia fra agenti. La distinzione è architetturale, non implica superiorità
né equivalenza empirica con FedAvg, FedMD o FedProto.
[Fonte bibliografica: FedMD e FedProto, `docs/letteratura.md` §14.1–§14.2; fonte di disegno: piano §9; L `docs/letteratura.md` §14.1–§14.2, McMahan, candidato esterno identificato in `FONTI_DELTA_0315.json`]

Time-FFM combina foundation model e federazione parametrica per il forecasting di serie temporali.
La sua esistenza impedisce di presentare l'accostamento fra federazione, modelli linguistici e serie
temporali come contributo autonomo; qui la domanda è invece la diagnosi con esperienza locale
disgiunta per classe e conoscenza testuale scambiata in contesto.
[Fonte bibliografica: Time-FFM, `docs/letteratura.md` §14.1–§14.2]

## Federazione testuale e apprendimento in contesto

Federation over Text di Yao et al. è il metodo di riferimento: gli agenti trasformano esperienza
locale in insight, che vengono condivisi senza trasmettere traiettorie o gradienti. FoT-TEP ne è un
adattamento a evidenza temporale multivariata e a un compito di diagnosi; non rivendica l'invenzione
di FoT o dello scambio di conoscenza in linguaggio naturale.
[Fonte bibliografica: Yao et al., `docs/letteratura.md` §14.1, §14.2, §14.5]

P042/FICAL usa un compendio in linguaggio naturale in un protocollo one-shot; P041/Fed-ICL coordina
più round di coppie domanda-risposta; P031/FedTextGrad aggrega prompt testuali e documenta il rischio
di perdita di dettaglio nella sintesi. Questi precedenti occupano lo scambio testuale, l'assenza di
parametri trasmessi e l'aggregazione lato server. La scelta peer-to-peer di conservare i record
integri è quindi una decisione di scopo e auditabilità, non una proprietà generale già dimostrata.
[Fonte bibliografica: P042/FICAL, P041/Fed-ICL e P031/FedTextGrad, `docs/letteratura.md` §14.1–§14.2; distinzione: piano §12.6–§12.8]

P030/FERA affronta contributi federati inaffidabili mediante stime di incertezza e pesatura; P001/ACE
descrive *brevity bias* e *context collapse* nella costruzione iterativa del contesto. Il presente
protocollo non introduce confidence weighting e non inferisce che i round aggiuntivi siano inutili:
induce invece un'associazione semanticamente errata e pre-specificata, mantenendo fisso il resto del
record, per misurare la dipendenza dalla correttezza dell'informazione.
[Fonte bibliografica: P030/FERA e P001/ACE, `docs/letteratura.md` §14.1–§14.2; distinzione: piano §12.7–§12.8]

P065/SYNAPSE è il precedente più vicino per artefatti tipizzati e portabilità lato consumer: un
compendio strutturato viene letto da famiglie di modelli diverse. Di conseguenza, né la struttura a
campi né la leggibilità cross-model sono rivendicate qui. Il braccio producer-swap risponde a una
domanda diversa: se una libreria completa, vincolata allo stesso schema e agli stessi cap, cambia
quando cambia il producer.
[Fonte bibliografica: P065/SYNAPSE, `docs/letteratura.md` §14.1–§14.2; distinzione: piano §8.4, §12.9]

## Serie temporali trasformate in testo

TRUCE collega descrizioni a condizioni verificabili; T2SP usa programmi strutturati; CGTime separa
percezione statistica e descrizione; S2S-FDD converte segnali industriali multivariati in descrizioni
per la diagnosi zero-shot. Questi lavori mostrano che l'interfaccia serie-temporale-verso-testo è un
componente noto. Nel presente studio il verbalizzatore è un mezzo deterministico e controllabile; il
contributo valutato è il trasferimento fra agenti e il controllo di specificità, non l'interfaccia.
[Fonte bibliografica: TRUCE, T2SP, CGTime e S2S-FDD, `docs/letteratura.md` §14.1–§14.2, §14.5–§14.6]

Le rappresentazioni simboliche e i confronti fra dati grezzi e descrizioni forniscono ulteriore
contesto, ma non autorizzano ad assumere che più ragionamento o più testo migliori la diagnosi. Zhou
e Yu riportano fragilità degli LLM sulle anomalie temporali; Lee et al. mostrano che una baseline a
regole può superare configurazioni LLM in rilevazione pur fallendo in classificazione. Il protocollo
separa quindi la qualità dell'evidence dal comportamento del reasoner e include baseline numeriche.
[Fonte bibliografica: Pappa et al., Zhou & Yu, Lee et al., `docs/letteratura.md` §14.1–§14.2]

## Diagnosi federata e diagnosi industriale con LLM

FedCKD dimostra che clienti con etichette esclusive non sono un regime inedito; FedMeta-FFD e il
trasferimento semantico zero-shot affrontano nuove categorie mediante meccanismi parametrici o
attributi intermedi. Zhang et al. e Xu et al. applicano metodi federati al Tennessee Eastman Process,
con protocolli diversi dal presente. Sono comparatori di dominio e impediscono di presentare la
baseline FedAvg come unico riferimento federato sul TEP.
[Fonte bibliografica: FedCKD, FedMeta-FFD, Sun et al., Zhang et al. 2026 e Xu et al. 2026, `docs/letteratura.md` §14.1–§14.2; fonte di disegno: piano §9.1]

FaultExplainer combina PCA, variabili deviate e un LLM per produrre ipotesi di causa sul TEP, anche
senza fornire il repertorio delle cause. Le sue misure non sono direttamente confrontabili con
l'accuratezza top-1 qui prevista: accettano alias, valutano una lista di ipotesi e restringono il
denominatore ai fault rilevati dalla PCA. Il confronto sostenibile riguarda quindi la struttura del
compito, non i valori riportati.
[Fonte bibliografica: FaultExplainer, `docs/letteratura.md` §14.1–§14.2, §14.5; qualificazioni: piano §12.5]

EviFDD-Agent collega campi di report a evidence prodotta da tool deterministici e misura la
tracciabilità sul TEP. La sua conformità riguarda il reporter; qui si misura la validità dello schema
lato producer insieme a retry, troncamenti e token. Le due grandezze sono complementari, perciò la
tabella di conformità di questo studio non viene presentata come senza precedenti.
[Fonte bibliografica: EviFDD-Agent, `docs/letteratura.md` §14.1–§14.2; distinzione: piano §8.9–§8.10]

## Privacy e prompt federati

DP-FPL e FedDTPT collocano privacy e prompt learning federato nello spazio dei precedenti; FedDTPT
tratta in particolare prompt discreti e trasferibili per LLM black-box. La loro presenza impedisce
di dedurre una garanzia di privacy dalla sola assenza di scambio dei dati grezzi. FoT-TEP non misura
privacy né implementa secure aggregation: usa questi lavori per delimitare il claim, non come prova
di equivalenza tecnica o protezione.
[Fonte bibliografica: DP-FPL e FedDTPT, `docs/letteratura.md` §14.1; limite: piano §5 G7 e §12.8]

## Posizionamento del contributo

Nel corpus consultato, i singoli componenti sono già presenti: federazione testuale, classi
disgiunte, verbalizzazione, artefatti strutturati e diagnosi LLM. La posizione difendibile è la loro
combinazione in un regime di esperienza temporale multivariata class-disjoint, con accuratezza
misurata sulla classe mai osservata localmente, protezione dell'esperienza locale e controllo fra
conoscenza corretta e associazione semanticamente errata.
[Fonte bibliografica: `docs/letteratura.md` §14.4–§14.6; fonte di claim: piano §12.9]

Il corpus non dimostra l'assenza assoluta di precedenti. La formulazione finale dovrà limitarsi a
dire che, nella ricerca documentata, non è stato identificato un lavoro che combini tutti questi
assi sotto un controllo di specificità pre-specificato. Non si rivendicano efficienza comunicativa,
privacy, generalità cross-model, scalabilità di rete o superiorità rispetto alla condivisione
numerica e alla centralizzazione.
[Fonte bibliografica: `docs/letteratura.md` §14.4–§14.6; limiti: piano §5, §12.7–§12.9]
