#!/usr/bin/env python3
"""Read-only checks of the tutorial against saved evidence, not an evaluation.

Standard library only. No workbook, scientific pipeline, network, or output write.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import unittest
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGE = HERE / "fot_walkthrough_part1.html"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.captures = {}
        self.stack = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        capture = attrs.get("id")
        if capture:
            self.ids.append(capture)
        if "data-threshold" in attrs:
            capture = "threshold:" + attrs["data-threshold"]
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append(attrs[attr])
        if capture:
            self.captures[capture] = []
        if tag not in {"meta", "link", "br", "img", "input", "hr"}:
            self.stack.append((tag, capture))

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_data(self, data):
        for _, capture in self.stack:
            if capture:
                self.captures[capture].append(data)

    def text(self, element_id):
        return "".join(self.captures[element_id])


def csv_rows(name):
    with (ROOT / "code/tep_analysis_v2" / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


def normalized(text):
    return " ".join(text.split())


def longest(values):
    best = run = 0
    previous = None
    for value in values:
        run = run + 1 if value and value == previous else int(bool(value))
        best = max(best, run)
        previous = value
    return best


class TutorialChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text()
        cls.page = Page(cls.html)
        cls.data = json.loads(cls.page.text("example-data"))
        cls.config = json.loads((ROOT / "code/verbalizer_config_v2.json").read_text())

    def test_links_and_unique_anchors(self):
        self.assertEqual(len(self.page.ids), len(set(self.page.ids)))
        readme = (HERE / "README.md").read_text()
        links = [(PAGE, link) for link in self.page.links]
        links += [(HERE / "README.md", link) for link in re.findall(r"\]\(([^)]+)\)", readme)]
        for source, link in links:
            with self.subTest(link=link):
                url = urlsplit(link)
                self.assertFalse(url.scheme, "Guide must use local sources only")
                path = (source.parent / unquote(url.path)).resolve() if url.path else source
                self.assertTrue(path.is_file(), path)
                if url.fragment:
                    ids = self.page.ids if path == PAGE else Page(path.read_text()).ids
                    self.assertIn(unquote(url.fragment), ids)

    def test_thresholds_exactly_match_frozen_config(self):
        self.assertEqual(self.data["thresholds"], self.config["thresholds"])
        for key, value in self.config["thresholds"].items():
            self.assertEqual(float(self.page.text("threshold:" + key)), value)

    def test_eight_saved_development_rows(self):
        rows = [r for r in csv_rows("development_window_features.csv")
                if (r["fault"], r["batch"], r["variable"]) == ("1", "1", "XMEAS-1")]
        self.assertEqual(len(rows), 8)
        self.assertEqual(len(self.data["windows"]), 8)
        columns = ["window_start_h", "window_end_h"] + self.data["columns"][2:]
        for actual, saved in zip(self.data["windows"], rows):
            for value, column in zip(actual, columns):
                with self.subTest(window=actual[0], column=column):
                    # CSV and pandas round-trips can differ by one floating-point ULP.
                    self.assertTrue(math.isclose(value, float(saved[column]), rel_tol=1e-12, abs_tol=1e-12))

    def test_static_table_matches_interactive_data(self):
        table = re.search(r'<table id="all-windows">(.*?)</table>', self.html, re.S)[1]
        rows = re.findall(r"<tr>(.*?)</tr>", table, re.S)[1:]
        self.assertEqual(len(rows), 8)
        for i, (row, values) in enumerate(zip(rows, self.data["windows"]), 1):
            cells = re.findall(r"<td>(.*?)</td>", row)
            self.assertEqual(int(cells[0]), i)
            self.assertEqual(cells[1], f"[{values[0]},{values[1]})")
            for text, value in zip(cells[2:], values[2:]):
                self.assertAlmostEqual(float(text.replace("−", "-")), value, delta=0.000501)

    def test_temporal_json_and_saved_counts(self):
        summary = json.loads(self.page.text("summary-json"))
        saved = next(r for r in csv_rows("development_temporal_signatures.csv")
                     if (r["fault"], r["batch"], r["variable"]) == ("1", "1", "XMEAS-1"))
        windows = self.data["windows"]
        for name, column, threshold in [("level", 2, "abs_shift_sigma"), ("trend", 3, "abs_slope_sigma_h")]:
            signs = [(1 if w[column] > 0 else -1) if abs(w[column]) > self.data["thresholds"][threshold] else 0 for w in windows]
            active = [i for i, sign in enumerate(signs) if sign]
            positive, negative = signs.count(1), signs.count(-1)
            expected = dict(n_active_windows=len(active), active_fraction=len(active)/8,
                            positive_count=positive, negative_count=negative,
                            sign_consistency=max(positive, negative)/len(active),
                            longest_same_sign_run=longest(signs),
                            first_active_window=windows[active[0]][0], last_active_window=windows[active[-1]][0],
                            early_active=any(signs[:2]), late_active=any(signs[-2:]))
            self.assertEqual(summary[name], expected)
            self.assertEqual(len(active), int(saved[name + "_positive_windows"]))
            self.assertEqual(longest(signs), int(saved[name + "_max_same_sign_run"]))
        residual = [w[4] > self.data["thresholds"]["residual_std_ratio"] for w in windows]
        diff = [w[5] > self.data["thresholds"]["diff_std_ratio"] for w in windows]
        self.assertEqual(summary["residual_variability"], dict(n_active_windows=sum(residual),
                         active_fraction=sum(residual)/8, longest_run=longest(residual),
                         initial_active_count=sum(residual[:2]), intermediate_active_count=sum(residual[2:-2]),
                         late_active_count=sum(residual[-2:])))
        self.assertEqual(sum(residual), int(saved["residual_positive_windows"]))
        self.assertEqual(sum(diff), int(saved["diff_positive_windows"]))
        self.assertEqual(sum(a and b for a, b in zip(residual, diff)), int(saved["rapid_positive_windows"]))

    def test_neutral_text_is_saved_EXM001(self):
        examples = json.loads((ROOT / "phase_b/local_knowledge/local_examples.json").read_text())
        saved = examples["packs"]["LKP-001"][0]
        self.assertEqual(saved["example_id"], "EXM-001")
        actual = normalized(self.page.text("neutral-text"))
        self.assertEqual(actual, normalized(saved["neutral_text"]))
        for forbidden in ("F1", "batch", "CLS-", ".xlsx", "oscillazione", "drift persistente"):
            self.assertNotIn(forbidden, actual)

    def test_normal_scores_and_calibration_example(self):
        maxima = csv_rows("normal_5h_window_maxima.csv")
        self.assertEqual(len(maxima), 50)
        self.assertEqual({r["normal_block"] for r in maxima}, {"N1", "N2", "N3", "N4", "N5"})
        for column in ("max_abs_shift", "max_abs_slope", "max_residual_ratio", "max_diff_ratio"):
            self.assertIn(maxima[0][column], self.html)
        self.assertEqual(sorted(float(r["max_abs_shift"]) for r in maxima)[48], self.data["thresholds"]["abs_shift_sigma"])
        variables = csv_rows("normal_5h_variable_features.csv")
        first = next(r for r in variables if r["normal_block"] == "N1" and float(r["window_start_h"]) == 0 and r["variable"] == "XMEAS-1")
        self.assertIn(first["shift_sigma"], self.html)

    def test_archived_files_byte_identical(self):
        expected = {
            "fot_7_flow_svg.html": "9178397d2d3e6bb764fbf91814aa468fa5a0a78769dbc12a73dcd355b7412ae8",
            "explain_1.png": "32151e73101f0882abe9fc4f44b9eddb0aab0b3fbf7c70bd3c835ed4d8e0f3bd",
            "explain_2.png": "63a5a7990c85fd7965978ede9967c37b99ba05fbe516fbcba48989a46b9292d6",
        }
        for name, sha in expected.items():
            self.assertEqual(hashlib.sha256((HERE / "archive" / name).read_bytes()).hexdigest(), sha)

    def test_phase_A_frozen_hashes(self):
        expected = {
            "verbalizer_config_v2.json": "552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519",
            "tep_verbalize_v2.py": "3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be",
            "evaluate_verbalizer_v2.py": "972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92",
            "tep_features.py": "cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c",
        }
        for name, sha in expected.items():
            self.assertEqual(hashlib.sha256((ROOT / "code" / name).read_bytes()).hexdigest(), sha)

    def test_scope_and_offline_delivery(self):
        self.assertEqual(len(re.findall(r'<section id=', self.html)), 14)
        self.assertEqual(len(re.findall(r'<summary>\d+\.', self.html)), 10)
        for statement in ("B−A resta il contrasto primario preregistrato", "B−E il contrasto specificity/mechanistic, non primary", "Non applicato a N6–N7", "feasibility gate", "Parte 1", "§15"):
            self.assertIn(statement, self.html)
        self.assertNotRegex(self.html, r'<script[^>]+src=|<iframe|fetch\(|XMLHttpRequest|https?://')


if __name__ == "__main__":
    unittest.main(verbosity=2)
