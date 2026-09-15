from pathlib import Path
import json,re,ast,collections
E=Path(__file__).resolve().parent;C=E.parent/'candidate';O=Path('/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence');F=Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence')
def link(p,label=None,line=None):return f'[{label or p.name}]({p}'+(f':{line}' if line else '')+')'
logs=[E/'targeted.log',E/'literal/evidence/extended.log',E/'literal/evidence/additional_edges/additional.log',E/'applicable/applicable.log']
def passed(name):
 for p in logs:
  if any(l.startswith(name+' ') and l.endswith(' ... ok') for l in p.read_text().splitlines()):return p
 raise AssertionError('No current pass: '+name)
rows=json.loads((O/'MATRICE_50_METODI.json').read_text())
text='''# Matrice nominativa dei 50 metodi — candidato a219bd4

Ogni riga conserva una corrispondenza nominativa, motivo dell'adattamento/accorpamento e log di una prova corrente effettivamente passata. La matrice acquisita rimane intatta; questa è una nuova valutazione fuori candidato. Gli ID sono discontinui: 50 metodi distinti, senza una pretesa 50/50 letterali e senza esclusioni implicite.

12 metodi letterali e N20/N21 con sola fixture/argomento formano i 14 applicabili. Altri 35 sono adattati/accorpati esplicitamente; N48 usa la regola C02 obbligatoria della nuova API, verificata fino a T3/T6 e ripresa. I falsi verdi storici N22–24/N41 non sono usati: le prove correnti partono da prerequisiti validi. Suite e sottocasi non si sommano.

D01 e le manifestazioni D02 delle Y/Z passano ora tutte. W01/W02 identificano il distinto D03: la prova zero-token persistita viene ricontrollata solo parzialmente. Questo limita la chiusura globale della verifica dei retry, senza negare il PASS dei casi nominali originari.

| Metodo originale | Modalità | Prova corrente e log | Motivazione | Riscontro e limite |
| --- | --- | --- | --- | --- |
'''
for r in rows:
 r['historical_evaluation_edb37f3']=dict(result=r['result'],rationale=r['rationale'],proof_link=r['proof_link'],current_pass_log=r['current_pass_log'])
 r['proof_link']=r['proof_link'].replace(str(O.parent/'candidate'),str(C)).replace(str(O),str(E))
 r['current_pass_log']=str(passed(r['proof_method'] or r['original']));r['result']='PASS della prova indicata, nel suo perimetro offline'
 if r['number']==7:r['rationale']='La riserva tardiva è rifiutata prima/dopo restart; X05 verifica il primario incompleto. X01/X02 e Y01/Y02 verificano gli stati alternativi irrisolti, anche nei vecchi gate. Z01–Z03 ora passano per integrità/copertura dei predecessori. D03 è un diverso limite della prova zero-token persistita.'
 if r['number'] in (1,11,43,44):r['result']='PASS del caso originario; validazione complessiva della prova di retry limitata da D03/W01/W02'
 text+='| '+' | '.join([link(F/'negative_probes.py',r['original'],r['original_line']),r['mode'],r['proof_link']+'; '+link(Path(r['current_pass_log']),'log'),r['rationale'],r['result']])+' |\n'
assert len(rows)==50 and len({r['original'] for r in rows})==50
(E/'MATRICE_50_METODI.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(E/'MATRICE_50_METODI.md').write_text(text)
text='''# Estensioni X, Y, Z e W — candidato a219bd4

Le copie X/Y/Z sono byte-identiche alle prove indipendenti precedenti. X mantiene 23 letterali PASS più un X23 adattato PASS: il solo X23 letterale conserva una failure perché attendeva l'interruzione difettosa C02. L'adattamento già verificato conserva lo stub sempre TimeoutError e pretende 120 INVALID, T3/T6 falliti, 40 triplette non valutabili, dati non osservati null, riconciliazione immutabile e nessun reinvio. Nessun nuovo adattamento di assertion in questa review; per l'esecuzione X23 è copiato anche il suo modulo sibling extended_probes.py.

Y01/Y02 generano i ledger legacy col codice esatto 0c8157f in subprocess senza SQL alterato. Z01–Z03 introducono invece fault SQL espliciti dopo un positivo, soltanto su copie sacrificabili. Tutte le Y e Z ora passano; le modifiche D01/D02 sono verificate nelle manifestazioni originarie. W è una nuova suite autonoma della prova di riconciliazione e dell'assenza di cache persistenti.

| Metodo e sorgente | Esito corrente | Provenienza/limite |
| --- | --- | --- |
'''
sources=[('X',E/'literal/evidence/extended_probes.py'),('X',E/'literal/evidence/additional_edges.py'),('Y',E/'y_original/evidence/edge_probes.py'),('Z',E/'z_original/evidence/chain_probes.py'),('W',E/'retry_proof_probes.py')]
entries=[]
for group,p in sources:
 for n in ast.walk(ast.parse(p.read_text())):
  if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'+group):
   number=int(n.name[6:8]);result='FAIL letterale, PASS adattato' if group=='X' and number==23 else 'FAIL — D03' if group=='W' and number<3 else 'PASS'
   note='23 letterali + solo X23 già adattato' if group=='X' else 'script letterale, nessuna modifica' if group in ('Y','Z') else 'nuova prova indipendente'
   entries.append(dict(group=group,number=number,name=n.name,path=str(p),line=n.lineno,result=result))
   text+=f'| {link(p,n.name,n.lineno)} | {result} | {note} |\n'
text+='''
W01: sette alterazioni indipendenti della sola prova persistita (token positivi, token assenti o booleani, ricevuta/evidenza provider assente, autore approvazione assente), cinque ingressi normativi dopo un positivo. W02: timeout e retry producer, chiusura lecita, poi token positivi nel solo evento di riconciliazione; runner gate --resume. Non si modifica alcun hash o outcome per rendere il guasto coerente con l'intero database.

W03: retry a due passaggi valido, dieci intenti/otto coppie; perdita successiva della prova intermedia respinta nella stessa istanza. W04: positivo seguito da raw corrotto nella stessa istanza, nessuna cache riusata. Questi due positivi passano. I sottocasi W01 non sono metodi aggiuntivi; due failure W sono un solo difetto D03. Nessuna perdita spontanea, nuova chiamata o GO inferita dai fault.
'''
(E/'MATRICE_ESTENSIONI.md').write_text(text);(E/'MATRICE_ESTENSIONI.json').write_text(json.dumps(entries,indent=2)+'\n')
print(json.dumps(dict(originals=len(rows),modes=dict(collections.Counter(r['mode'] for r in rows)),extensions=dict(collections.Counter(r['group'] for r in entries)))))
