from pathlib import Path
import json
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--harness-dir',type=Path,required=True);parser.add_argument('--checks-dir',type=Path,required=True);args=parser.parse_args()
H=args.harness_dir;K=args.checks_dir
c=json.loads((H/'DURABLE_FIELD_CONTRACT.json').read_text());r=json.loads((K/'red_contract.json').read_text());g=json.loads((K/'green_contract.json').read_text())
assert (r['tests'],r['failures'],r['errors'])==(9,8,0)
assert (g['tests'],g['failures'],g['errors'])==(9,0,0)
a,b=r['observations'],g['observations'];rows=[]
for f in c['fields']:
 row=dict(f)
 if f['scope']=='sql':
  row.update(red=[x for x in a['sql_matrix'] if x['field']==f['path']],green=[x for x in b['sql_matrix'] if x['field']==f['path']],verification='generated SQL field mutation')
 elif f['scope']=='zero_token':
  row.update(red=[x for x in a['symmetric'] if x['field']==f['path']],green=[x for x in b['symmetric'] if x['field']==f['path']],verification='generated field variants across acquisition/retry/gate')
 elif f['event'] in ('reconciled','reconciled_integrity'):
  row.update(red=[x for x in a['envelope_matrix'] if x['field']==f['path']],green=[x for x in b['envelope_matrix'] if x['field']==f['path']],verification='generated envelope field deletion')
 else:
  row.update(verification='historical contract tests; no new per-field mutation claim',reference='non_ok_a219bd4_20260915/files/MATRICE_50_METODI.md',tests={'outcome':'test_D02_record_digest_binding_and_frozen_evidence_are_reauthenticated / X01,X02,X04','frozen_gate':'test_R08_* / X18 / D02','transport_invalidity':'test_C02_* / Z05 / X23 adapted','remediation_authorized':'test_R06_* / X10,X20,X24','remediation_waived':'test_R05_* / X09','suspended':'test_R01_* / test_R09_* / Y03,Y05','note':'D03 SQL matrix forensic positive control'}[f['event']])
 rows.append(row)
result=dict(inventory='DURABLE_FIELD_CONTRACT.json',entries=len(rows),new_generated_field_entries=sum('green' in r for r in rows),historical_contract_entries=sum('green' not in r for r in rows),default='DA_COPRIRE',symmetry=dict(fields=11,variants=len(b['symmetric']),routes=3,controls=b['shared_controls']),rows=rows,limits='Field classifications are complete for named structures; opaque sealed JSON subtrees inherit N. This finite matrix does not enumerate every value or combined fault; historical per-field mutation is not claimed.')
(H/'MATRICE_D03_CAMPI.json').write_text(json.dumps(result,indent=2)+'\n')
text='''# Matrice dei campi durevoli — generata dall’inventario\n\nFonte: [DURABLE_FIELD_CONTRACT.json](DURABLE_FIELD_CONTRACT.json). Default per nuovi campi strutturali, incluse le chiavi nominate di evidence/approval: **DA_COPRIRE**. I payload opachi improntati ereditano la classe N per tutti i discendenti.\n\nN = normativo; F = forense. La prova SQL altera una colonna per volta; le varianti evidence/approval sono applicate in acquisizione, antenato retry e gate riconciliato. Non si sommano metodi, sottocasi e verifiche sovrapposte.\n\n'''
text+=f"Inventario: **{len(rows)} voci**, **{result['new_generated_field_entries']}** esercitate dalle nuove mutazioni generate e **{result['historical_contract_entries']}** collegate alle prove di contratto storiche. Per queste ultime non si dichiara una nuova mutazione individuale di ogni campo. **37 varianti × 3 percorsi**, 11 controlli di contenuto comuni, 33 colonne SQL, 12 campi degli involucri di riconciliazione e 14 alterazioni di contenuti/impronte apparentemente plausibili.\n\n"
text+='| Campo | Classe | Copertura |\n| --- | --- | --- |\n'
for row in rows:text+='| `'+row['path']+'` | '+row['kind']+' | '+row['verification']+' |\n'
text+='\nIl [JSON completo](MATRICE_D03_CAMPI.json) contiene gli esiti rosso/verde e le corrispondenze storiche. Matrice simmetrica e matrice SQL sono rosse su a219bd4; tutte le aspettative generate sono verdi dopo il delta. La guardia controlla anche schema e campi nuovi annidati; non è una dimostrazione di esaustività per ogni valore o combinazione di guasti.\n'
(H/'MATRICE_D03_CAMPI.md').write_text(text)
print('Generated',len(rows),'entries;',result['new_generated_field_entries'],'new field entries;',result['historical_contract_entries'],'historical')
