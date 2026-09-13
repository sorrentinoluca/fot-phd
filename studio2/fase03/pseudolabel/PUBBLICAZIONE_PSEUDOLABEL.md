# Pubblicazione della sotto-fase 03.7

Data: 2026-09-13. **Artefatti v1 verificati, integrati e tag pubblicato.**
La Fase 03 resta aperta; la compatibilità finale con 03.12 e il controllo dei
prompt reali competono alle sottofasi successive.

## Identità pubblicate e controlli

Il branch originale `codex/studio2-pseudolabel` termina a
`fdf06b82a35a92508a8de602a594adba44c08fe6`. Le rettifiche e la verifica sono nel
commit `f6d9aad`; la coppia walkthrough aggiornata è nel commit
`c16b533016db4617deb1ba96853253f117e8e32b`, integrato con fast-forward in `main`.
L’integrazione include la dipendenza 03.4 già presente nel main locale a `d815ce9`.

Dopo il push di `main`, `git ls-remote origin refs/heads/main` ha confermato
`c16b533016db4617deb1ba96853253f117e8e32b`. Il commit sorgente del freeze
`8c90ecec421980211258e9323d4266a32ba70ccd` è suo antenato ed è raggiungibile
da `origin/main`. Il verbale di verifica OK è incluso nella stessa storia.

Tag annotato pubblicato: `studio2-fase03-pseudolabel-frozen-001`.
Oggetto tag remoto: `6854c49b4034c16b8df3b11d45dd759a343463e2`;
commit peeled remoto: `c16b533016db4617deb1ba96853253f117e8e32b`.
Entrambi confermati con `git ls-remote` dopo il push del tag. Nessun tag
preesistente è stato spostato o sovrascritto.

Al commit integrato e poi taggato sono stati rieseguiti:

- `python3 -m studio2.fase03.pseudolabel.pseudolabel_draw --check`: quattro artefatti byte-identici;
- `python3 -m unittest studio2.fase03.pseudolabel.test_pseudolabel`: 21/21 OK;
- `python3 -m unittest discover -s studio2/fase03/tests`: 16/16 OK;
- controllo indipendente SHA-256 e dimensioni: 7/7 corrispondono al freeze originale;
- `git diff --check`: nessun errore.

`python3 docs/test_explanation.py` prima e dopo le modifiche documentali:
35 test, 14 fallimenti preesistenti e 1 skipped, stessi identificativi dei
fallimenti. Questa suite non copre la sottofase. Parità del testo integrale
aggiunto in §4.7 Markdown/HTML, stato iniziale, riga di sintesi e rinvio §6.5
verificata sul contenuto; i nuovi link locali risolvono.

## Stato dei documenti

`PSEUDOLABEL_FREEZE.json` resta immutato con lo stato storico
`frozen_pending_independent_verification`. Lo stato successivo è attestato
da `VERIFICA_PSEUDOLABEL.md`, dal tag pubblicato e da questo record:
non si riscrivono specifica, codice, test, log o impronte della versione v1.
Il report originale è stato rettificato con riesame indipendente delle correzioni;
i suoi SHA e quello della decisione sono registrati nel verbale.

`DECISIONE_ACCETTAZIONE_V1.md` conserva la decisione dell’autore: accettazione
post-osservazione del sorteggio unico, Spearman −5/6 dichiarato, limite del test
`|rho|<1` esplicito, nessun riordinamento compensativo. Non è una nuova
soglia statistica pre-specificata. Non sono state avviate inferenze o simulazioni.

## File modificati o aggiunti dopo il lavoro originale

- `studio2/fase03/pseudolabel/REPORT_PSEUDOLABEL.md`: rettifica di lunghezze, opacità, correlazione, prova di processo e interfaccia 03.12.
- `studio2/fase03/pseudolabel/DECISIONE_ACCETTAZIONE_V1.md`: decisione esplicita dell’autore e condizioni di integrazione.
- `studio2/fase03/pseudolabel/VERIFICA_PSEUDOLABEL.md`: riscontri indipendenti, riesame delle rettifiche e verdetto OK.
- `docs/fot_walkthrough_conversazione_studio2.md`: §4.7 e rinvii di stato.
- `docs/fot_walkthrough_conversazione_studio2.html`: contenuto allineato alla versione Markdown e voce di navigazione.
- `studio2/fase03/pseudolabel/PUBBLICAZIONE_PSEUDOLABEL.md`: questo record successivo al tag.

La sintesi divulgativa resta invariata: è preparazione interna, senza risultati
scientifici da sintetizzare. Piano, implementazione Q8 e artefatti del primo
studio non sono stati modificati. Non sono state incorporate modifiche delle
sottofasi soglie Normal, evidence, schema insight o piano statistico.

## Pulizia operativa

Il worktree originale era registrato al percorso non più esistente
`/sessions/rcw-014dgfyhavbra2ah4kmannp5/mnt/fot-tep/.worktrees/pseudolabel`.
È stato rimosso selettivamente con `git worktree remove`, senza prune globale.
Non si attesta la cancellazione fisica di una directory su un altro computer:
qui era presente solo il riferimento Git obsoleto. Rimossi anche i worktree
temporanei locali di revisione e integrazione pseudolabel; la copia temporanea
del verbale è stata confrontata byte per byte con quella pubblicata prima
della rimozione. Il worktree temporaneo di main viene rimosso dopo il push di
questo record e il controllo finale. I branch restano recuperabili.

Nessun file di lock è stato cancellato e nessun permesso aggiuntivo è stato
necessario. La copia di lavoro principale resta sul branch delle soglie Normal;
i suoi file non committati e i worktree degli altri cantieri sono preservati.
