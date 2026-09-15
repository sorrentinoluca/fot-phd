# Nuova verifica indipendente — correzioni R01–R10 harness offline 03.10

Prima di modificare qualsiasi cosa leggi docs/MAINTENANCE.md e rispettalo.
Questo incarico è una review indipendente, in una finestra distinta da quella che ha
implementato le correzioni. Non correggere il candidato. Lavora su un clone/worktree
isolato e pulito, detached sul commit esatto:

- candidato tecnico: **0c8157f23bee49a3a5a2df648525c34706da29d7**;
- tree: **a1573b49615a875f24ee97f9f1cd4bab399be93d**;
- parent/acquisizione: ec012911444de6baf1751ae4bf4aee8e9c24adbb;
- base della catena: 288dc1926bfd7ab4ce43bb4377a9a0064313ad69;
- base pubblicata comunicata: a00605862f627710347bd63c49f79a6d0a00135f;
- remoto effettivo: https://github.com/sorrentinoluca/fot-phd.git;
- manifest HARNESS_OFFLINE_CANDIDATE.json: **8ed9fbc37ee14d162ce65f55430159bb1e2507e95cf65aa8d72df3743170dbe1**, 11662 byte, 44 membri.

Il report e questo prompt sono consegna documentale successiva: non fanno parte del tree
tecnico. La base per il confronto delle sole correzioni è il commit di acquisizione; per
l’intera consegna confrontare anche 288dc192. Non importare lavori paralleli. Verifica il
main sul remoto effettivo, non origin/main di un clone con origin locale.

## Fonti

1. REPORT_CORREZIONI_HARNESS_03_10.md e MAPPA_RIPRODUZIONI_R01_R10.md: sono affermazioni da verificare.
2. Contratto CONTRATTO_ESECUZIONE_E_RIPRESA.md e codice/CLI/runner effettivi.
3. non_ok_20260915/evidence/VERIFICA_HARNESS_OFFLINE_03_10.md, SHA-256
   fc9725d5412ff30b789977cf12e6ae4742f8063cce7b6e5e2242aeddb3d61547;
   SHA256SUMS originale, SHA-256 0d25177f41ef9651ee246d5ad8610c020e43c931e168f3c18ba9098d871f0223.
4. ACQUISIZIONE.json: 2.754 membri, 1.471 acquisiti e 1.283 reference esterni con collocazione/hash/dimensione.
5. Script, osservazioni, log originali e correzioni_evidence; fonti normative improntate nel manifest.

Non eseguire lo script originale dentro l’acquisizione: riscriverebbe le prove. Copialo in
un contenitore sacrificabile con candidate separato e reference puntato ai byte verificati.
Tutte le fixture false/alterate, approvazioni e risposte stub restano non scientifiche.

## Prove da eseguire e ampliare

Non limitarti ai risultati dichiarati. Ricostruisci ogni R01–R10 dal verbale e prova anche
percorsi ordinari/alternativi, CLI, concorrenza, crash e resume. Verifica in particolare:

- UNDECIDED/SUSPENDED bloccati prima di server/SDK/trasporto; coordinate ledger approvate;
- tutti i pin e le dipendenze reali nei percorsi di consumo, e rifiuti a **zero invii stub**;
- handoff ricostruito dai raw del ciclo attivo, R4, manifest e label canoniche; nessuna
  autocertificazione o approvazione di fixture trasferita agli artefatti reali;
- atomicità di controllo/transizione, impossibilità di PASS su richieste fallite/incerte,
  eventi normativi non falsificabili tramite API pubblica e assenza di riapertura;
- identità completa attraverso alias, stage_run, directory e restart; catene retry senza
  biforcazioni; triplette con tre originali distinti del gruppo corretto;
- remediation soltanto per diagnosi registrata ammissibile e diff/template approvati,
  stessi otto casi/contratti, vecchio handoff escluso e timeout non convertito in difetto prompt;
- persistenza durante lo stadio, finestre intento→trasporto→raw→record→outcome/file finale,
  crash di processi reali, mancato reinvio incerto e riconciliazione documentata;
- primo gate vincolato ai byte/configurazione e risultati sonda, inclusi tentativi di
  ricalcolare tutti gli hash di artefatti alterati;
- identità per ogni risposta, sospensione e conservazione di raw/token/consumo;
- campione congelato e 40 triplette autentiche, ripetizioni 1–3, 8/16/16, hash e ID,
  matched_transfer/context_stress, semantica T3/T4/T6 e R3 pending T5;
- limiti 8r+t≤15, quota7 sonda, 152/160 e hardstop200 distinti; zero retry gate;
- i tre file metriche e gli artefatti fuori perimetro sono invariati.

Runtime indicato dal verbale e usato qui: **/opt/anaconda3/bin/python3 3.13.9 arm64**, SQLite
3.51.0. Distingui eventuali errori di dipendenza dalle assertion del candidato.

```text
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 docs/test_explanation.py
```

I test nuovi usano la reference locale già verificata; per una diversa collocazione impostare
FOT_HARNESS_TEST_EVIDENCE alla cartella contenente EVIDENCE_MANIFEST.csv/EVALUATOR_INDEX.csv/units.
Non scaricare o rigenerare dati chiusi senza una necessità concreta del delta.

Attesi dall’esecutore: 82/82 mirati, 117/117 discovery; 14/14 riproduzioni applicabili
con wrapper RUN_APPLICABLE_ORIGINAL.py (12 metodi invariati, N20/N21 con sola fixture e
argomento nuovi). Le 50 prove originali sul respinto restano 32 metodi non conformi,
34 failure di assertion e 0 errori. Il guardiano è **35 test, stessi 14 fallimenti storici,
1 skip, 0 errori: non PASS**. Confronta gli identificativi in DOCUMENTATION_COMPARISON.json.

D9 è già approvata: 122B principale/consumer, 27B alternativo completo, Terra storico
interno. Non chiedere nuovamente i ruoli; non trasferire l’approvazione al preflight
storico non recepito. L’ordine label 1a resta pending. Nessun nuovo OK del raccordo viene
trasferito automaticamente a questo harness o al futuro delta D9.

## Consegna della review

Produci un verbale autonomo con modello/finestra realmente osservati, commit/tree/base,
prerequisiti, controlli per requisito, riproduzioni, log e impronte, limiti e rilievi puntuali.
Concludi OK oppure NON OK solo dopo le prove, limitando il verdetto al candidato esatto.
Mantieni originali e prove fuori dal tree candidato; consegna hash e inventario espliciti.

Nessuna scrittura sul candidato, copia principale, revisore precedente o lavori paralleli.
Nessun push, merge, tag, freeze, GO, chiamata API, inferenza o simulazione scientifica.
Nessuna modifica a piano, APERTURA, D9, walkthrough, A/B, FAR, U3 o freeze 03.9/03.12.
