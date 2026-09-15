from pathlib import Path
import subprocess,json,hashlib,tarfile,shutil,sys,sqlite3,platform
W=Path('/Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review'); O=W/'outputs/d9-corrections-review'; S=Path('/Users/luker/fot-tep-harness-d9-correzioni'); C=W/'work/corrections-candidate'
H='studio2/fase03/harness/d9_corrections'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(S),*a]).decode().strip()
def inv(root):
 paths=subprocess.check_output(['git','-C',str(root),'ls-files','-z']).decode().split('\0')
 return {p:{'bytes':(root/p).stat().st_size,'sha256':sha(root/p)} for p in paths if p and (root/p).is_file()}
assert not C.exists()
identity={'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'technical_tree':git('rev-parse','16c98f3^{tree}'),'status':git('status','--porcelain'),'remote':git('remote','-v'),'worktrees':git('worktree','list','--porcelain'),'python':sys.version,'platform':platform.platform(),'sqlite':sqlite3.sqlite_version}
assert identity['head']=='cf763333b7951b4cf711e1286657f6afc6a9df87' and identity['technical_tree']=='1dd8f84d991190d9d8316e6c56899bc115232716' and not identity['status']
(O/'evidence/identity.json').write_text(json.dumps(identity,indent=2)+'\n')
roots=[S,Path('/Users/luker/fot-tep-harness-d9'),Path('/Users/luker/fot-tep-harness-0310-d04')]
before={str(r):inv(r) for r in roots}
old=W/'outputs/d9-review';before[str(old)]={str(p.relative_to(old)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in old.rglob('*') if p.is_file()}
(O/'evidence/before.json').write_text(json.dumps(before,indent=2)+'\n')
subprocess.run([sys.executable,str(old/'evidence/verify_package.py')],check=True)
a=W/'work/corrections-candidate.tar'
with a.open('xb') as f:subprocess.run(['git','-C',str(S),'archive','16c98f39c044d812458705234b1a3f8ee4940b34'],stdout=f,check=True)
C.mkdir()
with tarfile.open(a) as t:t.extractall(C,filter='data')
# Original exact rejected archive, compare extracted files to retained snapshot.
with tarfile.open(W/'work/candidate.tar') as t:
 n=0
 for m in t:
  if m.isfile():
   p=W/'work/candidate'/m.name;assert p.read_bytes()==t.extractfile(m).read(),m.name;n+=1
identity['rejected_archive_members_verified']=n
m=S/H/'CANDIDATO_CORREZIONI_D9.json';assert sha(m)=='a2fbabcaa997831446c4c2775d62fa6fc2078229a4c71187337be30a9ae7e4e1'
manifest=json.loads(m.read_text());assert len(manifest['files'])==1062
for item in manifest['files']:
 p=C/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],item['path']
py=json.loads((S/H/'results/TESTED_BYTES.json').read_text())
for item in py['files']:assert sha(C/item['path'])==item['sha256'],item['path']
identity.update(candidate_members_verified=1062,preparer_python_members_verified=len(py['files']),archive={'path':str(a),'bytes':a.stat().st_size,'sha256':sha(a)})
(O/'evidence/identity.json').write_text(json.dumps(identity,indent=2)+'\n')
for name in ['PROMPT_RIVERIFICA_CORREZIONI_D9.md','CONTRATTO_CORREZIONI_D9.md','REPORT_CORREZIONI_D9.md','CONSEGNA_CORREZIONI_D9.json','CANDIDATO_CORREZIONI_D9.json','ACQUISIZIONE_NON_OK.json']:
 shutil.copy2(S/H/name,O/'evidence'/name)
for name,p in [('test_d9_corrections.py',C/'studio2/fase03/harness/test_d9_corrections.py'),('transport_boundary_regression.py',C/H/'transport_boundary_regression.py'),('independent_probes.py',old/'evidence/independent_probes.py')]:shutil.copy2(p,O/'evidence'/name)
(O/'evidence/source_inventory.json').write_text(json.dumps({str(p.relative_to(C)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in C.rglob('*') if p.is_file()},indent=2)+'\n')
print(json.dumps(identity,indent=2));print('SETUP OK')
