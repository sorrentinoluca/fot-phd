"""Read-only exact-candidate integrity and provenance checks. No provider access."""
from pathlib import Path
import json,hashlib,subprocess,collections,shutil,difflib,ast,platform,sqlite3,sys
E=Path(__file__).resolve().parent;C=E.parent/'candidate';H=C/'studio2/fase03/harness'
OLD=Path('/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/evidence')
TECH='9e18bcbd06fa2c54202c8eeda079c112dbfcefcd';PARENT='b882c27103dbd9d0e0462df20731123f5ed5a0c1'
def sha(b):return hashlib.sha256(b).hexdigest()
def g(*a):return subprocess.check_output(['git','-C',str(C),*a])
checks=[]
def check(kind,path,expected,size=None):
 b=Path(path).read_bytes();r=dict(kind=kind,path=str(path),sha256=sha(b),bytes=len(b),expected=expected,ok=sha(b)==expected and (size is None or size==len(b)));checks.append(r);assert r['ok'],r
check('manifest',H/'HARNESS_OFFLINE_CANDIDATE.json','e0b6fc2ba4752b485829b397867b5ae5ee1a7ec5356ea4d11f24e09f39b2f228',14155)
m=json.loads((H/'HARNESS_OFFLINE_CANDIDATE.json').read_text())
for r in m['files']:check('technical_member',C/r['path'],r['sha256'],r['bytes'])
acq=H/'non_ok_0c8157f_20260915';a=json.loads((acq/'ACQUISITION_INVENTORY.json').read_text())
for r in a['entries']:
 check('acquisition-source',r['source'],r['sha256'],r['bytes'])
 if r['disposition']=='copied_byte_identical':check('acquired-copy',acq/'evidence'/r['relative_path'],r['sha256'],r['bytes'])
repro=json.loads((H/'c01_c03_evidence/REPRODUCTION_INVENTORY.json').read_text())
for r in repro['files']:
 check('reproduction-source',r['source'],r['sha256'],r['bytes'])
 if r['disposition']=='copied_byte_identical':check('reproduction-copy',H/'c01_c03_evidence'/r['path'],r['sha256'],r['bytes'])
for line in (H/'c01_c03_evidence/SHA256SUMS').read_text().splitlines():
 h,p=line.split('  ',1);check('new-proof-manifest',H/'c01_c03_evidence'/p,h)
for r in m['preserved_qualified_metric_files']:check('metric_vs_published',C/r,sha(g('show','a00605862f627710347bd63c49f79a6d0a00135f:'+r)))
protected=['docs','phase_b','code','studio2/fase03/piano_statistico','studio2/fase03/schema_insight','studio2/fase03/baseline_numerica','studio2/fase03/pseudolabel','studio2/fase03/config/pilot_preflight.json','studio2/fase03/harness/PILOT_INPUT_SOURCES.pending.json']
scope={p:g('diff','--name-only','6268437b8b64288b50ad5f7c924e1fcab85b27d3',TECH,'--',p).decode() for p in protected};assert all(not v for v in scope.values())
(E/'technical.diff').write_bytes(g('diff',PARENT,TECH,'--','*.py',':(exclude)*/c01_c03_evidence/*'))
(E/'technical_paths.txt').write_bytes(g('diff','--name-status',PARENT,TECH))
(E/'documentary_paths.txt').write_bytes(g('diff','--name-status',TECH,'52e13e1ed540e1ad076474398bf850445c9a4a00'))
original=(OLD/'additional_edges.py').read_text();adapted=(H/'c01_c03_evidence/x23_adapted/evidence/additional_edges.py').read_text()
(E/'X23_adaptation.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),adapted.splitlines(True),fromfile='reviewer original',tofile='preparer adaptation')))
runtime=[]
for p in [Path('/Users/luker/.codex/sessions/2026/09/15/rollout-2026-09-15T00-23-30-01a0a204-abda-7a00-8466-f52f5bc84812.jsonl'),Path('/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T23-56-47-01a0a1ec-35a4-7870-9c39-9bf922d36c85.jsonl')]:
 events=[]
 for l in p.open():
  v=json.loads(l)
  if v.get('type') in ('session_meta','turn_context'):events.append(dict(type=v['type'],**{k:v['payload'][k] for k in ('id','model','effort','timestamp') if k in v['payload']}))
 runtime.append(dict(source=str(p),events=events))
(E/'runtime.json').write_text(json.dumps(dict(metadata=runtime,python=sys.version,architecture=platform.machine(),sqlite=sqlite3.sqlite_version),indent=2)+'\n')
out=dict(checks=checks,acquisition_counts=dict(collections.Counter(r['disposition'] for r in a['entries'])),reproduction_counts=dict(collections.Counter(r['disposition'] for r in repro['files'])),protected_scope=scope)
(E/'integrity.json').write_text(json.dumps(out,indent=2)+'\n')
# Only after source hashes are checked, create fresh sacrificial replay containers.
for name,files in [('literal',{'extended_probes.py':OLD/'extended_probes.py','additional_edges.py':OLD/'additional_edges.py'}),('x23_adapted',{'extended_probes.py':OLD/'extended_probes.py','additional_edges.py':H/'c01_c03_evidence/x23_adapted/evidence/additional_edges.py'})]:
 root=E/name;root.mkdir();(root/'candidate').symlink_to(C,target_is_directory=True);d=root/'evidence';d.mkdir()
 for target,source in files.items():shutil.copyfile(source,d/target)
print(json.dumps(dict(checks=len(checks),acquisition=out['acquisition_counts'],reproduction=out['reproduction_counts'],failures=0)))
