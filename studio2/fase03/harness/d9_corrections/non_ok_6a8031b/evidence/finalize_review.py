import pathlib,json,hashlib,re,subprocess,os,time
r=pathlib.Path.cwd();o=r/'outputs/d9-review';e=o/'evidence';c=r/'work/candidate'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def parse(name):
 log=(e/(name+'.log')).read_text();m=re.search(r'Ran (\d+) tests? in ([0-9.]+)s',log)
 if not m:raise RuntimeError('unfinished log '+name)
 last=next(x for x in reversed(log.splitlines()) if x == 'OK' or x.startswith(('OK (','FAILED (')));n=lambda k:int(re.search(k+r'=(\d+)',last)[1]) if re.search(k+r'=(\d+)',last) else 0
 return {'tests':int(m[1]),'seconds':float(m[2]),'failures':n('failures'),'errors':n('errors'),'skipped':n('skipped'),'summary':last,'log':name+'.log'}
for name in ['targeted','discovery','d9','antecedent','guardian']:
 assert (e/(name+'_command.json')).exists(),name+' still running'
res={n:parse(n) for n in ['targeted','discovery','d9','antecedent','guardian','independent_probes','independent_probes_antecedent']}
(e/'RESULTS.json').write_text(json.dumps(res,indent=2))
observed=[l.removeprefix('FAIL: ') for l in (e/'guardian.log').read_text().splitlines() if l.startswith('FAIL: ')]
expected=json.loads((c/'studio2/fase03/harness/d9_evidence/guardian_comparison.json').read_text())['failure_ids']
g={'status':'NON PASS','observed_failure_ids':observed,'expected_failure_ids':expected,'same_identifiers':sorted(observed)==sorted(expected),'result':res['guardian']}
(e/'guardian_comparison_independent.json').write_text(json.dumps(g,indent=2))
assert g['same_identifiers'];assert res['guardian']['tests']==35 and res['guardian']['failures']==14 and res['guardian']['errors']==0 and res['guardian']['skipped']==1
before=json.loads((e/'original_tracked_before.json').read_text());pres={}
for base,files in before.items():
 mismatches=[p for p,h in files.items() if not (pathlib.Path(base)/p).is_file() or sha(pathlib.Path(base)/p)!=h]
 status=subprocess.check_output(['git','-C',base,'status','--porcelain=v1'],text=True)
 pres[base]={'files_compared':len(files),'mismatches':mismatches,'status':status,'head':subprocess.check_output(['git','-C',base,'rev-parse','HEAD'],text=True).strip()}
 assert not mismatches and not status
m=json.loads((c/'studio2/fase03/harness/HARNESS_D9_CANDIDATE.json').read_text());bad=[x['path'] for x in m['files'] if sha(c/x['path'])!=x['sha256'] or (c/x['path']).stat().st_size!=x['bytes']]
pres['snapshot_manifest_mismatches']=bad;assert not bad
pres['review_thread_id']=os.environ.get('CODEX_THREAD_ID');pres['remote_was_not_contacted']=True
(e/'preservation_final.json').write_text(json.dumps(pres,indent=2))
labels={'targeted':'Suite mirata fornita','discovery':'Discovery completa fornita','d9':'D9 finale fornito','antecedent':'Stesso D9 finale su aae29a9','independent_probes':'Sonde indipendenti finali U01–U08','independent_probes_antecedent':'Stesse U04–U07 su aae29a9','guardian':'Guardiano documentale'}
table=['| Prova | Metodi | Fallimenti | Errori | Skip | Secondi | Log |','| --- | ---: | ---: | ---: | ---: | ---: | --- |']
for n in labels:
 x=res[n];table.append(f"| {labels[n]} | {x['tests']} | {x['failures']} | {x['errors']} | {x['skipped']} | {x['seconds']:.3f} | [{n}.log](evidence/{n}.log) |")
guard='⚠️ **Guardiano storico NON PASS:**35 test,14 fallimenti,1 skip,0 errori. Gli identificativi dei14 FAIL, inclusi i subtest, coincidono con guardian_comparison.json del candidato. Non è PASS e non dimostra correttezza del delta. Il confronto nominativo è in [guardian_comparison_independent.json](evidence/guardian_comparison_independent.json); il log completo è conservato. Nessuna correzione alla documentazione storica.'
s=(r/'work/VERIFICA_D9.template.md').read_text().replace('{{RESULTS_TABLE}}','\n'.join(table)).replace('{{GUARDIAN}}',guard)
assert '{{' not in s
(o/'VERIFICA_D9.md').write_text(s)
# Verify report relative artifact links, including not-yet-written final manifest.
missing=[]
for target in re.findall(r'\]\(([^)]+)\)',s):
 if target=='MANIFEST.json':continue
 if not (o/target).exists():missing.append(target)
assert not missing,missing
print(json.dumps({'results':res,'preserved':{k:v for k,v in pres.items() if k!='snapshot_manifest_mismatches'},'report_bytes':(o/'VERIFICA_D9.md').stat().st_size},indent=2))
