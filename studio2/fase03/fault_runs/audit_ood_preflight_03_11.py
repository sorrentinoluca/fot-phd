#!/usr/bin/env python3
"""Audit the sealed OOD probes and enforce the frozen substitution chain."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from fault_protocol import audit_campaign, digest, write_json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def admissible(record: dict) -> bool:
    return (
        record['status'] == 'complete'
        and record['trip_time_h'] is None
        and record['actual_end_h'] == 65.0
        and record['activation_observed'] is True
        and record['idv_trace_valid'] is True
        and record['useful_windows_complete'] == 8
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    plan = HERE / 'plans/ood_preflight_03_11.csv'
    campaign = HERE / 'ood_preflight/ood_preflight_001'
    generic = audit_campaign(plan, campaign)
    records = {
        int(record['idv']): record
        for record in (
            json.loads(path.read_text())
            for path in campaign.glob('*.manifest.json')
        )
    }
    if set(records) != {4, 6}:
        raise ValueError('expected exactly F6 and F4 manifests')
    f6_ok, f4_ok = admissible(records[6]), admissible(records[4])
    required_substitute = None if f6_ok else 'F5'
    substitute_evidence = ROOT / 'studio2/fase03/fault_runs/SUBSTITUTE_DETECTABILITY_F5.json'
    substitute_ready = required_substitute is None or substitute_evidence.is_file()
    batch_authorized = f6_ok and f4_ok
    if required_substitute and substitute_ready:
        batch_authorized = False  # F5 still needs its own technical probe in a new sealed step.
    status = 'PASS' if batch_authorized else 'BLOCKED_UNRESOLVED_SUBSTITUTE'
    source_paths = [
        ROOT / 'studio2/fase03/piano_statistico/PIANO_STATISTICO.md',
        ROOT / 'studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_bozza.md',
        ROOT / 'docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md',
        HERE / 'SPECIFICA_PREFLIGHT_OOD_03_11.md',
        plan,
    ]
    result = {
        'schema_version': 1,
        'status': status,
        'batch_89_authorized': batch_authorized,
        'generic_campaign_audit': generic,
        'probes': {
            'F6': {
                'admissible': f6_ok,
                'status': records[6]['status'],
                'actual_end_h': records[6]['actual_end_h'],
                'trip_time_h': records[6]['trip_time_h'],
                'trip_code': records[6]['trip_code'],
                'complete_windows': records[6]['useful_windows_complete'],
                'manifest_sha256': digest(campaign/'preflight-F6-001.manifest.json'),
                'raw_sha256': records[6]['sha256'],
            },
            'F4': {
                'admissible': f4_ok,
                'status': records[4]['status'],
                'actual_end_h': records[4]['actual_end_h'],
                'trip_time_h': records[4]['trip_time_h'],
                'trip_code': records[4]['trip_code'],
                'complete_windows': records[4]['useful_windows_complete'],
                'manifest_sha256': digest(campaign/'preflight-F4-001.manifest.json'),
                'raw_sha256': records[4]['sha256'],
            },
        },
        'frozen_chain': {'F6': ['F5', 'F12'], 'F4': ['F11', 'F5']},
        'required_next_candidate': required_substitute,
        'required_candidate_detectability_record_present': substitute_ready,
        'blocking_reason': (
            None if batch_authorized else
            'F6 tripped before 65 h; F5 is next, but the normative package records no verified '
            'detectability number for F5 and no approved F5 evidence exists in this worktree.'
        ),
        'source_hashes': {str(path.relative_to(ROOT)): digest(path) for path in source_paths},
        'preserved_local_evidence': {
            'campaign_path': str(campaign.relative_to(ROOT)),
            'events_sha256': digest(campaign/'events.jsonl'),
            'generation_manifest_sha256': digest(campaign/'generation_manifest.csv'),
            'matlab_log_path': 'studio2/fase03/fault_runs/runtime/ood_preflight_03_11/matlab.log',
            'matlab_log_sha256': digest(HERE/'runtime/ood_preflight_03_11/matlab.log'),
        },
        'scientific_model_calls': 0,
        'qwen_calls': 0,
        'test_batch_runs_started': 0,
    }
    write_json(args.output, result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if batch_authorized else 3


if __name__ == '__main__':
    raise SystemExit(main())
