from pathlib import Path
import json,hashlib,subprocess,shutil
W=Path('/Users/luker/fot-tep-harness-0310-d03');S=Path('/Users/luker/fot-tep-harness-0310-d02');E=Path('/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence');K=Path('/Users/luker/fot-tep-harness-0310-d03-checks')
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base='e9b60c5db77edfd3c06a29857e6ba5f61ebe139a';rejected='a219bd469bbd280f56b7fa9cb56cda115b0975ed';tree='3fb8e50c189b85b447503b8a1ac99c1741904a5b'
previous=json.loads((S/'studio2/fase03/harness/non_ok_edb37f3_20260915/INITIAL_GIT_STATE.json').read_text())['repositories']
repos=[Path(x) for x in previous]+[S,E.parent/'candidate']
state={str(p):{k:git(p,*a) for k,a in dict(head=['rev-parse','HEAD'],tree=['rev-parse','HEAD^{tree}'],branch=['branch','--show-current'],status=['status','--porcelain=v1']).items()} for p in repos}
assert state[str(S)]['head']==base and not state[str(S)]['status']
assert git(S,'rev-parse','HEAD^')==rejected
assert state[str(E.parent/'candidate')]['head']==rejected and state[str(E.parent/'candidate')]['tree']==tree and not state[str(E.parent/'candidate')]['status']
assert set(git(S,'diff','--name-only',rejected,base).splitlines())=={'studio2/fase03/harness/'+f for f in ['REPORT_CORREZIONE_D02.md','PROMPT_VERIFICA_D02.md','CONSEGNA_D02.json','DELIVERY_AUDIT_D02.json']}
for i in json.loads((S/'studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json').read_text())['files']:
 p=S/i['path'];assert sha(p)==i['sha256'] and p.stat().st_size==i['bytes']
assert sha(E/'VERIFICA_D02.md')=='b88f046592ac9d1b0f784c1d127f83ea3cc609c93bd547bbc91c7541cfd0223f'
assert sha(E/'SHA256SUMS')=='4ed360ee40d521e989e38fa2a2a68d5a5c461a5a6397c94dd34a598300141776'
manifest=[]
for line in (E/'SHA256SUMS').read_text().splitlines()+[sha(E/'SHA256SUMS')+'  SHA256SUMS']:
 h,name=line.split(maxsplit=1);name=name.lstrip('*');assert sha(E/name)==h;manifest.append((h,name))
remote=git(S,'ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/heads/main')
worktrees=git(S,'worktree','list','--porcelain')
subprocess.run(['git','-C',str(S),'worktree','add','-b','codex/studio2-harness-0310-d03',str(W),base],check=True,stdout=subprocess.DEVNULL)
A=W/'studio2/fase03/harness/non_ok_a219bd4_20260915';A.mkdir()
items=[]
for h,name in manifest:
 p=E/name;copy=len(Path(name).parts)==1 or name.startswith('retry_proof_fixtures/') or p.suffix=='.py' or p.name.endswith(('.log','.md')) or p.name in ('edge_probes.json','chain_probes.json')
 dst=A/'files'/name
 if copy:dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst);assert sha(dst)==h
 items.append(dict(source=str(p),path=name,sha256=h,bytes=p.stat().st_size,storage='copy' if copy else 'external',copy=str(dst.relative_to(W)) if copy else None,reason='D03 W fixtures, report, script or log' if copy else 'Repeated sacrificial N/X/Y/Z fixtures preserved in immutable review'))
(A/'ACQUISITION_INVENTORY.json').write_text(json.dumps(dict(source=str(E),files=items,symlinks=[dict(path=str(p),target=str(p.readlink())) for p in E.rglob('*') if p.is_symlink()]),indent=2)+'\n')
(A/'INITIAL_GIT_STATE.json').write_text(json.dumps(dict(repositories=state,remote_main=remote,worktrees=worktrees),indent=2)+'\n')
(A/'PROVENIENZA.md').write_text(f'''# Acquisizione NON OK a219bd4 — D03\n\nBase documentale {base}; tecnico respinto {rejected}; tree {tree}. Verbale e manifest verificati con le impronte dell’autore prima dell’esecuzione; tutti i membri riletti. Copie byte-identiche, esterni recuperabili con coordinate/hash/dimensioni/motivazione nell’inventario. Symlink inventariati separatamente.\n\nLe fixture W contengono **guasti SQL deliberati, soltanto prove sacrificabili**, mai input scientifici. X/Y/Z/N restano alla loro posizione originaria. Tutte le nuove esecuzioni in directory esterne distinte, senza sovrascrivere le review.\n\nMandato aggiornato: correzione D03, validatore comune nei tre percorsi, inventario prima del runtime, prove rosse sul respinto, fail-closed delle prove storiche senza digest e nessun backfill. Il nuovo requisito non equivale a una migrazione approvata. Nessun freeze o GO.\n''')
shutil.copyfile(__file__,A/'acquire.py')
# Fable analysis, as supplied by the author, is context; not an independent code verdict.
f=Path('/Users/luker/.codex/attachments/eec4e006-778d-4504-9eab-2bbd75a8be8f/pasted-text.txt');shutil.copyfile(f,A/'FABLE_ANALISI_FORNITA.txt')
(A/'FABLE_PROVENIENZA.json').write_text(json.dumps(dict(source=str(f),sha256=sha(f),bytes=f.stat().st_size,role='process analysis supplied by user; amended limits/severity in subsequent user messages; not new technical approval'),indent=2)+'\n')
K.mkdir()
for label,target in [('before',E.parent/'candidate'),('after',W)]:
 q=K/label;(q/'evidence').mkdir(parents=True);(q/'candidate').symlink_to(target,target_is_directory=True);shutil.copyfile(E/'retry_proof_probes.py',q/'evidence/retry_proof_probes.py')
print('Verified/acquired',len(items),'members;',sum(i['storage']=='copy' for i in items),'copies;',len(state),'repos preserved')
