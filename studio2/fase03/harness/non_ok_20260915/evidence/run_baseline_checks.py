import subprocess, json, os, pathlib, time
root=pathlib.Path(__file__).resolve().parent.parent
cwd=root/'candidate'; out=root/'evidence'
env=dict(os.environ, PYTHONPYCACHEPREFIX=str(out/'pycache'))
commands={
 'targeted':['python3','-m','unittest','-v','studio2.fase03.harness.test_harness_offline','studio2.fase03.harness.test_metric_raccordo','studio2.fase03.tests.test_execution_guard','studio2.fase03.tests.test_protocol'],
 'discovery':['/opt/anaconda3/bin/python3','-m','unittest','discover','-v','studio2/fase03'],
 'compileall':['python3','-m','compileall','-q','studio2/fase03'],
 'diff_check':['git','diff','--check','a00605862f627710347bd63c49f79a6d0a00135f..59b6b93cd9c215e8b687e540f7cd579804b7c66a'],
 'documentation':['python3','docs/test_explanation.py']}
results={}
for name,cmd in commands.items():
 start=time.monotonic()
 r=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (out/(name+'.log')).write_text(r.stdout)
 results[name]={'command':cmd,'returncode':r.returncode,'seconds':time.monotonic()-start,'tail':r.stdout[-1200:]}
 print(name,r.returncode,r.stdout[-250:],flush=True)
(out/'baseline_checks.json').write_text(json.dumps(results,indent=2))
