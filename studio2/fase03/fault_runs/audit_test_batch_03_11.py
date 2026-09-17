#!/usr/bin/env python3
"""Read-only audit of the 89-run F5 test lot."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from fault_protocol import audit_campaign, digest, write_json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CATALOG = (1, 2, 3, 8, 10, 13, 14, 15)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    plan = HERE / 'plans/test_batch_f5.csv'
    campaign = HERE / 'test_batch/test_batch_f5_001'
    generic = audit_campaign(plan, campaign)
    records = [json.loads((campaign/f'{row["run_id"]}.manifest.json').read_text())
               for row in __import__('build_generation_plan').validate_plan(plan)]
    primary_fault = [r for r in records if r['run_id'].startswith('test-primary-F')]
    primary_normal = [r for r in records if r['run_id'].startswith('test-primary-Normal')]
    ood = [r for r in records if r['run_id'].startswith('test-ood-')]
    spares = [r for r in records if r['run_id'].startswith('test-spare-')]
    expected = (
        len(records) == 89 and len(primary_fault) == 64 and len(primary_normal) == 8
        and len(ood) == 6 and len(spares) == 11
        and Counter(r['idv'] for r in primary_fault) == Counter({x: 8 for x in CATALOG})
        and Counter(r['idv'] for r in ood) == Counter({5: 3, 4: 3})
        and all(r['status'] == 'complete' for r in records)
        and all(r['actual_end_h'] == 65.0 and r['useful_windows_complete'] == 8 for r in records)
        and all(r['git_commit'] == 'f650f0306a9e7aa3220de6a3b4d14fc0377f8770' for r in records)
        and not (HERE/'ood_chain_f12').exists()
    )
    result = {
        'schema_version': 1,
        'status': 'PASS' if expected and generic['accepted'] else 'FAIL',
        'batch_path': str(campaign.relative_to(ROOT)),
        'active_ood_substitution': 'F6 -> F5',
        'F12_executed': False,
        'counts': {
            'total_generated': len(records),
            'primary_fault': len(primary_fault),
            'primary_normal': len(primary_normal),
            'ood': len(ood),
            'technical_spares': len(spares),
            'complete': sum(r['status'] == 'complete' for r in records),
            'physical_trip': sum(r['status'] == 'physical_trip' for r in records),
            'technical_failure': sum(r['status'] == 'technical_failure' for r in records),
            'not_run': sum(r['status'] == 'not_run' for r in records),
            'spares_activated_as_replacements': 0,
            'complete_windows': sum(r['useful_windows_complete'] for r in records),
        },
        'generic_campaign_audit': generic,
        'plan': {'path': str(plan.relative_to(ROOT)), 'sha256': digest(plan)},
        'generation_manifest': {
            'path': str((campaign/'generation_manifest.csv').relative_to(ROOT)),
            'sha256': digest(campaign/'generation_manifest.csv'),
        },
        'events': {
            'path': str((campaign/'events.jsonl').relative_to(ROOT)),
            'sha256': digest(campaign/'events.jsonl'),
        },
        'matlab_log': {
            'path': 'studio2/fase03/fault_runs/runtime/test_batch_f5.matlab.log',
            'sha256': digest(HERE/'runtime/test_batch_f5.matlab.log'),
        },
        'matlab_versions': sorted({r['matlab_version'] for r in records}),
        'mex_hashes': sorted({r['mex_sha256'] for r in records}),
        'run_commit': sorted({r['git_commit'] for r in records}),
        'runtime_seconds_sum': sum(r['runtime_seconds'] for r in records),
        'qwen_calls': 0,
        'scientific_model_calls': 0,
        'selection_on_diagnostic_performance': False,
    }
    write_json(args.output, result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
