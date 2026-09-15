import pathlib,subprocess,json,hashlib,platform,sqlite3,sys
root=pathlib.Path.cwd(); e=root/'outputs/d9-review/evidence'; repo='/Users/luker/fot-tep-harness-d9'; c=root/'work/candidate'; h=c/'studio2/fase03/harness'
def git(*a):return subprocess.check_output(['git','-C',repo,*a])
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((h/'HARNESS_D9_CANDIDATE.json').read_text()); print('manifest keys',list(m))
checks=[]
for x in m['files']:
 b=(c/x['path']).read_bytes(); checks.append({'path':x['path'],'ok':len(b)==x['bytes'] and sha(b)==x['sha256']})
sources=[]
for x in json.loads((h/'d9_evidence/SOURCES.json').read_text()):
 b=git('show',x['commit']+':'+x['path']);sources.append(dict(x,ok=b==(c/x['copy']).read_bytes() and len(b)==x['bytes'] and sha(b)==x['sha256']))
t=json.loads((h/'d9_evidence/TESTED_BYTES.json').read_text()); print('tested keys',list(t))
(e/'integrity.json').write_text(json.dumps({'manifest_sha256':sha((h/'HARNESS_D9_CANDIDATE.json').read_bytes()),'members':checks,'sources':sources},indent=2))
(e/'runtime.json').write_text(json.dumps({'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'machine':platform.machine(),'sqlite':sqlite3.sqlite_version},indent=2))
changes=git('diff','--name-only','5886c6f','6a8031b').decode().splitlines();(e/'delta_paths.json').write_text(json.dumps(changes,indent=2))
(e/'runtime.diff').write_bytes(git('diff','5886c6f','6a8031b','--','*.py'))
tracked={}
for base in [repo,'/Users/luker/fot-tep-harness-0310-d04']:
 paths=subprocess.check_output(['git','-C',base,'ls-files','-z']).decode().split('\0');tracked[base]={p:sha((pathlib.Path(base)/p).read_bytes()) for p in paths if p and (pathlib.Path(base)/p).is_file()}
(e/'original_tracked_before.json').write_text(json.dumps(tracked,indent=2))
print('members',len(checks),'bad',sum(not x['ok'] for x in checks),'sources',len(sources),'bad',sum(not x['ok'] for x in sources))
