# Acquisizione OK — recepimento delle decisioni D9 su `3180aea`

Data di acquisizione: **2026-09-15 19:17 CEST (Europe/Rome)**.

## Esito acquisito

È acquisito byte per byte il verbale indipendente con verdetto **OK limitato al solo delta
`af50d54..3180aea`**, insieme alle tre prove nuove consegnate dal revisore. Il target è
`3180aeaacbec25a5907d556e8ca2aa7060a04865`, tree
`460a1a1d20eb7a3c6587a13682c31f398261498c`, genitore unico
`af50d54f1efea2c489b04f54e16cd99778f20c31`.

Sorgente esterna al candidato:
`/Users/luker/fot-tep/Claude outputs/verifica_recepimento_d9_3180aea/`.
Destinazione conservata:
`studio2/fase03/harness/d9_decisions_ok_20260915/`.

| Artefatto acquisito | Byte | SHA-256 |
| --- | ---: | --- |
| `VERIFICA_RECEPIMENTO_DECISIONI_D9_3180AEA.md` | 10.319 | `8b36472755e66aee7b598dc06d9262afe11e6154495772c353a1cfef2ca39030` |
| `evidence/fail_closed_probe.py` | 1.177 | `fd984e52d24002f06c78fe45246c6c8e0c55e87290ca5dd05b74aabc44c18ee3` |
| `evidence/fail_closed_probe.log` | 146 | `0e4718c33ce65ed77ea939b5314983f089fe2a725fca8fe3c682d9775224cfb8` |
| `evidence/guardian_summary.txt` | 295 | `56129a4cf834c71f2efa0e9c80d00c355b9182d9492349f0c87f38c7efd42da4` |

Per tutti e quattro i file, confronto `cmp` sorgente→copia concluso senza differenze;
dimensioni e SHA-256 sono stati ricalcolati dopo la copia. L'inventario macchina è in
`d9_decisions_ok_20260915/ACQUISITION_INVENTORY.json`. Le prove sono acquisite come record
della review: non sono state rieseguite in questa finestra.

## Portata e limiti conservati

- L'OK copre soltanto i tre JSON aggiunti da `3180aea`; non estende l'OK runtime D9, non
  modifica né rivalida runtime o ledger e non riapre D04 o R-D9-01/R-D9-02.
- `pilot_d9_decisions_received.json` resta un prospetto documentale sospeso, non collegato
  automaticamente a un loader. La barriera esecutiva resta il validatore runtime.
- La riconciliazione durevole S resta mancante e bloccante: nessun `request_id`, identity hash,
  prova zero-token, backfill, reset o modifica del ledger è acquisito o autorizzato dall'OK.
- Servizi 122B/27B, configurazioni, tokenizer/template, disponibilità e qualificazioni non sono
  certificati. Nessun GO, pilot, chiamata o autorizzazione esecutiva deriva dal verdetto.
- Il revisore dichiara una sessione Claude Opus 4.8 indipendente dalla preparazione di
  `3180aea`, ma non ha potuto leggere la skill locale harness. Il limite è parte integrante
  dell'OK e non viene corretto o omesso in acquisizione.
- Il guardiano riportato resta **NON PASS** sia sulla base sia sul candidato: 35 test,
  14 fallimenti storici e 1 skip, flussi per-test identici. Questa acquisizione non lo
  riclassifica PASS e non lo riesegue.

Il prompt di verifica preesistente e non tracciato nella worktree preparatrice resta fuori da
questa acquisizione. Nessuna suite, review, chiamata a servizi, pubblicazione o tag è stata
eseguita o creata qui.
