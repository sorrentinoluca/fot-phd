from __future__ import annotations

import ast
import csv
import hashlib
import json
from pathlib import Path
import re
import unittest

from phase_b.prompts.leakage import scan_files


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT / "phase_b/final_evaluation"
MANIFEST_PATH = OUTPUT_ROOT / "heldout_verbalizations_manifest.json"
SOURCE_MANIFEST_PATH = ROOT / "phase_b/heldout/phase_b_heldout_manifest.csv"
RUNNER_PATH = OUTPUT_ROOT / "generate_frozen_verbalizations.py"
EXPECTED_PHASE_A_HASHES = {
    "code/verbalizer_config_v2.json": "552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519",
    "code/tep_verbalize_v2.py": "3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be",
    "code/evaluate_verbalizer_v2.py": "972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92",
    "code/tep_features.py": "cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FinalHeldoutVerbalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        with SOURCE_MANIFEST_PATH.open(newline="", encoding="utf-8") as stream:
            cls.source_rows = list(csv.DictReader(stream))

    def test_exactly_fifteen_case_id_only_artifact_pairs(self) -> None:
        cases = self.manifest["cases"]
        self.assertEqual(self.manifest["case_count"], 15)
        self.assertEqual(len(cases), 15)
        self.assertEqual(
            [entry["physical_case_id"] for entry in cases],
            [f"PBH-{index:03d}" for index in range(1, 16)],
        )
        self.assertEqual(
            len(list((OUTPUT_ROOT / "verbalized/structured").glob("PBH-*.json"))),
            15,
        )
        self.assertEqual(
            len(list((OUTPUT_ROOT / "verbalized/neutral_text").glob("PBH-*.txt"))),
            15,
        )
        for entry in cases:
            self.assertRegex(Path(entry["structured_output_path"]).name, r"^PBH-\d{3}\.json$")
            self.assertRegex(Path(entry["neutral_text_path"]).name, r"^PBH-\d{3}\.txt$")

    def test_output_hashes_and_frozen_v2_schema(self) -> None:
        expected_variables = {f"XMEAS-{index}" for index in range(1, 42)}
        for entry in self.manifest["cases"]:
            structured_path = ROOT / entry["structured_output_path"]
            neutral_path = ROOT / entry["neutral_text_path"]
            self.assertEqual(sha256_file(structured_path), entry["structured_output_sha256"])
            self.assertEqual(sha256_file(neutral_path), entry["neutral_text_sha256"])
            structured = json.loads(structured_path.read_text(encoding="utf-8"))
            self.assertEqual(structured["verbalizer_version"], "2.0")
            self.assertEqual(structured["n_windows"], 8)
            self.assertEqual(structured["time_range_h"], [10.0, 50.0])
            self.assertEqual(set(structured["variables"]), expected_variables)
            self.assertTrue(neutral_path.read_text(encoding="utf-8").strip())

    def test_neutral_text_is_label_blind_and_prompt_contract_is_text_only(self) -> None:
        neutral_dir = OUTPUT_ROOT / "verbalized/neutral_text"
        self.assertEqual(scan_files([neutral_dir]), [])
        forbidden = re.compile(r"\bCLS-[A-Z0-9]{5}\b|\bmode1_", re.IGNORECASE)
        source_filenames = {row["filename"].lower() for row in self.source_rows}
        for path in neutral_dir.glob("PBH-*.txt"):
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(forbidden.search(text))
            self.assertFalse(any(name in text.lower() for name in source_filenames))
        self.assertEqual(self.manifest["diagnostic_input_contract"], "neutral_text_only")
        self.assertFalse(self.manifest["structured_json_is_diagnostic_input"])

    def test_input_and_phase_a_hashes_are_preserved(self) -> None:
        source_by_case = {row["case_id"]: row for row in self.source_rows}
        for path_text, expected in EXPECTED_PHASE_A_HASHES.items():
            self.assertEqual(sha256_file(ROOT / path_text), expected)
        for entry in self.manifest["cases"]:
            source = source_by_case[entry["physical_case_id"]]
            self.assertEqual(entry["source_file_sha256"], source["sha256"])
            self.assertEqual(entry["frozen_v2_hashes"], EXPECTED_PHASE_A_HASHES)
            self.assertEqual(
                sha256_file(ROOT / "tep_heldout/mode1" / source["filename"]),
                source["sha256"],
            )

    def test_runner_has_no_llm_dependency(self) -> None:
        tree = ast.parse(RUNNER_PATH.read_text(encoding="utf-8"))
        imports = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imports.update(
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        )
        self.assertNotIn("openai", imports)


if __name__ == "__main__":
    unittest.main()
