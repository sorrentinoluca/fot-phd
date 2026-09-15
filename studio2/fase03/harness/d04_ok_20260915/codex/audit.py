from pathlib import Path
import json,hashlib,subprocess,shutil,collections,ast,sys,sqlite3,platform
E=Path(__file__).resolve().parent;C=E.parent/'candidate';H=C/'studio2/fase03/harness';O=Path('/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence')
def sha(b):return hashlib.sha256(b).hexdigest()
def g(*args):return subprocess.check_output(['git','-C',str(C),*args])
checks=[]
def check(kind,p,h,size=None):
 b=Path(p).read_bytes();assert sha(b)==h and (size is None or len(b)==size),(kind,p);checks.append(dict(kind=kind,path=str(p),sha256=h,bytes=len(b),ok=True))
check('technical-manifest',H/'HARNESS_OFFLINE_CANDIDATE.json','9fbad8c036075605a9bbdfdac84078259428b679fc33341ed98f21050a07efd6',24151)
m=json.loads((H/'HARNESS_OFFLINE_CANDIDATE.json').read_text())
for r in m['files']:
 check('technical-member',C/r['path'],r['sha256'],r['bytes']);assert (C/r['path']).read_bytes()==g('show','HEAD:'+r['path'])
acq=H/'non_ok_23859a2_20260915';a=json.loads((acq/'ACQUISITION_INVENTORY.json').read_text())
for r in a['files']:
 check('acquisition-source',r['source'],r['sha256'],r['bytes'])
 if r['storage']=='copy':check('acquisition-copy',C/r['copy'],r['sha256'],r['bytes'])
repro=H/'d04_evidence';d=json.loads((repro/'REPRODUCTION_INVENTORY.json').read_text())
for r in d['files']:
 check('reproduction-source',r['source'],r['sha256'],r['bytes'])
 if r['storage']=='copy':check('reproduction-copy',C/r['copy'],r['sha256'],r['bytes'])
for line in (repro/'SHA256SUMS').read_text().splitlines():
 h,p=line.split('  ',1);check('reproduction-manifest-member',repro/p,h)
# Re-read earlier sources, qualified pins and recovered modules rather than trust old results.
prior=json.loads(Path('/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/lineage_integrity.json').read_text())
for r in prior['checks']:
 k=r['kind']
 if k=='original-preserved':check(k,r['path'],r['sha256'],r['bytes'])
 elif k.startswith('exact-source-'):
  b=g('show',r['path']);assert sha(b)==r['sha256'];checks.append(dict(r))
 elif k=='module-provenance':
  p=r['path'];check(k,C/p,r['current_sha256']);assert sha(g('show',r['source_commit']+':'+p))==r['source_sha256'];assert g('show','9e18bcbd06fa2c54202c8eeda079c112dbfcefcd:'+p)==(C/p).read_bytes()
 elif k=='remote-tag':
  observed=g('ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/tags/'+r['path'],'refs/tags/'+r['path']+'^{}').decode();assert observed==r['remote'];checks.append(dict(r))
protected=prior['protected_scope'];scope={p:g('diff','--name-only','97868f9d6ef281c2dd4ab1c6ffb67e2477ee5715','HEAD','--',p).decode() for p in protected};assert all(not v for v in scope.values())
for p in m['preserved_qualified_metric_files']:check('metric-vs-published',C/p,sha(g('show','a00605862f627710347bd63c49f79a6d0a00135f:'+p)))
live=[]
for p in sorted((C/'studio2/fase03').rglob('*.py')):
 if any(part.startswith('non_ok_') or part.endswith('_evidence') for part in p.parts):continue
 tree=ast.parse(p.read_text());compile(tree,str(p),'exec');live.append(str(p.relative_to(C)))
 for node in ast.walk(tree):
  names=[x.name for x in node.names] if isinstance(node,ast.Import) else [node.module or ''] if isinstance(node,ast.ImportFrom) else []
  assert not any(n=='phase_b' or n.startswith('phase_b.') for n in names),p
(E/'technical.diff').write_bytes(g('diff','f0dca4d2d46a290d2ffeb1840abd46eb7664f0ae','HEAD','--','studio2/fase03/harness/ledger.py','studio2/fase03/harness/test_d04_open_quota.py','studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md'))
(E/'technical_paths.txt').write_bytes(g('diff','--name-status','f0dca4d2d46a290d2ffeb1840abd46eb7664f0ae','HEAD'))

# Independent exact-blob test-first and protected-files checks.
first='bf7774f2d153ecc50f27ba095f77b612933b4d26'
tf=json.loads((H/'d04_evidence/TEST_FIRST.json').read_text())
for r in tf['test_and_contract_files']+tf['red_proofs']:
 b=g('show',first+':'+r['path']);assert sha(b)==r['sha256'];checks.append(dict(kind='exact-source-test-first',path=first+':'+r['path'],sha256=sha(b),bytes=len(b),ok=True))
assert g('show',first+':studio2/fase03/harness/ledger.py')==g('show','23859a29225ccd9cd6f47e4a0b6e36258831dbab:studio2/fase03/harness/ledger.py')
assert sha(g('show',first+':studio2/fase03/harness/ledger.py'))==tf['runtime_sha256']
assert g('rev-parse','HEAD^').decode().strip()==first
test_path='studio2/fase03/harness/test_d04_open_quota.py'
assert g('show',first+':'+test_path)==(C/test_path).read_bytes()
check('test-first-final-identical',C/test_path,tf['test_and_contract_files'][2]['sha256'])
(E/'test_first_final.diff').write_bytes(g('diff',first,'HEAD','--',test_path))
cl=json.loads((acq/'CLAUDE_PROVENIENZA.json').read_text())
check('claude-original',cl['source'],cl['sha256'],cl['bytes']);check('claude-copy',acq/'VERIFICA_D03_CLAUDE.md',cl['sha256'],cl['bytes'])
protected_files=json.loads((H/'d04_evidence/runs/scope.json').read_text())['protected_files_unchanged']
assert len(protected_files)==177
for r in protected_files:
 check('protected-file',C/r['path'],r['sha256'],r['bytes']);assert (C/r['path']).read_bytes()==g('show','97868f9d6ef281c2dd4ab1c6ffb67e2477ee5715:'+r['path'])
(E/'maintenance_candidate.diff').write_bytes(g('diff','819b12e97fb94d501032655ec2f226139e6c5ca5','HEAD','--','docs/MAINTENANCE.md'))

runtime=[]
for p in [Path('/Users/luker/.codex/sessions/2026/09/15/rollout-2026-09-15T00-23-30-01a0a204-abda-7a00-8466-f52f5bc84812.jsonl'),Path('/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T23-56-47-01a0a1ec-35a4-7870-9c39-9bf922d36c85.jsonl')]:
 events=[]
 for line in p.open():
  r=json.loads(line)
  if r.get('type') in ('session_meta','turn_context'):events.append(dict(type=r['type'],**{k:r['payload'][k] for k in ('id','model','effort','timestamp') if k in r['payload']}))
 runtime.append(dict(source=str(p),events=events))
(E/'runtime.json').write_text(json.dumps(dict(metadata=runtime,python=sys.version,architecture=platform.machine(),sqlite=sqlite3.sqlite_version),indent=2)+'\n')
out=dict(checks=checks,acquisition_counts=dict(collections.Counter(r['storage'] for r in a['files'])),reproduction_counts=dict(collections.Counter(r['storage'] for r in d['files'])),protected_scope=scope,compiled_live=live)
(E/'integrity.json').write_text(json.dumps(out,indent=2)+'\n')
# Fresh containers only, after provenance checks. Scripts remain byte-identical.
for name,sources in [('v_original',{'independent_d03_probes.py':O/'independent_d03_probes.py'}),('w_original',{'retry_proof_probes.py':O/'w_original/evidence/retry_proof_probes.py'}),('z_original',{'chain_probes.py':O/'z_original/evidence/chain_probes.py'}),('y_original',{'edge_probes.py':O/'y_original/evidence/edge_probes.py'}),('literal',{'extended_probes.py':O/'literal/evidence/extended_probes.py','additional_edges.py':O/'literal/evidence/additional_edges.py'}),('x23_adapted',{'extended_probes.py':O/'x23_adapted/evidence/extended_probes.py','additional_edges.py':O/'x23_adapted/evidence/additional_edges.py'})]:
 root=E/name;root.mkdir();(root/'candidate').symlink_to(C,target_is_directory=True);(root/'evidence').mkdir()
 for name,source in sources.items():shutil.copyfile(source,root/'evidence'/name)
print(json.dumps(dict(checks=len(checks),acquisition=out['acquisition_counts'],reproduction=out['reproduction_counts'],compiled=len(live),failures=0)))
