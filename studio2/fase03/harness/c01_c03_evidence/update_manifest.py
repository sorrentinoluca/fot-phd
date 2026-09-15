from pathlib import Path
import hashlib,json
root=Path('/Users/luker/fot-tep-harness-0310-c01-c03');h=root/'studio2/fase03/harness';p=h/'HARNESS_OFFLINE_CANDIDATE.json';v=json.loads(p.read_text())
v.update(artifact_version='3',delivery_base_commit='6268437b8b64288b50ad5f7c924e1fcab85b27d3',rejected_candidate='0c8157f23bee49a3a5a2df648525c34706da29d7',rejected_tree='a1573b49615a875f24ee97f9f1cd4bab399be93d',acquisition_commit='b882c27103dbd9d0e0462df20731123f5ed5a0c1',non_ok_report_sha256='1785fb3cfb832b5a299fe885ac740a4f557ad83431e002451d447afab64f4efc',non_ok_manifest_sha256='e5cb1589a9f8006303c9ea91a3ea37be742990c2ac6c86fb8ffc7e59fcbf7f80',matrix='MATRICE_R01_R10_C01_C03.md',correction_scope=['C01 / R04','C02 / R07 / N48','C03 / R07'],producer_summary_version='4',ledger_schema_version=2)
v['historical_documents_superseded_for_this_delta']+=['REPORT_CORREZIONI_HARNESS_03_10.md','PROMPT_VERIFICA_CORREZIONI_HARNESS_03_10.md','CONSEGNA_CORREZIONI_HARNESS_03_10.json']
paths={r['path'] for r in v['files']}
paths.update('studio2/fase03/harness/'+n for n in ['REPORT_CORREZIONI_HARNESS_03_10.md','PROMPT_VERIFICA_CORREZIONI_HARNESS_03_10.md','test_c01_c03.py','MATRICE_R01_R10_C01_C03.md','c01_c03_evidence/SHA256SUMS','c01_c03_evidence/REPRODUCTION_INVENTORY.json','c01_c03_evidence/RESULTS.json','c01_c03_evidence/COMANDI.md','non_ok_0c8157f_20260915/ACQUISITION_INVENTORY.json','non_ok_0c8157f_20260915/PROVENIENZA.md'])
v['files']=[dict(path=n,bytes=(root/n).stat().st_size,sha256=hashlib.sha256((root/n).read_bytes()).hexdigest()) for n in sorted(paths)]
v['manifest_scope']='54 direct files; evidence SHA256SUMS covers copied new test artifacts; reproduction and acquisition inventories cover external fixtures with exact coordinates, bytes and hashes. Excludes this manifest and subsequent documentary delivery to avoid self-reference.'
assert len(v['files'])==54,len(v['files'])
p.write_text(json.dumps(v,indent=2)+'\n')
print('Manifest',len(v['files']),'files',hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size)
