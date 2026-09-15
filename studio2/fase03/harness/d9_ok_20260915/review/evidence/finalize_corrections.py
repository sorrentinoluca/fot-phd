from pathlib import Path
import hashlib,json,subprocess,re,tarfile,gzip
W=Path('/Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review');O=W/'outputs/d9-corrections-review';E=O/'evidence';C=W/'work/corrections-candidate';S=Path('/Users/luker/fot-tep-harness-d9-correzioni')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def validate(root,items):
 for name,i in items.items():
  p=root/name;assert p.is_file() and p.stat().st_size==i['bytes'] and sha(p)==i['sha256'],str(p)
 return len(items)
before=json.loads((E/'before.json').read_text());verified={root:validate(Path(root),items) for root,items in before.items()}
verified[str(C)]=validate(C,json.loads((E/'source_inventory.json').read_text()))
audit=json.loads((E/'source_audit.json').read_text());legacy=Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output');verified[str(legacy)]=validate(legacy,audit['legacy_reference_inventory'])
results=json.loads((E/'TEST_RESULTS.json').read_text())
expected={'targeted':(156,0,0,0),'discovery':(191,0,0,0),'corrections_red':(11,32,0,0),'corrections_green':(11,0,0,0),'original_U_red':(8,3,0,0),'original_U_green':(8,0,0,0),'transport_red':(3,2,0,0),'transport_green':(3,0,0,0),'guardian_rejected':(35,14,0,1),'guardian_corrected':(35,14,0,1)}
for name,counts in expected.items():
 s=(E/(name+'.log')).read_text();n=int(re.findall(r'Ran (\d+) tests?',s)[-1]);end=s[s.rfind('\nRan '):];actual=(n,*[int(re.search(k+r'=(\d+)',end).group(1)) if re.search(k+r'=(\d+)',end) else 0 for k in ('failures','errors','skipped')]);assert actual==counts,(name,actual);assert results[name]['exit_code']==int(counts[1]>0),(name,results[name]['exit_code']);results[name]['counts']=actual
ids={name:re.findall(r'^FAIL: .+$',(E/(name+'.log')).read_text(),re.M) for name in ('guardian_rejected','guardian_corrected')};assert ids['guardian_rejected']==ids['guardian_corrected'] and len(ids['guardian_corrected'])==14
oldlogs=list((W/'outputs/d9-review/evidence').rglob('*guardian*.log'));ids['old_review_comparisons']={str(p.relative_to(W/'outputs/d9-review')):re.findall(r'^FAIL: .+$',p.read_text(),re.M)==ids['guardian_corrected'] for p in oldlogs}
(E/'guardian_comparison.json').write_text(json.dumps(ids,indent=2)+'\n')
# Validate all previously acquired NON OK evidence, including excluded local archive.
old=W/'outputs/d9-review';acquired=S/'studio2/fase03/harness/d9_corrections/non_ok_6a8031b';m=json.loads((old/'MANIFEST.json').read_text())
for i in m['files']:
 p=acquired/i['path'];assert p.stat().st_size==i['bytes'] and sha(p)==i['sha256'],str(p)
for name in ['MANIFEST.json','CONSEGNA.json']:assert (old/name).read_bytes()==(acquired/name).read_bytes()
for pin,archive in [('6a8031b',W/'work/candidate.tar'),('16c98f3',W/'work/corrections-candidate.tar')]:
 p=subprocess.Popen(['git','-C',str(S),'archive',pin],stdout=subprocess.PIPE);h=hashlib.sha256()
 for b in iter(lambda:p.stdout.read(1048576),b''):h.update(b)
 assert p.wait()==0 and h.hexdigest()==sha(archive),pin
with gzip.open(O/'candidate_16c98f3.tar.gz','rb') as f:
 h=hashlib.sha256()
 for b in iter(lambda:f.read(1048576),b''):h.update(b)
assert h.hexdigest()==sha(W/'work/corrections-candidate.tar')
for root,items in before.items():
 if not root.endswith('/d9-review'):
  tracked=set(filter(None,subprocess.check_output(['git','-C',root,'ls-files','-z']).decode().split('\0')));assert tracked==set(items),root
assert subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD']).decode().strip()=='cf763333b7951b4cf711e1286657f6afc6a9df87'
statuses={root:subprocess.check_output(['git','-C',root,'status','--porcelain']).decode() for root in before if not root.endswith('/d9-review')};assert not any(statuses.values()),statuses
(E/'preservation_final.json').write_text(json.dumps({'verified_unchanged_members':verified,'acquired_original_review_members':591,'worktree_status':statuses,'archive_matches_git_technical_and_rejected':True,'candidate_compressed_archive_roundtrip':True},indent=2)+'\n')
(E/'RESULTS_VERIFIED.json').write_text(json.dumps(results,indent=2)+'\n');print('All expected test outcomes, guard IDs, source bytes and original evidence verified.')
