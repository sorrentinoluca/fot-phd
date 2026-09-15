#!/usr/bin/env python3
"""Deterministic plans for qualified fault campaigns and technical OOD preflight."""
import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CATALOG = (1, 2, 3, 8, 10, 13, 14, 15)
KEY = '0x464f545445503032'
FIELDS = ('run_id', 'set_name', 'batch', 'run_index_uint64', 'stream_id', 'seed_descriptor',
          'stream_lo32', 'stream_hi32', 'idv', 'burn_in_h', 'onset_h', 'horizon_h',
          'stop_time_h', 'window_h', 'useful_windows_expected')


def occupied_indices():
    source = ROOT / 'studio2/fase02/build_generation_plan.py'
    spec = importlib.util.spec_from_file_location('phase02_plan', source)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    occupied = set().union(*map(set, mod.STREAM_RANGES.values())) | {999999}
    for p in (ROOT / 'studio2/fase02').rglob('generation_manifest.csv'):
        with p.open(newline='') as handle:
            for row in csv.DictReader(handle):
                if row.get('stream_id'):
                    occupied.add(int(row['stream_id']))
    return occupied


def build_rows(kind):
    allowed = ('fault_dev', 'smoke', 'ood_preflight', 'ood_chain_f5', 'ood_chain_f12',
               'test_batch_f5', 'test_batch_f12')
    if kind not in allowed:
        raise ValueError('unknown plan kind')
    catalog = json.loads((HERE.parent / 'selection/CATALOG_FREEZE.json').read_text())
    if tuple(catalog['catalog']) != CATALOG:
        raise ValueError('catalog differs from approved frozen catalog')
    rows = []
    occupied = occupied_indices()
    specs = []
    if kind == 'fault_dev':
        specs = [(f'fault-dev-F{CATALOG[k]}-b{b:02d}', CATALOG[k], b, 30000+5*k+b-1)
                 for k in range(8) for b in range(1, 6)]
    elif kind == 'smoke':
        specs = [('smoke-F1-001', 1, 0, 30040)]
    elif kind == 'ood_preflight':
        specs = [('preflight-F6-001', 6, 0, 70000), ('preflight-F4-001', 4, 0, 70001)]
    elif kind in ('ood_chain_f5', 'ood_chain_f12'):
        idv = 5 if kind.endswith('f5') else 12
        specs = [(f'chain-F{idv}-001', idv, 0, 70002 if idv == 5 else 70003)]
    else:
        ood = 5 if kind.endswith('f5') else 12
        base = 71000 if ood == 5 else 72000
        for idv in CATALOG:
            for repetition in range(1, 9):
                specs.append((f'test-primary-F{idv}-r{repetition:02d}', idv, repetition,
                              base + len(specs)))
        for repetition in range(1, 9):
            specs.append((f'test-primary-Normal-r{repetition:02d}', 0, repetition,
                          base + len(specs)))
        for idv in (ood, 4):
            for repetition in range(1, 4):
                specs.append((f'test-ood-F{idv}-r{repetition:02d}', idv, repetition,
                              base + len(specs)))
        for label, idv in [(f'F{x}', x) for x in CATALOG] + [('Normal', 0), (f'F{ood}', ood), ('F4', 4)]:
            specs.append((f'test-spare-{label}-r01', idv, 0, base + len(specs)))
    for run_id, idv, b, idx in specs:
        if idx in occupied:
            raise ValueError(f'occupied stream: {idx}')
        horizon = 0.1 if kind == 'smoke' else 40
        rows.append(dict(zip(FIELDS, (
            run_id,
            kind, b, str(idx), str(idx), f'{KEY}:{idx:016x}', idx & 0xffffffff, idx >> 32,
            idv, 20, 25, horizon, 25+horizon, 5, 0 if kind == 'smoke' else 8))))
    return rows


def validate_plan(path):
    with Path(path).open(newline='') as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError('plan columns differ from specification')
        actual = list(reader)
    if not actual:
        raise ValueError('empty plan')
    expected = [{k: str(v) for k, v in r.items()} for r in build_rows(actual[0]['set_name'])]
    if actual != expected:
        raise ValueError('plan differs from deterministic approved rows/order')
    return actual


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('kind', choices=[
        'fault_dev', 'smoke', 'ood_preflight', 'ood_chain_f5', 'ood_chain_f12',
        'test_batch_f5', 'test_batch_f12'])
    ap.add_argument('output', type=Path)
    a = ap.parse_args()
    output = a.output.resolve()
    if output.parent != HERE / 'plans':
        ap.error('plans must be written directly under fault_runs/plans/')
    rows = build_rows(a.kind)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    validate_plan(output)
    print(f'{len(rows)} rows; sha256={hashlib.sha256(output.read_bytes()).hexdigest()}')

if __name__ == '__main__':
    main()
