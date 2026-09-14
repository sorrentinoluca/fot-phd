"""Read-only independent provenance audit. Writes only beside this script."""
import csv, hashlib, json, pathlib, subprocess, tarfile, difflib

OUT = pathlib.Path(__file__).resolve().parent
ROOT = OUT.parent / 'candidate'
C = '59b6b93cd9c215e8b687e540f7cd579804b7c66a'
B = 'a00605862f627710347bd63c49f79a6d0a00135f'
S = '1ac06ebdc92f73d3b630ccca9bf75f413bea170b'
P = '6aaa5b3eebfed4ba502c25c0443caabd0051af21'
R = '3c64390bc4dd58c48cc4e1e388a38989b32b3143'
def git(*args): return subprocess.check_output(['git', '-C', str(ROOT), *args])
def blob(ref, path): return git('show', ref+':'+path)
def sha(raw): return hashlib.sha256(raw).hexdigest()
checks=[]
def check(kind, path, raw, digest=None, size=None, ref=C):
    row=dict(kind=kind, path=path, ref=ref, sha256=sha(raw), bytes=len(raw))
    row['ok']=(digest is None or row['sha256']==digest) and (size is None or len(raw)==size)
    if digest: row['expected_sha256']=digest
    checks.append(row)

manifest_path='studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json'
raw=blob(C,manifest_path)
check('candidate_manifest',manifest_path,raw,'751b95a8bce62c4f8acbf907ba1cbfcf01850538711ae9dfe6928f62ebd430d3')
m=json.loads(raw)
for row in m['files']: check('candidate_file',row['path'],blob(C,row['path']),row['sha256'],row['bytes'])
for group in ['recovered_byte_identical_from_1ac06eb','adapted_from_1ac06eb']:
    for path in m['recovery'][group]:
        a,b=blob(S,path),blob(C,path)
        checks.append(dict(kind=group,path=path,source_commit=S,source_sha256=sha(a),candidate_sha256=sha(b),identical=a==b,ok=(a==b)==group.startswith('recovered')))
        (OUT/('recovery_'+pathlib.Path(path).name+'.diff')).write_text(''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile=S+':'+path,tofile=C+':'+path)))
for path in m['preserved_qualified_metric_files']:
    check('metric_unchanged',path,blob(C,path),sha(blob(B,path)))
diff=git('diff','--name-status',B,C).decode();(OUT/'candidate_delta.txt').write_text(diff)
assert not any(x in diff for x in ['/piano_statistico/','APERTURA_SOTTOFASI','walkthrough'])
for path,digest in [('PIANO_STATISTICO.md',m['normative_sources']['statistical_plan_sha256']),('PIANO_STATISTICO_FREEZE.json',m['normative_sources']['statistical_manifest_sha256']),('DELTA_HARNESS_03_10.md',m['normative_sources']['delta_harness_sha256'])]:
    full='studio2/fase03/piano_statistico/'+path;raw=blob(P,full)
    check('plan_pin',full,raw,digest,ref=P);(OUT/'sources'/(P[:8]+'_'+path)).write_bytes(raw)
schema=json.loads(blob(R,'studio2/fase03/schema_insight/SCHEMA_FREEZE.json'))
for row in schema['files']+schema['source_files']:
    ref=R if row in schema['files'] else ('a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155' if 'source_ref' in row else schema['base_commit'])
    check('r4_manifest_member',row['path'],blob(ref,row['path']),row['sha256'],row['bytes'],ref)
baseline=json.loads(blob(B,'studio2/fase03/baseline_numerica/BASELINE_FREEZE_rev005.json'))
for row in baseline['source_files']+baseline['revision_chain']+baseline['published_evidence']:
    check('baseline_pin',row['path'],blob(B,row['path']),row['sha256'],ref=B)
inventory=json.loads(blob(C,'studio2/fase03/harness/PILOT_INPUT_SOURCES.pending.json'))
for key in ['pseudolabel','agent_assignment','derangements','normal_handoff']:
    row=inventory['sources'][key];check('input_pin',row['path'],blob(C,row['path']),row['sha256'])
for tag in ['studio2-fase03-schema-insight-frozen-001','studio2-fase03-baseline-numerica-frozen-001','studio2-fase03-pseudolabel-frozen-001']:
    local=git('rev-parse',tag,tag+'^{}').decode().splitlines()
    remote=subprocess.check_output(['git','-C',str(ROOT),'ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/tags/'+tag,'refs/tags/'+tag+'^{}']).decode()
    checks.append(dict(kind='tag',tag=tag,object=local[0],peeled=local[1],remote=remote,ok=all(x in remote for x in local)))

# Re-read an existing archive by its bytes; no inference, extraction pipeline or API.
archive=pathlib.Path('/private/tmp/fot-tep-evidence-v2-redownload-curl-001/studio2-fase03-evidence-v2.tar')
check('evidence_archive',str(archive),archive.read_bytes(),m['normative_sources']['evidence_archive_sha256'],62185472,ref='existing local release copy, independently rehashed')
conservation=list(csv.DictReader(blob(B,'studio2/fase03/evidence/MANIFEST_CONSERVAZIONE.csv').decode().splitlines()))
with tarfile.open(archive) as tar:
    members={x.name:x for x in tar.getmembers() if x.isfile()}
    assert len(members)==1283
    for row in conservation:
        raw=tar.extractfile(members[row['path']]).read()
        check('archive_member',row['path'],raw,row['sha256'],int(row['bytes']),ref='verified evidence-v2 tar')
        assert sha(raw)==row['sha256']
        destination=OUT/'reference'/row['path']
        assert destination.resolve().is_relative_to((OUT/'reference').resolve())
        destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(raw)

import sys
sys.path.insert(0,str(ROOT))
from studio2.fase03.harness.inputs import build_inventory
rebuilt,executable=build_inventory(evidence_root=OUT/'reference/studio2/fase03/evidence/output',pseudolabel_path=ROOT/'studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json',assignment_path=ROOT/'studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json',derangement_path=ROOT/'studio2/fase03/pseudolabel/CONDITION_E_DERANGEMENTS.json',normal_handoff=ROOT/'studio2/fase03/baseline_numerica/NORMAL_DEV_HANDOFF.json',assembly_base_commit=B)
assert rebuilt==inventory and executable is None
checks.append(dict(kind='inventory_rebuild',ok=True,cases=len(rebuilt['development_cases']),local_faults=len(rebuilt['local_example_provenance']),normal_examples=8,fixed_contracts=len(rebuilt['fixed_insight_contracts']),equal_to_candidate=True,executable=None))
(OUT/'integrity.json').write_text(json.dumps(checks,indent=2))
print(json.dumps({'checks':len(checks),'failures':[x for x in checks if not x['ok']]},indent=2))
