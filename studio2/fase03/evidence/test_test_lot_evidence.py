"""Offline tests for the 03.11 test-lot consumer input driver.

The decisive test is byte identity: the unit produced for the assigned window by the new
driver must equal, byte for byte, the unit 03.6 produces for the same window of the same
run.  That is what "same frozen pipeline, same thresholds, same descriptors, same neutral
renderer" means operationally.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

try:
    from .extract_evidence import extract_rows, load_frozen_api, sha256_file
    from . import extract_test_lot_evidence as driver
except ImportError:  # pragma: no cover - direct execution
    from extract_evidence import extract_rows, load_frozen_api, sha256_file
    import extract_test_lot_evidence as driver

ROOT = Path(__file__).resolve().parents[3]


class TestLotEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = load_frozen_api(ROOT)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.baseline, self.case = self.synthetic_baseline_and_case()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def synthetic_baseline_and_case(self):
        pd = self.api.pd
        blocks = []
        for block_index in range(5):
            time = np.arange(0.0, 20.0, 0.1)
            values = {"Time": time}
            for index, name in enumerate(self.api.xmeas, start=1):
                values[name] = (index + np.sin(time * (0.25 + index / 80.0) + block_index * 0.2)
                                + 0.05 * np.cos(time * 2.0 + index))
            blocks.append(pd.DataFrame(values))
        baseline = self.api.compute_baseline_stats_from_blocks(blocks)
        time = np.arange(20.0, 65.0 + 0.05, 0.1)
        values = {"Time": time}
        for index, name in enumerate(self.api.xmeas, start=1):
            values[name] = (index + np.sin(time * (0.25 + index / 80.0))
                            + 0.05 * np.cos(time * 2.0 + index)
                            + (0.2 if index % 3 == 0 else 0.0) * np.maximum(time - 25.0, 0.0))
        return baseline, pd.DataFrame(values)

    def lot_row(self, run_id: str) -> dict[str, str]:
        source = self.base / f"{run_id}.csv"
        self.case.to_csv(source, index=False, lineterminator="\n")
        return {"run_id": run_id, "status": "complete", "stream_id": "999", "idv": "1",
                "useful_windows_complete": "8", "output_path": str(source),
                "output_sha256": sha256_file(source)}

    def run_driver(self, assignment, rows, name="out"):
        return driver.extract(
            api=self.api, assignment=assignment,
            lot_rows={row["run_id"]: row for row in rows},
            baseline=self.baseline, output_dir=self.base / name, runs_root=None,
            baseline_provenance={"baseline_sha256": "synthetic", "r2_guard_sha256": "synthetic"})

    def test_one_unit_per_run_on_the_assigned_window(self):
        assignment = [
            {"case_id": "test-primary-F1-r01", "window_ordinal": 3,
             "window_start_h": 35.0, "window_end_h": 40.0},
            {"case_id": "test-primary-F1-r02", "window_ordinal": 8,
             "window_start_h": 60.0, "window_end_h": 65.0},
        ]
        rows = [self.lot_row(item["case_id"]) for item in assignment]
        summary = self.run_driver(assignment, rows)
        self.assertEqual(summary["evidence_unit_count"], 2)
        self.assertEqual(summary["not_extracted"], [])
        self.assertEqual(summary["windows_extracted_per_run"], 1)
        units = sorted((self.base / "out" / "units").glob("*.txt"))
        self.assertEqual(len(units), 2)

    def test_unit_is_byte_identical_to_the_frozen_03_6_unit(self):
        ordinal = 5
        run_id = "test-primary-F1-r01"
        row = self.lot_row(run_id)
        # 03.6 parses the development batch out of the run_id; only the identifier
        # differs, the bytes of the source CSV are the same file.
        reference_row = dict(row, run_id="synthetic-b01")
        reference = extract_rows(repo_root=ROOT, api=self.api, rows=[reference_row],
                                 baseline=self.baseline, output_dir=self.base / "ref")
        self.assertEqual(reference["evidence_unit_count"], 8)
        assignment = [{"case_id": run_id, "window_ordinal": ordinal,
                       "window_start_h": 25.0 + (ordinal - 1) * 5.0,
                       "window_end_h": 30.0 + (ordinal - 1) * 5.0}]
        self.run_driver(assignment, [row], name="one")
        for suffix in (".txt", ".evidence.json", ".features.csv", ".signature.csv"):
            frozen_unit = self.base / "ref" / "units" / f"EVD-{ordinal:04d}{suffix}"
            driver_unit = self.base / "one" / "units" / f"EVT-0001{suffix}"
            self.assertEqual(frozen_unit.read_bytes(), driver_unit.read_bytes(), suffix)

    def test_missing_run_is_recorded_and_never_substituted(self):
        assignment = [
            {"case_id": "test-primary-F1-r01", "window_ordinal": 1,
             "window_start_h": 25.0, "window_end_h": 30.0},
            {"case_id": "test-primary-F1-r02", "window_ordinal": 2,
             "window_start_h": 30.0, "window_end_h": 35.0},
        ]
        rows = [self.lot_row("test-primary-F1-r01")]
        summary = self.run_driver(assignment, rows)
        self.assertEqual(summary["evidence_unit_count"], 1)
        self.assertEqual([item["case_id"] for item in summary["not_extracted"]],
                         ["test-primary-F1-r02"])
        self.assertIn("substitution_policy", summary)

    def test_run_without_eight_windows_is_recorded_not_extracted(self):
        row = self.lot_row("test-primary-F1-r01")
        row["useful_windows_complete"] = "7"
        assignment = [{"case_id": "test-primary-F1-r01", "window_ordinal": 1,
                       "window_start_h": 25.0, "window_end_h": 30.0}]
        summary = self.run_driver(assignment, [row])
        self.assertEqual(summary["evidence_unit_count"], 0)
        self.assertIn("useful windows", summary["not_extracted"][0]["reason"])

    def test_extraction_is_deterministic(self):
        assignment = [{"case_id": "test-primary-F1-r01", "window_ordinal": 4,
                       "window_start_h": 40.0, "window_end_h": 45.0}]
        rows = [self.lot_row("test-primary-F1-r01")]
        one = self.run_driver(assignment, rows, name="a")
        two = self.run_driver(assignment, rows, name="b")
        self.assertEqual(one["evidence_manifest_sha256"], two["evidence_manifest_sha256"])

    def test_consumer_manifest_carries_a_hash_per_case(self):
        assignment = [{"case_id": "test-primary-F1-r01", "window_ordinal": 2,
                       "window_start_h": 30.0, "window_end_h": 35.0}]
        self.run_driver(assignment, [self.lot_row("test-primary-F1-r01")])
        manifest = (self.base / "out" / "EVIDENCE_MANIFEST_TEST.csv").read_text(encoding="utf-8")
        self.assertIn("neutral_text_sha256", manifest)
        self.assertIn("test-primary-F1-r01", manifest)

    def test_fault_never_reaches_the_consumer_side_manifest(self):
        assignment = [{"case_id": "test-primary-F1-r01", "window_ordinal": 2,
                       "window_start_h": 30.0, "window_end_h": 35.0}]
        self.run_driver(assignment, [self.lot_row("test-primary-F1-r01")])
        consumer = (self.base / "out" / "EVIDENCE_MANIFEST_TEST.csv").read_text(encoding="utf-8")
        evaluator = (self.base / "out" / "EVALUATOR_INDEX_TEST.csv").read_text(encoding="utf-8")
        self.assertNotIn("fault", consumer)
        self.assertIn("fault", evaluator)

    def test_download_instructions_name_the_release_and_the_hash(self):
        instructions = driver.download_instructions(Path("/tmp/lot"))
        self.assertEqual(instructions["release"], "studio2-fase03-test-v1")
        self.assertTrue(any("shasum -a 256 -c" in line for line in instructions["commands"]))
        self.assertIn(instructions["asset_sha256"], json.dumps(instructions))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
