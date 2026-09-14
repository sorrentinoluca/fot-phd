#!/usr/bin/env python3
"""Score only the pre-registered final window of each cal_thr run."""
import argparse, csv, hashlib, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; F2=ROOT/'studio2'/'fase02'; sys.path.insert(0,str(F2/'analysis'))
from combined_score import fit_score, load_n1_n5, score_case_windows

FIELDS=('run_id','stream_id','J','S')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--runs',type=Path,required=True); ap.add_argument('--plan',type=Path,required=True); ap.add_argument('--normal',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
    baseline,fit=fit_score(load_n1_n5(a.normal)); plan=list(csv.DictReader(a.plan.open())); out=a.output.resolve(); rows=[]
    for p in plan:
        path=a.runs/(p['run_id']+'.xlsx'); table=score_case_windows(path,baseline,fit,start_h=20,end_h=float(p['stop_time_h']))
        j=int(p['J'])
        if len(table)!=j: raise SystemExit(f'{p["run_id"]}: expected {j} windows, got {len(table)}')
        rows.append({'run_id':p['run_id'],'stream_id':int(p['stream_id']),'J':j,'S':float(table.iloc[-1].S)})
    if len(rows)!=350 or len({r['run_id'] for r in rows})!=350: raise SystemExit('cal_thr score count failure')
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n'); w.writeheader(); w.writerows(rows)
    print(json.dumps({'rows':len(rows),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'variant':fit.variant},indent=2))
if __name__=='__main__': main()
