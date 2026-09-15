from pathlib import Path
import os,subprocess,time,json,re,hashlib
W=Path('/Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review');E=W/'outputs/d9-corrections-review/evidence';C=W/'work/corrections-candidate';R=W/'work/candidate';PY='/opt/anaconda3/bin/python3';H=C/'studio2/fase03/harness/d9_corrections'
summary={}
def run(name,cmd,target,extra={}):
 tmp=W/'work'/('tmp-correction-'+name);tmp.mkdir(exist_ok=False)
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(tmp),'FOT_D9_TARGET':str(target),**extra}
 started=time.time();record={'command':cmd,'cwd':str(target),'environment_overrides':{k:env[k] for k in ('PYTHONDONTWRITEBYTECODE','TMPDIR','FOT_D9_TARGET')},'extra_environment':extra,'started_epoch':started}
 with (E/(name+'.log')).open('xb') as log:p=subprocess.run(cmd,cwd=target,env=env,stdout=log,stderr=subprocess.STDOUT)
 s=(E/(name+'.log')).read_text();record.update(exit_code=p.returncode,elapsed_seconds=time.time()-started,summary=s[s.rfind('\nRan '):].strip());summary[name]=record
 (E/(name+'_command.json')).write_text(json.dumps(record,indent=2)+'\n');(E/'TEST_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n');print(name,record['summary'],flush=True)
for name in ('targeted','discovery'):
 run(name,json.loads((H/'results'/(name+'_command.json')).read_text())['command'],C)
for color,target in [('red',R),('green',C)]:
 run('corrections_'+color,[PY,str(E/'test_d9_corrections.py')],target)
 run('original_U_'+color,[PY,str(E/'independent_probes.py')],target,{'PROBE_OUTPUT':str(E/('fixtures_U_'+color))})
 run('transport_'+color,[PY,str(E/'transport_boundary_regression.py')],target,{'TRANSPORT_RESULTS':str(E/('transport_'+color))})
for name,target in [('guardian_rejected',R),('guardian_corrected',C)]:run(name,[PY,'docs/test_explanation.py'],target)
