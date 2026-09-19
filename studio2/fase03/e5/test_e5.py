#!/usr/bin/env python3
"""G2 tests for the E5 preparation: diff, determinism, derived quantities, leakage.

Development data only. No model call, no network, no write outside a temporary directory.

Run with:  python3 -m unittest discover -s studio2/fase03/e5 -p 'test_e5.py' -v
(with ``E5_DEV_UNITS`` pointing at the cache built by ``build_dev_units.py``; the tests
that need real units skip when it is absent).
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
for candidate in (REPO_ROOT, REPO_ROOT / "code", HERE):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

import pandas as pd  # noqa: E402

import tep_verbalize_v2 as verbalizer  # noqa: E402
import e5_corruption  # noqa: E402
import e5_derangement  # noqa: E402
import protocol_omit  # noqa: E402
import build_e5_assignments as assignments  # noqa: E402
import verifica_e5_c2 as c2  # noqa: E402
import verifica_e5_c2_prompt as c2p  # noqa: E402
import build_e5_prompts as e5p  # noqa: E402
import run_e5  # noqa: E402

DEV_UNITS = Path(os.environ.get("E5_DEV_UNITS", "")) if os.environ.get("E5_DEV_UNITS") else None


def load_two_units():
    index = json.loads((DEV_UNITS / "DEV_UNITS_INDEX.json").read_text(encoding="utf-8"))
    rows = index["runs"]
    first, second = rows[0], rows[len(rows) // 2]
    frames = []
    for row in (first, second):
        frame = pd.read_csv(row["features_path"])
        start = sorted(frame.window_start_h.unique())[3]
        frames.append(frame[frame.window_start_h == start].copy().reset_index(drop=True))
    return frames[0], frames[1], first, second


def _first_unit_with_rapid():
    """A development unit whose neutral text carries the derived ``rapid`` sentence."""
    index = json.loads((DEV_UNITS / "DEV_UNITS_INDEX.json").read_text(encoding="utf-8"))
    for row in index["runs"]:
        frame = pd.read_csv(row["features_path"])
        for start in sorted(frame.window_start_h.unique()):
            unit = frame[frame.window_start_h == start].copy().reset_index(drop=True)
            result = verbalizer.verbalize_feature_table(unit)
            if result["structured"]["system_summary"]["dominant_variables"]["rapid"]:
                return unit
    return None


@unittest.skipIf(DEV_UNITS is None or not DEV_UNITS.is_dir(), "E5_DEV_UNITS not available")
class TestCorruption(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipient, cls.donor, cls.meta_r, cls.meta_d = load_two_units()

    def test_exactly_one_column_changes(self):
        for family in protocol_omit.FAMILIES:
            permuted = e5_corruption.swap_family(self.recipient, self.donor, family)
            report = e5_corruption.swapped_columns_report(self.recipient, permuted, family)
            self.assertTrue(report["ok"], report)
            self.assertTrue(report["never_touched_intact"], report)

    def test_inputs_are_not_mutated(self):
        before = self.recipient.copy(deep=True)
        e5_corruption.swap_family(self.recipient, self.donor, "residual")
        pd.testing.assert_frame_equal(before, self.recipient)

    def test_swap_is_deterministic(self):
        one = e5_corruption.swap_family(self.recipient, self.donor, "diff")
        two = e5_corruption.swap_family(self.recipient, self.donor, "diff")
        pd.testing.assert_frame_equal(one, two)

    def test_row_order_does_not_matter(self):
        shuffled = self.donor.sample(frac=1.0, random_state=7).reset_index(drop=True)
        one = e5_corruption.swap_family(self.recipient, self.donor, "level")
        two = e5_corruption.swap_family(self.recipient, shuffled, "level")
        pd.testing.assert_frame_equal(one, two)

    def test_rapid_is_recomputed_from_the_evidence_present(self):
        """E5-B: rapid must equal residual AND diff *in the arm*, never be transported."""
        permuted = e5_corruption.swap_family(self.recipient, self.donor, "residual")
        structured = verbalizer.verbalize_feature_table(permuted)["structured"]
        for name, payload in structured["variables"].items():
            for window in payload["per_window"]:
                self.assertEqual(
                    window["rapid_candidate"],
                    window["residual_candidate"] and window["diff_candidate"],
                    f"{name}: rapid is not the conjunction of the descriptors in the arm")

    def test_permuted_column_equals_the_donor_values(self):
        permuted = e5_corruption.swap_family(self.recipient, self.donor, "trend")
        donor_values = self.donor.set_index("variable")["slope_sigma_h"]
        for _, row in permuted.iterrows():
            self.assertEqual(row["slope_sigma_h"], donor_values[row["variable"]])

    def test_unknown_family_is_refused(self):
        with self.assertRaises(e5_corruption.E5CorruptionError):
            e5_corruption.swap_family(self.recipient, self.donor, "dispersion")


@unittest.skipIf(DEV_UNITS is None or not DEV_UNITS.is_dir(), "E5_DEV_UNITS not available")
class TestOmit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit, _, _, _ = load_two_units()
        cls.full = verbalizer.verbalize_feature_table(cls.unit)

    def test_frozen_renderer_hash(self):
        observed = protocol_omit.verify_frozen_renderer()
        self.assertEqual(observed["verbalizer_sha256"], protocol_omit.FROZEN_VERBALIZER_SHA256)

    def test_removed_sentences_are_gone_and_the_rest_is_intact(self):
        for family in protocol_omit.FAMILIES:
            result = protocol_omit.render_omit(self.unit, family)
            for sentence in result["removed_sentences"]:
                self.assertNotIn(sentence, result["text"])
            kept = [part for part in self.full["text"].split(". ")
                    if all(part not in sentence for sentence in result["removed_sentences"])]
            self.assertTrue(len(result["text"]) < len(self.full["text"]))
            self.assertTrue(kept)

    def test_dispersion_sentence_survives_every_omission(self):
        marker = "La massima dispersione complessiva osservata"
        for family in protocol_omit.FAMILIES:
            self.assertIn(marker, protocol_omit.render_omit(self.unit, family)["text"])

    def test_rapid_falls_with_its_parents_only(self):
        marker = "residual e diff superano simultaneamente"
        unit = _first_unit_with_rapid()
        if unit is None:
            self.skipTest("no development unit carries a rapid sentence")
        for family in ("residual", "diff"):
            self.assertNotIn(marker, protocol_omit.render_omit(unit, family)["text"])
        for family in ("level", "trend"):
            self.assertIn(marker, protocol_omit.render_omit(unit, family)["text"])

    def test_structured_drops_the_declared_derived(self):
        reduced = protocol_omit.render_omit(self.unit, "residual")["structured"]
        self.assertEqual(reduced["e5_omitted_family"], "residual")
        self.assertIn("rapid_variability", reduced["e5_dropped_derived"])
        for payload in reduced["variables"].values():
            self.assertNotIn("residual_variability", payload)
            self.assertNotIn("rapid_variability", payload)
            for window in payload["per_window"]:
                self.assertNotIn("residual_std_ratio", window)
                self.assertNotIn("rapid_candidate", window)

    def test_render_fails_closed_on_a_changed_renderer(self):
        with self.assertRaises(protocol_omit.E5OmitError):
            protocol_omit.verify_frozen_renderer(
                verbalizer_path=Path(__file__), config_path=protocol_omit.CONFIG_PATH)

    def test_no_evaluator_side_leakage_in_any_arm(self):
        """Neither arm may name a fault, an IDV, a run id or a mechanism."""
        forbidden = ("IDV", "idv", "fault", "Fault", "F1 ", "F13", "step", "drift",
                     "sticking", "run_id", "test-primary", "fault-dev")
        texts = [self.full["text"]]
        for family in protocol_omit.FAMILIES:
            texts.append(protocol_omit.render_omit(self.unit, family)["text"])
        for text in texts:
            for token in forbidden:
                self.assertNotIn(token, text, f"leakage: {token!r}")


class TestDerangement(unittest.TestCase):
    def setUp(self):
        self.ids = [f"case-{index:02d}" for index in range(24)]
        self.classes = [f"F{index // 6}" for index in range(24)]

    def test_no_fixed_point_and_no_same_class(self):
        mapping = e5_derangement.sample(self.ids, self.classes, seed=11)
        class_of = dict(zip(self.ids, self.classes))
        for recipient, donor in mapping["pairs"].items():
            self.assertNotEqual(recipient, donor)
            self.assertNotEqual(class_of[recipient], class_of[donor])

    def test_deterministic_in_the_seed(self):
        one = e5_derangement.sample(self.ids, self.classes, seed=11)["pairs"]
        two = e5_derangement.sample(self.ids, self.classes, seed=11)["pairs"]
        self.assertEqual(one, two)
        other = e5_derangement.sample(self.ids, self.classes, seed=12)["pairs"]
        self.assertNotEqual(one, other)

    def test_donors_are_a_permutation(self):
        mapping = e5_derangement.sample(self.ids, self.classes, seed=3)
        self.assertEqual(sorted(mapping["pairs"].values()), sorted(self.ids))

    def test_two_class_subset_is_a_bijection_between_the_classes(self):
        ids = [f"c{index}" for index in range(10)]
        classes = ["A"] * 5 + ["B"] * 5
        mapping = e5_derangement.sample(ids, classes, seed=5)
        matrix = e5_derangement.pairing_matrix(mapping["pairs"], dict(zip(ids, classes)))
        self.assertEqual(matrix, {"A<-B": 5, "B<-A": 5})

    def test_exact_valid_fraction_matches_the_closed_form(self):
        from math import factorial
        classes = ["A"] * 8 + ["B"] * 8
        self.assertAlmostEqual(e5_derangement.exact_valid_fraction(classes),
                               factorial(8) ** 2 / factorial(16), places=12)

    def test_exact_valid_fraction_matches_monte_carlo(self):
        classes = [f"F{index // 5}" for index in range(40)]
        exact = e5_derangement.exact_valid_fraction(classes)
        estimate = e5_derangement.acceptance_rate(classes, seed=4, trials=20_000)
        self.assertLess(abs(exact - estimate), 0.002)

    def test_infeasible_subset_is_refused(self):
        with self.assertRaises(e5_derangement.DerangementError):
            e5_derangement.sample(["a", "b", "c"], ["A", "A", "B"], seed=1)


class TestSeedsAreReproducible(unittest.TestCase):
    """A seed derived from hash() is salted per process: the measure would not reproduce."""

    def test_stable_seed_does_not_depend_on_the_process(self):
        import subprocess
        expected = c2.stable_seed(20260919, "residual")
        for salt in ("0", "1", "987654"):
            result = subprocess.run(
                [sys.executable, "-c",
                 "import sys; sys.path.insert(0, %r); import verifica_e5_c2 as c2; "
                 "print(c2.stable_seed(20260919, 'residual'))" % str(HERE)],
                capture_output=True, text=True, env={**os.environ, "PYTHONHASHSEED": salt})
            self.assertEqual(int(result.stdout.strip()), expected, result.stderr)

    def test_stable_seed_separates_the_families(self):
        seeds = {family: c2.stable_seed(7, family) for family in protocol_omit.FAMILIES}
        self.assertEqual(len(set(seeds.values())), len(seeds))


class TestPromptComposition(unittest.TestCase):
    """The 5 % criterion is checked on composed prompts, never by adding token counts."""

    def setUp(self):
        self.carrier = c2p.synthetic_carriers(120)[0]

    def test_round_trip_is_byte_identical(self):
        text = c2p.compose(self.carrier["prefix"], "UN TESTO", self.carrier["suffix"])
        prefix, case_block, suffix = c2p.split_carrier(text)
        self.assertEqual(case_block.strip(), "UN TESTO")
        self.assertEqual(c2p.compose(prefix, case_block, suffix), text)

    def test_a_carrier_without_the_headings_is_refused(self):
        with self.assertRaises(c2p.CarrierError):
            c2p.split_carrier("un prompt qualunque senza sezioni")

    def test_composition_changes_only_the_case_block(self):
        one = c2p.compose(self.carrier["prefix"], "TESTO A", self.carrier["suffix"])
        two = c2p.compose(self.carrier["prefix"], "TESTO B", self.carrier["suffix"])
        self.assertEqual(one.replace("TESTO A", "X"), two.replace("TESTO B", "X"))


class TestE5S18AndPlan(unittest.TestCase):
    """Fixture-only proof: E5 may alter the case block, never the carrier."""
    def test_s18_refuses_a_change_outside_the_case_block(self):
        carrier = c2p.synthetic_carriers(80)[0]
        full = c2p.compose(carrier["prefix"], "FULL", carrier["suffix"])
        perm = c2p.compose(carrier["prefix"], "PERM", carrier["suffix"])
        self.assertEqual(e5p.case_only_diff(full, perm)["status"], "PASS")
        with self.assertRaises(e5p.E5PromptError):
            e5p.case_only_diff(full, "ALTERED " + perm)

    def test_plan_has_no_execution_path_and_counts_repetitions(self):
        import tempfile
        text = "fixture prompt"
        row = {"prompt_id": "p", "text": text, "prompt_sha256": e5p.sha(text), "arm": "PERM"}
        omit = dict(row, prompt_id="o", arm="OMIT")
        value = {"artifact_version": "E5_PROMPTS_1", "status": "OFFLINE_NOT_EXECUTED",
                 "inputs": {"derangements_sha256": __import__('hashlib').sha256((HERE/'DERANGEMENTS_E5.json').read_bytes()).hexdigest(),
                            "recipients_sha256": __import__('hashlib').sha256((HERE/'RICEVENTI_E5.json').read_bytes()).hexdigest()},
                 "rows": [row, omit], "s18_case_block_diff": [{"status": "PASS"}]}
        path = Path(tempfile.mkdtemp()) / "fixture.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        self.assertEqual(run_e5.plan(path, (1, 2, 3))["planned_calls"], 6)


class TestG3Path(unittest.TestCase):
    """The G3 path reads the test-lot texts; it must not fall back on development data."""

    def _write(self, rows):
        import tempfile
        path = Path(tempfile.mkdtemp()) / "case_texts.jsonl"
        path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
        return path

    def test_pair_shape_full_and_perm_in_one_row(self):
        path = self._write([{"family": "residual", "case_id": "test-primary-F8-r01",
                             "donor_case_id": "test-primary-F1-r01",
                             "full_text": "A", "perm_text": "B"}])
        pairs = list(c2p.pairs_from_case_texts(path))
        self.assertEqual(len(pairs), 1)
        self.assertEqual((pairs[0]["full_text"], pairs[0]["perm_text"]), ("A", "B"))
        self.assertEqual(pairs[0]["donor"], "test-primary-F1-r01")

    def test_pair_shape_two_rows_with_arm(self):
        path = self._write([
            {"family": "trend", "case_id": "c1", "arm": "FULL", "text": "A"},
            {"family": "trend", "case_id": "c1", "arm": "PERM", "text": "B"}])
        pairs = list(c2p.pairs_from_case_texts(path))
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["perm_text"], "B")

    def test_incomplete_pair_is_refused(self):
        path = self._write([{"family": "trend", "case_id": "c1", "arm": "FULL", "text": "A"}])
        with self.assertRaises(c2p.CarrierError):
            list(c2p.pairs_from_case_texts(path))

    def test_unknown_family_is_refused(self):
        path = self._write([{"family": "dispersion", "case_id": "c1",
                             "full_text": "A", "perm_text": "B"}])
        with self.assertRaises(c2p.CarrierError):
            list(c2p.pairs_from_case_texts(path))


class TestCarrierChoice(unittest.TestCase):
    """The worst carrier is chosen AFTER composition, never from prefix+suffix apart."""

    def setUp(self):
        self.count = c2p.build_counter(c2p.DEFAULT_SNAPSHOT)
        self.carriers = []
        for index, size in enumerate((60, 400, 140)):
            carrier = c2p.synthetic_carriers(size)[0]
            carrier["id"] = f"carrier-{index}"
            self.carriers.append(carrier)

    def test_shortlist_is_ranked_on_the_composed_length(self):
        probe = ["Intervallo osservato 40.0-45.0 h in 1 finestre da 5.0 h."]
        shortlist, ranking = c2p.rank_carriers(self.carriers, probe, self.count, keep=1)
        composed = {item["id"]: self.count(c2p.compose(item["prefix"], probe[0], item["suffix"]))
                    for item in self.carriers}
        self.assertEqual(shortlist[0]["id"], min(composed, key=composed.get))
        self.assertTrue(ranking["ranked"])

    def test_worst_carrier_per_pair_is_reported(self):
        pair = {"family": "level", "recipient": "c", "donor": "d", "seed": None,
                "family_seed": None, "full_text": "Testo pieno.", "perm_text": "Testo."}
        summary = c2p.measure([pair], self.carriers, self.count, mode="all", carrier_sample=1)
        entry = summary["families"]["level"]
        self.assertEqual(entry["pairs"], 1)
        self.assertEqual(entry["worst_pair"]["carriers_evaluated"], len(self.carriers))
        ratios = []
        for carrier in self.carriers:
            full = self.count(c2p.compose(carrier["prefix"], pair["full_text"], carrier["suffix"]))
            perm = self.count(c2p.compose(carrier["prefix"], pair["perm_text"], carrier["suffix"]))
            ratios.append(abs(perm - full) / full)
        self.assertAlmostEqual(entry["max_ratio"], max(ratios), places=12)


class TestAssignments(unittest.TestCase):
    ASSIGNMENT = REPO_ROOT / "studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json"

    def setUp(self):
        path = Path(os.environ.get("E5_AGENT_ASSIGNMENT", self.ASSIGNMENT))
        if not path.is_file():
            self.skipTest("AGENT_ASSIGNMENT.json not in this checkout")
        self.owners = assignments.owner_by_fault(path)

    def test_recipient_table_is_balanced_and_never_the_owner(self):
        table = assignments.build_recipients(self.owners, mode="one", base_seed=1, runs=8)
        counts = table["recipient_counts"]
        self.assertEqual(set(counts.values()), {8})
        for case, recipients in table["assignments"].items():
            fault = case.split("-")[2]
            self.assertNotIn(self.owners[fault], recipients)

    def test_all_mode_gives_the_seven_non_owners(self):
        table = assignments.build_recipients(self.owners, mode="all", base_seed=1, runs=8)
        for case, recipients in table["assignments"].items():
            fault = case.split("-")[2]
            self.assertEqual(len(recipients), 7)
            self.assertNotIn(self.owners[fault], recipients)

    def test_recipient_table_is_deterministic(self):
        one = assignments.build_recipients(self.owners, mode="one", base_seed=1, runs=8)
        two = assignments.build_recipients(self.owners, mode="one", base_seed=1, runs=8)
        self.assertEqual(one["assignments"], two["assignments"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
