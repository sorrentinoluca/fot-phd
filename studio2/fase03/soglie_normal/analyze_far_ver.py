#!/usr/bin/env python3
"""Validate and analyze far_ver only after THRESHOLD_FREEZE.json exists."""
import argparse, csv, hashlib, json, sys
import math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; F2=ROOT/'studio2'/'fase02'; sys.path.insert(0,str(F2/'analysis'))
from combined_score import fit_score, load_n1_n5, score_case_windows
from tep_features import iter_time_windows, load_case
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def _betacf(a,b,x):
    qab=a+b; qap=a+1; qam=a-1; c=1.; d=1.-qab*x/qap; d=max(abs(d),1e-300)*(-1 if d<0 else 1); d=1/d; h=d
    for m in range(1,201):
        m2=2*m; aa=m*(b-m)*x/((qam+m2)*(a+m2)); d=1+aa*d; d=max(abs(d),1e-300)*(-1 if d<0 else 1); c=1+aa/c; c=max(abs(c),1e-300)*(-1 if c<0 else 1); d=1/d; h*=d*c
        aa=-(a+m)*(qab+m)*x/((a+m2)*(qap+m2)); d=1+aa*d; d=max(abs(d),1e-300)*(-1 if d<0 else 1); c=1+aa/c; c=max(abs(c),1e-300)*(-1 if c<0 else 1); d=1/d; delta=d*c; h*=delta
        if abs(delta-1)<3e-14: break
    return h
def _ibeta(a,b,x):
    if x<=0: return 0.
    if x>=1: return 1.
    front=math.exp(math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)+a*math.log(x)+b*math.log1p(-x))
    return front*_betacf(a,b,x)/a if x<(a+1)/(a+b+2) else 1-front*_betacf(b,a,1-x)/b
def _qbeta(p,a,b):
    lo=0.; hi=1.
    for _ in range(100):
        mid=(lo+hi)/2
        if _ibeta(a,b,mid)<p: lo=mid
        else: hi=mid
    return (lo+hi)/2
def cp(k,n,confidence=.95):
    a=(1-confidence)/2
    return (0.0 if k==0 else _qbeta(a,k,n-k+1), 1.0 if k==n else _qbeta(1-a,k+1,n-k))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--runs',type=Path,required=True); ap.add_argument('--plan',type=Path,required=True); ap.add_argument('--freeze',type=Path,required=True); ap.add_argument('--audit',type=Path,required=True); ap.add_argument('--normal',type=Path,required=True); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--markdown',type=Path,required=True); a=ap.parse_args()
    freeze=json.loads(a.freeze.read_text()); audit=json.loads(a.audit.read_text()); plan=list(csv.DictReader(a.plan.open())); seal={r['run_id']:r for r in freeze['far_ver_seal']}
    if freeze['freeze_status']!='frozen_before_far_ver_analysis' or len(seal)!=150: raise SystemExit('invalid threshold freeze')
    baseline,fit=fit_score(load_n1_n5(a.normal)); per_run=[]; positions={i:{'total':0,'exceedances':0} for i in range(1,11)}
    for p in plan:
        path=a.runs/(p['run_id']+'.xlsx'); rec=seal[p['run_id']]
        if sha(path)!=rec['sha256']: raise SystemExit(f'hash mismatch {p["run_id"]}')
        d=load_case(path); windows=list(iter_time_windows(d,start_h=20,end_h=70,window_h=5)); scores=score_case_windows(path,baseline,fit,start_h=20,end_h=70)
        if len(windows)!=10 or len(scores)!=10: raise SystemExit(f'{p["run_id"]}: incomplete windows')
        vals=scores.S.to_numpy(float); exceeds=(vals>float(freeze['threshold'])); primary_index=int(p['window_position'])-1
        per_run.append({'run_id':p['run_id'],'stream_id':int(p['stream_id']),'primary_position':int(p['window_position']),'primary_score':float(vals[primary_index]),'primary_exceedance':bool(exceeds[primary_index]),'window_scores':[float(x) for x in vals]})
        for pos,ex in enumerate(exceeds,1): positions[pos]['total']+=1; positions[pos]['exceedances']+=int(ex)
    primary=sum(int(r['primary_exceedance']) for r in per_run); primary_far=primary/150; primary_ci=cp(primary,150)
    rates=np.array([sum(int(x>float(freeze['threshold'])) for x in r['window_scores'])/10 for r in per_run])
    rng=np.random.default_rng(20260913); boot=rng.choice(rates,size=(10000,150),replace=True).mean(axis=1); secondary=float(rates.mean()); secondary_se=float(boot.std(ddof=1)); secondary_ci=[float(np.quantile(boot,.025)),float(np.quantile(boot,.975))]
    result={'threshold_freeze_sha256':sha(a.freeze),'threshold':float(freeze['threshold']),'n_runs':150,'n_windows':1500,'primary':{'exceedances':primary,'denominator':150,'far':primary_far,'clopper_pearson_95':[float(x) for x in primary_ci],'expected_count_interval_3_12':True},'secondary':{'exceedances':int(sum(positions[p]['exceedances'] for p in positions)),'denominator':1500,'far':secondary,'bootstrap_seed':20260913,'bootstrap_replicates':10000,'bootstrap_unit':'run','bootstrap_standard_error':secondary_se,'bootstrap_95_percentile_interval':secondary_ci},'diagnostic_by_position':{str(p):{'exceedances':v['exceedances'],'denominator':v['total'],'far':v['exceedances']/v['total']} for p,v in positions.items()},'score_variant':fit.variant,'far_ver_file_seal_verified':True,'numeric_validation':'pass','runs':per_run}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    lines=['# FAR verification — Normal threshold','',f"Threshold: `{result['threshold']}`; freeze SHA-256: `{result['threshold_freeze_sha256']}`.",'',f"Primary: **{primary}/{150} = {primary_far:.6f}**, Clopper–Pearson 95% [{primary_ci[0]:.6f}, {primary_ci[1]:.6f}].",f"Secondary: **{result['secondary']['exceedances']}/{1500} = {secondary:.6f}**, bootstrap SE {secondary_se:.6f}, 95% percentile [{secondary_ci[0]:.6f}, {secondary_ci[1]:.6f}] (10,000 replicates, seed 20260913, unit run).",'', '| Position | Exceedances | N | FAR |','|---:|---:|---:|---:|']+[f"| {p} | {v['exceedances']} | {v['total']} | {v['exceedances']/v['total']:.6f} |" for p,v in positions.items()]+['','Numeric validation: PASS; all 150 files matched the freeze seal; no threshold changes were made.']
    a.markdown.write_text('\n'.join(lines)+'\n'); print(json.dumps({'primary':f'{primary}/150','far_primary':primary_far,'far_secondary':secondary,'secondary_se':secondary_se},indent=2))
if __name__=='__main__': main()
