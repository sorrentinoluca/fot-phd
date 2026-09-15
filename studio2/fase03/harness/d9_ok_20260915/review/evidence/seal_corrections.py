from pathlib import Path
import json,hashlib,shutil
W=Path('/Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review');O=W/'outputs/d9-corrections-review';E=O/'evidence'
r=json.loads((E/'RESULTS_VERIFIED.json').read_text());assert (E/'preservation_final.json').exists()
audit=json.loads((E/'source_audit.json').read_text())
for name,expected in audit['test_script_hashes'].items():assert hashlib.sha256((E/name).read_bytes()).hexdigest()==expected,name
names={'targeted':'Mirata completa — corretto','discovery':'Discovery completa — corretto','corrections_red':'Correzioni finali — respinto','corrections_green':'Stesse correzioni — corretto','original_U_red':'U01–U08 originali — respinto','original_U_green':'Stesse U01–U08 — corretto','transport_red':'Trasporto reale / SDK fittizio — respinto','transport_green':'Stesso test trasporto — corretto','guardian_rejected':'Guardiano — respinto','guardian_corrected':'Guardiano — corretto'}
rows=['| Prova | Metodi | Fallimenti | Errori | Skip | Esito |','| --- | ---: | ---: | ---: | ---: | --- |']
for k,title in names.items():
 n,f,e,skip=r[k]['counts'];status='NON PASS storico' if k.startswith('guardian') else ('Rosso discriminante' if k.endswith('_red') else 'PASS')
 rows.append(f'| {title} | {n} | {f} | {e} | {skip} | {status} |')
rows.append('| Controlli indipendenti aggiuntivi — corretto | 2 | 0 | 0 | 0 | PASS |')
report=(W/'work/VERIFICA_CORREZIONI_D9.template.md').read_text().replace('{{RESULTS_TABLE}}','\n'.join(rows));assert '{{' not in report
(O/'VERIFICA_CORREZIONI_D9.md').write_text(report)
for name in ['finalize_corrections.py','seal_corrections.py']:shutil.copy2(W/'work'/name,E/name)
shutil.copy2(W/'outputs/d9-review/evidence/verify_package.py',E/'verify_package.py')
def item(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return {'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
files=[item(p) for p in sorted(O.rglob('*')) if p.is_file() and p not in (O/'MANIFEST.json',O/'CONSEGNA.json')]
(O/'MANIFEST.json').write_text(json.dumps({'scope':'Independent D9 correction review, local offline evidence; all listed paths relative to package','technical_candidate':'16c98f39c044d812458705234b1a3f8ee4940b34','technical_tree':'1dd8f84d991190d9d8316e6c56899bc115232716','files':files},indent=2)+'\n')
cert={'verdict':'OK limitato offline','technical_candidate':'16c98f39c044d812458705234b1a3f8ee4940b34','technical_tree':'1dd8f84d991190d9d8316e6c56899bc115232716','documentary_head':'cf763333b7951b4cf711e1286657f6afc6a9df87','report':item(O/'VERIFICA_CORREZIONI_D9.md'),'manifest':item(O/'MANIFEST.json'),'members':len(files),'guardian':'NON PASS: 35 tests, 14 historical failures, 1 skip, 0 errors','original_non_ok_preserved':True,'services_or_scientific_execution':False,'go':False}
(O/'CONSEGNA.json').write_text(json.dumps(cert,indent=2)+'\n');print(json.dumps(cert,indent=2))
