#!/usr/bin/env python3
"""Complete registry C4 from sealed scores; never update the operational threshold."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import beta, binom

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_hash(path: Path, expected: str) -> None:
    if sha256(path) != expected:
        raise ValueError(f"frozen input hash mismatch: {path}")


def bootstrap_order_statistic(values, rank: int, seed: int, replicates: int):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or not len(values) or not np.isfinite(values).all():
        raise ValueError("expected a nonempty finite one-dimensional score sample")
    if not 1 <= rank <= len(values) or replicates < 2:
        raise ValueError("invalid rank or replicate count")
    rng = np.random.Generator(np.random.PCG64(seed))
    indices = rng.integers(0, len(values), size=(replicates, len(values)))
    return np.partition(values[indices], rank - 1, axis=1)[:, rank - 1]


def exact_bootstrap_distribution(values, rank: int):
    """CDF(T* <= x) = P(Binom(n, empirical_CDF(x)) >= rank)."""
    values = np.asarray(values, dtype=float)
    support, counts = np.unique(values, return_counts=True)
    cdf = binom.sf(rank - 1, len(values), np.cumsum(counts) / len(values))
    pmf = np.diff(np.concatenate(([0.0], cdf)))
    return support, cdf, pmf


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--protocol', type=Path, default=HERE/'THRESHOLD_UNCERTAINTY_PROTOCOL.json')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('refusing to overwrite an existing result')
    protocol = json.loads(args.protocol.read_text())
    for relative, digest in protocol['immutable_inputs'].items():
        require_hash(ROOT/relative, digest)
    freeze_path = HERE/'THRESHOLD_FREEZE.json'
    freeze = json.loads(freeze_path.read_text())
    scores_path = HERE/'CAL_THR_SCORES.csv'
    require_hash(scores_path, freeze['sources']['cal_thr_scores_csv'])
    plan_path = HERE/'plans/cal_thr.csv'
    require_hash(plan_path, freeze['sources']['cal_thr_plan_csv'])
    with scores_path.open(newline='') as f:
        rows = list(csv.DictReader(f))
    with plan_path.open(newline='') as f:
        plan = list(csv.DictReader(f))
    by_id = {row['run_id']: row for row in rows}
    if len(by_id) != len(rows) or set(by_id) != {p['run_id'] for p in plan}:
        raise ValueError('duplicate or missing calibration run')
    for p in plan:
        if any(by_id[p['run_id']][k] != p[k] for k in ('stream_id', 'J')):
            raise ValueError(f"plan mismatch: {p['run_id']}")
    values = np.array([float(by_id[p['run_id']]['S']) for p in plan])
    n = len(values)
    rank = math.ceil((n + 1) * (1 - freeze['alpha']))
    conf = protocol['bootstrap']
    if n != freeze['n'] or n != conf['sample_size'] or rank != freeze['rank'] or rank != conf['rank_one_based']:
        raise ValueError('calibration n/rank differs from freeze/protocol')
    threshold = float(np.sort(values)[rank - 1])
    if threshold != freeze['threshold'] or freeze['rule'] != 'S > threshold':
        raise ValueError('operational threshold/rule differs from sealed sample')
    boot = bootstrap_order_statistic(values, rank, conf['seed'], conf['replicates'])
    tail = (1 - conf['percentile_confidence']) / 2
    interval = np.quantile(boot, [tail, 1-tail], method=conf['percentile_method'])
    support, cdf, pmf = exact_bootstrap_distribution(values, rank)
    exact_mean = float(pmf @ support)
    exact_sd = float(np.sqrt(pmf @ ((support - exact_mean)**2)))
    exact_interval = [float(support[np.searchsorted(cdf, q)]) for q in (tail, 1-tail)]
    counts = Counter(float(x) for x in values)
    duplicates = [{'score': v, 'multiplicity': count} for v, count in sorted(counts.items()) if count > 1]
    shapes = [n+1-rank, rank]
    if shapes != protocol['beta']['shapes']:
        raise ValueError('beta shapes differ from protocol')
    beta_tail = (1 - protocol['beta']['confidence']) / 2
    beta_result = {
        'shapes': shapes,
        'assumptions': protocol['beta']['assumptions'],
        'calibration_ties_observed': bool(duplicates),
        'continuity_proven_by_no_ties': False,
        'interpretation': 'distribution of true conditional mixture FAR across repeated calibration samples, conditional on a fixed score fit; not an empirical FAR interval',
    }
    if duplicates:
        beta_result['status'] = 'omitted_due_to_observed_calibration_ties'
    else:
        beta_result.update(status='reported_conditionally_on_assumptions', mean=float(beta.mean(*shapes)),
                           standard_deviation=float(beta.std(*shapes)), confidence=protocol['beta']['confidence'],
                           central_interval=beta.ppf([beta_tail,1-beta_tail],*shapes).tolist())
    result = {
        'schema_version': 1,
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'source_commit': protocol['source_commit'],
        'analysis_timing': protocol['analysis_timing'],
        'protocol_sha256': sha256(args.protocol),
        'script_sha256': sha256(Path(__file__)),
        'immutable_inputs': protocol['immutable_inputs'],
        'environment': {'python': sys.version, 'platform': platform.platform(), 'numpy': np.__version__, 'scipy': scipy.__version__},
        'n': n, 'rank': rank, 'alpha': freeze['alpha'], 'operational_threshold': threshold,
        'rule': freeze['rule'], 'operational_threshold_modified': False,
        'ties': {'distinct_scores': len(counts), 'duplicate_excess': n-len(counts),
                 'duplicate_groups': duplicates, 'multiplicity_at_threshold': counts[threshold]},
        'bootstrap_threshold': {
            **conf, 'mean': float(boot.mean()), 'standard_error': float(boot.std(ddof=conf['standard_error_ddof'])),
            'percentile_interval': interval.tolist(), 'bootstrap_values_sha256_float64_le': hashlib.sha256(boot.astype('<f8').tobytes()).hexdigest(),
            'interpretation': 'descriptive uncertainty of the fixed-rank empirical threshold; conditional on fitted score; no replacement threshold',
            'exact_empirical_distribution_check': {'mean': exact_mean, 'standard_deviation': exact_sd,
                'central_generalized_inverse_interval': exact_interval,
                'mean_monte_carlo_z': float((boot.mean()-exact_mean)/(exact_sd/math.sqrt(conf['replicates']))) if exact_sd else 0,
                'max_ecdf_difference': float(np.max(np.abs(np.searchsorted(np.sort(boot), support, side='right')/len(boot)-cdf)))},
        },
        'beta_conditional_far': beta_result,
        'binomial_count_3_through_12': {str(p): float(binom.cdf(12,150,p)-binom.cdf(2,150,p)) for p in (shapes[0]/(n+1),0.0484,0.05)},
    }
    # Check again after all calculations and before producing the supplementary result.
    for relative, digest in protocol['immutable_inputs'].items():
        require_hash(ROOT/relative, digest)
    with args.output.open('x') as f:
        f.write(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
