from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import jsonschema

from phase_b.exp3_v2 import evaluate_exp3v2_frozen_predictions as evaluator


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "phase_b/exp3_v2"


def synthetic_truth() -> dict[str, str]:
    mapping = {
        "N": "Normal",
        "F1": "CLS-ZOGAA",
        "F8": "CLS-OJNSG",
        "F10": "CLS-R463B",
        "F13": "CLS-Z3ISU",
    }
    result: dict[str, str] = {}
    for case_id in evaluator.canonical_case_ids():
        token = case_id.split("-")[1]
        result[case_id] = mapping[token]
    return result


def outcome(repetition: int, label: str | None, *, parse_failure: bool = False) -> dict:
    return {
        "repetition": repetition,
        "predicted_label": label,
        "abstain": label is None,
        "parse_failure": parse_failure,
    }


def aggregate(case_id: str, agent_id: str, condition: str, label: str | None) -> dict:
    fallback = next(item for item in evaluator.LABELS if item != label)
    outcomes = [outcome(1, label), outcome(2, label), outcome(3, fallback)]
    parsed = {
        "predicted_label": label,
        "abstain": label is None,
        "used_insight_ids": [],
        "reasoning_summary": (
            "aggregate_majority_2_of_3"
            if label is not None
            else "aggregate_no_label_majority"
        ),
    }
    if label is None:
        outcomes = [
            outcome(1, evaluator.LABELS[0]),
            outcome(2, evaluator.LABELS[1]),
            outcome(3, None, parse_failure=True),
        ]
    return {
        "physical_case_id": case_id,
        "agent_id": agent_id,
        "condition": condition,
        "parsed_output": parsed,
        "repetition_outcomes": outcomes,
        "aggregation_rule": "frozen_valid_label_majority_2_of_3_else_abstain",
    }


def synthetic_aggregates() -> list[dict]:
    truth = synthetic_truth()
    values: list[dict] = []
    for case_id, agent_id, condition in evaluator.expected_aggregate_keys():
        true_label = truth[case_id]
        if condition == "B":
            label = true_label
        elif true_label == "Normal":
            label = "Normal"
        else:
            label = "Normal"
        values.append(aggregate(case_id, agent_id, condition, label))
    return values


class Exp3V2EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.truth = synthetic_truth()
        cls.aggregates = synthetic_aggregates()
        cls.results, cls.bootstrap = evaluator.confirmatory_bundle(
            cls.aggregates,
            cls.truth,
            aggregate_sha256="0" * 64,
        )

    def test_config_is_exact_and_schema_valid(self) -> None:
        config = evaluator.load_json(HERE / "EXP3_V2_EVALUATION_CONFIG_001.json")
        schema = evaluator.load_json(
            HERE / "evaluation_schemas/exp3v2_evaluation_config.schema.json"
        )
        jsonschema.Draft202012Validator(schema).validate(config)
        self.assertEqual(config["optional_analyses"], [])
        self.assertEqual(config["bootstrap"]["seed"], 320031)

    def test_exact_canonical_coverage_and_denominators(self) -> None:
        self.assertEqual(len(evaluator.canonical_case_ids()), 30)
        self.assertEqual(len(self.aggregates), 360)
        self.assertEqual(self.results["primary_agent_case_rows_per_condition"], 72)
        self.assertEqual(
            self.results["secondary_agent_case_rows_per_condition"],
            {"local_seen": 24, "normal": 24, "overall": 120},
        )
        self.assertEqual(self.results["physical_fault_clusters"], 24)
        for metrics in self.results["condition_metrics"].values():
            self.assertEqual(
                {name: value["n"] for name, value in metrics.items()},
                {"unseen": 72, "local_seen": 24, "normal": 24, "overall": 120},
            )
            for value in metrics.values():
                self.assertEqual(value["correct"] + value["incorrect"], value["n"])
                self.assertLessEqual(value["abstentions"], value["incorrect"])

    def test_populations_are_disjoint_complete_and_exact(self) -> None:
        populations = evaluator.population_rows(
            evaluator.validate_aggregates(deepcopy(self.aggregates)),
            self.truth,
            {
                "agent_1": "CLS-ZOGAA",
                "agent_2": "CLS-OJNSG",
                "agent_3": "CLS-R463B",
                "agent_4": "CLS-Z3ISU",
            },
        )
        keys = {
            name: {(row["physical_case_id"], row["agent_id"]) for row in rows}
            for name, rows in populations.items()
        }
        self.assertEqual(
            {name: len(value) for name, value in keys.items()},
            {
                "unseen": 72,
                "local_seen": 24,
                "normal": 24,
                "overall": 120,
            },
        )
        self.assertFalse(keys["unseen"] & keys["local_seen"])
        self.assertFalse(keys["unseen"] & keys["normal"])
        self.assertFalse(keys["local_seen"] & keys["normal"])
        self.assertEqual(
            keys["unseen"] | keys["local_seen"] | keys["normal"], keys["overall"]
        )
        with self.assertRaisesRegex(RuntimeError, "bijectively"):
            evaluator.population_rows(
                evaluator.validate_aggregates(deepcopy(self.aggregates)),
                self.truth,
                {
                    "agent_1": "CLS-ZOGAA",
                    "agent_2": "CLS-ZOGAA",
                    "agent_3": "CLS-R463B",
                    "agent_4": "CLS-Z3ISU",
                },
            )
        incomplete_truth = dict(self.truth)
        incomplete_truth.pop("EXP3V2-N-001")
        with self.assertRaisesRegex(RuntimeError, "incomplete or incorrectly"):
            evaluator.population_rows(
                evaluator.validate_aggregates(deepcopy(self.aggregates)),
                incomplete_truth,
                {
                    "agent_1": "CLS-ZOGAA",
                    "agent_2": "CLS-OJNSG",
                    "agent_3": "CLS-R463B",
                    "agent_4": "CLS-Z3ISU",
                },
            )

    def test_minimal_confirmatory_outputs_only(self) -> None:
        self.assertEqual(set(self.results["contrasts"]), {"B_minus_A", "B_minus_E"})
        self.assertEqual(self.results["optional_analyses_included"], [])
        encoded = evaluator.canonical_json_bytes(self.results)
        for forbidden in (
            b"confusion",
            b"per_agent",
            b"pooled",
            b"recall",
            b"repetition_stability",
            b"helped",
            b"harmed",
            b"p_value",
        ):
            self.assertNotIn(forbidden, encoded)
        for condition in evaluator.CONDITIONS:
            for population in ("local_seen", "normal", "overall"):
                metric = self.results["condition_metrics"][condition][population]
                self.assertNotIn("ci_lower", metric)
                self.assertNotIn("ci_upper", metric)
                self.assertNotIn("success", metric)

    def test_success_criteria_match_prospective_contract(self) -> None:
        criteria = self.results["success_criteria"]
        self.assertTrue(criteria["requires_observed_B_minus_A_gt_0"])
        self.assertTrue(criteria["requires_B_minus_A_ci_lower_gt_0"])
        self.assertTrue(criteria["semantic_specificity_ci_is_not_a_gate"])
        self.assertEqual(
            self.results["multiplicity_adjustment"], "none_single_primary_contrast"
        )

    def test_bootstrap_contract_and_determinism(self) -> None:
        repeated = evaluator.bootstrap_confirmatory(
            evaluator.primary_rows(
                evaluator.validate_aggregates(deepcopy(self.aggregates)),
                self.truth,
                {
                    "agent_1": "CLS-ZOGAA",
                    "agent_2": "CLS-OJNSG",
                    "agent_3": "CLS-R463B",
                    "agent_4": "CLS-Z3ISU",
                },
            )
        )
        self.assertEqual(self.bootstrap, repeated)
        self.assertEqual(self.bootstrap["draws"], 10000)
        self.assertEqual(self.bootstrap["seed"], 320031)
        self.assertEqual(self.bootstrap["n_physical_clusters"], 24)
        self.assertEqual(self.bootstrap["clusters_per_pseudolabel"], 6)
        self.assertTrue(self.bootstrap["paired_conditions"])
        self.assertEqual(len(self.bootstrap["B_minus_A"]["distribution"]), 10000)
        self.assertEqual(len(self.bootstrap["B_minus_E"]["distribution"]), 10000)
        for contrast in ("B_minus_A", "B_minus_E"):
            values = self.bootstrap[contrast]["distribution"]
            self.assertEqual(
                self.bootstrap[contrast]["ci_lower"],
                float(evaluator.np.quantile(values, 0.025)),
            )
            self.assertEqual(
                self.bootstrap[contrast]["ci_upper"],
                float(evaluator.np.quantile(values, 0.975)),
            )

    def test_exact_synthetic_counts_and_abstention_partition(self) -> None:
        self.assertEqual(
            self.results["condition_metrics"]["B"],
            {
                "unseen": {
                    "n": 72,
                    "correct": 72,
                    "incorrect": 0,
                    "abstentions": 0,
                    "accuracy": 1.0,
                },
                "local_seen": {
                    "n": 24,
                    "correct": 24,
                    "incorrect": 0,
                    "abstentions": 0,
                    "accuracy": 1.0,
                },
                "normal": {
                    "n": 24,
                    "correct": 24,
                    "incorrect": 0,
                    "abstentions": 0,
                    "accuracy": 1.0,
                },
                "overall": {
                    "n": 120,
                    "correct": 120,
                    "incorrect": 0,
                    "abstentions": 0,
                    "accuracy": 1.0,
                },
            },
        )
        values = deepcopy(self.aggregates)
        key = ("EXP3V2-F1-001", "agent_2", "A")
        index = evaluator.expected_aggregate_keys().index(key)
        values[index] = aggregate(*key, None)
        revised, _ = evaluator.confirmatory_bundle(
            values, self.truth, aggregate_sha256="0" * 64
        )
        unseen_a = revised["condition_metrics"]["A"]["unseen"]
        self.assertEqual(unseen_a["abstentions"], 1)
        self.assertEqual(unseen_a["correct"] + unseen_a["incorrect"], 72)
        self.assertLessEqual(unseen_a["abstentions"], unseen_a["incorrect"])

    def test_parse_failure_and_majority_tie_become_abstention(self) -> None:
        record = aggregate("EXP3V2-N-001", "agent_1", "A", None)
        evaluator.validate_aggregates(
            [
                (
                    aggregate(case_id, agent_id, condition, "Normal")
                    if (case_id, agent_id, condition)
                    != ("EXP3V2-N-001", "agent_1", "A")
                    else record
                )
                for case_id, agent_id, condition in evaluator.expected_aggregate_keys()
            ]
        )
        self.assertIsNone(evaluator.normalized_prediction(record["parsed_output"]))

    def test_two_valid_votes_win_despite_one_parse_failure(self) -> None:
        record = aggregate("EXP3V2-N-001", "agent_1", "A", "Normal")
        record["repetition_outcomes"][2] = outcome(3, None, parse_failure=True)
        values = synthetic_aggregates()
        values[0] = record
        evaluator.validate_aggregates(values)
        self.assertEqual(
            evaluator.normalized_prediction(record["parsed_output"]), "Normal"
        )

    def test_missing_extra_duplicate_and_reordered_records_fail_closed(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "360"):
            evaluator.validate_aggregates(self.aggregates[:-1])
        with self.assertRaisesRegex(RuntimeError, "360"):
            evaluator.validate_aggregates([*self.aggregates, self.aggregates[-1]])
        duplicate = deepcopy(self.aggregates)
        duplicate[-1] = deepcopy(duplicate[0])
        with self.assertRaisesRegex(RuntimeError, "duplicate"):
            evaluator.validate_aggregates(duplicate)
        reordered = deepcopy(self.aggregates)
        reordered[0], reordered[1] = reordered[1], reordered[0]
        with self.assertRaisesRegex(RuntimeError, "order or coverage"):
            evaluator.validate_aggregates(reordered)

    def test_wrong_aggregate_majority_is_rejected(self) -> None:
        values = deepcopy(self.aggregates)
        values[0]["parsed_output"]["predicted_label"] = "CLS-ZOGAA"
        with self.assertRaisesRegex(RuntimeError, "majority"):
            evaluator.validate_aggregates(values)

    def test_output_manifest_is_deterministic_and_detects_tamper(self) -> None:
        result_bytes = evaluator.canonical_json_bytes(self.results)
        bootstrap_bytes = evaluator.canonical_json_bytes(self.bootstrap)
        first = evaluator.output_manifest(result_bytes, bootstrap_bytes)
        second = evaluator.output_manifest(result_bytes, bootstrap_bytes)
        self.assertEqual(first, second)
        tampered = evaluator.output_manifest(result_bytes + b" ", bootstrap_bytes)
        self.assertNotEqual(first["inventory_sha256"], tampered["inventory_sha256"])

    def test_draft_manifest_blocks_production_before_runtime_or_inputs(self) -> None:
        frozen_manifest_path = HERE / "EXP3_V2_EVALUATION_HARNESS_MANIFEST_001.json"
        draft = evaluator.load_json(frozen_manifest_path)
        draft["status"] = "PRE_FREEZE_DRAFT"
        draft["tag_created"] = False
        schema = evaluator.load_json(
            HERE / "evaluation_schemas/exp3v2_evaluation_harness_manifest.schema.json"
        )
        jsonschema.Draft202012Validator(schema).validate(draft)
        self.assertEqual(draft["status"], "PRE_FREEZE_DRAFT")
        self.assertFalse(draft["tag_created"])

        with tempfile.TemporaryDirectory() as temporary:
            draft_path = Path(temporary) / frozen_manifest_path.name
            draft_path.write_bytes(evaluator.canonical_json_bytes(draft))
            with self.assertRaisesRegex(RuntimeError, "not frozen"):
                evaluator.validate_harness_boundary(draft_path)

    def test_clean_detached_annotated_tag_enforcement(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(
                ["git", "config", "user.name", "Synthetic Test"], cwd=repo, check=True
            )
            subprocess.run(
                ["git", "config", "user.email", "synthetic@example.invalid"],
                cwd=repo,
                check=True,
            )
            (repo / "fixture.txt").write_text("synthetic\n", encoding="utf-8")
            subprocess.run(["git", "add", "fixture.txt"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "synthetic"], cwd=repo, check=True)
            subprocess.run(
                ["git", "tag", "-a", "synthetic-tag", "-m", "synthetic"],
                cwd=repo,
                check=True,
            )
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=repo, text=True
            ).strip()
            tag_object = subprocess.check_output(
                ["git", "rev-parse", "synthetic-tag"], cwd=repo, text=True
            ).strip()
            subprocess.run(
                ["git", "checkout", "-q", "--detach", "synthetic-tag^{}"],
                cwd=repo,
                check=True,
            )
            self.assertEqual(
                evaluator.verify_clean_detached_tag(
                    repo,
                    tag="synthetic-tag",
                    tag_object=tag_object,
                    peeled_commit=commit,
                ),
                commit,
            )
            (repo / "unexpected.txt").write_text("dirty\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "not clean"):
                evaluator.verify_clean_detached_tag(repo, tag="synthetic-tag")

    def test_no_provider_or_workbook_dependency(self) -> None:
        for path in (
            HERE / "evaluate_exp3v2_frozen_predictions.py",
            HERE / "verify_exp3v2_evaluation.py",
        ):
            source = path.read_text(encoding="utf-8")
            self.assertNotIn("OPENAI_API_KEY", source)
            self.assertNotIn("OpenAI", source)
            self.assertNotIn("openpyxl", source)
            self.assertNotIn(".xlsx", source)

    @unittest.skipUnless(
        importlib.metadata.version("numpy") == "2.5.2",
        "full production CLI rehearsal requires the pinned evaluation runtime",
    )
    def test_full_production_cli_and_verifier_with_synthetic_tagged_inputs(
        self,
    ) -> None:
        def canonical(value: object) -> bytes:
            return evaluator.canonical_json_bytes(value)

        def initialize_tagged_repo(
            root: Path, tag: str, files: dict[str, bytes]
        ) -> tuple[str, str]:
            root.mkdir(exist_ok=True)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "user.name", "Synthetic Test"], cwd=root, check=True
            )
            subprocess.run(
                ["git", "config", "user.email", "synthetic@example.invalid"],
                cwd=root,
                check=True,
            )
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            subprocess.run(["git", "add", "--all"], cwd=root, check=True)
            subprocess.run(
                ["git", "commit", "-qm", "synthetic boundary"], cwd=root, check=True
            )
            subprocess.run(
                ["git", "tag", "-a", tag, "-m", "synthetic boundary"],
                cwd=root,
                check=True,
            )
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip()
            tag_object = subprocess.check_output(
                ["git", "rev-parse", tag], cwd=root, text=True
            ).strip()
            subprocess.run(
                ["git", "checkout", "-q", "--detach", f"{tag}^{{}}"],
                cwd=root,
                check=True,
            )
            return tag_object, commit

        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            truth = synthetic_truth()
            case_plan = {
                "cases": [
                    {
                        "physical_case_id": case_id,
                        "condition": (
                            "Normal"
                            if truth[case_id] == "Normal"
                            else {
                                "CLS-ZOGAA": "F1",
                                "CLS-OJNSG": "F8",
                                "CLS-R463B": "F10",
                                "CLS-Z3ISU": "F13",
                            }[truth[case_id]]
                        ),
                        "primary_seed": 320001 + index,
                    }
                    for index, case_id in enumerate(evaluator.canonical_case_ids())
                ]
            }
            mapping = {
                "real_to_opaque": {
                    "F1": "CLS-ZOGAA",
                    "F8": "CLS-OJNSG",
                    "F10": "CLS-R463B",
                    "F13": "CLS-Z3ISU",
                },
                "normal_label": "Normal",
            }
            data_lines = ["physical_case_id,fault/status,attempt,seed\n"]
            for index, case in enumerate(case_plan["cases"]):
                data_lines.append(
                    f"{case['physical_case_id']},{case['condition']},0,{320001 + index}\n"
                )
            data_bytes = "".join(data_lines).encode()
            aggregate_bytes = b"".join(
                canonical(item) for item in synthetic_aggregates()
            )

            role_specs = {
                "source": (
                    "exp3-v2-heldout-frozen-002",
                    "phase_b/exp3_v2/EXP3_V2_FREEZE_MANIFEST_002.json",
                    {
                        "phase_b/exp3_v2/exp3v2_case_plan.json": canonical(case_plan),
                        "phase_b/config/evaluator_side/pseudolabel_mapping.json": canonical(
                            mapping
                        ),
                    },
                ),
                "data": (
                    "exp3-v2-heldout-data-frozen-001",
                    "phase_b/exp3_v2/EXP3_V2_DATA_FREEZE_MANIFEST_001.json",
                    {"tep_exp3_v2_heldout/exp3v2_manifest.csv": data_bytes},
                ),
                "verbalization_harness": (
                    "exp3-v2-verbalization-harness-frozen-001",
                    "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json",
                    {},
                ),
                "verbalizations": (
                    "exp3-v2-verbalizations-frozen-001",
                    "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_DATA_FREEZE_MANIFEST_001.json",
                    {},
                ),
                "inference_harness": (
                    "exp3-v2-inference-harness-frozen-001",
                    "phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json",
                    {},
                ),
                "execution_authorization": (
                    "exp3-v2-inference-execution-frozen-001",
                    "phase_b/exp3_v2/EXP3_V2_INFERENCE_EXECUTION_AUTHORIZATION_MANIFEST_001.json",
                    {},
                ),
                "inference_outputs": (
                    "exp3-v2-inference-frozen-001",
                    "phase_b/exp3_v2/EXP3_V2_INFERENCE_DATA_FREEZE_MANIFEST_001.json",
                    {"inference_outputs/aggregate_records.jsonl": aggregate_bytes},
                ),
            }
            roots: dict[str, Path] = {}
            bindings: list[dict] = []
            for role, (tag, manifest_path, extra) in role_specs.items():
                boundary_bytes = canonical({"synthetic_boundary": role})
                files = {manifest_path: boundary_bytes, **extra}
                root = base / role
                tag_object, commit = initialize_tagged_repo(root, tag, files)
                roots[role] = root
                bindings.append(
                    {
                        "role": role,
                        "tag": tag,
                        "tag_object": tag_object,
                        "peeled_commit": commit,
                        "manifest_path": manifest_path,
                        "manifest_sha256": hashlib.sha256(boundary_bytes).hexdigest(),
                    }
                )

            harness = base / "harness"
            harness.mkdir()
            allowlist = evaluator.load_json(
                HERE / "EXP3_V2_EVALUATION_HARNESS_MANIFEST_001.json"
            )["freeze_commit_allowlist"]
            for relative in allowlist:
                source = ROOT / relative
                destination = harness / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
            config_path = harness / "phase_b/exp3_v2/EXP3_V2_EVALUATION_CONFIG_001.json"
            config = json.loads(config_path.read_text())
            config["status"] = "FROZEN_BEFORE_EVALUATION"
            config_path.write_bytes(canonical(config))
            manifest_path = (
                harness / "phase_b/exp3_v2/EXP3_V2_EVALUATION_HARNESS_MANIFEST_001.json"
            )
            manifest = json.loads(manifest_path.read_text())
            manifest["status"] = evaluator.FROZEN_STATUS
            manifest["tag_created"] = True
            manifest["upstream_tags"] = bindings
            manifest["inputs"] = {
                "case_plan": {
                    "path": "phase_b/exp3_v2/exp3v2_case_plan.json",
                    "size_bytes": len(canonical(case_plan)),
                    "sha256": hashlib.sha256(canonical(case_plan)).hexdigest(),
                },
                "data_manifest": {
                    "path": "tep_exp3_v2_heldout/exp3v2_manifest.csv",
                    "size_bytes": len(data_bytes),
                    "sha256": hashlib.sha256(data_bytes).hexdigest(),
                },
                "pseudolabel_mapping": {
                    "path": "phase_b/config/evaluator_side/pseudolabel_mapping.json",
                    "size_bytes": len(canonical(mapping)),
                    "sha256": hashlib.sha256(canonical(mapping)).hexdigest(),
                },
                "aggregate_records": {
                    "path": "inference_outputs/aggregate_records.jsonl",
                    "size_bytes": len(aggregate_bytes),
                    "sha256": hashlib.sha256(aggregate_bytes).hexdigest(),
                },
            }
            for binding in manifest["harness_artifacts"]:
                path = harness / binding["path"]
                binding["size_bytes"] = path.stat().st_size
                binding["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            manifest_path.write_bytes(canonical(manifest))
            initialize_tagged_repo(
                harness,
                evaluator.HARNESS_TAG,
                {relative: (harness / relative).read_bytes() for relative in allowlist},
            )

            output_root = base / "output"
            command = [
                sys.executable,
                str(harness / "phase_b/exp3_v2/evaluate_exp3v2_frozen_predictions.py"),
                "--harness-manifest",
                str(manifest_path),
                "--source-root",
                str(roots["source"]),
                "--data-root",
                str(roots["data"]),
                "--verbalization-harness-root",
                str(roots["verbalization_harness"]),
                "--verbalizations-root",
                str(roots["verbalizations"]),
                "--inference-harness-root",
                str(roots["inference_harness"]),
                "--authorization-root",
                str(roots["execution_authorization"]),
                "--inference-root",
                str(roots["inference_outputs"]),
                "--output-root",
                str(output_root),
            ]
            completed = subprocess.run(
                command, check=True, text=True, capture_output=True
            )
            self.assertEqual(json.loads(completed.stdout)["status"], "PASS")
            verifier_command = command.copy()
            verifier_command[1] = str(
                harness / "phase_b/exp3_v2/verify_exp3v2_evaluation.py"
            )
            verified = subprocess.run(
                verifier_command, check=False, text=True, capture_output=True
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
            self.assertEqual(json.loads(verified.stdout)["status"], "PASS")
            self.assertEqual(
                {path.name for path in output_root.iterdir()}, evaluator_output_names()
            )


def evaluator_output_names() -> set[str]:
    return {
        "exp3v2_confirmatory_bootstrap.json",
        "exp3v2_confirmatory_results.json",
        "exp3v2_evaluation_output_hash_manifest.json",
    }


if __name__ == "__main__":
    unittest.main()
