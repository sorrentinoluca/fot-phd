from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))

from combined_score import FEATURES, fit_parameters, score_feature_table  # noqa: E402
from validate_numerics import compare_values  # noqa: E402


class CombinedScoreTests(unittest.TestCase):
    def feature_tables(self) -> list[pd.DataFrame]:
        tables = []
        for window in range(3):
            table = pd.DataFrame(
                {
                    feature: np.linspace(0.1 + window, 2.1 + window, 41)
                    * (index + 1)
                    for index, feature in enumerate(FEATURES)
                }
            )
            tables.append(table)
        return tables

    def test_a_and_a_prime_are_finite(self) -> None:
        table = self.feature_tables()[0]
        for variant in ("A", "A_prime"):
            parameters = fit_parameters(self.feature_tables(), variant)
            score, maxima = score_feature_table(table, parameters)
            self.assertTrue(np.isfinite(score))
            self.assertTrue(np.isfinite(maxima).all())

    def test_a_prime_rejects_absent_positive_values(self) -> None:
        tables = self.feature_tables()
        for table in tables:
            table[FEATURES[0]] = 0.0
        with self.assertRaisesRegex(ValueError, "c_f is undefined"):
            fit_parameters(tables, "A_prime")

    def test_zero_mad_is_blocking(self) -> None:
        tables = self.feature_tables()
        for table in tables:
            table[FEATURES[1]] = 1.0
        with self.assertRaisesRegex(ValueError, "MAD is zero"):
            fit_parameters(tables, "A")

    def test_comparison_limits(self) -> None:
        reference = np.arange(1.0, 10.0)
        self.assertTrue(compare_values(reference.copy(), reference)["pass"])
        self.assertFalse(compare_values(reference + 10.0, reference)["pass"])


if __name__ == "__main__":
    unittest.main()
