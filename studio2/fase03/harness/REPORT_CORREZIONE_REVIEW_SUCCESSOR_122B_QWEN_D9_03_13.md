# Correzione review successor 122B — Qwen D9 03.13

## Esito

**READY FOR NEW INDEPENDENT REVIEW.** Sono stati corretti esclusivamente i rilievi F1 e F2 del
verbale indipendente NON OK sul candidato `65dad03c7878b5ba1b3dc185861f93387bef78a0`, tree
`2df08d333d8c7e887bc70986a2819135d8bcad09`, parent
`6e15fe59fe7b2f69c3e74e0bbf344985fa696c36`.

Il verbale è conservato byte-identico in
`harness/reviews/VERIFICA_IMPLEMENTAZIONE_RECUPERO_SUCCESSOR_122B_QWEN_D9_03_13.md`; sorgente e
copia hanno SHA-256 `58ca090df717cbce192767c71679fc127047a2472cda0e722c6b7702a82857b5`.
Il manifest della correzione è
`CORREZIONE_REVIEW_SUCCESSOR_122B_QWEN_D9_03_13.manifest.json`, SHA-256
`7f81b29de49b01e2c2fe6bb01e010858de81908e38a06b2c918ad2e01eacaf50`.

Questa consegna non crea un'autorizzazione di esecuzione e non autorizza la qualifica tecnica.

## Difetti riprodotti sul candidato respinto

Gli stessi byte finali di `test_successor_recovery.py` sono stati eseguiti in una copia isolata
del commit `65dad03...`. Risultato: 12 metodi, 11 failure comportamentali, 0 errori di
import/interfaccia. Il rosso riproduce:

- accettazione di `enable_thinking=0` nel producer e nel guard;
- accettazione della mutazione durevole `false -> 0` prima dello stage successivo;
- accettazione D9 delle mutazioni post-import di `request_id`, identità con digest riallineato,
  source binding, raw hash, record hash e approval hash;
- riuso diretto dell'ID nativo del predecessore dopo la mutazione di `request_id`, con scrittura
  dell'intent che rende il dump diverso.

I byte originari dei 10 test dichiarati nella consegna precedente non sono realmente recuperabili:
non sono stati ricostruiti né certificati per inferenza. I 9 test finali preesistenti sono rimasti
presenti; tre metodi discriminanti sono stati aggiunti.

## F1 — autenticazione completa del lineage

`PilotLedger._validated_predecessor_lineage` è ora l'unico validatore semantico completo riusato
dalla quota/prenotazione, dalle precondizioni e dal percorso D9. Nella stessa transazione della
decisione:

1. riapre package, approval e predecessore dai riferimenti durevoli;
2. riesegue `validate_successor_lineage_artifacts` per validare byte, decisione autoriale,
   provenienza e predecessore;
3. lega nome e hash dell'evento, package SHA, approval SHA, predecessor SHA e riferimenti esatti;
4. confronta ogni riga approvata con tutti i campi persistiti: ordinal, request ID, source kind,
   identity JSON canonico e digest, source binding SHA, disposition, raw/record SHA, package SHA e
   predecessor SHA.

L'import su un ledger nuovo persiste i riferimenti assoluti e gli SHA-256 di package e approval
nell'evento create-once. Il percorso D9 delega allo stesso validatore e richiede che i riferimenti
della configurazione coincidano con quelli durevoli. Non resta una seconda checklist parziale.

Le regressioni alterano separatamente tutti i campi elencati, dopo un import valido, alternando
same-instance e restart. Sia API diretta sia D9 rifiutano prima di nuovi intent; il conteggio
`requests` resta zero e il dump logico resta identico alla baseline già mutata. I controlli
positivi raggiungono la prenotazione/validazione corretta.

## F2 — booleano stretto e accounting effettivamente persistito

`d9.no_thinking_template_kwargs` accetta soltanto un dizionario con la singola chiave
`enable_thinking` e il valore di tipo booleano esattamente `False`. `0`, `True`, omissioni e chiavi
aggiuntive sono rifiutati. La stessa funzione è usata dal contratto producer, dal guard di
accounting e dalla qualifica tecnica.

La rivalidazione accounting calcola ora il digest del dettaglio effettivamente letto dal ledger,
lo confronta con event hash, proof della richiesta e commitment atteso, e riconvalida
semanticamente i kwargs. Anche il percorso record→accounting usato dalla chiusura dello stage
ricalcola il digest e applica il controllo di tipo. La mutazione persistita `false -> 0`, senza
riallineare gli hash, viene quindi respinta prima del binding dello stage producer successivo,
senza intent o trasporto.

## Verifiche finali

| Verifica | Risultato osservato |
|---|---|
| Test mirati finali | 12/12 PASS |
| Stessi byte sul candidato respinto | 12 metodi, 11 failure comportamentali attese, 0 errori |
| Regressione pertinente completa, 15 moduli | 189/189 PASS in 464,422 s |
| `git diff --check` | PASS |
| Guardian documentale storico | 35 test, 14 failure, 1 skip; NON PASS invariato |

La regressione completa include D9, accounting, lineage/history, quote, lifecycle, replay,
runner offline, protocollo ed execution guard. I `ResourceWarning` SQLite già presenti in alcuni
test storici non hanno modificato l'esito.

## Invarianti e runtime privato

Non sono stati modificati disegno scientifico, quote, ruoli 122B/27B, prompt scientifici, ordine
degli stage o decisione autoriale. Il massimo cumulativo resta 166, hard stop 200 e margine non
spendibile 34; remediation resta non consumata e non autorizzata.

I ledger reali non sono mai stati aperti con `PilotLedger`. Sono stati eseguiti soltanto hash e
controlli di mode read-only:

- ledger successor: SHA-256 `9c9101826d2cb39498c1e8d0b167921680c38f045aa156220a3a4ba077ed304b`;
- configurazione successor: SHA-256
  `f21b33a5e9a625ca8fa9f08711a09d456ee613b23b1f7f447faf6b26bd114067`;
- ledger predecessore: SHA-256
  `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`;
- directory privata mode `0700`; ledger e configurazione mode `0600`.

Tutti questi byte sono invariati. Il ledger successor v4 esistente, creato dal candidato respinto,
non contiene i nuovi riferimenti durevoli package/approval: sotto il codice corretto fallisce
quindi chiuso e non è stato migrato o retrofittato. Una futura materializzazione, dopo nuova review
e con un target fresco, dovrà produrre l'evento corretto; resta comunque necessaria una separata
authorization prima di qualunque chiamata.

## Limiti e attività escluse

Nessun provider contattato, zero token, nessun tunnel, nessuna execution authorization, nessuna
sonda o qualifica tecnica reale. `server_enea.json` non è stato letto o stampato. Nessun push,
merge o tag. Il commit e il tree del nuovo candidato sono riportati nell'handoff finale, dopo la
finalizzazione degli artefatti, per evitare riferimenti circolari nei file versionati.
