# Richiesta metadati Qwen — testo pronto da inoltrare

**BOZZA NON INVIATA** — 15 settembre 2026, Europe/Rome. Il testo sotto chiede documentazione, non prove, riavvii o modifiche. L'inoltro resta esterno a questa consegna. Provenienza, pin storici e matrice M01–M14: [inventario D9](INVENTARIO_SERVIZI_D9_2026-09-15.md). Non allegare credenziali.

---

Oggetto: metadati mancanti dei servizi Qwen per Studio 2 FoT-TEP

Per i servizi di tua competenza, ci servono i dati sotto, con data di validità e indicazione di eventuali informazioni non disponibili. I ruoli sono già fissati: 122B producer principale e consumer; 27B solo producer alternativo, per una libreria di 16 insight.

Per il 122B abbiamo già alias `qwen3.5-122b`, contesto dichiarato 131.072, output massimo 16.384 e l'indicazione di **omettere `temperature`** (default dichiarato 0,6). Ci manca:

- Repository esatto e revisione immutabile dei pesi caricati, eventuali adattatori e manifest/hash; quantizzazione effettiva, dtype di calcolo/KV, hardware e parallelismo; mapping alias→backend, comprese repliche o routing.
- Tokenizer con repository/revisione, versione, file e SHA-256; template effettivo con byte/hash e criterio di hashing, override, special token e opzioni applicate. Serving con versione/build, configurazione senza segreti, parser reasoning e supporto structured output.
- Semantica dei limiti input/output/combinati, inclusione del thinking, overhead e gestione oltre limite/tagli silenziosi; modalità/default thinking, controlli del budget, campi reasoning; altri parametri di sampling/seed/stop supportati, ignorati o rifiutati e relativi default.
- Campi disponibili per correlare richiesta/risposta, usage (anche reasoning), finish reason e fingerprint; timeout di server/proxy/coda, errori e possibilità di documentare mancata generazione e contatori zero per una specifica richiesta. Basta documentazione o un esempio già disponibile, senza nuova generazione.
- Politica di aggiornamento/riavvio e segnalazione dei cambi backend; periodi di disponibilità/manutenzione, rate limit, concorrenza ammessa, code e carico condiviso.

Per il 27B occorre riconfermare o aggiornare gli stessi dati partendo dal record del 13/09: `Qwen/Qwen3.8-27B-FP8`, revisione `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, alias `fot-exp2-consumer`, vLLM 0.28.0, contesto 16384, max-num-seqs=1. Il record riporta anche architettura `Qwen3_5ForConditionalGeneration`: chiediamo di chiarire la corrispondenza, senza rinominare i pesi. Servono inoltre endpoint/modalità di accesso correnti per il producer e riconferma dei pin tokenizer/template. Il loopback storico 8001 non identifica l'accesso dalla nostra postazione.

Non chiediamo test, cambi di configurazione o credenziali; le prove del servizio saranno autorizzate separatamente.
