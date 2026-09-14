# Verifica indipendente del nuovo delta 03.15 — candidato 91a880b

Verifica il delta redazionale della sotto-fase 03.15, studio 2 FoT-TEP, e la coerenza
risultante delle sezioni del paper. Non riscrivere le bozze mentre le verifichi.
Non ripetere la review storica del pacchetto cf79e81: il suo OK resta acquisito e
limitato al suo contenuto. Il nuovo delta non eredita quell'OK.

## Identificazione richiesta prima della review

Documenta **effettivamente**, usando i metadati a cui hai accesso:

- modello e versione/ID completo;
- provider;
- reasoning/effort, se esposto; altrimenti «non esposto»;
- ID della task/finestra, sessione e ruolo del revisore;
- worktree effettivamente usato, branch/detached HEAD e commit;
- fonte di queste identificazioni e limiti di accesso ai metadati.

Non dedurre l'identità dallo stile o dal nome «Codex/Claude». Se un campo non è
verificabile, dichiaralo. Esecutore noto: **OpenAI gpt-6-astra, high**, task
`01a0a0bb-1683-7dd0-b29b-edfffb83de56`, agente `/root`. Usa un'altra sessione e
preferibilmente un altro modello; rendi esplicito il grado di indipendenza ottenuto.
Una rilettura dell'esecutore non è una verifica indipendente.

## Candidato e consegna da usare

Repository: `/Users/luker/fot-tep`.
Worktree dell'esecutore, da non modificare: `/Users/luker/fot-tep-paper-sections`.
Branch sorgente: `codex/studio2-paper-sections`; non usare il suo HEAD come candidato implicito.

| Oggetto | Commit completo |
| --- | --- |
| Storico scientifico OK | `cf79e81f917c7969dfd375e38db54315c28d4c07` |
| Acquisizione verbale | `50f07a998afb87b832aab6653c9241c69ac3b020` |
| Base di ingresso nuova attività | `1d480fd62ff72c4bc5e60df6ffb46ee36f58151a` |
| Commit documentale e base immediata scientifica | `bcb462da3f3c329af5b80d9cb028bb8893a8d09d` |
| **Candidato da verificare** | **`91a880b136dee5d805b54040f5e32345be361eb2`** |

Il report e i controlli sono documenti successivi al candidato, nel commit locale
di consegna indicato dall'esecutore. Leggili come oggetti della verifica, non come
fonti sufficienti per approvare le affermazioni:

- `/Users/luker/fot-tep-paper-sections/studio2/fase03/paper_sections/REPORT_DELTA_0315.md`;
- `/Users/luker/fot-tep-paper-sections/studio2/fase03/paper_sections/CONTROLLI_DELTA_0315.json`;
- il presente prompt.

SHA-256 atteso del report consegnato:
`1f59eabf8070f1f4b7b77d89564d4e3593308469e8d8aee56676c93dbabd40f1`.
Se la copia sul disco è avanzata, recupera il blob dal commit di consegna indicato
in chat e confronta l'impronta, senza sostituirlo con un nuovo report implicito.

Prima delle scritture verifica stato, worktree, modifiche preesistenti, branch/HEAD,
`origin/main` e `git ls-remote origin refs/heads/main`. Il preflight dell'esecutore
ha registrato entrambi i main a `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`.
Un avanzamento successivo non cambia il candidato o le fonti identificate.
Usa un worktree detached isolato al candidato esatto, per esempio, se il percorso è libero:

```bash
git -C /Users/luker/fot-tep worktree add --detach /Users/luker/fot-tep-verifica-delta-0315-91a880b 91a880b136dee5d805b54040f5e32345be361eb2
```

Se il percorso è occupato, scegli un nuovo percorso isolato e registralo. Non fare
checkout, pulizia o correzioni nei worktree altrui, soprattutto nel raccordo seriale
03.6→03.12→letteratura. Nessun merge in main, push o tag.

## Letture e perimetro

Leggi MAINTENANCE §§1–2, 5, 8.2–8.6 e i prompt pertinenti in `docs/prompts/`,
quindi handoff rev02, record/report di acquisizione, verbale storico e report del
nuovo delta. Il verbale storico deve restare byte-identico: 13.949 byte,
SHA-256 `8faca80c87071d87bf66d97848c290a5724f6569be6f6040cfb6568bad022cb1`.
Controlla la conservazione del NON OK precedente, senza riaprire la sua review.

Nel candidato leggi `FONTI_DELTA_0315.json`: 54 fonti con commit/path/SHA-256.
Leggi le fonti primarie pertinenti a ogni nuova frase della matrice, con `git show
<commit-esatto>:<path>`, non da HEAD mobili. In particolare:

- S05/S09 a `c486eee`: consegna 03.5, freeze, FAR, decisione autore; specifiche
  normal_dev/baseline, audit, accettazione, prototipi, manifest, handoff, consegna
  03.9, rev. 3 e prova di riscaricamento;
- S08 a `6aaa5b3`: piano rev. 10, atto non firmato, addendum/approvazione, budget;
  S08-consegna a `51782e8`: consegna e verbale;
- S06 a `c66bd8d`: dipendenze/U3, evidence-v2 e sorgenti; S12 a `3c64390`: schema R4;
- L a `40911d0`: corpus, addendum PHM e verbale bibliografico per i raccordi;
- H, handoff `/Users/luker/fot-tep/studio2/fase03/HANDOFF_FASE03_2026-09-14_rev02.md`,
  per disponibilità dichiarata e D9, verificandone l'impronta. È non tracciato:
  non inventare un commit o una qualificazione tecnica del servizio.

Puoi ricontrollare le impronte Git in sola lettura dal worktree isolato:

```python
import hashlib, json, pathlib, subprocess
p = pathlib.Path('studio2/fase03/paper_sections/FONTI_DELTA_0315.json')
for r in json.loads(p.read_text())['sources']:
    b = (subprocess.check_output(['git', 'show', r['commit'] + ':' + r['path']])
         if r['commit'] else pathlib.Path(r['path']).read_bytes())
    assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256'], r
```

Delta scientifico: **bcb462d..91a880b**, otto file identificati nel report.
Correzione documentale: **1d480fd..bcb462d**, solo «figlio diretto».
Controlla anche le cinque sezioni complete risultanti e la mappa per contraddizioni
introdotte dall'allineamento. Le parti storiche non toccate servono come contesto,
non come invito a ripetere la review su cf79e81.

## Controlli scientifici richiesti

1. **normal_dev reale e provenienza:** 40 run preassegnati, cinque/agente,
   320 finestre ma 40 cluster; stream/configurazione/data sostenuti; sviluppo esclusivo,
   divieti corretti; deviazioni accettate non trasformate in conformità. Evidence nella
   destinazione normal_dev_002, otto esempi pre-specificati. S09 integrata/pubblicata,
   freeze inefficace nello snapshot e residui distinti.
2. **Baseline numerica:** 9 globali+16 locali, 697-D, media aritmetica, L1 media,
   pareggio entro 1e-12 con astensione, nessun ripiego globale o soglia di distanza.
   Scarto dei vettori riportato come controllo storico, non nuova performance.
   U3/N1–N5/soglie V2 e rigenerazione se R2 decade; nessun uso dei blocchi legacy
   come osservazioni Normal di sviluppo. Non rigenerare prototipi/evidence.
3. **03.5 chiusa:** numero/rango/regola della soglia, FAR e intervalli distinti su
   fonti JSON; freeze prima dell'apertura analitica registrata, accessibilità precedente
   e limite accettato. Nessuna riapertura FAR, ricalibrazione o nuova inferenza statistica.
4. **Rev. 10:** D2, H1/H2 Hoeffding, H3 Tango, m=0,125, α=0,05 e sensibilità H3 0,025,
   gerarchia, guadagnati/persi/saldo, D11 e R approvati; firma/freeze distinti.
   Non trasformare la garanzia H1/H2 in garanzia di potenza/indipendenza o Tango
   in test esatto. Controlla denominatori di astensione e invalidità.
5. **A e contabilità:** formula completa, nucleo 1.728/5.184 distinto dal totale,
   E5 R=1, audit senza doppio conteggio, canary/giorni, librerie/FULL, pilot, X/Q;
   tutte le richieste per identità effettiva del modello. Margine temporale 20%,
   sospensione organizzativa se non fattibile, nessun tetto vigente 3.700,
   ampliamento automatico della finestra, riduzione del disegno o NO-GO scientifico.
   Riserva/remediation, triplette, zero token, gate senza retry e hard stop 200 coerenti.
6. **B e OOD:** candidati/criteri/catene prima dei run, controlli tecnici 03.11
   dopo il freeze statistico e prima delle chiamate; F6/F4 condizionati e due
   catene intatte; verifiche proprie dei sostituti e distinzione degli OOD,
   sospensione se collisione su F5; nessun ritorno al ciclo 03.8→03.11→03.8.
7. **D9 e paper:** 122B dichiarato operativo, identità completa/qualificazione aperte;
   nessuna assegnazione autonoma di ruoli a 27B/122B/Terra. Producer-swap e alternativo
   D9.1 ancora da decidere preservati. Otto fault opachi, Normal letterale, Unknown
   solo astensione; Normal senza insight. Nessuna trasformazione dello storico Terra
   in braccio controllato, nessun risultato diagnostico, abstract o conclusione.
   Provenienza interna e descrizione del riuso rispettano MAINTENANCE.
8. **Raccordi e perimetro:** modifiche a method/threats/mappa/annotazione related_work
   strettamente necessarie e sostenute; fonti bibliografiche disponibili al pin L
   senza dichiararle già integrate nel branch. Walkthrough, corpus, artefatti
   congelati, verbale indipendente e risultati storici preservati.

## Test e output della verifica

Esegui il lint delle cinque sezioni e `git diff --check bcb462d..91a880b`.
Esegui il guardiano sulla base in copia isolata e sul candidato:

```bash
python3 studio2/fase03/paper_sections/lint_paper_sections.py --corpus docs/letteratura.md
python3 docs/test_explanation.py
```

Atteso dichiarato, da verificare: lint 5 file/0 segnalazioni; guardiano 35 test,
14 fallimenti preesistenti, 1 skip, 0 errori. Confronta **identificativi e parametri
dei subtest**, non il solo numero: il preambolo e l'elenco dei fallimenti del
preparatore sono in `CONTROLLI_DELTA_0315.json`. Questi test non provano il merito
scientifico: verifica manualmente riferimenti, numeri e coerenza sulle fonti.
Non lanciare test che effettuano nuove simulazioni, Monte Carlo, inferenze o API;
non rigenerare FAR/bootstrap, lotti, evidence o prototipi.

Per ogni controllo riporta ✅ verificato, ⚠️ limite/non verificabile, ❌ smentito,
con fonte e localizzatore. Poi concludi **OK** oppure **NON OK** sul solo nuovo
delta e sulla coerenza risultante. Se NON OK, rilievi puntuali con file/righe,
fonte, conseguenza e correzione richiesta; non applicare le correzioni mentre
certifichi. Gli arretrati storici invariati vanno distinti dalle regressioni nuove.

Scrivi esclusivamente un nuovo verbale `VERIFICA_DELTA_0315.md` nella cartella
`studio2/fase03/paper_sections/` del tuo worktree isolato, con verdetto in prima
riga, identità effettiva completa, commit e fonti/impronte, test, limiti e perimetro.
Eventuali log vanno in un supporto esterno identificato. Non sovrascrivere
`VERIFICA_PAPER_SECTIONS.md` né modificare candidato, walkthrough o fonti.
Nessun commit/merge/push/tag, simulazione o chiamata sperimentale. Consegna percorso,
SHA-256 del verbale e verdetto. Un eventuale OK non chiude 03.15 o Fase 03, non
firma la rev. 10, non sceglie D9 e non autorizza pilot o pubblicazione.
