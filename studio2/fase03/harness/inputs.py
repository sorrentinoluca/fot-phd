#!/usr/bin/env python3
"""Build the autonomous real-input inventory and, only when complete, pilot manifest."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path
import re
from typing import Any

from .common import HarnessError, canonical_json, load_json, require_sha256, sha256_file, sha256_text
from .ordering import PRESENTATION_NAMESPACE, presentation_order, spearman_against_catalog


EVIDENCE_COMMIT = "c66bd8dddf8e2af9dd0665ee30afd36c248b93fb"
EVIDENCE_INTEGRATION_COMMIT = "7c99a8318cbe24bf864790566302f72614d963ed"
EVIDENCE_RELEASE = "studio2-fase03-evidence-v2"
EVIDENCE_ARCHIVE_SHA256 = "6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf"
EVIDENCE_MANIFEST_SHA256 = "5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020"
EVALUATOR_INDEX_SHA256 = "b966cdd3d579efaf595fd48c4b9baa70747ba584522926520840a1e914dbf69c"
NORMAL_HANDOFF_SHA256 = "e2409c64ad4e36e0f3b597a5e0b9745d866af72f4da717fc7a128b25753c166a"
NORMAL_SOURCE_COMMIT = "6372cb3c457a30b39c838e066b613c61313c35db"
SCHEMA_TARGET_COMMIT = "3c64390bc4dd58c48cc4e1e388a38989b32b3143"
SCHEMA_MANIFEST_SHA256 = "d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12"
SCHEMA_TAG = "studio2-fase03-schema-insight-frozen-001"
SCHEMA_TAG_OBJECT = "4d15c4fb915ea9db9f7425225d231746778f0ba1"
CANONICAL_INPUT_ROOT = Path(__file__).resolve().parents[1]
SELECTION_NAMESPACE = "studio2-fase03-pilot-selection-v1"
PSEUDOLABEL_SHA256 = "b0ce81d53f11038ddf51c9ec964a1e838a7045e2e57b8ac3368f05e9a215bbc6"
ASSIGNMENT_SHA256 = "df7434230dcd1d5460cd19e0d27e909efd40289f64d89a4b3fee2a0e55b79fcf"
DERANGEMENT_SHA256 = "34350c7e49b11d29b885da128d4b34ce3df31cd41df7c521cb66421aa1b9d001"
PENDING_INVENTORY_SHA256 = "7103482d6c7b8038944b0af63bac58548557c8d0b8f5d24e420346bd93fa304b"
CATALOG = ("F1", "F2", "F3", "F8", "F10", "F13", "F14", "F15")
AGENTS = tuple(f"agent_{index}" for index in range(1, 9))
VARIABLE = re.compile(r"^X(MEAS|MV)-(\d+)$")


def _read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))
    except (OSError, UnicodeError, csv.Error) as exc:
        raise HarnessError(f"cannot read CSV {path}: {exc}") from exc


def _load_evidence(root: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, str]]]:
    evidence_manifest = root / "EVIDENCE_MANIFEST.csv"
    evaluator_index = root / "EVALUATOR_INDEX.csv"
    require_sha256(evidence_manifest, EVIDENCE_MANIFEST_SHA256, role="03.6 evidence manifest")
    require_sha256(evaluator_index, EVALUATOR_INDEX_SHA256, role="03.6 evaluator index")
    manifest_rows = _read_csv(evidence_manifest)
    index_rows = _read_csv(evaluator_index)
    if len(manifest_rows) != 320 or len(index_rows) != 320:
        raise HarnessError("03.6 release must contain exactly 320 evidence units")
    manifest_by_id = {row["evidence_id"]: row for row in manifest_rows}
    index_by_id = {row["evidence_id"]: row for row in index_rows}
    if len(manifest_by_id) != 320 or set(manifest_by_id) != set(index_by_id):
        raise HarnessError("evidence and evaluator manifests disagree on evidence IDs")
    cases: list[dict[str, Any]] = []
    for evidence_id in sorted(manifest_by_id):
        public = manifest_by_id[evidence_id]
        private = index_by_id[evidence_id]
        if private["fault"] not in CATALOG or private["window_ordinal"] != public["window_ordinal"]:
            raise HarnessError(f"invalid evaluator metadata for {evidence_id}")
        require_sha256(root / public["json_path"], public["json_sha256"], role=f"evidence JSON {evidence_id}")
        text_path = root / public["text_path"]
        require_sha256(text_path, public["text_sha256"], role=f"neutral text {evidence_id}")
        neutral = text_path.read_text(encoding="utf-8").strip()
        if not neutral:
            raise HarnessError(f"empty neutral text: {evidence_id}")
        cases.append(
            {
                "case_id": evidence_id,
                "fault": private["fault"],
                "batch": int(private["batch"]),
                "window_ordinal": int(private["window_ordinal"]),
                "neutral_text": neutral,
                "neutral_text_sha256": sha256_text(neutral),
                "release_text_sha256": public["text_sha256"],
                "release_text_path": public["text_path"],
                "evidence_json_path": public["json_path"],
                "evidence_json_sha256": public["json_sha256"],
            }
        )
    return cases, manifest_by_id


def _fault_assignment(owners: dict[str, str]) -> dict[str, str]:
    """Select one no-fixed-point agent→fault bijection by a single digest minimum."""
    candidates: list[tuple[str, dict[str, str]]] = []
    for permutation in itertools.permutations(CATALOG):
        mapping = dict(zip(AGENTS, permutation))
        if any(owners[agent] == fault for agent, fault in mapping.items()):
            continue
        key = sha256_text(f"{SELECTION_NAMESPACE}|assignment|{canonical_json(mapping)}")
        candidates.append((key, mapping))
    if not candidates:
        raise HarnessError("no locally-unseen transfer assignment exists")
    return min(candidates, key=lambda item: item[0])[1]


def _select_transfer_cases(
    cases: list[dict[str, Any]], assignment: dict[str, str]
) -> dict[str, str]:
    selected: dict[str, str] = {}
    for agent in AGENTS:
        eligible = [row for row in cases if row["fault"] == assignment[agent]]
        if not eligible:
            raise HarnessError(f"no evidence for assigned transfer fault of {agent}")
        selected[agent] = min(
            eligible,
            key=lambda row: sha256_text(
                f"{SELECTION_NAMESPACE}|transfer|{agent}|{row['case_id']}"
            ),
        )["case_id"]
    return selected


def _normal_examples(path: Path | None) -> tuple[dict[str, dict[str, str]], list[str]]:
    if path is None:
        return {}, ["normal_dev examples frozen by 03.9"]
    require_sha256(path, NORMAL_HANDOFF_SHA256, role="03.9 Normal example handoff")
    value = load_json(path)
    required = {"status", "source_commit", "selection_rule", "selection_rule_frozen", "examples"}
    if not isinstance(value, dict) or set(value) != required:
        raise HarnessError("normal_dev handoff has unexpected fields")
    if value["status"] != "FROZEN_NORMAL_DEV_EXAMPLES" or value["selection_rule_frozen"] is not True:
        raise HarnessError("normal_dev selection rule is not frozen")
    if value["source_commit"] != NORMAL_SOURCE_COMMIT:
        raise HarnessError("normal_dev handoff source commit differs from the verified 03.9 input")
    examples = value["examples"]
    if not isinstance(examples, dict) or tuple(sorted(examples)) != AGENTS:
        raise HarnessError("normal_dev handoff must contain one example per agent")
    result: dict[str, dict[str, str]] = {}
    for agent in AGENTS:
        row = examples[agent]
        required_row = {"example_id", "neutral_text", "neutral_text_sha256", "source_sha256"}
        if not isinstance(row, dict) or set(row) != required_row:
            raise HarnessError(f"invalid normal_dev example for {agent}")
        if sha256_text(row["neutral_text"].strip()) != row["neutral_text_sha256"]:
            raise HarnessError(f"normal_dev neutral-text hash mismatch for {agent}")
        result[agent] = row
    return result, []


def verified_pending_inventory():
    path = Path(__file__).with_name('PILOT_INPUT_SOURCES.pending.json')
    require_sha256(path, PENDING_INVENTORY_SHA256, role='authenticated producer source inventory')
    return load_json(path)


def verify_conformance_inventory(inventory):
    for relative, pin in [('pseudolabel/PSEUDOLABEL_MAP.json', PSEUDOLABEL_SHA256),
                          ('pseudolabel/AGENT_ASSIGNMENT.json', ASSIGNMENT_SHA256),
                          ('pseudolabel/CONDITION_E_DERANGEMENTS.json', DERANGEMENT_SHA256),
                          ('baseline_numerica/NORMAL_DEV_HANDOFF.json', NORMAL_HANDOFF_SHA256)]:
        require_sha256(CANONICAL_INPUT_ROOT/relative, pin, role='canonical development source')
    expected = verified_pending_inventory()
    if inventory != expected:
        raise HarnessError('producer inventory differs from authenticated development sources/contracts')
    return expected


def _insights(path, *, ledger=None, token_count=None, schema_dir=None, library_role="primary"):
    if path is None:
        return [], ['16 real schema-valid producer insights'], None
    if ledger is None or token_count is None or schema_dir is None:
        raise HarnessError('insight handoff requires durable producer ledger and R4 validation')
    from .insight_adapter import validate_library
    from .ledger import digest
    value = load_json(path)
    if library_role not in {'primary', 'alternate'}:
        raise HarnessError('unknown producer library role')
    stage = ('alternate_conformity' if library_role == 'alternate' else
             ('producer_remediation' if ledger.event('remediation_authorized') else 'producer_conformity'))
    outcome = ledger.event('outcome:' + stage)
    ledger.verify_stage_success(stage)
    binding = ledger.binding(stage)
    records = ledger.stage_records(stage)
    if not outcome or outcome['outcome'] != 'PASS' or ledger.unreconciled_suspensions():
        raise HarnessError('handoff requires successful active producer cycle')
    library = []
    for row in records:
        raw = ledger.response(row['request_id'])['raw']
        try:
            library.extend(json.loads(raw['choices'][0]['message']['content'])['insights'])
        except (KeyError, TypeError, IndexError, ValueError) as exc:
            raise HarnessError('handoff raw response cannot reproduce library') from exc
    library.sort(key=lambda x: x['insight_id'])
    expected = dict(schema_commit=SCHEMA_TARGET_COMMIT, schema_manifest_sha256=SCHEMA_MANIFEST_SHA256,
                    library=library, library_sha256=digest(library), validated=True,
                    pilot_id=ledger.pilot_id, stage=stage, binding_sha256=digest(binding),
                    records_sha256=digest(records))
    if value != expected or binding.get('inventory_sha256') != digest(verified_pending_inventory()):
        raise HarnessError('insight handoff provenance does not match active producer records')
    validate_library(library, inventory=verified_pending_inventory(), token_count=token_count, schema_dir=schema_dir)
    return library, [], {k: v for k, v in expected.items() if k != 'library'}


def _dominant_variable_ids(evidence_json: Path) -> list[str]:
    value = load_json(evidence_json)
    variables, thresholds = value.get("variables"), value.get("thresholds")
    if not isinstance(variables, dict) or not isinstance(thresholds, dict):
        raise HarnessError(f"variables or thresholds missing in {evidence_json}")
    scored: list[tuple[float, int, str]] = []
    for raw, metrics in variables.items():
        match = VARIABLE.fullmatch(raw)
        if not match or match.group(1) != "MEAS" or not isinstance(metrics, dict):
            continue
        per_window = metrics.get("per_window")
        if not isinstance(per_window, list) or not per_window:
            continue
        scores: list[float] = []
        for row in per_window:
            scores.extend(
                (
                    abs(float(row["shift_sigma"])) / float(thresholds["abs_shift_sigma"]),
                    abs(float(row["slope_sigma_h"])) / float(thresholds["abs_slope_sigma_h"]),
                    float(row["residual_std_ratio"]) / float(thresholds["residual_std_ratio"]),
                    float(row["diff_std_ratio"]) / float(thresholds["diff_std_ratio"]),
                )
            )
        index = int(match.group(2))
        scored.append((max(scores), index, f"XMEAS({index})"))
    if len(scored) != 41:
        raise HarnessError(f"expected 41 scored XMEAS variables in {evidence_json}")
    return [identifier for _, _, identifier in sorted(scored, key=lambda row: (-row[0], row[1]))[:8]]


def build_inventory(
    *,
    evidence_root: Path,
    pseudolabel_path: Path,
    assignment_path: Path,
    derangement_path: Path,
    assembly_base_commit: str,
    normal_handoff: Path | None = None,
    insight_handoff: Path | None = None,
    ledger=None, token_count=None, schema_dir=None, presentation_approval=None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    if not re.fullmatch(r"[0-9a-f]{40}", assembly_base_commit):
        raise HarnessError("assembly_base_commit must be a full Git object ID")
    for path, pin in ((pseudolabel_path, PSEUDOLABEL_SHA256), (assignment_path, ASSIGNMENT_SHA256), (derangement_path, DERANGEMENT_SHA256)):
        require_sha256(path, pin, role='frozen 03.7 input')
    cases, public_by_id = _load_evidence(evidence_root)
    labels = load_json(pseudolabel_path)
    assignment_value = load_json(assignment_path)
    derangements = load_json(derangement_path)
    label_by_fault = labels["label_by_identifier"]
    if tuple(f"F{labels['idv_by_identifier'][fault]}" for fault in CATALOG) != CATALOG:
        raise HarnessError("pseudolabel catalog differs from frozen D1")
    agents = assignment_value["agents"]
    owners = {
        agent: assignment_value["assignment"][agent]["identifier"] for agent in AGENTS
    }
    transfer_faults = _fault_assignment(owners)
    transfer_cases = _select_transfer_cases(cases, transfer_faults)
    normal, missing_normal = _normal_examples(normal_handoff)
    insights, missing_insights, insight_validation = _insights(insight_handoff, ledger=ledger, token_count=token_count, schema_dir=schema_dir)
    missing = [*missing_normal, *missing_insights]

    prompt_cases = [
        {
            "case_id": row["case_id"],
            "split": "development",
            "fault_label": label_by_fault[row["fault"]],
            "neutral_text": row["neutral_text"],
            "neutral_text_sha256": row["neutral_text_sha256"],
        }
        for row in cases
    ]
    local_examples: dict[str, list[dict[str, str]]] = {}
    provenance_examples: list[dict[str, Any]] = []
    fixed_contracts: list[dict[str, Any]] = []
    counter = 0
    insight_counter = 0
    by_fault_batch_window = {
        (row["fault"], row["batch"], row["window_ordinal"]): row for row in cases
    }
    for agent in AGENTS:
        rows: list[dict[str, str]] = []
        local_fault = owners[agent]
        for batch in (1, 2):
            source = by_fault_batch_window[(local_fault, batch, 1)]
            counter += 1
            example_id = f"S2-EXM-{counter:03d}"
            rows.append(
                {
                    "example_id": example_id,
                    "pseudolabel": label_by_fault[local_fault],
                    "neutral_text": source["neutral_text"],
                }
            )
            provenance_examples.append(
                {
                    "example_id": example_id,
                    "evidence_id": source["case_id"],
                    "fault": local_fault,
                    "batch": batch,
                    "window_ordinal": 1,
                    "neutral_text_sha256": source["neutral_text_sha256"],
                }
            )
            insight_counter += 1
            fixed_contracts.append(
                {
                    "insight_id": f"S2-INS-{insight_counter:03d}",
                    "source_agent": agent,
                    "pseudolabel": label_by_fault[local_fault],
                    "evidence_scope": "one 5 h development window",
                    "variable_ids": _dominant_variable_ids(
                        evidence_root / public_by_id[source["case_id"]]["json_path"]
                    ),
                    "source_example_id": example_id,
                }
            )
        if agent in normal:
            counter += 1
            normal_row = normal[agent]
            rows.append(
                {
                    "example_id": f"S2-EXM-{counter:03d}",
                    "pseudolabel": "Normal",
                    "neutral_text": normal_row["neutral_text"].strip(),
                }
            )
        local_examples[agent] = rows

    catalog_order_labels = [label_by_fault[fault] for fault in CATALOG]
    displayed = presentation_order(labels["label_space"])
    inventory = {
        "artifact_version": "1",
        "status": "COMPLETE_READY_TO_FREEZE" if not missing else "INCOMPLETE",
        "provenance_kind": "study2_scientific_partial" if missing else "study2_scientific",
        "assembly_base_commit": assembly_base_commit,
        "missing_requirements": missing,
        "selection": {
            "namespace": SELECTION_NAMESPACE,
            "transfer_fault_by_agent_evaluator_side": transfer_faults,
            "transfer_case_by_agent": transfer_cases,
            "stress_case_rule": "maximum B-LF token count among other locally-unseen development cases; tie=max(case_id)",
        },
        "presentation": {
            "namespace": PRESENTATION_NAMESPACE,
            "ordered_labels": displayed,
            "catalog_order_labels_evaluator_side": catalog_order_labels,
            "spearman_fault_labels": spearman_against_catalog(displayed[:-1], catalog_order_labels),
            "author_decision": "pending",
        },
        "sources": {
            "evidence": {
                "commit": EVIDENCE_COMMIT,
                "integration_commit": EVIDENCE_INTEGRATION_COMMIT,
                "release": EVIDENCE_RELEASE,
                "archive_sha256": EVIDENCE_ARCHIVE_SHA256,
                "evidence_manifest_sha256": EVIDENCE_MANIFEST_SHA256,
                "evaluator_index_sha256": EVALUATOR_INDEX_SHA256,
            },
            "pseudolabel": {
                "path": "studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json",
                "sha256": sha256_file(pseudolabel_path),
            },
            "agent_assignment": {
                "path": "studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json",
                "sha256": sha256_file(assignment_path),
            },
            "derangements": {
                "path": "studio2/fase03/pseudolabel/CONDITION_E_DERANGEMENTS.json",
                "sha256": sha256_file(derangement_path),
            },
            "normal_handoff": None if normal_handoff is None else {
                "path": "studio2/fase03/baseline_numerica/NORMAL_DEV_HANDOFF.json",
                "sha256": sha256_file(normal_handoff),
                "source_commit": NORMAL_SOURCE_COMMIT,
            },
            "schema_contract": {
                "revision": 4,
                "target_commit": SCHEMA_TARGET_COMMIT,
                "manifest_sha256": SCHEMA_MANIFEST_SHA256,
                "tag": SCHEMA_TAG,
                "tag_object": SCHEMA_TAG_OBJECT,
                "tag_peeled": SCHEMA_TARGET_COMMIT,
            },
            "insight_validation": insight_validation,
        },
        "input_roles": {
            "producer_conformance_inputs": "verified development evidence, sixteen fixed contracts and eight Normal examples",
            "validated_insight_library": "absent until producer conformance succeeds under R4; never synthesized by this inventory",
            "probe_and_gate_dependency": "requires the resulting validated sixteen-insight library and cannot feed producer conformance",
        },
        "producer_conformance_inputs": {
            "local_examples": local_examples,
            "fixed_insight_contracts": fixed_contracts,
            "required_calls": 8,
            "insights_per_call": 2,
            "scientific_library_present": False,
        },
        "development_cases": [
            {
                "case_id": row["case_id"],
                "neutral_text_sha256": row["neutral_text_sha256"],
                "release_text_sha256": row["release_text_sha256"],
                "release_text_path": row["release_text_path"],
                "evidence_json_sha256": row["evidence_json_sha256"],
                "evaluator": {
                    "fault": row["fault"],
                    "batch": row["batch"],
                    "window_ordinal": row["window_ordinal"],
                },
            }
            for row in cases
        ],
        "local_example_provenance": provenance_examples,
        "fixed_insight_contracts": fixed_contracts,
    }
    if presentation_approval is not None:
        from .guards import require_presentation
        inventory['presentation']['author_decision'] = 'accepted'
        require_presentation(inventory, presentation_approval)
    executable = None
    if not missing:
        executable = {
            "artifact_version": "1",
            "status": "FROZEN_FOR_PHASE03_PRE_GATE" if presentation_approval else "PENDING_PRESENTATION_APPROVAL",
            "provenance_kind": "study2_scientific",
            "source_commit": assembly_base_commit,
            "catalog_id": labels["namespace"],
            "label_space": labels["label_space"],
            "agents": agents,
            "development_cases": prompt_cases,
            "local_examples": local_examples,
            "insights": insights,
            "derangements": derangements["derangements"],
            "transfer_case_by_agent": transfer_cases,
        }
    return inventory, executable


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--assembly-base-commit", required=True)
    parser.add_argument("--normal-handoff", type=Path)
    parser.add_argument("--insight-handoff", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--pilot-id")
    parser.add_argument("--model-snapshot", type=Path)
    parser.add_argument("--executable-output", type=Path)
    parser.add_argument("--pseudolabel", type=Path, default=root / "studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json")
    parser.add_argument("--assignment", type=Path, default=root / "studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json")
    parser.add_argument("--derangements", type=Path, default=root / "studio2/fase03/pseudolabel/CONDITION_E_DERANGEMENTS.json")
    args = parser.parse_args()
    execution = {}
    if args.insight_handoff is not None:
        from .ledger import PilotLedger
        from .guards import require_execution, require_pilot_ledger, verify_tokenizer
        from studio2.fase03.prepare_gate import offline_token_counter
        from studio2.fase03.protocol import PREFLIGHT_CONFIG_PATH
        config = load_json(PREFLIGHT_CONFIG_PATH)
        require_execution(config)
        if args.ledger is None or args.pilot_id is None or args.model_snapshot is None:
            raise HarnessError('insight handoff requires shared ledger, pilot id and pinned tokenizer snapshot')
        ledger = PilotLedger(args.ledger, pilot_id=args.pilot_id)
        require_pilot_ledger(config, ledger)
        verify_tokenizer(args.model_snapshot, **config['tokenizer'])
        execution = dict(ledger=ledger, token_count=offline_token_counter(args.model_snapshot, chat_template=False),
                         schema_dir=root/'studio2/fase03/schema_insight', presentation_approval=config['presentation_approval'])
    inventory, executable = build_inventory(
        **execution,
        evidence_root=args.evidence_root,
        pseudolabel_path=args.pseudolabel,
        assignment_path=args.assignment,
        derangement_path=args.derangements,
        assembly_base_commit=args.assembly_base_commit,
        normal_handoff=args.normal_handoff,
        insight_handoff=args.insight_handoff,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if executable is not None:
        if args.executable_output is None:
            raise HarnessError("complete inputs require --executable-output")
        args.executable_output.write_text(json.dumps(executable, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(canonical_json({"status": inventory["status"], "missing": inventory["missing_requirements"], "executable_written": executable is not None}))
    return 0 if executable is not None else 3


if __name__ == "__main__":
    raise SystemExit(main())
