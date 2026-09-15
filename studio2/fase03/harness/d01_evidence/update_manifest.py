from pathlib import Path
import hashlib,json
root=Path('/Users/luker/fot-tep-harness-0310-d01');h=root/'studio2/fase03/harness';p=h/'HARNESS_OFFLINE_CANDIDATE.json';v=json.loads(p.read_text())
v.update(artifact_version='4',delivery_base_commit='52e13e1ed540e1ad076474398bf850445c9a4a00',rejected_candidate='9e18bcbd06fa2c54202c8eeda079c112dbfcefcd',rejected_tree='5d1fd7924c4e1e46346f367590e6aa1977a6ba75',acquisition_commit='89b016a728bdbf5d2d8b438416e6133b050683da',non_ok_report_sha256='35e047834ec957a8008db7b82c375d3022cbcfeb7a8d2fb80143f44e9cabfe42',non_ok_manifest_sha256='29385ea6589286e7a551c13ee61c8588b7b5792dabba7fa5d3ebebcd090a34ea',matrix='MATRICE_R01_R10_D01.md',correction_scope=['D01 / C01 / R04: confirmation of legacy outcomes'],previous_verified_closures=['C02','C03'])
v['historical_documents_superseded_for_this_delta']+=['REPORT_CORREZIONI_C01_C03.md','PROMPT_VERIFICA_C01_C03.md','CONSEGNA_C01_C03.json']
paths={r['path'] for r in v['files']}
paths.update('studio2/fase03/harness/'+n for n in ['test_d01_replay.py','MATRICE_R01_R10_D01.md','d01_evidence/RESULTS.json','d01_evidence/SHA256SUMS','d01_evidence/REPRODUCTION_INVENTORY.json','d01_evidence/COMANDI.md','non_ok_9e18bcb_20260915/ACQUISITION_INVENTORY.json','non_ok_9e18bcb_20260915/PROVENIENZA.md'])
v['files']=[dict(path=n,bytes=(root/n).stat().st_size,sha256=hashlib.sha256((root/n).read_bytes()).hexdigest()) for n in sorted(paths)]
assert len(v['files'])==62
v['manifest_scope']='62 direct files. Proof SHA256SUMS covers copied artifacts; acquisition and reproduction inventories describe exact external paths, hashes and dimensions. This manifest and subsequent documentary report/prompt/delivery/audit excluded to avoid self-reference.'
p.write_text(json.dumps(v,indent=2)+'\n')
print(len(v['files']),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size)
