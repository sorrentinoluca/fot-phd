# Comandi e riproduzione della review D9

Sede di lavoro dei comandi seguenti:
`/Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review`.
Non eseguirli nel repository originale. Dopo la ripresa la cwd della task è diventata
`/Users/luker/fot-tep`: ogni comando con scritture ha continuato a usare esplicitamente
la sede di review originaria.

## Identità e snapshot

I risultati esatti delle letture iniziali sono in identity_before.json. Operazioni:

```sh
git -C /Users/luker/fot-tep-harness-d9 status --porcelain=v1
git -C /Users/luker/fot-tep-harness-d9 rev-parse HEAD 'HEAD^{tree}' '6a8031b^{tree}'
git -C /Users/luker/fot-tep-harness-d9 branch --show-current
git -C /Users/luker/fot-tep-harness-d9 remote -v
git -C /Users/luker/fot-tep-harness-d9 worktree list --porcelain
git -C /Users/luker/fot-tep-harness-d9 archive 6a8031b25aa1208047d79cc7f030bf9cf7841e67
git -C /Users/luker/fot-tep-harness-d9 archive aae29a908356e4a4842a214fdc3db9bff26ec3ca
```

Gli stream tar sono stati salvati in work/candidate.tar e work/antecedent.tar ed
estratti rispettivamente in work/candidate e work/antecedent con tarfile.
Nessuna registrazione/mutazione di worktree Git. `gzip -c work/candidate.tar`
ha prodotto l'archivio candidato consegnato. Lo script audit_identity.py conserva
le verifiche di manifest, fonti, perimetro e impronte iniziali dei file tracciati.
Le letture ps e lsof sono osservazioni, non garanzia di esclusione concorrente.
`lsof -nP +D /Users/luker/fot-tep-harness-d9/studio2/fase03/harness` ha restituito
nessuna riga, exit1. Nessun contatto remoto eseguito per aggiornare origin/main.

## Suite richieste

Eseguito una volta ` /opt/anaconda3/bin/python3 work/run_suites.py` dalla sede
originaria. Copia dello script in questa cartella. Il launcher imposta
PYTHONDONTWRITEBYTECODE=1 e TMPDIR separato per ogni suite, poi esegue serialmente:

1. unittest mirata sugli undici moduli di COMANDI della preparatrice;
2. `python3 -m unittest discover -v studio2/fase03`;
3. `python3 -m unittest -v studio2.fase03.harness.test_d9`;
4. stesso file finale test_d9.py con FOT_D9_TARGET al nostro work/antecedent;
5. `python3 docs/test_explanation.py`.

Per tutte queste chiamate python3 è `/opt/anaconda3/bin/python3`.
Gli argv, cwd, exit code e durata sono nei rispettivi *_command.json; stdout+stderr
nei log omonimi. Per il confronto antecedente il launcher imposta anche
`FOT_D9_TARGET=/Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review/work/antecedent`;
questo valore non è duplicato dal primo schema env_overrides del record JSON,
ma è esplicito nel launcher e qui.

Alla ripresa dopo interruzione della conversazione, il launcher PID99546 e la
discovery figlia PID889 erano ancora attivi. resume_processes.txt ne conserva
il riscontro. Non sono state avviate copie delle suite né sovrascritti i log.

Le CLI piano sono riprodotte in cli_plans.json con --config puntato al config
pending dello snapshot: exit0,0,3. Nessun --execute in queste tre chiamate.
La compilazione usa compile(bytes,path,'exec') in memoria: compile_same_scope.json
copre gli stessi98 file della preparatrice; compile_independent.json conserva
la precedente selezione autonoma di79 file. Non sono esecuzioni di quei moduli.

## Sonde indipendenti

Comandi finali, dalla sede di review:

```sh
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 outputs/d9-review/evidence/independent_probes.py
FOT_D9_TARGET="$PWD/work/antecedent" PROBE_OUTPUT=probe_fixtures_antecedent PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 outputs/d9-review/evidence/independent_probes.py Independent.test_U04_positive_direct_reserve Independent.test_U05_missing_r4_snapshot_direct_reserve_must_refuse Independent.test_U06_missing_r4_snapshot_restart_reserve_must_refuse Independent.test_U07_missing_snapshot_ordinary_runner_refuses
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 outputs/d9-review/evidence/transport_snapshot_probe.py
```

I comandi sono stati rediretti ai log corrispondenti. Le copie fixture finali e
observations.json restano disponibili sotto probe_fixtures e
probe_fixtures_antecedent. La sonda transport conserva result.json e la fixture
con raw/journal. Gli script rifiutano sovrascritture dei risultati: per riprodurre
usare una nuova copia della sede o una nuova destinazione PROBE_OUTPUT.

independent_probes_initial.py/log documentano il primo lancio interrotto per
raccolta involontaria della classe RunnerRevisions importata. independent_probes_v1.py/log
conservano il primo run di soli8 metodi. I byte finali aggiungono scelta target e
osservazioni; assertion sostanziali invariate, rieseguite sul candidato e, per
U04–U07, sull'antecedente. Gli esiti intermedi non si sommano ai finali.

## Limiti delle fixture e recuperabilità

RunnerRevisions usa input development congelati ma risposte e contatori sintetici,
SDK fittizio e socket vietati; d9_offline_fixtures modifica soltanto il contesto di test,
con fonte storica0/0 e tokenizer fixture. D01 richiede il checkout legacy0c8157f
esterno già disponibile; le sue verifiche di identità/pulizia sono parte della suite.
Non sono stati copiati dati scientifici nel ledger reale o avviati servizi.

Le copie dei database/raw conservano i path assoluti temporanei originali, anche
quando la fixture è stata ripulita da unittest: sono prove forensi recuperabili,
non ledger riapprovati per esecuzione. Gli script rigenerano gli stessi scenari
in nuove directory. L'archivio del candidato permette di recuperare i byte;
le dipendenze legacy locali devono essere ripristinate esplicitamente in altro ambiente.
