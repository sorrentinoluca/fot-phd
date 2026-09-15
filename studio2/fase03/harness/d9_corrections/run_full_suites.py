from pathlib import Path
import subprocess,os,json,time,hashlib,platform,sqlite3,sys
root=Path('/Users/luker/fot-tep-harness-d9-correzioni'); ev=root/'studio2/fase03/harness/d9_corrections/results'
modules=['studio2.fase03.harness.'+m for m in ('test_c01_c03','test_d01_replay','test_d02_predecessors','test_d03_contract','test_d04_open_quota','test_d9','test_d9_corrections','test_harness_offline','test_metric_raccordo','test_revisions')]+['studio2.fase03.tests.test_execution_guard','studio2.fase03.tests.test_protocol']
commands={'targeted':['-m','unittest','-v']+modules,'discovery':['-m','unittest','discover','-v','studio2/fase03']}
paths=subprocess.check_output(['git','ls-files','--','*.py'],cwd=root,text=True).splitlines()
record={'python':sys.version,'platform':platform.platform(),'sqlite':sqlite3.sqlite_version,'executed_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'python_inventory_scope':'tracked Python files, not a claim each was executed','files':[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in paths]}
(ev/'TESTED_BYTES.json').write_text(json.dumps(record,indent=2)+'\n')
runs=[]
for name,args in commands.items():
 cmd=[sys.executable]+args;f=(ev/(name+'.log')).open('w');p=subprocess.Popen(cmd,cwd=root,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=f,stderr=subprocess.STDOUT);f.close();runs.append((name,p,time.monotonic(),cmd));print(name,p.pid,flush=True)
for name,p,start,cmd in runs:
 result={'command':cmd,'cwd':str(root),'exit_code':p.wait(),'elapsed_seconds':time.monotonic()-start}
 (ev/(name+'_command.json')).write_text(json.dumps(result,indent=2)+'\n');print(name,result['exit_code'],flush=True)
