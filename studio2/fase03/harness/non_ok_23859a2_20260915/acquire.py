from pathlib import Path
import json,hashlib,subprocess,shutil
W=Path('/Users/luker/fot-tep-harness-0310-d04');S=Path('/Users/luker/fot-tep-harness-0310-d03');E=Path('/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/evidence');K=Path('/Users/luker/fot-tep-harness-0310-d04-checks')
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base='97868f9d6ef281c2dd4ab1c6ffb67e2477ee5715';rejected='23859a29225ccd9cd6f47e4a0b6e36258831dbab';tree='fe66025f4925e27676b0be16428475e3fcaee060'
previous=json.loads((S/'studio2/fase03/harness/non_ok_a219bd4_20260915/INITIAL_GIT_STATE.json').read_text())['repositories']
repos=[Path(x) for x in previous]+[S,E.parent/'candidate']
state={str(p):{k:git(p,*a) for k,a in dict(head=['rev-parse','HEAD'],tree=['rev-parse','HEAD^{tree}'],branch=['branch','--show-current'],status=['status','--porcelain=v1']).items()} for p in repos}
assert state[str(S)]['head']==base and state[str(S)]['status']=='?? VERIFICA_D03.md'
assert git(S,'rev-parse','HEAD^')==rejected
assert state[str(E.parent/'candidate')]['head']==rejected and state[str(E.parent/'candidate')]['tree']==tree and not state[str(E.parent/'candidate')]['status']
assert set(git(S,'diff','--name-only',rejected,base).splitlines())=={'studio2/fase03/harness/'+f for f in ['REPORT_CORREZIONE_D03.md','PROMPT_VERIFICA_D03.md','CONSEGNA_D03.json','DELIVERY_AUDIT_D03.json']}
for i in json.loads((S/'studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json').read_text())['files']:
 p=S/i['path'];assert sha(p)==i['sha256'] and p.stat().st_size==i['bytes']
assert sha(E/'VERIFICA_D03.md')=='21e457af023a9a8fae3560f663784c55788408942f8c9e902b3d468764aceef9'
assert sha(E/'SHA256SUMS')=='9334c9c57b159cf14f047d28646544615c99aaf751298753e573f893dbbb86a1'
manifest=[]
for line in (E/'SHA256SUMS').read_text().splitlines()+[sha(E/'SHA256SUMS')+'  SHA256SUMS']:
 h,name=line.split(maxsplit=1);name=name.lstrip('*');assert sha(E/name)==h;manifest.append((h,name))
remote=git(S,'ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/heads/main')
worktrees=git(S,'worktree','list','--porcelain')
subprocess.run(['git','-C',str(S),'worktree','add','-b','codex/studio2-harness-0310-d04',str(W),base],check=True,stdout=subprocess.DEVNULL)
A=W/'studio2/fase03/harness/non_ok_23859a2_20260915';A.mkdir()
items=[]
for h,name in manifest:
 p=E/name;copy=len(Path(name).parts)==1 or name.startswith('independent_fixtures/') or p.suffix=='.py' or p.name.endswith(('.log','.md')) or p.name in ('edge_probes.json','chain_probes.json')
 dst=A/'files'/name
 if copy:dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst);assert sha(dst)==h
 items.append(dict(source=str(p),path=name,sha256=h,bytes=p.stat().st_size,storage='copy' if copy else 'external',copy=str(dst.relative_to(W)) if copy else None,reason='D04 V fixtures, report, script or log' if copy else 'Repeated sacrificial N/X/Y/Z fixtures preserved in immutable review'))
(A/'ACQUISITION_INVENTORY.json').write_text(json.dumps(dict(source=str(E),files=items,symlinks=[dict(path=str(p),target=str(p.readlink())) for p in E.rglob('*') if p.is_symlink()]),indent=2)+'\n')
(A/'INITIAL_GIT_STATE.json').write_text(json.dumps(dict(repositories=state,remote_main=remote,worktrees=worktrees),indent=2)+'\n')
(A/'PROVENIENZA.md').write_text(f"""# Acquisizione delle due review 23859a2 — D04

Base documentale {base}; tecnico respinto {rejected}; tree {tree}.
Tutti i membri del manifest Codex sono verificati prima dell’uso; copie byte-identiche,
esterni con collocazione, hash, dimensione e motivo. Fixture V con guasti SQL deliberati:
soltanto prove offline sacrificabili, mai input scientifici. Symlink non seguiti.

Claude: OK limitato al nucleo D03; suite non raggiungibili nella VM dichiarate. Verbale
fornito dall’autore e preservato come untracked nel source, senza incorporarlo nel source.
Nessuna verifica autonoma dei log scratch Claude, non disponibili qui.
Codex: D03 chiuso nelle prove; NON OK per D04 P2 su quota_kind nello stadio aperto.
Le due review non si annullano: perimetro e prove effettivamente eseguite restano distinti.

Mandato R05/R07 già autorizzato: consolidare la validazione prima delle nuove riserve/riprese;
nessun cambiamento quote, rinunce, no-backfill o contenuti D03. Prima test rossi e contratto,
poi runtime. Nessun freeze/GO; D9 eseguibile, label, qualificazioni, T5/pilot separati.
""")
shutil.copyfile(__file__,A/'acquire.py')
f=S/'VERIFICA_D03.md'
assert sha(f)=='bc3ee96afb2bd890d0b326ca4965d03c46d241f288a30c5ee1455a0c8ec9a47f' and f.stat().st_size==13529
shutil.copyfile(f,A/'VERIFICA_D03_CLAUDE.md')
(A/'CLAUDE_PROVENIENZA.json').write_text(json.dumps(dict(source=str(f),sha256=sha(f),bytes=f.stat().st_size,role='independent review supplied by user, OK limited to D03; external runtime suites not reproduced by Claude; original left untracked and untouched'),indent=2)+'\n')
K.mkdir()
for label,target in [('before',E.parent/'candidate'),('after',W)]:
 q=K/label;(q/'evidence').mkdir(parents=True);(q/'candidate').symlink_to(target,target_is_directory=True);shutil.copyfile(E/'independent_d03_probes.py',q/'evidence/independent_d03_probes.py')
print('Verified/acquired',len(items),'members;',sum(i['storage']=='copy' for i in items),'copies;',len(state),'repos preserved')
