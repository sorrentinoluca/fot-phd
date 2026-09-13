OK

# Appendice 01 alla verifica indipendente D1 — anteriorità dei parametri di sorteggio

Data: **2026-09-13**. Verificatore: **Codex**; modello richiesto per il sottoagente dal tool:
**gpt-5.6-sol**; autoidentificazione disponibile nel contesto: **GPT-5**. Agente/finestra separata
`/root/verifica_criteri`.

Questa appendice è una verifica **nuova ed ex post** del punto specifico richiesto. Colma
un'omissione esplicita di `VERIFICA_CATALOGO_D1.md`: quel verbale verificava impronte, ricalcolo e
risultato, ma non attestava frase per frase che tutti i parametri del sorteggio fossero già scritti
nel registro al tag della revisione 1. La presente attestazione non viene attribuita
retroattivamente al primo controllo.

Non sono stati eseguiti replay, enumerazioni, digest D1 o test; non sono stati aperti risultati
per-fault, sonde o predizioni e non è stata svolta alcuna inferenza sperimentale.

## 1. Identità del registro vincolato

Il tag `studio2-fase03-criteri-selezione-frozen-001` è un **tag annotato**, oggetto
`e2a7c49bbe75d53beb87095c8b77a66570f09c08`, e risolve al commit
`9faecaf7337e5864b7a3ad44cadb8971853dd260`. Il suo messaggio limita il freeze ai criteri e
dichiara D1 non ancora eseguita.

Da quel tag, il file
`docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md` misura **11.339 byte** e ha
SHA-256 `d58a7606d69a560a626da44833c065ddbf1aa395ae8b2e523262daf8622231c7`.
`CRITERIA_FREEZE.json`, letto dallo stesso tag, misura **2.284 byte**, ha SHA-256
`ecae57172d6a83d8b0943f5a9f47b49a3966b96e2fb47f807a9ff61449755c9b` e registra per quel
documento esattamente percorso, ruolo `normative_criteria_revision`, 11.339 byte e la medesima
impronta. Il blob del registro al `source_commit`
`9d0e1911afd6c244f748f05f62934590f5314794` è byte-identico a quello incluso nel tag.

Il manifest non ripete seed, namespace o algoritmo. Ne vincola invece il documento normativo per
percorso, dimensione, impronta e commit sorgente; i parametri prescritti nel §5 di quel preciso
blob sono quindi quelli attestati dal freeze.

## 2. Parametri già prescritti nel §5 al tag della revisione 1

La lettura diretta delle righe 112–133 del registro al tag dà evidenza distinta per ogni elemento:

| Elemento richiesto | Evidenza già presente nel registro congelato |
| --- | --- |
| Ordine di enumerazione | Riga 116: combinazioni **crescenti** di quattro ID fra gli undici non di continuità. |
| Ordine degli ammissibili | Righe 117–118: aggiunta la continuità e applicato il filtro §4, le quadruple ammissibili sono ordinate lessicograficamente **come tuple di interi**; nessun peso deriva da risultati o FDR. |
| Metodo | Riga 119: selezione uniforme dell'indice mediante **rejection sampling deterministico su SHA-256**. |
| Seed | Riga 120: seed ASCII **`20260913`**. |
| Namespace | Riga 121: namespace ASCII **`studio2-fase03-D1-v1`**. |
| Messaggio e codifica | Righe 121–123: per `c=0,1,…`, messaggio `studio2-fase03-D1-v1|20260913|c`, `c` decimale senza zeri iniziali, hash dei byte **UTF-8** mediante **SHA-256**. |
| Interpretazione del digest | Riga 123: i 32 byte sono interpretati come intero unsigned **big-endian** `x`. |
| Soglia e rifiuto | Righe 123–125: `L = 2^256 − (2^256 mod N)`; si accetta il primo `x < L`, rifiutando implicitamente ogni precedente `x ≥ L`; se `N=0` si arresta prima di qualsiasi hash. |
| Contatore e indice | Righe 121–124: il contatore parte da zero e cresce di uno; l'indice zero-based è `x mod N`. |
| Primitive vietate | Riga 125: divieto di usare `hash()` del linguaggio. |
| Traccia obbligatoria | Righe 126–127: registrazione di lista ordinata, `N`, seed, contatore accettato, digest, indice, catalogo, conteggi, commit e hash dei criteri. |
| Nessun nuovo seed o rilancio | Righe 127–128: divieto esplicito di secondo seed, sorteggio di prova o rilancio per cambiare catalogo; un replay deve riprodurre lo stesso esito. |

Questi elementi erano dunque prescritti nel blob congelato; non sono parametri ricostruiti dal log
D1 o aggiunti dopo aver conosciuto l'esito.

## 3. Anteriorità registrata nella storia Git

Il tag annotato del catalogo `studio2-fase03-catalogo-D1-frozen-001`, oggetto
`b6828afc3062e1e6371376638c42eab529635e32`, risolve al commit
`ab43f0b20f45cdb475c0caf52c6f7afcbae50891`. Il controllo
`git merge-base --is-ancestor` termina con codice 0 per il commit dei criteri `9faecaf…` rispetto
al commit D1 `ab43f0b…`: il commit contenente il registro congelato è un antenato del commit che
documenta il catalogo D1. Le date annotate registrate sono 2026-09-13 10:35:51 +02:00 per il tag
dei criteri e 2026-09-13 11:22:15 +02:00 per il tag D1; l'evidenza più forte nel repository resta
la relazione di contenuto e antenato, insieme al messaggio del primo tag che dichiara D1 non
eseguita.

Comandi riproducibili, tutti di sola lettura:

```bash
git cat-file -t studio2-fase03-criteri-selezione-frozen-001
git rev-parse studio2-fase03-criteri-selezione-frozen-001
git rev-parse 'studio2-fase03-criteri-selezione-frozen-001^{}'
git for-each-ref --format='%(contents)' refs/tags/studio2-fase03-criteri-selezione-frozen-001
git show 'studio2-fase03-criteri-selezione-frozen-001:docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md' | sed -n '112,133p'
git show 'studio2-fase03-criteri-selezione-frozen-001:docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md' | shasum -a 256
git show 'studio2-fase03-criteri-selezione-frozen-001:docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md' | wc -c
git show 'studio2-fase03-criteri-selezione-frozen-001:studio2/fase03/selection/CRITERIA_FREEZE.json'
git cat-file -t studio2-fase03-catalogo-D1-frozen-001
git rev-parse 'studio2-fase03-catalogo-D1-frozen-001^{}'
git merge-base --is-ancestor 9faecaf7337e5864b7a3ad44cadb8971853dd260 ab43f0b20f45cdb475c0caf52c6f7afcbae50891
```

L'ultimo comando deve terminare con codice **0**. I comandi non calcolano il digest del sorteggio:
calcolano soltanto, dove indicato, l'impronta del documento normativo già congelato.

## 4. Verdetto e limite probatorio

**OK — seed, namespace, ordinamento, codifica e SHA-256, interpretazione big-endian, contatore,
soglia `L`, rejection sampling, riduzione modulo `N` e divieto di nuovi seed o rilanci erano già
prescritti nel registro vincolato dal tag della revisione 1, antecedente nella storia Git al commit
D1.** Il manifest della revisione 1 non deve duplicare tali parametri: identifica senza ambiguità
il blob normativo che li contiene.

Il repository prova l'anteriorità **registrata** del testo e la sua discendenza fino al commit D1.
Non prova l'assenza di calcoli, consultazioni o conoscenze private anteriori alla formalizzazione;
le date Git non sono da sole un'autorità temporale esterna. Questa appendice non modifica né
estende il risultato scientifico o il catalogo e non sostituisce i limiti già dichiarati nel
verbale principale.
