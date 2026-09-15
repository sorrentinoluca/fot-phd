#!/usr/bin/env python3
"""Strict fault log parser, immutable run manifests and read-only batch validation."""
import argparse
import csv
import hashlib
import json
import math
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from build_generation_plan import HERE, ROOT, KEY, validate_plan

DIAG_FIELDS = ('time_h', 'idv_mask', 'feed_a_pct', 'feed_b_pct', 'feed_c_pct',
               'd_feed_temp', 'c_feed_temp', 'reactor_cw_temp', 'condenser_cw_temp',
               'kinetic_r1', 'kinetic_r2', 'reactor_valve_command',
               'condenser_valve_command', 'reactor_valve_position', 'condenser_valve_position')
RAW_FIELDS = ['Time (h)'] + [f'XMEAS-{i}' for i in range(1, 42)] + [f'XMV-{i}' for i in range(1, 13)]
REQUIRED = set('schema_version run_id set_name batch run_index_uint64 stream_id seed_descriptor '
               'stream_lo32 stream_hi32 rng_algorithm rng_key_hex counter_start counter_end '
               'idv onset_h horizon_h stop_time_h burn_in_h ts_base_h output_interval_h msflag '
               'window_h pre_fault_window post_fault_windows useful_windows_expected '
               'useful_windows_complete status actual_end_h trip_time_h trip_code message '
               'activation_observed observed_onset_h idv_trace_valid platform matlab_version '
               'started_at_utc finished_at_utc runtime_seconds simulation_seconds mex_sha256 '
               'model_sha256 script_sha256 source_sha256 base_source_sha256 plan_sha256 '
               'spec_sha256 dependency_hashes model_overrides git_commit output_path sha256 '
               'data_rows columns diagnostic_path diagnostic_sha256 simulation_log_path '
               'simulation_log_sha256'.split())


def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest() if hasattr(hashlib, 'file_digest') else hashlib.sha256(f.read()).hexdigest()


def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds')


def write_json(path, data):
    with Path(path).open('x') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')


def parse_simulation_log(text):
    diagnostics, transitions, trips = [], [], []
    for line in text.splitlines():
        line = line.strip()
        if 'FOT_' not in line:
            continue
        parts = line.split(',')
        tag = parts[0]
        expected = {'FOT_DIAG': 16, 'FOT_IDV': 3, 'FOT_TRIP': 3}
        if tag not in expected or len(parts) != expected[tag]:
            raise ValueError(f'malformed instrumentation line: {line[:100]}')
        values = [float(x) for x in parts[1:]]
        if not all(math.isfinite(x) for x in values):
            raise ValueError('non-finite diagnostics')
        if values[0] < 0 or values[1] != int(values[1]):
            raise ValueError('invalid time/mask/code')
        if tag == 'FOT_DIAG':
            if not 0 <= values[1] < 2**28:
                raise ValueError('invalid diagnostic IDV mask')
            if diagnostics and values[0] <= diagnostics[-1][0]:
                raise ValueError('nonmonotone diagnostic times')
            diagnostics.append(values)
        elif tag == 'FOT_IDV':
            if not 0 <= values[1] < 2**28:
                raise ValueError('invalid transition mask')
            if transitions and values[0] < transitions[-1][0]:
                raise ValueError('nonmonotone IDV transitions')
            transitions.append(values)
        else:
            if not 1 <= values[1] <= 8:
                raise ValueError('unknown physical trip code')
            trips.append(values)
    return diagnostics, transitions, trips


def parse_event_log(path):
    events = [json.loads(s) for s in Path(path).read_text().splitlines() if s.strip()]
    if not events or events[0]['event'] != 'campaign_start':
        raise ValueError('missing campaign_start')
    active, ended, previous, done = None, set(), None, False
    for e in events:
        t = datetime.fromisoformat(e['timestamp_utc'].replace('Z', '+00:00'))
        if t.tzinfo is None or (previous and t < previous) or done:
            raise ValueError('invalid event timestamp/order')
        previous = t
        if e['event'] == 'run_start':
            if active or e['run_id'] in ended:
                raise ValueError('duplicate/overlapping run')
            active = e['run_id']
        elif e['event'] == 'run_end':
            if active != e['run_id']:
                raise ValueError('unmatched run_end')
            ended.add(active)
            active = None
        elif e['event'] == 'campaign_end':
            if active:
                raise ValueError('campaign ended with active run')
            done = True
        elif e['event'] != 'campaign_start' or e is not events[0]:
            raise ValueError('unexpected event')
    if not done:
        raise ValueError('incomplete campaign event log')
    return events


def inspect_raw(path):
    with Path(path).open() as f:
        reader = csv.reader(f)
        if next(reader) != RAW_FIELDS:
            raise ValueError('raw data columns differ')
        rows = []
        for r in reader:
            if len(r) != 54:
                raise ValueError('raw data width differs')
            v = list(map(float, r))
            if not all(math.isfinite(x) for x in v):
                raise ValueError('non-finite raw data')
            expected_time = len(rows)/60
            if abs(v[0] - expected_time) > 1e-8:
                raise ValueError('raw time grid differs')
            rows.append(v)
    if not rows:
        raise ValueError('empty raw output')
    return rows


def check_idv(diag, transitions, onset, idv, end):
    mask = 1 << (idv-1)
    for row in diag:
        expected = 0 if row[0] < onset-1e-8 else mask
        if abs(row[0]-onset) <= 1e-8 and int(row[1]) in (0,mask):
            continue  # Continuous S-function may observe the discontinuity after this sample.
        if int(row[1]) != expected:
            raise ValueError('wrong IDV before/after onset')
    if end >= onset + 1/60:
        if len(transitions) != 1 or int(transitions[0][1]) != mask:
            raise ValueError('missing or extra IDV transition')
        if not onset-1e-8 <= transitions[0][0] <= onset+1/60+1e-8:
            raise ValueError('incorrect observed onset')
    elif transitions:
        if len(transitions) != 1 or int(transitions[0][1]) != mask or abs(transitions[0][0]-onset) > 1/60+1e-8:
            raise ValueError('unexpected transition in short prefix')
    return bool(transitions), transitions[0][0] if transitions else None


def windows(row, actual):
    def window(a, b, eligible):
        return {'start_h': a, 'end_h': b, 'development_eligible': eligible,
                'complete': actual is not None and actual >= b-1e-8}
    pre = window(20, 25, False)
    eligible = row['set_name'] == 'fault_dev'
    post = [window(25+5*j, 30+5*j, eligible) for j in range(int(row['useful_windows_expected']))]
    return pre, post


def preflight(plan, destination):
    rows = validate_plan(plan)
    dest = Path(destination).resolve()
    roots = {'fault_dev': 'runs', 'smoke': 'smoke', 'ood_preflight': 'ood_preflight'}
    parent = HERE / roots[rows[0]['set_name']]
    if dest.parent != parent or not re.fullmatch('[A-Za-z0-9_-]+', dest.name):
        raise ValueError('destination must be a direct campaign child of the prescribed root')
    if parent.exists() and any(p.is_dir() for p in parent.iterdir()):
        raise FileExistsError('this namespace already has a campaign directory; no implicit rerun')
    if dest.exists():
        raise FileExistsError('refusing existing campaign directory')
    # Verify the scientific base dependencies before any run or output allocation.
    audit = json.loads((HERE/'SOURCE_AUDIT.json').read_text())
    for f in audit['files']:
        if f['path'].startswith('studio2/fase02/') or f['path'].endswith('CATALOG_FREEZE.json'):
            if digest(ROOT/f['path']) != f['sha256']:
                raise ValueError(f'changed dependency: {f["path"]}')
    return rows


def finalize(meta_path):
    meta_path = Path(meta_path).resolve()
    meta = json.loads(meta_path.read_text())
    row = meta.pop('plan_row')
    directory = meta_path.parent
    run_id = row['run_id']
    raw = directory/(run_id+'.csv')
    log = directory/(run_id+'.simulation.log')
    diagnostic = directory/(run_id+'.diagnostics.csv')
    record = dict(meta)
    if record.get('counter_end') == []:
        record['counter_end'] = None
    for key in ('run_id', 'set_name', 'seed_descriptor', 'run_index_uint64', 'stream_id'):
        record[key] = str(row[key])
    for key in ('batch', 'idv', 'stream_lo32', 'stream_hi32', 'useful_windows_expected'):
        record[key] = int(row[key])
    for key in ('onset_h', 'horizon_h', 'stop_time_h', 'burn_in_h', 'window_h'):
        record[key] = float(row[key])
    record.update(schema_version=1, rng_algorithm='Philox4x32-10', rng_key_hex=KEY,
                  counter_start='0', ts_base_h=0.0005, output_interval_h=1/60, msflag=0,
                  trip_time_h=None, trip_code=None, activation_observed=False, observed_onset_h=None,
                  idv_trace_valid=False, output_path=None, sha256=None, data_rows=0, columns=54,
                  actual_end_h=None, diagnostic_path=None, diagnostic_sha256=None,
                  simulation_log_path=str(log), simulation_log_sha256=digest(log))
    error = record.pop('technical_error', '')
    record['status'] = 'technical_failure' if error else 'complete'
    record['message'] = error
    try:
        diag, transitions, trips = parse_simulation_log(log.read_text())
        # Preserve a positively observed trip even if a later technical check fails.
        if trips:
            record['trip_time_h'], code = trips[0]
            record['trip_code'] = int(code)
        if error:
            raise ValueError(error)
        data = inspect_raw(raw)
        end = data[-1][0]
        if len(diag) != len(data) or any(abs(a[0]-b[0]) > 1e-8 for a,b in zip(diag,data)):
            raise ValueError('diagnostic grid differs from saved data')
        active, first = check_idv(diag, transitions, record['onset_h'], record['idv'], end)
        record.update(actual_end_h=end, activation_observed=active, observed_onset_h=first,
                      idv_trace_valid=True, data_rows=len(data))
        if trips:
            trip_time = trips[0][0]
            if not end-1e-8 <= trip_time <= end+1/60+1e-8 or trip_time > record['stop_time_h']+1e-8:
                raise ValueError('trip time incompatible with saved prefix')
            record['actual_end_h'] = trip_time
            record['status'] = 'physical_trip'
            record['message'] = f'Physical shutdown code {int(trips[0][1])}; prefix retained'
        elif abs(end-record['stop_time_h']) > 1e-8:
            raise ValueError('early stop without instrumented physical trip')
        if not str(record.get('counter_end', '')).isdigit() or int(record['counter_end']) <= 0:
            raise ValueError('missing final RNG counter')
        with diagnostic.open('x', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(DIAG_FIELDS)
            writer.writerows(diag)
        record.update(output_path=str(raw), sha256=digest(raw), diagnostic_path=str(diagnostic),
                      diagnostic_sha256=digest(diagnostic))
    except Exception as exc:
        record['status'] = 'technical_failure'
        record['message'] = str(exc)
        if raw.exists():
            record['quarantined_output_path'] = str(raw)
            record['quarantined_output_sha256'] = digest(raw)
    pre, post = windows(row, record['actual_end_h'])
    record.update(pre_fault_window=pre, post_fault_windows=post,
                  useful_windows_complete=sum(w['complete'] for w in post))
    record['finished_at_utc'] = utcnow()
    record['runtime_seconds'] = (datetime.fromisoformat(record['finished_at_utc']) -
        datetime.fromisoformat(record['started_at_utc'].replace('Z','+00:00'))).total_seconds()
    validate_manifest(record, verify_files=True)
    write_json(directory/(run_id+'.manifest.json'), record)
    print(record['status'])
    return record


def validate_manifest(record, verify_files=False):
    if not REQUIRED <= record.keys():
        raise ValueError('missing manifest fields: '+str(sorted(REQUIRED-record.keys())))
    if record['status'] not in ('complete','physical_trip','technical_failure','not_run'):
        raise ValueError('invalid manifest status')
    expected_horizon = 0.1 if record['set_name']=='smoke' else 40
    if record['set_name'] not in ('fault_dev','smoke','ood_preflight'):
        raise ValueError('unknown run set')
    invariants = {'onset_h':25, 'stop_time_h':25+expected_horizon, 'horizon_h':expected_horizon,
                  'burn_in_h':20, 'ts_base_h':0.0005, 'output_interval_h':1/60, 'msflag':0, 'window_h':5}
    if any(record[k] != v for k,v in invariants.items()):
        raise ValueError('manifest violates invariant timing/configuration')
    expected_row = next((r for r in __import__('build_generation_plan').build_rows(record['set_name'])
                         if r['run_id']==record['run_id']), None)
    if expected_row is None or any(str(record[k]) != str(expected_row[k]) for k in
            ('idv','batch','stream_id','seed_descriptor','stream_lo32','stream_hi32','useful_windows_expected')):
        raise ValueError('manifest identity differs from reserved plan')
    pre,post = windows(expected_row, record['actual_end_h'])
    if record['pre_fault_window'] != pre or record['post_fault_windows'] != post or \
            record['useful_windows_complete'] != sum(w['complete'] for w in post):
        raise ValueError('manifest window roles/counts inconsistent')
    if record['status'] in ('complete','physical_trip') and any(not record[k] for k in
            ('output_path','sha256','diagnostic_path','diagnostic_sha256','simulation_log_path','simulation_log_sha256')):
        raise ValueError('successful/tripped run missing artifacts')
    if record['rng_key_hex'] != KEY or record['rng_algorithm'] != 'Philox4x32-10':
        raise ValueError('RNG changed')
    for field in ('run_index_uint64','stream_id','counter_start'):
        if not isinstance(record[field],str) or not record[field].isdigit() or not 0 <= int(record[field]) < 2**64:
            raise ValueError('uint64 fields must be exact decimal strings')
    if record['run_index_uint64'] != record['stream_id']:
        raise ValueError('index/stream mismatch')
    if record['counter_end'] is not None and (not isinstance(record['counter_end'],str) or
            not record['counter_end'].isdigit() or not 0 <= int(record['counter_end']) < 2**64):
        raise ValueError('invalid draw counter')
    if record['pre_fault_window']['development_eligible'] is not False:
        raise ValueError('pre-fault control cannot enter development')
    if record['set_name']=='ood_preflight' and any(w['development_eligible'] for w in record['post_fault_windows']):
        raise ValueError('technical OOD preflight cannot enter scientific data')
    if record['trip_time_h'] is None and record['status']=='physical_trip':
        raise ValueError('physical trip without time')
    if record['status']=='complete' and (record['trip_time_h'] is not None or
            abs(record['actual_end_h']-record['stop_time_h']) > 1e-8 or not record['idv_trace_valid']):
        raise ValueError('inconsistent completed run')
    for field in ('mex_sha256','model_sha256','script_sha256','source_sha256','base_source_sha256',
                  'plan_sha256','spec_sha256'):
        if not re.fullmatch('[0-9a-f]{64}',record[field]):
            raise ValueError(f'invalid hash: {field}')
    if not math.isfinite(record['runtime_seconds']) or record['runtime_seconds']<0:
        raise ValueError('invalid runtime')
    if verify_files:
        for path_key, hash_key in [('output_path','sha256'),('diagnostic_path','diagnostic_sha256'),
                                  ('simulation_log_path','simulation_log_sha256'),
                                  ('quarantined_output_path','quarantined_output_sha256')]:
            if record.get(path_key):
                if digest(record[path_key]) != record[hash_key]:
                    raise ValueError('artifact hash mismatch: '+path_key)
            elif record.get(hash_key) is not None:
                raise ValueError('hash without artifact path')


def finish_campaign(plan, dest):
    rows = validate_plan(plan)
    dest = Path(dest).resolve()
    records = []
    for row in rows:
        p = dest/(row['run_id']+'.manifest.json')
        if p.exists():
            records.append(json.loads(p.read_text()))
        else:
            # A stopped campaign makes every unexecuted index explicit, with no invented run data.
            record = dict(records[-1]) if records else None
            if record is None:
                raise ValueError('no attempted manifest; campaign failed before any run')
            for k in ('run_id','set_name','run_index_uint64','stream_id','seed_descriptor'):
                record[k] = row[k]
            for k in ('batch','idv','stream_lo32','stream_hi32'):
                record[k] = int(row[k])
            for k in ('output_path','sha256','diagnostic_path','diagnostic_sha256','simulation_log_path',
                      'simulation_log_sha256','counter_end','actual_end_h','trip_time_h','trip_code',
                      'observed_onset_h'):
                record[k] = None
            record.pop('quarantined_output_path',None)
            record.pop('quarantined_output_sha256',None)
            record.update(status='not_run', message='Campaign stopped after technical failure',
                          started_at_utc=None,finished_at_utc=None,runtime_seconds=0,
                          simulation_seconds=0,activation_observed=False,idv_trace_valid=False,
                          data_rows=0,useful_windows_complete=0)
            record['pre_fault_window'],record['post_fault_windows']=windows(row,None)
            validate_manifest(record)
            write_json(p, record)
            records.append(record)
    fields = sorted(set().union(*(r.keys() for r in records)))
    with (dest/'generation_manifest.csv').open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n')
        w.writeheader()
        for record in records:
            w.writerow({k:json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else v for k,v in record.items()})
    return records


def audit_campaign(plan, dest):
    rows = validate_plan(plan)
    dest=Path(dest).resolve()
    records=[]
    for row in rows:
        r=json.loads((dest/(row['run_id']+'.manifest.json')).read_text())
        validate_manifest(r,verify_files=True)
        for key in ('run_id','stream_id','seed_descriptor','idv','onset_h','horizon_h','stop_time_h'):
            if str(r[key]) != str(row[key]) and key not in ('onset_h','horizon_h','stop_time_h'):
                raise ValueError('plan/manifest mismatch: '+key)
            if key in ('onset_h','horizon_h','stop_time_h') and float(r[key]) != float(row[key]):
                raise ValueError('timing mismatch')
        if r['plan_sha256'] != digest(plan):
            raise ValueError('plan hash mismatch')
        if r['status'] in ('complete','physical_trip'):
            data=inspect_raw(r['output_path'])
            diag,trips_idv,trips=parse_simulation_log(Path(r['simulation_log_path']).read_text())
            check_idv(diag,trips_idv,r['onset_h'],r['idv'],data[-1][0])
            if len(data)!=r['data_rows'] or len(diag)!=len(data):
                raise ValueError('record/data counts mismatch')
        records.append(r)
    manifests=list(dest.glob('*.manifest.json'))
    if len(manifests)!=len(rows):
        raise ValueError('extra or missing manifests')
    event=parse_event_log(dest/'events.jsonl')
    starts=[e['run_id'] for e in event if e['event']=='run_start']
    if starts != [r['run_id'] for r in records if r['status']!='not_run']:
        raise ValueError('events/attempts mismatch')
    with (dest/'generation_manifest.csv').open() as f:
        aggregate=list(csv.DictReader(f))
    if [x['run_id'] for x in aggregate]!=[r['run_id'] for r in records]:
        raise ValueError('aggregate manifest IDs differ')
    for a,r in zip(aggregate,records):
        for k,v in r.items():
            expected=json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else ('' if v is None else str(v))
            if a[k]!=expected:
                raise ValueError('aggregate manifest differs: '+k)
    counts={s:sum(r['status']==s for r in records) for s in ('complete','physical_trip','technical_failure','not_run')}
    return {'manifest_count':len(records),'expected_count':len(rows),'counts':counts,
            'useful_windows_complete':sum(r['useful_windows_complete'] for r in records),
            'hashes_verified':True,'accepted':counts['technical_failure']==counts['not_run']==0,
            'generation_manifest_sha256':digest(dest/'generation_manifest.csv'),
            'events_sha256':digest(dest/'events.jsonl')}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('action',choices=['preflight','finalize','finish','audit'])
    ap.add_argument('path',type=Path)
    ap.add_argument('destination',nargs='?',type=Path)
    a=ap.parse_args()
    if a.action=='preflight':
        print(f'{len(preflight(a.path,a.destination))} approved rows')
    elif a.action=='finalize':
        finalize(a.path)
    elif a.action=='finish':
        finish_campaign(a.path,a.destination)
    else:
        result=audit_campaign(a.path,a.destination)
        print(json.dumps(result,indent=2))
        if not result['accepted']:
            raise SystemExit(1)

if __name__=='__main__':
    main()
