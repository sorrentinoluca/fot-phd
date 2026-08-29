from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

from phase_b.config import load_protocol_config
from phase_b.insights import (
    build_fixed_derangements,
    corrupt_peer_insights,
    peer_only_insights,
    validate_global_insights,
)
from phase_b.prompts.leakage import scan_files


ROOT = Path(__file__).resolve().parents[2]
INSIGHT_DIR = ROOT / "phase_b/insights"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FinalInsightStructuralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_protocol_config()
        cls.values = json.loads(
            (INSIGHT_DIR / "final_local_insights.json").read_text(encoding="utf-8")
        )
        cls.insights = validate_global_insights(cls.values, cls.config)
        cls.runs = json.loads(
            (INSIGHT_DIR / "generation_runs.json").read_text(encoding="utf-8")
        )
        cls.hashes = json.loads(
            (INSIGHT_DIR / "final_insight_hashes.json").read_text(encoding="utf-8")
        )["sha256"]

    def test_four_generations_and_exactly_eight_insights(self) -> None:
        self.assertEqual(self.runs["status"], "COMPLETE")
        self.assertEqual(self.runs["generation_completed"], 4)
        self.assertEqual(len(self.runs["generations"]), 4)
        self.assertEqual(len(self.insights), 8)
        self.assertEqual(
            Counter(item.source_agent for item in self.insights),
            Counter({f"agent_{index}": 2 for index in range(1, 5)}),
        )

    def test_first_structurally_valid_output_wins_and_provenance_is_complete(self) -> None:
        required = {
            "source_agent", "pseudolabel", "development_scope", "requested_model",
            "returned_model", "reasoning_effort", "temperature", "seed",
            "response_id", "request_id", "input_tokens", "output_tokens",
            "total_tokens", "timestamp", "retry_count", "prompt_hash",
            "input_bundle_hash", "raw_response_hash", "parsed_response_hash",
        }
        for generation in self.runs["generations"]:
            self.assertTrue(required.issubset(generation))
            self.assertEqual(generation["development_scope"], [1, 2, 3, 4, 5])
            self.assertTrue(generation["first_structurally_valid_output_wins"])
            valid_indices = [
                item["attempt"] for item in generation["attempts"]
                if item["structurally_valid"]
            ]
            self.assertEqual(valid_indices, [generation["first_valid_attempt"]])
            self.assertEqual(generation["attempt_count"], len(generation["attempts"]))
            self.assertEqual(generation["retry_count"], len(generation["attempts"]) - 1)
            self.assertEqual(generation["first_valid_attempt"], len(generation["attempts"]))

    def test_peer_libraries_and_strong_B_E_invariance(self) -> None:
        frozen = json.loads(
            (ROOT / "phase_b/config/evaluator_side/condition_e_derangements.json").read_text()
        )["derangements"]
        self.assertEqual(frozen, build_fixed_derangements(self.config))
        labels = self.config["label_space"][:-1]
        for agent_id in self.config["agents"]:
            b = peer_only_insights(self.insights, agent_id, self.config)
            e = corrupt_peer_insights(b, agent_id=agent_id, derangements=frozen)
            self.assertEqual(len(b), 6)
            self.assertEqual(len(e), 6)
            self.assertEqual([item.insight_id for item in b], [item.insight_id for item in e])
            self.assertTrue(all(x.pseudolabel != y.pseudolabel for x, y in zip(b, e)))
            b_path = INSIGHT_DIR / "peer_libraries" / f"{agent_id}_B.json"
            e_path = INSIGHT_DIR / "peer_libraries" / f"{agent_id}_E.json"
            b_text = b_path.read_text(encoding="utf-8")
            e_text = e_path.read_text(encoding="utf-8")
            self.assertEqual(len(b_text), len(e_text))
            for label in labels:
                b_text = b_text.replace(f'"{label}"', '"<LABEL>"')
                e_text = e_text.replace(f'"{label}"', '"<LABEL>"')
            self.assertEqual(b_text.encode(), e_text.encode())

    def test_leakage_and_hash_completeness(self) -> None:
        self.assertEqual(
            scan_files(
                [
                    ROOT / "phase_b/prompts/insight_generation.txt",
                    INSIGHT_DIR / "input_bundles",
                    INSIGHT_DIR / "final_local_insights.json",
                    INSIGHT_DIR / "peer_libraries",
                    INSIGHT_DIR / "generation_runs.json",
                ]
            ),
            [],
        )
        required_groups = {
            "insight_generation_prompt_template", "input_bundles",
            "rendered_generation_prompts", "raw_generation_outputs",
            "final_local_insights", "peer_libraries", "pseudolabel_mapping",
            "derangement_config", "execution_config", "local_insight_schema",
            "provider_insight_schema",
        }
        self.assertEqual(set(self.hashes), required_groups)
        self.assertEqual(
            self.hashes["final_local_insights"],
            sha256_file(INSIGHT_DIR / "final_local_insights.json"),
        )
        self.assertEqual(len(self.hashes["input_bundles"]), 4)
        self.assertEqual(len(self.hashes["peer_libraries"]), 8)
        self.assertEqual(
            len(self.hashes["raw_generation_outputs"]),
            sum(len(item["attempts"]) for item in self.runs["generations"]),
        )


if __name__ == "__main__":
    unittest.main()
