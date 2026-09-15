# Preparazione locale — integrazione schema insight 03.12 R4

Data: 2026-09-14, Europe/Rome. Stato: **candidato locale; nessuna pubblicazione eseguita**.
La Fase 03 resta aperta. Questo record documenta controlli e passaggi preparati: non attesta
merge in `main`, push, creazione o pubblicazione del tag.

## Oggetto già verificato

- Verdetto indipendente: **OK R4-V**.
- Target implementativo verificato e unico destinatario futuro del tag:
  `3c64390bc4dd58c48cc4e1e388a38989b32b3143`.
- Contratto revisione 4; manifest revisione 5, stato storico
  `frozen_pending_independent_verification` e `tag_created=false` preservati.
- `SCHEMA_FREEZE.json`: 12.323 byte, SHA-256
  `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`.
- `previous_manifest_sha256`: `d6ef52de0f573edf3e5d6eb5ad3530400c5f63e6bcfa6579a93f21fdfb8865b5`,
  coincidente con il manifest rev. 4 al commit `e058cb07dceeefa8eb4a4b6d1f6fcab5aad483db`.
- Esecutore R4: Codex/OpenAI `gpt-5.6-sol`, reasoning medium, task
  `01a09f1b-a581-7c41-a1ec-87912c8896ef`, secondo l'evidenza runtime citata nel verbale.
- Verificatore indipendente: Claude/Anthropic, identificativo configurato
  `claude-fable-5-1`, sessione `session_01Y11UC227qhEvrbQxjzRpzK`; i limiti
  dell'identificazione sono dichiarati nel verbale.

L'OK riguarda il contratto e le fixture verificate. Non sono stati prodotti insight e non sono
dimostrate validità scientifica delle narrative, capienza dei prompt reali o ottimalità dei cap.

## Evidenze successive al target

Il commit `43b31afc1ff271594cb4bd21a39fa4469a8c83bc` acquisisce, dopo R4, il verbale OK,
il log della qualifica e il prompt operativo. È discendente di `3c64390…`, ma non sostituisce il
target del tag.

| Evidenza | Byte | SHA-256 | Provenienza |
| --- | ---: | --- | --- |
| `TEST_RESULTS_qwen_rev004.txt` | 7.459 | `a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972` | trascrizione del terminale fornita dall'autore e copiata byte per byte dall'allegato; non file originale scaricato dal server |
| `VERIFICA_SCHEMA_INSIGHT_rev004.md` | 21.288 | `d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e` | verbale indipendente R4-V, verdetto OK |
| `VERIFICA_SCHEMA_INSIGHT_rev004_NON_OK_STORICO.md` | 19.064 | `5bd196820f74b7fbd5ee6736df2b72afc64afbbfb26459dc69f1fe5e15dafd19` | precedente NON OK, acquisito separatamente e byte-identico nel commit locale `9b1fac9808b92222f45b8b590db32a378d73c136` |

Il log e i verbali sono esterni alle 18 voci del manifest rev. 5. Non è stato creato un manifest
rev. 6 e il pacchetto R4 non è stato riscritto per incorporare evidenze posteriori.

## Controlli locali della preparazione

Il worktree dedicato è `/Users/luker/fot-tep-schema-insight-r4-integrazione`, branch
`codex/studio2-schema-insight-r4-integrazione`, creato dal `origin/main` osservato e verificato
anche sul remoto a `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`. Il commit locale
`c0f4da01b7b68f21e717f3b52c2409cbe81c649d` integra la storia del candidato e conserva, nel solo conflitto effettivo,
entrambe le sezioni di `studio2/PROVENIENZA.md`.

- 18/18 voci del manifest verificate per SHA-256 e dimensione: 10 file al target R4,
  6 fonti al commit base `d815ce96d928254de79209f02e11a561445764cd`, 2 fonti 03.7 al commit
  registrato `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155` e al tag congelato.
- Tag 03.7: oggetto annotato `6854c49b4034c16b8df3b11d45dd759a343463e2`, peeled
  `c16b533016db4617deb1ba96853253f117e8e32b`; antenato del commit 03.7 registrato.
- Contratto, manifest rev. 5, decisione e report storico R4 byte-identici al target
  `3c64390…` dopo il merge locale.
- Il tag `studio2-fase03-schema-insight-frozen-001` era assente al controllo iniziale.
- Suite 03.12 nel venv locale qualificato (Python 3.13.15, jsonschema 4.26.0): 26 test,
  **25 PASS, 0 FAIL/ERROR e 1 SKIP** per assenza dello snapshot tokenizer pinnato.
- Regressioni `studio2/fase03/tests`: **16 PASS**, 0 FAIL/ERROR/SKIP.
- Guardiano documentale prima e dopo: 35 test, **14 FAIL storici e 1 SKIP**, con gli stessi
  identificativi e subtest; nessuna regressione. Il primo lancio non qualificante col Python di
  sistema ha riprodotto l'incompatibilità x86_64/arm64 di `rpds` già registrata nel report
  (46 FAIL, 6 ERROR, 1 SKIP) e non è stato interpretato come difetto del contratto.
- Parità della nuova sezione Markdown/HTML: 26/26 fatti controllati; 8/8 link della sezione
  risolti; anchor e collegamenti di navigazione univoci.

Esiti da mantenere distinti: la suite locale R4 documenta **25 PASS + 1 SKIP** su 26 per
assenza dello snapshot tokenizer; la trascrizione dell'autore documenta **26 PASS su 26** sul
server, senza skip. La seconda non è stata rieseguita in questa preparazione.

## Annotazione proposta per il futuro tag

Target: `3c64390bc4dd58c48cc4e1e388a38989b32b3143`.

> studio2(fase03): schema insight contratto rev004 verificato R4-V;
> manifest rev005 d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12;
> Normal letterale allineata a 03.7; qualifica Qwen R4 documentata 26/26;
> verbale d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e;
> evidenze supplementari conservate in main; insight scientifici non prodotti;
> Fase 03 aperta

L'annotazione è soltanto proposta: nessun oggetto tag o peeled 03.12 esiste ancora da registrare.

## Passaggi residui per l'integrazione seriale

1. Ricontrollare `origin/main` remoto e l'assenza del tag immediatamente prima dell'integrazione.
2. Integrare questo candidato nel `main` corrente in un unico cantiere seriale, risolvendo soltanto
   conflitti effettivi e senza modificare i byte del pacchetto R4.
3. Verificare che `3c64390…`, `43b31af…`, il commit locale d'integrazione e il commit documentale
   siano antenati del `main` risultante; ripetere hash, dimensioni, link, parità e test pertinenti.
4. Solo con autorizzazione esplicita, pubblicare `main` e accertare la raggiungibilità remota della
   storia e delle evidenze.
5. Solo dopo tale riscontro, creare il tag annotato sul target esatto `3c64390…`, pubblicare quel
   solo tag e verificare con `git ls-remote` oggetto e peeled.
6. Soltanto dopo la pubblicazione effettiva, creare `PUBBLICAZIONE_SCHEMA_INSIGHT.md` con i ref e
   i controlli reali. Non retrodatare lo stato pending del manifest.
7. In un'attività 03.10 separata, aggiornare pin, commit, manifest e messaggio dell'adapter,
   incluso l'hash di `validator.py` da `ec24159b50dc745963ccf820ccbb8ae2ce05c3894d005239aaf5c960ad9f1228`
   a `cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508`.

Questa preparazione non ha modificato `main`, non ha eseguito push, non ha creato tag, non ha
rilanciato test sul server, non ha qualificato il servizio 122B, non ha prodotto insight e non ha
modificato l'adapter 03.10.
