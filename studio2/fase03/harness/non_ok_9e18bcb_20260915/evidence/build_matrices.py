from pathlib import Path
import json,re,ast,hashlib,collections
E=Path(__file__).resolve().parent;C=E.parent/'candidate';O=Path('/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/evidence');F=Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence')
def link(p,label=None,line=None):return f'[{label or p.name}]({p}'+(f':{line}' if line else '')+')'
logs=[E/'targeted.log',E/'literal/evidence/extended.log',E/'literal/evidence/additional_edges/additional.log',E/'applicable/applicable.log']
def passed(name):
 for p in logs:
  if any(l.startswith(name+' ') and l.endswith(' ... ok') for l in p.read_text().splitlines()):return p
 raise AssertionError('No passing current test: '+name)
def method_link(p,name):
 nodes=[n for n in ast.walk(ast.parse(p.read_text())) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name];assert len(nodes)==1,(p,name)
 return link(p,name,nodes[0].lineno)
rows=json.loads((O/'MATRICE_50_METODI.json').read_text());out=[]
for old in rows:
 r=dict(old);n=r['number'];r['historical_evaluation_0c8157f']=dict(result=r.pop('result'),rationale=r['rationale'],proof_link=r.get('proof_link'));name=r['proof_method'] or r['original'];r['current_pass_log']=str(passed(name))
 r['proof_link']=r.get('proof_link','') or method_link(F/'negative_probes.py',r['original'])
 r['proof_link']=r['proof_link'].replace(str(O.parent/'candidate'),str(C)).replace(str(O/'extended_probes.py'),str(E/'literal/evidence/extended_probes.py')).replace(str(O/'additional_edges.py'),str(E/'literal/evidence/additional_edges.py'))
 r['result']='PASS della prova indicata sul candidato 9e18bcb; perimetro offline'
 if n==2:r['rationale']=r['rationale'].replace('X06 valido nel rerun con cwd corretto.','X06 letterale corrente usa già il cwd corretto, 12 processi reali.')
 if n==7:
  r['rationale']=r['rationale'].replace('X01/X02 scoprono il residuo alternativo C01.','X01/X02 ora bloccano i nuovi stati alternativi. Y01/Y02 mostrano il residuo C01 nei gate v2 storici già chiusi.')
  r['result']='PASS del caso primario e dei nuovi stati; R04 ancora PARZIALE: D01/Y01/Y02'
 if n==44:r['rationale']=r['rationale'].replace('X15 rileva separatamente il riepilogo errato C03.','X15 ora verifica anche summary=9; Y07 conferma 9 nello stadio alternativo contro 17 cumulativi pilot.')
 if n==48:
  r['mode']='sostituzione API/fixture equivalente al requisito, verificata end-to-end'
  r['rationale']='La firma privata return_error_record è rimossa: la regola è obbligatoria nel gate. X03 passa con 120 primi tentativi, 119 validi, INVALID senza raw, tripletta divergente e R3. test_C02_N48_single_timeout_is_119_of_120_and_replays_without_sends verifica replay/prova successiva; Y04 copre errore journal, X23 adattato 120 invalidi. La precedente sostituzione NON equivalente è superata da queste prove, non cancellata dalla storia.'
 if n==51:r['rationale']+=' C02 aggiunge INVALID durevoli e arresto reale dopo commit, ripresa in nuovo processo con 118 invii; Y04 controlla errore I/O journal.'
 out.append(r)
assert len(out)==50 and len({r['original'] for r in out})==50
(E/'MATRICE_50_METODI.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
head='''# Corrispondenza esplicita dei 50 metodi — candidato 9e18bcb

Questa matrice aggiorna quella indipendente acquisita, preservata byte per byte. Ogni riga ha una prova rieseguita e passata in questa finestra: non è una dichiarazione 50/50 dello script storico. Le 14 riproduzioni applicabili coprono 12 metodi letterali e N20/N21 con soli adattamenti di fixture/expected_prompts; gli altri 36 hanno sostituzioni o accorpamenti dichiarati. Nessun requisito è escluso implicitamente. Gli ID originali sono discontinui e identificano comunque 50 metodi distinti.

Il file storico completo non viene rieseguito in-place: le sue incompatibilità API/fixture erano state misurate nel secondo verbale (50 eseguiti, 2 failure, 32 errori, 16 verdi). Qui si rieseguono le prove corrispondenti con prerequisiti validi. I vecchi verdi N22/N23/N24/N41 ottenibili per prerequisito mancante non sono accettati come prova pertinente.

N48 è ora esercitato fino a T3/T6 e al replay, ripristinando il requisito normativo. Il caso aggiuntivo D01 non è nascosto dai PASS: la chiusura globale R04/C01 resta parziale per il gate storico irregolare. Il JSON conserva separatamente anche valutazione e motivazione della precedente review.

| Metodo originale | Modalità | Prova corrente e log | Adattamento/accorpamento motivato | Esito e limite |
| --- | --- | --- | --- | --- |
'''
for r in out:head+=f"| {method_link(F/'negative_probes.py',r['original'])} | {r['mode']} | {r['proof_link']}; {link(Path(r['current_pass_log']),'log')} | {r['rationale']} | {r['result']} |\n"
(E/'MATRICE_50_METODI.md').write_text(head)
x=[]
for p in [E/'literal/evidence/extended_probes.py',E/'literal/evidence/additional_edges.py']:
 for n in ast.walk(ast.parse(p.read_text())):
  if isinstance(n,ast.FunctionDef) and n.name.startswith('test_X'):
   num=int(n.name[6:8]);x.append(dict(number=num,name=n.name,source=str(p),line=n.lineno,literal='FAIL: vecchia attesa di interruzione' if num==23 else 'PASS',current='PASS adattato' if num==23 else 'PASS letterale'))
x.sort(key=lambda r:r['number']);assert len(x)==24
(E/'MATRICE_X01_X24.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
text='''# Estensioni X01–X24 e sette nuove prove Y

24 metodi distinti: 23 letterali conformi; X23 letterale fallisce e il suo adattamento esplicito passa. Nessuna somma con le suite 96/131 o i 50 metodi mappati. Le copie letterali hanno gli hash dei due script indipendenti originali. L'adattamento è della preparatrice ed è stato letto, confrontato e rieseguito dal revisore.

X23 originario attestava il difetto C02 aspettando interruzione definitiva dopo un timeout. Questa attesa contrasta con il piano rev.10, righe 831/871–875. Il nuovo X23 mantiene lo stub che fallisce ogni invio, ma richiede 120 INVALID e 40 triplette non valutabili, NO_GO tecnico, raw/identità/token assenti, prova successiva immutabile e nessun reinvio. Diff in `X23_adaptation.diff`. Le sole modifiche sono il corpo X23 e la selezione per eseguire soltanto X23: nessun altro metodo è riscritto. L'adattamento è giustificato dal requisito; non certifica un comportamento reale del servizio.

| ID e codice | Run letterale | Consolidamento motivato |
| --- | --- | --- |
'''
for r in x:text+=f"| {link(Path(r['source']),r['name'],r['line'])} | {r['literal']} | {r['current']} |\n"
text+='\nProve nuove autonome (script `edge_probes.py`, JSON/log omonimi):\n\n| ID | Requisito | Risultato |\n| --- | --- | --- |\n'
desc={1:'Ripresa runner del gate v2 chiuso con alternativo FAILED',2:'Verifica successo e replay outcome con alternativo INTENT',3:'Raw con modello errato non convertibile in assenza risposta',4:'Errore journal dopo commit INVALID: ripresa, 119/120 e R3 senza reinvio',5:'HarnessError preventiva resta INTENT bloccante, senza INVALID fittizio',6:'INVALID riconciliato resta immutabile e non abilita retry gate',7:'Alternativo: summary/outcome 9 richieste e 8 coppie, pilot 17; replay senza summary file'}
for i in range(1,8):text+=f"| Y{i:02} | {desc[i]} | {'FAIL — D01 residuo C01' if i<3 else 'PASS'} |\n"
text+='\nY01/Y02 costruiscono i vecchi ledger eseguendo soltanto codice 0c8157f in copie sacrificabili, poi li aprono con 9e18bcb. Nessuna manomissione SQL, nessuna modifica al vecchio candidato o alla vecchia review. I percorsi temporanei contenuti negli artefatti rimangono forensi; per riprodurre, creare nuove fixture dallo script.\n'
(E/'MATRICE_X01_X24.md').write_text(text)
print(json.dumps(dict(originals=len(out),modes=dict(collections.Counter(r['mode'] for r in out)),extensions=len(x))))
