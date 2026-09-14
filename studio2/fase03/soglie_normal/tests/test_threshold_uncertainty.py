import importlib.util
import itertools
from pathlib import Path

import numpy as np
import pytest

spec = importlib.util.spec_from_file_location('uncertainty', Path(__file__).resolve().parents[1]/'complete_threshold_uncertainty.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_exact_distribution_matches_exhaustive_resampling_with_ties():
    values = [1., 1., 4.]
    support, cdf, pmf = module.exact_bootstrap_distribution(values, 2)
    exact = np.array([sorted(sample)[1] for sample in itertools.product(values, repeat=3)])
    np.testing.assert_allclose(cdf, [(exact <= x).mean() for x in support], atol=1e-15)
    np.testing.assert_allclose(pmf, [(exact == x).mean() for x in support], atol=1e-15)


def test_resampling_uses_order_statistic_not_interpolated_quantile():
    actual = module.bootstrap_order_statistic([1., 4., 20.], 2, 37, 50)
    assert set(actual) <= {1., 4., 20.}
    indices = np.random.Generator(np.random.PCG64(37)).integers(0, 3, size=(50,3))
    expected = [sorted([1.,4.,20.][i] for i in row)[1] for row in indices]
    np.testing.assert_array_equal(actual, expected)


def test_reject_invalid_rank_and_nonfinite_scores():
    with pytest.raises(ValueError): module.bootstrap_order_statistic([1.,2.], 3, 1, 10)
    with pytest.raises(ValueError): module.bootstrap_order_statistic([1.,float('nan')], 2, 1, 10)


def test_frozen_input_mismatch_is_rejected(tmp_path):
    path = tmp_path/'scores.csv'
    path.write_text('original')
    digest = module.sha256(path)
    path.write_text('changed')
    with pytest.raises(ValueError, match='frozen input hash mismatch'):
        module.require_hash(path, digest)
