"""Independent read-only audit of exact commits and acquired prior evidence."""
import hashlib, json, subprocess, pathlib, collections, ast
E=pathlib.Path(__file__).resolve().parent
C=E.parent/'candidate'
OLD=pathlib.Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence')
TECH='0c8157f23bee49a3a5a2df648525c34706da29d7'
DOC='6268437b8b64288b50ad5f7c924e1fcab85b27d3'
BASE='a00605862f627710347bd63c49f79a6d0a00135f'
def git(*args):return subprocess.check_output(['git','-C',str(C),*args])
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[]
def check(kind,path,raw,expected,size=None):
    checks.append(dict(kind=kind,path=str(path),sha256=sha(raw),bytes=len(raw),expected_sha256=expected,ok=sha(raw)==expected and (size is None or len(raw)==size)))
m_path='studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json'
mraw=(C/m_path).read_bytes();m=json.loads(mraw)
check('manifest',m_path,mraw,'8ed9fbc37ee14d162ce65f55430159bb1e2507e95cf65aa8d72df3743170dbe1',11662)
for r in m['files']:
    check('candidate-member',r['path'],(C/r['path']).read_bytes(),r['sha256'],r['bytes'])
    check('checkout-vs-commit',r['path'],(C/r['path']).read_bytes(),sha(git('show',TECH+':'+r['path'])))
acq_root=C/'studio2/fase03/harness/non_ok_20260915'
acq=json.loads((acq_root/'ACQUISIZIONE.json').read_text())
for r in acq['files']:
    path=acq_root/'evidence'/r['path'] if r['storage']=='acquired' else pathlib.Path(r['source'])
    check('acquisition-'+r['storage'],path,path.read_bytes(),r['sha256'],r['bytes'])
    check('original-preserved',r['source'],pathlib.Path(r['source']).read_bytes(),r['sha256'],r['bytes'])
check('prior-manifest',OLD/'SHA256SUMS',(OLD/'SHA256SUMS').read_bytes(),'0d25177f41ef9651ee246d5ad8610c020e43c931e168f3c18ba9098d871f0223')
for r in m.get('preserved_qualified_metric_files',[]):
    check('metric-vs-published',r,(C/r).read_bytes(),sha(git('show',BASE+':'+r)))
# Every path outside technical diff is compared against the acquisition parent.
parent=git('rev-parse',TECH+'^').decode().strip()
delta=git('diff','--name-status',parent,TECH).decode();(E/'technical_delta.txt').write_text(delta)
(E/'technical_diff.patch').write_bytes(git('diff',parent,TECH))
ddelta=git('diff','--name-status',TECH,DOC).decode();(E/'documentary_delta.txt').write_text(ddelta)
# Keep module origin distinctions explicit, including byte-identical recovered modules.
old_manifest=json.loads(git('show','59b6b93cd9c215e8b687e540f7cd579804b7c66a:'+m_path))
for group in ['recovered_byte_identical_from_1ac06eb','adapted_from_1ac06eb']:
    for path in old_manifest['recovery'][group]:
        origin=git('show','1ac06ebdc92f73d3b630ccca9bf75f413bea170b:'+path)
        old=git('show','59b6b93cd9c215e8b687e540f7cd579804b7c66a:'+path)
        new=(C/path).read_bytes()
        checks.append(dict(kind='module-provenance',path=path,source_sha256=sha(origin),old_sha256=sha(old),new_sha256=sha(new),unchanged_since_old=old==new,identical_to_recovery=origin==new,ok=True))
for tag in ['studio2-fase03-schema-insight-frozen-001','studio2-fase03-baseline-numerica-frozen-001','studio2-fase03-pseudolabel-frozen-001']:
    local=git('rev-parse',tag,tag+'^{}').decode().splitlines()
    remote=git('ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/tags/'+tag,'refs/tags/'+tag+'^{}').decode()
    checks.append(dict(kind='remote-tag',path=tag,object=local[0],peeled=local[1],remote=remote,ok=all(x in remote for x in local)))
# Recheck all historical exact-source positive integrity assertions (no extraction).
prior=json.loads((OLD/'integrity.json').read_text())
for r in prior:
    if r['kind'] in ('r4_manifest_member','baseline_pin','plan_pin','input_pin'):
        raw=git('show',r['ref']+':'+r['path'])
        check('exact-source-'+r['kind'],r['ref']+':'+r['path'],raw,r['sha256'],r['bytes'])
methods=[]
tree=ast.parse((OLD/'negative_probes.py').read_text())
for cls in tree.body:
    if isinstance(cls,ast.ClassDef):
        for f in cls.body:
            if isinstance(f,ast.FunctionDef) and f.name.startswith('test_'):
                methods.append(dict(class_name=cls.name,name=f.name,number=int(f.name.split('_')[1]),line=f.lineno))
(E/'original_methods.json').write_text(json.dumps(methods,indent=2)+'\n')
result=dict(technical=TECH,tree=git('rev-parse',TECH+'^{tree}').decode().strip(),parent=parent,documentary=DOC,
            remote_main=git('ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/heads/main').decode().strip(),
            acquisition_counts=dict(collections.Counter(r['storage'] for r in acq['files'])),
            original_method_count=len(methods),checks=checks)
(E/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),failures=[r for r in checks if not r['ok']],acquisition=result['acquisition_counts'],methods=len(methods)),indent=2))
