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
from html import unescape
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGE = HERE / "fot_walkthrough_part1.html"
CONVERSATION = HERE / "fot_walkthrough_conversazione.html"
CONVERSATION_MD = HERE / "fot_walkthrough_conversazione.md"
MAIN_WALKTHROUGH = HERE / "fot_walkthrough.html"
PAPER_BLUEPRINT = HERE / "paper/FoT_TEP_paper_blueprint.html"
ARCHIVE = HERE / "archive"
FIGURES = HERE / "figures"


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
        if not PAGE.is_file():
            raise unittest.SkipTest("legacy part-1 walkthrough is not present in this checkout")
        cls.html = PAGE.read_text()
        cls.page = Page(cls.html)
        cls.data = json.loads(cls.page.text("example-data"))
        cls.config = json.loads((ROOT / "code/verbalizer_config_v2.json").read_text())

    def test_links_and_unique_anchors(self):
        self.assertEqual(len(self.page.ids), len(set(self.page.ids)))
        readme = (ROOT / "README.md").read_text()
        links = [(PAGE, link) for link in self.page.links]
        links += [(ROOT / "README.md", link) for link in re.findall(r"\]\(([^)]+)\)", readme)]
        for source, link in links:
            with self.subTest(link=link):
                url = urlsplit(link)
                if source == ROOT / "README.md" and url.scheme:
                    self.assertIn(url.scheme, {"http", "https"})
                    continue
                self.assertFalse(url.scheme, "Guide must use local sources only")
                path = (source.parent / unquote(url.path)).resolve() if url.path else source
                self.assertTrue(path.exists(), path)
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

    def test_worked_raw_to_shift_calculation(self):
        # Reference values reconstructed read-only from pinned XLSX files;
        # this lightweight regression does not reopen the workbooks.
        expected = {
            "worked-window-n": 300,
            "worked-window-sum": 216.7053282371516,
            "worked-window-mean": 0.7223510941238387,
            "worked-baseline-n": 15000,
            "worked-mu0": 0.26679593084899306,
            "worked-sigma0": 0.005941491332146645,
            "worked-shift": 76.67353831016274,
        }
        actual = {key: float(self.page.text(key)) for key in expected}
        self.assertEqual(actual, expected)
        self.assertEqual(actual["worked-window-n"], 5 * 60)
        self.assertAlmostEqual(actual["worked-window-sum"] / actual["worked-window-n"],
                               actual["worked-window-mean"], places=15)
        result = (actual["worked-window-mean"] - actual["worked-mu0"]) / actual["worked-sigma0"]
        self.assertEqual(result, actual["worked-shift"])
        self.assertEqual(result, self.data["windows"][0][2])
        threshold = float(self.page.text("worked-shift-threshold"))
        self.assertEqual(threshold, self.config["thresholds"]["abs_shift_sigma"])
        self.assertGreater(abs(result), threshold)
        substitution = self.page.text("worked-substitution")
        for key in ("worked-window-mean", "worked-mu0", "worked-sigma0"):
            self.assertIn(self.page.text(key), substitution)

    def test_raw_preview_and_reference_scope(self):
        # First/last three B602:B901 values from mode1_1_1.xlsx, Sheet1.
        reference = [0.2662062165533218, 0.2642580735114897, 0.26587986868132885,
                     1.018144579110935, 1.017490265451267, 1.018570880685642]
        preview = [float(value) for value in re.findall(r"\d+\.\d+", self.page.text("worked-raw-preview"))]
        self.assertEqual(preview, [round(value, 6) for value in reference])
        bridge = normalized(self.page.text("raw-to-shift"))
        for term in ("Runtime / per finestra × XMEAS", "non 300 repliche indipendenti",
                     "ddof=1", "N1–N5", "[0,250)", "B602:B901", "B2:B15001",
                     "non si applica LOBO", "non legge XLSX nel browser"):
            self.assertIn(term, bridge)

    def test_static_flags_match_frozen_comparisons(self):
        table = re.search(r'<table id="window-flags">(.*?)</table>', self.html, re.S)[1]
        rows = re.findall(r"<tr>(.*?)</tr>", table, re.S)[1:]
        self.assertEqual(len(rows), 8)
        keys = ["abs_shift_sigma", "abs_slope_sigma_h", "residual_std_ratio", "diff_std_ratio"]
        counts = [0, 0, 0, 0]
        for index, (row, values) in enumerate(zip(rows, self.data["windows"]), 1):
            cells = re.findall(r"<td>(.*?)</td>", row)
            self.assertEqual(cells[0], f"W{index}")
            actual = [int(cell) for cell in cells[1:]]
            expected = [int((abs(values[2+i]) if i < 2 else values[2+i]) > self.config["thresholds"][key])
                        for i, key in enumerate(keys)]
            self.assertEqual(actual, expected)
            counts = [a + b for a, b in zip(counts, actual)]
        saved = next(r for r in csv_rows("development_temporal_signatures.csv")
                     if (r["fault"], r["batch"], r["variable"]) == ("1", "1", "XMEAS-1"))
        self.assertEqual(counts, [int(saved[feature + "_positive_windows"])
                                 for feature in ("level", "trend", "residual", "diff")])

    def test_pedagogical_bridges_static_and_source_commit_retained(self):
        self.assertEqual(self.page.stack, [], "HTML elements must close cleanly")
        static_html = re.sub(r"<script\b[^>]*>.*?</script>|<noscript>.*?</noscript>|<details>.*?</details>",
                             "", self.html, flags=re.S)
        for element_id in ("raw-to-shift", "worked-shift", "window-flags", "json-rationale",
                           "signature-gloss", "score-gloss"):
            self.assertIn(f'id="{element_id}"', static_html)
        self.assertLess(self.html.index('id="json-rationale"'), self.html.index('id="summary-json"'))
        self.assertLess(self.html.index('id="score-gloss"'), self.html.index("Primo score reale"))
        self.assertIn("non una copia integrale delle serie raw", self.page.text("json-rationale"))
        self.assertIn("non è un'interpretazione LLM", self.page.text("json-rationale"))
        self.assertEqual(self.data["source_commit"], "10acccdd3dd8b8bab9ee0b584c99899d59d8c906")

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
        expected_archive = {
            "fot_7_flow_svg.html": "9178397d2d3e6bb764fbf91814aa468fa5a0a78769dbc12a73dcd355b7412ae8",
        }
        expected_figures = {
            "explain_1.png": "32151e73101f0882abe9fc4f44b9eddb0aab0b3fbf7c70bd3c835ed4d8e0f3bd",
            "explain_2.png": "63a5a7990c85fd7965978ede9967c37b99ba05fbe516fbcba48989a46b9292d6",
        }
        for name, sha in expected_archive.items():
            self.assertEqual(hashlib.sha256((ARCHIVE / name).read_bytes()).hexdigest(), sha)
        for name, sha in expected_figures.items():
            self.assertEqual(hashlib.sha256((FIGURES / name).read_bytes()).hexdigest(), sha)

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


class UnifiedConversationChecks(unittest.TestCase):
    """Regression checks for the complete, unified pedagogical walkthrough."""

    @classmethod
    def setUpClass(cls):
        cls.html = CONVERSATION.read_text()
        cls.markdown = CONVERSATION_MD.read_text()
        cls.page = Page(cls.html)
        cls.text = normalized(unescape(re.sub(r"<[^>]+>", " ", cls.html)))

    def test_valid_markup_links_and_unique_anchors(self):
        self.assertEqual(self.page.stack, [], "HTML elements must close cleanly")
        self.assertEqual(len(self.page.ids), len(set(self.page.ids)))
        for link in self.page.links:
            url = urlsplit(link)
            if url.scheme:
                self.assertIn(url.scheme, {"http", "https"})
                continue
            path = (CONVERSATION.parent / unquote(url.path)).resolve() if url.path else CONVERSATION
            self.assertTrue(path.is_file(), path)
            if url.fragment:
                ids = self.page.ids if path == CONVERSATION else Page(path.read_text()).ids
                self.assertIn(unquote(url.fragment), ids)

        for link in re.findall(r"\]\(([^)]+)\)", self.markdown):
            url = urlsplit(link)
            if url.scheme:
                self.assertIn(url.scheme, {"http", "https"})
                continue
            path = ((CONVERSATION_MD.parent / unquote(url.path)).resolve()
                    if url.path else CONVERSATION_MD)
            self.assertTrue(path.is_file(), path)
            if url.fragment and path.suffix.lower() in {".html", ".htm"}:
                self.assertIn(unquote(url.fragment), Page(path.read_text()).ids)

    def test_one_flow_and_ordered_step_headings(self):
        sections = re.findall(r'<section id="step-(\d+)"[^>]*>(.*?)</section>', self.html, re.S)
        self.assertEqual([int(number) for number, _ in sections], list(range(1, 29)))
        self.assertNotIn("Parte 1 —", self.html)
        self.assertNotIn("Parte 2 —", self.html)
        self.assertIn('<span id="current-step">1</span> / 28', self.html)
        self.assertNotRegex(self.html, r"Step \d+ / (?:17|25|27)")
        self.assertNotRegex(self.markdown, r"Step \d+ / (?:17|25|27)")
        for number, fragment in sections:
            with self.subTest(step=number):
                self.assertEqual(fragment.count("<h2>"), 1)
                self.assertIn(f"Step {number} / 28", fragment)

        markers = list(re.finditer(r"^\*\*Step (\d+) / 28.*?\*\*$",
                                   self.markdown, re.M))
        self.assertEqual([int(marker.group(1)) for marker in markers], list(range(1, 29)))
        for index, marker in enumerate(markers):
            end = markers[index + 1].start() if index + 1 < len(markers) else len(self.markdown)
            fragment = self.markdown[marker.end():end]
            with self.subTest(markdown_step=marker.group(1)):
                self.assertEqual(len(re.findall(r"^## ", fragment, re.M)), 1)

    def test_condition_c_contract_and_caveats(self):
        html_links = {
            "../icl/full_evaluation/evaluation_results_c.json",
            "audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md",
            "../icl/PLAN_CENTRAL_POOLED_ICL.md",
        }
        markdown_links = set(re.findall(r"\]\(([^)]+)\)", self.markdown))
        for link in html_links:
            with self.subTest(link=link):
                self.assertIn(f'href="{link}"', self.html)
                self.assertIn(link, markdown_links)

        required = (
            "15 / 15", "12 / 12", "3 / 3", "5/36", "0.138889",
            "0.083333", "0.166667", "10.000", "20260906",
            "GO WITH LIMITATIONS", "CLS-OJNSG", "soli cinque valori",
            "temperature=null", "seed=null", "inferenza stateless",
            "senza astensioni", "non un risultato empiricamente misurato",
            "centralized full-information pooled ICL post-hoc exploratory reference",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.html)
                self.assertIn(phrase, self.text)
                self.assertIn(phrase, self.markdown)

        for document in (self.html, self.markdown):
            self.assertIn("Per ciascuno dei 15 casi, le tre ripetizioni hanno prodotto la stessa decisione aggregabile.", document)
            self.assertIn("gli altri nove casi fault", document)
            self.assertIn("EXP3_V2 non comprende una propria baseline centralized pooled", document)

    def test_forbidden_condition_c_formulations_absent(self):
        forbidden = (
            "A rappresenta esattamente il modello local-only",
            "a pari informazione",
            "equal-information",
            "stesso seed di ragionamento",
            "stessa temperatura",
            "selezionati dallo schedule",
            "45 ripetizioni unanimi",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.html)
                self.assertNotIn(phrase, self.markdown)

    def test_real_reduced_example_and_calibration(self):
        config = json.loads((ROOT / "code/verbalizer_config_v2.json").read_text())
        expected = {
            "worked-window-n": 300,
            "worked-window-sum": 216.7053282371516,
            "worked-window-mean": 0.7223510941238387,
            "worked-baseline-n": 15000,
            "worked-mu0": 0.26679593084899306,
            "worked-sigma0": 0.005941491332146645,
            "worked-shift": 76.67353831016274,
            "worked-shift-threshold": 1.9695333234149084,
        }
        self.assertEqual({key: float(self.page.text(key)) for key in expected}, expected)
        self.assertEqual(expected["worked-shift-threshold"], config["thresholds"]["abs_shift_sigma"])
        maxima = csv_rows("normal_5h_window_maxima.csv")
        ordered = sorted(float(row["max_abs_shift"]) for row in maxima)
        self.assertEqual(ordered[48], expected["worked-shift-threshold"])
        self.assertEqual(ordered[49], 2.0050511992352518)
        self.assertNotIn("TEST_POTENZA", self.html)
        self.assertNotIn("TEST_PAZZIA", self.html)
        self.assertNotIn("fantasia", self.html.lower())

    def test_json_and_neutral_text_are_real_pair(self):
        summary = json.loads(self.page.text("summary-json"))
        self.assertEqual(summary["variable"], "XMEAS-1")
        self.assertEqual(summary["level"]["n_active_windows"], 8)
        examples = json.loads((ROOT / "phase_b/local_knowledge/local_examples.json").read_text())
        saved = examples["packs"]["LKP-001"][0]
        self.assertEqual(saved["example_id"], "EXM-001")
        self.assertEqual(normalized(self.page.text("neutral-text")), normalized(saved["neutral_text"]))

    def test_real_heldout_A_B_E_case(self):
        records = [json.loads(line) for line in
                   (ROOT / "phase_b/final_evaluation/inference/aggregate_records.jsonl").read_text().splitlines()]
        expected = {"A": (None, True), "B": ("CLS-ZOGAA", False), "E": ("CLS-OJNSG", False)}
        for condition, outcome in expected.items():
            record = next(row for row in records if row["physical_case_id"] == "PBH-004"
                          and row["agent_id"] == "agent_3" and row["condition"] == condition)
            parsed = record["parsed_output"]
            self.assertEqual((parsed["predicted_label"], parsed["abstain"]), outcome)
            self.assertEqual(len(record["repetition_outcomes"]), 3)
        for phrase in ("PBH-004", "Agent 3", "mode1_1_11.xlsx", "used_insight_ids=[]",
                       "B−A", "endpoint primario", "B−E",
                       "contrasto sulla pertinenza dell'informazione pre-specificato"):
            self.assertIn(phrase, self.text)

    def test_collapsible_navigation_and_progressive_layout(self):
        for phrase in ('id="nav-toggle"', 'aria-controls="guide-nav"', 'aria-expanded="true"',
                       "Nascondi indice", "Mostra indice", "nav-collapsed", "nav-open",
                       "Escape", "IntersectionObserver", 'id="current-step"'):
            self.assertIn(phrase, self.html)
        self.assertIn("body.nav-collapsed .layout{grid-template-columns:0 minmax(0,1fr)", self.html)
        self.assertIn("@media(max-width:900px)", self.html)
        self.assertNotIn("grid-template-columns:repeat(2", self.html)

    def test_step27_qwen_protocol_stable_facts(self):
        """Stable facts from the frozen Qwen protocol (commit d9bb95c).

        These values come from the capability probe and config.json
        and will not change after the full run completes.
        Do NOT add transient state (e.g. "run in corso") here.
        """
        # ---- present in both HTML and Markdown ----
        for document_label, document in (("html", self.html), ("md", self.markdown)):
            with self.subTest(doc=document_label):
                # frozen commit
                self.assertIn("d9bb95c", document)
                # model identity
                self.assertIn("Qwen3.8-27B-FP8", document)
                # vLLM version
                self.assertIn("0.28.0", document)
                # experiment structure
                self.assertIn("540", document)       # 540 inferences
                self.assertIn("180", document)        # 180 aggregate decisions
                # token budget from config.json
                self.assertIn("1536", document)       # max_tokens
                self.assertIn("1024", document)       # thinking_token_budget
                # context window
                self.assertIn("4096", document)       # max_model_len
                # correct prompt token count from probe
                self.assertIn("2340", document)       # max raw prompt tokens
                # probe result
                self.assertIn("19/19", document)      # all 19 checks pass
                # conditions
                self.assertIn("A/B/E", document)
                # determinism
                self.assertIn("temperature", document)
                self.assertIn("seed", document)

        # ---- forbidden invented metrics ----
        for document_label, document in (("html", self.html), ("md", self.markdown)):
            with self.subTest(doc=document_label, check="no invented metrics"):
                # The re-audit originally had an erroneous prompt token count;
                # ensure it never leaks into the walkthrough
                self.assertNotIn("max_prompt_tokens: 3876", document)
                self.assertNotIn("totale di ~5000", document)

        # ---- HTML-specific structure ----
        import re
        step27 = re.search(r'<section id="step-27"[^>]*>(.*?)</section>', self.html, re.S)
        self.assertIsNotNone(step27, "step-27 section must exist")
        s27 = step27.group(1)
        # exactly one H2
        self.assertEqual(s27.count("<h2>"), 1)
        # step kicker present
        self.assertIn("Step 27 / 28", s27)
        # phase badge
        self.assertIn("phase-badge", s27)
        # Frozen lane links are now canonical and checked by test_links_and_assets.
        self.assertIn("../phase_b/exp2/qwen/evaluation/EVALUATION_REPORT.md", s27)

    def test_step27_qwen_frozen_results_and_limitations(self):
        required = (
            "0/36", "34/36", "1/36", "94.44%", "2.78%",
            "0.944444", "0.916667", "0.833333", "34 helped",
            "0 harmed", "2 unchanged-incorrect", "zero astensioni",
            "C1–C4: 4/4 PASS", "H2", "controllo secondario distinto",
            "local-seen", "75%", "91.67%", "41.67%",
            "GO WITH LIMITATIONS", "1023 token", "budget nominale di 1024",
            "36 aggregati B non cappati sono corretti", "CLS-OJNSG",
            "CLS-Z3ISU", "un solo consumer open-weight",
            "non è una replica end-to-end interamente open-weight",
            "confronto cross-model è descrittivo", "non dimostra portabilità universale",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.text)
                self.assertIn(phrase, self.markdown)

        tags_and_commits = {
            "phase-b-exp2-qwen-protocol-frozen-001": "d9bb95c31bdeb2f1608aaedc52f25b98de9bbf96",
            "phase-b-exp2-qwen-predictions-frozen-001": "a4f264c210873536c989ebd99aa2c6cf9857c85c",
            "phase-b-exp2-qwen-evaluator-frozen-001": "a8f9884dfe2150a89131ba604b34ff1f6914f6e9",
            "phase-b-exp2-qwen-results-frozen-001": "37195cf2c5076b5da724b857f10e157177654cac",
        }
        for tag, commit in tags_and_commits.items():
            self.assertIn(tag, self.html)
            self.assertIn(tag, self.markdown)
            self.assertIn(commit, self.html)
            self.assertIn(commit, self.markdown)

        links = (
            "../phase_b/exp2/qwen/evaluation/EVALUATION_REPORT.md",
            "../phase_b/exp2/qwen/evaluation/evaluation_results.json",
            "audits/EXP2_QWEN_EVALUATOR_REVIEW.md",
            "audits/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md",
        )
        markdown_links = set(re.findall(r"\]\(([^)]+)\)", self.markdown))
        for link in links:
            self.assertIn(f'href="{link}"', self.html)
            self.assertIn(link, markdown_links)

        obsolete = (
            "full run attualmente in esecuzione",
            "inferenza è ancora in corso",
            "non esistono ancora risultati del full run",
            "nessun risultato scientifico ancora disponibile",
            "EXP2 Qwen da completare",
            "EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW" + ".md",
        )
        for phrase in obsolete:
            self.assertNotIn(phrase.lower(), self.text.lower())
            self.assertNotIn(phrase.lower(), self.markdown.lower())

    def test_active_readme_publishes_main_guide_and_artifacts_exist(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn("docs/fot_walkthrough_conversazione.html", readme)
        self.assertTrue(CONVERSATION.is_file())
        self.assertTrue(CONVERSATION_MD.is_file())


class C02bDocumentationChecks(unittest.TestCase):
    """Keep the three walkthroughs aligned with the frozen C02b artifacts."""

    @classmethod
    def setUpClass(cls):
        cls.conversation_html = CONVERSATION.read_text(encoding="utf-8")
        cls.conversation_md = CONVERSATION_MD.read_text(encoding="utf-8")
        cls.main_html = MAIN_WALKTHROUGH.read_text(encoding="utf-8")
        cls.result_path = (
            ROOT
            / "phase_b/baselines/c02b_shared_numeric_prototypes/results/metrics.json"
        )
        cls.results = json.loads(cls.result_path.read_text(encoding="utf-8"))
        cls.suite_result_path = (
            ROOT
            / "phase_b/baselines/c02b_supervisor_model_suite/results/metrics.json"
        )
        cls.suite_results = json.loads(
            cls.suite_result_path.read_text(encoding="utf-8")
        )
        cls.paper_blueprint = PAPER_BLUEPRINT.read_text(encoding="utf-8")

    def test_artifact_values_and_status(self):
        shared = self.results["metrics"]["shared_prototypes"]
        self.assertEqual(shared["overall"]["correct"], 60)
        self.assertEqual(shared["local_unseen"]["correct"], 36)
        self.assertEqual(self.results["c02b_status"], "MITIGATA")
        self.assertEqual(self.results["communication"]["total_payload_bytes"], 67020)

    def test_three_walkthroughs_report_same_c02b_outcome(self):
        documents = (
            self.conversation_html,
            self.conversation_md,
            self.main_html,
        )
        for document in documents:
            with self.subTest(document=document[:40]):
                self.assertIn("36/36", document)
                self.assertIn("31/36", document)
                self.assertIn("67.020", document)
                self.assertIn("Mitigata", document)
                self.assertIn("prototipi condivisi", document.lower())
                self.assertNotIn("C02b resta aperta", document)

    def test_html_is_balanced_and_main_step_contract_matches(self):
        for path in (CONVERSATION, MAIN_WALKTHROUGH):
            page = Page(path.read_text(encoding="utf-8"))
            self.assertEqual(page.stack, [], str(path))
            self.assertEqual(len(page.ids), len(set(page.ids)), str(path))
        main = self.main_html
        containers = re.findall(r'<div class="step-container" data-step="(\d+)">', main)
        self.assertEqual([int(value) for value in containers], list(range(23)))
        steps_literal = re.search(r"const STEPS = \[(.*?)\];", main, re.S).group(1)
        self.assertEqual(steps_literal.count("{phase:"), len(containers))

    def test_supervisor_model_suite_values_and_documentation(self):
        expected = {
            "adaboost": 15,
            "random_forest": 15,
            "mlp": 15,
            "linear_elastic_net": 15,
            "knn": 15,
            "lstm_causal_attention": 15,
            "bilstm_attention": 14,
            "multimodal_bilstm_attention_tfidf": 14,
        }
        self.assertEqual(set(self.suite_results["metrics"]), set(expected))
        for model, correct in expected.items():
            self.assertEqual(
                self.suite_results["metrics"][model]["physical_cases"]["correct"],
                correct,
            )
        documents = (
            self.conversation_html,
            self.conversation_md,
            self.main_html,
            self.paper_blueprint,
        )
        for document in documents:
            with self.subTest(document=document[:40]):
                for term in (
                    "AdaBoost",
                    "Random Forest",
                    "MLP",
                    "elastic-net",
                    "k-NN",
                    "LSTM",
                    "BiLSTM",
                    "multimodale",
                ):
                    self.assertIn(term, document)
                self.assertIn("15/15", document)
                self.assertIn("14/15", document)
                self.assertIn("centralizz", document.lower())



class Exp2QwenDocumentStatusChecks(unittest.TestCase):
    """Regression: Exp 2 Qwen must be registered as completed in canonical
    planning and literature review documents (P2 fix).

    Tests are multiline-safe: context windows operate on the full text,
    not individual lines, so a keyword split across lines is still caught.
    """

    LIT_REVIEW = ROOT / 'docs' / 'lit_review' / 'FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md'
    EXP_PLAN = ROOT / 'docs' / 'lit_review' / 'FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md'

    @classmethod
    def setUpClass(cls):
        cls.lit_review = cls.LIT_REVIEW.read_text()
        cls.exp_plan = cls.EXP_PLAN.read_text()

    # ---- No remaining in-progress references to Exp 2 (multiline-safe) ----

    def _assert_no_exp2_in_corso(self, text, filename):
        """Sliding window on full text: catches keywords even across lines."""
        low = text.lower()
        start = 0
        while True:
            idx = low.find('in corso', start)
            if idx == -1:
                break
            ctx = low[max(0, idx - 400):min(len(low), idx + 400)]
            for kw in ('exp 2', 'qwen', 'secondo llm', '540 inferenz'):
                self.assertNotIn(kw, ctx,
                    f'{filename} offset {idx}: Exp 2 still referenced as in corso')
            start = idx + 1

    def test_lit_review_no_exp2_in_corso(self):
        self._assert_no_exp2_in_corso(self.lit_review, 'LITERATURE_REVIEW')

    def test_exp_plan_no_exp2_in_corso(self):
        self._assert_no_exp2_in_corso(self.exp_plan, 'EXPERIMENT_PLAN')

    def _assert_no_exp2_avviato(self, text, filename):
        low = text.lower()
        start = 0
        while True:
            idx = low.find('avviato', start)
            if idx == -1:
                break
            ctx = low[max(0, idx - 400):min(len(low), idx + 400)]
            for kw in ('exp 2', 'qwen', '540 inferenz'):
                self.assertNotIn(kw, ctx,
                    f'{filename} offset {idx}: Exp 2 still referenced as avviato')
            start = idx + 1

    def test_lit_review_no_exp2_avviato(self):
        self._assert_no_exp2_avviato(self.lit_review, 'LITERATURE_REVIEW')

    def test_exp_plan_no_exp2_avviato(self):
        self._assert_no_exp2_avviato(self.exp_plan, 'EXPERIMENT_PLAN')

    # ---- Key completed-status markers present ----

    def test_lit_review_completed_markers(self):
        for marker in (
            'COMPLETATO',
            'GO WITH LIMITATIONS',
            '0.944444',
            'Rev. 3',
            'phase-b-exp2-qwen-results-frozen-001',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.lit_review)

    def test_exp_plan_completed_markers(self):
        for marker in (
            'COMPLETATO',
            'GO WITH LIMITATIONS',
            '0.944444',
            'Rev. 4',
            'phase-b-exp2-qwen-results-frozen-001',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.exp_plan)

    # ---- Frozen chain tags present ----

    def _check_frozen_chain(self, text, filename):
        tags = {
            'phase-b-exp2-qwen-protocol-frozen-001': 'd9bb95c',
            'phase-b-exp2-qwen-predictions-frozen-001': 'a4f264c',
            'phase-b-exp2-qwen-evaluator-frozen-001': 'a8f9884',
            'phase-b-exp2-qwen-results-frozen-001': '37195cf',
        }
        for tag, commit_prefix in tags.items():
            with self.subTest(tag=tag, file=filename):
                self.assertIn(commit_prefix, text,
                    f'{filename}: frozen chain commit prefix {commit_prefix} missing')

    def test_lit_review_frozen_chain(self):
        self._check_frozen_chain(self.lit_review, 'LITERATURE_REVIEW')

    def test_exp_plan_frozen_chain(self):
        self._check_frozen_chain(self.exp_plan, 'EXPERIMENT_PLAN')

    # ---- P1: correct seed value (20260829, not 42) ----

    def test_no_seed_42_in_exp_plan(self):
        self.assertNotIn('seed=42', self.exp_plan,
            'EXPERIMENT_PLAN still contains erroneous seed=42')

    def test_no_seed_42_in_lit_review(self):
        self.assertNotIn('seed=42', self.lit_review,
            'LITERATURE_REVIEW still contains erroneous seed=42')

    def test_correct_seed_present_exp_plan(self):
        self.assertIn('seed=20260829', self.exp_plan,
            'EXPERIMENT_PLAN missing correct seed=20260829')

    # ---- P1: C2/C4 criteria mapping ----

    def test_exp_plan_b_minus_e_not_mapped_to_c2(self):
        """B−E supports C4 (delta_unseen > delta_E), not C2
        (positive delta in ≥3/4 agents)."""
        import re
        # Find any table row where B−E and C2 appear together
        for line in self.exp_plan.split('\n'):
            if 'B−E' in line and '|' in line:
                self.assertNotIn('C2 PASS', line,
                    'B−E is mapped to C2 but should be C4')

    # ---- P2: B error count and description ----

    def test_exp_plan_b_errors_count_accurate(self):
        """Must mention 5 B errors, not 2."""
        self.assertIn('5 errori B', self.exp_plan,
            'EXPERIMENT_PLAN must state 5 total B errors')

    def test_exp_plan_b_error_pattern_complete(self):
        """All three error types must be listed."""
        low = self.exp_plan.lower()
        for pattern in ('ojnsg', 'z3isu', 'zogaa'):
            with self.subTest(pattern=pattern):
                self.assertIn(pattern, low,
                    f'EXPERIMENT_PLAN missing error class {pattern}')

    def test_exp_plan_capped_errors_noted(self):
        """The relationship between B errors and the 1023-token cap
        must be documented."""
        low = self.exp_plan.lower()
        # Check that the cap-error relationship is mentioned
        self.assertIn('cap', low)
        self.assertIn('36', self.exp_plan)  # 36 uncapped aggregates

    # ---- P2: B error analysis present in literature review too ----

    def test_lit_review_b_errors_and_cap(self):
        """Literature review must document: all 5 B errors at cap,
        36 uncapped correct, H2 confounded, B/E matched."""
        low = self.lit_review.lower()
        self.assertIn('5 errori', low,
            'LITERATURE_REVIEW must state 5 B errors')
        self.assertIn('36', self.lit_review,
            'LITERATURE_REVIEW must mention 36 uncapped aggregates')
        for kw in ('cap', 'matched', 'citation rate'):
            with self.subTest(kw=kw):
                self.assertIn(kw, low,
                    f'LITERATURE_REVIEW missing B error analysis keyword: {kw}')

    # ---- P2: submission readiness is PLAUSIBLE, not SOLID ----

    def test_lit_review_not_solid(self):
        """Walkthrough says PLAUSIBLE (limite alto). SOLID is unjustified."""
        import re
        # Must not contain "readiness: SOLID" or "readiness:SOLID"
        matches = re.findall(r'readiness[:\s]+SOLID', self.lit_review,
                             re.IGNORECASE)
        self.assertEqual(matches, [],
            f'LITERATURE_REVIEW contains unjustified SOLID: {matches}')

    def test_lit_review_plausible(self):
        self.assertIn('PLAUSIBLE', self.lit_review,
            'LITERATURE_REVIEW must preserve PLAUSIBLE readiness')

    # ---- P3: unversioned references annotated AND non-clickable ----

    def test_p3_phase_b_design_v1_annotated_and_not_linked(self):
        doc_index = (ROOT / 'DOCUMENTATION_INDEX.md').read_text()
        sr_readme = (ROOT / 'supporting_records' / 'README.md').read_text()
        # Annotation present
        self.assertIn('not git-tracked', doc_index)
        self.assertIn('not git-tracked', sr_readme)
        # Link syntax removed: no [...](...PHASE_B_EXPERIMENT_DESIGN.md)
        import re
        for name, text in [('DOCUMENTATION_INDEX', doc_index),
                           ('supporting_records/README', sr_readme)]:
            clickable = re.findall(
                r'\[.*?PHASE_B_EXPERIMENT_DESIGN\.md.*?\]\(', text)
            self.assertEqual(clickable, [],
                f'{name} still has clickable link to non-tracked file: {clickable}')

    def test_p3_xlsx_annotated_and_not_linked(self):
        lr_readme = (ROOT / 'docs' / 'lit_review' / 'README.md').read_text()
        self.assertIn('not git-tracked', lr_readme)
        import re
        clickable = re.findall(
            r'\[.*?FoT_literature_review\.xlsx.*?\]\(', lr_readme)
        self.assertEqual(clickable, [],
            f'docs/lit_review/README still has clickable link to non-tracked xlsx: {clickable}')


if __name__ == "__main__":
    unittest.main(verbosity=2)
