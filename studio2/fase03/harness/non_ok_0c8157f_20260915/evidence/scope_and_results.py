"""Exact-source scope, tests/method coverage and documentary comparison."""
from pathlib import Path
import ast,json,hashlib,subprocess,re,collections
E=Path(__file__).resolve().parent;C=E.parent/'candidate'
def git(*args):return subprocess.check_output(['git','-C',str(C),*args])
def sha(b):return hashlib.sha256(b).hexdigest()
tech='0c8157f23bee49a3a5a2df648525c34706da29d7';old='59b6b93cd9c215e8b687e540f7cd579804b7c66a';acq='ec012911444de6baf1751ae4bf4aee8e9c24adbb'
paths=git('diff','--name-only',acq,tech).decode().splitlines()
protected=['docs','phase_b','code','icl','ablation','studio2/fase03/piano_statistico','studio2/fase03/pseudolabel','studio2/fase03/schema_insight','studio2/fase03/baseline_numerica','studio2/fase03/soglie_normal','studio2/fase03/APERTURA_SOTTOFASI_FASE03.md','studio2/fase03/config/pilot_preflight.json','studio2/fase03/harness/PILOT_INPUT_SOURCES.pending.json','studio2/fase03/harness/metric_adapter.py','studio2/fase03/harness/metrics.py','studio2/fase03/harness/test_metric_raccordo.py']
scope={p:git('diff','--name-only',old,tech,'--',p).decode().splitlines() for p in protected}
assert all(not x for x in scope.values())
def methods(text):
    return sorted(n.name+'.'+f.name for n in ast.parse(text).body if isinstance(n,ast.ClassDef) for f in n.body if isinstance(f,ast.FunctionDef) and f.name.startswith('test_'))
method_changes={}
for p in paths:
    if Path(p).name.startswith('test_') and p.endswith('.py'):
        new=methods((C/p).read_text())
        try:before=methods(git('show',old+':'+p).decode())
        except subprocess.CalledProcessError:before=[]
        method_changes[p]=dict(before=len(before),after=len(new),removed=sorted(set(before)-set(new)),added=sorted(set(new)-set(before)))
doc=(E/'documentation.log').read_text()
failure_ids=[l.removeprefix('FAIL: ') for l in doc.splitlines() if l.startswith('FAIL: ')]
declared=json.loads((C/'studio2/fase03/harness/correzioni_evidence/DOCUMENTATION_COMPARISON.json').read_text())
original=(Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence')/'documentation.log').read_text()
original_ids=[l.removeprefix('FAIL: ') for l in original.splitlines() if l.startswith('FAIL: ')]
comparison=dict(tests=35,failure_assertions=len(failure_ids),errors=len(re.findall('^ERROR:',doc,re.M)),skips=1,ids_match_declared=sorted(failure_ids)==sorted(declared['failure_ids']),ids_match_original=sorted(failure_ids)==sorted(original_ids),failure_ids=failure_ids)
assert comparison['ids_match_declared'] and comparison['ids_match_original']
source=Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.json')
first=json.loads(source.read_text());reproduced=json.loads((C/'studio2/fase03/harness/correzioni_evidence/reproduced_non_ok.json').read_text())
prior_comparison=dict(original_tests=first['tests'],reproduced_tests=reproduced['tests'],original_failures=len(first['failures']),reproduced_failures=len(reproduced['failures']),same_failed_method_ids=first['failed_methods']==reproduced['failed_methods'])
syntax=[];imports=[]
for p in C.joinpath('studio2/fase03').rglob('*.py'):
    if 'non_ok_20260915' in p.parts:continue
    s=p.read_text();compile(s,str(p),'exec');syntax.append(str(p.relative_to(C)))
    for n in ast.walk(ast.parse(s)):
        if isinstance(n,ast.ImportFrom) and n.module and n.module.startswith('phase_b'):imports.append([str(p),n.lineno,n.module])
        elif isinstance(n,ast.Import):
            imports.extend([str(p),n.lineno,a.name] for a in n.names if a.name.startswith('phase_b'))
manifest=json.loads((E/'CONSEGNA_CORREZIONI_HARNESS_03_10.json').read_text())
document_hashes=[]
for r in manifest['documentary_files']:
    b=(E/Path(r['path']).name).read_bytes();document_hashes.append(dict(path=r['path'],sha256=sha(b),bytes=len(b),ok=sha(b)==r['sha256'] and len(b)==r['bytes']))
result=dict(technical_changed_paths=len(paths),diff_stat=git('diff','--shortstat',acq,tech).decode().strip(),protected_unchanged=scope,test_method_changes=method_changes,documentation=comparison,prior_reproduction_comparison=prior_comparison,syntax_checked_files=syntax,phase_b_imports=imports,documentary_members=document_hashes)
(E/'scope_and_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('syntax_checked_files','protected_unchanged','test_method_changes')},indent=2))
