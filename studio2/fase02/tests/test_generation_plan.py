import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "build_generation_plan.py"
SPEC = importlib.util.spec_from_file_location("build_generation_plan", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GenerationPlanTests(unittest.TestCase):
    def test_prefix_plan_has_all_pairs(self):
        rows = MODULE.build_rows("prefix_qual", 20, False)
        self.assertEqual(len(rows), 110)
        for stream_id in range(100, 110):
            stream_rows = [row for row in rows if row["stream_id"] == stream_id]
            self.assertEqual(len(stream_rows), 11)
            self.assertEqual(
                sorted(row["window_position"] for row in stream_rows), list(range(11))
            )
            full = next(row for row in stream_rows if row["window_position"] == 0)
            self.assertEqual(full["stop_time_h"], 70)
            for row in stream_rows:
                if row["window_position"]:
                    self.assertEqual(
                        row["stop_time_h"], 20 + 5 * row["window_position"]
                    )

    def test_operational_stream_ranges_are_disjoint(self):
        names = ("pilot", "baseline_fit_new", "cal_thr", "far_ver")
        seen = set()
        for name in names:
            values = set(MODULE.STREAM_RANGES[name])
            self.assertFalse(seen & values)
            seen |= values

    def test_legacy_seeds_are_fixed_and_distinct(self):
        rows = MODULE.build_rows("legacy_generator_qual", 20, False)
        self.assertEqual(
            [row["legacy_seed"] for row in rows], list(range(1431655766, 1431655776))
        )


if __name__ == "__main__":
    unittest.main()
