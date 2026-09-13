#!/usr/bin/env python3
"""Deterministic plans for the approved 8 x 5 development campaign and one smoke."""
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
        for row in csv.DictReader(p.open()):
            if row.get('stream_id'):
                occupied.add(int(row['stream_id']))
    return occupied


def build_rows(kind):
    if kind not in ('fault_dev', 'smoke'):
        raise ValueError('unknown plan kind')
    catalog = json.loads((HERE.parent / 'selection/CATALOG_FREEZE.json').read_text())
    if tuple(catalog['catalog']) != CATALOG:
        raise ValueError('catalog differs from approved frozen catalog')
    rows = []
    pairs = [(k, b) for k in range(8) for b in range(1, 6)] if kind == 'fault_dev' else [(0, 0)]
    occupied = occupied_indices()
    for k, b in pairs:
        idx = 30000 + 5*k + b - 1 if kind == 'fault_dev' else 30040
        if idx in occupied:
            raise ValueError(f'occupied stream: {idx}')
        horizon = 40 if kind == 'fault_dev' else 0.1
        rows.append(dict(zip(FIELDS, (
            f'fault-dev-F{CATALOG[k]}-b{b:02d}' if kind == 'fault_dev' else 'smoke-F1-001',
            kind, b, str(idx), str(idx), f'{KEY}:{idx:016x}', idx & 0xffffffff, idx >> 32,
            CATALOG[k], 20, 25, horizon, 25+horizon, 5, 8 if kind == 'fault_dev' else 0))))
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
    ap.add_argument('kind', choices=['fault_dev', 'smoke'])
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
