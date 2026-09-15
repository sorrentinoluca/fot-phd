from pathlib import Path
import json,hashlib,shutil,subprocess
src=Path('/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/evidence')
root=Path('/Users/luker/fot-tep-harness-0310-c01-c03')
dst=root/'studio2/fase03/harness/non_ok_0c8157f_20260915';dst.mkdir()
rows=[]
for line in (src/'SHA256SUMS').read_text().splitlines()+[hashlib.sha256((src/'SHA256SUMS').read_bytes()).hexdigest()+'  SHA256SUMS']:
 h,n=line.split('  ',1);p=src/n;b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==h
 # Prior 50-method reruns contain repeated source inventories; retain scripts and observations, reference large duplicate trees.
 copied=not (n.startswith(('applicable/','original_all_unadapted/')) and '/fixtures/' in n)
 if copied:
  q=dst/'evidence'/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert q.read_bytes()==b
 rows.append(dict(source=str(p),relative_path=n,sha256=h,bytes=len(b),disposition='copied_byte_identical' if copied else 'external_verified',reason=None if copied else 'Repeated old fixture/source trees; preserved at exact source, already acquired in prior NON OK; not scientific inputs.'))
links=[dict(path=str(p),target=str(p.readlink())) for p in src.rglob('*') if p.is_symlink()]
(dst/'ACQUISITION_INVENTORY.json').write_text(json.dumps(dict(entries=rows,symlinks_external=links),indent=2)+'\n')
repos=['/Users/luker/fot-tep','/Users/luker/fot-tep-harness-0310-correzioni','/Users/luker/fot-tep-harness-0310-offline','/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate','/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate']
states={}
for p in repos:
 if Path(p).is_dir():
  states[p]={k:subprocess.check_output(['git','-C',p,*args],text=True) for k,args in [('head',['rev-parse','HEAD']),('tree',['rev-parse','HEAD^{tree}']),('status',['status','--porcelain=v1']),('branch',['branch','--show-current'])]}
(Path('/Users/luker/fot-tep-harness-0310-c01-c03-checks')/'initial_git_state.json').write_text(json.dumps(states,indent=2)+'\n')
(dst/'INITIAL_GIT_STATE.json').write_text(json.dumps(states,indent=2)+'\n')
counts={k:sum(r['disposition']==k for r in rows) for k in ['copied_byte_identical','external_verified']}
(dst/'PROVENIENZA.md').write_text(f'''# Acquisizione del secondo NON OK — C01–C03

Fonte: `{src}`. Candidato respinto `0c8157f23bee49a3a5a2df648525c34706da29d7`, tree `a1573b49615a875f24ee97f9f1cd4bab399be93d`; successore documentale `6268437b8b64288b50ad5f7c924e1fcab85b27d3` (base del nuovo worktree).

Verificati 3025 membri del manifest più il manifest stesso, prima dell'uso. Verbale SHA-256 `1785fb3cfb832b5a299fe885ac740a4f557ad83431e002451d447afab64f4efc`; manifest SHA-256 `e5cb1589a9f8006303c9ea91a3ea37be742990c2ac6c86fb8ffc7e59fcbf7f80`.

Copie byte-identiche: {counts['copied_byte_identical']}; riferimenti esterni verificati: {counts['external_verified']}. Inventario esplicito con percorsi, impronte, dimensioni e motivi in ACQUISITION_INVENTORY.json. I symlink sono descritti separatamente, non percorsi ricorsivamente. Script, log, matrici, osservazioni e tutte le nuove fixture X01–X24 sono acquisiti. Le fixture replicate dei precedenti 50 metodi restano al percorso esterno indicato; nessuna prova viene ricostruita o normalizzata.

**Fixture false/alterate e stub SOLO OFFLINE**: ogni albero di fixture in questa acquisizione è forense, non fonte scientifica. Non eseguire script in-place: creano/sovrascrivono output. Le intestazioni e i percorsi interni conservano il contesto originale.

Verificati repository, worktree, HEAD e stati iniziali (INITIAL_GIT_STATE.json). Remoto effettivo `https://github.com/sorrentinoluca/fot-phd.git`, main osservato `a00605862f627710347bd63c49f79a6d0a00135f`. Nessuna importazione parallela. Acquisizione separata dalle correzioni; nessun cambio al verdetto indipendente.
''')
shutil.copyfile(__file__,dst/'acquire.py')
print(counts);print('bytes',sum(r['bytes'] for r in rows if r['disposition']=='copied_byte_identical'))
