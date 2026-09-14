from pathlib import Path
import subprocess,json,hashlib,re,datetime
R=Path(__file__).resolve().parents[4];O=Path(__file__).parent;A='9b6bd64';B='e82b5a0';P='studio2/fase03/paper_sections/'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def blob(ref,p):return git('show',ref+':'+p)
def info(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def ancestor(x,y):return subprocess.run(['git','merge-base','--is-ancestor',x,y],cwd=R).returncode==0
out={}
refs=['e82b5a0','cf79e81','50f07a9','1d480fd','bcb462d','91a880b','dc6e30c','d35b684','18aa3bb','705f1c4','532cc77','9b6bd64','7c99a83','3c64390','43b31af','c9f83c6','e37c3db','40911d0']
out['genealogy']=[{'commit':git('rev-parse',x).decode().strip(),'parents':git('show','-s','--format=%P',x).decode().strip().split(),'ancestor_A':ancestor(x,A),'ancestor_remote_main_observed':ancestor(x,'c486eee')} for x in refs]
ps=git('ls-tree','-r','--name-only','d35b684','--',P).decode().splitlines()
out['package']=[{'path':p,**info(blob(A,p)),'same_d35':blob(A,p)==blob('d35b684',p),'same_disk':blob(A,p)==(R/p).read_bytes(),'same_merge':blob('18aa3bb',p)==blob('d35b684',p)} for p in ps]
out['package_delta']=git('diff','--name-status','d35b684',A,'--',P).decode().splitlines()
prov='studio2/PROVENIENZA.md';a=blob(A,prov);b=blob(B,prov);d=blob('d35b684',prov)
tail=d[d.index(b'## Fase 03',d.index(b'## 9.')):] if b'## 9.' in d else b''
# Locate the source 03.15 heading explicitly, independent of numbering.
dt=d.decode();m=re.search(r'^## Sotto-fase 03\.15.*$',dt,re.M);tail=dt[m.start():];tail=re.sub(r'^## Sotto-fase 03\.15.*$', '## 14. Fase 03 — sotto-fase 03.15: sezioni del paper indipendenti dal modello',tail,count=1,flags=re.M);tail=tail.replace('## Fase 03 — delta di allineamento 03.15 del 2026-09-14','### 14.1 Delta di allineamento 03.15 del 2026-09-14')
out['provenienza']={'base_1_13_exact_prefix':a.startswith(b),'source_0315_tail_equal_after_two_heading_changes':a[a.index(b'## 14.'):].decode()==tail,'headings':re.findall(r'^##+ .*$',a.decode(),re.M)}
changes=git('diff','--name-status',B,A).decode().splitlines();out['delta_paths']=changes;allow={p for p in ps}|{prov,'docs/fot_walkthrough_conversazione_studio2.md','docs/fot_walkthrough_conversazione_studio2.html',P+'CONSEGNA_0315_2026-09-14.md',P+'CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md'};out['unexpected_delta']=[x for x in changes if x.split('\t')[-1] not in allow]
out['step_diffs']={ref:git('diff-tree','--no-commit-id','--name-status','-r',ref).decode() for ref in ['705f1c4','532cc77','9b6bd64']}
bt=(O/'CONSEGNA_ESTERNA_B.md').read_text();inv=re.findall(r'^\| ([AM]) \| `([^`]+)` \|$',bt,re.M);out['B_inventory_matches']=sorted('\t'.join(x) for x in inv)==sorted(changes)
h=P+'CONSEGNA_0315_2026-09-14.md';out['historical_delivery']={'path':h,**info(blob(A,h)),'matches_source':blob(A,h)==(Path('/Users/luker/fot-tep-paper-sections')/h).read_bytes(),'matches_acquisition':blob(A,h)==blob('705f1c4',h)}
# Reachability and fingerprints only: no scientific extraction or calculations.
f=json.loads(blob(A,P+'FONTI_DELTA_0315.json'));out['source54']=[]
for e in f['sources']:
 if e.get('commit'):data=blob(e['commit'],e['path'])
 else:
  p=Path(e['path']);p=p if p.is_absolute() else Path('/Users/luker/fot-tep')/p;data=p.read_bytes();(O/('fonte_esterna_'+p.name)).write_bytes(data)
 actual=info(data);out['source54'].append({**e,'fingerprint_matches':all(actual[k]==e[k] for k in ['bytes','sha256']),'commit_ancestor_A':ancestor(e['commit'],A) if e.get('commit') else None})
pr=Path('/Users/luker/fot-tep-verifica-raccordo-e82b5a0/studio2/fase03/VERIFICA_RACCORDO_DOCUMENTALE_036_0312_LETTERATURA.md');data=pr.read_bytes();assert info(data)['sha256']=='7c1d6ebf90ccb29d2b3f418b0b6740b62435626db8e9a6b7f6abdd8512a27511';(O/'VERIFICA_BASE_e82b5a0.md').write_bytes(data);out['base_verdict']={'source':str(pr),**info(data)}
logs=[(O/x).read_text() for x in ['guardiano_base.log','guardiano_A.log']];fail=[[l for l in x.splitlines() if l.startswith('FAIL:')] for x in logs];skip=[[l for l in x.splitlines() if '... skipped ' in l] for x in logs]
c=json.loads(blob(A,P+'CONTROLLI_DELTA_0315.json'))['guardian'];out['guardian']={'script_equal':blob(A,'docs/test_explanation.py')==blob(B,'docs/test_explanation.py'),'failures_identical':fail[0]==fail[1],'failure_identifiers':fail[1],'skip_identical':skip[0]==skip[1],'skip':skip[1],'full_logs_normalized_equal':logs[0].replace('/Users/luker/fot-tep-verifica-raccordo-e82b5a0','ROOT')==logs[1].replace(str(R),'ROOT'),'historical_identifiers':c.get('failure_identifiers_with_subtests')}
for scope,args in [('all_delta',[B,A]),('documentation',['705f1c4','532cc77'])]:
 r=subprocess.run(['git','diff','--check',*args],cwd=R,capture_output=True);(O/('diff_check_'+scope+'.log')).write_bytes(r.stdout+r.stderr);out['diff_check_'+scope]=r.returncode
(O/'integrity.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
for k,v in out.items():
 if k in ['package','source54']:print(k,len(v),[x for x in v if any(x.get(y) is False for y in ['same_d35','same_disk','same_merge','fingerprint_matches'])])
 elif k not in ['genealogy','guardian']:print(k,str(v)[:1800])
print('guardian', {k:v for k,v in out['guardian'].items() if 'identifiers' not in k})
