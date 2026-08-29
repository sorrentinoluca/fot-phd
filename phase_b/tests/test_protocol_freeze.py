from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
FREEZE_PATH = ROOT / "phase_b/config/phase_b_protocol_frozen.json"
MANIFEST_PATH = ROOT / "phase_b/PHASE_B_PROTOCOL_HASHES.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ProtocolFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_global_manifest_matches_every_frozen_artifact(self) -> None:
        artifacts = self.manifest["artifacts"]
        self.assertGreaterEqual(len(artifacts), 50)
        self.assertEqual(len(artifacts), len(set(artifacts)))
        for relative, expected in artifacts.items():
            path = Path(relative)
            self.assertFalse(path.is_absolute())
            self.assertNotIn(path.suffix.lower(), {".xls", ".xlsx"})
            self.assertTrue((ROOT / path).is_file(), relative)
            self.assertEqual(sha256_file(ROOT / path), expected, relative)

    def test_freeze_records_required_execution_and_statistical_rules(self) -> None:
        execution = self.freeze["execution"]
        self.assertEqual(execution["provider"], "openai")
        self.assertEqual(execution["requested_model"], "gpt-5.6-terra")
        self.assertEqual(execution["returned_model"], "gpt-5.6-terra")
        self.assertEqual(execution["reasoning_effort"], "medium")
        self.assertIsNone(execution["temperature"])
        self.assertIsNone(execution["seed"])
        self.assertEqual(execution["repetitions"], 3)
        self.assertEqual(execution["max_structural_retries"], 2)
        self.assertEqual(self.freeze["conditions"], ["A", "B", "E"])
        self.assertEqual(self.freeze["metrics"]["H2_epsilon"], 0.0)
        self.assertEqual(self.freeze["statistics"]["bootstrap_draws"], 10_000)
        self.assertEqual(self.freeze["statistics"]["bootstrap_seed"], 20260829)
        self.assertEqual(
            self.freeze["statistics"]["primary_physical_fault_run_clusters"], 12
        )
        self.assertFalse(
            self.freeze["statistics"]["agent_case_observations_independent"]
        )

    def test_freeze_hash_references_match_global_manifest(self) -> None:
        artifacts = self.manifest["artifacts"]
        self.assertEqual(
            artifacts["phase_b/config/evaluator_side/pseudolabel_mapping.json"],
            self.freeze["pseudolabel_mapping"]["sha256"],
        )
        self.assertEqual(
            artifacts["phase_b/local_knowledge/local_examples.json"],
            self.freeze["local_examples"]["artifact"]["sha256"],
        )
        self.assertEqual(
            artifacts["phase_b/insights/final_local_insights.json"],
            self.freeze["insights"]["final_library"]["sha256"],
        )
        self.assertEqual(
            artifacts["phase_b/config/execution_config.json"],
            self.freeze["execution"]["config_sha256"],
        )
        self.assertEqual(
            artifacts["phase_b/heldout/phase_b_heldout_manifest.csv"],
            self.freeze["heldout_freeze"]["manifest_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
