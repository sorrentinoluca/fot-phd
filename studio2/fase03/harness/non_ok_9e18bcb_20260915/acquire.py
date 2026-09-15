from pathlib import Path
import json,hashlib,shutil,subprocess
root=Path('/Users/luker/fot-tep-harness-0310-d01');src=Path('/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence');dst=root/'studio2/fase03/harness/non_ok_9e18bcb_20260915';dst.mkdir()
for n,sha in [('VERIFICA_C01_C03.md','35e047834ec957a8008db7b82c375d3022cbcfeb7a8d2fb80143f44e9cabfe42'),('SHA256SUMS','29385ea6589286e7a551c13ee61c8588b7b5792dabba7fa5d3ebebcd090a34ea')]:assert hashlib.sha256((src/n).read_bytes()).hexdigest()==sha
rows=[]
for line in (src/'SHA256SUMS').read_text().splitlines()+[hashlib.sha256((src/'SHA256SUMS').read_bytes()).hexdigest()+'  SHA256SUMS']:
 sha,n=line.split('  ',1);p=src/n;b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==sha,n
 # Keep all new Y fixtures; existing X/N fixture replicas remain externally retrievable.
 copied=not any(part in {'fixtures','extended_fixtures'} for part in Path(n).parts)
 if copied:
  q=dst/'evidence'/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert q.read_bytes()==b
 rows.append(dict(source=str(p),relative_path=n,sha256=sha,bytes=len(b),disposition='copied_byte_identical' if copied else 'external_verified',reason=None if copied else 'Repeated old N/X fixtures; preserved and verified at source; no scientific input'))
links=[dict(path=str(p),target=str(p.readlink())) for p in src.rglob('*') if p.is_symlink()]
(dst/'ACQUISITION_INVENTORY.json').write_text(json.dumps(dict(entries=rows,symlinks_external=links),indent=2)+'\n')
repos=['/Users/luker/fot-tep','/Users/luker/fot-tep-harness-0310-c01-c03','/Users/luker/fot-tep-harness-0310-correzioni','/Users/luker/fot-tep-harness-0310-offline','/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/candidate','/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate','/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate']
states={}
for p in repos:
 if Path(p).is_dir():states[p]={k:subprocess.check_output(['git','-C',p,*args],text=True) for k,args in [('head',['rev-parse','HEAD']),('tree',['rev-parse','HEAD^{tree}']),('status',['status','--porcelain=v1']),('branch',['branch','--show-current'])]}
(dst/'INITIAL_GIT_STATE.json').write_text(json.dumps(states,indent=2)+'\n')
counts={k:sum(r['disposition']==k for r in rows) for k in ['copied_byte_identical','external_verified']}
(dst/'PROVENIENZA.md').write_text(f'''# Terzo NON OK — residuo D01 / C01 / R04

Acquisizione da `{src}` dopo verifica byte per byte delle impronte: 1788 membri del manifest più il manifest stesso. Candidato respinto `9e18bcbd06fa2c54202c8eeda079c112dbfcefcd`, tree `5d1fd7924c4e1e46346f367590e6aa1977a6ba75`; base documentale nuova `52e13e1ed540e1ad076474398bf850445c9a4a00`.

Verbale SHA-256 `35e047834ec957a8008db7b82c375d3022cbcfeb7a8d2fb80143f44e9cabfe42`; manifest SHA-256 `29385ea6589286e7a551c13ee61c8588b7b5792dabba7fa5d3ebebcd090a34ea`.

{counts['copied_byte_identical']} file copiati byte-identici; {counts['external_verified']} riferimenti esterni verificati. Inventario esplicito di percorsi, hash, dimensioni e motivi; symlink descritti, non seguiti ricorsivamente. Tutte le nuove fixture Y01–Y07, script, log e osservazioni sono acquisite. Le copie replicate N/X restano nei percorsi esatti indicati, non vengono rigenerate o ripulite.

**Tutte le fixture sono sacrificabili e deliberatamente false/alterate.** Non costituiscono dati scientifici o approvazioni reali. Non eseguire script in-place: utilizzare un nuovo contenitore e il candidato esatto. C02/C03 risultano chiusi nella review acquisita; questo delta è limitato al residuo di riconferma storica C01/R04.

Prima di scrivere controllati HEAD, tree, branch, stato e worktree; fonti preservate in INITIAL_GIT_STATE.json. Remoto effettivo `https://github.com/sorrentinoluca/fot-phd.git`, main osservato `a00605862f627710347bd63c49f79a6d0a00135f`. Acquisizione separata dalle correzioni; nessun push, merge, tag o nuovo verdetto indipendente.
''')
shutil.copyfile(__file__,dst/'acquire.py');print(counts)
check=Path('/Users/luker/fot-tep-harness-0310-d01-checks');p=check/'before';(p/'evidence').mkdir(parents=True)
(p/'candidate').symlink_to('/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/candidate',target_is_directory=True)
shutil.copyfile(src/'edge_probes.py',p/'evidence/edge_probes.py')
(check/'worktrees_before.txt').write_text(subprocess.check_output(['git','-C',str(root),'worktree','list','--porcelain'],text=True))
