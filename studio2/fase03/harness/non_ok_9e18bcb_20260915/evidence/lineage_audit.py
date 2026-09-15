from pathlib import Path
import json,hashlib,subprocess,ast,re,collections
E=Path(__file__).resolve().parent;C=E.parent/'candidate';O=Path('/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/evidence')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(C),*a])
prior=json.loads((O/'integrity.json').read_text());checks=[]
for r in prior['checks']:
 k=r['kind']
 if k.startswith('exact-source-'):
  b=git('show',r['path']);actual=sha(b);assert actual==r['expected_sha256'];checks.append(dict(kind=k,path=r['path'],sha256=actual,bytes=len(b),ok=True))
 elif k=='original-preserved':
  b=Path(r['path']).read_bytes();actual=sha(b);assert actual==r['expected_sha256'];checks.append(dict(kind=k,path=r['path'],sha256=actual,bytes=len(b),ok=True))
 elif k=='module-provenance':
  p=r['path'];b=(C/p).read_bytes();current=sha(b);old=sha(git('show','0c8157f23bee49a3a5a2df648525c34706da29d7:'+p));source=sha(git('show','1ac06ebdc92f73d3b630ccca9bf75f413bea170b:'+p))
  assert current==old==r['new_sha256'];assert source==r['source_sha256'];checks.append(dict(kind=k,path=p,source_commit='1ac06ebdc92f73d3b630ccca9bf75f413bea170b',source_sha256=source,current_sha256=current,unchanged_since_0c8157f=True,identical_to_recovery=current==source,ok=True))
 elif k=='remote-tag':
  remote=git('ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/tags/'+r['path'],'refs/tags/'+r['path']+'^{}').decode();assert remote==r['remote'];checks.append(dict(kind=k,path=r['path'],remote=remote,ok=True))
syntax=[];badimports=[]
for p in sorted((C/'studio2/fase03').rglob('*.py')):
 if any(x in p.parts for x in ('non_ok_20260915','non_ok_0c8157f_20260915','correzioni_evidence','c01_c03_evidence')):continue
 t=ast.parse(p.read_text());compile(t,str(p),'exec');syntax.append(str(p.relative_to(C)))
 for n in ast.walk(t):
  names=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module or ''] if isinstance(n,ast.ImportFrom) else []
  if any(n=='phase_b' or n.startswith('phase_b.') for n in names):badimports.append(str(p))
assert not badimports
doc=(E/'documentation.log').read_text();before=(O/'documentation.log').read_text();ids=lambda s: sorted(re.findall(r'^FAIL: (.+)$',s,re.M));assert ids(doc)==ids(before);assert len(ids(doc))==14
protected=json.loads((O/'scope_and_results.json').read_text())['protected_unchanged'];scope={p:git('diff','--name-only','6268437b8b64288b50ad5f7c924e1fcab85b27d3','HEAD','--',p).decode() for p in protected};assert all(not s for s in scope.values())
out=dict(checks=checks,counts=dict(collections.Counter(r['kind'] for r in checks)),compiled_live_files=syntax,forbidden_imports=badimports,documentation=dict(tests=35,failures=14,skips=1,failed_ids=ids(doc),same_ids_as_prior=True,status='NON PASS'),protected_scope=scope)
(E/'lineage_integrity.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),counts=out['counts'],compiled=len(syntax),documentation=out['documentation'])))
