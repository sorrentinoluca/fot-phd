import hashlib
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[2]
F2 = ROOT / "studio2" / "fase02"
JSON_PATH = HERE / "R2_GUARD_RECHECK.json"
SOURCES = {
    "score_fit_legacy_sha256": F2 / "validation" / "score_fit_legacy.json",
    "r2_guard_result_v2_sha256": F2 / "validation" / "r2_guard_result_v2.json",
    "combined_score_sha256": F2 / "analysis" / "combined_score.py",
    "tep_features_sha256": F2 / "analysis" / "tep_features.py",
    "validate_numerics_sha256": F2 / "analysis" / "validate_numerics.py",
}


class R2GuardRecheckTest(unittest.TestCase):
    def test_all_fingerprints_are_current_64_hex_sha256(self):
        record = json.loads(JSON_PATH.read_text())
        for key, path in SOURCES.items():
            value = record[key]
            self.assertRegex(value, r"^[0-9a-f]{64}$", key)
            self.assertEqual(value, hashlib.sha256(path.read_bytes()).hexdigest(), key)

    def test_r2_matches_independent_phase02_result(self):
        self.assertEqual(
            json.loads((F2 / "validation" / "r2_guard_result_v2.json").read_text()),
            json.loads((F2 / "validation" / "r2_guard_result.json").read_text()),
        )
        self.assertTrue(json.loads(JSON_PATH.read_text())["guard_pass"])


if __name__ == "__main__":
    unittest.main()
