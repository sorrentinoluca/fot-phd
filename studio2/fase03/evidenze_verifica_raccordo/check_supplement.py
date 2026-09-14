from pathlib import Path
import subprocess,json,hashlib,re,csv,collections,datetime
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(ref,p):return git('show',ref+':'+p)
out={}
ps=git('ls-tree','-r','--name-only','2f6dd8d','--','studio2/fase03/evidence').decode().splitlines();out['evidence_vs_scientific_verified']=[{'path':p,'same':blob('2f6dd8d',p)==blob('e82b5a0',p)} for p in ps]
out['schema_core_vs_R4']=[{'path':p,'same':blob('3c64390','studio2/fase03/schema_insight/'+p)==blob('e82b5a0','studio2/fase03/schema_insight/'+p)} for p in ['SCHEMA_FREEZE.json','REPORT_SCHEMA_INSIGHT.md','DECISIONE_SCHEMA_INSIGHT.md']]
f=json.loads((R/'phase_b/PHASE_B_PROTOCOL_HASHES.json').read_text());out['frozen_source_hashes']=[{'path':p,'sha256':sha((R/p).read_bytes()),'match':sha((R/p).read_bytes())==f['artifacts'][p]} for p in ['code/tep_features.py','code/tep_verbalize_v2.py','code/verbalizer_config_v2.json','code/evaluate_verbalizer_v2.py']]
base='studio2/fase03/baseline_numerica/';hashes={x:sha((R/'studio2/fase03/evidence'/x).read_bytes()) for x in ['extract_evidence.py','leakage.py']}
out['evidence_pins']={p:{x:h in (R/base/p).read_text() for x,h in hashes.items()} for p in ['extract_normal_evidence.py','BASELINE_FREEZE_rev002.json','BASELINE_FREEZE_rev003.json','VERIFICA_BASELINE_NUMERICA.md']}
out['baseline_source9']=[{'path':e['path'],'match':sha((R/e['path']).read_bytes())==e['sha256']} for e in json.loads((R/base/'BASELINE_FREEZE_rev003.json').read_text())['source_files']]
with (R/'studio2/fase03/evidence/MANIFEST_CONSERVAZIONE.csv').open() as f:rows=list(csv.DictReader(f))
out['manifest_evidence']={'columns':list(rows[0]),'rows':len(rows),'unique_paths':len(set(x['path'] for x in rows)),'bytes':sum(int(x['bytes']) for x in rows)}
# Prove old walkthrough core sections unaffected and appended HTML source slices exact.
for ext in ['md','html']:
 p='docs/fot_walkthrough_conversazione_studio2.'+ext
 out['literal_sections_'+ext]={}
 for anchor,ref in [('evidence-697-d','7c99a83'),('schema-insight-0312','c9f83c6'),('soglie-normal-63','c486eee'),('pseudolabel-037','c486eee'),('normal-dev-baseline-039','c486eee')]:
  def section(ref):
   t=blob(ref,p)
   if ext=='html':
    start=t.index(('<section id="'+anchor+'">').encode());end=t.index(b'</section>',start)+len(b'</section>');return t[start:end]
   start=t.index(('<a id="'+anchor+'"></a>').encode());ends=[x for x in [t.find(b'<a id=',start+1),t.find(b'### Sintesi per sezione',start)] if x>=0];return t[start:min(ends) if ends else len(t)].rstrip()
  a,b=section('e82b5a0'),section(ref);out['literal_sections_'+ext][anchor]={'reference':ref,'same':a==b,'sha256':sha(a),'bytes':len(a)}
out['bibliographic_base_shared_unchanged']={p:blob('a572d1c',p)==blob('c486eee',p) for p in ['docs/letteratura.md','docs/letteratura.html','docs/paper/FoT_TEP_paper_blueprint.html','papers/README.md']}
out['source_status_final']=subprocess.check_output(['git','status','--porcelain=v1'],cwd='/Users/luker/fot-tep-raccordo-036-0312-letteratura').decode()
p='studio2/fase03/CONSEGNA_RACCORDO_03_6_03_12_LETTERATURA_2026-09-14.md';out['B_source_unchanged']=(Path('/Users/luker/fot-tep-raccordo-036-0312-letteratura')/p).read_bytes()==(O/'CONSEGNA_ESTERNA_B.md').read_bytes()
out['remote_observation']={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'refs':git('ls-remote','origin','refs/heads/main','refs/tags/studio2-fase03-schema-insight-frozen-001','refs/tags/studio2-fase03-schema-insight-frozen-001^{}').decode()}
out['local_tag_exists']=subprocess.run(['git','show-ref','--verify','--quiet','refs/tags/studio2-fase03-schema-insight-frozen-001'],cwd=R).returncode==0
out['diff_check']={'exit_code':subprocess.run(['git','diff','--check','c486eee','e82b5a0'],cwd=R,stdout=subprocess.DEVNULL).returncode,'by_path':dict(collections.Counter(re.findall(r'^([^:\n]+):\d+:',(O/'diff_check.log').read_text(errors='replace'),re.M)))}
(O/'supplement.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
