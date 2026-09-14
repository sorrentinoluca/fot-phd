# Prompt di verifica circoscritta — consolidamento 03.15 e raccordo metriche

Verifica in una finestra indipendente il solo candidato tecnico locale:

`04dee86140b3ff18882f9d164beef5ab7bf33e00`

Repository sorgente: `/Users/luker/fot-tep`. Il candidato si trova sul branch locale
`codex/studio2-consolidamento-0315-metriche`; il worktree dell'esecutore è
`/Users/luker/fot-tep-consolidamento-0315-metriche` e non deve essere modificato. Crea, se serve,
un worktree di verifica separato e detached all'hash esatto. Non usare la copia principale o un
branch `main` locale come base implicita. Non fare merge, commit, push, tag, freeze, chiamate a
modelli o simulazioni.

## Perimetro e precedenze

Il candidato deve consolidare come antenati:

- base comune `e82b5a08bf642ad45f77e71832958207beb1181c`;
- 03.15 corretto `10582798eb5a4b52672bfbcb1cc028adcb73e9f1`, che comprende il pacchetto
  `d35b684acbfd1f357bc34f3a21cebb18e8a6bea0` e il delta R1/R2 da `9b6bd64`;
- raccordo metriche minimo `3360867751c66a39e819247f86dab8e936f8cbb3`.

Il merge di consolidamento è `4ba2ad6e4a298411b4f0f7572ad3ef8e55948015`, con genitori
`10582798` e `3360867`. I commit successivi acquisiscono prove/documenti e applicano una sola
correzione tipografica di parità HTML; non estendono gli OK scientifici pregressi.

Leggi il record
`studio2/fase03/CONSEGNA_CONSOLIDAMENTO_0315_METRICHE_2026-09-14.md` dal branch di preparazione
come indice operativo. Il record e questo prompt sono documenti successivi al candidato tecnico
fissato sopra e non fanno parte del delta da qualificare.

## Controlli richiesti

1. **Grafo e perimetro.** Conferma che i quattro riferimenti sopra siano antenati del candidato e
   che `4ba2ad6` sia un merge a due genitori nell'ordine dichiarato. Verifica che non sia stato
   importato il vecchio harness completo: il codice runtime nuovo deve restare limitato a
   `common.py`, `metric_adapter.py`, `metrics.py`, `__init__.py` e al test mirato, con le sole
   dipendenze standard/documentali dichiarate.
2. **Identità dei pacchetti.** Confronta blob per blob i 17 file di
   `studio2/fase03/paper_sections/` presenti a `d35b684` e i 14 file di
   `studio2/fase03/harness/` presenti a `3360867`. Devono coincidere nel candidato; le sole
   aggiunte posteriori nelle due cartelle devono essere consegne, verbali o report acquisiti.
   Controlla inoltre che l'albero scientifico `studio2/fase03/evidence` coincida con `e82b5a0`.
3. **R4 e fonti 03.6/03.9.** Verifica le 18 voci di `SCHEMA_FREEZE.json` nei rispettivi riferimenti
   storici e che i 10 file di contratto R4 presenti coincidano con il target
   `3c64390bc4dd58c48cc4e1e388a38989b32b3143`. Non creare il tag: il target futuro resta soltanto
   `3c64390`. Ricontrolla le quattro impronte 03.9 fissate in
   `CONTRATTO_RACCORDO_METRICHE.md` e le impronte di `evidence/extract_evidence.py` e
   `evidence/leakage.py` registrate da 03.9.
4. **R1/R2 e walkthrough.** La ripartizione 44/8/2 di `FONTI_DELTA_0315.json` deve restare valida
   sia nel perimetro `10582798` sia rispetto al candidato finale; non reinterpretare le due fonti
   locali come committate. Conferma ordine, anchor, link, indice e parità normalizzata MD/HTML per
   §4.10 e §4.15. Il solo delta rispetto alle due versioni sorgente deve essere il raccordo della
   sintesi/indice e, in `04dee86`, tre spazi tipografici attorno alle frecce del mapping HTML.
   `studio2/PROVENIENZA.md` deve conservare §§1–14 come in `10582798`.
5. **Acquisizioni.** Verifica sorgente, copia di lavoro e blob Git per i cinque verbali principali,
   le due directory di evidenza e i quattro documenti esterni successivi. I manifest devono
   validare 30/30 e 28/28 voci senza sostituire se stessi. In particolare conserva distinti:
   snapshot B comune, 17.597 byte, SHA-256
   `46185e3d15867253e98f5c9f08df5ab8ed8a6a6643a15d5011079341045514e6`; snapshot B 03.15,
   11.046 byte, SHA-256
   `b7398a24f57f18b59be4cd77e40785a286805e619f76eb65d8642f0d941ba607`; consegna 03.15 viva
   successiva, 11.801 byte, SHA-256
   `8f2c1082606eea5554f0213d66a0f8dac5d66adc5ade4d35bca0a832bb4bdb71`.
   D ed E devono restare byte-identici ma con nomi distinti; D è non indipendente, E non espone
   ID sessione né effort.
6. **Metadati runtime.** Controlla il record
   `ACQUISIZIONE_IDENTITA_RUNTIME_CONSOLIDAMENTO_2026-09-14.md` contro le sole fonti mirate. Il
   collegamento dell'esecutore R1/R2 a `01a0a0e3-c3bd-7523-90ca-b5f28a40461f`,
   `gpt-5.6-sol`, effort `medium`, deve essere sostenuto dalla chiamata/output che crea
   `10582798`. Non dedurre identità dal committer o dallo stile. L'assenza di un riscontro
   affidabile per l'ID del revisore E è un limite da mantenere, non un motivo per alterare E.
7. **Test mirato e isolamento.** Da una copia ottenuta con `git archive` del candidato esegui
   `python3 -m unittest studio2.fase03.harness.test_metric_raccordo -v`: sono attesi 9 test OK,
   0 failure, 0 error e 0 skip. Verifica che il runtime non dipenda da checkout fratelli, percorsi
   assoluti, rete o dal package harness completo.
8. **Guardiano e lint.** Esegui
   `python3 studio2/fase03/paper_sections/lint_paper_sections.py --corpus docs/letteratura.md`
   (attesi 5 file, 0 segnalazioni). Esegui `python3 docs/test_explanation.py` sulla base
   `e82b5a0` e sul candidato: sono attesi 35 test, 14 failure storici, 1 skip e 0 errori, con gli
   stessi identificativi e subtest. Non descrivere il guardiano come PASS.

## Esclusioni

Non ripetere review scientifiche, estrazioni, bootstrap, ricerca bibliografica o riscaricamenti
già verificati in assenza di un difetto concreto. Restano fuori firma/freeze 03.8, D9,
qualificazione 122B, harness completo, pin 03.12, controlli OOD, simulazioni e chiamate
sperimentali. Non riaprire A/B, FAR o U3. 03.9, 03.10, 03.15 e Fase 03 restano aperte.

## Output

Produci un verbale separato con `VERDETTO: OK` oppure `VERDETTO: NON OK`, hash candidato completo,
identità runtime effettivamente esposta del revisore, comandi/esiti e limiti. Se NON OK, indica
file, rilievo e delta minimo necessario; non modificare il candidato. Se OK, limita esplicitamente
il verdetto al raccordo e alle acquisizioni di `04dee86`, senza estenderlo ai lavori aperti o
trasformarlo in autorizzazione a integrare, pubblicare o congelare. Restituisci alla finestra
orchestratrice percorso assoluto, byte e SHA-256 del verbale; non committarlo nel branch verificato.
