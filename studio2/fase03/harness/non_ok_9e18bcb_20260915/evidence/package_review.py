from pathlib import Path
import json,hashlib,subprocess,datetime,re,os
E=Path(__file__).resolve().parent;C=E.parent/'candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(p,*a):return subprocess.check_output(['git','-C',str(p),*a]).decode()
initial=json.loads((E/'initial_git_state.json').read_text());repos={}
for p,before in initial['repositories'].items():
 after=dict(identity=git(p,'rev-parse','HEAD','HEAD^{tree}'),status=git(p,'status','--short','--branch'));after['unchanged_from_initial']=all(after[k]==v for k,v in before.items());repos[p]=after
assert all(r['unchanged_from_initial'] for r in repos.values()),repos
candidate=dict(identity=git(C,'rev-parse','HEAD','HEAD^{tree}'),status=git(C,'status','--short','--branch'),remote=git(C,'remote','-v'))
assert candidate['identity']=='9e18bcbd06fa2c54202c8eeda079c112dbfcefcd\n5d1fd7924c4e1e46346f367590e6aa1977a6ba75\n';assert candidate['status']=='## HEAD (no branch)\n'
remote=git(C,'ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/heads/main');assert remote==initial['remote_main']
checks=json.loads((E/'integrity.json').read_text())['checks'];last=[]
for r in checks:
 p=Path(r['path']);assert sha(p)==r['expected'];last.append(dict(path=str(p),sha256=r['expected'],ok=True))
(E/'final_integrity.json').write_text(json.dumps(dict(rechecked=len(last),failures=0,checks=last),indent=2)+'\n')
state=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),repositories=repos,candidate=candidate,remote_main=remote,mutations='Only isolated clone and sibling evidence; no candidate edit/commit/tag/push/merge')
(E/'final_git_state.json').write_text(json.dumps(state,indent=2)+'\n')
scripts={}
old=Path('/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/evidence')
for name in ('extended_probes.py','additional_edges.py'):
 p=E/'literal/evidence'/name;assert sha(p)==sha(old/name);scripts[name]=sha(p)
results=dict(candidate='9e18bcbd06fa2c54202c8eeda079c112dbfcefcd',verdict='NON OK',open_findings=['D01: residual C01/R04'],closed_corrections=['C02','C03'],targeted=dict(tests=96,failures=0,errors=0),discovery=dict(tests=131,failures=0,errors=0),applicable=dict(tests=14,literal=12,fixture_adapted=[20,21],failures=0,errors=0),extensions=dict(distinct=24,literal_pass=23,literal_fail=['X23 obsolete expected interruption'],adapted_pass=['X23']),new_independent=dict(tests=7,pass_count=5,failures=['Y01','Y02'],errors=0),documentation=dict(tests=35,historical_failures=14,skips=1,status='NON PASS'),scripts_sha256=scripts,originals_mapped=50)
(E/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
# Validate every absolute Markdown link inside the newly authored report/matrices/commands.
checked=[]
for p in [E/'VERIFICA_C01_C03.md',E/'MATRICE_50_METODI.md',E/'MATRICE_X01_X24.md',E/'COMANDI.md']:
 for raw in re.findall(r'\]\((/[^)]+)\)',p.read_text()):
  path=re.sub(r':\d+$','',raw)
  if Path(path).name in ('SHA256SUMS','EVIDENCE_INVENTORY.json'):continue
  assert Path(path).exists(),(p,raw);checked.append(raw)
(E/'link_validation.json').write_text(json.dumps(dict(checked=len(checked),missing=0),indent=2)+'\n')
files=[];links=[]
for root,dirs,names in os.walk(E,followlinks=False):
 for name in dirs+names:
  p=Path(root)/name
  if p.is_symlink():links.append(dict(path=str(p.relative_to(E)),target=os.readlink(p),resolved=str(p.resolve())))
 for name in names:
  p=Path(root)/name
  if p.is_symlink() or name in ('SHA256SUMS','EVIDENCE_INVENTORY.json'):continue
  files.append(dict(path=str(p.relative_to(E)),bytes=p.stat().st_size,sha256=sha(p)))
files.sort(key=lambda r:r['path']);links.sort(key=lambda r:r['path'])
(E/'EVIDENCE_INVENTORY.json').write_text(json.dumps(dict(scope='All regular files in evidence, no symlink traversal; inventory and SHA256SUMS excluded to avoid self-reference',regular_files=len(files),bytes=sum(r['bytes'] for r in files),files=files,symlinks=links),indent=2)+'\n')
files.append(dict(path='EVIDENCE_INVENTORY.json',sha256=sha(E/'EVIDENCE_INVENTORY.json')))
(E/'SHA256SUMS').write_text(''.join(f"{r['sha256']}  {r['path']}\n" for r in sorted(files,key=lambda r:r['path'])))
for r in files:assert sha(E/r['path'])==r['sha256']
print(json.dumps(dict(verdict=results['verdict'],regular_files=len(files)-1,bytes=sum(r.get('bytes',0) for r in files),symlinks=len(links),report_sha256=sha(E/'VERIFICA_C01_C03.md'),manifest_sha256=sha(E/'SHA256SUMS'),candidate_status=candidate['status'],preserved_repositories=len(repos)),indent=2))
