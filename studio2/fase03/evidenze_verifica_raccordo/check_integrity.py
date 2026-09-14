from pathlib import Path
import subprocess,json,hashlib,re,collections
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent
A='e82b5a08bf642ad45f77e71832958207beb1181c';BASE='c486eee95fe24c1e7bf4135ed7cebf01ac2962f1'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def blob(ref,p):return git('show',ref+':'+p)
def info(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def paths(ref,p):return git('ls-tree','-r','--name-only',ref,'--',p).decode().splitlines()
def comp(ref,ps):return [{'path':p,'ref':ref,**info(blob(A,p)),'same':blob(A,p)==blob(ref,p),'disk_same':(R/p).read_bytes()==blob(A,p)} for p in ps]
out={}
refs=['c486eee','7c99a83','cf1f70f','daf5dc5','d54fa4a','2f6dd8d','54bbd0c','bb6d9e7','c66bd8d','3c64390','43b31af','c0f4da0','9b1fac9','c9f83c6','e37c3db','40911d0','5806871','903f37f','601fb70']
out['ancestry']=[{'commit':git('rev-parse',r).decode().strip(),'ancestor_A':subprocess.run(['git','merge-base','--is-ancestor',r,A],cwd=R).returncode==0,'ancestor_base':subprocess.run(['git','merge-base','--is-ancestor',r,BASE],cwd=R).returncode==0,'parents':git('show','-s','--format=%P',r).decode().strip()} for r in refs]
out['evidence']=comp('c66bd8d',paths('c66bd8d','studio2/fase03/evidence'))
out['evidence_delta']=git('diff','--name-status','c66bd8d',A,'--','studio2/fase03/evidence').decode()
out['schema']=comp('c9f83c6',paths('c9f83c6','studio2/fase03/schema_insight'))
out['schema_delta']=git('diff','--name-status','c9f83c6',A,'--','studio2/fase03/schema_insight').decode()
f=json.loads(blob(A,'studio2/fase03/schema_insight/SCHEMA_FREEZE.json'));checks=[]
for group,ref in [('files','3c64390'),('source_files',f['base_commit'])]:
 for e in f[group]:
  rr=re.search(r'[a-f0-9]{40}',e.get('source_ref',''));rr=rr.group() if rr else ref
  actual=info(blob(rr,e['path']));checks.append({'path':e['path'],'ref':rr,**actual,'match':all(actual[k]==e[k] for k in ['bytes','sha256']),'current_same':blob(A,e['path'])==blob(rr,e['path']),'frozen_same':blob(rr,e['path'])==blob(e['frozen_tag_commit'],e['path']) if 'frozen_tag_commit' in e else None})
out['manifest18']=checks;out['previous_manifest_match']=info(blob('e058cb0','studio2/fase03/schema_insight/SCHEMA_FREEZE.json'))['sha256']==f['previous_manifest_sha256']
invpath=Path('/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/ACQUISIZIONE_LETTERATURA_03_8.json');inv=json.loads(invpath.read_bytes());out['inventory_source']={'path':str(invpath),**info(invpath.read_bytes())}
for group in ['files','protected_files']:
 rows=[]
 for e in inv[group]:
  actual=info(blob(A,e['path']));rows.append({'path':e['path'],**actual,'match':all(actual[k]==e[k] for k in ['bytes','sha256'] if k in e)})
 out['literature_'+group]=rows
out['literature_committed']=comp('e37c3db', [e['path'] for e in inv['files']]);out['png_modes']=git('ls-tree','-r',A,'--','papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images').decode()
hist=[('/Users/luker/fot-tep-integrazione-evidence-036','studio2/fase03/evidence/CONSEGNA_INTEGRAZIONE_03_6.md'),('/Users/luker/fot-tep-schema-insight-r4-integrazione','studio2/fase03/schema_insight/CONSEGNA_LOCALE_SCHEMA_INSIGHT_R4.md'),('/Users/luker/fot-tep-letteratura-fase03','docs/lit_review/CONSEGNA_ACQUISIZIONE_LETTERATURA_FASE03_2026-09-14.md')]
out['historical_deliveries']=[{'path':p,'source':root,**info(blob(A,p)),'source_same':blob(A,p)==(Path(root)/p).read_bytes(),'acquisition_same':blob(A,p)==blob('601fb70',p)} for root,p in hist]
out['evidences']=comp('43b31af',['studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md','studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev004.txt'])+comp('40911d0',['docs/lit_review/VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md'])
out['non_ok_source_same']=blob(A,'studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004_NON_OK_STORICO.md')==Path('/Users/luker/fot-tep-verifica-schema-insight-rev004/studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md').read_bytes()
changes=git('diff','--name-status',BASE,A).decode().splitlines();out['changes']=changes
# New changes confined to package imports, handoffs and three narrative files.
allowed={e['path'] for e in out['evidence']+out['schema']+out['literature_files']+out['evidences']}|{p for _,p in hist}|{'studio2/PROVENIENZA.md','docs/fot_walkthrough_conversazione_studio2.md','docs/fot_walkthrough_conversazione_studio2.html','studio2/fase03/CONSEGNA_RACCORDO_03_6_03_12_LETTERATURA_2026-09-14.md'}
out['unexpected_paths']=[c for c in changes if c.split('\t')[-1] not in allowed]
out['protected_delta']=git('diff','--name-status',BASE,A,'--','code','phase_b','icl','ablation','reproducibility','studio2/fase03/baseline_numerica','studio2/fase03/harness','studio2/fase03/selection','studio2/fase03/pseudolabel','studio2/fase03/piano_statistico','studio2/fase03/paper_sections').decode()
out['ahead']=int(git('rev-list','--count',BASE+'..'+A));b=(O/'CONSEGNA_ESTERNA_B.md').read_text();decl=re.findall(r'^- `([AM])` `([^`]+)`$',b,re.M);out['B_inventory_matches']=sorted('\t'.join(x) for x in decl)==sorted(changes)
out['guard_script_same']=blob(A,'docs/test_explanation.py')==blob(BASE,'docs/test_explanation.py')
logs=[(O/x).read_text() for x in ['guardiano_base.log','guardiano_A.log']]
fail=[[l for l in t.splitlines() if l.startswith('FAIL:')] for t in logs];skip=[[l for l in t.splitlines() if '... skipped ' in l] for t in logs]
out['guardian']={'failure_ids_equal':fail[0]==fail[1],'failure_ids':fail[1],'skip_equal':skip[0]==skip[1],'skip':skip[1],'normalized_full_logs_equal':re.sub(r'Ran 35 tests in [0-9.]+s','TIME',logs[0].replace('/Users/luker/fot-tep-verifica-raccordo-base-c486eee','ROOT'))==re.sub(r'Ran 35 tests in [0-9.]+s','TIME',logs[1].replace(str(R),'ROOT'))}
(O/'integrity.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
for k,v in out.items():
 if isinstance(v,list):print(k,len(v), 'bad=',sum(1 for x in v if isinstance(x,dict) and any(x.get(z) is False for z in ['same','match','source_same','disk_same'])))
 elif k!='guardian':print(k,str(v)[:450])
print('guardian',out['guardian'])
