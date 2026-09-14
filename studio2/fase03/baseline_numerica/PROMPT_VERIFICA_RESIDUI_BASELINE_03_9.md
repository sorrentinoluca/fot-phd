# Prompt — verifica indipendente dei residui baseline 03.9

Esegui una verifica **indipendente e in sola lettura** del candidato esatto indicato dalla
consegna Git. Leggi prima `docs/MAINTENANCE.md` e `docs/prompts/Verifica_LLM.md`. Non correggere
il candidato, non creare commit, push, merge, release o tag. Non eseguire simulazioni, estrazioni,
costruzione prototipi, bootstrap, download, inferenze o run finali.

## Perimetro esclusivo

Confronta il candidato con la sua base `f1746e1e76c5657e5cb74ed765d2f22143f979ce` e verifica
soltanto questi cinque file nuovi:

- `studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md`;
- `studio2/fase03/baseline_numerica/ACQUISIZIONE_DELTA_HARNESS_03_10.json`;
- `studio2/fase03/baseline_numerica/BASELINE_FREEZE_rev004.json`;
- `studio2/fase03/baseline_numerica/RAPPORTO_RESIDUI_BASELINE_03_9_2026-09-14.md`;
- `studio2/fase03/baseline_numerica/PROMPT_VERIFICA_RESIDUI_BASELINE_03_9.md`.

La verifica scientifica di `normal_dev`, evidence e prototipi e la verifica tecnica del raccordo
`3360867`/`04dee86` sono già acquisite: non ripeterle. Riesegui soltanto i 19 test mirati se
necessario per accertare che il nuovo delta non abbia alterato i sorgenti, e il guardiano
documentale per verificare assenza di regressione.

## Controlli richiesti

1. Il file acquisito deve essere byte-identico a
   `6aaa5b3eebfed4ba502c25c0443caabd0051af21:studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md`:
   blob `780e08ae9e176a819a745ab2054a2e6ae79a8a9a`, SHA-256
   `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`.
2. Il delta non deve importare altre parti della rev.10, dichiarare approvato/congelato il piano
   03.8, decidere D9, qualificare 122B o autorizzare/eseguire il pilot.
3. Verifica sulla fonte pubblicata, non solo su `INTERFACE_CHECK.json`, che il mapping sia adottato
   e testato e che `non_abstained`/`invalid` abbiano la semantica riportata nella matrice.
4. Verifica ancestry e impronte dei sorgenti 03.6: `c66bd8d`, `7c99a83`,
   `extract_evidence.py` `46b451…24e97`, `leakage.py` `c77ae5…3887`, inclusi i pin effettivi di
   `extract_normal_evidence.py`.
5. Verifica che distanza mean L1, pareggi `1e-12`, astensione, denominatori e assenza di fallback
   globale non siano cambiati.
6. Verifica la catena SHA-256 delle revisioni e che `BASELINE_FREEZE.json`, rev.2 e rev.3 siano
   byte-identici alla base; l'adapter deve continuare a pinnare la rev.3 storica.
7. Controlla che la rev.4 non dichiari `effective=true`, non inventi nome/target del tag e separi
   candidato, pubblicazione del tag e successivo record di efficacia.
8. Conferma o smentisci la conclusione sulla rev.10: il file normativo è necessario alla
   provenienza riproducibile del raccordo, ma l'integrazione/congelamento dell'intero piano 03.8
   non è requisito del freeze 03.9.
9. Verifica che i risultati riusati siano distinti dai controlli eseguiti ora e che il diff non
   apra dati test, nuove prestazioni o artefatti voluminosi.

## Output obbligatorio

Scrivi un verbale nuovo, con `VERDETTO: OK` o `VERDETTO: NON OK` nella prima riga, modello,
sessione e commit completo verificato. Fornisci una tabella requisito/prova/esito e limita il
verdetto al delta di chiusura residui. Non autocertificare il freeze e non dichiarare chiuse 03.9,
03.10, 03.8 o Fase 03. Restituisci il percorso e SHA-256 del verbale perché una finestra successiva
possa acquisirlo byte-identico in un commit additivo.
