from pathlib import Path
import json,re,ast,collections
E=Path(__file__).resolve().parent;C=E.parent/'candidate';O=Path('/Users/luker/fot-tep-riverifica-harness-a219bd4-01a0a1ec/evidence');F=Path('/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence')
def link(p,label=None,line=None):return f'[{label or p.name}]({p}'+(f':{line}' if line else '')+')'
logs=[E/'targeted.log',E/'literal/evidence/extended.log',E/'literal/evidence/additional_edges/additional.log',E/'applicable/applicable.log']
def passed(name):
 for p in logs:
  if any(l.startswith(name+' ') and l.endswith(' ... ok') for l in p.read_text().splitlines()):return p
 raise AssertionError('No current pass: '+name)
rows=json.loads((O/'MATRICE_50_METODI.json').read_text())
text='''# Matrice nominativa dei 50 metodi — candidato 23859a2

Ogni metodo conserva fonte, corrispondenza, motivo dell'adattamento/accorpamento e log corrente. Gli ID sono discontinui: 50 metodi distinti, non 50/50 letterali. Le matrici precedenti rimangono intatte. Dodici letterali più N20/N21 con sola fixture/argomento formano i 14 applicabili; altri 35 sono adattati/accorpati; N48 è equivalente al requisito C02 nella nuova API. Nessuna esclusione implicita.

N48 conserva il trasporto fallito e verifica 120 INVALID, T3/T6 e ripresa; non si eredita la vecchia aspettativa errata. I falsi verdi storici N22–24/N41 non sono prove: le fixture correnti soddisfano i prerequisiti prima del fault. Suite e sottocasi non si sommano.

D01/D02/D03 originari passano nelle riproduzioni Y/Z/W e nei test correnti. Il distinto D04/V05/V06 limita R05: un campo quota alterato nello stadio ancora aperto permette un ottavo retry senza waiver, anche nel runner. La matrice storica copre casi finiti; non dimostra ogni combinazione di stadio, ruolo e valore del campo.

| Metodo originale | Modalità | Prova corrente e log | Motivazione | Riscontro e limite |
| --- | --- | --- | --- | --- |
'''
for r in rows:
 r['historical_evaluation_a219bd4']=dict(result=r['result'],rationale=r['rationale'],proof_link=r['proof_link'],current_pass_log=r['current_pass_log'])
 r['proof_link']=r['proof_link'].replace(str(O.parent/'candidate'),str(C)).replace(str(O),str(E))
 r['current_pass_log']=str(passed(r['proof_method'] or r['original']));r['result']='PASS della prova nominata, nel suo perimetro offline'
 if r['number']==7:r['rationale']='Nuovo piano immutabile e prerequisiti completi; riserva tardiva rifiutata, primario/alternativo incompleto rifiutati anche nelle catene legacy. Y/Z/W passano; nuovo requisito storico D03 blocca soltanto prove prive di digest/legame, senza backfill.'
 if r['number'] in (11,12,13,14,15,16,17):r['result']='PASS del caso storico; copertura delle quote negli stadi aperti limitata da D04/V05/V06'
 text+='| '+' | '.join([link(F/'negative_probes.py',r['original'],r['original_line']),r['mode'],r['proof_link']+'; '+link(Path(r['current_pass_log']),'log'),r['rationale'],r['result']])+' |\n'
assert len(rows)==50 and len({r['original'] for r in rows})==50
(E/'MATRICE_50_METODI.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');(E/'MATRICE_50_METODI.md').write_text(text)
text='''# Estensioni X, Y, Z, W e V — candidato 23859a2

X/Y/Z/W sono copie byte-identiche dei precedenti script indipendenti. X mantiene 23 letterali PASS più X23 già adattato PASS. X23 letterale fallisce perché attendeva l'interruzione difettosa C02; il log è conservato. L'adattamento conserva TimeoutError e pretende 120 INVALID, T3/T6 falliti, 40 triplette non valutabili, dati non osservati null, riconciliazione immutabile e nessun reinvio. Nessuna nuova assertion modificata.

Y genera i ledger legacy con il vecchio codice esatto 0c8157f, senza SQL che fabbrichi la precedenza. Z e W usano nuove fixture sacrificiali. Tutte passano. V è una nuova suite indipendente: sei metodi, quattro PASS e due failure pertinenti allo stesso D04. Le fixture non sono dati scientifici; nessuna API reale.

| Metodo e sorgente | Esito corrente | Provenienza/limite |
| --- | --- | --- |
'''
sources=[('X',E/'literal/evidence/extended_probes.py'),('X',E/'literal/evidence/additional_edges.py'),('Y',E/'y_original/evidence/edge_probes.py'),('Z',E/'z_original/evidence/chain_probes.py'),('W',E/'w_original/evidence/retry_proof_probes.py'),('V',E/'independent_d03_probes.py')]
entries=[]
for group,p in sources:
 for n in ast.walk(ast.parse(p.read_text())):
  if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'+group):
   number=int(n.name[6:8]);result='FAIL letterale, PASS adattato' if group=='X' and number==23 else 'FAIL — D04' if group=='V' and number>=5 else 'PASS'
   note='nuova prova indipendente' if group=='V' else '23 letterali + solo X23 già adattato' if group=='X' else 'script byte-identico, nessuna modifica'
   entries.append(dict(group=group,number=number,name=n.name,path=str(p),line=n.lineno,result=result))
   text+=f'| {link(p,n.name,n.lineno)} | {result} | {note} |\n'
text+='''
V01: morte reale del processo dopo il primo evento, il secondo evento e stato/INVALID prima del commit: rollback integrale; morte dopo commit: ripresa conforme senza nuovi intenti. V02: parsing/hash sugli stessi byte letti una sola volta; hash file distinti da digest contenuti; modifica a un dato annidato forense dentro un contenitore normativo respinta. V03: FAILED già INVALID poi riconciliato, record immutabile e nessuna risposta inventata; altro processo bloccato da BEGIN IMMEDIATE durante la verifica e libero dopo; nuova alterazione respinta nella stessa istanza. V04: producer aperto, prova alterata respinta prima della costruzione del client e del retry.

V05: dopo sette retry leciti l'ottavo è rifiutato. Si altera solo quota_kind di un vecchio retry da transport a base: binding aperto e ottavo retry vengono accettati. V06: stessa sequenza nel producer ordinario, un nuovo invio allo stub; il successivo HarnessError è il timeout dello stub, non il rifiuto preventivo. Otto archi retry_of contro sette transport_calls, nessun waiver, nove intenti totali. Non sono otto test né un GO.
'''
(E/'MATRICE_ESTENSIONI.md').write_text(text);(E/'MATRICE_ESTENSIONI.json').write_text(json.dumps(entries,indent=2)+'\n')
print(json.dumps(dict(originals=len(rows),modes=dict(collections.Counter(r['mode'] for r in rows)),extensions=dict(collections.Counter(r['group'] for r in entries)))))
