import importlib.util
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np


MODULE_PATH = Path(__file__).with_name("run_verifica_sintetica_h3.py")
SPEC = importlib.util.spec_from_file_location("h3synthetic", MODULE_PATH)
h3 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(h3)


class SyntheticH3Tests(unittest.TestCase):
    def test_tango_independent_control_and_degenerate_cases(self):
        checked = h3.verify_tango()
        self.assertEqual(len(checked["cases"]), 7)
        self.assertAlmostEqual(float(h3.tango_score_z(np.array([0]), np.array([0]))[0]), math.sqrt(64 * 0.125 / 0.875))
        self.assertAlmostEqual(float(h3.tango_score_z(np.array([0]), np.array([8]))[0]), 0.0)

    def test_manifest_shape_order_and_prechecks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.jsonl"
            summary = h3.build_manifest(path)
            records = h3.read_manifest(path)
        self.assertEqual(summary["target_scenarios"], 1620)
        self.assertEqual(summary["boundary_icc0_points"], 108)
        self.assertEqual(records[0]["rho_target"], 0.0)
        self.assertEqual(records[1]["rho_target"], 0.05)
        self.assertEqual(records[-1]["rho_target"], 0.40)

    def test_three_off_grid_smoke_scenarios(self):
        result = h3.self_test()
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["official_grid_used"])
        self.assertEqual(len(result["smoke_cases"]), 3)


if __name__ == "__main__":
    unittest.main()
