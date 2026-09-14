from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np

try:
    from .extract_evidence import (
        EXPECTED_SOURCE_PATHS,
        extract_rows,
        load_frozen_api,
        sha256_file,
        validate_r2_guard,
        verify_frozen_sources,
    )
    from .leakage import scan_json, scan_text
except ImportError:  # Direct execution from this directory.
    from extract_evidence import (
        EXPECTED_SOURCE_PATHS,
        extract_rows,
        load_frozen_api,
        sha256_file,
        validate_r2_guard,
        verify_frozen_sources,
    )
    from leakage import scan_json, scan_text


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(str(candidate.relative_to(path)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(candidate.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = load_frozen_api(ROOT)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def synthetic_baseline_and_case(self):
        pd = self.api.pd
        blocks = []
        for block_index in range(5):
            time = np.arange(0.0, 20.0, 0.1)
            values = {"Time": time}
            for index, name in enumerate(self.api.xmeas, start=1):
                values[name] = (
                    index
                    + np.sin(time * (0.25 + index / 80.0) + block_index * 0.2)
                    + 0.05 * np.cos(time * 2.0 + index)
                )
            blocks.append(pd.DataFrame(values))
        baseline = self.api.compute_baseline_stats_from_blocks(blocks)

        time = np.arange(20.0, 65.0 + 0.05, 0.1)
        values = {"Time": time}
        for index, name in enumerate(self.api.xmeas, start=1):
            values[name] = (
                index
                + np.sin(time * (0.25 + index / 80.0))
                + 0.05 * np.cos(time * 2.0 + index)
                + (0.2 if index % 3 == 0 else 0.0) * np.maximum(time - 25.0, 0.0)
            )
        case = pd.DataFrame(values)
        return baseline, case

    def fixture_row(self, case) -> dict[str, str]:
        source = self.base / "synthetic.csv"
        case.to_csv(source, index=False, lineterminator="\n")
        return {
            "run_id": "synthetic-b01",
            "status": "complete",
            "stream_id": "999",
            "idv": "1",
            "useful_windows_complete": "8",
            "output_path": str(source),
            "output_sha256": sha256_file(source),
        }

    def test_synthetic_end_to_end_dimension_and_determinism(self) -> None:
        baseline, case = self.synthetic_baseline_and_case()
        row = self.fixture_row(case)
        first = self.base / "first"
        second = self.base / "second"
        one = extract_rows(
            repo_root=ROOT,
            api=self.api,
            rows=[row],
            baseline=baseline,
            output_dir=first,
        )
        two = extract_rows(
            repo_root=ROOT,
            api=self.api,
            rows=[row],
            baseline=baseline,
            output_dir=second,
        )
        self.assertEqual(one, two)
        self.assertEqual(one["evidence_unit_count"], 8)
        self.assertEqual(tree_digest(first), tree_digest(second))
        signatures = sorted((first / "units").glob("*.signature.csv"))
        self.assertEqual(len(signatures), 8)
        for path in signatures:
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 697)
        structured = json.loads(
            (first / "units" / "EVD-0001.evidence.json").read_text(encoding="utf-8")
        )
        self.assertEqual(structured["n_windows"], 1)

    def test_hash_guard_rejects_altered_source(self) -> None:
        copied = self.base / "code"
        copied.mkdir()
        for relative in EXPECTED_SOURCE_PATHS:
            shutil.copy2(ROOT / relative, copied / Path(relative).name)
        target = copied / "tep_features.py"
        target.write_bytes(target.read_bytes() + b"\n# altered by guard test\n")
        with self.assertRaisesRegex(RuntimeError, "Frozen source guard failed"):
            verify_frozen_sources(ROOT, code_dir=copied)

    def test_r2_guard_rejects_noncanonical_file(self) -> None:
        path = self.base / "r2.json"
        path.write_text('{"guard_pass": false}\n', encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "R2 guard hash mismatch"):
            validate_r2_guard(path)

    def test_leakage_detects_fault_id_mechanism_and_origin(self) -> None:
        self.assertTrue(scan_text("Diagnosi F14 su IDV(14)"))
        self.assertTrue(scan_text("meccanismo sticking valve"))
        self.assertTrue(scan_json({"origine": "nuovo D1"}))


if __name__ == "__main__":
    unittest.main()
