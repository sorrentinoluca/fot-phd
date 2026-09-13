# Record del MEX strumentato dei run fault

Stato: **equivalenza dimostrata** il 2026-09-13. Questo record identifica il binario
effettivamente usato nei 40 run `fault_dev_001` e documenta la sua equivalenza con il MEX
base congelato della Fase 02. Non modifica i run, i loro manifest o la specifica
pre-esecuzione originale.

## 1. Provenienza e identità

| Elemento | Percorso | SHA-256 |
| --- | --- | --- |
| Sorgente base congelato | `studio2/fase02/simulator/source/temexd_philox.c` | `230086e7712e753bf48f3e9108cd0ce2f68aba97d9590ebb3c7593a47f8b6d25` |
| Sorgente strumentato | `studio2/fase03/fault_runs/runtime/source/temexd_fault_philox.c` | `74bf641bcd16ce42093b3c78cf03887376d19561041f8746ccf01339042fb4c9` |
| MEX base del freeze | `studio2/fase02/simulator/build/temexd_philox.mexmaca64` | `6ae7e7be5394773f1854f1c53eddbd778ad7557b61fb05a93b3edb0552b1d11e` |
| MEX strumentato dei run fault | `studio2/fase03/fault_runs/runtime/build/temexd_fault_philox.mexmaca64` | `834e2361915249402a1ec9074a4be04f22a6404deb841e5134bf34347dfde544` |

`prepare_simulator.py` accetta soltanto il sorgente base con l'impronta sopra, cambia il nome
della S-function e inserisce blocchi delimitati da `FOT_FAULT_DIAGNOSTICS_BEGIN/END`.
La funzione inversa usata dai test rimuove tali blocchi, ripristina il nome e ricostruisce
byte per byte il sorgente base.

La strumentazione era già prescritta in `SPECIFICA_RUN_FAULT.md`, riga 24, al commit
`c02111d132f3cc1c047d5c4ed112398724138e3f`, registrato il 2026-09-13 alle
11:56:40 CEST, prima della generazione del sorgente, della compilazione e del batch.
La specifica pre-esecuzione prescriveva il gemello strumentato ma non poteva preregistrarne
l'hash binario: il binario è stato compilato successivamente.

## 2. Diff completo del sorgente

Il diff contiene **35 inserimenti e 1 cancellazione**. Le aggiunte leggono IDV e variabili
interne e scrivono soltanto i due nuovi campi di controllo diagnostico e il log MATLAB.
Non modificano equazioni, stato Philox, ordine delle estrazioni casuali, XMEAS o XMV.

```diff
--- studio2/fase02/simulator/source/temexd_philox.c
+++ studio2/fase03/fault_runs/runtime/source/temexd_fault_philox.c
@@ -679,7 +679,7 @@
  *               S - F U N C T I O N   D E S C R I P T I O N               *
  *                                                                         *
  **************************************************************************/
-#define S_FUNCTION_NAME  temexd_philox
+#define S_FUNCTION_NAME  temexd_fault_philox
 #define S_FUNCTION_LEVEL 2
 
 
@@ -830,6 +830,10 @@ struct stModelData {
   doublereal code_sd;  
   doublereal tlastcomp;
   integer MSFlag;
+/* FOT_FAULT_DIAGNOSTICS_BEGIN */
+  doublereal fot_diag_last_t;
+  unsigned int fot_last_idv_mask;
+/* FOT_FAULT_DIAGNOSTICS_END */
 };
 
 
@@ -1365,6 +1369,10 @@ static void mdlInitializeConditions(SimStruct *S){
       
   (*ModelData).dvec_.idv[28] = (float)0.;
   (*ModelData).code_sd = (float)0.;
+/* FOT_FAULT_DIAGNOSTICS_BEGIN */
+  (*ModelData).fot_diag_last_t = -1.;
+  (*ModelData).fot_last_idv_mask = 0;
+/* FOT_FAULT_DIAGNOSTICS_END */
   setidv(S);
 }
 
@@ -1403,6 +1411,29 @@ static void mdlOutputs(SimStruct *S, int_T tid){
   
   // Call TEFUNC to update everything
   tefunc(ModelData, &NX, &rt, rx, dx, 1);
+/* FOT_FAULT_DIAGNOSTICS_BEGIN */
+
+  /* Diagnostics only: no model, random state or solver writes. */
+  if (ssIsMajorTimeStep(S)) {
+    unsigned int mask = 0;
+    int j;
+    for (j = 0; j < 28; ++j) {
+      if ((*ModelData).dvec_.idv[j] >= 0.5) mask |= (1U << j);
+    }
+    if (mask != (*ModelData).fot_last_idv_mask) {
+      mexPrintf("FOT_IDV,%.17g,%u\n", rt, mask);
+      (*ModelData).fot_last_idv_mask = mask;
+    }
+    if (fabs(rt * 60. - floor(rt * 60. + 0.5)) < 1e-7 &&
+        rt > (*ModelData).fot_diag_last_t + 1e-10) {
+      mexPrintf("FOT_DIAG,%.17g,%u", rt, mask);
+      for (j = 0; j < 9; ++j) mexPrintf(",%.17g", (*ModelData).pv_.xmeasdist[j]);
+      mexPrintf(",%.17g,%.17g,%.17g,%.17g\n",
+        (*ModelData).teproc_.vcv[9], (*ModelData).teproc_.vcv[10], rx[47], rx[48]);
+      (*ModelData).fot_diag_last_t = rt;
+    }
+  }
+/* FOT_FAULT_DIAGNOSTICS_END */
 
   y[0] = ssGetOutputPortRealSignal(S,0);
   y[1] = ssGetOutputPortRealSignal(S,(((*ModelData).MSFlag & 0x2) >> 1));
@@ -1435,6 +1466,9 @@ static void mdlOutputs(SimStruct *S, int_T tid){
   // Shut down the simulation if ISD is non-zero.
   if ((*ModelData).dvec_.idv[28] != (float)0. && rt > (float) 0.1){
 	(*ModelData).code_sd = (*ModelData).dvec_.idv[28];
+/* FOT_FAULT_DIAGNOSTICS_BEGIN */
+    mexPrintf("FOT_TRIP,%.17g,%d\n", rt, (int)(*ModelData).code_sd);
+/* FOT_FAULT_DIAGNOSTICS_END */
 	ssSetStopRequested(S,1);
   } //if ((*ModelData).dvec_.idv[28] != (float)0. && rt > (float) 0.1){
 } /* end mdlOutputs */
```

## 3. Compilazione

Ambiente: macOS Apple Silicon, MATLAB `25.2.0.3312555 (R2025b) Update 6`, esecuzione
nativa ARM64, compilatore **Xcode with Clang**, opzione MEX `-R2018a`. Il binario locale è
stato creato il 2026-09-13 alle 12:03:41 CEST dall'account macOS `luker`; i log e il commit
di preparazione sono attribuiti a Luca Sorrentino. Il log non registra un'identità più
specifica dell'esecutore.

Comandi documentati ed eseguiti:

```bash
python3 studio2/fase03/fault_runs/prepare_simulator.py
/usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch \
  "addpath('/Users/luker/fot-tep/studio2/fase03/fault_runs'); compile_fault_philox"
```

Il compilatore invoca:

```matlab
mex('-R2018a', '-outdir', buildDir, ...
    fullfile(sourceDir, 'temexd_fault_philox.c'), ['-I' sourceDir]);
```

Il controllo preliminare `base_mex_unchanged=6ae7…` attestava che il MEX congelato della
Fase 02 non era stato alterato. Non selezionava quel MEX per il batch. Il launcher controlla
piano e destinazione; `generate_fault_runs.m` aggiunge esplicitamente `runtime/build`, cambia
in memoria la S-function in `temexd_fault_philox`, verifica il percorso controllato e registra
l'hash `834e…` in ogni manifest.

## 4. Prove di equivalenza

### 4.1 Normal Fase 02 con il MEX strumentato

Caso: `burnin_qual-001`, stream 0, 70 h. Copia di riferimento:
`studio2/fase02/validation/data_v2/burnin_qual/burnin_qual-001.xlsx`, SHA-256 del
contenitore `c3409d1457f25e30a74d1dba9dfcb520a4b65a4ab5ea2ea7eb9057868b5991c4`.
Rigenerazione e log:
`studio2/fase03/fault_runs/runtime/mex_equivalence/normal_instrumented/`.

Il criterio confronta il **contenuto** XLSX: nomi e byte dei membri ZIP, intestazioni,
valori double IEEE-754 e contatore Philox. Non richiede l'identità del contenitore ZIP,
i cui timestamp DOS cambiano a ogni scrittura.

- membri ZIP identici: **7/7**; membri con contenuto diverso: **0**;
- intestazioni identiche; matrice **4201 × 54**;
- righe diverse: **0**; celle diverse: **0**; massimo scarto assoluto: **0**;
- byte IEEE-754 dei valori: identici;
- contatore Philox finale: **423367045**, uguale al manifest conservato;
- contenitore rigenerato: 2.386.697 byte, SHA-256
  `30bfe18f65983bcec305b1f72a619a7ae371bb6b02af9bae66981875a090f65d`;
- differenza esterna: 42 byte, esclusivamente timestamp DOS ZIP; nessuna differenza di
  contenuto.

Esito: **equivalente**.

### 4.2 F1/30000 con il MEX base

Caso: `fault-dev-F1-b01`, stream/run index 30000, onset 25 h, stop 65 h. Riferimento:
`studio2/fase03/fault_runs/runs/fault_dev_001/fault-dev-F1-b01.csv`. Rigenerazione e log:
`studio2/fase03/fault_runs/runtime/mex_equivalence/fault_base_30000/`. I file diagnostici,
disponibili soltanto nella versione strumentata, sono esclusi dal confronto.

- file CSV: identico byte per byte, 3.817.751 byte;
- SHA-256 di entrambe le copie:
  `acb4c4ec62c267f089c7fab2799e18d26cf39f657b78dbef28246ff347f5c62c`;
- intestazioni identiche; matrice **3901 × 54**;
- righe diverse: **0**; celle diverse: **0**; massimo scarto assoluto: **0**;
- byte IEEE-754 dei valori: identici;
- contatore Philox finale: **383902344**, uguale al manifest del run.

Esito: **identico**.

## 5. Conclusione

Le due prove mostrano che il MEX strumentato `834e…` conserva le uscite e la sequenza
Philox del MEX base `6ae7…` nei due confronti complementari richiesti. Il criterio corretto
per i 40 manifest è quindi: hash MEX uguale al binario strumentato dichiarato in questo
record, con equivalenza dimostrata rispetto al MEX base del freeze; non uguaglianza fra i
due hash binari.
