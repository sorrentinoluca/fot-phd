OK

Commit candidato: `fd41fcf05aa6374d01b45b26b0881e2ffcc98062`.
Tree candidato: `9010a6b3aab4029f20ff5355455c452bbefde1b5`.
Perimetro: `1cdf597b9a95e7f1c9a3d6711c2f840c8b5ab6aa..fd41fcf05aa6374d01b45b26b0881e2ffcc98062`.

Nessun rilievo bloccante. Catena lineare e separazione dei ruoli verificate: acquisizione del verbale precedente byte-identica (1.132 byte, SHA-256 `2fb7dc83eb82db7e15bbc56f947bcbe3781ef5a853fa1fd710eaeb95f587bae8`) in `ab8f5bb06e6d438c6727abf2d45b3f5efbefb55b`; prespecificazione in `f650f0306a9e7aa3220de6a3b4d14fc0377f8770`, tree `703dd58b3736ae7f1be173773bfd15121fdc0537`, precedente alla sonda F5; successore `fd41fcf05aa6374d01b45b26b0881e2ffcc98062` solo documentale/audit.

Risultati realmente eseguiti:

- `python3 -m unittest discover -s studio2/fase03/fault_runs/tests -p 'test_*.py'`: 27/27 OK.
- Audit generico read-only F5: 1/1 manifest, hash verificati, `complete`, IDV 5, attivazione valida, fine 65 h, nessun trip, 8/8 finestre.
- `audit_test_batch_03_11.py` rigenerato fuori dal worktree: PASS e byte-identico a `BATCH_AUDIT_03_11.json` (SHA-256 `420a61eb65a47961092ee042f7fa08797a25b350f875cad76c0954f7f3eeb6e3`).

Conteggi ricalcolati da piani, 89 manifest, eventi e raw verificati: 64 primari fault, 8 Normal, 6 OOD (F5 3, F4 3), 11 scorte; 89 `complete`, 0 trip, 0 errori tecnici, 0 `not_run`, 712 finestre complete. Tutti i 78 run ordinari sono completi e il ledger eventi non contiene semantica di rimpiazzo: scorte attivate come rimpiazzo 0. Applicata `F6→F5`; F12 assente. I due piani alternativi di lotto hanno 89 righe ciascuno e stream disgiunti 71000–71088 e 72000–72088.

PDF primario locale verificato visivamente a p. 6: Tabella 2/F5 conferma FDR DAE 100%, PCA-T² 29%, PCA-SPE 31%; SHA-256 PDF `e11310c44cebca7a6ebc368b3862dc2edc0003a4ee31cb9223feb6d5e0ae7b78`. Tutti i file, byte count e hash dichiarati in `SIGILLO_LOTTO_03_11.json`, inclusi i due archivi locali, sono ricalcolati e coincidenti. `external_publication=null` e `independent_review_of_this_candidate=null` confermati.

Limiti: sola review locale e in lettura; non rieseguiti MATLAB, sonde o lotto, né Qwen, guardian documentale o suite estranee. Le prove runtime ignorate da Git sono autenticate localmente; non attestano pubblicazione esterna.

Path: `/Users/luker/fot-tep/VERIFICA_ESECUZIONE_03_11_v2.md`.
