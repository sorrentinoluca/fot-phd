# Prompt — integrazione in main e pubblicazione del tag, sottofase 03.12 R4

Aggiornato il 2026-09-14 dopo l'OK indipendente R4-V. Questo documento prepara una
procedura futura: la sua acquisizione non esegue né autorizza automaticamente merge,
push o tag. La procedura va attuata su richiesta esplicita dell'autore.

## Oggetto verificato ed evidenze

- Branch candidato: `codex/studio2-schema-insight`.
- Commit implementativo verificato e destinatario esatto del tag:
  `3c64390bc4dd58c48cc4e1e388a38989b32b3143`.
- Contratto revisione 4, manifest revisione 5; `SCHEMA_FREEZE.json`: 12.323 byte,
  SHA-256 `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`.
- Base delta: `a1bcf61f0ccf20d070e92b7e2580dfdce5e9ea87`.
- Tag proposto: `studio2-fase03-schema-insight-frozen-001`.
- Log supplementare `TEST_RESULTS_qwen_rev004.txt`: 7.459 byte,
  SHA-256 `a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972`.
- Verbale OK `VERIFICA_SCHEMA_INSIGHT_rev004.md`: 21.288 byte,
  SHA-256 `d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e`.

Log e verbale sono nella stessa cartella di questo prompt. Il commit documentale che
li acquisisce è successivo al target implementativo: ricavane lo SHA con
`git log --diff-filter=A --format=%H -- studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md`
e verifica i suoi contenuti e la discendenza da R4. Non sostituire al target R4 tale
commit, l'HEAD corrente del branch o un futuro commit di merge.

Il log è una trascrizione del terminale fornita dall'autore, copiata byte per byte
dall'allegato; non un file originale scaricato dal server. È evidenza esterna alle
18 voci del manifest rev. 5, conservata insieme al verbale. Non generare un manifest
rev. 6 per questa acquisizione e non riscrivere lo stato pending o gli esiti storici.
La menzione dello skip locale nel manifest resta corretta per quella esecuzione.

Implementatore R4: Codex/OpenAI `gpt-5.6-sol`, reasoning medium,
thread `01a09f1b-a581-7c41-a1ec-87912c8896ef`, identificato nel log runtime della
sessione che ha creato 3c64390. Verificatore indipendente: Claude/Anthropic,
identificativo configurato `claude-fable-5-1`, sessione `session_01Y11UC227qhEvrbQxjzRpzK`;
limiti dell'identificazione esplicitati nel verbale. La dicitura generica «GPT-5» nel
report R4 e quella storica «GPT-6» non sostituiscono questi metadati.

Il precedente NON OK per indipendenza non attestabile resta conservato in
`/Users/luker/fot-tep-verifica-schema-insight-rev004/studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md`,
SHA-256 `5bd196820f74b7fbd5ee6736df2b72afc64afbbfb26459dc69f1fe5e15dafd19`.
Il nuovo verbale chiude quel rilievo; non sovrascrivere la verifica precedente.

## Procedura da eseguire solo quando richiesta dall'autore

1. Leggi `docs/MAINTENANCE.md`, `docs/prompts/Commit_LLM.md`,
   `docs/prompts/Documentazione_LLM.md`, decisione, report, proposta del tag e verbale
   R4-V. Il presente prompt aggiorna il target operativo rispetto alla proposta
   storica rev. 3. I vecchi OK non sono approvazioni di R4.

2. Ispeziona stato, branch, HEAD, worktree e riferimenti locali/remoti disponibili.
   Non assumere un valore storico di origin/main e non spostare checkout altrui.
   Verifica l'assenza del tag; se esiste già, controllane oggetto e peeled senza
   spostarlo o ricrearlo. Preserva modifiche estranee e prompt non tracciati.
   Lavora in un worktree dedicato all'integrazione; ispeziona prima quelli esistenti.

3. Prima dell'integrazione verifica gli hash e le dimensioni sopra riportati e le
   18 voci del manifest al target R4. Per le prime sei source_files usa anche la
   base dichiarata `d815ce96d928254de79209f02e11a561445764cd`; per le fonti 03.7 usa
   il main registrato `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155` e il tag
   `studio2-fase03-pseudolabel-frozen-001`, peeled
   `c16b533016db4617deb1ba96853253f117e8e32b`. Non confrontare fonti storiche con
   versioni mobili di documenti in main come se dovessero essere identiche.
   Conferma manifest rev. 5 / contratto rev. 4 e catena previous_manifest_sha256.

4. Completa la documentazione della sottofase prevista da MAINTENANCE §8.6 e
   Documentazione_LLM, in commit documentale distinto, aggiornando insieme le
   coppie Markdown/HTML pertinenti. Riporta identità degli esecutori, OK R4-V,
   provenienza del log e distinzione fra 25 PASS + 1 SKIP locali e 26 PASS server
   documentati. Record token: 83 per 001–006 e 013–016, 84 per 007–012; narrativa 20,
   scope 4. Nessuna prova di capienza reale o ottimalità scientifica dei cap.
   Mantieni i byte del pacchetto R4, inclusi report e manifest, come record storico;
   usa la documentazione successiva per attestare i nuovi passaggi. Fase 03 aperta.

5. Se l'autore ha richiesto l'integrazione, integra la storia del branch candidato
   in main preservando il lavoro concorrente. Non predeterminare i conflitti:
   ispeziona quelli effettivi. Per PROVENIENZA conserva entrambe le sezioni e i
   riferimenti corretti senza alterare gli artefatti verificati o i loro hash.
   Se occorre cambiare un byte del contratto R4, fermati: non è una risoluzione
   meccanica autorizzata da questa verifica. Controlla che il target R4, il commit
   delle evidenze e la documentazione siano tutti antenati del main risultante.
   Ricalcola gli hash del pacchetto e delle evidenze; le fonti esterne restano
   identificate dai propri riferimenti Git storici.

6. Riesegui le verifiche pertinenti e `docs/test_explanation.py` prima/dopo;
   confronta gli identificativi dei 14 fallimenti preesistenti, incluso il dettaglio
   dei subtest (35 test, 1 skip). Nessuna nuova inferenza o simulazione.
   Se manca il tokenizer pinnato, mantieni distinto lo skip locale dalla qualifica
   server documentata. Un problema d'ambiente non è un difetto del contratto.

7. La pubblicazione richiede una richiesta esplicita dell'autore. Prima prepara
   commit, controlli e annotazione reviewabili; non interpretare l'esistenza di
   questo prompt come autorizzazione al push. Pubblica soltanto i ref necessari,
   mai tutti i tag con `--tags`. Accerta che la storia verificata e le evidenze
   siano raggiungibili da origin/main prima di pubblicare il tag.

8. Con autorizzazione esplicita al tag, crea il tag annotato
   `studio2-fase03-schema-insight-frozen-001` sull'esatto
   `3c64390bc4dd58c48cc4e1e388a38989b32b3143`, NON sul commit di merge o di acquisizione.
   Annotazione proposta:
   «studio2(fase03): schema insight contratto rev004 verificato R4-V;
   manifest rev005 d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12;
   Normal letterale allineata a 03.7; qualifica Qwen R4 documentata 26/26;
   verbale d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e;
   evidenze supplementari conservate in main; insight scientifici non prodotti;
   Fase 03 aperta».
   Pubblica quel solo tag e verifica con `git ls-remote` oggetto e peeled.

9. Solo dopo pubblicazione effettiva, registra oggetto tag, peeled, commit delle
   evidenze, impronte e controlli in `PUBBLICAZIONE_SCHEMA_INSIGHT.md`, secondo il
   precedente 03.7. Il record di pubblicazione attesta il freeze: SCHEMA_FREEZE.json
   rev. 5 resta byte-identico e pending come fotografia storica. Non dichiarare
   pubblicato ciò che è soltanto preparato o creato localmente.

10. Consegna commit documentali e d'integrazione, oggetto tag e peeled, impronte,
    risultati dei test e stato remoto effettivo. Per 03.10 segnala l'aggiornamento
    successivo di pin, commit, manifest e messaggio dell'adapter: validator.py da
    `ec24159b50dc745963ccf820ccbb8ae2ce05c3894d005239aaf5c960ad9f1228` a
    `cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508`.
    Non eseguire tale modifica nell'integrazione di 03.12.
