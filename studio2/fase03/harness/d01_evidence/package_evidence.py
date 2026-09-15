from pathlib import Path
import hashlib,json,re,shutil
root=Path('/Users/luker/fot-tep-harness-0310-d01');src=Path('/Users/luker/fot-tep-harness-0310-d01-checks');dst=root/'studio2/fase03/harness/d01_evidence'
for log,n in [('d01.log',7),('targeted.log',103),('discovery.log',138)]:
 s=(src/log).read_text();assert f'Ran {n} tests' in s and re.search(r'^OK$',s,re.M),log
expected={'before/evidence/edge_probes.json':(7,2,0),'after/evidence/edge_probes.json':(7,0,0),'literal/evidence/extended.json':(18,0,0),'literal/evidence/additional_edges/additional.json':(6,1,0),'x23_adapted/evidence/additional_edges/additional.json':(1,0,0)}
for n,counts in expected.items():
 value=json.loads((src/n).read_text());assert (value['tests'],len(value['failures']),len(value['errors']))==counts,n
before=json.loads((src/'before/evidence/edge_probes.json').read_text())
assert all(any(k in v['test'] for v in before['failures']) for k in ['Y01','Y02'])
rows=[];links=[]
for p in sorted(src.rglob('*')):
 rel=p.relative_to(src)
 if p.is_symlink():links.append(dict(path=str(p),target=str(p.readlink())));continue
 if not p.is_file():continue
 copied=not any(k in {'fixtures','edge_fixtures','extended_fixtures'} for k in rel.parts)
 b=p.read_bytes();sha=hashlib.sha256(b).hexdigest()
 if copied:
  q=dst/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert q.read_bytes()==b
 rows.append(dict(source=str(p),relative_path=str(rel),sha256=sha,bytes=len(b),disposition='copied_byte_identical' if copied else 'external_verified',reason=None if copied else 'Sacrificial fixture preserved at exact source; not scientific input'))
(dst/'REPRODUCTION_INVENTORY.json').write_text(json.dumps(dict(files=rows,symlinks=links),indent=2)+'\n')
results=dict(targeted=dict(tests=103,failures=0,errors=0),discovery=dict(tests=138,failures=0,errors=0),new_regressions=7,applicable=dict(tests=14,failures=0,errors=0),before_Y=dict(tests=7,failures=2,errors=0),after_Y=dict(tests=7,failures=0,errors=0),extended_X=dict(literal_conforming=23,adapted_conforming=1,literal_X23_failure_preserved=True,new_adaptations=False),documentation=json.loads((src/'documentation_comparison.json').read_text()),compile=json.loads((src/'compile.json').read_text()),copied_files=sum(r['disposition']=='copied_byte_identical' for r in rows),external_files=sum(r['disposition']=='external_verified' for r in rows))
(dst/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
files=sorted(p for p in dst.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
(dst/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(dst))+'\n' for p in files))
print(json.dumps(results,indent=2))
