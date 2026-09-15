from pathlib import Path
import hashlib,json,re,shutil,subprocess
root=Path('/Users/luker/fot-tep-harness-0310-c01-c03');src=Path('/Users/luker/fot-tep-harness-0310-c01-c03-checks');dst=root/'studio2/fase03/harness/c01_c03_evidence'
assert 'Ran 96 tests' in (src/'targeted.log').read_text() and (src/'targeted.log').read_text().rstrip().endswith('OK')
assert 'Ran 131 tests' in (src/'discovery.log').read_text() and re.search(r'^OK$', (src/'discovery.log').read_text(), re.M)
expected={'before/evidence/extended.json':(18,4,0),'before/evidence/additional_edges/additional.json':(6,0,0),'after/evidence/extended.json':(18,0,0),'after/evidence/additional_edges/additional.json':(6,1,0),'x23_adapted/evidence/additional_edges/additional.json':(1,0,0)}
for p,counts in expected.items():
 value=json.loads((src/p).read_text());assert (value['tests'],len(value['failures']),len(value['errors']))==counts,(p,value)
first=json.loads((src/'before/evidence/extended.json').read_text())
assert all(any(k in row['id'] for row in first['failures']) for k in ['X01','X02','X03','X15'])
rows=[];links=[]
for p in sorted(src.rglob('*')):
 rel=p.relative_to(src)
 if p.is_symlink():links.append({'path':str(p),'target':str(p.readlink())});continue
 if not p.is_file():continue
 # Keep complete source observations, logs and scripts; large sacrificial fixture trees remain on disk.
 copy=not any(x in {'fixtures','extended_fixtures'} for x in rel.parts)
 b=p.read_bytes();sha=hashlib.sha256(b).hexdigest()
 row=dict(path=str(rel),source=str(p),sha256=sha,bytes=len(b),disposition='copied_byte_identical' if copy else 'external_verified',reason=None if copy else 'Sacrificial fixture tree kept at exact external location; never a scientific input')
 if copy:
  out=dst/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out);assert out.read_bytes()==b
 rows.append(row)
summary=dict(targeted_tests=96,targeted_failures=0,discovery_tests=131,discovery_failures=0,new_regressions=14,applicable_original_tests=14,applicable_failures=0,
             before_extended=dict(tests=24,failed_assertions=4,errors=0),after_extended=dict(distinct_methods=24,literal_conforming=23,adapted_conforming=1,literal_X23_failure_preserved=True),
             documentation=dict(tests=35,failures=14,skips=1,identifiers_unchanged=True,status='NOT_PASS'),
             scope=json.loads((src/'protected_scope.json').read_text()),runtime=json.loads((src/'runtime.json').read_text()),
             copied_files=sum(r['disposition']=='copied_byte_identical' for r in rows),external_files=sum(r['disposition']=='external_verified' for r in rows))
(dst/'REPRODUCTION_INVENTORY.json').write_text(json.dumps(dict(files=rows,symlinks=links),indent=2)+'\n')
(dst/'RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
files=[p for p in dst.rglob('*') if p.is_file() and p.name!='SHA256SUMS']
(dst/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(dst))+'\n' for p in sorted(files)))
print(json.dumps({k:v for k,v in summary.items() if k not in {'scope','runtime'}},indent=2))
