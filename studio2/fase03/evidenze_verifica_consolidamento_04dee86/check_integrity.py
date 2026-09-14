from pathlib import Path
import subprocess,json,hashlib,re,collections,ast
W=Path('/Users/luker/fot-tep-verifica-consolidamento-04dee86');O=Path(__file__).parent
A='04dee86140b3ff18882f9d164beef5ab7bf33e00';B='e82b5a08bf642ad45f77e71832958207beb1181c';P='10582798eb5a4b52672bfbcb1cc028adcb73e9f1';M='3360867751c66a39e819247f86dab8e936f8cbb3';D='d35b684acbfd1f357bc34f3a21cebb18e8a6bea0';R='3c64390bc4dd58c48cc4e1e388a38989b32b3143'
def git(*args):return subprocess.check_output(['git','-C',str(W),*args])
def blob(c,p):return git('show',c+':'+p)
def fp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def tree(c,p):return git('ls-tree','-r','--name-only',c,'--',p).decode().splitlines()
def anc(c,t):return subprocess.run(['git','-C',str(W),'merge-base','--is-ancestor',c,t]).returncode==0
out={};out['ancestors']={c:anc(c,A) for c in [B,P,D,M,'4ba2ad6e4a298411b4f0f7572ad3ef8e55948015']}
out['merge_parents']=git('show','-s','--format=%P','4ba2ad6').decode().split();assert out['merge_parents']==[P,M]
out['history']=git('log','--format=%H %P %s',P+'..'+A).decode()
out['delta_names']=git('diff','--name-status',B,A).decode().splitlines()
out['packages']={}
for folder,ref,n in [('paper_sections',D,17),('harness',M,14)]:
 root='studio2/fase03/'+folder;paths=tree(ref,root);assert len(paths)==n
 rows=[{'path':p,'blob':git('rev-parse',A+':'+p).decode().strip(),**fp(blob(A,p)),'same':blob(ref,p)==blob(A,p)==(W/p).read_bytes()} for p in paths]
 out['packages'][folder]={'files':rows,'additional_paths':sorted(set(tree(A,root))-set(paths))}
 assert all(x['same'] for x in rows)
out['evidence_tree']={c:git('rev-parse',c+':studio2/fase03/evidence').decode().strip() for c in [B,A]};assert len(set(out['evidence_tree'].values()))==1
out['provenienza']={'same_as_10582798':blob(P,'studio2/PROVENIENZA.md')==blob(A,'studio2/PROVENIENZA.md'),**fp(blob(A,'studio2/PROVENIENZA.md'))}
f=json.loads(blob(A,'studio2/fase03/schema_insight/SCHEMA_FREEZE.json'));out['R4']=[]
assert blob(A,'studio2/fase03/schema_insight/SCHEMA_FREEZE.json')==blob(R,'studio2/fase03/schema_insight/SCHEMA_FREEZE.json')
for category,rows in [('files',f['files']),('source_files',f['source_files'])]:
 for x in rows:
  ref=R if category=='files' else re.search(r'[0-9a-f]{40}',x.get('source_ref',f['base_commit'])).group()
  data=blob(ref,x['path']);row={**x,'checked_ref':ref,'category':category,'historical_match':fp(data)=={k:x[k] for k in ['bytes','sha256']}}
  if category=='files':row['candidate_same']=data==blob(A,x['path'])==(W/x['path']).read_bytes()
  out['R4'].append(row)
assert len(out['R4'])==18 and all(x['historical_match'] and x.get('candidate_same',True) for x in out['R4'])
contract=blob(A,'studio2/fase03/harness/CONTRATTO_RACCORDO_METRICHE.md').decode();out['pinned_039']=[]
for name,sha in re.findall(r'- `([^`]+)`, SHA-256\s+`([a-f0-9]{64})`',contract):
 p='studio2/fase03/baseline_numerica/'+name;data=blob('c486eee',p);out['pinned_039'].append({'path':p,**fp(data),'declared':sha,'same':data==blob(A,p),'match':fp(data)['sha256']==sha})
assert len(out['pinned_039'])==4 and all(x['same'] and x['match'] for x in out['pinned_039'])
f39=json.loads(blob(A,'studio2/fase03/baseline_numerica/BASELINE_FREEZE_rev003.json'))['normal_evidence'];out['pinned_036']=[]
for name,key in [('extract_evidence.py','phase03_6_extractor_sha256'),('leakage.py','phase03_6_leakage_sha256')]:
 p='studio2/fase03/evidence/'+name;data=blob(A,p);out['pinned_036'].append({'path':p,**fp(data),'declared':f39[key],'match':fp(data)['sha256']==f39[key]})
assert all(x['match'] for x in out['pinned_036'])
f15=json.loads(blob(A,'studio2/fase03/paper_sections/FONTI_DELTA_0315.json'));out['sources_0315']=[]
for x in f15['sources']:
 c=x['commit'];data=blob(c,x['path']) if c else Path(x['path']).read_bytes();row={**x,'match':fp(data)=={k:x[k] for k in ['bytes','sha256']},'at_P':('ancestor' if anc(c,P) else 'external_commit') if c else 'local_uncommitted','at_A':('ancestor' if anc(c,A) else 'external_commit') if c else 'local_uncommitted'};out['sources_0315'].append(row)
out['sources_counts']={k:dict(collections.Counter(x[k] for x in out['sources_0315'])) for k in ['at_P','at_A']};assert all(x['match'] for x in out['sources_0315'])
out['runtime_files']=[]
for p in tree(A,'studio2/fase03/harness'):
 if not p.endswith('.py'):continue
 t=ast.parse(blob(A,p));imports=[];strings=[]
 for n in ast.walk(t):
  if isinstance(n,ast.Import):imports += [x.name for x in n.names]
  elif isinstance(n,ast.ImportFrom):imports.append('.'*n.level+(n.module or ''))
  elif isinstance(n,ast.Constant) and isinstance(n.value,str) and (n.value.startswith('/') or 'http://' in n.value or 'https://' in n.value):strings.append(n.value)
 out['runtime_files'].append({'path':p,'imports':imports,'absolute_or_url_literals':strings})
assert len(out['runtime_files'])==5
out['acquisitions']=[]
srcA=Path('/Users/luker/fot-tep-verifica-raccordo-e82b5a0');srcB=Path('/Users/luker/fot-tep-verifica-raccordo-0315-9b6bd64')
pairs=[(srcA/'studio2/fase03/VERIFICA_RACCORDO_DOCUMENTALE_036_0312_LETTERATURA.md','studio2/fase03/VERIFICA_RACCORDO_DOCUMENTALE_036_0312_LETTERATURA.md'),(srcB/'studio2/fase03/paper_sections/VERIFICA_RACCORDO_DOCUMENTALE_0315.md','studio2/fase03/paper_sections/VERIFICA_RACCORDO_DOCUMENTALE_0315.md'),(Path('/Users/luker/fot-tep/.worktrees/verifica-delta-raccordo-0315-10582798/studio2/fase03/paper_sections/VERIFICA_DELTA_RACCORDO_0315.md'),'studio2/fase03/paper_sections/VERIFICA_DELTA_RACCORDO_0315.md'),(Path('/Users/luker/fot-tep/Claude outputs/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE.md'),'studio2/fase03/harness/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE_ESECUTORE.md'),(Path('/Users/luker/fot-tep/.worktrees/integrazione-raccordo-metriche/_delivery/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE.md'),'studio2/fase03/harness/VERIFICA_INTEGRAZIONE_RACCORDO_METRICHE_INDIPENDENTE.md')]
for root,p in [(Path('/Users/luker/fot-tep-raccordo-036-0312-letteratura'),'studio2/fase03/CONSEGNA_RACCORDO_03_6_03_12_LETTERATURA_2026-09-14.md'),(Path('/Users/luker/fot-tep-raccordo-0315-local'),'studio2/fase03/paper_sections/CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md'),(Path('/Users/luker/fot-tep/.worktrees/acquisizione-raccordo-ok'),'studio2/fase03/harness/CONSEGNA_ACQUISIZIONE_OK_RACCORDO_METRICHE.md')]:pairs.append((root/p,p))
pairs.append((Path('/Users/luker/fot-tep/.worktrees/integrazione-raccordo-metriche/_delivery/REPORT_INTEGRAZIONE_RACCORDO_METRICHE.md'),'studio2/fase03/harness/REPORT_INTEGRAZIONE_RACCORDO_METRICHE.md'))
for src,p in pairs:
 data=src.read_bytes();out['acquisitions'].append({'source':str(src),'destination':p,**fp(data),'source_worktree_blob_equal':data==(W/p).read_bytes()==blob(A,p)})
assert all(x['source_worktree_blob_equal'] for x in out['acquisitions'])
out['bundles']=[]
for src,folder,expected in [(srcA,'studio2/fase03/evidenze_verifica_raccordo',30),(srcB,'studio2/fase03/paper_sections/evidenze_verifica_raccordo_0315',28)]:
 paths=tree(A,folder);assert len(paths)==expected
 entries=[]
 for p in paths:
  data=(src/p).read_bytes();entries.append({'path':p,**fp(data),'same':data==(W/p).read_bytes()==blob(A,p)})
 manifest=json.loads(blob(A,folder+'/MANIFEST_EVIDENZE.json'));manifest=manifest if isinstance(manifest,list) else manifest['files'];validated=[]
 for x in manifest:
  p=str(Path(x['path']).relative_to(src)) if x['path'].startswith('/') else x['path'];data=blob(A,p);validated.append({'original_path':x['path'],'mapped_relative_path':p,'match':fp(data)=={k:x[k] for k in ['bytes','sha256']}})
 assert len(validated)==expected and all(x['match'] for x in validated) and all(x['same'] for x in entries)
 assert not any(x['mapped_relative_path']==folder+'/MANIFEST_EVIDENZE.json' for x in validated)
 out['bundles'].append({'folder':folder,'files':entries,'manifest_validation':validated})
(O/'integrity.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'ancestor_checks':out['ancestors'],'packages':{k:len(v['files']) for k,v in out['packages'].items()},'R4':len(out['R4']),'sources':out['sources_counts'],'acquisitions':len(out['acquisitions']),'bundles':[len(x['manifest_validation']) for x in out['bundles']],'runtime':out['runtime_files']},indent=2))
