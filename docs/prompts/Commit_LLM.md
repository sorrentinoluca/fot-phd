# Commit — studio 2 FoT-TEP

**Le regole stanno in `docs/MAINTENANCE.md` §8** (perimetro, riuso, commit, congelamenti,
verificabilità). Leggile e applicale: qui non sono ripetute. Leggi anche
`docs/fot_walkthrough_conversazione_studio2.md` §0 per le fonti autorevoli.

**Non eseguire push né merge** senza una richiesta esplicita.

Procedi così:

1. **Stato corrente.** Branch, commit, tag, file tracciati, esclusioni, modifiche non committate.
   Identifica il lavoro preesistente **prima** di intervenire: in questo repository capita che più
   sessioni lavorino insieme. Se un `.git/index.lock` da 0 byte blocca l'operazione e nessun
   processo git è attivo, rimuovilo.
2. **Controlli di MAINTENANCE prima dei commit**, non dopo: §5 per la definizione di «fatto», §8.3
   per la separazione dei commit, e le coppie MD/HTML di §3 sempre nello stesso commit.
3. **Selezione esplicita dei file.** Niente modifiche estranee trascinate dentro. Se un file
   contiene cambiamenti che appartengono a commit diversi e non si separano in modo pulito,
   **dillo** e proponi un commit unico con la motivazione, invece di tagliare a caso.
4. **Messaggi** `studio2(<ambito>): <azione concreta>`. Il corpo dice *cosa* è cambiato e *perché*,
   non come.
5. **Nessun tag di congelamento** se i controlli previsti non sono stati eseguiti (§8.4).
6. **Includi report e verifica.** `studio2/fase<N>/REPORT_FASE<N>.md` e
   `studio2/fase<N>/VERIFICA_FASE<N>.md` entrano nel commit: sono la traccia di che cosa è stato
   fatto e di chi lo ha verificato in modo indipendente. Per una sotto-fase, il file atteso è
   `studio2/fase<N>/<SOTTOFASE>/REPORT_<SOTTOFASE>.md` e `VERIFICA_<SOTTOFASE>.md`; la verifica di
   fase, invece, verifica coerenza fra sotto-fasi senza rifare controlli già fatti nelle singole
   sotto-fasi.
   Se manca il file di verifica, dillo e non committare l'aggiornamento del walkthrough.

Al termine riporta: i commit creati, i file inclusi in ciascuno, le verifiche svolte con i loro
esiti, le modifiche lasciate fuori con il motivo, e le decisioni ancora necessarie.

7. **Fase chiusa e consegna.** Una sotto-fase non chiude la fase ai fini di consegna. Una fase si considera chiusa solo se **report e verifica** della fase sono committati e presenti in `origin/main` (non basta che siano in locale). L'integrazione di una sotto-fase in `main` è ammessa su richiesta dell'autore; la fase successiva parte da `origin/main` solo dopo la chiusura di fase.
   La fase non è considerata consegnata se i suoi dati voluminosi non sono pubblicati su `fot-tep-data`
   e verificati tramite riscaricamento degli asset.
