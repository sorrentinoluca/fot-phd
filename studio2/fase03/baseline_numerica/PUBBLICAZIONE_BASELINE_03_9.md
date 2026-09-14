# Pubblicazione e registrazione dell'efficacia — baseline numerica 03.9

Data del record: 2026-09-14. La baseline numerica 03.9 è congelata con il tag annotato
`studio2-fase03-baseline-numerica-frozen-001`; la rev.5 successiva al target ne registra
l'efficacia. 03.10, piano 03.8 e Fase 03 restano aperti. Questo record non qualifica l'harness
completo, il servizio 122B o il pilot.

| Passaggio | Fonte e riscontro |
| --- | --- |
| Dati pubblicati e riscaricati | `studio2-fase03-normal-dev-v1`; [record storico](VERIFICA_RISCARICAMENTO_NORMAL_DEV.json): 1.336 membri, zero differenze, SHA-256 archivio `eef69b42d8506c993ac45d77208df982d138b4354d7d4134bd67ba421dc91a03`. Nessun nuovo download in questa pubblicazione. |
| Verifica scientifica storica | [Verbale](VERIFICA_BASELINE_NUMERICA.md), OK su `ba1a206e1fe31c062d5491b4fb821ff925149982`; audit, evidence e prototipi riusati senza nuova review. Le deviazioni accettate e i limiti restano validi. |
| Mapping e sorgenti integrati | Raccordo minimo `3360867751c66a39e819247f86dab8e936f8cbb3`, consolidamento `04dee86140b3ff18882f9d164beef5ab7bf33e00`, sorgenti 03.6 `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb` e `7c99a8318cbe24bf864790566302f72614d963ed`, già pubblicati prima del candidato residui. |
| Fonte normativa rev.10 | `../piano_statistico/DELTA_HARNESS_03_10.md`, blob `780e08ae9e176a819a745ab2054a2e6ae79a8a9a`, SHA-256 `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`, acquisito in `49bc53b6d4630e7675eb5cf59c6d483d694ab042`, ora raggiungibile dal target pubblicato. Non è freeze del piano completo. |
| OK sui residui | Candidato `49bc53b6d4630e7675eb5cf59c6d483d694ab042`; verbale acquisito al percorso `evidenze_verifica_residui_49bc53b/VERIFICA_RESIDUI_BASELINE_03_9_2026-09-14.md`, SHA-256 `2131277d6d8840e767e73e3b0ab9e421f4b27acaa39a18faa770f19a69dd536a`; commit acquisizione `9370346c61d6edfdb0521aea812003a5f013748d`; [record di acquisizione](REGISTRO_OK_E_DECISIONE_TAG_BASELINE_03_9_2026-09-14.md), SHA-256 `6caa9f27cfb669db14ca8d0a1572412195f3d4e83265a0c7378831271fb35fd6`. |
| Decisione sul tag | Nome e regola del target approvati dall'autore; [record pubblicato](REGISTRO_OK_E_DECISIONE_TAG_BASELINE_03_9_2026-09-14.md), SHA-256 `6caa9f27cfb669db14ca8d0a1572412195f3d4e83265a0c7378831271fb35fd6`. |
| Pubblicazione prima del tag | Commit completo pubblicato `38cb5f5eaa2e5a7dddfd53564a7d020b6b50fa1e`, comprendente candidato, acquisizione OK e prerequisiti; target determinato `38cb5f5eaa2e5a7dddfd53564a7d020b6b50fa1e`. Nessun materiale preparatorio né rev.5 efficace nel tree del target. |
| Tag effettivamente pubblicato | Oggetto annotato locale e ref remoto `124262f5a6172a20965d019f220ff93954284922`; peeled `38cb5f5eaa2e5a7dddfd53564a7d020b6b50fa1e`; riscontro UTC `2026-09-14T20:53:04Z` con main remoto `38cb5f5eaa2e5a7dddfd53564a7d020b6b50fa1e`. Prova conservata [PROVA_REMOTA_FREEZE_BASELINE_03_9_2026-09-14.json](PROVA_REMOTA_FREEZE_BASELINE_03_9_2026-09-14.json), SHA-256 `1d49faf2c0eb04c98e0051810039cf4b21a9fd7868e539e8f314388544821303`. |
| Efficacia successiva | [BASELINE_FREEZE_rev005.json](BASELINE_FREEZE_rev005.json), SHA-256 `c52c7231021f52fc7b60b3b55eb67b5205854176395eb809db4d20227978b7cc`, creato in un commit strettamente successivo al target; la sua identità si risolve dalla storia Git, senza hash autoreferenziali nel record. |

La rev.5 è un nuovo record: revisioni 1–4 e verbali storici sono preservati byte-identici.
Il raccordo continua a pinnare la rev.3 (`0312f416dfdbaf8984b2063df2c2e9d00e1737321b9a65dd7e32b0295a937ec8`).
Distanza mean L1, tolleranza dei pareggi `1e-12`, astensione, denominatori e assenza di fallback
globale non cambiano. Il lotto dati e il tag baseline sono due oggetti distinti.

Le verifiche scientifiche e i 19 test mirati sono riusati. I controlli di finalizzazione hanno
verificato la catena di antenati e prerequisiti, gli hash delle revisioni 1–4, le nove sorgenti
della rev.3, l'estratto e il leakage 03.6, la fonte normativa rev.10, verbale e prove residue,
l'assenza di materiali preparatori nel target, nonché oggetto e peeled del tag e `main` remoti.
Il guardiano documentale prima e dopo l'aggiornamento ha eseguito 35 test con gli stessi 14
fallimenti storici, 1 skip e 0 errori; gli identificatori normalizzati dei fallimenti coincidono.
Log: SHA-256 pre-efficacia `be9cfd45eab761ac7d6b5628c1832d8eb44edcd3e811c40bfceaffa653c60dc4`,
post-aggiornamento `8ad1adb0e96ecd41f4bbcd24152b19bdaaa881cb1f1ea43c1d8d92f7f984bdfd`.
I valori delle prove pregresse non sono presentati come nuove esecuzioni.

Lo [schema insight 03.12](../schema_insight/PUBBLICAZIONE_SCHEMA_INSIGHT.md) resta congelato con
`studio2-fase03-schema-insight-frozen-001`, oggetto `4d15c4fb915ea9db9f7425225d231746778f0ba1`,
peeled `3c64390bc4dd58c48cc4e1e388a38989b32b3143`. Il pin 03.12 nell'harness è una questione
separata. Non sono stati eseguiti simulazioni, estrazioni, ricostruzione prototipi, riscaricamenti,
bootstrap, inferenze o run finali. FAR, A/B, U3 e PROVENIENZA restano invariati.
