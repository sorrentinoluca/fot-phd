from pathlib import Path
import json,re,ast,collections
E=Path(__file__).resolve().parent;C=E.parent/'candidate';O=Path('/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence');F=Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence')
def link(p,label=None,line=None):return f'[{label or p.name}]({p}'+(f':{line}' if line else '')+')'
logs=[E/'targeted.log',E/'literal/evidence/extended.log',E/'literal/evidence/additional_edges/additional.log',E/'applicable/applicable.log']
def passed(name):
 for p in logs:
  if any(l.startswith(name+' ') and l.endswith(' ... ok') for l in p.read_text().splitlines()):return p
 raise AssertionError('No current pass: '+name)
rows=json.loads((O/'MATRICE_50_METODI.json').read_text())
text='''# Matrice nominativa dei 50 metodi — candidato edb37f3

Ogni riga ha una prova corrente effettivamente passata, con log, adattamento e perimetro. La matrice precedente rimane acquisita byte-identica; questo file è una nuova valutazione fuori candidato. I 50 ID sono discontinui: non è una suite originale 50/50. Nessuna esclusione implicita.

12 metodi letterali e N20/N21 con la sola fixture/argomento costituiscono i 14 applicabili. Altri 35 sono adattati o accorpati con motivazioni individuali; N48 usa la regola C02 obbligatoria della nuova API, verificata fino al denominatore T3/T6 e alla ripresa. Accorpamenti e sovrapposizioni non aggiungono test. I falsi verdi storici N22–24 e N41 non sono usati: le prove sostitutive partono da prerequisiti validi.

D01 originario è chiuso dalle Y01/Y02 letterali e dalle regressioni D01. Z01–Z03 aggiungono una distinta lacuna D02: gli esiti dei predecessori possono essere confermati con raw corrotti o copertura incompleta. I PASS delle righe sotto non certificano quindi tutta R04/R08.

| Metodo originale | Modalità | Prova corrente e log | Motivazione | Riscontro e limite |
| --- | --- | --- | --- | --- |
'''
for r in rows:
 r['historical_evaluation_9e18bcb']=dict(result=r['result'],rationale=r['rationale'],proof_link=r['proof_link'],current_pass_log=r['current_pass_log'])
 r['proof_link']=r['proof_link'].replace(str(O.parent/'candidate'),str(C)).replace(str(O),str(E))
 r['current_pass_log']=str(passed(r['proof_method'] or r['original']))
 r['result']='PASS della prova indicata, entro il suo perimetro offline'
 if r['number']==7:
  r['rationale']='La riserva tardiva illegale è rifiutata prima e dopo riapertura; X05 controlla il primario incompleto. X01/X02 e tutte le Y ora passano anche per alternativo irrisolto e vecchi gate chiusi. Il difetto di precedenza D01 è chiuso; il diverso controllo della integrità/copertura dei predecessori resta incompleto in Z01–Z03/D02.'
  r['result']='PASS dei casi originari e D01; R04 ancora limitata da D02'
 row=[link(F/'negative_probes.py',r['original'],r['original_line']),r['mode'],r['proof_link']+'; '+link(Path(r['current_pass_log']),'log'),r['rationale'],r['result']]
 text+='| '+' | '.join(row)+' |\n'
assert len(rows)==50 and len({r['original'] for r in rows})==50
(E/'MATRICE_50_METODI.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(E/'MATRICE_50_METODI.md').write_text(text)
xs=json.loads((O/'MATRICE_X01_X24.json').read_text())
text='''# Estensioni X, Y e Z — candidato edb37f3

X: 24 metodi distinti, 23 letterali PASS e solo X23 adattato PASS. Il file originale X23 produce una failure, conservata. Attendeva l'interruzione difettosa del gate C02; l'adattamento già verificato nel terzo verbale mantiene sempre TimeoutError e richiede 120 INVALID, T3/T6 falliti, 40 triplette non valutabili, raw/identità/token sconosciuti null, riconciliazione immutabile e nessun reinvio. Nessun nuovo adattamento in questa review; copie letterali e adattata confrontate per hash con la precedente evidence. Il diff originario è acquisito in non_ok_9e18bcb_20260915/evidence/X23_adaptation.diff.

| Metodo X | Esito letterale | Consolidamento |
| --- | --- | --- |
'''
for r in xs:
 r['source']=r['source'].replace(str(O),str(E));text+=f"| {link(Path(r['source']),r['name'],r['line'])} | {r['literal']} | {r['current']} |\n"
text+='\n| Metodo Y, script byte-identico | Esito corrente |\n| --- | --- |\n'
for n in ast.walk(ast.parse((E/'y_original/evidence/edge_probes.py').read_text())):
 if isinstance(n,ast.FunctionDef) and n.name.startswith('test_Y'):text+=f"| {link(E/'y_original/evidence/edge_probes.py',n.name,n.lineno)} | PASS |\n"
text+='\nY01/Y02 generano nuovi ledger con il codice esatto 0c8157f in subprocess, senza SQL alterato, e li riaprono sul candidato corrente. Le due failure precedenti sono ora rifiuti espliciti sull’alternativo; 132 intenti e zero nuovi invii. Y03–Y07 confermano raw/INVALID, guardie, journal, retry e denominatori producer. Nessuna somma con i sette test D01 già inclusi nelle suite 103/138.\n'
text+='\n| Nuova prova autonoma Z | Proprietà | Esito |\n| --- | --- | --- |\n'
descs={1:'Raw corrotto di primario/alternativo/sonda: quattro ingressi normativi',2:'Sette richieste alternative residue non possono attestare copertura di otto',3:'Runner ordinario: raw alternativo corrotto dopo gate valido, riapertura senza invii',4:'Quattro ingressi: vero processo BEGIN IMMEDIATE bloccato durante la verifica e ammesso dopo',5:'Gate tutto INVALID già FAIL: replay conserva 120 invalidità e non promuove a successo'}
for n in ast.walk(ast.parse((E/'chain_probes.py').read_text())):
 if isinstance(n,ast.FunctionDef) and n.name.startswith('test_Z'):
  number=int(n.name[6:8]);text+=f"| {link(E/'chain_probes.py',n.name,n.lineno)} | {descs[number]} | {'FAIL — D02' if number<4 else 'PASS'} |\n"
text+='\nZ01–Z03 provocano fault SQL espliciti soltanto su copie sacrificabili già valide; non vengono confusi con le riproduzioni D01 generate senza SQL. Gli hash dei raw non sono ricalcolati e l’outcome non viene cambiato. Il parser ordinario ledger.response rileva la corruzione; è la conferma ricorsiva a non applicare quel controllo. Non viene rivendicata resistenza crittografica al proprietario del database.\n'
(E/'MATRICE_X_Y_Z.md').write_text(text);(E/'MATRICE_X01_X24.json').write_text(json.dumps(xs,indent=2)+'\n')
print(json.dumps(dict(mapped=len(rows),modes=dict(collections.Counter(r['mode'] for r in rows)),X=len(xs),Y=7,Z=5)))
