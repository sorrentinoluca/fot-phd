# VERIFICA_PROTOCOLLO_FINALE — review indipendente 7.3-R

Data: 2026-09-17. Modalità: offline, sola lettura, shell nativa; nessuna chiamata a provider,
nessuna lettura di `api_key.json` o `server_enea.json`. Oggetto verificato:
`e0db132fc6ef477bc054d8c02b3fb62f8c39da06`,
`codex/studio2-freeze-protocollo-finale`,
`PROTOCOLLO_FINALE_CANDIDATE.md` SHA-256
`d4f00224d473800105baa1d347b4f65a6685ff108f8c26331a2557de808e97fa`.

## Esito

**NON OK.** Il contenuto scientifico e contabile verificato è coerente, ma il requisito di
eseguibilità senza un meccanismo nuovo del §7 non è soddisfatto: manca l'esecutore finale che
applichi durevolmente schedule, canary e stop al batch. Il tag proposto
`studio2-fase03-protocollo-finale-frozen-001` **non deve essere creato** su questi byte.

## Riscontri

1. **Riferimenti congelati.** Ho ricalcolato tutti i 31 SHA dei file repository elencati nel
   manifest: coincidono, incluso il renderer `protocol.py` (`791fa347…53d1e`),
   `sampling.py` (`3ad3291f…c6a8f`) e il candidato. Coincidono anche tutti gli SHA delle fonti
   esterne leggibili, inclusi i tre artefatti 7.2 (`235fb0de…58a5a`,
   `90e93923…c036`, `fce3b955…4aaad9`). Gli otto tag nominati in §2 si risolvono agli oggetti
   attesi. Gli SHA con ambito diverso sono dichiarati correttamente: archivio evidence e array
   di presentation order.

   I commit delle librerie non sono raggiungibili da `main` né dal candidato: `c284523` e
   `f0d0393` sono contenuti soltanto da
   `codex/studio2-riconciliazione-stop-contabile`. Ordine necessario per una futura
   raggiungibilità da `main`: integrare prima quel ramo (fino a `f0d0393`), poi integrare il
   candidato 7.3 e soltanto allora creare il tag finale. Le due release citate non sono ref Git
   locali; l'evidence v2 è però documentata con asset e SHA in fonti locali. Vedi rilievo R2.

2. **Conteggio ricostruito dalle fonti.** Da `BUDGET_RISORSE_REV10.md`, catalogo Q8,
   `SIGILLO_LOTTO_03_11.json` (64 primari, 8 Normal, 6 OOD e 11 scorte non sostitutive) e otto
   riceventi: nucleo `4032+576+576=5184`; swap `4×8×7×3=672`; ablation
   `(8×8+4×3×7)×3=444`; OOD `2×3×8×3×3=432`. Con canary `10×7=70`, `X=100`, E5/FULL=0,
   librerie=0 e retry=0: `5184+672+444+432+70+100=6902`. Coincide. Il delta da 7.174 è
   `−256` E5/FULL e `−16` riuso librerie; il superamento storico è 3.202 (+86,5%).

3. **T5.** Ricalcolo sequenziale: `6902×26,209/3600×1,20=60,298 h` e
   `6902×36,661/3600×1,20=84,345 h`; entrambi minori di 168 h. Il candidato non usa un
   vantaggio di concorrenza.

4. **Piano statistico.** Blocchi, P1/P2/P3/P4, otto agenti e otto run, endpoint, invalidità e
   gerarchia H1→H2→H3 rinviano fedelmente a `PIANO_STATISTICO.md` §§2–4, 7 e 10. Le tre
   ripetizioni sono recepite correttamente: primaria=replica 1; repliche 2–3=tasso descrittivo;
   maggioranza soltanto nella sensibilità dell'audit deterministico. Le aggiunte operative
   individuate (intercalazione/schedule, Q=0, due giorni canary marcati, X=100) sono dichiarate
   come pre-registrazione nel candidato; il problema è la loro implementazione, non una
   riscrittura dell'inferenza.

5. **S18.** Ho ricostruito i 16 insight `G_P` dal manifest input congelato e chiamato
   indipendentemente `protocol.peer_insights` per gli otto agenti in B-LF ed E-LF: 112 record,
   112 con il solo campo `pseudolabel` diverso, zero differenze negli altri campi. PASS.

6. **T8.** `select_canaries` sul `pilot_prompts.jsonl` seleziona esattamente i dieci ID in §6,
   con bilanciamento 2/4/4 e copertura di otto agenti. Nel ledger del pilot ogni selezionato ha
   tre record concordi nella coppia parsata e nel relativo hash raw indicato. PASS per selezione
   ed aspettative.

7. **Checklist e deviazioni.** Le evidenze citate per PASS/PASS-C sono presenti; le decisioni
   richieste sono recepite senza «template unico», con E5 fuori batch e con il superamento 3.700
   esplicitamente dichiarato. L'asimmetria template e la covariata descrittiva 6/16 contro 0/16
   sono riportate fedelmente al verbale 7.2-R. Nessun blocco contabile o statistico è stato
   mascherato.

## Rilievi

### R1 — bloccante — il batch finale non è eseguibile con l'harness esistente

Il candidato §6–§7 richiede: inventario di 2.244 prompt, tre schedule PCG64 persistite,
resume che non rimescola, canary giornaliero prima del primo lotto, stop immediato su
`returned_model` **o** `system_fingerprint`, conteggio dei giorni marcati e stop prima del lotto
successivo. Non esiste un entrypoint che implementi questa transazione.

La sola ricerca del namespace `studio2-fase03-final-order-v1`, del seed PCG64 e della regola
del secondo giorno marcato restituisce il candidato, non codice. `run_pilot.py` è esplicitamente
limitato a `budget_probe` e `stability_gate`; `runtime.execute_request` è una primitiva per una
richiesta; `canary.py` offre soltanto funzioni isolate. In particolare
`canary.suspension_required` riceve un booleano `returned_model_changed`, non ispeziona né
persiste `system_fingerprint`, e non orchestra la barriera fra canary e lotto.

Perciò l'affermazione §7 «nessun meccanismo nuovo richiesto all'harness» non è dimostrata e
7.4-PREP non può partire senza una decisione/implementazione ulteriore. Prima di un nuovo
candidato servono un runner finale e test offline discriminanti che dimostrino: autenticazione
e persistenza della schedule prima del primo invio; resume senza rimescolamento né riuso slot;
canary identity-stop prima di ogni invio scientifico; primo/secondo giorno marcato; e conteggio
atomico contro il massimo 6.902. Il nuovo candidato dovrà essere riesaminato sui suoi byte.

### R2 — da correggere prima del tag — le release non sono verificabili come riferimenti congelati locali

`studio2-fase03-evidence-v2` e `studio2-fase03-test-v1` non sono tag/ref nel repository locale.
Il candidato riporta nome e SHA, ma non un URL/asset immutabile o una prova locale di esistenza
per entrambe; quindi non è possibile soddisfare offline alla lettera la verifica «ogni
tag/release esiste». Aggiungere al manifest le coordinate immutabili dell'asset e la prova di
verifica disponibile; riesaminare il documento modificato.

### R3 — nota — ordine di integrazione delle librerie

La dipendenza 7.2 è byte-identificata e corretta, ma vive esclusivamente sul ramo di
riconciliazione. Conservare esplicitamente nell'operazione di release l'ordine:
`f0d0393` in `main` → candidato finale in `main` → tag annotato. Questo non cambia le decisioni
autore né autorizza un merge in questa review.

## Condizione per 7.4-PREP

Manca soltanto quanto in R1 per rendere eseguibile il protocollo; R2 deve essere corretto prima
del tag. Tutte le altre decisioni necessarie risultano già congelate.
