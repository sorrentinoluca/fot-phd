# Fase 02 — Provenienza della copia del simulatore

La copia modificabile vive interamente sotto `studio2/fase02/simulator/`. Gli originali in
`tep_parent_a0413e16/`, `tennessee-eastman-dataset/` e nelle aree congelate non sono stati
modificati.

## Origine

Base del simulatore: stato pre-setpoint identificato dal commit
`a0413e16c940f0fc8b554d6a86248020d7fb7527`, lo stesso documentato per i run PBH.

| File copiato | SHA-256 originale | Modifica nello studio 2 |
| --- | --- | --- |
| `temexd_mod.c` | `0da41d939e5ab7ba122d7b70c124368ee0882fce40e775dba5d180e7a7e24e5e` | convertiti i commenti Windows-1252 in UTF-8; S-function rinominato; stato legacy sostituito da stream/contatore Philox; corretti due specificatori di formato che producevano warning |
| `teprob_mod.h` | `e8d07857030a837443ce947361335f2e6f2ade5d2fa54a85bcc5c4a6d9afe939` | nessuna |
| `MultiLoop_mode1.mdl` | `d2f6659f65935021d4b1813e7189be02e7ae9f5639b794e8edc4f2f3c5cddba8` | S-function `temexd_philox`; parametro esplicito `fot_stream_id`; `MSFlag=0` |
| `tesys.mdl` | `53fb449f1fb592134a584dc8ad7d6c8cbbf2a33fa72fc87f5e795e8f4111c341` | stesso cambio di S-function e parametro |
| `TElib.mdl` | `4605de6ca0e6da67626e2be6d5f328c735f8bf5a5a730dc67f558a3f1dabddba` | nessuna |
| `Mode_1_Init.m` | `9dfb4e404c8c982c035fe47472020443b0a1d3f37b55425219968489d92d8933` | nessuna; contiene `Ts_base=0.0005` e `Ts_save=1/60` |
| `Mode1xInitial.mat` | `40eaebc92badb04ad026e358cfd28ec9c778fcf2d24a1b8f5d85565854da2747` | nessuna; il nome del modello resta `MultiLoop_mode1` perché i percorsi dello stato iniziale sono nominali |
| `TEplot.m` | `f10cc8751c1dd99c2efe989460871e701704bc8bde901d83a13834327e75b1be` | nessuna; dipendenza del callback legacy, disattivato dal launcher batch |

## Nuovi componenti

- `source/philox4x32.h`: implementazione autonoma Philox4×32-10, contatore a 128 bit formato da
  indice di blocco e stream ID, chiave a 64 bit;
- `source/philox_kat.c`: tre known-answer test della distribuzione primaria Random123, più replay
  deterministico e controllo minimo fra stream;
- `matlab/compile_philox.m`: compila soltanto in `simulator/build/` e rifiuta di sovrascrivere un
  MEX esistente;
- `matlab/generate_normal_runs.m`: accetta piano e destinazione espliciti, limita la destinazione a
  `studio2/`, rifiuta manifest o run preesistenti, scrive prima su file temporaneo e registra
  contatore RNG finale, impronte di MEX/modello, configurazione, durata, stato e SHA-256;
- `build_generation_plan.py`: assegna intervalli di stream disgiunti ai diversi insiemi e rifiuta
  output fuori `studio2/` o già esistenti.

Il MEX di prova è escluso da Git ma ricostruibile. Compilazione verificata con MATLAB R2025b ARM e
Xcode/Clang; SHA-256 della build locale definitiva, con esportazione del contatore diagnostico:
`6ae7e7be5394773f1854f1c53eddbd778ad7557b61fb05a93b3edb0552b1d11e`.
L'impronta identifica questa build locale, non una build portabile fra piattaforme.

## Smoke test tecnico

Il piano `tests/fixtures/runtime_smoke_plan.csv` usa lo stream riservato 999999 e 0,05 h di tempo
simulato; non appartiene a burn-in, pilot, calibrazione o verifica. Il launcher ha prodotto quattro
righe dati e 54 colonne, ha registrato un SHA-256 coincidente con il controllo esterno e ha rifiutato
la seconda scrittura nella stessa destinazione. Questo prova il percorso tecnico minimo; non
sostituisce i confronti numerici della sotto-fase di validazione.
