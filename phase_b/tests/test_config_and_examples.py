from __future__ import annotations

import json
import unittest
from pathlib import Path

from phase_b.config import load_protocol_config, validate_execution_ready
from phase_b.config.protocol import derive_opaque_pseudolabel


ROOT = Path(__file__).resolve().parents[2]


class ConfigAndExamplesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_protocol_config()
        cls.examples = json.loads(
            (ROOT / "phase_b/local_knowledge/local_examples.json").read_text()
        )

    def test_pseudolabel_mapping_is_deterministic_and_evaluator_side(self) -> None:
        path = ROOT / "phase_b/config/evaluator_side/pseudolabel_mapping.json"
        mapping_doc = json.loads(path.read_text())
        namespace = mapping_doc["namespace"]
        mapping = mapping_doc["real_to_opaque"]
        self.assertEqual(
            {real: derive_opaque_pseudolabel(real, namespace) for real in mapping},
            mapping,
        )
        self.assertEqual(set(mapping.values()), set(self.config["label_space"][:-1]))
        self.assertFalse(any(label in {"Class-A", "Class-B", "Class-C", "Class-D"} for label in mapping.values()))

    def test_execution_identity_is_capability_verified_and_ready(self) -> None:
        execution = self.config["execution"]
        self.assertEqual(execution["requested_model"], "gpt-5.6-terra")
        self.assertEqual(execution["returned_model"], "gpt-5.6-terra")
        self.assertEqual(execution["model_version"], "gpt-5.6-terra")
        self.assertEqual(execution["token_accounting_source"], "response.usage")
        self.assertEqual(execution["capability_probe_status"], "COMPLETE")
        validate_execution_ready(self.config)

    def test_exactly_two_examples_per_local_class(self) -> None:
        self.assertEqual(self.examples["examples_per_local_class"], 2)
        self.assertFalse(self.examples["contains_structured_numerical_json"])
        metadata = json.loads(
            (ROOT / "phase_b/config/evaluator_side/local_example_sources.json").read_text()
        )
        self.assertNotIn("agents", self.examples)
        self.assertNotIn("agent_", json.dumps(self.examples, ensure_ascii=False))
        self.assertEqual(set(self.examples["packs"]), {f"LKP-{index:03d}" for index in range(1, 5)})
        for agent_id, pack_id in metadata["agent_to_pack"].items():
            items = self.examples["packs"][pack_id]
            local = self.config["agents"][agent_id]["local_fault_label"]
            self.assertEqual(sum(item["pseudolabel"] == local for item in items), 2)
            self.assertEqual(sum(item["pseudolabel"] == "Normal" for item in items), 2)
            self.assertEqual(len(items), 4)
            self.assertTrue(all(set(item) == {"example_id", "pseudolabel", "neutral_text"} for item in items))

    def test_selection_sources_are_batches_one_two_only(self) -> None:
        metadata = json.loads(
            (ROOT / "phase_b/config/evaluator_side/local_example_sources.json").read_text()
        )
        fault_sources = [row for row in metadata["sources"] if row["real_class"] != "Normal"]
        normal_sources = [row for row in metadata["sources"] if row["real_class"] == "Normal"]
        self.assertEqual(set(metadata["agent_to_pack"]), set(self.config["agents"]))
        self.assertEqual({row["batch"] for row in fault_sources}, {1, 2})
        self.assertEqual({row["normal_block"] for row in normal_sources}, {"N1", "N2"})


if __name__ == "__main__":
    unittest.main()
