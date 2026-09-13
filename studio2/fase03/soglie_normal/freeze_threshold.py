#!/usr/bin/env python3
"""Freeze the Normal threshold before opening far_ver contents."""
import argparse, csv, hashlib, json, math, subprocess
from datetime import datetime, timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; F2=ROOT/'studio2'/'fase02'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--scores',type=Path,required=True); ap.add_argument('--audit',type=Path,required=True); ap.add_argument('--plan',type=Path,required=True); ap.add_argument('--far-plan',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
    scores=list(csv.DictReader(a.scores.open())); audit=json.loads(a.audit.read_text()); plan=list(csv.DictReader(a.plan.open())); farplan=list(csv.DictReader(a.far_plan.open()))
    if len(scores)!=350 or len(plan)!=350 or not audit.get('pass'): raise SystemExit('freeze prerequisites failed')
    values=sorted(float(r['S']) for r in scores); n=len(values); alpha=0.05; rank=math.ceil((n+1)*(1-alpha)); threshold=values[rank-1]
    far_records=[r for r in audit['records'] if r['set_name']=='far_ver']
    if len(far_records)!=150 or len(farplan)!=150: raise SystemExit('far seal count failure')
    far_by_id={r['run_id']:r for r in far_records}
    seal=[{'run_id':p['run_id'],'stream_id':int(p['stream_id']),'path':far_by_id[p['run_id']]['path'],'sha256':far_by_id[p['run_id']]['sha256']} for p in farplan]
    sources={'cal_thr_scores_csv':sha(a.scores),'score_fit_legacy_json':sha(F2/'validation'/'score_fit_legacy.json'),'combined_score_py':sha(F2/'analysis'/'combined_score.py'),'tep_features_py':sha(F2/'analysis'/'tep_features.py'),'validate_numerics_py':sha(F2/'analysis'/'validate_numerics.py'),'cal_thr_plan_csv':sha(a.plan),'far_ver_plan_csv':sha(a.far_plan),'precalibration_freeze_json':sha(F2/'validation'/'PRECALIBRATION_FREEZE.json'),'lot_audit_json':sha(a.audit)}
    result={'freeze_status':'frozen_before_far_ver_analysis','frozen_at_utc':datetime.now(timezone.utc).isoformat(),'source_head_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'alpha':alpha,'n':n,'rank':rank,'threshold':threshold,'rule':'S > threshold','score_variant':'A','score_ties_at_threshold':sum(v==threshold for v in values),'cal_thr_scores_sha256':sources['cal_thr_scores_csv'],'sources':sources,'far_ver_seal':seal}
    if any(len(r['sha256'])!=64 for r in seal): raise SystemExit('far seal digest length failure')
    a.output.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({'threshold':threshold,'rank':rank,'n':n,'far_sealed':len(seal),'output':str(a.output)},indent=2))
if __name__=='__main__': main()
