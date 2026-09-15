from pathlib import Path
import subprocess,json,hashlib
W=Path('/Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review');E=W/'outputs/d9-corrections-review/evidence';S=Path('/Users/luker/fot-tep-harness-d9-correzioni');C=W/'work/corrections-candidate'
def git(*args):
 p=subprocess.run(['git','-C',str(S),*args],capture_output=True,text=True);return {'command':['git',*args],'code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r={}
for name,args in [('runtime_diff',['diff','6a8031b','16c98f3','--','*.py',':!studio2/fase03/harness/d9_corrections/*']),('documentary_delta',['diff','--name-status','16c98f3','cf763333']),('red_equivalence',['diff','--name-status','6a8031b','08670fb']),('diff_check_source',['diff','--check','08670fb','16c98f3','--','*.py','*.md']),('diff_check_all',['diff','--check','08670fb','16c98f3']),('history',['log','--format=%H %P %s','08670fb..cf763333'])]:r[name]=git(*args)
# Read-only evidence on open descriptors; a sample cannot prove a global absence of writers.
p=subprocess.run(['lsof','-nP','+D',str(S)],capture_output=True,text=True);r['lsof_sample']={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
r['process_sample']=subprocess.check_output(['ps','-axo','pid,ppid,etime,command']).decode()
r['ancestor_instructions']={str(p):p.read_text() for p in [Path('/AGENTS.md'),Path('/Users/AGENTS.md'),Path('/Users/luker/AGENTS.md'),S/'AGENTS.md'] if p.exists()}
legacy=Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output')
r['legacy_reference_inventory']={str(p.relative_to(legacy)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in legacy.rglob('*') if p.is_file()}
r['test_script_hashes']={name:sha(E/name) for name in ['test_d9_corrections.py','transport_boundary_regression.py','independent_probes.py','independent_correction_edges.py']}
for name,original in [('test_d9_corrections.py',C/'studio2/fase03/harness/test_d9_corrections.py'),('transport_boundary_regression.py',C/'studio2/fase03/harness/d9_corrections/transport_boundary_regression.py'),('independent_probes.py',W/'outputs/d9-review/evidence/independent_probes.py')]:assert sha(E/name)==sha(original)
(E/'source_audit.json').write_text(json.dumps(r,indent=2)+'\n')
print('source audit saved; legacy members',len(r['legacy_reference_inventory']),'source diff check',r['diff_check_source']['code'],'whole diff check',r['diff_check_all']['code'],'ancestor instructions',list(r['ancestor_instructions']))
