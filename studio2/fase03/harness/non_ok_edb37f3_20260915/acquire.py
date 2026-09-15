from pathlib import Path
import json,subprocess,hashlib,shutil
W=Path('/Users/luker/fot-tep-harness-0310-d02'); S=Path('/Users/luker/fot-tep-harness-0310-d01'); E=Path('/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence')
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],text=True).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
repos=[Path('/Users/luker/fot-tep'),S,Path('/Users/luker/fot-tep-harness-0310-c01-c03'),Path('/Users/luker/fot-tep-harness-0310-correzioni'),Path('/Users/luker/fot-tep-harness-0310-offline'),E.parent/'candidate',Path('/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/candidate'),Path('/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate'),Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/candidate')]
state={str(p):{k:git(p,*a) for k,a in dict(head=['rev-parse','HEAD'],tree=['rev-parse','HEAD^{tree}'],branch=['branch','--show-current'],status=['status','--porcelain=v1']).items()} for p in repos}
assert state[str(S)]['head']=='7afbf41632aa8117c85274b5f471abca0a655462' and not state[str(S)]['status']
assert git(S,'rev-parse','HEAD^')=='edb37f359f29c461c5a507c1027c4bf411654130'
assert git(S,'rev-parse','HEAD^^')=='89b016a728bdbf5d2d8b438416e6133b050683da'
assert git(E.parent/'candidate','rev-parse','HEAD^{tree}')=='56d98666e1d18c7958ac8d3631ae6d5b8ec04bf9'
assert state[str(E.parent/'candidate')]['head']=='edb37f359f29c461c5a507c1027c4bf411654130' and not state[str(E.parent/'candidate')]['status']
manifest=json.loads((S/'studio2/fase03/harness/HARNESS_OFFLINE_CANDIDATE.json').read_text())
print('Manifest schema',list(manifest)); print('Member sample',manifest['files'][0])
for item in manifest['files']:
 p=S/item['path']; assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes']
assert set(git(S,'diff','--name-only','HEAD^','HEAD').splitlines())=={'studio2/fase03/harness/'+f for f in ['REPORT_CORREZIONE_D01.md','PROMPT_VERIFICA_D01.md','CONSEGNA_D01.json','DELIVERY_AUDIT_D01.json']}
subprocess.run(['git','-C',str(S),'worktree','add','-b','codex/studio2-harness-0310-d02',str(W),'7afbf41632aa8117c85274b5f471abca0a655462'],check=True)
A=W/'studio2/fase03/harness/non_ok_edb37f3_20260915';A.mkdir()
items=[]
for line in (E/'SHA256SUMS').read_text().splitlines()+[sha(E/'SHA256SUMS')+'  SHA256SUMS']:
 h,name=line.split(maxsplit=1); name=name.lstrip('*'); p=E/name; assert sha(p)==h
 # New Z fixtures copied; repeated X/Y/N fixtures retained at immutable review paths.
 copy=len(Path(name).parts)==1 or name.startswith('chain_fixtures/') or p.suffix=='.py' or p.name.endswith(('.log','.md')) or p.name in ('edge_probes.json','extended_probes.json','additional_edges.json')
 dest=A/'files'/name
 if copy:dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);assert sha(dest)==h
 items.append(dict(source=str(p),path=name,sha256=h,size_bytes=p.stat().st_size,storage='byte-identical-copy' if copy else 'external',copy=str(dest.relative_to(W)) if copy else None,reason='D02 evidence or script/log/report' if copy else 'Repeated sacrificial N/X/Y fixture; retained in prior independent review'))
links=[dict(path=str(p),target=str(p.readlink())) for p in E.rglob('*') if p.is_symlink()]
(A/'ACQUISITION_INVENTORY.json').write_text(json.dumps(dict(source=str(E),files=items,symlinks=links),indent=2)+'\n')
(A/'INITIAL_GIT_STATE.json').write_text(json.dumps(dict(repositories=state,remote_main=git(S,'ls-remote','https://github.com/sorrentinoluca/fot-phd.git','refs/heads/main')),indent=2)+'\n')
(A/'PROVENIENZA.md').write_text('''# Acquisizione NON OK edb37f3 — D02\n\nVerbale e manifest verificati prima dell’uso, con le impronte comunicate dall’autore. Tutti i membri sono stati riletti. Le copie sono byte-identiche; l’inventario registra collocazione, dimensioni, hash e motivazione degli esterni recuperabili. Symlink elencati separatamente.\n\nLe fixture Z contengono guasti SQL deliberati, dopo una chiusura valida: **prove sacrificabili, non input o risultati scientifici**. Le fixture X/Y/N ripetute restano nella review originaria; nessuna viene promossa a fonte canonica. Riproduzioni successive in nuove directory esterne. Nessuna modifica alle review o ai candidati precedenti.\n\nBase documentale 7afbf41632aa8117c85274b5f471abca0a655462; candidato respinto edb37f359f29c461c5a507c1027c4bf411654130, tree 56d98666e1d18c7958ac8d3631ae6d5b8ec04bf9. Nuovo branch codex/studio2-harness-0310-d02. Commit di acquisizione separato dalle correzioni.\n''')
shutil.copyfile(__file__,A/'acquire.py')
print('Acquired',len(items),'files;',sum(i['storage']=='byte-identical-copy' for i in items),'copies;',len(links),'symlinks')
K=Path('/Users/luker/fot-tep-harness-0310-d02-checks'); K.mkdir()
for label,candidate in [('before',S),('after',W)]:
 q=K/label; (q/'evidence').mkdir(parents=True);(q/'candidate').symlink_to(candidate,target_is_directory=True);shutil.copyfile(E/'chain_probes.py',q/'evidence/chain_probes.py')
