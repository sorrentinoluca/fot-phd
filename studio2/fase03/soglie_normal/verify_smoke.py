#!/usr/bin/env python3
import argparse, csv, json, sys
from pathlib import Path
import pandas as pd
HERE=Path(__file__).resolve().parent; F2=HERE.parents[1]/'fase02'; sys.path.insert(0,str(F2/'analysis'))
from combined_score import fit_score, load_n1_n5, score_case_windows
from tep_features import iter_time_windows
ap=argparse.ArgumentParser(); ap.add_argument('--runs',type=Path,required=True); ap.add_argument('--normal',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
baseline,fit=fit_score(load_n1_n5(a.normal)); result={'score_variant':fit.variant,'runs':[]}
for kind,expected in (('cal_thr',1),('far_ver',10)):
    records=list(csv.DictReader((a.runs/kind/'generation_manifest.csv').open()))
    if len(records)!=1 or records[0].get('status')!='complete': raise SystemExit(f'incomplete {kind}')
    rec=records[0]; path=Path(rec['output_path']); path=path if path.is_file() else a.runs/kind/(rec['run_id']+'.xlsx')
    scores=score_case_windows(path,baseline,fit,start_h=20,end_h=float(rec['actual_end_h']))
    windows=list(iter_time_windows(pd.read_excel(path),start_h=20,end_h=float(rec['actual_end_h']),window_h=5))
    if len(scores)!=expected or len(windows)!=expected: raise SystemExit(f'{kind}: expected {expected} windows')
    result['runs'].append({'set_name':kind,'stream_id':int(rec['stream_id']),'runtime_seconds':float(rec['runtime_seconds']),'actual_end_h':float(rec['actual_end_h']),'windows':len(scores),'trip':False,'scores':[float(x) for x in scores.S]})
a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2)+'\n'); print(f'PASS smoke runs=2 windows=11 output={a.output}')
