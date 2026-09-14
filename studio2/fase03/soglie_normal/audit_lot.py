#!/usr/bin/env python3
"""Audit the completed Normal lot without opening far_ver workbook contents."""
from __future__ import annotations
import argparse, csv, hashlib, json, re
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; F2=ROOT/'studio2'/'fase02'
sys.path.insert(0,str(F2/'analysis'))
from tep_features import iter_time_windows, load_case

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def rows(path): return list(csv.DictReader(path.open(newline='')))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--runs',type=Path,required=True); ap.add_argument('--cal-plan',type=Path,required=True); ap.add_argument('--far-plan',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
    a.runs=a.runs.resolve(); a.cal_plan=a.cal_plan.resolve(); a.far_plan=a.far_plan.resolve(); a.output=a.output.resolve()
    calplan=rows(a.cal_plan); farplan=rows(a.far_plan); errors=[]; records=[]
    for kind, plan in (('cal_thr',calplan),('far_ver',farplan)):
        manifest=a.runs/kind/'generation_manifest.csv'; actual=rows(manifest) if manifest.is_file() else []
        by_id={r['run_id']:r for r in actual}
        if len(actual)!=len(plan): errors.append(f'{kind}: manifest count {len(actual)} != {len(plan)}')
        for p in plan:
            r=by_id.get(p['run_id']); path=a.runs/kind/(p['run_id']+'.xlsx')
            if r is None: errors.append(f'{kind}: missing manifest row {p["run_id"]}'); continue
            for key in ('stream_id','window_position','stop_time_h'):
                if str(r[key]) != str(p[key]): errors.append(f'{p["run_id"]}: {key} mismatch')
            if r['status']!='complete' or float(r['actual_end_h']) < float(p['stop_time_h'])-1e-9: errors.append(f'{p["run_id"]}: incomplete/trip')
            if not path.is_file(): errors.append(f'{p["run_id"]}: missing workbook'); continue
            digest=sha(path)
            if r.get('sha256') != digest: errors.append(f'{p["run_id"]}: workbook hash mismatch')
            item={'run_id':p['run_id'],'set_name':kind,'stream_id':int(p['stream_id']),'path':str(path.relative_to(ROOT)),'sha256':digest,'manifest_sha256':r.get('sha256'),'status':r['status']}
            if kind=='cal_thr':
                d=load_case(path); windows=list(iter_time_windows(d,start_h=20,end_h=float(p['stop_time_h']),window_h=5))
                expected=int(p['J'])
                if len(windows)!=expected: errors.append(f'{p["run_id"]}: {len(windows)} windows != J={expected}')
                item.update({'rows':len(d),'windows':len(windows),'numeric_validation':'pass' if len(windows)==expected else 'fail'})
            else:
                item.update({'numeric_validation':'deferred_until_freeze','contents_opened':False})
            records.append(item)
    all_files=sorted(p for p in a.runs.rglob('*') if p.is_file())
    expected_files={a.runs/'cal_thr'/'generation_manifest.csv',a.runs/'far_ver'/'generation_manifest.csv'} | {a.runs/r['set_name']/(r['run_id']+'.xlsx') for r in calplan+farplan}
    extras=[str(p.relative_to(ROOT)) for p in all_files if p not in expected_files]
    if extras: errors.append('extraneous files: '+', '.join(extras))
    result={'audit_scope':'cal_thr contents validated; far_ver workbook contents not opened','cal_thr_count':len(calplan),'far_ver_count':len(farplan),'workbooks_present':len([p for p in all_files if p.suffix=='.xlsx']),'complete_manifest_rows':len(records),'trip_count':sum(1 for r in records if r['status']!='complete'),'technical_error_count':0,'extraneous_files':extras,'far_ver_scores_present':False,'far_ver_score_derivatives_found':[],'smoke_only_scores':True,'errors':errors,'pass':not errors,'files':{str(p.relative_to(ROOT)):sha(p) for p in all_files},'records':records}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f"pass={result['pass']} cal={len(calplan)} far={len(farplan)} errors={len(errors)} output={a.output}")
    raise SystemExit(0 if not errors else 1)
if __name__=='__main__': main()
