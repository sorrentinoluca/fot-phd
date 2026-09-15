from pathlib import Path
import os,shutil,subprocess,json
K=Path(__file__).resolve().parent;W=Path('/Users/luker/fot-tep-harness-0310-d02');E=Path('/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence');env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');py='/opt/anaconda3/bin/python3'
commands=[]
for label,scripts in [('y_original',['edge_probes.py']),('literal',['extended_probes.py','additional_edges.py']),('x23_adapted',['additional_edges.py'])]:
 q=K/label;(q/'evidence').mkdir(parents=True);(q/'candidate').symlink_to(W,target_is_directory=True)
 for name in scripts:
  src=E/label/'evidence'/name;dst=q/'evidence'/name;shutil.copyfile(src,dst);assert src.read_bytes()==dst.read_bytes()
  cmd=[py,str(dst)];commands.append(dict(cwd=str(W),argv=cmd,log=str(q/(name+'.console.log'))))
cmd=[py,str(W/'studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py'),'--candidate',str(W),'--original','/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.py','--reference','/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference','--sandbox',str(K/'applicable')]
commands.append(dict(cwd=str(W),argv=cmd,log=str(K/'applicable.console.log')))
(K/'extension_commands.json').write_text(json.dumps(commands,indent=2)+'\n')
# Independent scripts run as processes and never touch a previous evidence directory.
procs=[]
for cmd in commands:
 f=open(cmd['log'],'w');procs.append((subprocess.Popen(cmd['argv'],cwd=W,env=env,stdout=f,stderr=subprocess.STDOUT),f,cmd))
for p,f,cmd in procs:
 cmd['exit_code']=p.wait();f.close()
(K/'extension_commands.json').write_text(json.dumps(commands,indent=2)+'\n')
print([(Path(c['argv'][1]).name,c['exit_code']) for c in commands])
