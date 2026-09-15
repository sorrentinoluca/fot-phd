"""Contract evaluation for the single 40x3 stability gate (rev.10)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

from .common import HarnessError, sha256_text


CONDITIONS = ("A", "B-LF", "E-LF")


def is_transport_invalidity(record):
    """An absent response is invalid, never an identity-verified model response.

    The ledger authenticates the event; this evaluator checks its shape and still checks
    frozen prompt metadata/repetitions below. Arbitrary missing identities remain errors.
    """
    return (record.get('record_kind') == 'transport_invalidity'
            and record.get('response_received') is False
            and record.get('parse_valid_first_attempt') is False
            and all(k in record and record[k] is None for k in (
                'identity_valid','returned_model','system_fingerprint','response_id',
                'raw_output','raw_output_sha256','received_utc','parsed_output','finish_reason',
                'prompt_tokens','completion_tokens','total_tokens'))
            and isinstance(record.get('transport_error'), dict)
            and bool(record['transport_error'].get('error_type'))
            and isinstance(record.get('request_identity_sha256'), str)
            and len(record['request_identity_sha256']) == 64
            and all(c in '0123456789abcdef' for c in record['request_identity_sha256']))


def semantic_signature(record: dict[str, Any]) -> tuple[Any, ...]:
    """Validity plus parsed decision pair; raw/JSON/finish differences are forensic."""
    valid = record.get("parse_valid_first_attempt") is True
    if not valid:
        return (False, "INVALID")
    parsed = record.get("parsed_output")
    if not isinstance(parsed, dict):
        raise HarnessError("valid gate record lacks parsed_output")
    abstain = parsed.get("abstain")
    predicted = parsed.get("predicted_label")
    if type(abstain) is not bool or (abstain and predicted is not None) or (
        not abstain and not isinstance(predicted, str)
    ):
        raise HarnessError("valid gate record has an invalid abstain/predicted_label pair")
    return (True, abstain, predicted)


def evaluate_stability_gate(records: Iterable[dict[str, Any]], *, expected_prompts=None) -> dict[str, Any]:
    rows = list(records)
    if len(rows) != 120:
        raise HarnessError("the stability gate requires exactly 120 first attempts")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        prompt_id = row.get("prompt_id")
        if not isinstance(prompt_id, str) or row.get("condition") not in CONDITIONS:
            raise HarnessError("gate record lacks a valid prompt or condition")
        grouped[prompt_id].append(row)
    if len(grouped) != 40 or any(len(group) != 3 for group in grouped.values()):
        raise HarnessError("the stability gate requires forty complete triplets")

    if expected_prompts is None:
        raise HarnessError('gate requires the authenticated frozen prompt sample')
    expected = {p['prompt_id']: p for p in expected_prompts}
    if len(expected_prompts) != 40 or len(expected) != 40 or set(expected) != set(grouped):
        raise HarnessError('gate differs from the forty frozen prompts')
    if {c: sum(p['condition']==c for p in expected.values()) for c in CONDITIONS} != {'A':8,'B-LF':16,'E-LF':16}:
        raise HarnessError('frozen gate condition distribution must be 8/16/16')
    if len({p.get('prompt_sha256') for p in expected.values()}) != 40:
        raise HarnessError('frozen sample must contain forty distinct prompt hashes')
    agents = {p.get('agent_id') for p in expected.values()}
    if agents != {f'agent_{i}' for i in range(1,9)}:
        raise HarnessError('frozen gate must cover all eight agents')
    for agent in agents:
        group = [p for p in expected.values() if p['agent_id']==agent]
        transfer = [p for p in group if p.get('sample_role')=='matched_transfer']
        stress = [p for p in group if p.get('sample_role')=='context_stress']
        if len(transfer)!=3 or {p['condition'] for p in transfer}!=set(CONDITIONS) or len({p['case_id'] for p in transfer})!=1 or len(stress)!=2 or {p['condition'] for p in stress}!={'B-LF','E-LF'} or len({p['case_id'] for p in stress})!=1 or transfer[0]['case_id']==stress[0]['case_id']:
            raise HarnessError('frozen matched-transfer/context-stress distribution differs')
    if len({r.get('request_id') for r in rows}) != 120 or any(not r.get('request_id') for r in rows):
        raise HarnessError('gate request identities must be unique')
    for prompt_id, group in grouped.items():
        p = expected[prompt_id]
        if 'text' not in p or p.get('prompt_sha256') != sha256_text(p['text']):
            raise HarnessError('frozen prompt text hash mismatch')
        if {r.get('repetition') for r in group} != {1,2,3} or any(type(r.get('repetition')) is not int for r in group):
            raise HarnessError('gate triplet requires exact repetitions 1, 2, 3')
        for r in group:
            if any(r.get(k) != p.get(k) or p.get(k) is None for k in ('prompt_sha256','condition','agent_id','case_id','sample_role')):
                raise HarnessError('gate triplet prompt identity/condition differs from frozen sample')
            if r.get('record_kind') == 'transport_invalidity' and not is_transport_invalidity(r):
                raise HarnessError('malformed transport invalidity')
            if r.get('retry_count', 0) != 0 or (r.get('identity_valid') is not True and not is_transport_invalidity(r)):
                raise HarnessError('gate requires first attempts with verified response identity or explicit transport invalidity')

    valid = sum(row.get("parse_valid_first_attempt") is True for row in rows)
    truncations = sum(
        row.get("finish_reason") == "length" or row.get("truncated") is True for row in rows
    )
    abstention_coverage = {
        condition: any(
            row["condition"] == condition
            and semantic_signature(row) == (True, True, None)
            for row in rows
        )
        for condition in CONDITIONS
    }
    all_invalid = sorted(
        prompt_id
        for prompt_id, group in grouped.items()
        if all(signature[0] is False for signature in map(semantic_signature, group))
    )
    divergent = sorted(
        prompt_id
        for prompt_id, group in grouped.items()
        if prompt_id not in all_invalid
        and len({semantic_signature(row) for row in group}) > 1
    )
    t3 = valid >= 114 and all(abstention_coverage.values())
    t4 = truncations == 0
    t6_evaluable = not all_invalid
    if not t3 or not t4 or not t6_evaluable:
        status = "NO_GO_TECHNICAL"
    elif divergent:
        status = "R3_REQUIRED_PENDING_FEASIBILITY"
    else:
        status = "PASS_R1_PENDING_T5_AND_OTHER_PREREQUISITES"
    return {
        "status": status,
        "go_final": False,
        "provider_requests": 120,
        "valid_first_attempts": valid,
        "invalid_first_attempts": 120 - valid,
        "t3_pass": t3,
        "abstention_coverage": abstention_coverage,
        "length_truncations": truncations,
        "t4_pass": t4,
        "t6_evaluable": t6_evaluable,
        "all_invalid_prompt_ids": all_invalid,
        "divergent_prompt_ids": divergent,
        "divergent_prompt_count": len(divergent),
        "t5_temporal_feasibility": "NOT_MEASURED_BY_OFFLINE_EVALUATION",
    }
