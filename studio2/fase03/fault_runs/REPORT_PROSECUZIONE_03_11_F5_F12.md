# Rapporto unico — prosecuzione 03.11 F5/F12

Data: 2026-09-15. Esito operativo: **PASS locale del gate F5 e completamento del lotto
89/89; candidato sigillato in attesa di verifica indipendente, non pubblicato**.

## Esito, sostituzione e conteggi

Il verbale `VERIFICA_ESECUZIONE_03_11.md` e stato acquisito byte-identico con SHA-256
`2fb7dc83eb82db7e15bbc56f947bcbe3781ef5a853fa1fd710eaeb95f587bae8`. Restano
immutati lo STOP F6 e il precedente lotto 0/89 del candidato
`1cdf597b9a95e7f1c9a3d6711c2f840c8b5ab6aa`.

Il piano eseguibile e i criteri invariati della catena `F6→F5→F12` sono stati congelati
prima della nuova sonda nel commit `f650f0306a9e7aa3220de6a3b4d14fc0377f8770`,
tree `703dd58b3736ae7f1be173773bfd15121fdc0537`. La rilevabilita F5 ha superato la
sola condizione bibliografica prescritta; la successiva sonda tecnica F5 ha terminato a
65 h, senza trip, con attivazione osservata e 8/8 finestre complete. E stata quindi
applicata la sostituzione **F6→F5**. F12 non e stata eseguita.

Il lotto `test_batch_f5` e completo **89/89**: 64 primari fault, 8 primari Normal,
6 OOD (3 F5 e 3 F4) e 11 scorte tecniche. Tutti gli 89 run sono `complete`, con 712
finestre complete; 0 trip fisici, 0 errori tecnici, 0 `not_run`. Le 11 scorte sono state
generate come prespecificato e nessuna e stata attivata come sostituzione. L'audit specifico
e generico e `PASS`, inclusa la verifica degli hash.

## Path e sigillo

- sonda F5: `studio2/fase03/fault_runs/ood_chain_f5/chain_f5_001`;
- lotto: `studio2/fase03/fault_runs/test_batch/test_batch_f5_001`;
- audit: `studio2/fase03/fault_runs/BATCH_AUDIT_03_11.json`;
- sigillo: `studio2/fase03/fault_runs/SIGILLO_LOTTO_03_11.json`;
- archivi locali: `ood_chain_f5/chain_f5_001.tar.gz` e
  `test_batch/test_batch_f5_001.tar.gz`.

MATLAB e R2025b Update 6 arm64; il MEX qualificato ha SHA-256
`834e2361915249402a1ec9074a4be04f22a6404deb841e5134bf34347dfde544`.
Sono state effettuate zero chiamate Qwen o ad altri modelli e nessuna selezione su
prestazioni diagnostiche.

La suite del generatore e del protocollo e **27/27 PASS**. La rigenerazione read-only
dell'audit in un path temporaneo e byte-identica al record sigillato. Il guardiano
documentale riproduce il baseline preesistente: 35 test, 14 fallimenti e 1 skipped.

## Anomalie e limite di consegna

Non risultano anomalie tecniche nel nuovo lotto. Il guardiano documentale mantiene il
debito storico preesistente ed e registrato separatamente dalle verifiche del generatore.
Gli archivi voluminosi restano locali e ignorati da Git. Non esiste ancora una verifica
indipendente del nuovo candidato: walkthrough, pubblicazione esterna, tag, push e merge
restano esclusi.
