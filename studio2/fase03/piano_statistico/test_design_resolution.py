"""Test di `design_resolution.py` (sotto-fase 03.8): formule, guardia dati, simulazione.

Esecuzione: `python3 -m unittest studio2.fase03.piano_statistico.test_design_resolution`
oppure, dalla cartella, `python3 -m unittest test_design_resolution`.
Nessun dato reale è letto: i test girano su dati sintetici generati con seed fisso.
"""

from __future__ import annotations

import json
import math
import io
import os
import sys
import tempfile
from statistics import NormalDist
import unittest
from unittest.mock import patch
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import design_resolution as dr  # noqa: E402


class AnalyticTests(unittest.TestCase):
    def test_alpha_and_feasibility_in_analytic_grid(self) -> None:
        rows = dr.analytic_grid((64,), (0.1,), (0.125,), (0.3,), (0.5,), (0.2, 0.5), alpha=0.025)
        self.assertEqual(len(rows), 2)  # delta=0.5 > d=0.3 is impossible
        for row in rows:
            self.assertAlmostEqual(row.mde_80, dr.minimum_detectable(row.se, alpha=0.025))

    def test_hoeffding_mde_grid_range_and_unreachable_scenarios(self) -> None:
        rows = dr.analytic_grid((48, 64), (), (), (0.3, 0.5, 0.8), (0, 0.25, 0.5, 1), (0.2,))
        feasible = [r.hoeffding_mde_80 for r in rows if r.hoeffding_mde_80_feasible]
        self.assertAlmostEqual(min(feasible), 0.334084999653, places=5)
        self.assertAlmostEqual(max(feasible), 0.4619536338, places=5)
        self.assertTrue(all(not r.hoeffding_mde_80_feasible for r in rows if r.discordance == 0.3))


    def test_normal_functions_are_consistent(self) -> None:
        for p in (0.05, 0.2, 0.5, 0.8, 0.95, 0.975):
            self.assertAlmostEqual(dr.norm_cdf(dr.norm_ppf(p)), p, places=6)
        self.assertAlmostEqual(dr.norm_ppf(0.95), 1.6448536, places=5)
        self.assertAlmostEqual(dr.norm_ppf(0.975), 1.9599640, places=5)

    def test_se_paired_delta_formula(self) -> None:
        self.assertAlmostEqual(dr.se_paired_delta(48, 0.10), math.sqrt(0.10 / 48))
        # effetto di disegno di Kish: 7 osservazioni, rho = 1 → equivale a 1 osservazione per cluster
        self.assertAlmostEqual(dr.se_paired_delta(48, 0.5, 7, 1.0), math.sqrt(0.5 / 48))
        self.assertAlmostEqual(dr.se_paired_delta(48, 0.5, 7, 0.0), math.sqrt(0.5 / (7 * 48)))
        with self.assertRaises(ValueError):
            dr.se_paired_delta(48, 0.0)

    def test_power_and_mde_reference_values(self) -> None:
        se = dr.se_paired_delta(48, 0.10)
        # m = 0.125, d = 0.10, 48 cluster: z = 0.125/SE - 1.645
        expected = dr.norm_cdf(0.125 / se - dr.norm_ppf(0.95))
        self.assertAlmostEqual(dr.power_one_sided(se, 0.125), expected)
        self.assertGreater(dr.power_one_sided(se, 0.125), 0.80)
        # a δ = -m (bordo) la potenza analitica è esattamente alpha
        self.assertAlmostEqual(dr.power_one_sided(se, 0.0), 0.05, places=6)
        # MDE a potenza 80% = (z_.95 + z_.80) SE
        self.assertAlmostEqual(dr.minimum_detectable(se), (1.6448536 + 0.8416212) * se, places=5)
        # più cluster → SE minore, stessa discordanza
        self.assertLess(dr.se_paired_delta(64, 0.10), dr.se_paired_delta(48, 0.10))

    def test_analytic_grid_shape(self) -> None:
        rows = dr.analytic_grid((48, 64), (0.1, 0.2), (0.125,), (0.5,), (0.0, 1.0), (0.2,))
        self.assertEqual(len(rows), 2 * (2 * 1 + 1 * 2 * 1))
        self.assertTrue(all(r.hypothesis in {"H3", "H1/H2"} for r in rows))


class DataGuardTests(unittest.TestCase):
    def test_guard_blocks_update_modes_and_pathlib(self) -> None:
        # Only a synthetic temporary file is used to demonstrate the old bypasses.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.txt"
            path.write_text("synthetic")
            dr.install_data_guard()
            try:
                for opener in (open, io.open):
                    for mode in ("r", "rb", "r+", "w+", "a+", "x+"):
                        with self.subTest(opener=opener, mode=mode):
                            with self.assertRaises(dr.DataAccessError):
                                opener(path, mode)
                with self.assertRaises(dr.DataAccessError):
                    path.read_text()
            finally:
                dr.remove_data_guard()
            self.assertEqual(path.read_text(), "synthetic")

    def test_guard_blocks_reads_and_forbidden_paths(self) -> None:
        dr.install_data_guard()
        try:
            with self.assertRaises(dr.DataAccessError):
                open(__file__, "r", encoding="utf-8")
            with self.assertRaises(dr.DataAccessError):
                open("studio2/fase03/fault_runs/runs/x.csv", "w")
            with tempfile.TemporaryDirectory() as tmp:
                with open(Path(tmp) / "ok.txt", "w", encoding="utf-8") as fh:
                    fh.write("scrittura ammessa\n")
        finally:
            dr.remove_data_guard()
        # dopo la rimozione la lettura torna possibile
        with open(__file__, "r", encoding="utf-8") as fh:
            self.assertTrue(fh.readline())

    def test_forbidden_argv(self) -> None:
        with self.assertRaises(dr.DataAccessError):
            dr.assert_no_forbidden_argv(["--out", "studio2/fase03/soglie_normal/runs"])
        dr.assert_no_forbidden_argv(["--out", "."])


class TangoAndSignFlipTests(unittest.TestCase):
    def test_tango_zero_discordance_finite_closed_form(self) -> None:
        for n in (48, 64):
            for margin in (0.1, 0.125, 0.15):
                b = c = np.array([0.0])
                self.assertAlmostEqual(float(dr.tango_restricted_p21(b, c, n, -margin)[0]), margin)
                z = float(dr.tango_score_z(b, c, n, -margin)[0])
                self.assertTrue(math.isfinite(z))
                self.assertAlmostEqual(z, math.sqrt(n * margin / (1 - margin)))

    def test_restricted_mle_solves_score_equation(self) -> None:
        b, c, n, d0 = np.array([5.0]), np.array([3.0]), 48, -0.125
        tango_p21 = dr.tango_restricted_p21(b, c, n, d0)
        p21 = float(tango_p21[0])
        self.assertGreater(p21, 0.0)
        p12 = p21 + d0
        self.assertGreater(p12, 0.0)
        # derivata della log-verosimiglianza vincolata nulla nella radice
        score = b[0] / p12 + c[0] / p21 - 2.0 * (n - b[0] - c[0]) / (1.0 - 2.0 * p21 - d0)
        self.assertAlmostEqual(float(score), 0.0, places=6)
        self.assertEqual(tango_p21.shape, (1,))

    def test_tango_reference_behaviour(self) -> None:
        # a delta0 = 0 e b = c la statistica è nulla; con b > c è positiva
        self.assertAlmostEqual(float(dr.tango_score_z(np.array([4.0]), np.array([4.0]), 48, 0.0)[0]), 0.0)
        self.assertGreater(float(dr.tango_score_z(np.array([6.0]), np.array([2.0]), 48, 0.0)[0]), 0.0)
        # zero coppie discordanti e margine 0.125 su 48 coppie: la non inferiorità si dichiara
        z = float(dr.tango_score_z(np.array([0.0]), np.array([0.0]), 48, -0.125)[0])
        self.assertGreater(z, dr.norm_ppf(0.95))
        # perdita di 6 casi su 48 (= m) senza guadagni: siamo esattamente al bordo, non si rifiuta
        z = float(dr.tango_score_z(np.array([0.0]), np.array([6.0]), 48, -0.125)[0])
        self.assertAlmostEqual(z, 0.0, places=9)

    def test_sign_flip_pvalues(self) -> None:
        rng = np.random.default_rng(3)
        strong = np.full((2, 48), 0.5)
        p = dr.sign_flip_pvalues(strong, 500, rng)
        self.assertTrue(np.all(p < 0.05))
        null = rng.choice(np.array([-1.0, 0.0, 1.0]), size=(300, 48))
        p = dr.sign_flip_pvalues(null, 300, rng)
        self.assertLessEqual(float((p <= 0.05).mean()), 0.12)


class WeakNullTests(unittest.TestCase):
    def test_exact_two_point_pvalue_limits(self) -> None:
        # tutti i valori positivi: solo l'assegnazione originale raggiunge la somma osservata
        self.assertAlmostEqual(dr.sign_flip_exact_two_point(4, 4, 0.5, -1.0), 1 / 16)
        # media osservata negativa: p = 1 - (frazione di inversioni con somma < osservata) >= 0,5
        self.assertGreaterEqual(dr.sign_flip_exact_two_point(6, 1, 1 / 7, -1.0), 0.5)

    def test_counterexample_matches_independent_verification(self) -> None:
        # valori del secondo verbale: 0,0508194 (48 cluster) e 0,0849922 (64 cluster)
        r48 = dr.weak_null_counterexample(48)
        r64 = dr.weak_null_counterexample(64)
        self.assertAlmostEqual(r48["mean_under_null"], 0.0, places=12)
        self.assertAlmostEqual(r48["exact_size_sign_flip"], 0.0508194, places=6)
        self.assertAlmostEqual(r64["exact_size_sign_flip"], 0.0849922, places=6)
        # sotto una nulla simmetrica (a = -b, prob 1/2) il test è di livello alpha
        sym = dr.weak_null_counterexample(48, a=1.0, b=-1.0, prob_a=0.5)
        self.assertLessEqual(sym["exact_size_sign_flip"], 0.05 + 1e-12)
        # il test di Hoeffding controlla il livello anche sotto la nulla asimmetrica
        self.assertLessEqual(r48["exact_size_hoeffding"], 0.05)
        self.assertLessEqual(r64["exact_size_hoeffding"], 0.05)

    def test_hoeffding_threshold_and_power(self) -> None:
        # t = 2 sqrt(ln(1/alpha) / (2n)): 0,3533 a 48 cluster, 0,3060 a 64
        self.assertAlmostEqual(dr.hoeffding_threshold(48), 0.3533018, places=6)
        self.assertAlmostEqual(dr.hoeffding_threshold(64), 0.3059684, places=6)
        self.assertLess(dr.hoeffding_threshold(64), dr.hoeffding_threshold(48))
        se = dr.se_paired_delta(64, 0.8, 7, 0.5)
        self.assertLess(dr.hoeffding_power(se, 0.2, 64), dr.hoeffding_power(se, 0.5, 64))
        self.assertGreater(dr.hoeffding_power(se, 0.7, 64), 0.99)
        # sotto la nulla la potenza approssimata è ben sotto alpha (test conservativo)
        self.assertLess(dr.hoeffding_power(se, 0.0, 64), 0.01)
        with self.assertRaises(ValueError):
            dr.hoeffding_threshold(64, alpha=1.5)


class SimulationTests(unittest.TestCase):
    def test_serialized_one_sided_bound_name_and_level_follow_alpha(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for alpha in (0.05, 0.025):
                with self.subTest(alpha=alpha):
                    dr.main(["--quick", "--reps", "4", "--boot", "20",
                             "--alpha", str(alpha), "--out", tmp])
                    payload = json.loads((Path(tmp) / "DESIGN_RESOLUTION.json").read_text())
                    self.assertEqual(payload["alpha_one_sided"], alpha)
                    for row in payload["analytic"]:
                        self.assertNotIn("one_sided_bound_distance_95", row)
                        self.assertIn("one_sided_bound_distance", row)
                        expected = NormalDist().inv_cdf(1 - alpha) * row["se"]
                        self.assertAlmostEqual(row["one_sided_bound_distance"], expected, places=8)
                        # This separate bilateral interval remains fixed at 95%.
                        self.assertAlmostEqual(row["two_sided_halfwidth_95"],
                                               NormalDist().inv_cdf(0.975) * row["se"], places=8)

    def test_alpha_changes_decisions_but_not_central_90_interval(self) -> None:
        for simulation, args in ((dr.simulate_h3, (8, 0.2, 0, 0.125)),
                                 (dr.simulate_h12, (8, 0.5, 0.4, 0.5))):
            at_05 = simulation(*args, reps=80, boot=100, seed=91, alpha=0.05)
            at_025 = simulation(*args, reps=80, boot=100, seed=91, alpha=0.025)
            self.assertEqual(at_05["mean_halfwidth_90"], at_025["mean_halfwidth_90"])
            self.assertLessEqual(at_025["rejection_rate"], at_05["rejection_rate"])
            decision = "rejection_rate_tango" if simulation is dr.simulate_h3 else "rejection_rate_hoeffding"
            self.assertLessEqual(at_025[decision], at_05[decision])

    def test_main_propagates_alpha_to_both_simulation_tests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(dr, "simulate_h3", wraps=dr.simulate_h3) as h3, \
                    patch.object(dr, "simulate_h12", wraps=dr.simulate_h12) as h12:
                dr.main(["--quick", "--reps", "4", "--boot", "20", "--alpha", "0.025", "--out", tmp])
                for simulation in (h3, h12):
                    self.assertGreater(simulation.call_count, 0)
                    self.assertTrue(all(c.kwargs.get("alpha") == 0.025 for c in simulation.call_args_list))
            result = json.loads((Path(tmp) / "DESIGN_RESOLUTION.json").read_text())
            self.assertEqual(result["alpha_one_sided"], 0.025)
            self.assertIn("α = 0.025", (Path(tmp) / "DESIGN_RESOLUTION.md").read_text())

    def test_paired_delta_marginals(self) -> None:
        rng = np.random.default_rng(1)
        x = dr.draw_paired_deltas(rng, (200_000,), 0.4, 0.1)
        self.assertAlmostEqual(float((x != 0).mean()), 0.4, places=2)
        self.assertAlmostEqual(float(x.mean()), 0.1, places=2)
        with self.assertRaises(ValueError):
            dr.draw_paired_deltas(rng, (10,), 0.1, 0.2)

    def test_bootstrap_quantiles_degenerate_and_ordered(self) -> None:
        rng = np.random.default_rng(2)
        sums = np.zeros((8, 6), dtype=np.int64)
        sizes = np.ones((8, 6), dtype=np.int64)
        q = dr.stratified_cluster_bootstrap_quantiles(sums, sizes, 200, rng)
        self.assertEqual(tuple(q), (0.0, 0.0))
        sums = rng.integers(-1, 2, size=(8, 6)).astype(np.int64)
        q = dr.stratified_cluster_bootstrap_quantiles(sums, sizes, 500, rng)
        self.assertLessEqual(q[0], q[1])
        self.assertGreaterEqual(q[0], -1.0)
        self.assertLessEqual(q[1], 1.0)

    def test_h3_size_at_margin_and_power_at_zero(self) -> None:
        # 64 cluster, d = 0.10, m = 0.125: al bordo il tasso di rifiuto deve stare vicino ad alpha,
        # sotto delta = 0 deve essere alto (analitico ≈ 0.94).
        size = dr.simulate_h3(8, 0.10, -0.10, 0.10, reps=150, boot=400, seed=11)
        self.assertLessEqual(size["rejection_rate"], 0.18)
        self.assertLessEqual(size["rejection_rate_tango"], 0.10)
        power = dr.simulate_h3(8, 0.10, 0.0, 0.125, reps=150, boot=400, seed=12)
        self.assertGreaterEqual(power["rejection_rate"], 0.75)
        self.assertGreater(power["mean_halfwidth_90"], 0.0)

    def test_h12_icc_reduces_power_and_size_is_controlled(self) -> None:
        low = dr.simulate_h12(6, 0.5, 0.2, 0.0, reps=120, boot=400, seed=21)
        high = dr.simulate_h12(6, 0.5, 0.2, 1.0, reps=120, boot=400, seed=22)
        self.assertGreater(low["rejection_rate"], high["rejection_rate"])
        self.assertLess(low["mean_halfwidth_90"], high["mean_halfwidth_90"])
        null = dr.simulate_h12(6, 0.5, 0.0, 0.5, reps=150, boot=400, seed=23)
        self.assertLessEqual(null["rejection_rate"], 0.15)

    def test_main_quick_writes_outputs_and_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rc = dr.main(["--quick", "--reps", "20", "--boot", "100", "--out", tmp, "--seed", "5"])
            self.assertEqual(rc, 0)
            first = json.loads((Path(tmp) / "DESIGN_RESOLUTION.json").read_text(encoding="utf-8"))
            self.assertTrue(first["no_real_data"])
            self.assertTrue((Path(tmp) / "DESIGN_RESOLUTION.md").exists())
            dr.main(["--quick", "--reps", "20", "--boot", "100", "--out", tmp, "--seed", "5"])
            second = json.loads((Path(tmp) / "DESIGN_RESOLUTION.json").read_text(encoding="utf-8"))
            self.assertEqual(first["simulated"], second["simulated"])
            # float canonici: nessun valore con più di 12 cifre decimali
            def walk(o):
                if isinstance(o, float):
                    self.assertEqual(o, round(o, dr.FLOAT_DIGITS))
                elif isinstance(o, dict):
                    for v in o.values():
                        walk(v)
                elif isinstance(o, list):
                    for v in o:
                        walk(v)
            walk(first)
            self.assertEqual(first["float_digits"], dr.FLOAT_DIGITS)
        # la guardia non deve restare installata dopo main()
        self.assertIs(open, dr._ORIGINAL_OPEN)


class PublishedArtifactTests(unittest.TestCase):
    """Only synthetic design artifacts and the proposed plan are read here."""

    def test_published_analytic_and_markdown_match_generator(self) -> None:
        base = Path(__file__).resolve().parent
        payload = json.loads((base / "DESIGN_RESOLUTION.json").read_text())
        g = payload["grid"]
        rows = dr.analytic_grid(tuple(8 * n for n in g["n_per_fault"]), g["h3_discordance"],
                                g["h3_margins"], g["h12_discordance"], g["h12_icc"],
                                g["h12_effects"], payload["alpha_one_sided"])
        self.assertEqual(dr.canonical([dr.asdict(r) for r in rows]), payload["analytic"])
        # Reconstruct from the canonical JSON: documents must not depend on hidden results.
        canonical_rows = [dr.AnalyticRow(**r) for r in payload["analytic"]]
        expected = dr.markdown_tables(canonical_rows, payload["simulated"],
                                      payload["alpha_one_sided"], payload["reps"])
        expected += dr.weak_null_markdown(payload["weak_null_counterexample"], payload["alpha_one_sided"])
        self.assertEqual(expected, (base / "DESIGN_RESOLUTION.md").read_text())

    def test_plan_h3_summary_matches_published_results(self) -> None:
        base = Path(__file__).resolve().parent
        payload = json.loads((base / "DESIGN_RESOLUTION.json").read_text())
        plan = (base / "PIANO_STATISTICO.md").read_text()
        for n in (48, 64):
            cells = []
            for d in (0.05, 0.1, 0.2, 0.3):
                a = next(r for r in payload["analytic"] if r["hypothesis"] == "H3"
                         and r["n_clusters"] == n and r["discordance"] == d and r["margin_or_effect"] == 0.125)
                mc = next(r for r in payload["simulated"] if r["hypothesis"] == "H3"
                          and r["n_clusters"] == n and r["discordance"] == d
                          and r["margin"] == 0.125 and r["scenario"] == "power_at_zero_delta")
                cells.append(f"{a['power_at_null_or_effect']:.2f} ({mc['rejection_rate_tango']:.4f})".replace(".", ","))
            self.assertIn(f"| **{n}** ({n // 8} run) | " + " | ".join(cells) + " |", plan)


if __name__ == "__main__":
    unittest.main()
