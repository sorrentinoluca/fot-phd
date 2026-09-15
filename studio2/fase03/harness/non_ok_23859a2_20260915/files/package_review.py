from pathlib import Path
import json,hashlib,subprocess,re,os,datetime
E=Path(__file__).resolve().parent;C=E.parent/'candidate';O=Path('/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(p,*a):return subprocess.check_output(['git','-C',str(p),*a]).decode()
initial=json.loads((E/'initial_git_state.json').read_text());repos={}
for p,before in initial['repositories'].items():
 now=dict(identity=git(p,'rev-parse','HEAD','HEAD^{tree}'),status=git(p,'status','--short','--branch'));now['unchanged_from_initial']=all(now[k]==v for k,v in before.items());repos[p]=now
external_changes=[]
for path,r in repos.items():
 assert r['identity']==initial['repositories'][path]['identity'],r
 if not r['unchanged_from_initial']:
  assert path=='/Users/luker/fot-tep-harness-0310-d03' and r['status']=='## codex/studio2-harness-0310-d03\n?? VERIFICA_D03.md\n',r
  assert git(path,'diff','--name-only')=='' and git(path,'diff','--cached','--name-only')==''
  q=Path(path)/'VERIFICA_D03.md';external_changes.append(dict(path=str(q),bytes=q.stat().st_size,sha256=sha(q),note='Appeared during review; not created, edited, deleted, or used as evidence by this session. Source HEAD/tree/tracked contents unchanged.'))
(E/'external_git_changes.json').write_text(json.dumps(external_changes,indent=2)+'\n')
current=dict(identity=git(C,'rev-parse','HEAD','HEAD^{tree}'),status=git(C,'status','--short','--branch'),remote=git(C,'remote','-v'))
assert current['identity']=='23859a29225ccd9cd6f47e4a0b6e36258831dbab\nfe66025f4925e27676b0be16428475e3fcaee060\n';assert current['status']=='## HEAD (no branch)\n'
remote=git(C,'ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/heads/main');assert remote==initial['remote_main']
checks=json.loads((E/'integrity.json').read_text())['checks'];checked=0
for r in checks:
 if Path(r['path']).is_absolute():assert sha(Path(r['path']))==r['sha256'];checked+=1
 elif r['kind'].startswith('exact-source-'):
  b=subprocess.check_output(['git','-C',str(C),'show',r['path']]);assert hashlib.sha256(b).hexdigest()==r['sha256'];checked+=1
assert checked == len(checks)-3, (checked,len(checks))
(E/'worktrees_final.txt').write_text(git(C,'worktree','list','--porcelain'))
(E/'final_integrity.json').write_text(json.dumps(dict(rechecked_files_or_blobs=checked,failures=0,source='integrity.json'),indent=2)+'\n')
(E/'final_git_state.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),repositories=repos,candidate=current,remote_main=remote,external_changes=external_changes),indent=2)+'\n')
tests={}
for name,n in [('targeted',120),('discovery',155)]:
 text=(E/(name+'.log')).read_text();assert re.search(r'Ran '+str(n)+r' tests in ',text) and re.search(r'^OK$',text,re.M);assert not re.search(r'^(FAIL|ERROR):',text,re.M);tests[name]=dict(tests=n,failures=0,errors=0)
for name,path,n,fail in [('Y','y_original/evidence/edge_probes.json',7,0),('X01_X18','literal/evidence/extended.json',18,0),('X19_X24_literal','literal/evidence/additional_edges/additional.json',6,1),('X23_adapted','x23_adapted/evidence/additional_edges/additional.json',1,0),('Z','z_original/evidence/chain_probes.json',5,0),('W','w_original/evidence/retry_proof_probes.json',4,0),('V','independent_d03_probes.json',6,2)]:
 d=json.loads((E/path).read_text());assert d['tests']==n and len(d['failures'])==fail and not d['errors'];tests[name]=dict(tests=n,failures=fail,errors=0,source=path)
a=json.loads((E/'applicable/applicable.json').read_text());assert a['tests']==14 and not a['failures'] and not a['errors'];tests['applicable']=dict(tests=14,literal=12,fixture_adapted=[20,21],failures=0,errors=0)
tests['documentation']=json.loads((E/'documentation_comparison.json').read_text())
for name,n,f in [('red_contract',9,8),('green_contract',9,0)]:
 d=json.loads((E/(name+'.json')).read_text());assert (d['tests'],d['failures'],d['errors'])==(n,f,0);tests[name]=dict(tests=n,failures=f,errors=0)
scripts={}
for rel in ['w_original/evidence/retry_proof_probes.py','z_original/evidence/chain_probes.py','y_original/evidence/edge_probes.py','literal/evidence/extended_probes.py','literal/evidence/additional_edges.py','x23_adapted/evidence/extended_probes.py','x23_adapted/evidence/additional_edges.py']:
 prior=O/'retry_proof_probes.py' if rel.startswith('w_original') else O/rel
 assert sha(E/rel)==sha(prior);scripts[rel]=sha(E/rel)
(E/'RESULTS.json').write_text(json.dumps(dict(candidate='23859a29225ccd9cd6f47e4a0b6e36258831dbab',tree='fe66025f4925e27676b0be16428475e3fcaee060',verdict='NON OK',original_D01='CLOSED for documented original reproductions',original_D02='CLOSED for documented original reproductions',original_D03='CLOSED for documented original reproductions',residual='D04: open-stage quota_kind fault permits eighth retry without waiver and reaches stub transport',tests=tests,scripts_sha256=scripts,originals_mapped=50,no_tests_sum=True),indent=2)+'\n')
links=[]
for p in [E/'VERIFICA_D03.md',E/'MATRICE_50_METODI.md',E/'MATRICE_ESTENSIONI.md',E/'COMANDI.md',E/'generated_fields/MATRICE_D03_CAMPI.md']:
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
print(json.dumps(dict(verdict='NON OK',report_sha256=sha(E/'VERIFICA_D03.md'),manifest_sha256=sha(E/'SHA256SUMS'),regular_files=len(files)-1,bytes=sum(r.get('bytes',0) for r in files),symlinks=len(symlinks),repositories_with_same_identity=len(repos),repositories_with_same_status=sum(r['unchanged_from_initial'] for r in repos.values()),external_changes=external_changes,candidate_status=current['status']),indent=2))
