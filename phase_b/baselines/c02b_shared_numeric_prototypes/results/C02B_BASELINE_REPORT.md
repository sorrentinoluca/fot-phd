# C02b — baseline numerica con prototipi condivisi, ispirata a FedProto

## Esito

La baseline numerica equa è stata completata sullo stesso compito di FoT. Lo stato di C02b passa da **Aperta** a **Mitigata**: esiste ora un confronto esterno diretto, ma non una suite sufficiente di algoritmi federati originali per dichiarare la critica risolta sperimentalmente.

## Protocollo in breve

Ogni classe è riassunta dalla media di cinque vettori development a 697 componenti, estratti prima della verbalizzazione. Ogni agente conserva i prototipi Normal e del proprio fault e riceve i tre prototipi fault dei peer. La predizione è il prototipo a minima distanza L1 media. Il classificatore usa soltanto pseudolabel opache; la verità PBH viene unita dopo avere scritto le predizioni non valutate.

## Metriche

| Braccio | Complessiva | Local-seen | Local-unseen | Normal |
|---|---:|---:|---:|---:|
| `shared_prototypes` | 60/60 (100.0%) | 12/12 (100.0%) | 36/36 (100.0%) | 12/12 (100.0%) |
| `local_only` | 24/60 (40.0%) | 12/12 (100.0%) | 0/36 (0.0%) | 12/12 (100.0%) |
| `centralized_reference` | 60/60 (100.0%) | 12/12 (100.0%) | 36/36 (100.0%) | 12/12 (100.0%) |

Per la metrica primaria, l'intervallo bootstrap al 95% è [100.0%, 100.0%]. Il bootstrap ricampiona 12 casi fisici, stratificati per fault; le tre viste local-unseen dello stesso caso restano unite.

## Confronto diretto con A, B ed E

| Metodo | Accuratezza local-unseen | Differenza baseline numerica − metodo |
|---|---:|---:|
| Prototipi condivisi | 100.0% | — |
| FoT A | 0.0% | +100.0% |
| FoT B | 86.1% | +13.9% |
| FoT E | 8.3% | +91.7% |

Le differenze sono descrittive e appaiate sullo stesso held-out, ma qui non sono presentate come test di superiorità. A è un information floor senza conoscenza peer; E corrompe le associazioni testuali; B è il confronto FoT pertinente. Il riferimento centralizzato coincide matematicamente con il braccio condiviso perché entrambi usano gli stessi cinque centroidi; la differenza è dove vengono costruiti e trasferiti.

## Risultato per fault e agente — braccio condiviso

| Agente | Fault/pseudolabel | Ambito | Risultato |
|---|---|---|---:|
| `agent_1` | `CLS-ZOGAA` | local_seen | 3/3 (100.0%) |
| `agent_1` | `CLS-OJNSG` | local_unseen | 3/3 (100.0%) |
| `agent_1` | `CLS-R463B` | local_unseen | 3/3 (100.0%) |
| `agent_1` | `CLS-Z3ISU` | local_unseen | 3/3 (100.0%) |
| `agent_2` | `CLS-ZOGAA` | local_unseen | 3/3 (100.0%) |
| `agent_2` | `CLS-OJNSG` | local_seen | 3/3 (100.0%) |
| `agent_2` | `CLS-R463B` | local_unseen | 3/3 (100.0%) |
| `agent_2` | `CLS-Z3ISU` | local_unseen | 3/3 (100.0%) |
| `agent_3` | `CLS-ZOGAA` | local_unseen | 3/3 (100.0%) |
| `agent_3` | `CLS-OJNSG` | local_unseen | 3/3 (100.0%) |
| `agent_3` | `CLS-R463B` | local_seen | 3/3 (100.0%) |
| `agent_3` | `CLS-Z3ISU` | local_unseen | 3/3 (100.0%) |
| `agent_4` | `CLS-ZOGAA` | local_unseen | 3/3 (100.0%) |
| `agent_4` | `CLS-OJNSG` | local_unseen | 3/3 (100.0%) |
| `agent_4` | `CLS-R463B` | local_unseen | 3/3 (100.0%) |
| `agent_4` | `CLS-Z3ISU` | local_seen | 3/3 (100.0%) |

## Matrice di confusione — braccio condiviso

Le righe sono le pseudolabel vere; le colonne sono le predizioni. Ogni fault compare 12 volte perché i tre casi fisici sono valutati da quattro agenti; questa duplicazione non viene trattata come indipendenza statistica.

| Vera \ Predetta | CLS-ZOGAA | CLS-OJNSG | CLS-R463B | CLS-Z3ISU | Normal | Astensione |
|---|---:|---:|---:|---:|---:|---:|
| `CLS-ZOGAA` | 12 | 0 | 0 | 0 | 0 | 0 |
| `CLS-OJNSG` | 0 | 12 | 0 | 0 | 0 | 0 |
| `CLS-R463B` | 0 | 0 | 12 | 0 | 0 | 0 |
| `CLS-Z3ISU` | 0 | 0 | 0 | 12 | 0 | 0 |
| `Normal` | 0 | 0 | 0 | 0 | 12 | 0 |

## Comunicazione

Ogni agente riceve 3 prototipi, 2091 scalari e 16755 byte effettivi. Nel sistema sono trasmesse 12 copie di prototipo, 8364 scalari e 67020 byte. I byte includono pseudolabel e float64 nel formato congelato, ma non il framing di rete.

## Limiti

- È nearest-prototype su feature frozen, non l'algoritmo FedProto originale.
- Il vettore a 697 componenti eredita soglie e scelte del verbalizzatore V2; non misura il vantaggio del testo rispetto a tutte le possibili feature numeriche.
- Cinque casi development per classe e tre casi held-out per fault danno incertezza ampia; le 36 viste agente-caso non sono indipendenti.
- Il riferimento centralizzato non è un upper bound garantito e non è un confronto federato separato: è un controllo di equivalenza dei centroidi.
- PCA+SVM centralizzata e FedAvg non sono stati eseguiti perché, senza un nuovo protocollo di output class-disjoint, cambierebbero il compito o non renderebbero predicibili le pseudoclassi mai viste localmente.

## Artefatti

Configurazione, freeze, codice, prototipi, predizioni non valutate e valutate, matrici di confusione, dettaglio agente×fault, payload binari, bootstrap e manifest SHA-256 sono nella presente cartella.
