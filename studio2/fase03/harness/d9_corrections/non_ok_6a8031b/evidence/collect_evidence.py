import pathlib,shutil,json,hashlib,subprocess,ast,os
r=pathlib.Path.cwd();e=r/'outputs/d9-review/evidence';c=r/'work/candidate';h=c/'studio2/fase03/harness';ref=e/'references';ref.mkdir(exist_ok=False)
files=['docs/MAINTENANCE.md','docs/prompts/Prompt_LLM.md','docs/prompts/Verifica_LLM.md','studio2/fase03/harness/CONTRATTO_D9_PRIMA_DEL_CODICE.md','studio2/fase03/harness/CONTRATTO_D03_PRIMA_DEL_CODICE.md','studio2/fase03/harness/CONTRATTO_D04_PRIMA_DEL_CODICE.md','studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md','studio2/fase03/harness/HARNESS_D9_CANDIDATE.json','studio2/fase03/harness/d9_evidence/TESTED_BYTES.json','studio2/fase03/harness/d9_evidence/D9_FIELD_CONTRACT.json','studio2/fase03/harness/d9_evidence/SOURCES.json','studio2/fase03/harness/d9_evidence/COMANDI.md','studio2/fase03/harness/d9_evidence/ADATTAMENTI_E_LIMITI.md','studio2/fase03/harness/d9_evidence/guardian_comparison.json','studio2/fase03/schema_insight/DECISIONE_SCHEMA_INSIGHT.md']
for p in files:
 dest=ref/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(c/p,dest)
shutil.copytree(h/'d9_evidence/sources',ref/'sources')
for p in ['REPORT_D9.md','PROMPT_VERIFICA_D9.md','CONSEGNA_D9.json']:
 shutil.copy2(pathlib.Path('/Users/luker/fot-tep-harness-d9/studio2/fase03/harness')/p,ref/p)
shutil.copy2('/Users/luker/fot-tep/studio2/fase03/HANDOFF_FASE03_2026-09-15_rev03.md',ref/'HANDOFF_rev03.md')
for p in ['SKILL.md','references/lessons-and-evidence.md']:
 shutil.copy2(pathlib.Path('/Users/luker/.codex/skills/fot-tep-harness-lessons')/p,ref/pathlib.Path(p).name)
shutil.copy2(r/'work/run_suites.py',e/'run_suites.py');shutil.copy2(r/'work/audit_identity.py',e/'audit_identity.py')
compiled=[]
for p in (c/'studio2/fase03').rglob('*.py'):
 if any(x.startswith(('non_ok','evidenz','d04_ok')) for x in p.parts) or '/evidence/' in str(p) or '_evidence/' in str(p):continue
 try:compile(p.read_bytes(),str(p),'exec');error=None
 except Exception as ex:error=repr(ex)
 compiled.append({'path':str(p.relative_to(c)),'error':error})
(e/'compile_independent.json').write_text(json.dumps(compiled,indent=2))
print('compiled',len(compiled),'errors',sum(x['error'] is not None for x in compiled))
# Record specific legacy read dependencies; no mutation or execution here.
s= (h/'test_d01_replay.py').read_text();(e/'legacy_dependency_references.txt').write_text('\n'.join(x for x in s.splitlines() if '/Users/' in x or 'LEGACY' in x))
