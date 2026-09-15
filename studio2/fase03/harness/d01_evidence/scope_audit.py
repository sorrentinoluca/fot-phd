from pathlib import Path
import hashlib,json,subprocess,os,sys,sqlite3
from datetime import datetime,timezone
root=Path('/Users/luker/fot-tep-harness-0310-d01');out=Path('/Users/luker/fot-tep-harness-0310-d01-checks');base='52e13e1ed540e1ad076474398bf850445c9a4a00';acquisition='89b016a728bdbf5d2d8b438416e6133b050683da'
git=lambda *args:subprocess.check_output(['git','-C',str(root),*args],text=True)
(out/'scope_initial_issue.json').write_text(json.dumps(dict(issue='initial local audit used documentary base to allowlist only code delta and therefore included already authorized acquisition paths; assertion stopped before protected-file/compile checks',classification='audit setup error, not candidate defect',resolution='separate acquisition and technical diff bases; inventory verifies acquisition independently'),indent=2)+'\n')
changed=git('diff','--name-only',acquisition).splitlines()
allowed={'studio2/fase03/harness/ledger.py','studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md'}
assert set(changed)<=allowed,changed
paths=['studio2/fase03/harness/'+n for n in ['metric_adapter.py','metrics.py','test_metric_raccordo.py','runtime.py','gate_rules.py','test_c01_c03.py']]+['studio2/fase03/producer_probe.py','studio2/fase03/run_pilot.py']
for directory in ['studio2/fase03/schema_insight','studio2/fase03/pseudolabel','studio2/fase03/baseline_numerica','studio2/fase03/piano_statistico','docs']:
 paths+=git('ls-tree','-r','--name-only',base,'--',directory).splitlines()
protected=[]
for p in paths:
 b=(root/p).read_bytes();assert subprocess.check_output(['git','-C',str(root),'show',base+':'+p])==b,p
 protected.append(dict(path=p,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
(out/'scope.json').write_text(json.dumps(dict(base=base,technical_diff_base=acquisition,protected_files_unchanged=protected,only_live_runtime_delta='studio2/fase03/harness/ledger.py',scientific_execution=False),indent=2)+'\n')
files=[p for p in (root/'studio2/fase03').rglob('*.py') if not any(x.startswith('non_ok') or x.endswith('_evidence') for x in p.parts)]
for p in files:compile(p.read_bytes(),str(p),'exec')
(out/'compile.json').write_text(json.dumps(dict(live_files=len(files),syntax_errors=0,exclusions='forensic acquisitions and evidence folders'),indent=2)+'\n')
(out/'runtime.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),python=sys.version,sqlite=sqlite3.sqlite_version,thread_id=os.environ.get('CODEX_THREAD_ID'),role='implementation; same preparer task',model_effort='previous turn attested by acquired review as gpt-6-astra/xhigh; current turn not independently re-attested'),indent=2)+'\n')
print('Scope:',len(protected),'unchanged files; compile:',len(files))
