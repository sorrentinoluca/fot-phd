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
    if kind not in ('fault_dev', 'smoke', 'ood_preflight'):
        raise ValueError('unknown plan kind')
    catalog = json.loads((HERE.parent / 'selection/CATALOG_FREEZE.json').read_text())
    if tuple(catalog['catalog']) != CATALOG:
        raise ValueError('catalog differs from approved frozen catalog')
    rows = []
    if kind == 'fault_dev':
        pairs = [(k, b) for k in range(8) for b in range(1, 6)]
    elif kind == 'smoke':
        pairs = [(0, 0)]
    else:
        pairs = [(6, 0), (4, 0)]
    occupied = occupied_indices()
    for k, b in pairs:
        if kind == 'fault_dev':
            idx, idv, run_id = 30000 + 5*k + b - 1, CATALOG[k], f'fault-dev-F{CATALOG[k]}-b{b:02d}'
        elif kind == 'smoke':
            idx, idv, run_id = 30040, 1, 'smoke-F1-001'
        else:
            idx, idv, run_id = 70000 + len(rows), k, f'preflight-F{k}-001'
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
    ap.add_argument('kind', choices=['fault_dev', 'smoke', 'ood_preflight'])
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
