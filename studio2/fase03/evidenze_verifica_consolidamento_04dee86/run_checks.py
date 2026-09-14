from pathlib import Path
import subprocess,tempfile,tarfile,hashlib,json,os,sys,re,datetime
W=Path('/Users/luker/fot-tep-verifica-consolidamento-04dee86');O=Path(__file__).parent
root=Path(tempfile.mkdtemp(prefix='fot-tep-verifica-04dee86-'));out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.executable,'version':sys.version,'archive_root':str(root),'archives':[],'checks':[]}
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
for role,ref in [('candidate','04dee86140b3ff18882f9d164beef5ab7bf33e00'),('base','e82b5a08bf642ad45f77e71832958207beb1181c')]:
 archive=root/(role+'.tar');dest=root/role;dest.mkdir()
 with archive.open('wb') as f:subprocess.run(['git','-C',str(W),'archive','--format=tar',ref],stdout=f,check=True)
 with tarfile.open(archive) as t:
  assert not any(m.issym() or m.islnk() or m.name.startswith('/') or '..' in Path(m.name).parts for m in t.getmembers());t.extractall(dest)
 out['archives'].append({'role':role,'ref':ref,'directory':str(dest),'archive_bytes':archive.stat().st_size,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'git_dir_absent':not (dest/'.git').exists(),'symlinks':len([p for p in dest.rglob('*') if p.is_symlink()])})
 checks=[('guardiano_'+role,['python3','docs/test_explanation.py'])]
 if role=='candidate':checks=[('metriche',['python3','-m','unittest','studio2.fase03.harness.test_metric_raccordo','-v']),('lint',['python3','studio2/fase03/paper_sections/lint_paper_sections.py','--corpus','docs/letteratura.md'])]+checks
 for name,cmd in checks:
  p=subprocess.run(cmd,cwd=dest,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(O/(name+'.log')).write_bytes(p.stdout);txt=p.stdout.decode();out['checks'].append({'name':name,'cwd':str(dest),'command':cmd,'exit':p.returncode,'summary':re.findall(r'^(?:Ran .*|FAILED .*|OK|Lint.*|FAIL:.*|ERROR:.*|setUpClass.*skipped.*)$',txt,re.M)})
g={x['name']:x for x in out['checks']};g0=g['guardiano_base'];g1=g['guardiano_candidate'];out['guardian_identifiers_equal']=[x for x in g0['summary'] if x.startswith(('FAIL:','ERROR:','setUpClass'))]==[x for x in g1['summary'] if x.startswith(('FAIL:','ERROR:','setUpClass'))]
(O/'checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
