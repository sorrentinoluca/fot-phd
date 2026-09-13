#!/usr/bin/env python3
"""Read-only verification of the single prespecified F1 smoke; never launches MATLAB."""
import csv
import json
import math
from pathlib import Path
from fault_protocol import HERE, audit_campaign


def verify():
    root=HERE/'smoke'
    campaign=root/'f1_short_001'
    audit=audit_campaign(HERE/'plans/smoke.csv',campaign)
    r=json.loads((campaign/'smoke-F1-001.manifest.json').read_text())
    launch=json.loads((root/'LAUNCH_TIMING.json').read_text())
    assert r['status']=='complete' and r['idv']==1 and r['stream_id']=='30040'
    assert r['horizon_h']==0.1 and r['actual_end_h']==25.1
    assert r['useful_windows_complete']==0 and r['pre_fault_window']['development_eligible'] is False
    diag=list(csv.DictReader(Path(r['diagnostic_path']).open()))
    control=[x for x in diag if 20 <= float(x['time_h']) < 25]
    post=[x for x in diag if float(x['time_h']) > 25+1e-8]
    assert len(control)==300 and len(post)==6
    assert all(float(x['idv_mask'])==0 for x in diag if float(x['time_h'])<25)
    assert all(float(x['idv_mask'])==1 for x in post)
    pre_values={'feed_a_pct':48.5,'feed_b_pct':0.5,'feed_c_pct':51.0}
    post_values={'feed_a_pct':45.5,'feed_b_pct':0.5,'feed_c_pct':54.0}
    # Verify the implemented F1 forcing, not separability or a new scientific threshold.
    for name,value in pre_values.items():
        assert all(math.isclose(float(x[name]),value,abs_tol=1e-10,rel_tol=0) for x in control)
    for name,value in post_values.items():
        assert all(math.isclose(float(x[name]),value,abs_tol=1e-10,rel_tol=0) for x in post)
    assert launch['exit_code']==0
    assert len(list((HERE/'smoke').glob('*/*.manifest.json')))==1
    assert not (HERE/'runs').exists(), 'Full batch must remain unexecuted in this window'
    total=40*r['runtime_seconds']*65/25.1
    simulation=40*r['simulation_seconds']*65/25.1
    process_overhead=launch['wall_seconds']-r['runtime_seconds']
    return {'status':'PASS','simulations_executed':1,'fault':'F1','stream_id':'30040',
            'batch_runs_executed':0,'audit':audit,'control_samples':len(control),
            'post_onset_samples_including_endpoint':len(post),
            'pre_composition_pct':pre_values,'post_composition_pct':post_values,
            'nominal_onset_h':25,'observed_onset_h':r['observed_onset_h'],
            'onset_observation_lag_seconds':(r['observed_onset_h']-25)*3600,
            'first_active_saved_sample_h':min(float(x['time_h']) for x in diag if float(x['idv_mask'])==1),
            'boundary_sample_at_25h_retained_unchanged':True,
            'runtime_seconds':r['runtime_seconds'],'simulation_seconds':r['simulation_seconds'],
            'matlab_process_wall_seconds':launch['wall_seconds'],
            'projection_40_run_seconds':total,'projection_simulation_only_seconds':simulation,
            'measured_process_overhead_seconds':process_overhead,
            'projection_with_one_process_overhead_seconds':total+process_overhead,
            'projection_formula':'40 * runtime_smoke * 65 / 25.1',
            'projection_limitation':'single short F1, linear scaling; no measured distribution across faults, no bound',
            'regime_claim':'control input composition nominal; no statistical proof of process stationarity'}

if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
