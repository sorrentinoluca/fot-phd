from pathlib import Path
import json,hashlib,subprocess,re,os,datetime
E=Path(__file__).resolve().parent;C=E.parent/'candidate';O=Path('/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(p,*a):return subprocess.check_output(['git','-C',str(p),*a]).decode()
initial=json.loads((E/'initial_git_state.json').read_text());repos={}
for p,before in initial['repositories'].items():
 now=dict(identity=git(p,'rev-parse','HEAD','HEAD^{tree}'),status=git(p,'status','--short','--branch'));now['unchanged_from_initial']=all(now[k]==v for k,v in before.items());repos[p]=now
assert all(r['unchanged_from_initial'] for r in repos.values()), repos
preserved=initial['preserved_untracked'];q=Path(preserved['path'])
assert sha(q)==preserved['sha256'] and q.stat().st_size==preserved['bytes']
current=dict(identity=git(C,'rev-parse','HEAD','HEAD^{tree}'),status=git(C,'status','--short','--branch'),remote=git(C,'remote','-v'))
assert current['identity']=='aae29a908356e4a4842a214fdc3db9bff26ec3ca\n4e1f7f043725d64fb16b7d1c921c619bce8d1bb3\n';assert current['status']=='## HEAD (no branch)\n'
remote=git(C,'ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/heads/main');assert remote==initial['remote_main']
checks=json.loads((E/'integrity.json').read_text())['checks'];checked=0
for r in checks:
 if Path(r['path']).is_absolute():assert sha(Path(r['path']))==r['sha256'];checked+=1
 elif r['kind'].startswith('exact-source-'):
  b=subprocess.check_output(['git','-C',str(C),'show',r['path']]);assert hashlib.sha256(b).hexdigest()==r['sha256'];checked+=1
assert checked == len(checks)-3, (checked,len(checks))
(E/'worktrees_final.txt').write_text(git(C,'worktree','list','--porcelain'))
(E/'final_integrity.json').write_text(json.dumps(dict(rechecked_files_or_blobs=checked,failures=0,source='integrity.json'),indent=2)+'\n')
(E/'final_git_state.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),repositories=repos,candidate=current,remote_main=remote,preserved_untracked=preserved),indent=2)+'\n')
tests={}
for name,n in [('targeted',128),('discovery',163)]:
 text=(E/(name+'.log')).read_text();assert re.search(r'Ran '+str(n)+r' tests in ',text) and re.search(r'^OK$',text,re.M);assert not re.search(r'^(FAIL|ERROR):',text,re.M);tests[name]=dict(tests=n,failures=0,errors=0)
for name,path,n,fail in [('Y','y_original/evidence/edge_probes.json',7,0),('X01_X18','literal/evidence/extended.json',18,0),('X19_X24_literal','literal/evidence/additional_edges/additional.json',6,1),('X23_adapted','x23_adapted/evidence/additional_edges/additional.json',1,0),('Z','z_original/evidence/chain_probes.json',5,0),('W','w_original/evidence/retry_proof_probes.json',4,0),('V','v_original/evidence/independent_d03_probes.json',6,0),('U','decision_edge_probes.json',5,0)]:
 d=json.loads((E/path).read_text());assert d['tests']==n and len(d['failures'])==fail and not d['errors'];tests[name]=dict(tests=n,failures=fail,errors=0,source=path)
a=json.loads((E/'applicable/applicable.json').read_text());assert a['tests']==14 and not a['failures'] and not a['errors'];tests['applicable']=dict(tests=14,literal=12,fixture_adapted=[20,21],failures=0,errors=0)
tests['documentation']=json.loads((E/'documentation_comparison.json').read_text())
for name,n,f in [('red_contract',8,240),('green_contract',8,0)]:
 d=json.loads((E/(name+'.json')).read_text());assert (d['tests'],len(d['failures']),len(d['errors']))==(n,f,0);tests[name]=dict(tests=n,failures=f,errors=0)
scripts={}
for rel in ['v_original/evidence/independent_d03_probes.py','w_original/evidence/retry_proof_probes.py','z_original/evidence/chain_probes.py','y_original/evidence/edge_probes.py','literal/evidence/extended_probes.py','literal/evidence/additional_edges.py','x23_adapted/evidence/extended_probes.py','x23_adapted/evidence/additional_edges.py']:
 prior=O/'independent_d03_probes.py' if rel.startswith('v_original') else O/rel
 assert sha(E/rel)==sha(prior);scripts[rel]=sha(E/rel)
(E/'RESULTS.json').write_text(json.dumps(dict(candidate='aae29a908356e4a4842a214fdc3db9bff26ec3ca',tree='4e1f7f043725d64fb16b7d1c921c619bce8d1bb3',verdict='OK',original_D01='CLOSED for documented original reproductions',original_D02='CLOSED for documented original reproductions',original_D03='CLOSED for documented original reproductions',original_D04='CLOSED for original V05/V06, D04 matrix and independent U01-U05',residual=None,tests=tests,scripts_sha256=scripts,originals_mapped=50,no_tests_sum=True),indent=2)+'\n')
links=[]
for p in [E/'VERIFICA_D04.md',E/'MATRICE_50_METODI.md',E/'MATRICE_ESTENSIONI.md',E/'COMANDI.md',E/'generated_decisions/MATRICE_D04_DECISIONI.md']:
 for raw in re.findall(r'\]\((/[^)]+)\)',p.read_text()):
  q=Path(re.sub(r':\d+$','',raw))
  if q.name not in ('SHA256SUMS','EVIDENCE_INVENTORY.json'):assert q.exists(),(p,raw)
  links.append(raw)
(E/'link_validation.json').write_text(json.dumps(dict(checked=len(links),missing=0),indent=2)+'\n')
files=[];symlinks=[]
for root,dirs,names in os.walk(E,followlinks=False):
 for name in dirs+names:
  p=Path(root)/name
  if p.is_symlink():symlinks.append(dict(path=str(p.relative_to(E)),target=os.readlink(p),resolved=str(p.resolve())))
 for name in names:
  p=Path(root)/name
  if p.is_symlink() or name in ('SHA256SUMS','EVIDENCE_INVENTORY.json'):continue
  files.append(dict(path=str(p.relative_to(E)),bytes=p.stat().st_size,sha256=sha(p)))
files.sort(key=lambda r:r['path']);symlinks.sort(key=lambda r:r['path'])
(E/'EVIDENCE_INVENTORY.json').write_text(json.dumps(dict(scope='Regular evidence files without symlink traversal; this inventory and SHA256SUMS excluded to avoid self-reference',regular_files=len(files),bytes=sum(r['bytes'] for r in files),files=files,symlinks=symlinks),indent=2)+'\n')
files.append(dict(path='EVIDENCE_INVENTORY.json',sha256=sha(E/'EVIDENCE_INVENTORY.json')))
(E/'SHA256SUMS').write_text(''.join(f"{r['sha256']}  {r['path']}\n" for r in sorted(files,key=lambda r:r['path'])))
for r in files:assert sha(E/r['path'])==r['sha256']
print(json.dumps(dict(verdict='OK',report_sha256=sha(E/'VERIFICA_D04.md'),manifest_sha256=sha(E/'SHA256SUMS'),regular_files=len(files)-1,bytes=sum(r.get('bytes',0) for r in files),symlinks=len(symlinks),repositories_with_same_identity=len(repos),repositories_with_same_status=sum(r['unchanged_from_initial'] for r in repos.values()),preserved_untracked=preserved,candidate_status=current['status']),indent=2))
