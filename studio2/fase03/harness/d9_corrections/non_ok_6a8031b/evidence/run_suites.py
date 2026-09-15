import subprocess,pathlib,os,json,time,sys
root=pathlib.Path.cwd(); ev=root/'outputs/d9-review/evidence'; candidate=root/'work/candidate'
mods=['harness.'+x for x in ['test_c01_c03','test_d01_replay','test_d02_predecessors','test_d03_contract','test_d04_open_quota','test_d9','test_harness_offline','test_metric_raccordo','test_revisions']]+['tests.test_execution_guard','tests.test_protocol']
runs=[('targeted',['-m','unittest','-v']+['studio2.fase03.'+x for x in mods]),('discovery',['-m','unittest','discover','-v','studio2/fase03']),('d9',['-m','unittest','-v','studio2.fase03.harness.test_d9']),('antecedent',[str(candidate/'studio2/fase03/harness/test_d9.py'),'-v']),('guardian',['docs/test_explanation.py'])]
for name,args in runs:
 env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
 tmp=ev/('tmp_'+name);tmp.mkdir(exist_ok=True);env['TMPDIR']=str(tmp)
 if name=='antecedent':env['FOT_D9_TARGET']=str(root/'work/antecedent')
 argv=['/opt/anaconda3/bin/python3']+args;t=time.time()
 with (ev/(name+'.log')).open('w') as f:r=subprocess.run(argv,cwd=candidate,env=env,stdout=f,stderr=subprocess.STDOUT)
 record={'argv':argv,'cwd':str(candidate),'env_overrides':{k:env[k] for k in ['PYTHONDONTWRITEBYTECODE','TMPDIR']},'exit':r.returncode,'seconds':time.time()-t}
 (ev/(name+'_command.json')).write_text(json.dumps(record,indent=2));print(name,record['exit'],flush=True)
