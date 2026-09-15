from pathlib import Path
import hashlib,json,subprocess,os,sys,sqlite3
from datetime import datetime,timezone
root=Path('/Users/luker/fot-tep-harness-0310-d02');out=Path(__file__).resolve().parent;base='7afbf41632aa8117c85274b5f471abca0a655462';acquisition='5b45cdcabe40aa64b0aecd1b5fe9d09c92ce5bb4'
git=lambda *args:subprocess.check_output(['git','-C',str(root),*args],text=True)
changed=git('diff','--name-only',acquisition).splitlines()
allowed={'studio2/fase03/harness/ledger.py','studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md','studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json'}
assert set(changed)<=allowed,changed
paths=['studio2/fase03/harness/'+n for n in ['metric_adapter.py','metrics.py','test_metric_raccordo.py','runtime.py','gate_rules.py','test_c01_c03.py','test_d01_replay.py']]+['studio2/fase03/producer_probe.py','studio2/fase03/run_pilot.py']
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
rollout=Path('/Users/luker/.codex/sessions/2026/09/15/rollout-2026-09-15T00-23-30-01a0a204-abda-7a00-8466-f52f5bc84812.jsonl')
turns=[]
for line in rollout.open():
 j=json.loads(line)
 if j.get('type')=='turn_context':
  p=j['payload']; turns.append(dict(timestamp=j.get('timestamp'),model=p.get('model'),effort=p.get('effort')))
(out/'runtime.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),python=sys.version,sqlite=sqlite3.sqlite_version,thread_id='01a0a204-abda-7a00-8466-f52f5bc84812',role='implementation, not independent review',rollout=str(rollout),last_turn_context=turns[-1],prior_reviewer='01a0a1ec-35a4-7870-9c39-9bf922d36c85 / gpt-6-astra / high',model_diversity=False),indent=2)+'\n')
print('Scope:',len(protected),'unchanged files; compile:',len(files));print(turns[-1])
