# Specifica pre-osservazione — baseline numerica a prototipi 697-D

**Data:** 2026-09-14  
**Base:** `origin/main` a `46c0b62`  
**Stato:** specifica congelabile, scritta senza aprire firme per classe; prototipi e valutazione
reali assenti in attesa di `normal_dev` e dei run di test.

## Oggetto e confini

La baseline riassume ogni classe con la media aritmetica componente per componente delle firme
697-D (41 XMEAS × 17) prodotte dall'estrattore verificato della 03.6. È nearest-prototype su
feature congelate, ispirata al pattern C02B del primo studio; non è FedProto, non apprende una
rappresentazione e non implementa ottimizzazione federata.

Il codice non importa funzioni del primo studio e non ricalcola le firme: legge esclusivamente i
CSV di firma già pubblicati, dopo aver verificato manifest, SHA-256, dimensione, finitezza e range
`[0,1]`. Per le evidence fault il manifest ammesso è quello della release
`studio2-fase03-evidence-v1`, SHA-256
`5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020`, commit 03.6
`2f6dd8d`. Le evidence Normal devono derivare da `normal_dev` con le stesse funzioni, guardie e
impronte 03.6 e conservare la condizione U3/R2.

## Dati di sviluppo e prototipi

Non si selezionano finestre in base al contenuto.

- per ciascuno degli otto fault: tutte le otto finestre post-innesco `[25,65)` di ciascuno dei
  cinque run di sviluppo, quindi 40 firme per prototipo;
- per Normal globale: tutte le otto finestre `[25,65)` dei 40 run `normal_dev`, quindi 320 firme;
- per Normal locale dell'agente: le 40 firme dei suoi cinque run assegnati;
- per fault locale dell'agente: le stesse 40 firme del fault che gli è assegnato.

Le finestre sono osservazioni usate nella media, non repliche indipendenti. Il codice produce due
varianti dallo stesso percorso:

1. `global`: nove prototipi, otto pseudolabel opache più `Normal`;
2. `local`: per ciascun agente due prototipi, `Normal` e la propria pseudolabel fault.

Le classi assenti nella variante locale non sono candidate. **Nessun fallback globale** è
ammesso: la variante locale può soltanto scegliere fra le due classi disponibili o astenersi.
Questa è la controparte numerica della condizione A, non un classificatore open-set addestrato.

`PROTOTYPES.json` contiene solo pseudolabel, `agent_id`, vettori e conteggi; non contiene F-number,
IDV o mapping reale. `PROTOTYPES_MANIFEST.json` registra hash degli input e dell'output, metodo,
conteggi e dipendenza R2. Entrambi nascono soltanto quando le evidence Normal sono disponibili.

## Classificazione congelata

Per firma `x` e prototipo `p_c`, la distanza è la L1 media
`d_c = (1/697) * sum_j |x_j - p_cj|`. Il fattore costante non cambia l'ordinamento e conserva il
pattern C02B. Vince la distanza minima unica. Se due o più distanze differiscono dal minimo di non
più di **`1e-12` in valore assoluto**, l'esito è astensione:
`abstain=true`, `predicted_label=null`.

Non è prevista una soglia di astensione sulla distanza: il piano non la prescrive e introdurla
richiederebbe una decisione pre-specificata distinta prima del test. Non si usa confidence,
normalizzazione appresa sul test o tie-break lessicografico.

## Interfaccia di valutazione evaluator-side

L'input test è composto da un manifest evidence 03.6-compatible e da un indice evaluator-side
con una riga per coppia agente-caso:

`physical_case_id,evidence_id,agent_id,true_pseudolabel`.

La verità resta separata dalla costruzione della predizione. Il codice scrive prima le righe
`predictions_unscored.csv`, poi unisce la pseudolabel vera e scrive `predictions.csv`. Nessun
F-number è ammesso in questi file. Per ciascuna variante la riga valutata segue i campi proposti
dalla 03.8 per la 03.10:

`condition,agent_id,physical_case_id,true_pseudolabel,abstain,predicted_label,valid,is_correct,population`.

`condition` vale `numeric_global` o `numeric_local`; `valid=true` sempre, perché un errore di input
arresta l'esecuzione; `population` è `local_unseen`, `local_seen` o `normal`. Le distanze restano in
un file evaluator-side separato. La 03.10 non ha ancora pubblicato un branch/interfaccia da
adottare; questo schema riproduce i campi della 03.8 e dovrà essere confrontato byte-per-byte con
l'interfaccia definitiva prima del freeze.

Per ogni aggregato e per ogni cluster fisico `physical_case_id`, `metrics.json` riporta i tre
numeri:

1. `accuracy = correct / n`, con astensione nel denominatore come non corretta;
2. `abstention_rate = abstentions / n`;
3. `accuracy_non_abstained = correct / (n - abstentions)`, `null` se il denominatore è zero.

Sono inclusi i conteggi grezzi `n`, `correct`, `abstentions`, `non_abstained` e
`independence_claim=false`. Il cluster è il run fisico; tutte le viste agente-caso dello stesso run
restano unite. La futura valutazione sui test userà lo stesso bootstrap a cluster stratificato
della 03.8/03.10; qui non si implementano decisioni statistiche pending e non si testa la baseline
contro B-LF.

## Separazione, determinismo e stato

Costruzione e valutazione sono comandi distinti. La costruzione può leggere l'indice di sviluppo
evaluator-side; il classificatore riceve soltanto pseudolabel e prototipi. Gli output JSON sono
canonicalizzati (`sort_keys`, niente NaN, newline finale), i CSV hanno ordine e terminatori fissi,
gli input e gli output sono hashati. Un output esistente e diverso non viene sovrascritto.

La sola esecuzione autorizzata in questa finestra è la fixture sintetica. Non si esegue
leave-one-batch-out e non si apre alcuna firma reale per classe. Qualunque smoke futuro sui dati di
sviluppo è esclusivamente tecnico e non è una stima di prestazione.
